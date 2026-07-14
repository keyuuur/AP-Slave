from __future__ import annotations

from collections import Counter
from datetime import date
from pathlib import Path
import re
from typing import Any, Iterable

from pydantic import ValidationError
import yaml

from .models import IssueCode, ValidationIssue
from .schemas import (
    CatalogDocument,
    GolfEventSourcePackDocument,
    SourceEvidenceBundleDocument,
    SourceRegistryDocument,
)


CATALOG_PATH = Path("SPORT_ADAPTERS/catalog.yaml")
REGISTRY_PATH = Path("SPORT_ADAPTERS/source_registry.yaml")
README_PATH = Path("SPORT_ADAPTERS/README.md")
MONITORING_PATH = Path("PROMO_PLACEMENT_MONITORING_PLAYBOOK.md")
ANALYSIS_PATH = Path("PROMO_ANALYSIS_PLAYBOOK.md")
STANDALONE_ADAPTERS = (
    Path("SPORT_ADAPTERS/WNBA.md"),
    Path("SPORT_ADAPTERS/NBA.md"),
    Path("SPORT_ADAPTERS/NFL.md"),
    Path("SPORT_ADAPTERS/GOLF.md"),
)
EVIDENCE_TEMPLATES = {
    Path("evidence/templates/source_evidence_bundle.yaml"): SourceEvidenceBundleDocument,
    Path("evidence/templates/golf_event_source_pack.yaml"): GolfEventSourcePackDocument,
}
EXPECTED_PHASE_ORDER = (
    "intake",
    "distant_pregame",
    "official_release_window",
    "material_change",
    "shortlist_check",
    "final_sync",
)
EXPECTED_PHASES = set(EXPECTED_PHASE_ORDER)
EXPECTED_SECTION_ORDER = (
    "adapter_metadata",
    "profile_registry",
    "market_identity_settlement",
    "source_compliance",
    "signal_registry",
    "materiality_state",
    "refresh_policy",
    "tier_d_registry",
    "tier_x_exclusions",
    "provider_evidence",
    "contract_scenarios_fixtures",
    "run_decision_brief",
    "activation_change_log",
)
EXPECTED_SECTIONS = set(EXPECTED_SECTION_ORDER)
EXPECTED_LIFECYCLES = {
    "active",
    "pilot_enabled",
    "disabled_provider_validation",
    "disabled_model_only",
    "retired",
}
EXPECTED_CONTRACT_STATUSES = {"draft", "specified"}
EXPECTED_IMPLEMENTATION_STATUSES = {
    "documentation_only",
    "manual_input_runtime",
    "provider_integrated",
}
EXPECTED_SOURCE_READINESS = {
    "provider_validation_pending",
    "per_run_evidence_required",
    "cross_timing_validated",
}
SHARED_SIGNALS = {
    "promo_terms",
    "target_quote",
    "comparison_quotes_same_line",
    "market_status",
    "promo_expiration",
}
STATE_WORDS = {
    "ACTIONABLE_FOR_REVIEW",
    "BLOCKED",
    "CLEAR",
    "INELIGIBLE",
    "PASS",
    "WATCH",
}


def _issue(
    code: IssueCode,
    message: str,
    path: Path,
    *,
    line: int | None = None,
) -> ValidationIssue:
    return ValidationIssue(code=code, message=message, path=path, line=line)


def _read(root: Path, relative: Path, issues: list[ValidationIssue]) -> str | None:
    path = root / relative
    if not path.is_file():
        issues.append(_issue(IssueCode.FILE_MISSING, "required file is missing", path))
        return None
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        issues.append(_issue(IssueCode.FILE_MISSING, f"cannot read required file: {exc}", path))
        return None


