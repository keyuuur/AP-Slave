from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
from pathlib import Path
import socket
import yaml

import pytest

from ap_slave_runtime.engine import evaluate_manual_promotion
from ap_slave_runtime.models import ManualPromoEvaluation

from tests.runtime.factories import (
    NOW,
    candidate,
    evidence,
    market_identity,
    request_payload,
    write_runtime_contracts,
)


def _evaluate(payload: dict, tmp_path: Path):
    request = ManualPromoEvaluation.model_validate(payload)
    catalog_path, registry_path = write_runtime_contracts(tmp_path, request)
    return evaluate_manual_promotion(request, catalog_path, registry_path)


def _candidate_codes(brief, index: int = 0) -> set[str]:
    return set(brief.candidates[index].reason_codes)


@pytest.mark.parametrize(
    ("american_odds", "expected_boosted"),
    [(-150, Decimal("1.866666666666666666666666667")), (150, Decimal("2.95"))],
)
def test_positive_and_negative_american_odds_use_profit_only_formula(
    american_odds: int,
    expected_boosted: Decimal,
    tmp_path: Path,
) -> None:
    payload = request_payload(candidates=[candidate(target_odds=american_odds)])
    brief = _evaluate(payload, tmp_path)

    assert brief.candidates[0].boosted_decimal_odds == expected_boosted
    assert brief.candidates[0].break_even_probability == Decimal(1) / expected_boosted


@pytest.mark.parametrize("boost_percent", [None, "0", "-0.01"])
def test_missing_zero_or_negative_boost_fails_closed(
    boost_percent: str | None,
    tmp_path: Path,
) -> None:
    brief = _evaluate(request_payload(boost_percent=boost_percent), tmp_path)

    assert "PROMO_TERMS_AMBIGUOUS" in _candidate_codes(brief)
    assert brief.candidates[0].estimated_probability is None
    assert brief.candidates[0].ev_per_unit is None


def test_each_book_is_devigged_before_unweighted_mean(tmp_path: Path) -> None:
    brief = _evaluate(request_payload(), tmp_path)
    decision = brief.candidates[0]
    probabilities = [row.fair_probability for row in decision.consensus_audit.source_level_probabilities]

    assert abs(probabilities[0] - Decimal(12) / Decimal(23)) <= Decimal("1e-27")
    assert abs(probabilities[1] - Decimal("0.5")) <= Decimal("1e-27")
    assert abs(decision.estimated_probability - Decimal(47) / Decimal(92)) <= Decimal(
        "1e-27"
    )
    assert decision.consensus_audit.aggregation_method_version == "mlb_market_consensus_mean_v1"


def test_target_and_duplicate_origin_are_excluded_without_inflating_coverage(
    tmp_path: Path,
) -> None:
    row = candidate()
    target_copy = deepcopy(row["comparison_pairs"][0])
    target_copy.update(
        source_id="sportsbook_comparison_manual_evidence",
        sportsbook_id="FanDuel",
        pricing_origin_id="sportsbook_fanduel",
        evidence_id="evidence:target-as-comparison",
    )
    duplicate_origin = deepcopy(row["comparison_pairs"][0])
    duplicate_origin.update(
        sportsbook_id="Comparison A Skin",
        evidence_id="evidence:comparison-alias",
    )
    row["comparison_pairs"].extend([target_copy, duplicate_origin])
    row["evidence"].extend(
        [
            evidence(
                target_copy["evidence_id"],
                target_copy["source_id"],
                NOW,
            ),
            evidence(
                duplicate_origin["evidence_id"],
                duplicate_origin["source_id"],
                NOW,
            ),
        ]
    )

    decision = _evaluate(request_payload(candidates=[row]), tmp_path).candidates[0]

    assert decision.consensus_audit.raw_source_count == 4
    assert decision.consensus_audit.usable_book_count == 2
    assert decision.consensus_audit.pricing_origin_group_count == 2
    assert decision.consensus_audit.target_excluded is True
    assert len(decision.consensus_audit.excluded_sources) == 2
    assert all(
        "PRICING_ORIGIN_UNRESOLVED" in excluded.reason_codes
        for excluded in decision.consensus_audit.excluded_sources
    )


