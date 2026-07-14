from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


Lifecycle = Literal[
    "active",
    "pilot_enabled",
    "disabled_provider_validation",
    "disabled_model_only",
    "retired",
]
ContractStatus = Literal["draft", "specified"]
ImplementationStatus = Literal[
    "documentation_only", "manual_input_runtime", "provider_integrated"
]
SourceReadiness = Literal[
    "provider_validation_pending", "per_run_evidence_required", "cross_timing_validated"
]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CatalogMetadata(StrictModel):
    title: str
    default_timezone: str
    adapter_record_count: int = Field(ge=0)
    profile_record_count: int = Field(ge=0)
    lifecycle_distribution: dict[str, int]


class CatalogVocabularies(StrictModel):
    profile_lifecycle: list[str]
    contract_status: list[str]
    implementation_status: list[str]
    source_readiness: list[str]


class AdapterRecord(StrictModel):
    adapter_id: str
    version: str
    contract_version: Literal["adapter_contract_v1"]
    sport_league: str
    authoritative_location: str
    run_mode: str
    probability_method: str


class ProfileRecord(StrictModel):
    profile_id: str
    adapter_id: str
    lifecycle: Lifecycle
    contract_status: ContractStatus
    implementation_status: ImplementationStatus
    source_readiness: SourceReadiness
    exact_current_boundary: str
    activation_blocker: str


class CatalogDocument(StrictModel):
    schema_version: Literal["adapter_catalog_v1"]
    catalog_metadata: CatalogMetadata
    closed_vocabularies: CatalogVocabularies
    catalog_rules: dict[str, str]
    adapters: list[AdapterRecord]
    profiles: list[ProfileRecord]


RecordType = Literal[
    "concrete_source", "source_class", "terms_source", "season_artifact", "event_pack"
]
AccessMode = Literal[
    "manual_on_demand",
    "user_supplied_manual_evidence",
    "documented_public_api",
    "licensed_feed",
    "unconfigured",
]
AutomationPermission = Literal[
    "permitted_with_conditions", "prohibited", "license_required", "unresolved"
]
PermissionStatus = Literal[
    "conditionally_reviewed", "source_specific_review_required", "unresolved"
]
CoverageStatus = Literal[
    "exact_scope_documented",
    "instance_required",
    "provider_validation_pending",
    "wrong_season",
    "supporting_only",
]
OriginResolution = Literal["resolved", "unresolved", "target_excluded"]


class RegistryMetadata(StrictModel):
    title: str
    default_jurisdiction: str
    created_on: str
    network_validation_performed: bool
    provider_certification_claimed: bool


class RegistryVocabularies(StrictModel):
    record_type: list[str]
    access_mode: list[str]
    automation_permission: list[str]
    permission_status: list[str]
    coverage_status: list[str]
    origin_resolution_status: list[str]


class PricingOriginGroup(StrictModel):
    pricing_origin_id: str
    canonical_name: str
    known_aliases: list[str]
    origin_resolution_status: OriginResolution
    certification_scope: str


class SourceFamily(StrictModel):
    source_family_id: str
    purpose: str


class SourceRecord(StrictModel):
    source_id: str
    source_family_id: str
    record_type: RecordType
    label: str
    url: str | None
    facts: list[str]
    authority_rank: int = Field(ge=1)
    access_mode: AccessMode
    automation_permission: AutomationPermission
    permission_status: PermissionStatus
    coverage_status: CoverageStatus
    jurisdiction_scope: str
    season_event_scope: str
    last_reviewed_on: str | None
    review_trigger: str
    health_check_method: str
    permitted_use: str
    prohibited_use: str
    terms_source_id: str | None


class SourcePolicy(StrictModel):
    policy_id: str
    source_ids: list[str]
    jurisdiction_scope: str
    season_scope: str
    status: str
    safeguard: str


class SourceRegistryDocument(StrictModel):
    schema_version: Literal["source_registry_v1"]
    registry_metadata: RegistryMetadata
    closed_vocabularies: RegistryVocabularies
    registry_rules: dict[str, str]
    pricing_origin_groups: list[PricingOriginGroup]
    source_families: list[SourceFamily]
    source_records: list[SourceRecord]
    policies: list[SourcePolicy]


class EvidencePrivacy(BaseModel):
    model_config = ConfigDict(extra="allow")

    credential_free: Literal[True]
    manifest_only: Literal[True]
    contains_raw_screenshots: Literal[False]
    contains_raw_payloads: Literal[False]
    contains_personal_data: Literal[False]
    contains_account_identifiers: Literal[False]
    contains_credentials_or_session_data: Literal[False]
    raw_evidence_committed_to_repository: Literal[False]
    hash_algorithm: Literal["sha256"]


class EvidenceItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    evidence_id: str | None
    source_id: str | None
    content_sha256: str | None


class SourceEvidenceBundleDocument(BaseModel):
    model_config = ConfigDict(extra="allow")

    schema_version: Literal["source_evidence_bundle_v1"]
    privacy_and_storage: EvidencePrivacy
    scope: dict[str, Any]
    event_identity: dict[str, Any]
    market_identity: dict[str, Any]
    settlement_identity: dict[str, Any]
    evidence_items: list[EvidenceItem]
    coverage_and_independence: dict[str, Any]
    authorization_boundary: dict[str, Any]
    review: dict[str, Any]


class GolfEventSourcePackDocument(BaseModel):
    model_config = ConfigDict(extra="allow")

    schema_version: Literal["golf_event_source_pack_v1"]
    privacy_and_storage: EvidencePrivacy
    jurisdiction_and_book: dict[str, Any]
    event_and_competition_identity: dict[str, Any]
    competition_rules: dict[str, Any]
    market_identity: dict[str, Any]
    promotion_and_eligibility: dict[str, Any]
    settlement_identity: dict[str, Any]
    required_evidence: dict[str, EvidenceItem]
    comparison_coverage: dict[str, Any]
    authorization_boundary: dict[str, Any]
    review: dict[str, Any]