def _load_yaml(
    root: Path,
    relative: Path,
    model: type[Any],
    issues: list[ValidationIssue],
) -> Any | None:
    text = _read(root, relative, issues)
    if text is None:
        return None
    try:
        raw = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        issues.append(_issue(IssueCode.YAML_PARSE_ERROR, f"invalid YAML: {exc}", root / relative))
        return None
    try:
        return model.model_validate(raw)
    except ValidationError as exc:
        code = IssueCode.SCHEMA_INVALID
        details = exc.errors()
        locations = [".".join(str(part) for part in error["loc"]) for error in details]
        if relative == CATALOG_PATH and any("lifecycle" in loc for loc in locations):
            code = IssueCode.CATALOG_ENUM_INVALID
        issues.append(
            _issue(
                code,
                f"schema validation failed at {', '.join(locations[:5])}: {exc.error_count()} error(s)",
                root / relative,
            )
        )
        return None


def _duplicates(values: Iterable[str]) -> set[str]:
    return {value for value, count in Counter(values).items() if count > 1}


def _validate_catalog(root: Path, catalog: CatalogDocument, issues: list[ValidationIssue]) -> None:
    path = root / CATALOG_PATH
    adapter_ids = [record.adapter_id for record in catalog.adapters]
    profile_ids = [record.profile_id for record in catalog.profiles]
    for duplicate in sorted(_duplicates(adapter_ids) | _duplicates(profile_ids)):
        issues.append(_issue(IssueCode.CATALOG_DUPLICATE_ID, f"duplicate catalog ID: {duplicate}", path))

    metadata = catalog.catalog_metadata
    if metadata.adapter_record_count != len(catalog.adapters):
        issues.append(_issue(IssueCode.CATALOG_COUNT_MISMATCH, "adapter_record_count does not match adapters", path))
    if metadata.profile_record_count != len(catalog.profiles):
        issues.append(_issue(IssueCode.CATALOG_COUNT_MISMATCH, "profile_record_count does not match profiles", path))
    actual_lifecycle = Counter(profile.lifecycle for profile in catalog.profiles)
    declared = metadata.lifecycle_distribution
    for lifecycle in EXPECTED_LIFECYCLES:
        if declared.get(lifecycle, 0) != actual_lifecycle.get(lifecycle, 0):
            issues.append(
                _issue(
                    IssueCode.CATALOG_COUNT_MISMATCH,
                    f"lifecycle distribution mismatch for {lifecycle}",
                    path,
                )
            )

    adapter_set = set(adapter_ids)
    for profile in catalog.profiles:
        if profile.adapter_id not in adapter_set:
            issues.append(
                _issue(
                    IssueCode.CATALOG_REFERENCE_INVALID,
                    f"profile {profile.profile_id} references unknown adapter {profile.adapter_id}",
                    path,
                )
            )

    vocab = catalog.closed_vocabularies
    expected_vocab = {
        "profile_lifecycle": EXPECTED_LIFECYCLES,
        "contract_status": EXPECTED_CONTRACT_STATUSES,
        "implementation_status": EXPECTED_IMPLEMENTATION_STATUSES,
        "source_readiness": EXPECTED_SOURCE_READINESS,
    }
    for name, expected in expected_vocab.items():
        if set(getattr(vocab, name)) != expected:
            issues.append(_issue(IssueCode.CATALOG_ENUM_INVALID, f"closed vocabulary drift: {name}", path))


def _adapter_section(text: str, number: int) -> str:
    start = text.find(f"<!-- adapter-section: {number} ")
    if start < 0:
        return ""
    end = text.find(f"<!-- adapter-section: {number + 1} ", start)
    return text[start:] if end < 0 else text[start:end]


def _table_first_cells(text: str) -> list[str]:
    return re.findall(r"^\|\s*`([^`]+)`\s*\|", text, re.MULTILINE)