def test_aliases_from_one_origin_do_not_satisfy_two_origin_minimum(tmp_path: Path) -> None:
    row = candidate()
    alias = deepcopy(row["comparison_pairs"][0])
    alias.update(
        sportsbook_id="Comparison A Skin",
        evidence_id="evidence:comparison-alias",
    )
    row["comparison_pairs"] = [row["comparison_pairs"][0], alias]
    row["evidence"].append(
        evidence(alias["evidence_id"], alias["source_id"], NOW)
    )

    decision = _evaluate(request_payload(candidates=[row]), tmp_path).candidates[0]

    assert decision.consensus_audit.pricing_origin_group_count == 1
    assert "PRICING_ORIGIN_UNRESOLVED" in decision.reason_codes
    assert "CONSENSUS_INSUFFICIENT" in decision.reason_codes
    assert decision.estimated_probability is None


@pytest.mark.parametrize("evidence_kind", ["target", "comparison"])
def test_unreviewed_source_permission_never_clears_a_pricing_gate(
    evidence_kind: str,
    tmp_path: Path,
) -> None:
    row = candidate()
    evidence_index = 0 if evidence_kind == "target" else 1
    row["evidence"][evidence_index]["source_permission_reviewed"] = False

    decision = _evaluate(request_payload(candidates=[row]), tmp_path).candidates[0]

    assert "SCREENSHOT_VERIFICATION_REQUIRED" in decision.reason_codes
    assert decision.ev_per_unit is None


def test_stale_target_fails_before_valuation(tmp_path: Path) -> None:
    decision = _evaluate(
        request_payload(candidates=[candidate(target_age_seconds=181)]), tmp_path
    ).candidates[0]

    assert "TARGET_QUOTE_STALE" in decision.reason_codes
    assert decision.ev_per_unit is None


@pytest.mark.parametrize(
    ("mutation", "expected_codes"),
    [
        ("stale", {"COMPARISON_QUOTE_STALE", "CONSENSUS_INSUFFICIENT"}),
        ("suspended", {"MARKET_SUSPENDED", "CONSENSUS_INSUFFICIENT"}),
        ("incomplete", {"OUTCOME_SET_INCOMPLETE", "CONSENSUS_INSUFFICIENT"}),
    ],
)
def test_unusable_comparison_pairs_are_excluded(
    mutation: str,
    expected_codes: set[str],
    tmp_path: Path,
) -> None:
    row = candidate()
    if mutation == "stale":
        row["comparison_pairs"][0]["retrieved_at_utc"] = "2026-07-14T03:54:59Z"
    elif mutation == "suspended":
        row["comparison_pairs"][0]["market_status"] = "suspended"
    else:
        row["comparison_pairs"][0]["market_identity"][
            "outcome_set_completeness"
        ] = "incomplete"

    decision = _evaluate(request_payload(candidates=[row]), tmp_path).candidates[0]

    assert expected_codes <= set(decision.reason_codes)
    assert decision.consensus_audit.usable_book_count == 1
    assert decision.estimated_probability is None


def test_collection_skew_over_300_seconds_fails_closed(tmp_path: Path) -> None:
    row = candidate(target_age_seconds=0, comparison_age_seconds=(300, 10))
    row["target_quote"]["retrieved_at_utc"] = "2026-07-14T04:00:01Z"

    decision = _evaluate(request_payload(candidates=[row]), tmp_path).candidates[0]

    assert "QUOTE_BATCH_UNSYNCHRONIZED" in decision.reason_codes
    assert decision.consensus_audit.collection_skew_seconds == 301
    assert decision.ev_per_unit is None


