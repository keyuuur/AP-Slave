from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from ap_slave_validation import IssueCode, ValidationIssue, validate_repository


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def repository_copy(tmp_path: Path) -> Path:
    destination = tmp_path / "repository"
    shutil.copytree(
        REPOSITORY_ROOT,
        destination,
        ignore=shutil.ignore_patterns(
            ".git",
            ".agents",
            ".codex",
            ".pytest_cache",
            "__pycache__",
            ".venv",
            "tmp",
        ),
    )
    return destination


def _read(root: Path, relative_path: str) -> str:
    return (root / relative_path).read_text(encoding="utf-8")


def _write(root: Path, relative_path: str, content: str) -> None:
    (root / relative_path).write_text(content, encoding="utf-8")


def _replace_once(root: Path, relative_path: str, old: str, new: str) -> None:
    content = _read(root, relative_path)
    assert content.count(old) == 1, f"mutation anchor is not unique: {relative_path}: {old!r}"
    _write(root, relative_path, content.replace(old, new, 1))


def _yaml_list_record(content: str, marker: str, next_marker: str) -> tuple[int, int]:
    start = content.index(marker)
    end = content.index(next_marker, start + len(marker))
    return start, end


def _duplicate_yaml_list_record(
    root: Path,
    relative_path: str,
    marker: str,
    next_marker: str,
) -> None:
    content = _read(root, relative_path)
    start, end = _yaml_list_record(content, marker, next_marker)
    record = content[start:end]
    _write(root, relative_path, content[:end] + record + content[end:])


def _remove_yaml_list_record(
    root: Path,
    relative_path: str,
    marker: str,
    next_marker: str,
) -> None:
    content = _read(root, relative_path)
    start, end = _yaml_list_record(content, marker, next_marker)
    _write(root, relative_path, content[:start] + content[end:])


def _replace_in_yaml_list_record(
    root: Path,
    relative_path: str,
    marker: str,
    next_marker: str,
    old: str,
    new: str,
) -> None:
    content = _read(root, relative_path)
    start, end = _yaml_list_record(content, marker, next_marker)
    record = content[start:end]
    assert record.count(old) == 1, f"record mutation anchor is not unique: {old!r}"
    record = record.replace(old, new, 1)
    _write(root, relative_path, content[:start] + record + content[end:])


def _remove_markdown_row(root: Path, relative_path: str, row_token: str) -> None:
    content = _read(root, relative_path)
    lines = content.splitlines(keepends=True)
    matches = [index for index, line in enumerate(lines) if row_token in line]
    assert len(matches) == 1, f"row mutation anchor is not unique: {row_token!r}"
    del lines[matches[0]]
    _write(root, relative_path, "".join(lines))


def _remove_from_markdown_row(
    root: Path,
    relative_path: str,
    row_token: str,
    value: str,
) -> None:
    content = _read(root, relative_path)
    lines = content.splitlines(keepends=True)
    matches = [index for index, line in enumerate(lines) if row_token in line]
    assert len(matches) == 1, f"row mutation anchor is not unique: {row_token!r}"
    line_index = matches[0]
    assert value in lines[line_index]
    lines[line_index] = lines[line_index].replace(value, "", 1)
    _write(root, relative_path, "".join(lines))


def _replace_in_markdown_row(
    root: Path,
    relative_path: str,
    row_token: str,
    old: str,
    new: str,
) -> None:
    content = _read(root, relative_path)
    lines = content.splitlines(keepends=True)
    matches = [index for index, line in enumerate(lines) if row_token in line]
    assert len(matches) == 1, f"row mutation anchor is not unique: {row_token!r}"
    line_index = matches[0]
    assert lines[line_index].count(old) == 1
    lines[line_index] = lines[line_index].replace(old, new, 1)
    _write(root, relative_path, "".join(lines))


def _assert_issue(
    issues: list[ValidationIssue],
    code: IssueCode,
    *,
    path_suffix: str | None = None,
    message_contains: str | None = None,
) -> ValidationIssue:
    matches = [issue for issue in issues if issue.code == code]
    if path_suffix is not None:
        normalized_suffix = Path(path_suffix).as_posix()
        matches = [
            issue
            for issue in matches
            if Path(issue.path).as_posix().endswith(normalized_suffix)
        ]
    if message_contains is not None:
        matches = [
            issue
            for issue in matches
            if message_contains.casefold() in issue.message.casefold()
        ]
    assert matches, (
        f"expected {code.value}; got "
        f"{[(issue.code.value, str(issue.path), issue.message) for issue in issues]}"
    )
    return matches[0]


def test_clean_repository_passes(repository_copy: Path) -> None:
    assert validate_repository(repository_copy) == []