def _validate_adapter_structure(root: Path, relative: Path, text: str, issues: list[ValidationIssue]) -> None:
    path = root / relative
    marker_pairs = re.findall(r"<!-- adapter-section:\s*(\d+)\s+([a-z0-9_]+)\s*-->", text)
    expected_pairs = [(str(index), name) for index, name in enumerate(EXPECTED_SECTION_ORDER, start=1)]
    if marker_pairs != expected_pairs:
        issues.append(
            _issue(
                IssueCode.ADAPTER_SECTION_INVALID,
                "adapter section numbers, names, and order must match adapter_contract_v1",
                path,
            )
        )
    phase_section = _adapter_section(text, 7)
    found_phases = _table_first_cells(phase_section)
    if found_phases != list(EXPECTED_PHASE_ORDER):
        detail = f"refresh phases must be exactly {', '.join(EXPECTED_PHASE_ORDER)}; found {', '.join(found_phases)}"
        issues.append(_issue(IssueCode.REFRESH_PHASE_INVALID, detail, path))

    shared_section = _adapter_section(text, 5)
    shared_rows = [cell for cell in _table_first_cells(shared_section) if cell in SHARED_SIGNALS]
    if Counter(shared_rows) != Counter({signal: 1 for signal in SHARED_SIGNALS}):
        issues.append(
            _issue(
                IssueCode.SHARED_SIGNAL_REDEFINED,
                "shared signals must be extended exactly once and may not be redefined",
                path,
            )
        )


def _validate_mlb_mapping(root: Path, text: str, issues: list[ValidationIssue]) -> None:
    path = root / MONITORING_PATH
    mapping_start = text.find("### 6.0 `adapter_contract_v1` logical validator mapping")
    mapping_end = text.find("### 6.1", mapping_start)
    mapping = text[mapping_start:mapping_end] if mapping_start >= 0 and mapping_end >= 0 else ""
    mapped = set(re.findall(r"^\|\s*\d+\s*\|\s*`([a-z0-9_]+)`", mapping, re.MULTILINE))
    if mapped != EXPECTED_SECTIONS:
        issues.append(_issue(IssueCode.MLB_MAPPING_INVALID, "MLB logical mapping must contain all 13 sections", path))
    phase_start = text.find("### 6.7")
    phase_end = text.find("### 6.8", phase_start)
    phase_text = text[phase_start:phase_end] if phase_start >= 0 and phase_end >= 0 else ""
    found = Counter(cell for cell in _table_first_cells(phase_text) if cell in EXPECTED_PHASES)
    invalid = sorted(phase for phase in EXPECTED_PHASES if found[phase] != 1)
    if invalid:
        issues.append(
            _issue(
                IssueCode.REFRESH_PHASE_INVALID,
                f"MLB refresh phases missing/not-once: {', '.join(invalid)}",
                path,
            )
        )


def _validate_versions(
    root: Path,
    catalog: CatalogDocument,
    texts: dict[Path, str],
    issues: list[ValidationIssue],
) -> None:
    for adapter in catalog.adapters:
        relative = Path(adapter.authoritative_location.split(",", 1)[0])
        text = texts.get(relative)
        if text is None:
            continue
        yaml_pattern = rf"adapter_id:\s*{re.escape(adapter.adapter_id)}\s*\n\s*version:\s*([^\s]+)"
        yaml_matches = re.findall(yaml_pattern, text)
        metadata = _adapter_section(text, 1)
        prose_id = re.search(r"\*\*Adapter ID:\*\*\s*`([^`]+)`", metadata)
        prose_version = re.search(r"\*\*Version:\*\*\s*`([^`]+)`", metadata)
        claims: list[tuple[str, str]] = [
            (adapter.adapter_id, version.strip('`"\'')) for version in yaml_matches
        ]
        if prose_id is not None or prose_version is not None:
            claims.append(
                (
                    prose_id.group(1) if prose_id is not None else "",
                    prose_version.group(1) if prose_version is not None else "",
                )
            )
        if not claims or any(
            claimed_id != adapter.adapter_id or claimed_version != adapter.version
            for claimed_id, claimed_version in claims
        ):
            issues.append(
                _issue(
                    IssueCode.CATALOG_VERSION_MISMATCH,
                    f"catalog version for {adapter.adapter_id} does not match authoritative document",
                    root / CATALOG_PATH,
                )
            )


