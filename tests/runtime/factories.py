from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml

from ap_slave_runtime.models import ManualPromoEvaluation


NOW = datetime(2026, 7, 14, 4, 0, tzinfo=timezone.utc)
HASH = "a" * 64


def _iso(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def market_identity(
    *,
    league: str = "MLB",
    event_id: str = "mlb-game-1",
    participant_id: str | None = "player-1",
    market_key: str = "mlb.player_hits",
    side: str = "over",
    line: str | None = "0.5",
    period: str = "full_game",
    overtime: str = "included",
    push_behavior: str = "impossible",
    settlement_rule: str = "official full-game result including extra periods",
) -> dict[str, Any]:
    return {
        "jurisdiction": "US-MO",
        "league": league,
        "event_id": event_id,
        "participant_id": participant_id,
        "raw_market_label": "Player Hits" if league == "MLB" else "Game Moneyline",
        "raw_selection_label": "Over 0.5" if league == "MLB" else "Home",
        "canonical_market_key": market_key,
        "outcome_set_id": f"{event_id}:{market_key}:{line or 'none'}",
        "outcome_set_type": "binary_pair",
        "outcome_set_completeness": "complete",
        "participant_set_version": None,
        "market_wrapper": "standard",
        "side": side,
        "line": line,
        "period": period,
        "overtime_or_extra_innings_treatment": overtime,
        "push_behavior": push_behavior,
        "tie_or_dead_heat_treatment": "not_applicable",
        "participation_rule": "participant must start",
        "void_rule": "void if event is canceled",
        "stat_counting_rule": "official league statistics",
        "settlement_rule": settlement_rule,
        "ap_frankenstein_compatibility": "direct",
    }


def evidence(
    evidence_id: str,
    source_id: str,
    captured_at: datetime,
    *,
    permission_reviewed: bool = True,
) -> dict[str, Any]:
    return {
        "evidence_id": evidence_id,
        "source_id": source_id,
        "source_instance_id": f"instance:{source_id}",
        "jurisdiction": "US-MO",
        "captured_at_utc": _iso(captured_at),
        "provider_published_at_utc": None,
        "content_sha256": HASH,
        "source_permission_reviewed": permission_reviewed,
        "verification_status": "confirmed",
    }


def comparison_pair(
    identity: dict[str, Any],
    *,
    source_id: str,
    sportsbook_id: str,
    pricing_origin_id: str,
    retrieved_at: datetime,
    candidate_odds: int = -110,
    opposing_odds: int = -110,
    market_status: str = "open",
    evidence_id: str | None = None,
) -> dict[str, Any]:
    line = identity["line"]
    return {
        "source_id": source_id,
        "sportsbook_id": sportsbook_id,
        "pricing_origin_id": pricing_origin_id,
        "jurisdiction": "US-MO",
        "market_identity": deepcopy(identity),
        "outcomes": [
            {
                "outcome_id": f"{sportsbook_id}:candidate",
                "raw_selection_label": identity["raw_selection_label"],
                "side": identity["side"],
                "line": line,
                "american_odds": candidate_odds,
            },
            {
                "outcome_id": f"{sportsbook_id}:opposing",
                "raw_selection_label": "Under" if identity["side"] == "over" else "Away",
                "side": "under" if identity["side"] == "over" else "away",
                "line": line,
                "american_odds": opposing_odds,
            },
        ],
        "market_status": market_status,
        "retrieved_at_utc": _iso(retrieved_at),
        "provider_last_update_utc": None,
        "evidence_id": evidence_id or f"evidence:{sportsbook_id}",
    }


def candidate(
    *,
    candidate_id: str = "candidate-1",
    identity: dict[str, Any] | None = None,
    target_odds: int = -150,
    target_age_seconds: int = 30,
    comparison_age_seconds: tuple[int, int] = (40, 50),
) -> dict[str, Any]:
    identity = deepcopy(identity or market_identity())
    target_time = NOW - timedelta(seconds=target_age_seconds)
    pair_a_time = NOW - timedelta(seconds=comparison_age_seconds[0])
    pair_b_time = NOW - timedelta(seconds=comparison_age_seconds[1])
    pairs = [
        comparison_pair(
            identity,
            source_id="sportsbook_comparison_manual_evidence",
            sportsbook_id="Comparison A",
            pricing_origin_id="origin_a",
            retrieved_at=pair_a_time,
            candidate_odds=-120,
            opposing_odds=100,
            evidence_id=f"evidence:comparison:{candidate_id}:a",
        ),
        comparison_pair(
            identity,
            source_id="sportsbook_comparison_manual_evidence",
            sportsbook_id="Comparison B",
            pricing_origin_id="origin_b",
            retrieved_at=pair_b_time,
            candidate_odds=-110,
            opposing_odds=-110,
            evidence_id=f"evidence:comparison:{candidate_id}:b",
        ),
    ]
    evidence_rows = [
        evidence(f"evidence:target:{candidate_id}", "sportsbook_target_manual_evidence", target_time),
        evidence(pairs[0]["evidence_id"], pairs[0]["source_id"], pair_a_time),
        evidence(pairs[1]["evidence_id"], pairs[1]["source_id"], pair_b_time),
    ]
    return {
        "candidate_id": candidate_id,
        "market_identity": identity,
        "target_quote": {
            "source_id": "sportsbook_target_manual_evidence",
            "sportsbook_id": "FanDuel",
            "pricing_origin_id": "sportsbook_fanduel",
            "jurisdiction": "US-MO",
            "american_odds": target_odds,
            "market_status": "open",
            "retrieved_at_utc": _iso(target_time),
            "provider_last_update_utc": None,
            "evidence_id": f"evidence:target:{candidate_id}",
        },
        "comparison_pairs": pairs,
        "material_context": [],
        "latest_material_context_at_utc": None,
        "evidence": evidence_rows,
    }


def request_payload(
    *,
    adapter_id: str = "mlb.player_hits_v0_1",
    adapter_version: str = "0.1.1",
    profile_id: str = "mlb.player_hits",
    lifecycle: str = "active",
    candidates: list[dict[str, Any]] | None = None,
    boost_type: str = "profit_boost",
    boost_percent: str | None = "30",
    token_count: int = 1,
) -> dict[str, Any]:
    candidate_rows = deepcopy(candidates or [candidate()])
    event_ids = sorted({row["market_identity"]["event_id"] for row in candidate_rows})
    market_keys = sorted(
        {row["market_identity"]["canonical_market_key"] for row in candidate_rows}
    )
    return {
        "contract_version": "manual_promo_evaluation_v1",
        "run_id": "run-golden-1",
        "created_at_utc": _iso(NOW),
        "timezone": "America/Chicago",
        "jurisdiction": "US-MO",
        "adapter_id": adapter_id,
        "adapter_version": adapter_version,
        "adapter_contract_version": "adapter_contract_v1",
        "profile_id": profile_id,
        "profile_lifecycle": lifecycle,
        "promotion": {
            "promo_id": "promo-1",
            "sportsbook_id": "FanDuel",
            "jurisdiction": "US-MO",
            "raw_promotion_text": "30% profit boost, maximum $25 stake",
            "boost_type": boost_type,
            "boost_percent": boost_percent,
            "max_stake": "25",
            "payout_cap": None,
            "minimum_american_odds": -200,
            "maximum_american_odds": None,
            "odds_range_basis": "base_odds",
            "eligible_event_ids": event_ids,
            "eligible_market_keys": market_keys,
            "expires_at_utc": _iso(NOW + timedelta(hours=1)),
            "token_count": token_count,
            "void_push_rules": "voids return the token",
            "verification_status": "confirmed",
            "ambiguities": [],
        },
        "candidates": candidate_rows,
        "audit_evidence": [],
        "user_max_stake": "25",
    }


def request(**overrides: Any) -> ManualPromoEvaluation:
    return ManualPromoEvaluation.model_validate(request_payload(**overrides))


def write_runtime_contracts(
    tmp_path: Path,
    evaluation: ManualPromoEvaluation,
) -> tuple[Path, Path]:
    tmp_path.mkdir(parents=True, exist_ok=True)
    repository_root = Path(__file__).resolve().parents[2]
    catalog = yaml.safe_load(
        (repository_root / "SPORT_ADAPTERS" / "catalog.yaml").read_text(encoding="utf-8")
    )
    registry = yaml.safe_load(
        (repository_root / "SPORT_ADAPTERS" / "source_registry.yaml").read_text(
            encoding="utf-8"
        )
    )

    enabled = {
        "mlb.player_hits",
        "wnba.full_game.moneyline",
        "wnba.full_game.spread",
        "wnba.full_game.total",
    }
    for profile in catalog["profiles"]:
        if profile["profile_id"] in enabled:
            profile["implementation_status"] = "manual_input_runtime"

    known_sources = {row["source_id"] for row in registry["source_records"]}
    known_origins = {
        row["pricing_origin_id"] for row in registry["pricing_origin_groups"]
    }
    for candidate_row in evaluation.candidates:
        source_ids = [candidate_row.target_quote.source_id]
        source_ids.extend(pair.source_id for pair in candidate_row.comparison_pairs)
        source_ids.extend(fact.source_id for fact in candidate_row.material_context)
        for source_id in source_ids:
            if source_id not in known_sources:
                registry["source_records"].append({"source_id": source_id})
                known_sources.add(source_id)

        origins = [candidate_row.target_quote.pricing_origin_id]
        origins.extend(pair.pricing_origin_id for pair in candidate_row.comparison_pairs)
        for origin_id in origins:
            if origin_id not in known_origins:
                registry["pricing_origin_groups"].append(
                    {
                        "pricing_origin_id": origin_id,
                        "origin_resolution_status": "resolved",
                    }
                )
                known_origins.add(origin_id)

    catalog_path = tmp_path / "catalog.yaml"
    registry_path = tmp_path / "source_registry.yaml"
    catalog_path.write_text(yaml.safe_dump(catalog, sort_keys=False), encoding="utf-8")
    registry_path.write_text(yaml.safe_dump(registry, sort_keys=False), encoding="utf-8")
    return catalog_path, registry_path
