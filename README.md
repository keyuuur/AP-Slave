# Advantage Play Intern - Context Pack

**Version:** 0.1  
**Prepared:** 2026-07-10  
**Default timezone:** America/Chicago

## Purpose and current checkout

This repository specifies a local, human-supervised sports-market research system. The intended product collects exact evidence, applies deterministic pricing rules, and prepares an auditable decision brief for human review without placing a wager.

> **Current-checkout status:** This repository is a specification and documentation pack only. It contains no executable retrieval, calculation, ranking, scheduling, alerting, tracking, settlement, or provider-adapter runtime and records no provider certification. Current work is limited to human-supervised documentation, credential-free fixtures, and safe evidence manifests using explicitly supplied and verified information.

The governing idea is:

> The AI is an attention and research intern, not an oracle and not an autonomous bettor.

## Files and authority

- **`AGENTS.md`** - concise read-first, safety, authority, readiness, and working instructions.
- **`PROJECT_CONTEXT.md`** - current product specification, canonical objects, deterministic formulas, and broad acceptance requirements.
- **`ROADMAP.md`** - non-authoritative future possibilities and sequencing; it does not authorize implementation.
- **`PROMO_ANALYSIS_PLAYBOOK.md`** - promotion intake, analysis workflow, QA, reason codes, and `promotion_decision_brief_v2`.
- **`PROMO_PLACEMENT_MONITORING_PLAYBOOK.md`** - authoritative global lifecycle-enabled behavior, valuation, consensus, freshness, material-change, candidate-state, and anti-noise policy. Section 6 remains the MLB player-hits authority.
- **`SPORT_ADAPTERS/catalog.yaml`** - canonical `adapter_catalog_v1` adapter, profile, lifecycle, implementation-status, and source-readiness records.
- **`SPORT_ADAPTERS/source_registry.yaml`** - canonical `source_registry_v1` source roles, access permissions, coverage posture, pricing-origin groups, season/event policies, and review triggers.
- **`SPORT_ADAPTERS/README.md`** - human-readable catalog presentation, lifecycle vocabulary, authority boundaries, and adapter-selection rules.
- **`SPORT_ADAPTERS/ADAPTER_TEMPLATE.md`** - structural conformance contract `adapter_contract_v1`.
- **`SPORT_ADAPTERS/WNBA.md`**, **`SPORT_ADAPTERS/NBA.md`**, **`SPORT_ADAPTERS/NFL.md`**, and **`SPORT_ADAPTERS/GOLF.md`** - selected-sport market identity, settlement, signals, source application, cadence, gates, and fixtures.
- **`evidence/templates/`** - credential-free manifest templates. Raw screenshots, account/personal data, credentials, raw sportsbook payloads, private paths, and generated decision briefs stay local and ignored.

For any promotion review, apply the analysis playbook, monitoring playbook, canonical catalog, source registry, and selected sport authority together. Never run the reusable analysis prompt alone. An adapter may narrow global rules but cannot replace the governing formulas, report contracts, freshness/consensus gates, human-control boundary, or AP Frankenstein separation.

## Catalog and readiness

The canonical catalog owns the registered adapter/profile records and derived lifecycle distribution; `SPORT_ADAPTERS/README.md` presents them for humans. Numeric totals are not maintained independently here.

Lifecycle is policy permission, not proof of implementation or source certification. Implementation status and source readiness are separate canonical fields. `active` or `pilot_enabled` therefore does not mean this checkout has an executable runtime or a certified sportsbook, provider, market, pricing origin, or automated source.

- **MLB:** `mlb.player_hits` is the stable policy-active pregame profile. Its authority remains Section 6 of the monitoring playbook.
- **WNBA:** pregame full-game moneyline, reciprocal half-point spread, and half-point total have policy status `pilot_enabled` for supervised on-demand review only when every per-run evidence gate passes. Player points, rebounds, assists, and made threes remain disabled.
- **NBA:** registered full-game moneyline, half-point spread, half-point total, and non-push player points remain disabled. Rebounds, assists, made threes, and other absent props are unregistered.
- **NFL:** registered full-game moneyline, half-point spread, and half-point total remain disabled. Player props and other absent markets are unregistered.
- **Golf:** six Missouri individual-stroke-play profiles are registered but disabled. A FanDuel or DraftKings listing discovers only a possible event; it does not prove adapter support, competition identity, settlement, source permission, comparison coverage, or provider certification.
- **Other sports and markets:** Soccer, World Cup, NCAAF, NHL, and every catalog-absent profile are unregistered and unavailable. An absent profile has no lifecycle record and must fail closed.