def _validate_lifecycle_agreement(
    root: Path,
    catalog: CatalogDocument,
    texts: dict[Path, str],
    issues: list[ValidationIssue],
) -> None:
    for adapter in catalog.adapters:
        relative = Path(adapter.authoritative_location.split(",", 1)[0])
        text = texts.get(relative)
        if text is None:
            continue
        profiles = [profile for profile in catalog.profiles if profile.adapter_id == adapter.adapter_id]
        for profile in profiles:
            row_pattern = rf"^\|\s*`{re.escape(profile.profile_id)}`\s*\|\s*`{re.escape(profile.lifecycle)}`\s*\|"
            if re.search(row_pattern, text, re.MULTILINE) is None:
                issues.append(
                    _issue(
                        IssueCode.LIFECYCLE_MISMATCH,
                        f"{profile.profile_id} lifecycle does not match its authoritative profile table",
                        root / relative,
                    )
                )


def _validate_registry(root: Path, registry: SourceRegistryDocument, issues: list[ValidationIssue]) -> None:
    path = root / REGISTRY_PATH
    source_ids = [source.source_id for source in registry.source_records]
    family_ids = {family.source_family_id for family in registry.source_families}
    source_set = set(source_ids)
    for duplicate in sorted(_duplicates(source_ids)):
        issues.append(_issue(IssueCode.SOURCE_REFERENCE_INVALID, f"duplicate source ID: {duplicate}", path))
    for source in registry.source_records:
        if source.source_family_id not in family_ids:
            issues.append(_issue(IssueCode.SOURCE_REFERENCE_INVALID, f"{source.source_id} references unknown family", path))
        if source.terms_source_id and source.terms_source_id not in source_set:
            issues.append(_issue(IssueCode.SOURCE_REFERENCE_INVALID, f"{source.source_id} has unknown terms source", path))
        if source.last_reviewed_on:
            try:
                date.fromisoformat(source.last_reviewed_on)
            except ValueError:
                issues.append(_issue(IssueCode.SOURCE_POLICY_INVALID, f"{source.source_id} has invalid review date", path))
        permitted_api = (
            source.access_mode == "documented_public_api"
            and source.automation_permission == "permitted_with_conditions"
            and source.permission_status == "conditionally_reviewed"
        )
        if source.automation_permission == "permitted_with_conditions" and not permitted_api:
            issues.append(
                _issue(
                    IssueCode.SOURCE_PERMISSION_INVALID,
                    f"{source.source_id} permits automation without the documented-API review posture",
                    path,
                )
            )
        if source.access_mode == "licensed_feed" and source.automation_permission != "license_required":
            issues.append(
                _issue(
                    IssueCode.SOURCE_PERMISSION_INVALID,
                    f"{source.source_id} licensed feed must remain license_required",
                    path,
                )
            )
        if source.access_mode == "unconfigured" and source.automation_permission != "unresolved":
            issues.append(
                _issue(
                    IssueCode.SOURCE_PERMISSION_INVALID,
                    f"{source.source_id} unconfigured access must remain unresolved",
                    path,
                )
            )
        if (
            source.access_mode == "user_supplied_manual_evidence"
            and source.automation_permission != "prohibited"
        ):
            issues.append(
                _issue(
                    IssueCode.SOURCE_PERMISSION_INVALID,
                    f"{source.source_id} user-supplied evidence cannot authorize automation",
                    path,
                )
            )
    for policy in registry.policies:
        unknown = sorted(set(policy.source_ids) - source_set)
        if unknown:
            issues.append(_issue(IssueCode.SOURCE_REFERENCE_INVALID, f"{policy.policy_id} has unknown sources: {unknown}", path))

    by_id = {source.source_id: source for source in registry.source_records}
    season_requirements = {
        "nba_official_injury_report_2025_26": "wrong_season",
        "nfl_rulebook_2025": "wrong_season",
    }
    for source_id, required in season_requirements.items():
        source = by_id.get(source_id)
        if source is None or source.coverage_status != required:
            issues.append(
                _issue(
                    IssueCode.SOURCE_SEASON_INVALID,
                    f"{source_id} is a prior-season 2025-26 artifact and must remain {required}",
                    path,
                )
            )
    if registry.registry_metadata.default_jurisdiction != "US-MO":
        issues.append(_issue(IssueCode.SOURCE_JURISDICTION_INVALID, "default jurisdiction must be US-MO", path))
    golf_policy = next((p for p in registry.policies if p.policy_id == "golf_missouri_house_rules_v1"), None)
    if golf_policy is None or golf_policy.jurisdiction_scope != "US-MO":
        issues.append(_issue(IssueCode.SOURCE_JURISDICTION_INVALID, "Golf house-rule policy must be Missouri-specific", path))

    origins = registry.pricing_origin_groups
    origin_ids = [origin.pricing_origin_id for origin in origins]
    if _duplicates(origin_ids):
        issues.append(_issue(IssueCode.PRICING_ORIGIN_INVALID, "duplicate pricing-origin ID", path))
    required_origins = {
        "sportsbook_fanduel": "resolved",
        "sportsbook_draftkings": "resolved",
        "unresolved": "unresolved",
    }
    origin_map = {origin.pricing_origin_id: origin for origin in origins}
    for origin_id, status in required_origins.items():
        if origin_id not in origin_map or origin_map[origin_id].origin_resolution_status != status:
            issues.append(_issue(IssueCode.PRICING_ORIGIN_INVALID, f"{origin_id} must be {status}", path))
    aliases = [alias.casefold() for origin in origins for alias in origin.known_aliases]
    if _duplicates(aliases):
        issues.append(_issue(IssueCode.PRICING_ORIGIN_INVALID, "pricing-origin aliases must resolve uniquely", path))
    if "target" not in registry.registry_rules.get("target_exclusion", "").casefold():
        issues.append(_issue(IssueCode.PRICING_ORIGIN_INVALID, "registry must require target exclusion", path))