def test_duplicate_profile_fails(repository_copy: Path) -> None:
    _duplicate_yaml_list_record(
        repository_copy,
        "SPORT_ADAPTERS/catalog.yaml",
        "  - profile_id: mlb.player_hits\n",
        "  - profile_id: wnba.full_game.moneyline\n",
    )

    issues = validate_repository(repository_copy)

    _assert_issue(
        issues,
        IssueCode.CATALOG_DUPLICATE_ID,
        path_suffix="SPORT_ADAPTERS/catalog.yaml",
        message_contains="mlb.player_hits",
    )


def test_missing_profile_fails(repository_copy: Path) -> None:
    _remove_yaml_list_record(
        repository_copy,
        "SPORT_ADAPTERS/catalog.yaml",
        "  - profile_id: mlb.player_hits\n",
        "  - profile_id: wnba.full_game.moneyline\n",
    )

    issues = validate_repository(repository_copy)

    _assert_issue(
        issues,
        IssueCode.CATALOG_COUNT_MISMATCH,
        path_suffix="SPORT_ADAPTERS/catalog.yaml",
    )


def test_invalid_lifecycle_fails(repository_copy: Path) -> None:
    _replace_once(
        repository_copy,
        "SPORT_ADAPTERS/catalog.yaml",
        "    lifecycle: active\n",
        "    lifecycle: unexpectedly_enabled\n",
    )

    issues = validate_repository(repository_copy)

    _assert_issue(
        issues,
        IssueCode.CATALOG_ENUM_INVALID,
        path_suffix="SPORT_ADAPTERS/catalog.yaml",
        message_contains="lifecycle",
    )


def test_catalog_adapter_version_mismatch_fails(repository_copy: Path) -> None:
    _replace_in_yaml_list_record(
        repository_copy,
        "SPORT_ADAPTERS/catalog.yaml",
        "  - adapter_id: wnba.pregame_full_game_v0_1\n",
        "  - adapter_id: nba.pregame_full_game_v0_1\n",
        "    version: 0.2.1\n",
        "    version: 9.9.9\n",
    )

    issues = validate_repository(repository_copy)

    _assert_issue(
        issues,
        IssueCode.CATALOG_VERSION_MISMATCH,
        path_suffix="SPORT_ADAPTERS/catalog.yaml",
        message_contains="wnba",
    )


def test_wrong_season_policy_cannot_be_marked_current(repository_copy: Path) -> None:
    _replace_in_yaml_list_record(
        repository_copy,
        "SPORT_ADAPTERS/source_registry.yaml",
        "  - source_id: nba_official_injury_report_2025_26\n",
        "  - source_id: nba_official_schedule\n",
        "    coverage_status: wrong_season\n",
        "    coverage_status: exact_scope_documented\n",
    )

    issues = validate_repository(repository_copy)

    _assert_issue(
        issues,
        IssueCode.SOURCE_SEASON_INVALID,
        path_suffix="SPORT_ADAPTERS/source_registry.yaml",
        message_contains="2025-26",
    )


def test_required_pricing_origin_cannot_be_unresolved(repository_copy: Path) -> None:
    _replace_in_yaml_list_record(
        repository_copy,
        "SPORT_ADAPTERS/source_registry.yaml",
        "  - pricing_origin_id: sportsbook_fanduel\n",
        "  - pricing_origin_id: sportsbook_draftkings\n",
        "    origin_resolution_status: resolved\n",
        "    origin_resolution_status: unresolved\n",
    )

    issues = validate_repository(repository_copy)

    _assert_issue(
        issues,
        IssueCode.PRICING_ORIGIN_INVALID,
        path_suffix="SPORT_ADAPTERS/source_registry.yaml",
        message_contains="sportsbook_fanduel",
    )


def test_missing_refresh_phase_fails(repository_copy: Path) -> None:
    _remove_markdown_row(
        repository_copy,
        "SPORT_ADAPTERS/NBA.md",
        "| `final_sync` |",
    )

    issues = validate_repository(repository_copy)

    _assert_issue(
        issues,
        IssueCode.REFRESH_PHASE_INVALID,
        path_suffix="SPORT_ADAPTERS/NBA.md",
        message_contains="final_sync",
    )


def test_adapter_section_number_name_swap_fails(repository_copy: Path) -> None:
    _replace_once(
        repository_copy,
        "SPORT_ADAPTERS/NBA.md",
        "<!-- adapter-section: 2 profile_registry -->",
        "<!-- adapter-section: 2 market_identity_settlement -->",
    )
    _replace_once(
        repository_copy,
        "SPORT_ADAPTERS/NBA.md",
        "<!-- adapter-section: 3 market_identity_settlement -->",
        "<!-- adapter-section: 3 profile_registry -->",
    )

    issues = validate_repository(repository_copy)

    _assert_issue(
        issues,
        IssueCode.ADAPTER_SECTION_INVALID,
        path_suffix="SPORT_ADAPTERS/NBA.md",
    )


