# AP Slave — Durable Project Handoff

**Document status:** Subordinate, non-authoritative decision memory
**Authority:** Current instructions and governing documents verified against live Git, source, and tests override this handoff.
**Current posture:** Record Git state, validation results, phase progress, blockers, and next actions in `CURRENT_STATUS.md`, not here.

## Purpose

This file preserves stable cross-session decisions for multi-phase work. It does not replace or restate the authoritative root [PROJECT_CONTEXT.md](../../PROJECT_CONTEXT.md), and it never authorizes a source call, provider integration, profile activation, deployment, sportsbook action, or AP Frankenstein interaction.

Before using this handoff, verify it against the live repository and apply the authority order in [AGENTS.md](../../AGENTS.md). Canonical adapter/profile truth remains in [SPORT_ADAPTERS/catalog.yaml](../../SPORT_ADAPTERS/catalog.yaml), source policy remains in [SPORT_ADAPTERS/source_registry.yaml](../../SPORT_ADAPTERS/source_registry.yaml), and formulas, reason codes, freshness rules, and adapter behavior remain in their governing documents.

## Durable product boundary

- Advantage Play Intern is a local, human-supervised promotion-research system. The strongest result is a candidate for human review; the user alone decides whether to place a wager and performs every sportsbook action.
- Tested deterministic code owns recommendation-grade odds conversion, boost math, de-vigging, probability aggregation, EV, expected dollars, freshness, normalization, and ranking. The LLM may parse, map, summarize, and explain, but must not invent numerical inputs or replace deterministic calculation.
- Lifecycle expresses policy permission only. `contract_status`, `implementation_status`, and `source_readiness` remain independent canonical dimensions; provider exposure, contract scenarios, executable fixtures, or evidence manifests do not activate a profile.
- Disabled and catalog-absent profiles fail closed. An absent profile is unregistered, has no lifecycle, and cannot be inferred from a sportsbook or provider listing.
- The repository has no approved provider integration, paid API, sportsbook retrieval or automation, scheduler, polling, alerts, statistical model, live-market workflow, bet tracking, closing-line capture, or settlement runtime.
- AP Frankenstein remains a separate downstream system after a user manually places a wager. This project must not call it, edit it, write its spreadsheets, create a bridge, or infer that a reviewed candidate became a wager.

## Reliability-initiative baseline

At the verified initiative baseline, Git HEAD `a1ec284` on 2026-07-14 local time, the canonical catalog contains five adapters and twenty-one registered profiles. Four profiles have the credential-free manual-input runtime:

- `mlb.player_hits`;
- `wnba.full_game.moneyline`;
- `wnba.full_game.spread`;
- `wnba.full_game.total`.

NBA, NFL, Golf, disabled WNBA player profiles, and every unregistered profile remain unavailable for recommendation-grade valuation. The canonical catalog owns the exact lifecycle distribution and must be rechecked rather than copied from this handoff when making a run or change.

## Approved reliability initiative

The approved six-phase initiative hardens the existing four-profile manual calculator without expanding sport, provider, lifecycle, or integration scope:

1. Establish durable project handoffs and a verified baseline.
2. Make runtime catalog and source-registry loading strict and fail closed on malformed canonical contracts.
3. Harden manual-input trust boundaries, including stake, identity, origin, evidence, timestamp, and uniqueness validation.
4. Complete deterministic WNBA spread and total fixture/golden coverage and apply documentation-only MLB/WNBA patch versions where required.
5. Strengthen evidence-template and catalog-presentation validation without authorizing raw evidence, providers, or live access.
6. Synchronize governance language and perform the final offline release audit.

Each phase is dependency-gated. Preserve `manual_promo_evaluation_v1`, `adapter_contract_v1`, `promotion_decision_brief_v2`, existing formulas, reason codes, lifecycle values, freshness limits, human control, and the AP Frankenstein boundary unless a separately approved migration explicitly changes them.

## Change-control decisions

- Use credential-free fixtures, local evidence manifests, and offline checks by default. Raw screenshots, account data, credentials, private paths, raw sportsbook payloads, and generated decision briefs remain local and ignored.
- Workers may own disjoint implementation areas, but the coordinator owns shared-file integration, handoff synthesis, validation, commits, pushes, and release gates.
- Stop on authority conflict, unexpected worktree change, lifecycle/readiness drift, source-permission conflict, failed regression, or Git divergence. Current evidence overrides stale handoff prose.
- Update this file only when a durable product, architecture, contract, boundary, or strategy decision changes. Put verified operational progress and release evidence in `CURRENT_STATUS.md`.