def _validate_source_references(
    root: Path,
    registry: SourceRegistryDocument,
    texts: dict[Path, str],
    issues: list[ValidationIssue],
) -> None:
    known = {source.source_id for source in registry.source_records}
    known.update(origin.pricing_origin_id for origin in registry.pricing_origin_groups)
    prefixes = ("source_class_", "sportsbook_", "nws_", "mlb_official_", "wnba_official_", "nba_official_", "nfl_official_", "nfl_flexible_", "nfl_important_", "nfl_rulebook_", "golf_official_", "pga_tour_", "fanduel_", "draftkings_")
    for relative in (*STANDALONE_ADAPTERS, MONITORING_PATH):
        text = texts.get(relative, "")
        tokens = set(re.findall(r"`([a-z][a-z0-9_]+)`", text))
        unresolved = sorted(token for token in tokens if token.startswith(prefixes) and token not in known)
        if unresolved:
            issues.append(
                _issue(
                    IssueCode.SOURCE_REFERENCE_INVALID,
                    f"unresolved source references: {', '.join(unresolved)}",
                    root / relative,
                )
            )


def _known_reason_codes(analysis_text: str) -> set[str]:
    start = analysis_text.find("## 9. Standard reason codes")
    end = analysis_text.find("## 10.", start)
    section = analysis_text[start:end] if start >= 0 and end >= 0 else ""
    return set(re.findall(r"`([A-Z][A-Z0-9_]+)`", section))