@pytest.mark.parametrize(
    ("field", "value", "expected_code"),
    [
        ("canonical_market_key", "mlb.player_total_bases", "SETTLEMENT_RULE_MISMATCH"),
        ("period", "first_five", "SETTLEMENT_RULE_MISMATCH"),
        ("overtime_or_extra_innings_treatment", "excluded", "SETTLEMENT_RULE_MISMATCH"),
        ("push_behavior", "push", "SETTLEMENT_RULE_MISMATCH"),
        ("settlement_rule", "regulation only", "SETTLEMENT_RULE_MISMATCH"),
    ],
)
def test_comparison_identity_and_settlement_mismatches_are_excluded(
    field: str,
    value: str,
    expected_code: str,
    tmp_path: Path,
) -> None:
    row = candidate()
    row["comparison_pairs"][0]["market_identity"][field] = value

    decision = _evaluate(request_payload(candidates=[row]), tmp_path).candidates[0]

    assert expected_code in decision.reason_codes
    assert "CONSENSUS_INSUFFICIENT" in decision.reason_codes
    assert decision.ev_per_unit is None


def test_candidate_period_overtime_and_push_mismatches_fail_exact_identity(
    tmp_path: Path,
) -> None:
    identity = market_identity(
        period="regulation",
        overtime="excluded",
        push_behavior="push",
    )
    decision = _evaluate(
        request_payload(candidates=[candidate(identity=identity)]), tmp_path
    ).candidates[0]

    assert {
        "MARKET_IDENTITY_MISMATCH",
        "SETTLEMENT_RULE_MISMATCH",
        "PUSH_MODEL_UNAVAILABLE",
    } <= set(decision.reason_codes)
    assert decision.ev_per_unit is None


def test_material_context_newer_than_any_quote_requires_synchronization(
    tmp_path: Path,
) -> None:
    row = candidate()
    fact_time = NOW.replace(second=55) - __import__("datetime").timedelta(minutes=1)
    fact_id = "evidence:material-change"
    row["material_context"] = [
        {
            "fact_id": "fact-1",
            "signal_id": "mlb_starting_lineup",
            "source_id": "mlb_official_starting_lineups",
            "effective_at_utc": fact_time.isoformat().replace("+00:00", "Z"),
            "captured_at_utc": fact_time.isoformat().replace("+00:00", "Z"),
            "verification_status": "confirmed",
            "material": True,
            "summary": "Confirmed batting-order change",
            "evidence_id": fact_id,
        }
    ]
    row["latest_material_context_at_utc"] = fact_time.isoformat().replace(
        "+00:00", "Z"
    )
    row["evidence"].append(
        evidence(fact_id, "mlb_official_starting_lineups", fact_time)
    )

    decision = _evaluate(request_payload(candidates=[row]), tmp_path).candidates[0]

    assert "MATERIAL_CONTEXT_NEWER_THAN_QUOTES" in decision.reason_codes
    assert decision.monitoring_metadata.post_material_change_synchronized is False
    assert decision.estimated_probability is None


def test_promotion_expiry_short_circuits_before_candidate_valuation(tmp_path: Path) -> None:
    payload = request_payload(candidates=[candidate(target_odds=-250)])
    payload["promotion"]["expires_at_utc"] = payload["created_at_utc"]

    decision = _evaluate(payload, tmp_path).candidates[0]

    assert decision.reason_codes == ["PROMO_EXPIRED"]
    assert decision.state == "ineligible"
    assert decision.ev_per_unit is None
    assert decision.consensus_audit.source_level_probabilities == []


def test_minimum_odds_failure_blocks_candidate_valuation(tmp_path: Path) -> None:
    payload = request_payload(candidates=[candidate(target_odds=-250)])

    decision = _evaluate(payload, tmp_path).candidates[0]

    assert "PROMO_MIN_ODDS_FAIL" in decision.reason_codes
    assert decision.state == "ineligible"
    assert decision.ev_per_unit is None


def test_non_base_odds_range_basis_fails_closed(tmp_path: Path) -> None:
    payload = request_payload()
    payload["promotion"]["odds_range_basis"] = "unknown"

    decision = _evaluate(payload, tmp_path).candidates[0]

    assert "PROMO_TERMS_AMBIGUOUS" in decision.reason_codes
    assert decision.ev_per_unit is None


