from __future__ import annotations

from datetime import datetime
from decimal import Decimal, localcontext
from pathlib import Path
from typing import Any, Iterable

import yaml

from .models import (
    Blocker,
    CandidateDecision,
    CandidateState,
    ChangeSummary,
    ConsensusAudit,
    ExcludedSource,
    FreshnessSummary,
    ManualCandidateInput,
    ManualPromoEvaluationInput,
    MarketIdentity,
    MarketStatus,
    MonitoringMetadata,
    OverallStatus,
    PromotionDecisionBriefV2,
    PromotionSummary,
    QASummary,
    RunSummary,
    SourceLevelProbability,
    VerificationStatus,
)


DEFAULT_CATALOG_PATH = Path("SPORT_ADAPTERS/catalog.yaml")
DEFAULT_SOURCE_REGISTRY_PATH = Path("SPORT_ADAPTERS/source_registry.yaml")

_RUNTIME_PROFILES = {
    "mlb.player_hits": "mlb.player_hits_v0_1",
    "wnba.full_game.moneyline": "wnba.pregame_full_game_v0_1",
    "wnba.full_game.spread": "wnba.pregame_full_game_v0_1",
    "wnba.full_game.total": "wnba.pregame_full_game_v0_1",
}
_ENABLED_LIFECYCLES = {"active", "pilot_enabled"}
_RESOLVED_ORIGIN_STATUS = {"resolved"}
_IDENTITY_FIELDS = (
    "jurisdiction",
    "league",
    "event_id",
    "participant_id",
    "canonical_market_key",
    "outcome_set_id",
    "outcome_set_type",
    "outcome_set_completeness",
    "participant_set_version",
    "market_wrapper",
    "line",
    "period",
    "overtime_or_extra_innings_treatment",
    "push_behavior",
    "tie_or_dead_heat_treatment",
    "participation_rule",
    "void_rule",
    "stat_counting_rule",
    "settlement_rule",
)


def _american_to_decimal(american_odds: int) -> Decimal:
    odds = Decimal(american_odds)
    if american_odds > 0:
        return Decimal(1) + odds / Decimal(100)
    return Decimal(1) + Decimal(100) / abs(odds)


def _american_implied_ratio(american_odds: int) -> tuple[Decimal, Decimal]:
    odds = Decimal(american_odds)
    if american_odds > 0:
        return Decimal(100), odds + Decimal(100)
    absolute_odds = abs(odds)
    return absolute_odds, absolute_odds + Decimal(100)


def _profit_only_boost(base_decimal: Decimal, boost_percent: Decimal) -> Decimal:
    multiplier = Decimal(1) + boost_percent / Decimal(100)
    return Decimal(1) + multiplier * (base_decimal - Decimal(1))


def _age_seconds(now: datetime, captured_at: datetime) -> int:
    return int((now - captured_at).total_seconds())


def _blocker(
    code: str,
    message: str,
    *,
    candidate_id: str | None = None,
    field_path: str | None = None,
) -> Blocker:
    return Blocker(
        reason_code=code,
        message=message,
        candidate_id=candidate_id,
        field_path=field_path,
    )


