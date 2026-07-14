from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any

from .models import PromotionDecisionBriefV2, RuntimeValidationFailure


def _text(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, datetime):
        return value.isoformat().replace("+00:00", "Z")
    if isinstance(value, Enum):
        return str(value.value)
    return str(value)


def _cell(value: Any) -> str:
    return _text(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def _list(values: list[Any]) -> str:
    return ", ".join(_text(value) for value in values) if values else "none"


def _blocker_table(blockers: list[Any]) -> list[str]:
    rows = [
        "| Reason code | Candidate | Field | Message |",
        "|---|---|---|---|",
    ]
    if not blockers:
        rows.append("| none | — | — | No blockers recorded. |")
        return rows
    for blocker in blockers:
        rows.append(
            "| {code} | {candidate} | {field} | {message} |".format(
                code=_cell(blocker.reason_code),
                candidate=_cell(blocker.candidate_id),
                field=_cell(blocker.field_path),
                message=_cell(blocker.message),
            )
        )
    return rows


def render_decision_brief_markdown(brief: PromotionDecisionBriefV2) -> str:
    """Render a concise, audit-oriented view without changing engine values."""

    lines = [
        "# Promotion Decision Brief",
        "",
        "## Run",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Run ID | {_cell(brief.run.run_id)} |",
        f"| Created | {_cell(brief.run.created_at_utc)} |",
        f"| Timezone | {_cell(brief.run.timezone)} |",
        f"| Jurisdiction | {_cell(brief.run.jurisdiction)} |",
        f"| Adapter | {_cell(brief.run.adapter_id)} v{_cell(brief.run.adapter_version)} |",
        f"| Profile | {_cell(brief.run.profile_id)} ({_cell(brief.run.profile_lifecycle)}) |",
        f"| Overall status | {_cell(brief.run.overall_status)} |",
        "",
        "## Promotion",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Promotion ID | {_cell(brief.promotion.promo_id)} |",
        f"| Sportsbook | {_cell(brief.promotion.sportsbook_id)} ({_cell(brief.promotion.jurisdiction)}) |",
        f"| Boost | {_cell(brief.promotion.boost_type)} at {_cell(brief.promotion.boost_percent)}% |",
        f"| Maximum stake | {_cell(brief.promotion.max_stake)} |",
        f"| Expires | {_cell(brief.promotion.expires_at_utc)} |",
        f"| Verification | {_cell(brief.promotion.verification_status)} |",
        f"| Ambiguities | {_cell(_list(brief.promotion.ambiguities))} |",
        "",
        "## Ranked candidates",
        "",
        "| Rank | Candidate | Market / side | Target price | Boosted decimal | Break-even p | Estimated p | EV/unit | Expected dollars | State |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]

    if not brief.candidates:
        lines.append("| — | none | — | — | — | — | — | — | — | blocked |")
    else:
        for candidate in brief.candidates:
            market = f"{candidate.market_key} / {candidate.side}"
            if candidate.line is not None:
                market += f" {format(candidate.line, 'f')}"
            lines.append(
                "| {rank} | {candidate_id} | {market} | {target} | {boosted} | {break_even} | {probability} | {ev} | {expected} | {state} |".format(
                    rank=_cell(candidate.rank),
                    candidate_id=_cell(candidate.candidate_id),
                    market=_cell(market),
                    target=_cell(candidate.target_american_odds),
                    boosted=_cell(candidate.boosted_decimal_odds),
                    break_even=_cell(candidate.break_even_probability),
                    probability=_cell(candidate.estimated_probability),
                    ev=_cell(candidate.ev_per_unit),
                    expected=_cell(candidate.expected_dollars),
                    state=_cell(candidate.state),
                )
            )

    lines.extend(["", "## Candidate audits"])
    if not brief.candidates:
        lines.extend(["", "No candidate audit was produced."])
    for candidate in brief.candidates:
        audit = candidate.consensus_audit
        identity = candidate.market_identity
        source_probabilities = [
            f"{row.sportsbook_id}/{row.pricing_origin_id}: {_text(row.fair_probability)}"
            for row in audit.source_level_probabilities
        ]
        excluded = [
            f"{row.source_id} ({_list(row.reason_codes)}: {row.message})"
            for row in audit.excluded_sources
        ]
        candidate_blockers = [
            f"{row.reason_code}: {row.message}" for row in candidate.blockers
        ]
        lines.extend(
            [
                "",
                f"### {_cell(candidate.candidate_id)}",
                "",
                f"- Identity: event `{_cell(candidate.event_id)}`, participant `{_cell(candidate.participant_id)}`, raw market `{_cell(identity.raw_market_label)}`, raw selection `{_cell(identity.raw_selection_label)}`.",
                f"- Settlement: period `{_cell(identity.period)}`; overtime/extra innings `{_cell(identity.overtime_or_extra_innings_treatment)}`; push `{_cell(identity.push_behavior)}`; participation `{_cell(identity.participation_rule)}`; void `{_cell(identity.void_rule)}`; stat counting `{_cell(identity.stat_counting_rule)}`; settlement `{_cell(identity.settlement_rule)}`.",
                f"- Pricing audit: target `{_cell(audit.target_sportsbook_id)}` excluded `{_cell(audit.target_excluded)}`; raw sources `{audit.raw_source_count}`; usable books `{audit.usable_book_count}`; resolved origins `{audit.pricing_origin_group_count}`; method `{_cell(audit.aggregation_method_version)}`.",
                f"- Source-level probabilities: {_cell(_list(source_probabilities))}.",
                f"- Comparison timing: oldest age `{_cell(audit.oldest_comparison_age_seconds)}` seconds; collection skew `{_cell(audit.collection_skew_seconds)}` seconds; dispersion `{_cell(audit.dispersion_percentage_points)}` percentage points.",
                f"- Excluded sources: {_cell(_list(excluded))}.",
                f"- Freshness/refresh: post-change synchronized `{_cell(candidate.monitoring_metadata.post_material_change_synchronized)}`; next refresh `{_cell(candidate.monitoring_metadata.next_refresh_at)}`; reason `{_cell(candidate.monitoring_metadata.next_refresh_reason)}`.",
                f"- Reason codes: {_cell(_list(candidate.reason_codes))}.",
                f"- Blockers: {_cell(_list(candidate_blockers))}.",
                f"- Invalidation conditions: {_cell(_list(candidate.invalidation_conditions))}.",
                f"- Source references: {_cell(_list(candidate.source_refs))}.",
            ]
        )

    lines.extend(
        [
            "",
            "## Freshness",
            "",
            f"- Maximum target-quote age observed: `{_cell(brief.freshness.target_quote_max_age_seconds)}` seconds.",
            f"- Oldest material-input age observed: `{_cell(brief.freshness.oldest_material_input_age_seconds)}` seconds.",
            f"- Stale inputs: {_cell(_list(brief.freshness.stale_inputs))}.",
            "",
            "## Run blockers",
            "",
            *_blocker_table(brief.blockers),
            "",
            "## QA and changes",
            "",
            f"- QA: `{_cell(brief.qa.result)}`; issues: {_cell(_list(brief.qa.issues))}.",
            f"- Prior run: `{_cell(brief.change_summary.prior_run_id)}`; material change: `{_cell(brief.change_summary.material_change)}`; changes: {_cell(_list(brief.change_summary.changes))}.",
            "",
            "## Human decision boundary",
            "",
            brief.human_boundary,
            "",
        ]
    )
    return "\n".join(lines)


def render_validation_failure_markdown(failure: RuntimeValidationFailure) -> str:
    lines = [
        "# Manual Promotion Evaluation Error",
        "",
        "The request failed closed before a recommendation-grade evaluation could run.",
        "",
        "## Blockers",
        "",
        *_blocker_table(failure.blockers),
        "",
        "## Human decision boundary",
        "",
        failure.human_boundary,
        "",
    ]
    return "\n".join(lines)


def render_markdown(
    result: PromotionDecisionBriefV2 | RuntimeValidationFailure,
) -> str:
    if isinstance(result, PromotionDecisionBriefV2):
        return render_decision_brief_markdown(result)
    return render_validation_failure_markdown(result)
