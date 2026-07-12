# Advantage Play Intern - Sport Adapter Registry

**Document status:** Active catalog and adapter-selection policy  
**Default timezone:** `America/Chicago`

## 1. Purpose

This directory stores durable, sport-specific research capabilities. A sport adapter defines the exact market profiles the project understands, the facts those profiles consume, when those facts expire, and how missing or changed facts affect candidate state.

A sport adapter is not an odds-provider adapter:

- A **sport adapter** defines market meaning, settlement identity, signal consumers, refresh rules, state gates, model boundaries, and validation scenarios for a sport and market family.
- A **provider adapter** retrieves a vendor's payload and translates vendor fields into canonical objects. Provider exposure does not activate a sport profile or prove recommendation-grade coverage.

Keep provider-specific endpoints, credentials, payload parsing, retry logic, and vendor field mappings outside this registry when executable provider modules are introduced. Sport adapters may name approved source classes and record provider-validation evidence, but must remain provider-agnostic at their core.

## 2. Authority and delegation

Apply these documents together, in this order:

1. `PROJECT_CONTEXT.md` owns product architecture, canonical objects, deterministic formulas, and the broad roadmap.
2. `PROMO_ANALYSIS_PLAYBOOK.md` owns promotion intake, analysis, QA, reason codes, and the decision-brief contract.
3. `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md` owns global signal tiers, consensus and freshness gates, candidate-state rules, and active-scope boundaries.
4. This catalog owns the adapter lifecycle vocabulary and adapter-selection rules.
5. The selected sport adapter owns only that sport's exact market identity, sport-specific signals, sources, cadence, material changes, profile-level gates, and fixtures.

A sport adapter may narrow a global rule for its market, but it may not weaken or contradict a global eligibility, consensus, freshness, provenance, human-approval, or access-control rule. When documents or observed provider behavior conflict, fail closed, identify the conflict, and update the affected documentation and implementation together.

The established `mlb.player_hits` registry remains authoritative in Section 6 of `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md`. It is cataloged here by reference rather than copied, so it cannot drift into two competing registries.

The standalone league contracts are authoritative at `SPORT_ADAPTERS/WNBA.md`, `SPORT_ADAPTERS/NBA.md`, and `SPORT_ADAPTERS/NFL.md`. NBA and NFL are registered specification-only adapters: every profile in those two documents remains `disabled_provider_validation`, so their detailed contracts and credential-free fixtures do not authorize polling or candidate generation.

## 3. Lifecycle vocabulary

Lifecycle status is assigned per market profile, not merely per document.

| Status | Meaning | Permitted behavior |
|---|---|---|
| `active` | Stable, approved profile whose required evidence and validation gates are defined | On-demand candidate generation and deterministic ranking within the documented scope |
| `pilot_enabled` | Experimental, human-supervised profile approved to gather provider-validation evidence on demand; cross-timing source certification may still be incomplete and must be named | Local decision briefs only; every individual run must independently satisfy current target, comparison, identity, freshness, and context gates using verified evidence, and must fail closed on every unproven assumption |
| `disabled_provider_validation` | Profile is specified but exact coverage, identity, settlement, freshness, push handling, or source-independence evidence is incomplete | Documentation and recorded fixture work only; no recommendation-grade candidate generation |
| `disabled_model_only` | Profile or signal family requires a named, licensed, calibrated model that is not enabled | Design and backtest planning only; no routine collection, scoring, narration, or probability use |
| `retired` | Profile is deliberately withdrawn or superseded | Historical audit/reference only; never selected for a new run |

This vocabulary is closed for the current documentation pilot. Do not use an ambiguous status such as `enabled`, `future`, or `disabled` without one of the values above. Record the concrete blocker separately from lifecycle status.

## 4. Adapter catalog

Adapter identity and profile lifecycle are separate records. Adapter versions describe a document contract; lifecycle applies to each exact market profile.

### 4.1 Adapter records

