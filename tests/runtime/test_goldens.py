from __future__ import annotations

import json
from pathlib import Path
import shutil

import pytest

from ap_slave_runtime.cli import run
from ap_slave_runtime.engine import evaluate_manual_promotion
from ap_slave_runtime.models import ManualPromoEvaluation
from ap_slave_runtime.render import render_markdown

from tests.runtime.factories import write_runtime_contracts


HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"
GOLDENS = HERE / "goldens"


@pytest.mark.parametrize(
    ("fixture_name", "golden_stem"),
    [
        ("mlb_valid.json", "mlb_brief"),
        ("wnba_moneyline_valid.json", "wnba_moneyline_brief"),
    ],
)
def test_engine_json_and_markdown_goldens(
    fixture_name: str,
    golden_stem: str,
    tmp_path: Path,
) -> None:
    request = ManualPromoEvaluation.model_validate_json(
        (FIXTURES / fixture_name).read_text(encoding="utf-8")
    )
    catalog_path, registry_path = write_runtime_contracts(tmp_path, request)

    brief = evaluate_manual_promotion(request, catalog_path, registry_path)

    expected_json = json.loads(
        (GOLDENS / f"{golden_stem}.json").read_text(encoding="utf-8")
    )
    expected_markdown = (GOLDENS / f"{golden_stem}.md").read_text(
        encoding="utf-8"
    )
    assert brief.model_dump(mode="json") == expected_json
    assert render_markdown(brief) == expected_markdown


@pytest.mark.parametrize(
    ("fixture_name", "golden_stem"),
    [
        ("mlb_valid.json", "mlb_brief"),
        ("wnba_moneyline_valid.json", "wnba_moneyline_brief"),
    ],
)
def test_cli_writes_only_explicit_json_and_markdown_goldens(
    fixture_name: str,
    golden_stem: str,
    tmp_path: Path,
) -> None:
    request = ManualPromoEvaluation.model_validate_json(
        (FIXTURES / fixture_name).read_text(encoding="utf-8")
    )
    project_root = tmp_path / "project"
    adapter_dir = project_root / "SPORT_ADAPTERS"
    adapter_dir.mkdir(parents=True)
    catalog_path, registry_path = write_runtime_contracts(tmp_path / "contracts", request)
    shutil.copyfile(catalog_path, adapter_dir / "catalog.yaml")
    shutil.copyfile(registry_path, adapter_dir / "source_registry.yaml")
    input_path = tmp_path / fixture_name
    shutil.copyfile(FIXTURES / fixture_name, input_path)
    json_output = tmp_path / "brief.json"
    markdown_output = tmp_path / "brief.md"

    exit_code = run(
        [
            "--root",
            str(project_root),
            "--input",
            str(input_path),
            "--json-output",
            str(json_output),
            "--markdown-output",
            str(markdown_output),
        ]
    )

    assert exit_code == 0
    assert json.loads(json_output.read_text(encoding="utf-8")) == json.loads(
        (GOLDENS / f"{golden_stem}.json").read_text(encoding="utf-8")
    )
    assert markdown_output.read_text(encoding="utf-8") == (
        GOLDENS / f"{golden_stem}.md"
    ).read_text(encoding="utf-8")
    assert {path.name for path in tmp_path.iterdir()} == {
        "project",
        "contracts",
        fixture_name,
        "brief.json",
        "brief.md",
    }
