from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from enum import StrEnum
from typing import Annotated, Any, Literal

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    PlainSerializer,
    field_validator,
)


def _decimal_from_string(value: Any) -> Decimal:
    if isinstance(value, Decimal):
        result = value
    elif isinstance(value, str):
        try:
            result = Decimal(value)
        except InvalidOperation as exc:
            raise ValueError("must be a decimal string") from exc
    else:
        raise ValueError("recommendation-grade decimal values must be JSON strings")
    if not result.is_finite():
        raise ValueError("decimal value must be finite")
    return result


def _serialize_decimal(value: Decimal) -> str:
    return format(value, "f")


def _utc_datetime(value: Any) -> datetime:
    if isinstance(value, str):
        normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
        try:
            parsed = datetime.fromisoformat(normalized)
        except ValueError as exc:
            raise ValueError("must be an ISO-8601 datetime") from exc
    elif isinstance(value, datetime):
        parsed = value
    else:
        raise ValueError("must be a timezone-aware UTC datetime")
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("datetime must include a timezone offset")
    if parsed.utcoffset().total_seconds() != 0:
        raise ValueError("datetime must use UTC")
    return parsed.astimezone(timezone.utc)


def _serialize_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


DecimalString = Annotated[
    Decimal,
    BeforeValidator(_decimal_from_string),
    PlainSerializer(_serialize_decimal, return_type=str),
]
UTCDateTime = Annotated[
    datetime,
    BeforeValidator(_utc_datetime),
    PlainSerializer(_serialize_utc, return_type=str),
]


class StrictContractModel(BaseModel):
    # Closed enums, explicit validators, and forbidden extra keys make the
    # external contract strict while still allowing ordinary JSON strings to
    # populate enum fields.
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class ProfileLifecycle(StrEnum):
    ACTIVE = "active"
    PILOT_ENABLED = "pilot_enabled"
    DISABLED_PROVIDER_VALIDATION = "disabled_provider_validation"
    DISABLED_MODEL_ONLY = "disabled_model_only"
    RETIRED = "retired"


class CandidateState(StrEnum):
    ACTIONABLE_FOR_REVIEW = "actionable_for_review"
    WATCH = "watch"
    PASS = "pass"
    BLOCKED = "blocked"
    INELIGIBLE = "ineligible"


class OverallStatus(StrEnum):
    ACTIONABLE_FOR_REVIEW = "actionable_for_review"
    WATCH = "watch"
    NO_QUALIFYING_CANDIDATE = "no_qualifying_candidate"
    BLOCKED = "blocked"


class MarketStatus(StrEnum):
    OPEN = "open"
    SUSPENDED = "suspended"
    CLOSED = "closed"
    UNKNOWN = "unknown"


class VerificationStatus(StrEnum):
    CONFIRMED = "confirmed"
    NEEDS_REVIEW = "needs_review"


class MarketIdentity(StrictContractModel):
    jurisdiction: Literal["US-MO"]
    league: str = Field(min_length=1)
    event_id: str = Field(min_length=1)
    participant_id: str | None = None
    raw_market_label: str = Field(min_length=1)
    raw_selection_label: str = Field(min_length=1)
    canonical_market_key: str = Field(min_length=1)
    outcome_set_id: str = Field(min_length=1)
    outcome_set_type: Literal["binary_pair"]
    outcome_set_completeness: Literal["complete", "incomplete", "unknown"]
    participant_set_version: str | None = None
    market_wrapper: str = Field(min_length=1)
    side: str = Field(min_length=1)
    line: DecimalString | None = None
    period: str = Field(min_length=1)
    overtime_or_extra_innings_treatment: Literal["included", "excluded", "unknown"]
    push_behavior: Literal["impossible", "push", "unknown"]
    tie_or_dead_heat_treatment: str = Field(min_length=1)
    participation_rule: str = Field(min_length=1)
    void_rule: str = Field(min_length=1)
    stat_counting_rule: str = Field(min_length=1)
    settlement_rule: str = Field(min_length=1)
    ap_frankenstein_compatibility: Literal[
        "direct", "equivalent_but_not_supported", "unsupported"
    ]


class EvidenceReference(StrictContractModel):
    evidence_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    source_instance_id: str | None = None
    jurisdiction: Literal["US-MO"]
    captured_at_utc: UTCDateTime
    provider_published_at_utc: UTCDateTime | None = None
    content_sha256: str = Field(pattern=r"^[0-9a-fA-F]{64}$")
    source_permission_reviewed: bool
    verification_status: VerificationStatus