| adapter_id | version | contract_version | sport / league | authoritative location | run mode | probability method |
|---|---|---|---|---|---|---|
| `mlb.player_hits_v0_1` | `0.1.0` | `adapter_contract_v1` | Baseball / MLB | `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md`, Section 6 | on-demand local brief | de-vigged exact-market consensus |
| `wnba.pregame_full_game_v0_1` | `0.2.0` | `adapter_contract_v1` | Basketball / WNBA | `SPORT_ADAPTERS/WNBA.md` | on-demand local brief | de-vigged exact-market consensus for pilot-enabled profiles |
| `nba.pregame_full_game_v0_1` | `0.1.0` | `adapter_contract_v1` | Basketball / NBA | `SPORT_ADAPTERS/NBA.md` | specification only while profiles are disabled | de-vigged exact-market consensus after separate activation |
| `nfl.pregame_full_game_v0_1` | `0.1.0` | `adapter_contract_v1` | Football / NFL | `SPORT_ADAPTERS/NFL.md` | specification only while profiles are disabled | de-vigged exact-market consensus after separate activation |

### 4.2 Profile records

| profile_id | adapter_id | lifecycle | exact current boundary | activation blocker |
|---|---|---|---|---|
| `mlb.player_hits` | `mlb.player_hits_v0_1` | `active` | Pregame player hits only | none within documented stable scope |
| `wnba.full_game.moneyline` | `wnba.pregame_full_game_v0_1` | `pilot_enabled` | Pregame, full-game market with exact overtime/settlement match | stable activation still requires cross-timing provider evidence |
| `wnba.full_game.spread` | `wnba.pregame_full_game_v0_1` | `pilot_enabled` | Pregame, full-game, reciprocal half-point line only | push-aware lines disabled; stable activation still requires cross-timing provider evidence |
| `wnba.full_game.total` | `wnba.pregame_full_game_v0_1` | `pilot_enabled` | Pregame, full-game, half-point line only | push-aware lines disabled; stable activation still requires cross-timing provider evidence |
| `wnba.player.points` | `wnba.pregame_full_game_v0_1` | `disabled_provider_validation` | Exact full-game half-point over/under | exact two-sided same-threshold coverage not validated across required timing conditions |
| `wnba.player.rebounds` | `wnba.pregame_full_game_v0_1` | `disabled_provider_validation` | Exact full-game half-point over/under | exact two-sided same-threshold coverage not validated across required timing conditions |
| `wnba.player.assists` | `wnba.pregame_full_game_v0_1` | `disabled_provider_validation` | Exact full-game half-point over/under | exact two-sided same-threshold coverage not validated across required timing conditions |
| `wnba.player.made_threes` | `wnba.pregame_full_game_v0_1` | `disabled_provider_validation` | Exact full-game half-point over/under | exact two-sided same-threshold coverage not validated across required timing conditions |
| `nba.full_game.moneyline` | `nba.pregame_full_game_v0_1` | `disabled_provider_validation` | Pregame, full-game two-way moneyline with exact overtime/settlement match | real promotion evidence, exact source validation, and separate activation approval remain absent |
| `nba.full_game.spread` | `nba.pregame_full_game_v0_1` | `disabled_provider_validation` | Pregame, full-game principal reciprocal half-point line only | principal-line identity, exact two-sided source coverage, and separate activation approval remain unvalidated |
| `nba.full_game.total` | `nba.pregame_full_game_v0_1` | `disabled_provider_validation` | Pregame, full-game principal half-point total only | principal-line identity, exact two-sided source coverage, and separate activation approval remain unvalidated |
| `nba.player.points` | `nba.pregame_full_game_v0_1` | `disabled_provider_validation` | Exact non-push full-game over/under, including conditionally equivalent milestone shapes | exact participation/void/stat-counting/settlement equivalence, source coverage, and separate activation approval remain unvalidated |
| `nfl.full_game.moneyline` | `nfl.pregame_full_game_v0_1` | `disabled_provider_validation` | Pregame, full-game two-way moneyline only when tie and push are proven impossible | tie treatment, exact source coverage, and separate activation approval remain unvalidated |
| `nfl.full_game.spread` | `nfl.pregame_full_game_v0_1` | `disabled_provider_validation` | Pregame, full-game principal reciprocal half-point line only | principal-line identity, exact two-sided source coverage, and separate activation approval remain unvalidated |
| `nfl.full_game.total` | `nfl.pregame_full_game_v0_1` | `disabled_provider_validation` | Pregame, full-game principal half-point total only | principal-line identity, exact two-sided source coverage, and separate activation approval remain unvalidated |

