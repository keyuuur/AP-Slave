from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict


class IssueCode(StrEnum):
    FILE_MISSING = "FILE_MISSING"
    YAML_PARSE_ERROR = "YAML_PARSE_ERROR"
    SCHEMA_INVALID = "SCHEMA_INVALID"
    CATALOG_COUNT_MISMATCH = "CATALOG_COUNT_MISMATCH"
    CATALOG_DUPLICATE_ID = "CATALOG_DUPLICATE_ID"
    CATALOG_REFERENCE_INVALID = "CATALOG_REFERENCE_INVALID"
    CATALOG_VERSION_MISMATCH = "CATALOG_VERSION_MISMATCH"
    CATALOG_ENUM_INVALID = "CATALOG_ENUM_INVALID"
    SOURCE_REFERENCE_INVALID = "SOURCE_REFERENCE_INVALID"
    SOURCE_POLICY_INVALID = "SOURCE_POLICY_INVALID"
    SOURCE_SEASON_INVALID = "SOURCE_SEASON_INVALID"
    SOURCE_JURISDICTION_INVALID = "SOURCE_JURISDICTION_INVALID"
    SOURCE_PERMISSION_INVALID = "SOURCE_PERMISSION_INVALID"
    PRICING_ORIGIN_INVALID = "PRICING_ORIGIN_INVALID"
    ADAPTER_SECTION_INVALID = "ADAPTER_SECTION_INVALID"
    MLB_MAPPING_INVALID = "MLB_MAPPING_INVALID"
    REFRESH_PHASE_INVALID = "REFRESH_PHASE_INVALID"
    LIFECYCLE_MISMATCH = "LIFECYCLE_MISMATCH"
    REASON_CODE_MISMATCH = "REASON_CODE_MISMATCH"
    SHARED_SIGNAL_REDEFINED = "SHARED_SIGNAL_REDEFINED"
    DISABLED_SCENARIO_MISSING_BLOCKER = "DISABLED_SCENARIO_MISSING_BLOCKER"
    MARKDOWN_FENCE_UNBALANCED = "MARKDOWN_FENCE_UNBALANCED"
    MARKDOWN_TABLE_INVALID = "MARKDOWN_TABLE_INVALID"
    LOCAL_LINK_BROKEN = "LOCAL_LINK_BROKEN"
    README_CATALOG_DRIFT = "README_CATALOG_DRIFT"
    EVIDENCE_TEMPLATE_INVALID = "EVIDENCE_TEMPLATE_INVALID"
    GITIGNORE_POLICY_INVALID = "GITIGNORE_POLICY_INVALID"


class ValidationIssue(BaseModel):
    """One deterministic, network-free repository validation finding."""

    model_config = ConfigDict(frozen=True)

    code: IssueCode
    message: str
    path: Path
    line: int | None = None
    severity: Literal["error", "warning"] = "error"

    def render(self, root: Path | None = None) -> str:
        display_path = self.path
        if root is not None:
            try:
                display_path = self.path.relative_to(root)
            except ValueError:
                pass
        location = f"{display_path}:{self.line}" if self.line else str(display_path)
        return f"{self.severity.upper()} {self.code.value} {location} - {self.message}"