def test_contradictory_prose_adapter_version_fails(repository_copy: Path) -> None:
    _replace_once(
        repository_copy,
        "SPORT_ADAPTERS/NBA.md",
        "**Version:** `0.1.1`",
        "**Version:** `9.9.9`",
    )

    issues = validate_repository(repository_copy)

    _assert_issue(
        issues,
        IssueCode.CATALOG_VERSION_MISMATCH,
        path_suffix="SPORT_ADAPTERS/catalog.yaml",
        message_contains="nba",
    )


def test_unexpected_seventh_refresh_phase_fails(repository_copy: Path) -> None:
    content = _read(repository_copy, "SPORT_ADAPTERS/NBA.md")
    anchor = "| `final_sync` |"
    line_start = content.index(anchor)
    line_end = content.index("\n", line_start) + 1
    extra = "| `unexpected_phase` | unsupported | unsupported | unsupported | `BLOCKED` | none |\n"
    _write(
        repository_copy,
        "SPORT_ADAPTERS/NBA.md",
        content[:line_end] + extra + content[line_end:],
    )

    issues = validate_repository(repository_copy)

    _assert_issue(
        issues,
        IssueCode.REFRESH_PHASE_INVALID,
        path_suffix="SPORT_ADAPTERS/NBA.md",
        message_contains="unexpected_phase",
    )


def test_unbalanced_markdown_fence_fails(repository_copy: Path) -> None:
    readme = _read(repository_copy, "README.md")
    _write(repository_copy, "README.md", readme + "\n```text\nunclosed test fence\n")

    issues = validate_repository(repository_copy)

    _assert_issue(
        issues,
        IssueCode.MARKDOWN_FENCE_UNBALANCED,
        path_suffix="README.md",
    )


def test_malformed_markdown_table_fails(repository_copy: Path) -> None:
    readme = _read(repository_copy, "README.md")
    malformed_table = "\n| left | right |\n|---|---|\n| missing cell |\n"
    _write(repository_copy, "README.md", readme + malformed_table)

    issues = validate_repository(repository_copy)

    _assert_issue(
        issues,
        IssueCode.MARKDOWN_TABLE_INVALID,
        path_suffix="README.md",
    )


def test_broken_local_markdown_link_fails(repository_copy: Path) -> None:
    readme = _read(repository_copy, "README.md")
    _write(
        repository_copy,
        "README.md",
        readme + "\n[missing local validator artifact](docs/does-not-exist.md)\n",
    )

    issues = validate_repository(repository_copy)

    _assert_issue(
        issues,
        IssueCode.LOCAL_LINK_BROKEN,
        path_suffix="README.md",
        message_contains="does-not-exist.md",
    )


def test_unknown_reason_code_fails(repository_copy: Path) -> None:
    _replace_in_markdown_row(
        repository_copy,
        "SPORT_ADAPTERS/NBA.md",
        "`nba_points_over_20_push`",
        "`PUSH_MODEL_UNAVAILABLE` and `ADAPTER_PROFILE_DISABLED`",
        "`NOT_A_REGISTERED_REASON` and `ADAPTER_PROFILE_DISABLED`",
    )

    issues = validate_repository(repository_copy)

    _assert_issue(
        issues,
        IssueCode.REASON_CODE_MISMATCH,
        path_suffix="SPORT_ADAPTERS/NBA.md",
        message_contains="NOT_A_REGISTERED_REASON",
    )


def test_disabled_scenario_requires_disabled_blocker(repository_copy: Path) -> None:
    _remove_from_markdown_row(
        repository_copy,
        "SPORT_ADAPTERS/NBA.md",
        "`nba_points_20_plus_equivalent`",
        "`ADAPTER_PROFILE_DISABLED`",
    )

    issues = validate_repository(repository_copy)

    _assert_issue(
        issues,
        IssueCode.DISABLED_SCENARIO_MISSING_BLOCKER,
        path_suffix="SPORT_ADAPTERS/NBA.md",
        message_contains="nba_points_20_plus_equivalent",
    )


def test_raw_evidence_ignore_policy_is_required(repository_copy: Path) -> None:
    _replace_once(
        repository_copy,
        ".gitignore",
        "evidence/**\n",
        "",
    )

    issues = validate_repository(repository_copy)

    _assert_issue(
        issues,
        IssueCode.GITIGNORE_POLICY_INVALID,
        path_suffix=".gitignore",
        message_contains="evidence",
    )


def test_evidence_template_cannot_claim_raw_evidence_is_committed(
    repository_copy: Path,
) -> None:
    _replace_once(
        repository_copy,
        "evidence/templates/source_evidence_bundle.yaml",
        "  raw_evidence_committed_to_repository: false\n",
        "  raw_evidence_committed_to_repository: true\n",
    )

    issues = validate_repository(repository_copy)

    _assert_issue(
        issues,
        IssueCode.EVIDENCE_TEMPLATE_INVALID,
        path_suffix="evidence/templates/source_evidence_bundle.yaml",
        message_contains="raw evidence",
    )