def _append_blocker(blockers: list[Blocker], blocker: Blocker) -> None:
    key = (
        blocker.reason_code,
        blocker.message,
        blocker.candidate_id,
        blocker.field_path,
    )
    if all(
        (
            current.reason_code,
            current.message,
            current.candidate_id,
            current.field_path,
        )
        != key
        for current in blockers
    ):
        blockers.append(blocker)


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        document = yaml.safe_load(handle)
    if not isinstance(document, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return document


def _catalog_maps(catalog: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    profiles = {
        record["profile_id"]: record
        for record in catalog.get("profiles", [])
        if isinstance(record, dict) and isinstance(record.get("profile_id"), str)
    }
    adapters = {
        record["adapter_id"]: record
        for record in catalog.get("adapters", [])
        if isinstance(record, dict) and isinstance(record.get("adapter_id"), str)
    }
    return profiles, adapters


def _registry_maps(registry: dict[str, Any]) -> tuple[set[str], dict[str, str]]:
    source_ids = {
        record["source_id"]
        for record in registry.get("source_records", [])
        if isinstance(record, dict) and isinstance(record.get("source_id"), str)
    }
    origins = {
        record["pricing_origin_id"]: record.get("origin_resolution_status", "unresolved")
        for record in registry.get("pricing_origin_groups", [])
        if isinstance(record, dict)
        and isinstance(record.get("pricing_origin_id"), str)
    }
    return source_ids, origins


def _promotion_summary(request: ManualPromoEvaluationInput) -> PromotionSummary:
    promotion = request.promotion
    return PromotionSummary(
        promo_id=promotion.promo_id,
        sportsbook_id=promotion.sportsbook_id,
        jurisdiction=promotion.jurisdiction,
        boost_type=promotion.boost_type,
        boost_percent=promotion.boost_percent,
        max_stake=promotion.max_stake,
        expires_at_utc=promotion.expires_at_utc,
        verification_status=promotion.verification_status,
        ambiguities=promotion.ambiguities,
    )


def _empty_audit(candidate: ManualCandidateInput) -> ConsensusAudit:
    return ConsensusAudit(
        target_sportsbook_id=candidate.target_quote.sportsbook_id,
        target_excluded=True,
        raw_source_count=len(candidate.comparison_pairs),
        usable_book_count=0,
        pricing_origin_group_count=0,
        aggregation_method_version=None,
        source_level_probabilities=[],
        dispersion_percentage_points=None,
        oldest_comparison_age_seconds=None,
        collection_skew_seconds=None,
        excluded_sources=[],
    )


def _candidate_shell(
    candidate: ManualCandidateInput,
    blockers: list[Blocker],
    *,
    target_age: int | None,
    post_material_change_synchronized: bool,
    consensus_audit: ConsensusAudit | None = None,
) -> CandidateDecision:
    reason_codes = list(dict.fromkeys(blocker.reason_code for blocker in blockers))
    ineligible_codes = {
        "PROMO_MIN_ODDS_FAIL",
        "PROMO_MAX_ODDS_FAIL",
        "PROMO_MARKET_INELIGIBLE",
        "PROMO_EVENT_WINDOW_FAIL",
        "PROMO_EXPIRED",
    }
    return CandidateDecision(
        candidate_id=candidate.candidate_id,
        event_id=candidate.market_identity.event_id,
        participant_id=candidate.market_identity.participant_id,
        market_key=candidate.market_identity.canonical_market_key,
        market_identity=candidate.market_identity,
        side=candidate.market_identity.side,
        line=candidate.market_identity.line,
        target_american_odds=candidate.target_quote.american_odds,
        consensus_audit=consensus_audit or _empty_audit(candidate),
        state=(
            CandidateState.INELIGIBLE
            if ineligible_codes.intersection(reason_codes)
            else CandidateState.BLOCKED
        ),
        reason_codes=reason_codes,
        blockers=blockers,
        invalidation_conditions=[
            "Any promotion, identity, settlement, status, source, freshness, or material-context change requires a new evaluation."
        ],
        monitoring_metadata=MonitoringMetadata(
            next_refresh_at=None,
            next_refresh_reason=(
                blockers[0].message if blockers else "Refresh every input before human review."
            ),
            post_material_change_synchronized=post_material_change_synchronized,
        ),
        source_refs=list(
            dict.fromkeys(
                [candidate.target_quote.evidence_id]
                + [pair.evidence_id for pair in candidate.comparison_pairs]
                + [evidence.evidence_id for evidence in candidate.evidence]
            )
        ),
    )


def _same_identity(left: MarketIdentity, right: MarketIdentity) -> bool:
    return all(getattr(left, field) == getattr(right, field) for field in _IDENTITY_FIELDS)


def _is_half_point(value: Decimal | None) -> bool:
    if value is None:
        return False
    return abs(value) % Decimal(1) == Decimal("0.5")


def _normalized_period(value: str) -> str:
    return value.strip().casefold().replace("-", "_").replace(" ", "_")


def _profile_identity_blockers(
    request: ManualPromoEvaluationInput,
    candidate: ManualCandidateInput,
) -> list[Blocker]:
    identity = candidate.market_identity
    candidate_id = candidate.candidate_id
    blockers: list[Blocker] = []

    def add(code: str, message: str, field_path: str) -> None:
        _append_blocker(
            blockers,
            _blocker(code, message, candidate_id=candidate_id, field_path=field_path),
        )

    if identity.canonical_market_key != request.profile_id:
        add("MARKET_IDENTITY_MISMATCH", "Canonical market does not match the selected profile.", "market_identity.canonical_market_key")
    normalized_league = identity.league.strip().casefold()
    expected_league = "mlb" if request.profile_id == "mlb.player_hits" else "wnba"
    if expected_league not in normalized_league:
        add("MARKET_IDENTITY_MISMATCH", "Candidate league does not match the selected profile.", "market_identity.league")
    if identity.jurisdiction != request.jurisdiction:
        add("JURISDICTION_MISMATCH", "Candidate jurisdiction does not match the run.", "market_identity.jurisdiction")
    if identity.event_id not in request.promotion.eligible_event_ids:
        add("PROMO_EVENT_WINDOW_FAIL", "Candidate event is not promotion-eligible.", "market_identity.event_id")
    if identity.canonical_market_key not in request.promotion.eligible_market_keys:
        add("PROMO_MARKET_INELIGIBLE", "Candidate market is not promotion-eligible.", "market_identity.canonical_market_key")
    if identity.outcome_set_type != "binary_pair" or identity.outcome_set_completeness != "complete":
        add("OUTCOME_SET_INCOMPLETE", "The exact binary outcome set is not complete.", "market_identity.outcome_set_completeness")
    if _normalized_period(identity.period) != "full_game":
        add("MARKET_IDENTITY_MISMATCH", "Only pregame full-game markets are supported.", "market_identity.period")
    if identity.overtime_or_extra_innings_treatment != "included":
        add("SETTLEMENT_RULE_MISMATCH", "Overtime or extra-innings treatment must be included and exact.", "market_identity.overtime_or_extra_innings_treatment")
    if identity.push_behavior != "impossible":
        add("PUSH_MODEL_UNAVAILABLE", "Push-capable or unknown outcomes are unsupported.", "market_identity.push_behavior")
    if identity.ap_frankenstein_compatibility != "direct":
        add("MARKET_IDENTITY_MISMATCH", "The market is not in the reviewed direct compatibility lane.", "market_identity.ap_frankenstein_compatibility")
    if identity.market_wrapper.strip().casefold() != "standard":
        add("MARKET_IDENTITY_MISMATCH", "Only the standard principal market wrapper is supported.", "market_identity.market_wrapper")

    if request.profile_id == "wnba.full_game.moneyline":
        if identity.line is not None:
            add("MARKET_IDENTITY_MISMATCH", "A full-game moneyline cannot carry a point line.", "market_identity.line")
        if identity.participant_id is None:
            add("MARKET_IDENTITY_MISMATCH", "A moneyline candidate must identify its team.", "market_identity.participant_id")
    elif request.profile_id in {"wnba.full_game.spread", "wnba.full_game.total"}:
        if not _is_half_point(identity.line):
            add("PUSH_MODEL_UNAVAILABLE", "Only exact half-point WNBA lines are supported.", "market_identity.line")
        if request.profile_id.endswith("spread") and identity.participant_id is None:
            add("MARKET_IDENTITY_MISMATCH", "A spread candidate must identify its team.", "market_identity.participant_id")
    elif request.profile_id == "mlb.player_hits":
        if identity.participant_id is None:
            add("PLAYER_MAPPING_AMBIGUOUS", "An MLB player-hits candidate must identify its player.", "market_identity.participant_id")
        if not _is_half_point(identity.line):
            add("PUSH_MODEL_UNAVAILABLE", "MLB player-hits runtime valuation requires an exact non-push half-point threshold.", "market_identity.line")

    return blockers


def _global_blockers(
    request: ManualPromoEvaluationInput,
    profiles: dict[str, Any],
    adapters: dict[str, Any],
) -> list[Blocker]:
    blockers: list[Blocker] = []
    profile = profiles.get(request.profile_id)
    if profile is None:
        return [_blocker("ADAPTER_PROFILE_DISABLED", "The requested profile is unregistered in the catalog.", field_path="profile_id")]

    catalog_lifecycle = profile.get("lifecycle")
    if catalog_lifecycle not in _ENABLED_LIFECYCLES:
        label = "Golf profiles are evidence-review only and cannot be valued." if request.profile_id.startswith("golf.") else "The catalog profile is disabled and cannot be valued."
        _append_blocker(blockers, _blocker("ADAPTER_PROFILE_DISABLED", label, field_path="profile_id"))
    if request.profile_lifecycle.value != catalog_lifecycle:
        _append_blocker(blockers, _blocker("SOURCE_CONFLICT", "Request lifecycle does not match the catalog.", field_path="profile_lifecycle"))
    if profile.get("adapter_id") != request.adapter_id:
        _append_blocker(blockers, _blocker("MARKET_MAPPING_AMBIGUOUS", "Request adapter does not own the catalog profile.", field_path="adapter_id"))

    adapter = adapters.get(request.adapter_id)
    if adapter is None or adapter.get("version") != request.adapter_version:
        _append_blocker(blockers, _blocker("SOURCE_CONFLICT", "Request adapter version does not match the catalog.", field_path="adapter_version"))

    expected_adapter = _RUNTIME_PROFILES.get(request.profile_id)
    if expected_adapter != request.adapter_id:
        _append_blocker(blockers, _blocker("ADAPTER_PROFILE_DISABLED", "No deterministic runtime is registered for this exact profile.", field_path="profile_id"))
    if profile.get("implementation_status") not in {"manual_input_runtime", "provider_integrated"}:
        _append_blocker(blockers, _blocker("NO_VALIDATED_PROBABILITY", "The catalog does not authorize deterministic runtime valuation for this profile.", field_path="profile_id"))

    promotion = request.promotion
    if request.jurisdiction != "US-MO" or promotion.jurisdiction != "US-MO":
        _append_blocker(blockers, _blocker("JURISDICTION_MISMATCH", "Only verified Missouri promotion evidence is supported.", field_path="promotion.jurisdiction"))
    if promotion.boost_type != "profit_boost":
        _append_blocker(blockers, _blocker("PROBABILITY_METHOD_UNAVAILABLE", "Only verified profit-only boosts use the implemented formula.", field_path="promotion.boost_type"))
    if (
        promotion.verification_status != VerificationStatus.CONFIRMED
        or promotion.ambiguities
        or promotion.boost_percent is None
        or promotion.boost_percent <= 0
        or promotion.max_stake <= 0
    ):
        _append_blocker(blockers, _blocker("PROMO_TERMS_AMBIGUOUS", "Promotion terms, profit-only basis, boost percent, and positive stake cap must be verified.", field_path="promotion"))
    if promotion.payout_cap is not None:
        _append_blocker(blockers, _blocker("PROMO_TERMS_AMBIGUOUS", "A payout cap requires an exact cap basis that the current manual contract does not represent.", field_path="promotion.payout_cap"))
    if promotion.odds_range_basis != "base_odds":
        _append_blocker(blockers, _blocker("PROMO_TERMS_AMBIGUOUS", "The implemented minimum/maximum odds gate applies only when the promotion explicitly uses base odds.", field_path="promotion.odds_range_basis"))
    if request.created_at_utc >= promotion.expires_at_utc:
        _append_blocker(blockers, _blocker("PROMO_EXPIRED", "The promotion is expired at evaluation time.", field_path="promotion.expires_at_utc"))
    return blockers


def _evaluate_candidate(
    request: ManualPromoEvaluationInput,
    candidate: ManualCandidateInput,
    inherited_blockers: Iterable[Blocker],
    source_ids: set[str],
    origin_status: dict[str, str],
) -> CandidateDecision:
    now = request.created_at_utc
    candidate_id = candidate.candidate_id
    blockers = [
        blocker.model_copy(update={"candidate_id": blocker.candidate_id or candidate_id})
        for blocker in inherited_blockers
    ]
    for blocker in _profile_identity_blockers(request, candidate):
        _append_blocker(blockers, blocker)

    target = candidate.target_quote
    target_age = _age_seconds(now, target.retrieved_at_utc)
    stale_inputs: list[str] = []
    if target.sportsbook_id != request.promotion.sportsbook_id:
        _append_blocker(blockers, _blocker("MARKET_IDENTITY_MISMATCH", "Target quote sportsbook does not match the promotion.", candidate_id=candidate_id, field_path="target_quote.sportsbook_id"))
    if target.jurisdiction != request.jurisdiction:
        _append_blocker(blockers, _blocker("JURISDICTION_MISMATCH", "Target quote is not verified for Missouri.", candidate_id=candidate_id, field_path="target_quote.jurisdiction"))
    if target.market_status != MarketStatus.OPEN:
        _append_blocker(blockers, _blocker("MARKET_SUSPENDED", "Target market is not open.", candidate_id=candidate_id, field_path="target_quote.market_status"))
    if target_age < 0:
        _append_blocker(blockers, _blocker("SOURCE_CONFLICT", "Target timestamp is in the future.", candidate_id=candidate_id, field_path="target_quote.retrieved_at_utc"))
    elif target_age > 180:
        stale_inputs.append("target_quote")
        _append_blocker(blockers, _blocker("TARGET_QUOTE_STALE", "Target quote exceeds 180 seconds.", candidate_id=candidate_id, field_path="target_quote.retrieved_at_utc"))
    if target.source_id not in source_ids:
        _append_blocker(blockers, _blocker("SOURCE_CONFLICT", "Target source is absent from the source registry.", candidate_id=candidate_id, field_path="target_quote.source_id"))
    if origin_status.get(target.pricing_origin_id) not in _RESOLVED_ORIGIN_STATUS:
        _append_blocker(blockers, _blocker("PRICING_ORIGIN_UNRESOLVED", "Target pricing origin is unresolved.", candidate_id=candidate_id, field_path="target_quote.pricing_origin_id"))

    evidence_by_id = {
        evidence.evidence_id: evidence
        for evidence in [*candidate.evidence, *request.audit_evidence]
    }
    for fact in candidate.material_context:
        fact_evidence = evidence_by_id.get(fact.evidence_id)
        if (
            fact.verification_status != "confirmed"
            or fact_evidence is None
            or not fact_evidence.source_permission_reviewed
            or fact_evidence.verification_status != VerificationStatus.CONFIRMED
            or fact_evidence.source_id != fact.source_id
            or fact.source_id not in source_ids
        ):
            _append_blocker(blockers, _blocker("SOURCE_CONFLICT", "A material-context fact or its evidence is unverified, conflicting, source-mismatched, or unregistered.", candidate_id=candidate_id, field_path="material_context"))
        if fact.effective_at_utc > now or fact.captured_at_utc > now:
            _append_blocker(blockers, _blocker("SOURCE_CONFLICT", "A material-context timestamp is in the future.", candidate_id=candidate_id, field_path="material_context"))
    target_evidence = evidence_by_id.get(target.evidence_id)
    if (
        target_evidence is None
        or not target_evidence.source_permission_reviewed
        or target_evidence.verification_status != VerificationStatus.CONFIRMED
        or target_evidence.source_id != target.source_id
    ):
        _append_blocker(blockers, _blocker("SCREENSHOT_VERIFICATION_REQUIRED", "Target evidence is missing, unverified, or source-mismatched.", candidate_id=candidate_id, field_path="target_quote.evidence_id"))

    minimum = request.promotion.minimum_american_odds
    maximum = request.promotion.maximum_american_odds
    if minimum is not None and target.american_odds < minimum:
        _append_blocker(blockers, _blocker("PROMO_MIN_ODDS_FAIL", "Target odds are below the promotion minimum.", candidate_id=candidate_id, field_path="target_quote.american_odds"))
    if maximum is not None and target.american_odds > maximum:
        _append_blocker(blockers, _blocker("PROMO_MAX_ODDS_FAIL", "Target odds exceed the promotion maximum.", candidate_id=candidate_id, field_path="target_quote.american_odds"))

    excluded: list[ExcludedSource] = []
    included: list[tuple[Any, Decimal, int]] = []
    seen_origins: set[str] = set()
    for pair in candidate.comparison_pairs:
        pair_reasons: list[str] = []
        pair_age = _age_seconds(now, pair.retrieved_at_utc)
        if pair.source_id not in source_ids:
            pair_reasons.append("SOURCE_CONFLICT")
        if pair.jurisdiction != request.jurisdiction:
            pair_reasons.append("JURISDICTION_MISMATCH")
        if pair.market_status != MarketStatus.OPEN:
            pair_reasons.append("MARKET_SUSPENDED")
        if pair_age < 0:
            pair_reasons.append("SOURCE_CONFLICT")
        elif pair_age > 300:
            pair_reasons.append("COMPARISON_QUOTE_STALE")
        if not _same_identity(candidate.market_identity, pair.market_identity):
            pair_reasons.append("SETTLEMENT_RULE_MISMATCH")
        if pair.market_identity.outcome_set_completeness != "complete" or len(pair.outcomes) != 2:
            pair_reasons.append("OUTCOME_SET_INCOMPLETE")
        if pair.sportsbook_id == target.sportsbook_id or pair.pricing_origin_id == target.pricing_origin_id:
            pair_reasons.append("PRICING_ORIGIN_UNRESOLVED")
        if origin_status.get(pair.pricing_origin_id) not in _RESOLVED_ORIGIN_STATUS:
            pair_reasons.append("PRICING_ORIGIN_UNRESOLVED")
        if pair.pricing_origin_id in seen_origins:
            pair_reasons.append("PRICING_ORIGIN_UNRESOLVED")
        pair_evidence = evidence_by_id.get(pair.evidence_id)
        if (
            pair_evidence is None
            or not pair_evidence.source_permission_reviewed
            or pair_evidence.verification_status != VerificationStatus.CONFIRMED
            or pair_evidence.source_id != pair.source_id
        ):
            pair_reasons.append("SCREENSHOT_VERIFICATION_REQUIRED")

        matching = [outcome for outcome in pair.outcomes if outcome.side == candidate.market_identity.side]
        if (
            len(matching) != 1
            or len({outcome.side for outcome in pair.outcomes}) != 2
            or len({outcome.outcome_id for outcome in pair.outcomes}) != 2
        ):
            pair_reasons.append("OUTCOME_SET_INCOMPLETE")
        if len(matching) == 1:
            candidate_line = candidate.market_identity.line
            matching_outcome = matching[0]
            opposing = [outcome for outcome in pair.outcomes if outcome is not matching_outcome]
            if matching_outcome.line != candidate_line:
                pair_reasons.append("SETTLEMENT_RULE_MISMATCH")
            elif request.profile_id == "wnba.full_game.spread":
                if (
                    candidate_line is None
                    or len(opposing) != 1
                    or opposing[0].line != -candidate_line
                ):
                    pair_reasons.append("SETTLEMENT_RULE_MISMATCH")
            elif any(outcome.line != candidate_line for outcome in pair.outcomes):
                pair_reasons.append("SETTLEMENT_RULE_MISMATCH")

        pair_reasons = list(dict.fromkeys(pair_reasons))
        if pair_reasons:
            excluded.append(
                ExcludedSource(
                    source_id=pair.source_id,
                    reason_codes=pair_reasons,
                    message="Comparison source failed exact identity, evidence, status, freshness, or pricing-origin gates.",
                )
            )
            continue

        candidate_outcome = matching[0]
        opposing_outcome = next(outcome for outcome in pair.outcomes if outcome is not candidate_outcome)
        candidate_numerator, candidate_denominator = _american_implied_ratio(
            candidate_outcome.american_odds
        )
        opposing_numerator, opposing_denominator = _american_implied_ratio(
            opposing_outcome.american_odds
        )
        candidate_cross_product = candidate_numerator * opposing_denominator
        opposing_cross_product = opposing_numerator * candidate_denominator
        fair_probability = candidate_cross_product / (
            candidate_cross_product + opposing_cross_product
        )
        included.append((pair, fair_probability, pair_age))
        seen_origins.add(pair.pricing_origin_id)

    source_probabilities = [
        SourceLevelProbability(
            source_id=pair.source_id,
            sportsbook_id=pair.sportsbook_id,
            pricing_origin_id=pair.pricing_origin_id,
            fair_probability=fair_probability,
        )
        for pair, fair_probability, _ in included
    ]
    comparison_times = [pair.retrieved_at_utc for pair, _, _ in included]
    collection_times = [target.retrieved_at_utc, *comparison_times]
    collection_skew = (
        int((max(collection_times) - min(collection_times)).total_seconds())
        if collection_times
        else None
    )
    oldest_comparison_age = max((age for _, _, age in included), default=None)
    if collection_skew is not None and collection_skew > 300:
        _append_blocker(blockers, _blocker("QUOTE_BATCH_UNSYNCHRONIZED", "Included quote timestamps exceed 300 seconds of skew.", candidate_id=candidate_id, field_path="comparison_pairs"))
    if len(included) < 2 or len(seen_origins) < 2:
        _append_blocker(blockers, _blocker("CONSENSUS_INSUFFICIENT", "Two complete independent non-target pricing origins are required.", candidate_id=candidate_id, field_path="comparison_pairs"))

    material_times = [
        fact.effective_at_utc
        for fact in candidate.material_context
        if fact.material
    ]
    if candidate.latest_material_context_at_utc is not None:
        material_times.append(candidate.latest_material_context_at_utc)
        if candidate.latest_material_context_at_utc not in {
            fact.effective_at_utc
            for fact in candidate.material_context
            if fact.material
        }:
            _append_blocker(blockers, _blocker("SOURCE_CONFLICT", "The latest material-context timestamp lacks a matching material fact.", candidate_id=candidate_id, field_path="latest_material_context_at_utc"))
    latest_material = max(material_times, default=None)
    post_material_change_synchronized = True
    if latest_material is not None and any(
        quote_time < latest_material for quote_time in collection_times
    ):
        post_material_change_synchronized = False
        _append_blocker(blockers, _blocker("MATERIAL_CONTEXT_NEWER_THAN_QUOTES", "A material context fact is newer than an affected quote.", candidate_id=candidate_id, field_path="latest_material_context_at_utc"))

    fair_values = [probability for _, probability, _ in included]
    dispersion = (
        (max(fair_values) - min(fair_values)) * Decimal(100)
        if fair_values
        else None
    )
    audit = ConsensusAudit(
        target_sportsbook_id=target.sportsbook_id,
        target_excluded=True,
        raw_source_count=len(candidate.comparison_pairs),
        usable_book_count=len(included),
        pricing_origin_group_count=len(seen_origins),
        aggregation_method_version=(
            "mlb_market_consensus_mean_v1"
            if request.profile_id == "mlb.player_hits"
            else "wnba_market_consensus_mean_v1"
        ),
        source_level_probabilities=source_probabilities,
        dispersion_percentage_points=dispersion,
        oldest_comparison_age_seconds=oldest_comparison_age,
        collection_skew_seconds=collection_skew,
        excluded_sources=excluded,
    )
    exclusion_reason_codes = list(
        dict.fromkeys(
            reason_code
            for excluded_source in excluded
            for reason_code in excluded_source.reason_codes
        )
    )
    if blockers:
        blocked_decision = _candidate_shell(
            candidate,
            blockers,
            target_age=target_age,
            post_material_change_synchronized=post_material_change_synchronized,
            consensus_audit=audit,
        )
        return blocked_decision.model_copy(
            update={
                "reason_codes": list(
                    dict.fromkeys(
                        [*blocked_decision.reason_codes, *exclusion_reason_codes]
                    )
                )
            }
        )

    with localcontext() as context:
        context.prec = 28
        base_decimal = _american_to_decimal(target.american_odds)
        boosted_decimal = _profit_only_boost(base_decimal, request.promotion.boost_percent or Decimal(0))
        break_even = Decimal(1) / boosted_decimal
        estimated_probability = sum(fair_values, Decimal(0)) / Decimal(len(fair_values))
        ev_per_unit = estimated_probability * boosted_decimal - Decimal(1)
        permitted_stake = min(
            value
            for value in (request.promotion.max_stake, request.user_max_stake)
            if value is not None
        )
        expected_dollars = permitted_stake * ev_per_unit

    state = CandidateState.ACTIONABLE_FOR_REVIEW if ev_per_unit > 0 else CandidateState.PASS
    reason_codes = list(exclusion_reason_codes)
    if ev_per_unit <= 0:
        reason_codes.append("EV_BELOW_THRESHOLD")
    return CandidateDecision(
        candidate_id=candidate_id,
        event_id=candidate.market_identity.event_id,
        participant_id=candidate.market_identity.participant_id,
        market_key=candidate.market_identity.canonical_market_key,
        market_identity=candidate.market_identity,
        side=candidate.market_identity.side,
        line=candidate.market_identity.line,
        target_american_odds=target.american_odds,
        boosted_decimal_odds=boosted_decimal,
        break_even_probability=break_even,
        estimated_probability=estimated_probability,
        probability_method="market_consensus",
        consensus_audit=audit,
        ev_per_unit=ev_per_unit,
        permitted_stake=permitted_stake,
        expected_dollars=expected_dollars,
        state=state,
        reason_codes=reason_codes,
        blockers=[],
        invalidation_conditions=[
            "Any promotion, quote, identity, settlement, market-status, or material-context change requires a new evaluation."
        ],
        monitoring_metadata=MonitoringMetadata(
            next_refresh_at=None,
            next_refresh_reason=None,
            post_material_change_synchronized=True,
        ),
        source_refs=list(
            dict.fromkeys(
                [target.evidence_id]
                + [pair.evidence_id for pair, _, _ in included]
                + [evidence.evidence_id for evidence in candidate.evidence]
            )
        ),
    )


def _rank_candidates(
    candidates: list[CandidateDecision],
    token_count: int,
) -> list[CandidateDecision]:
    valued = [candidate for candidate in candidates if candidate.expected_dollars is not None]
    valued.sort(key=lambda item: (-item.expected_dollars, item.candidate_id))
    ranks = {candidate.candidate_id: index for index, candidate in enumerate(valued, 1)}
    ranked: list[CandidateDecision] = []
    for candidate in candidates:
        update: dict[str, Any] = {"rank": ranks.get(candidate.candidate_id)}
        if candidate.expected_dollars is not None and candidate.expected_dollars > 0:
            candidate_rank = ranks[candidate.candidate_id]
            if candidate_rank > token_count:
                update.update(
                    state=CandidateState.PASS,
                    reason_codes=list(
                        dict.fromkeys(
                            [*candidate.reason_codes, "DOMINATED_BY_BETTER_TOKEN_USE"]
                        )
                    ),
                )
        ranked.append(candidate.model_copy(update=update))
    return sorted(
        ranked,
        key=lambda item: (
            item.rank is None,
            item.rank if item.rank is not None else 10**9,
            item.candidate_id,
        ),
    )


def evaluate_manual_promotion(
    request: ManualPromoEvaluationInput,
    catalog_path: Path = DEFAULT_CATALOG_PATH,
    source_registry_path: Path = DEFAULT_SOURCE_REGISTRY_PATH,
) -> PromotionDecisionBriefV2:
    """Evaluate credential-free manual evidence without network access or writes."""

    global_blockers: list[Blocker] = []
    try:
        catalog = _load_yaml(Path(catalog_path))
        registry = _load_yaml(Path(source_registry_path))
        profiles, adapters = _catalog_maps(catalog)
        source_ids, origin_status = _registry_maps(registry)
        global_blockers.extend(_global_blockers(request, profiles, adapters))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        profiles, adapters, source_ids, origin_status = {}, {}, set(), {}
        global_blockers.append(
            _blocker(
                "PROVIDER_FAILURE",
                f"Local catalog or source-registry validation failed: {exc}",
            )
        )

    if global_blockers:
        decisions = [
            _candidate_shell(
                candidate,
                [
                    blocker.model_copy(
                        update={"candidate_id": blocker.candidate_id or candidate.candidate_id}
                    )
                    for blocker in global_blockers
                ],
                target_age=max(
                    0,
                    _age_seconds(
                        request.created_at_utc,
                        candidate.target_quote.retrieved_at_utc,
                    ),
                ),
                post_material_change_synchronized=not bool(
                    candidate.material_context
                    or candidate.latest_material_context_at_utc is not None
                ),
            )
            for candidate in request.candidates
        ]
    else:
        decisions = [
            _evaluate_candidate(
                request,
                candidate,
                global_blockers,
                source_ids,
                origin_status,
            )
            for candidate in request.candidates
        ]
    decisions = _rank_candidates(decisions, request.promotion.token_count)

    run_blockers: list[Blocker] = []
    for blocker in global_blockers:
        _append_blocker(run_blockers, blocker)

    states = {decision.state for decision in decisions}
    if CandidateState.ACTIONABLE_FOR_REVIEW in states:
        overall_status = OverallStatus.ACTIONABLE_FOR_REVIEW
    elif CandidateState.WATCH in states:
        overall_status = OverallStatus.WATCH
    elif states and states <= {CandidateState.BLOCKED, CandidateState.INELIGIBLE}:
        overall_status = OverallStatus.BLOCKED
        for decision in decisions:
            for blocker in decision.blockers:
                _append_blocker(run_blockers, blocker)
    else:
        overall_status = OverallStatus.NO_QUALIFYING_CANDIDATE

    target_ages = [
        max(0, _age_seconds(request.created_at_utc, candidate.target_quote.retrieved_at_utc))
        for candidate in request.candidates
    ]
    material_ages = [
        max(0, _age_seconds(request.created_at_utc, fact.effective_at_utc))
        for candidate in request.candidates
        for fact in candidate.material_context
        if fact.material
    ]
    stale_inputs = list(
        dict.fromkeys(
            blocker.field_path or blocker.reason_code
            for blocker in run_blockers
            if blocker.reason_code
            in {
                "TARGET_QUOTE_STALE",
                "COMPARISON_QUOTE_STALE",
                "QUOTE_BATCH_UNSYNCHRONIZED",
                "MATERIAL_CONTEXT_NEWER_THAN_QUOTES",
            }
        )
    )
    qa_pass = not global_blockers and any(
        decision.state not in {CandidateState.BLOCKED, CandidateState.INELIGIBLE}
        for decision in decisions
    )
    return PromotionDecisionBriefV2(
        contract_version="promotion_decision_brief_v2",
        run=RunSummary(
            run_id=request.run_id,
            created_at_utc=request.created_at_utc,
            timezone=request.timezone,
            jurisdiction=request.jurisdiction,
            adapter_id=request.adapter_id,
            adapter_version=request.adapter_version,
            adapter_contract_version=request.adapter_contract_version,
            profile_id=request.profile_id,
            profile_lifecycle=request.profile_lifecycle,
            overall_status=overall_status,
        ),
        promotion=_promotion_summary(request),
        freshness=FreshnessSummary(
            target_quote_max_age_seconds=max(target_ages, default=None),
            oldest_material_input_age_seconds=max(material_ages, default=None),
            stale_inputs=stale_inputs,
        ),
        candidates=decisions,
        blockers=run_blockers,
        qa=QASummary(
            result="pass" if qa_pass else "fail",
            issues=[blocker.message for blocker in run_blockers],
        ),
        change_summary=ChangeSummary(),
    )