@pytest.mark.parametrize(
    ("adapter_id", "version", "profile_id", "league", "line"),
    [
        ("nba.pregame_full_game_v0_1", "0.1.1", "nba.full_game.moneyline", "NBA", None),
        ("nfl.pregame_full_game_v0_1", "0.1.1", "nfl.full_game.moneyline", "NFL", None),
        ("golf.pregame_stroke_play_v0_1", "0.1.1", "golf.player.top_n_finish", "Golf", None),
    ],
)
def test_disabled_profiles_block_before_probability_or_ev(
    adapter_id: str,
    version: str,
    profile_id: str,
    league: str,
    line: str | None,
    tmp_path: Path,
) -> None:
    identity = market_identity(
        league=league,
        market_key=profile_id,
        side="home" if "moneyline" in profile_id else "yes",
        line=line,
    )
    payload = request_payload(
        adapter_id=adapter_id,
        adapter_version=version,
        profile_id=profile_id,
        lifecycle="disabled_provider_validation",
        candidates=[candidate(identity=identity)],
    )

    decision = _evaluate(payload, tmp_path).candidates[0]

    assert "ADAPTER_PROFILE_DISABLED" in decision.reason_codes
    assert decision.estimated_probability is None
    assert decision.ev_per_unit is None
    assert decision.rank is None
    assert decision.consensus_audit.source_level_probabilities == []
    assert decision.consensus_audit.usable_book_count == 0
    assert decision.consensus_audit.pricing_origin_group_count == 0


def test_unregistered_profile_fails_before_valuation(tmp_path: Path) -> None:
    profile_id = "soccer.full_game.moneyline"
    identity = market_identity(league="Soccer", market_key=profile_id, line=None)
    payload = request_payload(
        adapter_id="soccer.pregame_v0_1",
        adapter_version="0.1.0",
        profile_id=profile_id,
        lifecycle="active",
        candidates=[candidate(identity=identity)],
    )

    decision = _evaluate(payload, tmp_path).candidates[0]

    assert "ADAPTER_PROFILE_DISABLED" in decision.reason_codes
    assert decision.estimated_probability is None
    assert decision.ev_per_unit is None
    assert decision.consensus_audit.source_level_probabilities == []
    assert decision.consensus_audit.usable_book_count == 0


def test_named_unsupported_promotion_shape_returns_structured_blocker(
    tmp_path: Path,
) -> None:
    brief = _evaluate(
        request_payload(boost_type="odds_boost", boost_percent=None), tmp_path
    )

    assert "PROBABILITY_METHOD_UNAVAILABLE" in _candidate_codes(brief)
    assert brief.candidates[0].ev_per_unit is None


def test_token_allocation_is_order_independent_and_deterministic(tmp_path: Path) -> None:
    weaker = candidate(candidate_id="candidate-a", target_odds=-110)
    stronger = candidate(candidate_id="candidate-b", target_odds=100)
    first = _evaluate(
        request_payload(candidates=[weaker, stronger], token_count=1), tmp_path / "first"
    )
    second = _evaluate(
        request_payload(candidates=[stronger, weaker], token_count=1), tmp_path / "second"
    )

    def allocation(brief):
        return [
            (row.candidate_id, row.rank, row.state.value, tuple(row.reason_codes))
            for row in brief.candidates
        ]

    assert allocation(first) == allocation(second)
    assert allocation(first)[0][:3] == ("candidate-b", 1, "actionable_for_review")
    assert allocation(first)[1][:3] == ("candidate-a", 2, "pass")
    assert "DOMINATED_BY_BETTER_TOKEN_USE" in allocation(first)[1][3]


