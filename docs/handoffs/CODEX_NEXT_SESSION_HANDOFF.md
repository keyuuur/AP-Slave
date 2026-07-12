# Codex Next Session Handoff

**Artifact type:** Temporary one-use handoff; do not commit or push  
**Prepared:** 2026-07-12  
**Project:** Advantage Play Intern / AP Slave  
**Project root:** `C:\Users\Keyur\Desktop\Claude Code YEET\Personal Coding Projects\AP Slave`

## Project identity and current anchor

This project is currently a documentation-only context pack for a local, human-supervised promotion-placement research system. It contains no executable adapter framework yet.

The project directory is not an independent Git repository. Git resolves upward to:

- root: `C:/Users/Keyur/Desktop/Claude Code YEET`;
- branch: `main`;
- upstream: `origin/main`;
- remote: `https://github.com/keyuuur/Threats-to-Biodiversity-2026.git`;
- preflight divergence: `0 ahead / 0 behind` at handoff creation.

That parent repository is unrelated to AP Slave and has unrelated dirty/untracked work. Every current AP Slave project document is untracked from the parent repository. Do not stage, commit, or push AP Slave from that parent anchor unless Keyur separately establishes an intentional repository boundary and explicitly requests Git work.

No durable LLM handoff exists in the project root or docs tree. Per the `codex-handoff` contract, none was created.

## Recent changes

The approved documentation-only Sport-Adapter Contract Normalization was implemented:

- `SPORT_ADAPTERS/README.md` now separates two adapter records from eight profile records.
- `SPORT_ADAPTERS/ADAPTER_TEMPLATE.md` is the structural conformance contract `adapter_contract_v1` for existing and future adapters.
- Shared semantic roles and six refresh phase IDs are normalized: `intake`, `distant_pregame`, `official_release_window`, `material_change`, `shortlist_check`, and `final_sync`.
- MLB remains authoritative in Section 6 of `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md`. It now declares adapter `mlb.player_hits_v0_1` version `0.1.0` and exposes normalized metadata, profile, identity/settlement, source, signal, materiality, refresh, evidence, fixture, run-contract, and change-log sections.
- WNBA remains standalone in `SPORT_ADAPTERS/WNBA.md`, now version `0.2.0`. Its profile lifecycle states did not change.
- WNBA duplicate policy signals were normalized to shared-signal extensions. Historical IDs remain only in a migration table:
  - `wnba_promo_settlement_terms` -> shared `promo_terms`;
  - `wnba_consensus_quality` -> shared `comparison_quotes_same_line` plus `wnba_market_consensus_mean_v1`;
  - `wnba_post_news_market_state` -> shared quote/status signals plus `wnba_post_change_price_sync_v1`.
- `PROMO_ANALYSIS_PLAYBOOK.md` now defines additive local output contract `promotion_decision_brief_v2` and sport-neutral adapter/data-quality reason codes.
- `PROJECT_CONTEXT.md`, `README.md`, and `AGENTS.md` now state explicitly that soccer/World Cup is concept-only and non-runnable.

## Current project state

- Registered adapters: exactly two—MLB and WNBA.
- Registered profiles: exactly eight.
- Lifecycle distribution:
  - one `active`: `mlb.player_hits`;
  - three `pilot_enabled`: WNBA pregame full-game moneyline, half-point spread, and half-point total;
  - four `disabled_provider_validation`: WNBA points, rebounds, assists, and made threes.
- NBA profiles remain disabled.
- Soccer and World Cup have no adapter/profile record and must be treated as unavailable until a separate approved design phase.
- Fair probability remains de-vigged, exact same-line market consensus from at least two usable independent non-target pricing origins.
- Target/comparison freshness defaults remain 180/300 seconds.
- Sport context may invalidate prices or change state, but it may not create narrative probability adjustments.
- No statistical model, live betting, background scheduler, automatic alerts, bet placement, settlement workflow, or AP Frankenstein bridge is active.
- AP Frankenstein remains a separate downstream receipt/spreadsheet/settlement system after a user manually places a wager.

## Validation performed

All checks passed before this handoff:

- Markdown table column consistency across the normalized documents.
- Catalog integrity: two adapter records, eight profile records, and only closed lifecycle values.
- Lifecycle counts: one active, three pilot-enabled, four provider-validation-disabled.
- Both adapters declare `adapter_contract_v1` and all six normalized refresh phases.
- Shared signals have one authoritative ten-field definition in Monitoring Playbook Section 5.
- MLB has nine enabled sport-specific ten-field signal rows.
- WNBA has seven sport-specific ten-field signal rows.
- Former WNBA signal IDs appear exactly once each and only in the migration map.
- `promotion_decision_brief_v2` parses as valid JSON and contains adapter, market-identity, consensus-audit, and monitoring blocks.
- Required sport-neutral reason codes are present.
- Regression outcomes remain intact: MLB unconfirmed lineup is `WATCH`; material starter/context changes invalidate prices without direct probability changes; missing consensus cannot produce positive-EV/actionable language; missing WNBA starting five alone does not block valid game lines; WNBA whole-number lines and player props remain blocked; soccer/World Cup remains unregistered.
- Global, MLB, and WNBA target/comparison quote limits remain 180/300 seconds.
- Scope check before this temporary file: only the eight approved project documentation files appeared in scoped Git status.

