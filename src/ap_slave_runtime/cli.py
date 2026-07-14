from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from pydantic import ValidationError

from .models import (
    Blocker,
    ManualPromoEvaluationInput,
    PromotionDecisionBriefV2,
    RuntimeValidationFailure,
)
from .render import render_markdown


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ap-slave-evaluate",
        description=(
            "Evaluate one credential-free manual promotion JSON file. "
            "The command performs no network or sportsbook access."
        ),
    )
    parser.add_argument(
        "--root",
        type=Path,
        required=True,
        help="Project root containing SPORT_ADAPTERS/catalog.yaml and source_registry.yaml.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Input JSON conforming to manual_promo_evaluation_v1.",
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        help="Explicit destination for promotion_decision_brief_v2 JSON.",
    )
    parser.add_argument(
        "--markdown-output",
        type=Path,
        help="Explicit destination for the concise Markdown brief.",
    )
    return parser


def _reason_code_for_location(location: tuple[object, ...]) -> str:
    parts = tuple(str(part) for part in location)
    joined = ".".join(parts)
    if "jurisdiction" in parts:
        return "JURISDICTION_MISMATCH"
    if any(
        marker in joined
        for marker in (
            "settlement_rule",
            "participation_rule",
            "void_rule",
            "stat_counting_rule",
            "overtime_or_extra_innings_treatment",
            "tie_or_dead_heat_treatment",
        )
    ):
        return "SETTLEMENT_RULE_MISMATCH"
    if "push_behavior" in joined:
        return "PUSH_MODEL_UNAVAILABLE"
    if parts and (parts[0] == "candidates" or "market_identity" in parts):
        return "MARKET_IDENTITY_MISMATCH"
    return "PROMO_TERMS_AMBIGUOUS"


def _validation_failure(error: ValidationError) -> RuntimeValidationFailure:
    blockers: list[Blocker] = []
    seen: set[tuple[str, str, str]] = set()
    ordered_errors = sorted(error.errors(include_url=False), key=lambda row: tuple(map(str, row["loc"])))
    for row in ordered_errors:
        location = tuple(row["loc"])
        field_path = ".".join(str(part) for part in location) or "$"
        reason_code = _reason_code_for_location(location)
        message = f"Invalid manual input at {field_path}: {row['msg']}."
        key = (reason_code, field_path, message)
        if key in seen:
            continue
        seen.add(key)
        candidate_id = None
        if len(location) > 1 and location[0] == "candidates" and isinstance(location[1], int):
            candidate_id = f"candidate_index:{location[1]}"
        blockers.append(
            Blocker(
                reason_code=reason_code,
                message=message,
                candidate_id=candidate_id,
                field_path=field_path,
            )
        )
    return RuntimeValidationFailure(blockers=blockers)


def _single_failure(
    reason_code: str,
    message: str,
    *,
    field_path: str | None = None,
) -> RuntimeValidationFailure:
    return RuntimeValidationFailure(
        blockers=[
            Blocker(
                reason_code=reason_code,
                message=message,
                field_path=field_path,
            )
        ]
    )


def _json_text(result: PromotionDecisionBriefV2 | RuntimeValidationFailure) -> str:
    return result.model_dump_json(indent=2) + "\n"


def _write_outputs(
    result: PromotionDecisionBriefV2 | RuntimeValidationFailure,
    *,
    json_output: Path | None,
    markdown_output: Path | None,
) -> None:
    if json_output is None:
        sys.stdout.write(_json_text(result))
    else:
        json_output.write_text(_json_text(result), encoding="utf-8", newline="\n")
    if markdown_output is not None:
        markdown_output.write_text(
            render_markdown(result), encoding="utf-8", newline="\n"
        )


def _resolved(path: Path) -> Path:
    return path.expanduser().resolve()


def _validate_paths(args: argparse.Namespace) -> tuple[Path, Path, Path, Path | None, Path | None]:
    root = _resolved(args.root)
    input_path = _resolved(args.input)
    catalog_path = root / "SPORT_ADAPTERS" / "catalog.yaml"
    source_registry_path = root / "SPORT_ADAPTERS" / "source_registry.yaml"
    json_output = _resolved(args.json_output) if args.json_output else None
    markdown_output = _resolved(args.markdown_output) if args.markdown_output else None

    if not root.is_dir():
        raise OSError("The explicit project root is not a directory.")
    if not input_path.is_file():
        raise OSError("The explicit input JSON path is not a file.")
    if not catalog_path.is_file() or not source_registry_path.is_file():
        raise OSError("The project root does not contain the canonical catalog and source registry.")

    protected = {root, input_path, catalog_path.resolve(), source_registry_path.resolve()}
    outputs = [path for path in (json_output, markdown_output) if path is not None]
    if len(set(outputs)) != len(outputs):
        raise OSError("JSON and Markdown output paths must be different.")
    if any(path in protected for path in outputs):
        raise OSError("An output path cannot overwrite the input, project root, catalog, or source registry.")
    for output in outputs:
        if not output.parent.is_dir():
            raise OSError("Every explicit output path must have an existing parent directory.")

    return root, input_path, catalog_path, source_registry_path, json_output, markdown_output


def run(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)

    try:
        (
            _root,
            input_path,
            catalog_path,
            source_registry_path,
            json_output,
            markdown_output,
        ) = _validate_paths(args)
    except OSError as exc:
        failure = _single_failure("PROVIDER_FAILURE", str(exc), field_path="$path")
        sys.stderr.write(_json_text(failure))
        return 2

    try:
        raw_input = json.loads(input_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        failure = _single_failure(
            "PROMO_TERMS_AMBIGUOUS",
            "The explicit input file is not readable UTF-8 JSON.",
            field_path="$",
        )
        try:
            _write_outputs(
                failure,
                json_output=json_output,
                markdown_output=markdown_output,
            )
        except OSError:
            sys.stderr.write(_json_text(failure))
        return 2

    try:
        request = ManualPromoEvaluationInput.model_validate(raw_input)
    except ValidationError as exc:
        failure = _validation_failure(exc)
        try:
            _write_outputs(
                failure,
                json_output=json_output,
                markdown_output=markdown_output,
            )
        except OSError:
            sys.stderr.write(_json_text(failure))
        return 2

    try:
        from .engine import evaluate_manual_promotion

        evaluated = evaluate_manual_promotion(
            request,
            catalog_path,
            source_registry_path,
        )
        result = PromotionDecisionBriefV2.model_validate(evaluated)
    except Exception:
        failure = _single_failure(
            "PROVIDER_FAILURE",
            "Evaluation failed closed because local catalog, source-registry, or runtime validation could not complete.",
            field_path="$runtime",
        )
        try:
            _write_outputs(
                failure,
                json_output=json_output,
                markdown_output=markdown_output,
            )
        except OSError:
            sys.stderr.write(_json_text(failure))
        return 2

    try:
        _write_outputs(
            result,
            json_output=json_output,
            markdown_output=markdown_output,
        )
    except OSError:
        failure = _single_failure(
            "PROVIDER_FAILURE",
            "Evaluation completed, but an explicit output path could not be written.",
            field_path="$output",
        )
        sys.stderr.write(_json_text(failure))
        return 2
    return 0


def main(argv: Sequence[str] | None = None) -> None:
    raise SystemExit(run(argv))