def test_no_token_use_is_forced_when_every_candidate_has_nonpositive_ev(
    tmp_path: Path,
) -> None:
    payload = request_payload(candidates=[candidate(target_odds=-500)])
    payload["promotion"]["minimum_american_odds"] = None

    brief = _evaluate(payload, tmp_path)
    decision = brief.candidates[0]

    assert brief.run.overall_status == "no_qualifying_candidate"
    assert decision.state == "pass"
    assert decision.reason_codes == ["EV_BELOW_THRESHOLD"]
    assert decision.expected_dollars < 0


def test_evaluation_is_decimal_reproducible(tmp_path: Path) -> None:
    payload = request_payload()
    first = _evaluate(deepcopy(payload), tmp_path / "first")
    second = _evaluate(deepcopy(payload), tmp_path / "second")

    assert first.model_dump_json() == second.model_dump_json()


def test_runtime_makes_no_network_calls_or_unrequested_writes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = ManualPromoEvaluation.model_validate(request_payload())
    contract_dir = tmp_path / "contracts"
    catalog_path, registry_path = write_runtime_contracts(contract_dir, request)
    before = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }

    def deny_network(*_args, **_kwargs):
        raise AssertionError("runtime attempted network access")

    original_path_open = Path.open

    def guarded_path_open(path: Path, mode: str = "r", *args, **kwargs):
        if any(flag in mode for flag in "wax+") and not path.resolve().is_relative_to(
            tmp_path.resolve()
        ):
            raise AssertionError(f"runtime attempted an external write: {path}")
        return original_path_open(path, mode, *args, **kwargs)

    monkeypatch.setattr(socket, "create_connection", deny_network)
    monkeypatch.setattr(socket.socket, "connect", deny_network)
    monkeypatch.setattr(Path, "open", guarded_path_open)

    brief = evaluate_manual_promotion(request, catalog_path, registry_path)

    after = {
        path.relative_to(tmp_path): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }
    assert brief.candidates[0].estimated_probability is not None
    assert after == before


def test_live_catalog_and_registry_support_the_four_profile_manual_runtime() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    payload = request_payload()
    payload["promotion"]["sportsbook_id"] = "FanDuel"
    row = payload["candidates"][0]
    row["target_quote"]["sportsbook_id"] = "FanDuel"
    row["target_quote"]["pricing_origin_id"] = "sportsbook_fanduel"
    row["target_quote"]["american_odds"] = 100
    comparison_details = (
        ("DraftKings", "sportsbook_draftkings"),
        ("Circa Sports", "sportsbook_circa"),
    )
    evidence_by_id = {item["evidence_id"]: item for item in row["evidence"]}
    for pair, (sportsbook_id, origin_id) in zip(
        row["comparison_pairs"], comparison_details, strict=True
    ):
        pair["source_id"] = "sportsbook_comparison_manual_evidence"
        pair["sportsbook_id"] = sportsbook_id
        pair["pricing_origin_id"] = origin_id
        evidence_by_id[pair["evidence_id"]]["source_id"] = pair["source_id"]

    request = ManualPromoEvaluation.model_validate(payload)
    brief = evaluate_manual_promotion(
        request,
        repository_root / "SPORT_ADAPTERS" / "catalog.yaml",
        repository_root / "SPORT_ADAPTERS" / "source_registry.yaml",
    )

    assert brief.run.overall_status == "actionable_for_review"
    assert brief.candidates[0].state == "actionable_for_review"
    assert brief.candidates[0].consensus_audit.pricing_origin_group_count == 2
    assert brief.candidates[0].estimated_probability is not None
    assert brief.candidates[0].expected_dollars is not None


def test_live_catalog_registers_exactly_the_four_implemented_profiles() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    catalog = yaml.safe_load(
        (repository_root / "SPORT_ADAPTERS" / "catalog.yaml").read_text(
            encoding="utf-8"
        )
    )

    runtime_profiles = {
        profile["profile_id"]
        for profile in catalog["profiles"]
        if profile["implementation_status"] == "manual_input_runtime"
    }

    assert runtime_profiles == {
        "mlb.player_hits",
        "wnba.full_game.moneyline",
        "wnba.full_game.spread",
        "wnba.full_game.total",
    }