class TargetQuoteInput(StrictContractModel):
    source_id: str = Field(min_length=1)
    sportsbook_id: str = Field(min_length=1)
    pricing_origin_id: str = Field(min_length=1)
    jurisdiction: Literal["US-MO"]
    american_odds: int
    market_status: MarketStatus
    retrieved_at_utc: UTCDateTime
    provider_last_update_utc: UTCDateTime | None = None
    evidence_id: str = Field(min_length=1)

    @field_validator("american_odds")
    @classmethod
    def american_odds_are_valid(cls, value: int) -> int:
        if value == 0 or -99 <= value <= 99:
            raise ValueError("American odds must be <= -100 or >= +100")
        return value


class ComparisonOutcomeInput(StrictContractModel):
    outcome_id: str = Field(min_length=1)
    raw_selection_label: str = Field(min_length=1)
    side: str = Field(min_length=1)
    line: DecimalString | None = None
    american_odds: int

    @field_validator("american_odds")
    @classmethod
    def american_odds_are_valid(cls, value: int) -> int:
        if value == 0 or -99 <= value <= 99:
            raise ValueError("American odds must be <= -100 or >= +100")
        return value


class ComparisonBinaryPairInput(StrictContractModel):
    source_id: str = Field(min_length=1)
    sportsbook_id: str = Field(min_length=1)
    pricing_origin_id: str = Field(min_length=1)
    jurisdiction: Literal["US-MO"]
    market_identity: MarketIdentity
    outcomes: list[ComparisonOutcomeInput] = Field(min_length=2, max_length=2)
    market_status: MarketStatus
    retrieved_at_utc: UTCDateTime
    provider_last_update_utc: UTCDateTime | None = None
    evidence_id: str = Field(min_length=1)


class MaterialContextFactInput(StrictContractModel):
    fact_id: str = Field(min_length=1)
    signal_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    effective_at_utc: UTCDateTime
    captured_at_utc: UTCDateTime
    verification_status: Literal["confirmed", "probable", "unconfirmed", "conflicting"]
    material: bool
    summary: str = Field(min_length=1)
    evidence_id: str = Field(min_length=1)


class ManualCandidateInput(StrictContractModel):
    candidate_id: str = Field(min_length=1)
    market_identity: MarketIdentity
    target_quote: TargetQuoteInput
    comparison_pairs: list[ComparisonBinaryPairInput] = Field(default_factory=list)
    material_context: list[MaterialContextFactInput] = Field(default_factory=list)
    latest_material_context_at_utc: UTCDateTime | None = None
    evidence: list[EvidenceReference] = Field(min_length=1)


class PromotionInput(StrictContractModel):
    promo_id: str = Field(min_length=1)
    sportsbook_id: str = Field(min_length=1)
    jurisdiction: Literal["US-MO"]
    raw_promotion_text: str = Field(min_length=1)
    boost_type: Literal[
        "profit_boost",
        "odds_boost",
        "payout_boost",
        "bonus_bet",
        "insured_bet",
        "parlay_boost",
        "other",
    ]
    boost_percent: DecimalString | None = None
    max_stake: DecimalString
    payout_cap: DecimalString | None = None
    minimum_american_odds: int | None = None
    maximum_american_odds: int | None = None
    odds_range_basis: Literal["base_odds", "boosted_odds", "unknown"]
    eligible_event_ids: list[str] = Field(min_length=1)
    eligible_market_keys: list[str] = Field(min_length=1)
    expires_at_utc: UTCDateTime
    token_count: int = Field(default=1, ge=1)
    void_push_rules: str = Field(min_length=1)
    verification_status: VerificationStatus
    ambiguities: list[str] = Field(default_factory=list)


class ManualPromoEvaluationInput(StrictContractModel):
    contract_version: Literal["manual_promo_evaluation_v1"]
    run_id: str = Field(min_length=1)
    created_at_utc: UTCDateTime
    timezone: Literal["America/Chicago"]
    jurisdiction: Literal["US-MO"]
    adapter_id: str = Field(min_length=1)
    adapter_version: str = Field(pattern=r"^\d+\.\d+\.\d+$")
    adapter_contract_version: Literal["adapter_contract_v1"]
    profile_id: str = Field(min_length=1)
    profile_lifecycle: ProfileLifecycle
    promotion: PromotionInput
    candidates: list[ManualCandidateInput] = Field(min_length=1)
    audit_evidence: list[EvidenceReference] = Field(default_factory=list)
    user_max_stake: DecimalString | None = None


class Blocker(StrictContractModel):
    reason_code: str = Field(pattern=r"^[A-Z][A-Z0-9_]+$")
    message: str = Field(min_length=1)
    candidate_id: str | None = None
    field_path: str | None = None