def _validate_reason_codes_and_disabled_scenarios(
    root: Path,
    catalog: CatalogDocument,
    analysis_text: str,
    texts: dict[Path, str],
    issues: list[ValidationIssue],
) -> None:
    known = _known_reason_codes(analysis_text)
    known_with_states = known | STATE_WORDS
    disabled_adapters = {
        adapter.adapter_id
        for adapter in catalog.adapters
        if all(
            profile.lifecycle.startswith("disabled_")
            for profile in catalog.profiles
            if profile.adapter_id == adapter.adapter_id
        )
    }
    adapter_by_path = {Path(adapter.authoritative_location.split(",", 1)[0]): adapter.adapter_id for adapter in catalog.adapters}
    for relative in (*STANDALONE_ADAPTERS, MONITORING_PATH):
        text = texts.get(relative, "")
        if relative == MONITORING_PATH:
            start = text.find("### 6.10")
            end = text.find("### 6.11", start)
            scenarios = text[start:end]
        else:
            scenarios = _adapter_section(text, 11)
        used = set(re.findall(r"`([A-Z][A-Z0-9_]+)`", scenarios))
        for unknown in sorted(used - known_with_states):
            issues.append(_issue(IssueCode.REASON_CODE_MISMATCH, f"unknown reason code {unknown}", root / relative))

        adapter_id = adapter_by_path.get(relative)
        all_disabled = adapter_id in disabled_adapters
        for line_number, line in enumerate(text.splitlines(), start=1):
            match = re.match(r"^\|\s*`([^`]+)`\s*\|", line)
            if not match:
                continue
            scenario_id = match.group(1)
            in_scenario = scenario_id in _table_first_cells(scenarios)
            requires = in_scenario and (all_disabled or scenario_id.startswith("wnba_player_"))
            if scenario_id == "nfl_fx_manual_placement":
                requires = False
            if requires and "ADAPTER_PROFILE_DISABLED" not in line:
                issues.append(
                    _issue(
                        IssueCode.DISABLED_SCENARIO_MISSING_BLOCKER,
                        f"disabled scenario {scenario_id} must retain ADAPTER_PROFILE_DISABLED",
                        root / relative,
                        line=line_number,
                    )
                )