No tests, deployments, provider calls, Git staging, commits, or pushes were run by the handoff workflow. The completed work itself was documentation-only.

## Decisions and preserved safety gates

- Keep MLB authoritative in Monitoring Playbook Section 6; do not create a duplicate `MLB.md`.
- Keep WNBA game-line pilot behavior and every lifecycle status unchanged.
- Keep WNBA player props disabled even if a provider exposes them.
- Defer World Cup to a separate exact-promotion, exact-market, settlement, source, materiality, and refresh discovery phase.
- Treat `promotion_decision_brief_v2` fields as local output/audit metadata, not a persisted-schema migration.
- Do not certify a provider from exposure or a single successful retrieval.
- Do not weaken same-line consensus, pricing-origin independence, freshness, provenance, jurisdiction, settlement, or human-approval gates.
- Never place, confirm, or automate a wager.
- Never call or write to AP Frankenstein from this project.

## Blockers, risks, assumptions, and unresolved questions

- Git/repository ownership is unresolved: AP Slave is untracked inside an unrelated dirty parent repository. This blocks safe commit/push work.
- No durable LLM handoff exists; this temporary artifact is the only handoff.
- The project has no executable adapter implementation or recorded credential-free provider fixtures.
- WNBA automated target/comparison source certification remains incomplete; player props remain disabled.
- World Cup market scope and promotion terms have not been discovered or designed.
- Any next implementation must be separately scoped and approved; do not infer that documentation normalization authorized code, schemas, automation, or new profiles.

## Recommended next steps

1. Complete the fresh-session read-only bootstrap below.
2. Ask Keyur to choose the next bounded task.
3. If the next task is World Cup planning, begin with exact promotion/market discovery and create a separate plan; do not reuse MLB/WNBA materiality assumptions.
4. If the next task is executable implementation, first establish a safe project repository boundary and then design typed schemas/functions from the normalized contracts without activating disabled profiles.
5. If the next task is provider validation, use recorded evidence and fixtures across the timing conditions specified by the selected adapter; do not treat one live result as certification.

## Important files to read

Read in this order:

1. `AGENTS.md`
2. `PROJECT_CONTEXT.md`
3. `PROMO_ANALYSIS_PLAYBOOK.md`
4. `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md`
5. `SPORT_ADAPTERS/README.md`
6. `SPORT_ADAPTERS/ADAPTER_TEMPLATE.md`
7. `SPORT_ADAPTERS/WNBA.md`
8. `README.md`

## Complete next-instance starter prompt

```text
Resume the Advantage Play Intern / AP Slave project at:
C:\Users\Keyur\Desktop\Claude Code YEET\Personal Coding Projects\AP Slave

FIRST TURN: READ-ONLY CONTEXT BOOTSTRAP ONLY.

1. Confirm the exact project root. Inspect the current Git root, branch, upstream, remote, worktree status, and ahead/behind state. Be alert that AP Slave was an untracked subdirectory inside the unrelated parent repository C:\Users\Keyur\Desktop\Claude Code YEET, whose origin was Threats-to-Biodiversity-2026. Stop on any changed or unclear anchor.
2. Read this temporary handoff completely:
C:\Users\Keyur\Desktop\Claude Code YEET\Personal Coding Projects\AP Slave\docs\handoffs\CODEX_NEXT_SESSION_HANDOFF.md
3. No durable LLM handoff existed when this artifact was created. Recheck for one, excluding CODEX_NEXT_SESSION_HANDOFF.md; if none exists, do not create one during the bootstrap.
4. Read the applicable AGENTS.md first, then PROJECT_CONTEXT.md, PROMO_ANALYSIS_PLAYBOOK.md, PROMO_PLACEMENT_MONITORING_PLAYBOOK.md, SPORT_ADAPTERS/README.md, SPORT_ADAPTERS/ADAPTER_TEMPLATE.md, SPORT_ADAPTERS/WNBA.md, and README.md. Inspect enough current content to verify the handoff's claims rather than trusting the summary alone.
5. Verify the normalized adapter state: two adapter records, eight profile records, MLB authority remaining in Monitoring Playbook Section 6, WNBA version 0.2.0, adapter_contract_v1, promotion_decision_brief_v2, unchanged lifecycle/freshness gates, and soccer/World Cup remaining unregistered.
6. Make no edits, file writes, staging, commits, pushes, branch changes, deployments, tests with external side effects, provider calls, sportsbook access, AP Frankenstein calls, or other mutations during the first turn.
7. Return a concise bootstrap summary covering the current project state, authority structure, adapter architecture, active/pilot/disabled boundaries, validation posture, Git risk, uncertainties, and likely next steps.
8. Ask Keyur for the next scoped task. Stop on any failed gate, documentation conflict, unexpected durable handoff, or unclear project/Git anchor.
```