The catalog therefore contains exactly four adapter records and fifteen profile records: one `active`, three `pilot_enabled`, and eleven `disabled_provider_validation`.

If a profile is absent from this catalog, treat it as `disabled_provider_validation`. Provider availability alone does not grant activation.

NBA rebounds, assists, and made-threes profiles are absent and unavailable. NFL player-prop profiles, including passing- and rushing-yard props, are unregistered and unavailable. Do not recreate underscore-style NBA placeholders or infer any missing profile from provider exposure.

Soccer and World Cup concepts in `PROJECT_CONTEXT.md` are roadmap hypotheses only. They are not adapter or profile records and cannot be selected for a run. Their eventual discovery and design must begin as a separate phase using `ADAPTER_TEMPLATE.md`.

## 5. Structural conformance contract

`ADAPTER_TEMPLATE.md` is the structural conformance contract for existing and future adapters, version `adapter_contract_v1`. An authoritative adapter may remain embedded in another governing document, as MLB does, but it must still expose the same normalized information:

1. adapter metadata and profile registry;
2. market identity and settlement contract;
3. probability/comparison policy;
4. source and compliance policy;
5. inherited shared-signal extensions and sport-specific Tier A/B/C signals;
6. materiality and state-resolution rules;
7. event-relative refresh phases;
8. Tier D and Tier X registries;
9. provider-validation evidence requirements;
10. fixtures and acceptance scenarios;
11. on-demand run/decision-brief contract; and
12. change log.

Shared signals remain authoritative only in Section 5 of `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md`. Adapters reference or narrow them through an extension table; they must not create competing definitions for promotion terms, target quotes, comparison quotes, market status, or promotion expiration.

### 5.1 Shared semantic roles

Semantic roles make adapter behavior comparable without renaming or merging sport-specific signals.

| semantic_role | purpose | MLB mapping | WNBA mapping | NBA mapping | NFL mapping |
|---|---|---|---|---|---|
| `event_identity_status` | verify exact event and current game state | `mlb_game_identity`, `mlb_game_status` | `wnba_event_identity_status` | `nba_event_identity_status` | `nfl_event_identity_status` |
| `participant_availability` | verify participant eligibility or availability | `mlb_player_status` | `wnba_target_player_availability` for player profiles; `wnba_team_availability_delta` for team markets | `nba_target_player_status` for player points; `nba_team_availability_delta` for team markets | `nfl_team_availability_delta` |
| `official_release_state` | track the sport's critical official release or confirmation | `mlb_starting_lineup`, `mlb_opposing_starter` | `wnba_injury_submission_state`, `wnba_starting_five_role_event` | `nba_injury_submission_state`, `nba_starting_five_role_event` | `nfl_injury_report_state`, `nfl_starting_quarterback_status`, `nfl_inactive_list_state` |
| `material_context_delta` | invalidate prices after a registered confirmed change | lineup, starter, roof/weather, or allowlisted bullpen signals | availability, roster/transaction, event, or confirmed-role signals | event, injury/availability, roster/transaction, target-player, or confirmed-role signals | event, injury/availability, quarterback, inactive-list, roster/transaction, venue, or operational-weather signals |
| `post_change_price_sync` | require target and comparison quotes newer than the change | shared quote signals after any MLB material change | shared quote signals after any WNBA material change | shared quote signals under `nba_post_change_price_sync_v1` | shared quote signals under `nfl_post_change_price_sync_v1` |
| `consensus_valuation` | derive and audit fair probability | shared `comparison_quotes_same_line` under MLB configuration | shared `comparison_quotes_same_line` under `wnba_market_consensus_mean_v1` | shared `comparison_quotes_same_line` under `nba_market_consensus_mean_v1` | shared `comparison_quotes_same_line` under `nfl_market_consensus_mean_v1` |

NFL candidates also retain adapter-local `season_phase`, `tie_possible`, and `tie_treatment` audit fields. These narrow the NFL identity contract without changing `promotion_decision_brief_v2` or any global schema.

### 5.2 Standard refresh phases