class RunSummary(StrictContractModel):
    run_id: str
    created_at_utc: UTCDateTime
    timezone: Literal["America/Chicago"]
    jurisdiction: Literal["US-MO"]
    adapter_id: str
    adapter_version: str
    adapter_contract_version: Literal["adapter_contract_v1"]
    profile_id: str
    profile_lifecycle: ProfileLifecycle
    overall_status: OverallStatus


class PromotionSummary(StrictContractModel):
    promo_id: str
    sportsbook_id: str
    jurisdiction: Literal["US-MO"]
    boost_type: str
    boost_percent: DecimalString | None
    max_stake: DecimalString
    expires_at_utc: UTCDateTime
    verification_status: VerificationStatus
    ambiguities: list[str]


class FreshnessSummary(StrictContractModel):
    target_quote_max_age_seconds: int | None = Field(default=None, ge=0)
    oldest_material_input_age_seconds: int | None = Field(default=None, ge=0)
    stale_inputs: list[str] = Field(default_factory=list)


class SourceLevelProbability(StrictContractModel):
    source_id: str
    sportsbook_id: str
    pricing_origin_id: str
    fair_probability: DecimalString


class ExcludedSource(StrictContractModel):
    source_id: str
    reason_codes: list[str]
    message: str


class ConsensusAudit(StrictContractModel):
    target_sportsbook_id: str
    target_excluded: bool
    raw_source_count: int = Field(ge=0)
    usable_book_count: int = Field(ge=0)
    pricing_origin_group_count: int = Field(ge=0)
    aggregation_method_version: str | None = None
    source_level_probabilities: list[SourceLevelProbability] = Field(default_factory=list)
    dispersion_percentage_points: DecimalString | None = None
    oldest_comparison_age_seconds: int | None = Field(default=None, ge=0)
    collection_skew_seconds: int | None = Field(default=None, ge=0)
    excluded_sources: list[ExcludedSource] = Field(default_factory=list)


class MonitoringMetadata(StrictContractModel):
    next_refresh_at: UTCDateTime | None = None
    next_refresh_reason: str | None = None
    post_material_change_synchronized: bool


class CandidateDecision(StrictContractModel):
    candidate_id: str
    rank: int | None = Field(default=None, ge=1)
    event_id: str
    participant_id: str | None = None
    market_key: str
    market_identity: MarketIdentity
    side: str
    line: DecimalString | None = None
    target_american_odds: int
    boosted_decimal_odds: DecimalString | None = None
    break_even_probability: DecimalString | None = None
    estimated_probability: DecimalString | None = None
    probability_low: DecimalString | None = None
    probability_method: Literal["market_consensus"] | None = None
    calculation_version: str | None = None
    consensus_audit: ConsensusAudit
    ev_per_unit: DecimalString | None = None
    conservative_ev_per_unit: DecimalString | None = None
    permitted_stake: DecimalString | None = None
    expected_dollars: DecimalString | None = None
    data_quality_score: DecimalString | None = None
    state: CandidateState
    reason_codes: list[str]
    blockers: list[Blocker] = Field(default_factory=list)
    invalidation_conditions: list[str]
    monitoring_metadata: MonitoringMetadata
    source_refs: list[str]


class QASummary(StrictContractModel):
    result: Literal["pass", "fail"]
    issues: list[str]


class ChangeSummary(StrictContractModel):
    prior_run_id: str | None = None
    material_change: bool = False
    changes: list[str] = Field(default_factory=list)


class PromotionDecisionBriefV2(StrictContractModel):
    contract_version: Literal["promotion_decision_brief_v2"]
    run: RunSummary
    promotion: PromotionSummary
    freshness: FreshnessSummary
    candidates: list[CandidateDecision]
    blockers: list[Blocker] = Field(default_factory=list)
    qa: QASummary
    change_summary: ChangeSummary
    human_boundary: Literal["No wager has been placed or confirmed."] = (
        "No wager has been placed or confirmed."
    )


class RuntimeValidationFailure(StrictContractModel):
    contract_version: Literal["manual_promo_evaluation_error_v1"] = (
        "manual_promo_evaluation_error_v1"
    )
    overall_status: Literal["blocked"] = "blocked"
    blockers: list[Blocker] = Field(min_length=1)
    human_boundary: Literal["No wager has been placed or confirmed."] = (
        "No wager has been placed or confirmed."
    )


# Compatibility aliases for engine and downstream imports.
ManualPromoEvaluation = ManualPromoEvaluationInput
ManualPromoEvaluationRequest = ManualPromoEvaluationInput
PromotionDecisionBrief = PromotionDecisionBriefV2