def _validate_markdown(root: Path, issues: list[ValidationIssue]) -> None:
    for path in sorted(root.rglob("*.md")):
        if any(part in {".git", ".venv", ".pytest_cache"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        fence_open = False
        for line in text.splitlines():
            if re.match(r"^\s*```", line):
                fence_open = not fence_open
        if fence_open:
            issues.append(_issue(IssueCode.MARKDOWN_FENCE_UNBALANCED, "unbalanced Markdown fence", path))

        lines = text.splitlines()
        for index, line in enumerate(lines):
            if not line.lstrip().startswith("|"):
                continue
            block: list[tuple[int, str]] = []
            cursor = index
            while cursor < len(lines) and lines[cursor].lstrip().startswith("|"):
                block.append((cursor + 1, lines[cursor]))
                cursor += 1
            if len(block) < 2 or not re.match(r"^\s*\|?\s*:?-{3,}", block[1][1]):
                continue
            expected = block[0][1].count("|")
            for line_number, row in block[1:]:
                if row.count("|") != expected:
                    issues.append(_issue(IssueCode.MARKDOWN_TABLE_INVALID, "Markdown table row has inconsistent cell count", path, line=line_number))
            if cursor > index:
                # Outer loop repeats harmlessly; duplicate findings are removed later.
                pass

        for match in re.finditer(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text):
            target = match.group(1).strip().split("#", 1)[0]
            if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
                continue
            target = target.strip("<>")
            if not (path.parent / target).resolve().exists():
                issues.append(_issue(IssueCode.LOCAL_LINK_BROKEN, f"broken local link: {target}", path))


def _validate_readme_catalog(root: Path, catalog: CatalogDocument, readme: str, issues: list[ValidationIssue]) -> None:
    path = root / README_PATH
    for adapter in catalog.adapters:
        expected = f"| `{adapter.adapter_id}` | `{adapter.version}` | `{adapter.contract_version}` |"
        if expected not in readme:
            issues.append(_issue(IssueCode.README_CATALOG_DRIFT, f"adapter presentation drift: {adapter.adapter_id}", path))
    for profile in catalog.profiles:
        expected = f"| `{profile.profile_id}` | `{profile.adapter_id}` | `{profile.lifecycle}` |"
        if expected not in readme:
            issues.append(_issue(IssueCode.README_CATALOG_DRIFT, f"profile presentation drift: {profile.profile_id}", path))


def _validate_evidence_and_ignore(root: Path, issues: list[ValidationIssue]) -> None:
    for relative, model in EVIDENCE_TEMPLATES.items():
        before = len(issues)
        document = _load_yaml(root, relative, model, issues)
        if document is None:
            for index in range(before, len(issues)):
                if issues[index].path == root / relative:
                    message = issues[index].message
                    if "raw_evidence_committed_to_repository" in message:
                        message = "raw evidence must never be committed; template schema rejected the claim"
                    issues[index] = issues[index].model_copy(
                        update={"code": IssueCode.EVIDENCE_TEMPLATE_INVALID, "message": message}
                    )
            continue
        privacy = document.privacy_and_storage
        if privacy.raw_evidence_committed_to_repository is not False:
            issues.append(_issue(IssueCode.EVIDENCE_TEMPLATE_INVALID, "raw evidence must never be committed", root / relative))

    ignore_text = _read(root, Path(".gitignore"), issues)
    if ignore_text is None:
        return
    required = ("evidence/**", "data/screenshots/", "data/raw_evidence/")
    for rule in required:
        if not re.search(rf"(?m)^{re.escape(rule)}\s*$", ignore_text):
            issues.append(_issue(IssueCode.GITIGNORE_POLICY_INVALID, f"missing raw-evidence ignore rule: {rule}", root / ".gitignore"))
    if "!evidence/templates/**" not in ignore_text or "!evidence/manifests/**/*.yaml" not in ignore_text:
        issues.append(_issue(IssueCode.GITIGNORE_POLICY_INVALID, "safe template/manifest allowlist is incomplete", root / ".gitignore"))


def validate_repository(root: Path) -> list[ValidationIssue]:
    """Validate repository contracts without performing any network access."""

    root = Path(root).resolve()
    issues: list[ValidationIssue] = []
    catalog = _load_yaml(root, CATALOG_PATH, CatalogDocument, issues)
    registry = _load_yaml(root, REGISTRY_PATH, SourceRegistryDocument, issues)

    required_texts = {
        README_PATH,
        MONITORING_PATH,
        ANALYSIS_PATH,
        *STANDALONE_ADAPTERS,
    }
    texts: dict[Path, str] = {}
    for relative in required_texts:
        text = _read(root, relative, issues)
        if text is not None:
            texts[relative] = text

    if catalog is not None:
        _validate_catalog(root, catalog, issues)
        _validate_versions(root, catalog, texts, issues)
        _validate_lifecycle_agreement(root, catalog, texts, issues)
        readme = texts.get(README_PATH)
        if readme is not None:
            _validate_readme_catalog(root, catalog, readme, issues)
    for relative in STANDALONE_ADAPTERS:
        if relative in texts:
            _validate_adapter_structure(root, relative, texts[relative], issues)
    if MONITORING_PATH in texts:
        _validate_mlb_mapping(root, texts[MONITORING_PATH], issues)
    if registry is not None:
        _validate_registry(root, registry, issues)
        _validate_source_references(root, registry, texts, issues)
    if catalog is not None and ANALYSIS_PATH in texts:
        _validate_reason_codes_and_disabled_scenarios(root, catalog, texts[ANALYSIS_PATH], texts, issues)

    _validate_markdown(root, issues)
    _validate_evidence_and_ignore(root, issues)

    unique: dict[tuple[str, str, str, int | None], ValidationIssue] = {}
    for issue in issues:
        key = (issue.code.value, str(issue.path), issue.message, issue.line)
        unique[key] = issue
    return sorted(unique.values(), key=lambda item: (str(item.path), item.line or 0, item.code.value, item.message))