Every adapter uses these phase IDs while retaining sport-specific times, sources, and gates:

| phase_id | shared meaning |
|---|---|
| `intake` | capture promotion, eligible slate, initial identity/context, target, and comparisons |
| `distant_pregame` | refresh the slate and registered facts while the event is not yet near start |
| `official_release_window` | monitor the sport's lineup, pitcher, injury-report, roster, or other critical release window |
| `material_change` | invalidate affected prices and obtain a synchronized post-change batch |
| `shortlist_check` | refresh shortlisted candidates near event start |
| `final_sync` | perform the final synchronized eligibility, state, target, comparison, and QA check before human review |

## 6. Adapter selection rules

For every promotion-analysis request:

1. Parse the sportsbook, jurisdiction, sport, league, eligible market, event window, period, overtime treatment, boost structure, odds restrictions, stake cap, expiry, and void/push rules.
2. Preserve the sportsbook's raw market label and map it to a canonical profile only through an explicit equivalence rule.
3. Select exactly one adapter profile whose event, participant, period, line, side, overtime, settlement, and push behavior all match.
4. Continue to candidate generation only when that profile is `active` or `pilot_enabled` and all global gates pass.
5. Return `BLOCKED` for an unresolved mapping or a `disabled_provider_validation` / `disabled_model_only` profile. Return `INELIGIBLE` when the promotion terms clearly exclude it.
6. Record the selected adapter ID and version in the decision brief and local evidence snapshot.

Do not silently fall back to a nearby market. A full-game total is not a team total, a regulation-only market is not an overtime-included market, and a one-sided ladder is not a complete two-way market.

## 7. Activation and change control

A profile may advance to `pilot_enabled` only after the selected adapter contains:

- exact raw and canonical market identities;
- promotion and settlement eligibility inputs;
- the full ten-field contract for every enabled Tier A, B, and C signal;
- recommendation-grade source hierarchy and source-permission review;
- freshness, collection-skew, and material-change rules;
- candidate-state effects and explicit Tier D/Tier X boundaries;
- defined missing, stale, conflicting, suspended, and material-change scenarios with exact expected outcomes;
- a verified screenshot/manual or otherwise permitted evidence path capable of satisfying every gate within an individual run;
- deterministic calculation and report expectations;
- every unfinished cross-timing or automated-source validation item named as a blocker to stable activation; and
- explicit activation approval reflected consistently in this catalog, the sport adapter, the monitoring playbook, `AGENTS.md`, and `README.md`.

`pilot_enabled` does not certify an automated source or waive provider validation. A pilot candidate can become `ACTIONABLE FOR REVIEW` only when that specific run independently obtains a current exact target quote, two fresh complete independent non-target comparison markets, and all other required evidence.

A profile may advance from `pilot_enabled` to `active` only after all pilot requirements remain satisfied; credential-free fixtures have been recorded; and target-quote/comparison-source validation has passed across every timing condition required by the adapter, with recorded evidence, stable identity and timestamp behavior, resolved pricing-origin independence, and approved source use.

Status must not be relaxed merely to produce a recommendation. A provider regression, source-terms problem, unresolved pricing-origin relationship, or failed validation may immediately force `WATCH`/`BLOCKED` in a run and should trigger a documented lifecycle review.

## 8. Cross-project boundary

These adapters produce local research metadata and decision briefs only. They do not place or confirm wagers.

`market_identity.ap_frankenstein_compatibility` is descriptive metadata with one of:

- `direct`
- `equivalent_but_not_supported`
- `unsupported`

It does not authorize AP Frankenstein access. This project must not edit AP Frankenstein, call it, write its spreadsheets, create a bridge contract, or assume a candidate became a wager. After a user manually places a wager, AP Frankenstein remains the separate downstream owner of its existing receipt, spreadsheet, settlement, and tracking workflow.

## 9. Adding another adapter

Copy `ADAPTER_TEMPLATE.md`, retain `adapter_contract_v1`, give every profile a lifecycle state, and add both the adapter record and its profile records to this catalog. Keep the adapter narrow: activate one exact market family only after its own evidence passes. A soccer or future basketball adapter must not inherit WNBA or MLB materiality assumptions merely because the fields look similar.