Credential-free fixtures and source manifests document expected behavior only. They cannot activate a profile, certify a source, authorize polling, or permit candidate generation.

## Current analytical contract

The documents specify the following behavior for a future deterministic implementation or a separately performed human-supervised review:

1. Capture the exact promotion, sportsbook, Missouri jurisdiction where applicable, event, participant, market, side, line, period, settlement, expiry, and void/push terms.
2. Require a current exact target quote and complete exact-market outcome sets from at least two non-target comparison books assigned to two resolved independent pricing-origin groups.
3. Exclude the target sportsbook, preserve raw labels, and de-vig each usable comparison source separately under the governing method.
4. Use only registered sport context to validate identity and freshness. A material fact newer than prices invalidates the batch and requires synchronized prices; it never creates a narrative probability adjustment.
5. Keep missing, stale, suspended, conflicting, unreadable, or unverified evidence explicit and fail closed under the governing candidate states and reason codes.
6. Use deterministic tested code for recommendation-grade odds, boost, no-vig, EV, expected-dollar, freshness, aggregation, and ranking calculations once such code is separately implemented.
7. Present research for human review. The user alone decides whether to place a wager.

No repository-contained runtime currently performs those steps. `promotion_decision_brief_v2`, adapter/profile/version metadata, raw/canonical identity, source-origin audit, settlement metadata, and next-refresh metadata remain specification contracts rather than persisted-schema or runtime claims.

## Sources and evidence

`SPORT_ADAPTERS/source_registry.yaml` and the selected adapter control source use. Provider marketing, a visible field, or one successful capture never proves exact book, jurisdiction, market, settlement, timing, or future coverage.

- Prefer official league/team/organizer and government sources for event facts, then licensed/documented providers, sportsbook-originated evidence, approved specialist sources, and verified screenshots or structured manual entry.
- Preserve source identity, exact jurisdiction, capture time in UTC, provider time/object ID when available, event/market identity, source permission, pricing-origin group, and a safe snapshot hash or manifest reference.
- Never automate authenticated sportsbook pages or bypass authentication, geolocation, age/jurisdiction controls, CAPTCHAs, anti-bot controls, paywalls, rate limits, or source terms.
- Golf requires an event-specific organizer, competition, market, and settlement source pack. FanDuel or DraftKings Missouri availability remains discovery-only.
- Raw/private evidence and generated decision briefs must stay in ignored local paths. Only credential-free manifest/hash metadata belongs in repository evidence templates.

## Human and project boundaries

This project never places, submits, confirms, or pretends to place a wager. It does not log in to sportsbooks, handle sportsbook credentials, or automate sportsbook account actions.

After the user manually places a wager, AP Frankenstein remains the separate downstream receipt, spreadsheet, tracking, and settlement owner. This project makes no AP Frankenstein edits, API calls, spreadsheet writes, bridge contract, or assumption that a researched candidate became a wager.

Statistical/manual probability overrides, Tier D feature use, live betting, recurring schedules, background polling, automatic alerts, bet tracking, closing-line capture, and settlement are not current behavior. `ROADMAP.md` may describe future possibilities, but each requires separate approval and synchronized governing changes before implementation.

## Success target

A separately implemented first version should reliably answer:

> Given this exact promotion, sportsbook, eligible slate, current prices, and current game context, which candidates deserve human review right now, why, and what evidence could invalidate the result?

It should be judged by reproducibility, exact market matching, source quality, freshness, fail-closed behavior, deterministic calculation tests, and time saved - not by a short winning streak or confident-sounding pick.
