# NFL Boost-Analysis Sport Adapter

<!-- adapter-section: 1 adapter_metadata -->
## 1. Adapter metadata

**Adapter ID:** `nfl.pregame_full_game_v0_1`

**Version:** `0.1.1`

**Structural contract:** `adapter_contract_v1`

**Document status:** Active pre-activation documentation policy

**Sport:** American football

**League:** NFL

**Lifecycle:** All registered profiles are `disabled_provider_validation`

**Last reviewed:** 2026-07-13

**Default timezone:** `America/Chicago`

**Run mode:** On-demand local decision brief after a separately approved lifecycle change

**Fair-probability method:** De-vigged, exact-market consensus from independent non-target pricing origins

```yaml
adapter:
  adapter_id: nfl.pregame_full_game_v0_1
  version: 0.1.1
  contract_version: adapter_contract_v1
  document_status: active pre-activation documentation policy
  sport: American football
  league: NFL
  default_timezone: America/Chicago
  last_reviewed: 2026-07-13
  review_owner: Advantage Play Intern
  run_mode: on_demand_local_brief_after_separate_activation
  probability_method: de_vigged_same_line_market_consensus
  autonomous_wagering: false
  ap_frankenstein_integration: false
```

This adapter specifies a credential-free, pre-activation contract for supervised NFL promotion research. Promotion value is expected to create most of any future opportunity. NFL context may verify identity and eligibility, invalidate an older price batch, or block a scenario; it never creates an ad hoc probability adjustment and this adapter does not predict NFL outcomes.

This adapter must be applied with `PROJECT_CONTEXT.md`, `PROMO_ANALYSIS_PLAYBOOK.md`, `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md`, and `SPORT_ADAPTERS/README.md`. It does not authorize provider calls, sportsbook access, candidate generation, recurring monitoring, alerts, scheduling, code, or AP Frankenstein integration. Every registered profile remains blocked until provider evidence, source permission, deterministic validation, and separate activation approval exist.

---

<!-- adapter-section: 2 profile_registry -->
## 2. Profile registry

| profile_id | lifecycle | participant | period | allowed line shape | overtime/tie treatment | probability method | activation blocker |
|---|---|---|---|---|---|---|---|
| `nfl.full_game.moneyline` | `disabled_provider_validation` | team | full game | binary two-team moneyline only when both tie and push are proven impossible | overtime included; `season_phase`, `tie_possible=false`, `tie_treatment`, and settlement must match every source | `nfl_market_consensus_mean_v1` after activation | exact no-tie settlement, target coverage, two independent comparison origins, cross-timing freshness, and separate approval are unproven |
| `nfl.full_game.spread` | `disabled_provider_validation` | team | full game | principal reciprocal half-point spread only | overtime treatment and settlement must exactly match; push impossible | `nfl_market_consensus_mean_v1` after activation | principal-line identity, target coverage, two independent comparison origins, cross-timing freshness, and separate approval are unproven |
| `nfl.full_game.total` | `disabled_provider_validation` | event | full game | principal half-point over/under only | overtime treatment and settlement must exactly match; push impossible | `nfl_market_consensus_mean_v1` after activation | principal-line identity, target coverage, two independent comparison origins, cross-timing freshness, and separate approval are unproven |

No NFL player-prop profile is registered. Passing yards, rushing yards, receiving yards, touchdowns, player milestones, team totals, alternate lines, first-half or quarter markets, regulation-only markets, three-way markets, tie options, futures, parlays, same-game parlays, and all live markets are unavailable by catalog absence. A provider exposing one of these markets does not activate it or make it equivalent to a registered profile.

---

<!-- adapter-section: 3 market_identity_settlement -->
## 3. Market identity and settlement contract

Every target and comparison quote must retain the complete identity below. The NFL-local `season_phase`, `tie_possible`, and `tie_treatment` fields are additive local audit annotations in `promotion_decision_brief_v2`; they do not change a global schema or formula.

```yaml
market_identity:
  sportsbook_id: string
  jurisdiction: string
  league: NFL
  event_id: string
  provider_event_id: string
  home_team_id: string
  away_team_id: string
  participant_id: string | null
  provider_participant_id: string | null
  raw_market_label: string
  raw_selection_label: string
  canonical_market_key: string
  outcome_set_id: string | null
  outcome_set_type: binary_pair | mutually_exclusive_exhaustive_multiway | other
  outcome_set_completeness: complete | incomplete | unknown
  participant_set_version: string | null
  market_wrapper: standard | other | null
  side: home | away | over | under
  line: number | null
  period: full_game
  overtime_treatment: included | excluded | unknown
  season_phase: preseason | regular_season | postseason | unknown
  tie_possible: true | false | unknown
  tie_treatment: impossible_by_competition_rule | push | separate_outcome | loss | void | unknown
  push_behavior: impossible | push | unknown
  tie_or_dead_heat_treatment: not_applicable | refund | dead_heat | full_pay | unknown
  void_and_participation_rule: string | unknown
  american_odds: integer
  decimal_odds: number
  market_status: open | suspended | closed | unknown
  retrieved_at_utc: datetime
  provider_last_update_utc: datetime | null
  source_id: string
  raw_snapshot_id: string
  ap_frankenstein_compatibility: unsupported

binary_outcome_set_audit:
  applies: true
  source_sportsbook_id: string
  source_pricing_origin_id: string
  candidate_outcome_id: string
  opposing_outcome_id: string
  candidate_retrieved_at_utc: datetime
  opposing_retrieved_at_utc: datetime
  same_book: boolean
  same_market_identity: boolean
  same_line: boolean
  same_settlement_contract: boolean
  complete: boolean
  exclusion_reason_codes: list[string]
```

`ap_frankenstein_compatibility` defaults to `unsupported` for every NFL shape. The field is descriptive only and creates no API, spreadsheet, receipt, settlement, or handoff integration.

### 3.1 Raw-to-canonical equivalence

| raw market shape | canonical profile | equivalence conditions | settlement conditions | AP compatibility | status |
|---|---|---|---|---|---|
| postseason `Moneyline`, `Game Moneyline`, or `To Win` | `nfl.full_game.moneyline` | exactly two named teams in one event; pregame full game; raw labels retained; official competition rules and book rules prove no tie outcome | overtime included; `season_phase=postseason`; `tie_possible=false`; `tie_treatment=impossible_by_competition_rule`; `push_behavior=impossible`; void rules match | `unsupported` | structurally approved only; profile remains disabled |
| preseason or regular-season two-way moneyline | none | NFL game can finish tied, so a binary win/loss model cannot assume a zero tie probability | tie-capable settlement or push requires unavailable push-aware probability and EV math | `unsupported` | `BLOCKED` with `PUSH_MODEL_UNAVAILABLE` |
| three-way moneyline or a market with a tie/draw option | none | outcome space differs from a binary two-team moneyline | separate tie outcome is not the registered settlement contract | `unsupported` | `BLOCKED` with `MARKET_IDENTITY_MISMATCH` |
| regulation-only moneyline | none | period and overtime treatment differ from full game | overtime excluded and settlement differs | `unsupported` | `BLOCKED` with `MARKET_IDENTITY_MISMATCH` |
| principal `Spread` with reciprocal team handicaps at the same `x.5` | `nfl.full_game.spread` | same event; exact reciprocal half-point; both sides from the same book; provider marks the line as principal, not alternate | full game; overtime, void, and settlement rules match; push impossible | `unsupported` | structurally approved only; profile remains disabled |
| principal `Total` or `Game Total` with exact `Over/Under x.5` | `nfl.full_game.total` | same event and threshold; complete over/under pair from one book; provider marks the line as principal, not alternate | full game; overtime, void, and settlement rules match; push impossible | `unsupported` | structurally approved only; profile remains disabled |
| whole-number spread or total | none | a push is possible at the quoted number | push-aware probability and EV math are unavailable | `unsupported` | `BLOCKED` with `PUSH_MODEL_UNAVAILABLE` |
| alternate, team, partial-game, live, parlay, or player-prop shape | none | identity, participant, line family, period, or product differs | not the registered full-game principal-line contract | `unsupported` | `BLOCKED` with `MARKET_IDENTITY_MISMATCH` or catalog absence |

For `nfl.full_game.moneyline`, a two-way display is not proof that a tie is impossible. The event's official competition rules and the exact book settlement terms must independently establish `tie_possible=false`, `tie_treatment=impossible_by_competition_rule`, and `push_behavior=impossible`. Postseason labeling alone does not replace settlement verification. Any unknown or conflicting tie field is `BLOCKED` with `PUSH_MODEL_UNAVAILABLE` or `SETTLEMENT_RULE_MISMATCH`, as applicable.

For spreads and totals, `principal` means the sportsbook's identified main pregame full-game line at capture time. An alternate line does not become principal because another book happens to quote the same threshold. Every comparison pair must use the candidate's exact threshold, reciprocal sides where applicable, period, overtime, push, and void contract.

Never manufacture an opposing outcome, combine opposite sides from different books, infer a missing tie price, or substitute a nearby threshold.

---

### 3.2 Outcome-set and probability policy

`nfl_market_consensus_mean_v1` narrows the global same-line consensus gate without redefining it:

1. Exclude the target sportsbook from fair probability and comparison coverage.
2. Require at least two usable non-target books assigned to two distinct resolved pricing-origin groups.
3. Require a complete exact opposing pair from each included book. Never construct a pair across books.
4. Match jurisdiction, event, participant, canonical market, threshold, period, overtime, `season_phase`, tie, push, void, and settlement rules exactly.
5. De-vig each book separately with the project's two-way proportional method.
6. Aggregate only the included source-level fair probabilities with an unweighted arithmetic mean, version `nfl_market_consensus_mean_v1`.
7. Require target-quote age no greater than 180 seconds, comparison-quote age no greater than 300 seconds, and collection-time skew no greater than 300 seconds.
8. Report target exclusion; raw, usable, and pricing-origin counts; every source-level pair and fair probability; the mean; dispersion; oldest comparison age; collection skew; and every exclusion with an existing reason code.

| profile | source-level outcome-set requirement | de-vig method | push requirement | dead-heat requirement | current status |
|---|---|---|---|---|---|
| `nfl.full_game.moneyline` | one complete same-book binary pair only when competition and book rules prove tie and push impossible | `nfl_market_consensus_mean_v1` after activation | impossible and explicitly verified | not applicable | inactive specification; profile disabled |
| `nfl.full_game.spread` | one complete same-book reciprocal principal half-point pair | `nfl_market_consensus_mean_v1` after activation | impossible at the exact half-point line | not applicable | inactive specification; profile disabled |
| `nfl.full_game.total` | one complete same-book principal half-point Over/Under pair | `nfl_market_consensus_mean_v1` after activation | impossible at the exact half-point line | not applicable | inactive specification; profile disabled |

If fewer than two usable independent comparison books remain, use `WATCH` during a future approved research run and `BLOCKED` at its final check. The brief may show the target price, boosted price, break-even probability, and labeled non-consensus comparisons, but it may not report positive EV or `ACTIONABLE FOR REVIEW`.

Under the current lifecycle, even a structurally valid, fresh, independent consensus produces `BLOCKED` with `ADAPTER_PROFILE_DISABLED`; no recommendation-grade calculation or candidate generation may run.

---

<!-- adapter-section: 4 source_compliance -->
## 4. Source and compliance policy

Source IDs resolve through `source_registry_v1` in `SPORT_ADAPTERS/source_registry.yaml`. The registry owns URLs, access/automation permission, season artifacts, coverage posture, review dates, and triggers; this adapter owns the NFL-required facts and gates. URL health alone clears none of them.

| source_id/class | facts or markets supplied | authority rank | access method | jurisdiction coverage | timestamp behavior | terms/license reviewed | permitted use | current status |
|---|---|---:|---|---|---|---|---|---|
| `nfl_official_schedule`, `nfl_flexible_scheduling_procedures` | event identity, scheduled kickoff, flex/TBD changes, and season phase | 1 | registry-owned | league-wide event facts | retain official effective/publication time and local UTC retrieval | see registry | manual operational verification and material-event evidence only | registry posture controls |
| `nfl_important_dates`, `nfl_official_injury_reporting_policy_2026` | season-specific practice-report and game-status-report filing windows | 1 | registry-owned | league policy | retain season/policy version, deadline timezone, publication/effective time, and local UTC retrieval | see registry | manual official-report deadline and submission-state verification | exact 2026 injury artifact unresolved; cannot clear gate |
| `nfl_official_inactives` | official game-day inactive list | 1 | registry-owned | named event/team | retain list publication time and local UTC retrieval | see registry | manual inactive-state verification and price invalidation | registry posture controls |
| `nfl_rulebook_2025` | season-specific overtime/tie competition rules | 1 | registry-owned | competition rule by season phase | retain rulebook season/version and local UTC retrieval | see registry | historical settlement-identity evidence only; sportsbook rules still required | wrong-season for 2026; cannot clear tie gate |
| `source_class_official_team_announcement` | injury status, starting quarterback, roster, venue, roof, relocation, or operational change | 1-2 | registry-owned | named club/event | publication/effective time and local UTC retrieval required | see registry | material operational fact and price invalidation | exact instance required |
| `source_class_licensed_sports_data_provider` | schedule, event status, injury report, availability, quarterback, inactive, roster, or venue facts | 2 | registry-owned | contract-defined | provider update and local UTC timestamps retained | see registry | operational facts within reviewed license | exact instance required |
| `nws_weather_api`, `source_class_official_non_us_operational` | venue-matched observations, forecasts, alerts, and operational weather risk | 1 for official weather facts | registry-owned | mapped venue/location | observation/forecast validity and local UTC retrieval required | see registry | operational gate under a versioned rule only; not a probability input | exact venue/rule mapping required |
| `sportsbook_target_manual_evidence`, `source_class_permitted_sportsbook_feed` | exact target quote, promotion, jurisdiction, tie, push, void, and settlement terms | 1 for displayed target | registry-owned | exact displayed book and state only | local UTC capture required; provider time retained when present | see registry | target identity and promotion evidence | manual fallback; feed requires registration |
| `source_class_licensed_multi_book_odds_provider` | exact target or comparison markets | 1-2 for quoted markets | registry-owned | contract-defined books and jurisdictions | provider and local UTC timestamps retained | see registry | exact quotes within reviewed permission | exact instance required |
| `sportsbook_comparison_manual_evidence`, `source_class_permitted_sportsbook_feed` | one non-target comparison book | 2 | registry-owned | exact displayed book and state only | local UTC capture required | see registry | one exact complete opposing pair | manual conditional; feed requires registration |
| `source_class_secondary_reporting_lead` | possible registered material-change lead | 4 | registry-owned | named event/team; not an odds-jurisdiction source | publication and retrieval times required | see registry | may create `WATCH` pending authoritative confirmation in a future active run | never recommendation-grade alone |

The `nfl_terms_of_use` registry record preserves the restriction on systematic retrieval absent express prior written consent. NFL.com and NFL Football Operations pages therefore remain manual/on-demand references in this adapter unless a separate license or permission expressly covers the intended use. Do not scrape them, depend on undocumented endpoints, or treat a public page as authorization for a poller.

Store injury-report filing rules as a season-specific configuration such as `nfl_injury_reporting_policy_2026_v1`. Store game-day inactive timing in the same reverified policy family. Never carry a prior season's day/time assumptions into a new season without checking the current official policy.

The official flex-scheduling policy makes certain kickoff assignments subject to change and is itself season-specific. A confirmed flex, Week 18 assignment, venue move, or kickoff change is a material event change; its official effective/publication time must invalidate every older affected quote.

For every source retain the source identifier or URL, retrieval time in UTC, provider object IDs where present, exact jurisdiction, and raw snapshot reference or content hash. Never automate an authenticated sportsbook page, spoof location, bypass geolocation or anti-bot controls, evade rate limits, or use one state's feed as evidence for another.

---

<!-- adapter-section: 5 signal_registry -->
## 5. Active signal registry

The shared `promo_terms`, `target_quote`, `comparison_quotes_same_line`, `market_status`, and `promo_expiration` signals retain their only authoritative ten-field definitions in Section 5 of `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md`. The extensions below add NFL constraints and do not create duplicate signal IDs or collection paths.

All NFL-specific rows are complete pre-activation contracts but are dormant while every profile is `disabled_provider_validation`. They authorize contract-scenario review only, not source polling or candidate generation.

### 5.1 Inherited shared-signal extensions

| shared_signal_id | profiles | NFL-specific identity/settlement constraint | maximum-age override | reporting extension |
|---|---|---|---|---|
| `promo_terms` | all NFL profiles | verify event/market/odds eligibility, token count, cap, expiry, overtime, season phase, tie, push, void, cancellation, and token-return rules | inherit; reverify at final check after activation | show every material term, confidence, and ambiguity |
| `target_quote` | all NFL profiles | require exact target book/jurisdiction, raw market/selection, event, participant, principal-line status, period, line, overtime, season phase, tie, push, settlement, status, and timestamp | inherit 180 seconds | show raw/canonical identity, local NFL audit fields, jurisdiction, status, age, and `unsupported` AP compatibility |
| `comparison_quotes_same_line` | all NFL profiles | require two complete exact pairs from distinct resolved non-target pricing origins and apply `nfl_market_consensus_mean_v1` | inherit 300 seconds and 300-second skew | show target exclusion, source-level fair probabilities, dispersion, ages/skew, origins, and exclusions |
| `market_status` | all NFL profiles | a post-material-change batch must prove every included market is open and synchronized | inherit | show non-open state, change time, and synchronization result |
| `promo_expiration` | all NFL profiles | no additional collection path | inherit | show time remaining |

### 5.2 NFL-specific signal registry

| signal_id | market_profile | tier | source_hierarchy | refresh_trigger | maximum_age | material_change_rule | candidate_state_effect | probability_use | reporting_rule |
|---|---|---|---|---|---|---|---|---|---|
| `nfl_event_identity_status` | all NFL profiles | A/C | `nfl_official_schedule`; `nfl_flexible_scheduling_procedures`; `source_class_official_team_announcement`; `source_class_licensed_sports_data_provider` | baseline, T-24h, T-6h, T-90m, final check, and confirmed schedule/status change | 600 seconds inside T-2h; event identity retained for run; latest official flex/status publication controls | event ID, opponents, season phase, venue, neutral/international state, kickoff, flex/TBD assignment, scheduled/delayed/postponed/canceled status, or relocation changes | identity conflict, cancellation, or unresolved postponement `BLOCKED`; resolvable change `WATCH` and synchronized refetch after activation | none | always show identity/season phase; emphasize flex/status changes and blockers |
| `nfl_injury_report_state` | all NFL profiles | A/C | `nfl_official_injury_reporting_policy_2026`; `source_class_official_team_announcement`; `source_class_licensed_sports_data_provider` | baseline, each applicable filing deadline, each revision, T-24h through final check | current report version; retrieval <=600 seconds inside T-2h; must postdate latest known update | required practice/game-status report becomes due, missing, submitted, corrected, or revised; team row/version changes | not due or incomplete `WATCH` in research; overdue final report `BLOCKED`; revision newer than quotes `WATCH` and refetch after activation | none | show policy version, applicable deadline/timezone, submission/version state, and affected-team changes |
| `nfl_team_availability_delta` | all NFL profiles | C | `nfl_official_injury_reporting_policy_2026`; `source_class_official_team_announcement`; `source_class_licensed_sports_data_provider` | every official report revision and candidate-relevant confirmation | same current-report rule as `nfl_injury_report_state` | player added/removed or practice, game-status, illness, suspension, personal, or participation designation changes after quote retrieval | `WATCH` and synchronized target/comparison refetch after activation; unresolved authoritative conflict `BLOCKED` at final check | none | show exact old/new official state and timestamps only; no narrative adjustment |
| `nfl_starting_quarterback_status` | all NFL profiles | A/C | `source_class_official_team_announcement`; `nfl_official_injury_reporting_policy_2026`; `source_class_licensed_sports_data_provider` | baseline, every report/revision, confirmed starter announcement, T-90m, and final check | current official status; retrieval <=600 seconds inside T-2h; must postdate latest candidate-relevant change | expected starter identity or official availability changes; starter becomes questionable/doubtful/out/inactive; replacement is confirmed; conflicting authoritative reports appear | material change `WATCH` and refetch; unresolved identity/availability conflict `BLOCKED` at final check; out/inactive is not a manual probability penalty | none | always show current starter identity/status or blocker for shortlisted future scenarios |
| `nfl_inactive_list_state` | all NFL profiles | A/C | `nfl_official_inactives`; `source_class_official_team_announcement`; `source_class_licensed_sports_data_provider` | season-policy release window, publication, correction, T-90m, and final check | current official list; local retrieval <=300 seconds after publication for final use; must postdate any correction | list becomes due/published/corrected; starting quarterback or registered candidate-relevant participant changes active/inactive state | not due `WATCH` in preliminary research; overdue/missing or conflicting final list `BLOCKED`; material inactive change `WATCH` and refetch after activation | none | show policy version, publication time, relevant inactive entries, corrections, and synchronization state |
| `nfl_roster_transaction_eligibility` | all NFL profiles | A/C | `source_class_official_team_announcement`; `source_class_licensed_sports_data_provider` | baseline, T-24h, T-6h, and confirmed candidate-relevant change | retrieval <=3600 seconds distant and <=600 seconds inside T-2h; latest effective transaction controls | team membership, activation, elevation, signing, waiver, release, trade, suspension, reserve-list, or eligibility state changes after quotes | identity conflict `BLOCKED`; clear promotion violation `INELIGIBLE`; other material change `WATCH` and refetch after activation | none | report candidate-relevant transaction, effective time, and identity effect only |
| `nfl_venue_state` | all NFL profiles | A/C | `nfl_official_schedule`; `nfl_flexible_scheduling_procedures`; `source_class_official_team_announcement`; `source_class_licensed_sports_data_provider` | baseline, T-24h, T-6h, T-90m, final check, and venue/roof/surface change | 600 seconds inside T-2h for mutable operational state; event-scoped identity retained | venue, city, neutral/international site, playing surface, roof/wall designation, relocation, or operational availability changes | identity conflict or unresolved relocation `BLOCKED`; material resolvable change `WATCH` and synchronized refetch after activation | none | always show venue/neutral state; roof, surface, or relocation only when material |
| `nfl_operational_weather` | all NFL profiles | A/C | `nws_weather_api`; `source_class_official_non_us_operational`; `source_class_official_team_announcement` | early outlook, T-24h, T-6h, T-90m, T-30m, final check, and configured threshold/alert change | 900 seconds inside T-2h; latest official operational notice controls | venue-matched configured rule changes among `CLEAR`, `WATCH`, and `BLOCKED`, including delay, postponement, relocation, roof/wall, unsafe travel, or field-operation conditions | configured `WATCH` or `BLOCKED`; resolution requires synchronized post-change quotes after activation | none | report venue, source validity time, rule version, and operational state only; never describe weather as an edge |

<!-- adapter-section: 6 materiality_state -->
## 6. Materiality and state rules

| rule_id | profiles | source fields / qualifying change | effective-time rule | state effect | required refetch | resolution rule | probability effect |
|---|---|---|---|---|---|---|---|
| `nfl_event_state_materiality_v1` | all NFL profiles | event/opponents, season phase, venue, neutral/international state, kickoff, flex/TBD assignment, delay, postponement, cancellation, relocation, or status changes | any authoritative effective/publication time newer than an affected quote invalidates it | conflict/cancellation/unresolved postponement `BLOCKED`; resolvable change `WATCH` after activation | shared target and complete comparison signals | current authoritative event state plus synchronized post-change batch | none |
| `nfl_injury_availability_materiality_v1` | all NFL profiles | report due/submitted/missing/revised state or candidate-relevant official availability designation change | compare season-policy deadline and report publication/effective time with every affected quote retrieval | missing due report `WATCH`, then `BLOCKED` at final check; newer change `WATCH` after activation | shared target and complete comparison signals | current report/version and availability facts plus synchronized post-change batch | none |
| `nfl_starting_quarterback_materiality_v1` | all NFL profiles | expected starter identity, official availability, replacement confirmation, or authoritative conflict | any qualifying fact newer than a quote invalidates it | `WATCH` after activation; unresolved final identity/status conflict `BLOCKED` | shared target and complete comparison signals | current verified quarterback identity/status plus synchronized post-change batch | none |
| `nfl_inactive_list_materiality_v1` | all NFL profiles | inactive list due/published/corrected or registered participant active/inactive state changes | list publication/correction time compared with every affected quote | not due `WATCH`; overdue/missing/conflicting final list `BLOCKED`; newer correction `WATCH` after activation | shared target and complete comparison signals | current official list plus synchronized post-change batch | none |
| `nfl_roster_transaction_materiality_v1` | all NFL profiles | membership, activation, elevation, signing, waiver, release, trade, suspension, reserve-list, or eligibility change | official effective/publication time compared with affected quotes | identity conflict `BLOCKED`; clear promotion violation `INELIGIBLE`; otherwise `WATCH` after activation | shared target and complete comparison signals | resolved identity/eligibility plus synchronized post-change batch | none |
| `nfl_venue_weather_materiality_v1` | all NFL profiles | venue/relocation/surface/roof/wall state or configured operational-weather rule crosses `CLEAR`, `WATCH`, or `BLOCKED` | latest venue-matched official/configured fact must postdate prior state and be compared with affected quotes | configured `WATCH` or `BLOCKED`; identity conflict `BLOCKED` | shared target and complete comparison signals after resolution | current venue/operational state plus synchronized post-resolution batch | none |
| `nfl_post_change_price_sync_v1` | all NFL profiles | market suspension/reopening or any target/comparison quote older than a registered material fact | every included quote must postdate the newest applicable material fact and meet age/skew rules | remain `WATCH` after activation; unavailable/suspended final batch `BLOCKED`; valid batch re-ranks from Tier B only | shared target, comparison, and market-status signals | synchronized open batch with valid consensus and `post_material_change_synchronized=true` | none |

### 6.1 State-resolution rules

- A lifecycle check precedes every other gate. While the selected profile is `disabled_provider_validation`, return `BLOCKED` with `ADAPTER_PROFILE_DISABLED`, do not fetch sources, and do not generate candidates. Contract-scenario rows below may still document the state a future activated run would have reached.
- Before an applicable injury-report or inactive-list deadline, store `not_due`; any preliminary future result remains `WATCH` and cannot clear the final critical-context gate.
- After an applicable deadline, a missing, stale, or conflicting required report/list is `WATCH` during future research and `BLOCKED` at the final check.
- A starting-quarterback identity or availability conflict remains `WATCH` until resolved and becomes `BLOCKED` at the final check. A confirmed change newer than prices invalidates the batch but never causes a manual probability penalty.
- A schedule flex, kickoff change, relocation, venue/roof/surface change, injury revision, availability change, inactive correction, roster transaction, or operational-weather change newer than any affected quote requires `WATCH` and a synchronized target/comparison refresh after activation.
- Suspended, closed, unknown-status, stale, or settlement-mismatched target quotes are `BLOCKED`. Excluded comparisons reduce coverage and may cause `CONSENSUS_INSUFFICIENT`.
- A canceled event, unresolved event identity, or unresolved postponement is `BLOCKED`. A clear promotion violation is `INELIGIBLE` only after exact terms prove it.
- A resolved material fact clears its context blocker only when every included quote is newer than the fact, open, within 180/300/300 limits, and the consensus remains valid. Refreshed Tier B prices are the only active numerical valuation input.
- `nfl_operational_weather_rules_v1` must name the source field, operator, threshold/qualifying value, venue/time match, roof handling, state effect, and resolution for every operational rule. If a required rule or venue mapping cannot be evaluated, use `WATCH` and then `BLOCKED` at final check after activation. Generic wind, temperature, precipitation, travel, or field-condition prose never creates an edge.

Every contract scenario or future candidate snapshot must include:

```yaml
monitoring_metadata:
  next_refresh_at: datetime | null
  next_refresh_reason: registered signal or final-check reason
  post_material_change_synchronized: boolean
```

These values and the NFL-local identity fields are local brief/audit annotations until a separately reviewed persisted-schema change is approved.

---

<!-- adapter-section: 7 refresh_policy -->
## 7. Refresh policy

The six phases below specify the evidence cadence for credential-free contract scenarios and for a possible future approved on-demand run. They do not authorize execution while profiles are disabled and do not install a scheduler, background poller, automatic alert, closing-line job, or settlement job.

| phase_id | NFL window or trigger | required refresh after activation | maximum ages | state if unavailable after activation | next refresh reason |
|---|---|---|---|---|---|
| `intake` | promotion intake | each token's terms; eligible slate; event, season phase, tie/settlement, venue, report/list state; target; comparison pairs; source/jurisdiction metadata | source/event scoped; quote limits apply | material term/target missing `BLOCKED`; incomplete critical context or consensus `WATCH` | applicable report deadline, schedule/flex update, provider refresh, or material fact |
| `distant_pregame` | around T-24h and T-6h | event/kickoff/flex state, roster transaction, official report state, quarterback status, venue/early operational risk, target, and comparisons | roster <=3600 seconds distant; quotes 180/300 seconds with <=300-second skew when used for valuation | `WATCH` when required current evidence or consensus is unavailable | next report filing, flex/status event, or T-2h window |
| `official_release_window` | each season-specific injury/game-status filing window through the official inactive-list window | report/version for both teams, changed availability rows, quarterback, roster, inactive-list state, event/venue notices, target, and comparisons after material changes | current report/list; <=600 seconds for sport facts inside T-2h; inactive list <=300 seconds after publication; quote limits apply | missing after due time `WATCH`; unresolved final requirement `BLOCKED` | next filing/revision, inactive publication, confirmed change, or synchronized batch |
| `material_change` | any registered material event | invalidate affected quotes; refresh the changed fact, target, complete comparisons, market status, and synchronization audit | target <=180 seconds; comparisons <=300 seconds; skew <=300 seconds; facts per registry | `WATCH`; final unavailable synchronized batch `BLOCKED` | synchronized post-change price batch |
| `shortlist_check` | around T-90m and T-30m | shortlist identity/eligibility, event, report/availability, quarterback, inactive list, roster, venue/weather, target, comparisons, and consensus audit | registry ages and 180/300/300 quote limits | `WATCH` or `BLOCKED` according to failed gate | inactive publication/correction or final synchronized check |
| `final_sync` | immediately before human placement after activation | promotion, event/season/tie identity, report/availability, quarterback, inactives, roster, venue/weather, target, comparisons, jurisdiction, settlement, and QA | all final recommendation-grade limits | any fatal, stale, missing, disabled, or conflicting input `BLOCKED` | none; new evidence requires a new run |

While lifecycle remains disabled, every phase stops at the lifecycle gate with `BLOCKED` and `ADAPTER_PROFILE_DISABLED`. The phase table exists so future provider evidence and contract scenarios are evaluated against a complete contract rather than an invented cadence.

---

<!-- adapter-section: 8 tier_d_registry -->
## 8. Tier D model-only registry

All groups below are `disabled_model_only`. They are hypotheses, not active metrics, and must not be routinely fetched, stored as model inputs, scored, narrated, or used to change probability, state, or rank.

| group_id | potential profile consumers | candidate future inputs | required source permission | named model consumer | activation evidence | anti-noise boundary | lifecycle |
|---|---|---|---|---|---|---|---|
| `nfl_model_team_efficiency_pace` | moneyline, spread, total | versioned possession pace, play efficiency, drive outcomes, calibrated opponent adjustments | separately licensed/permitted data | none | exact-market model, leak-free history, out-of-sample result, calibration, uncertainty, monitoring | no raw season rank, points-per-game rank, or recent-score narrative | `disabled_model_only` |
| `nfl_model_quarterback_offense` | moneyline, spread, total | projected quarterback identity, dropbacks, efficiency, pressure response, receiver/line context | separately licensed/permitted data | none | same full model requirements | no manual quarterback points, one-game result, win-loss record, or reputation adjustment | `disabled_model_only` |
| `nfl_model_trenches_and_defense` | moneyline, spread, total | versioned offensive-line continuity, pass protection, run blocking, pressure, coverage, and run-defense measures | separately licensed/permitted data | none | same full model requirements | no generic unit ranking, sack total, or tiny matchup split | `disabled_model_only` |
| `nfl_model_availability_role` | moneyline, spread, total | snap/route/rush/target role, replacement mapping, active roster, and uncertainty distributions | separately licensed/permitted data | none | same full model requirements | no direct injury headline or fantasy ranking adjustment; do not double-count refreshed prices | `disabled_model_only` |
| `nfl_model_weather_field` | spread and total; moneyline only if validated | venue-matched wind, precipitation, temperature, surface, roof, and calibrated scoring effects | separately licensed/permitted data | none | same full model requirements | operational weather remains a separate gate; no generic bad-weather narrative | `disabled_model_only` |
| `nfl_model_rest_travel_coaching` | moneyline, spread, total | versioned rest, travel, time-zone, coaching/system, and schedule effects | separately licensed/permitted data | none | same full model requirements | no revenge, primetime, short-week, travel, interim-coach, or must-win story without a validated consumer | `disabled_model_only` |

NFL.com content is not an approved systematic model-input source under the current terms. A future model must identify a separately licensed or expressly permitted source, exact fields and transformations, and the complete activation evidence required by `ADAPTER_TEMPLATE.md`.

---

<!-- adapter-section: 9 tier_x_exclusions -->
## 9. Tier X exclusions

| excluded group | examples | reason excluded | permitted operational use |
|---|---|---|---|
| recent results and betting trends | last five, streaks, ATS/over-under records, head-to-head, home/away or day-of-week splits | no enabled calibrated consumer; unstable or selection-biased | none |
| motivation and broadcast narratives | revenge, must-win, rivalry, primetime, national TV, homecoming, milestone, coach/player confidence | narrative rather than validated input | none |
| unsupported market claims | public betting percentages, social sentiment, steam, anonymous or unsupported sharp-money labels | unresolved provenance and no probability contract | none |
| injury, roster, or quarterback rumors | generic headline, anonymous report, depth-chart guess, fantasy projection | insufficient authority for a registered fact | lower-authority lead may create `WATCH` only after activation pending approved confirmation |
| weak matchup proxies | generic offense/defense rank, fantasy points allowed, tiny coverage/player samples, raw prior matchup | disabled or unvalidated model input | none |
| weather and field narratives | cold-weather record, wind game story, snow-team reputation, generic poor field claim | no configured operational rule or validated model | authoritative lead may create `WATCH` pending venue-matched confirmation only |
| player-prop narratives | target share, rushing role, passing/rushing/receiving yard trend, touchdown streak | no NFL prop profile is registered | none |
| LLM-authored adjustment | manually invented probability, score, or ranking change | violates deterministic valuation boundary | none |

Tier X material cannot supply probability, rank, positive-EV language, or persuasive candidate support.

---

<!-- adapter-section: 10 provider_evidence -->
## 10. Provider evidence

No recommendation-grade automated target source, comparison-origin configuration, or context feed is certified by this document. Contract scenarios prove expected documentation behavior only; they do not prove live coverage, source permission, or promotion readiness. Real timestamped captures belong in provider evidence; future machine-readable inputs belong in executable fixture files backed by a test runner.

| evidence_id | profile scope | role | timing conditions required | current evidence state | certification effect |
|---|---|---|---|---|---|
| `nfl_game_line_target_cross_timing` | all three profiles | target | board open/distant pregame, after schedule or availability change, after inactive release, and near kickoff | not recorded | none; profiles remain disabled |
| `nfl_game_line_comparison_origins` | all three profiles | comparison | same timing conditions with exact complete pairs, 180/300/300 compliance, target exclusion, and two resolved non-target origins | no two-origin configuration certified | none; profiles remain disabled |
| `nfl_moneyline_tie_settlement_validation` | moneyline | identity/settlement | representative preseason, regular-season, and postseason events plus exact book rules | no provider/book configuration proves all required tie fields | none; moneyline remains disabled and tie-capable shapes fail structurally |
| `nfl_context_cross_timing` | all three profiles | sport facts | report filing, quarterback change, inactive release/correction, roster event, flex/venue change, weather resolution, and near kickoff | not recorded | none; profiles remain disabled |

For each target capture, record exact agreement with timestamped user-visible evidence on sportsbook, jurisdiction, event, teams, market, side, line, principal/alternate designation, period, overtime, season phase, tie, push, void, settlement, status, and price. A price difference is explainable only when timestamps demonstrate market movement rather than identity failure.

For each comparison origin, require its own complete exact pair and resolved pricing-origin identity. Retain request/capture start and end times, provider timestamp when present, local UTC retrieval, raw snapshot/content hash, user-visible agreement when available, every exclusion, and discrepancy resolution.

Validation must cover board open or distant pregame, after each category of registered material change, after official inactive publication, and near kickoff. It must demonstrate stale, suspended, duplicate, one-sided, mismatched, unresolved-origin, schema-change, and provider-failure behavior. Provider exposure or one successful capture never certifies future coverage.

Promotion to `pilot_enabled` requires credential-free recorded evidence, deterministic calculation and executable-fixture verification, source and terms approval, exact market and settlement validation, two independent non-target comparison origins, all governing-document updates, and separate explicit activation approval.

---

<!-- adapter-section: 11 contract_scenarios_fixtures -->
## 11. Contract scenarios and executable fixtures

```yaml
executable_fixtures:
  schema_version: not_implemented
  implementation_status: not_implemented
  fixture_paths: []
  deterministic_runner: not_implemented
  paid_or_live_calls_required: false
  provider_certification_claimed: false
```

These Markdown rows are synthetic contract scenarios, not provider evidence, executable fixtures, or claims about a real sportsbook or provider. The timestamps, books, events, and prices are synthetic. Every structurally valid scenario still stops at the lifecycle gate with `BLOCKED` and `ADAPTER_PROFILE_DISABLED`; the future-rule column records the additional behavior that must remain true after a separately approved activation.

| scenario_id | credential-free input condition | current required outcome | future contract behavior / audit evidence |
|---|---|---|---|
| `nfl_fx_postseason_ml_valid_shape` | synthetic postseason event; target `Moneyline`; overtime included; `tie_possible=false`; tie impossible by current competition rule; no push; exact book rule verified; target age 60s; two non-target complete pairs ages 90s/120s from origins A/B; skew 60s | `BLOCKED`; `ADAPTER_PROFILE_DISABLED`; no candidate generation | structurally valid; after activation deterministic EV/ranking may run only with rulebook/book versions, target exclusion, per-book de-vig, and `nfl_market_consensus_mean_v1` audit |
| `nfl_fx_regular_ml_tie` | synthetic regular-season two-way moneyline; `tie_possible=true`; book refunds/pushes a tie | `BLOCKED`; `PUSH_MODEL_UNAVAILABLE`; `ADAPTER_PROFILE_DISABLED` | reject before consensus; preserve season phase, tie treatment, and raw labels |
| `nfl_fx_preseason_ml_tie` | synthetic preseason moneyline; tie can remain final; push/tie treatment is not impossible | `BLOCKED`; `PUSH_MODEL_UNAVAILABLE`; `ADAPTER_PROFILE_DISABLED` | reject before consensus; no zero-tie assumption |
| `nfl_fx_three_way_ml` | synthetic full-game home/draw/away market | `BLOCKED`; `MARKET_IDENTITY_MISMATCH`; `ADAPTER_PROFILE_DISABLED` | three-outcome market is not the binary registered profile |
| `nfl_fx_regulation_only_ml` | synthetic `60-Minute Moneyline`; overtime excluded | `BLOCKED`; `MARKET_IDENTITY_MISMATCH`; `ADAPTER_PROFILE_DISABLED` | period/overtime mismatch retained in raw/canonical audit |
| `nfl_fx_half_spread_valid_shape` | synthetic principal `-2.5/+2.5` full-game pair; overtime and settlement match; valid fresh independent consensus | `BLOCKED`; `ADAPTER_PROFILE_DISABLED`; no candidate generation | structurally valid reciprocal no-push line; after activation calculate only from exact same-line pairs |
| `nfl_fx_whole_spread` | synthetic principal `-3/+3` | `BLOCKED`; `PUSH_MODEL_UNAVAILABLE`; `ADAPTER_PROFILE_DISABLED` | never treat push probability as zero |
| `nfl_fx_half_total_valid_shape` | synthetic principal `Over/Under 47.5`; full game; valid fresh independent consensus | `BLOCKED`; `ADAPTER_PROFILE_DISABLED`; no candidate generation | structurally valid no-push line; after activation calculate only from exact same-line pairs |
| `nfl_fx_whole_total` | synthetic principal `Over/Under 47` | `BLOCKED`; `PUSH_MODEL_UNAVAILABLE`; `ADAPTER_PROFILE_DISABLED` | never treat push probability as zero |
| `nfl_fx_alternate_line` | synthetic alternate `-6.5/+6.5` while principal is `-3.5/+3.5` | `BLOCKED`; `MARKET_IDENTITY_MISMATCH`; `ADAPTER_PROFILE_DISABLED` | alternate designation and raw labels retained |
| `nfl_fx_target_excluded` | synthetic target book also appears in comparison payload plus two independent non-target origins | `BLOCKED`; `ADAPTER_PROFILE_DISABLED`; no candidate generation | exclude target from probability and coverage; audit target exclusion, then use only origins A/B after activation |
| `nfl_fx_origin_duplicate` | two comparison records resolve to the same underlying pricing origin | `BLOCKED`; `ADAPTER_PROFILE_DISABLED`; `CONSENSUS_INSUFFICIENT` when only one independent origin remains | count the origin once; show duplicate exclusion and break-even only |
| `nfl_fx_one_sided_or_synthetic_pair` | one book supplies candidate side only, or opposing side is taken from another book | `BLOCKED`; `ADAPTER_PROFILE_DISABLED`; `CONSENSUS_INSUFFICIENT` | exclude as non-de-viggable; never create a cross-book pair |
| `nfl_fx_stale_suspended` | target age 181s or target status suspended; comparison age 301s or included batch skew 301s | `BLOCKED`; `TARGET_QUOTE_STALE` or `MARKET_SUSPENDED`; `ADAPTER_PROFILE_DISABLED`; stale comparison excluded | enforce 180/300/300 exactly; downgrade coverage and preserve ages/status |
| `nfl_fx_settlement_mismatch` | target and comparison differ on overtime, season phase, tie, push, or void treatment | `BLOCKED`; `SETTLEMENT_RULE_MISMATCH`; `ADAPTER_PROFILE_DISABLED` | reject equivalence; show both raw identities and settlement fields |
| `nfl_fx_flex_change_after_quotes` | official kickoff/flex change timestamp is newer than target and comparisons | `BLOCKED`; `ADAPTER_PROFILE_DISABLED`; no fetch or candidate generation | after activation apply `nfl_event_state_materiality_v1`: `WATCH`, invalidate batch, synchronized refetch, no probability adjustment |
| `nfl_fx_injury_report_not_due` | applicable season-policy filing deadline has not arrived | `BLOCKED`; `ADAPTER_PROFILE_DISABLED` | after activation preliminary state is `WATCH`; store policy version/deadline and next refresh |
| `nfl_fx_injury_report_overdue` | required report is due but absent or stale | `BLOCKED`; `ADAPTER_PROFILE_DISABLED`; `OFFICIAL_REPORT_MISSING` | after activation remain `WATCH` during research and `BLOCKED` at final check |
| `nfl_fx_availability_revision` | official candidate-relevant availability row changes after quotes | `BLOCKED`; `ADAPTER_PROFILE_DISABLED`; no fetch or candidate generation | after activation `WATCH`, synchronized refetch, exact old/new timestamps, no direct probability effect |
| `nfl_fx_quarterback_change` | expected starting quarterback changes or is ruled out after quotes | `BLOCKED`; `ADAPTER_PROFILE_DISABLED`; no manual penalty | after activation `WATCH` under `nfl_starting_quarterback_materiality_v1`; require verified replacement/status and synchronized prices |
| `nfl_fx_quarterback_conflict` | authoritative sources conflict on starting-quarterback identity/status at final check | `BLOCKED`; `ADAPTER_PROFILE_DISABLED`; `SOURCE_CONFLICT` | cannot clear until authoritative current identity/status is resolved |
| `nfl_fx_inactives_not_due` | official inactive list has not reached the season-policy release window | `BLOCKED`; `ADAPTER_PROFILE_DISABLED` | after activation preliminary state is `WATCH`; next refresh is official inactive publication |
| `nfl_fx_inactive_correction` | official inactive list or correction changes a registered participant after quotes | `BLOCKED`; `ADAPTER_PROFILE_DISABLED`; no direct probability effect | after activation `WATCH`, record original/correction times, and require synchronized refetch |
| `nfl_fx_roster_change` | official elevation, activation, trade, suspension, reserve move, or release is newer than quotes | `BLOCKED`; `ADAPTER_PROFILE_DISABLED` unless exact terms independently make it `INELIGIBLE` | after activation invalidate prices; resolve identity/eligibility and synchronize |
| `nfl_fx_venue_relocation` | official venue, neutral-site, roof, surface, or relocation fact changes after quotes | `BLOCKED`; `ADAPTER_PROFILE_DISABLED` | after activation `WATCH` or identity `BLOCKED` under `nfl_venue_weather_materiality_v1`; synchronize after resolution |
| `nfl_fx_operational_weather` | venue-matched configured weather/operational rule changes from `CLEAR` to `WATCH` or `BLOCKED` after quotes | `BLOCKED`; `ADAPTER_PROFILE_DISABLED` | after activation enforce configured state, then refresh prices after resolution; no narrative adjustment |
| `nfl_fx_post_change_sync_missing` | material fact at 18:00 UTC; target at 17:59; comparisons at 17:58/17:59 | `BLOCKED`; `ADAPTER_PROFILE_DISABLED`; `post_material_change_synchronized=false` | after activation `WATCH`; all affected quotes must postdate 18:00 and meet 180/300/300 or final state is `BLOCKED` |
| `nfl_fx_post_change_sync_resolved` | same fact at 18:00; open target and two independent complete comparison pairs all retrieved after 18:00 within age/skew limits | `BLOCKED`; `ADAPTER_PROFILE_DISABLED`; no candidate generation | context blocker resolves after activation; rank only from refreshed Tier B prices and set synchronization true |
| `nfl_fx_disabled_profile` | any structurally valid request for one of the three registered profiles | `BLOCKED`; `ADAPTER_PROFILE_DISABLED`; no candidate generation, EV ranking, alert, or provider call | lifecycle and exact activation blocker shown |
| `nfl_fx_unregistered_prop` | passing-yards, rushing-yards, receiving-yards, touchdown, or other NFL prop request | `BLOCKED`; `ADAPTER_PROFILE_DISABLED`; catalog-absence audit annotation; no registered profile | do not map it to a game line or create a profile implicitly |
| `nfl_fx_tier_x_claim` | recent ATS streak, sharp-money claim, quarterback narrative, or generic weather story | `BLOCKED`; `ADAPTER_PROFILE_DISABLED`; claim has no valuation effect | ignore as Tier X; no probability, state improvement, or rank effect |
| `nfl_fx_manual_placement` | user later reports manually placing a researched wager | no AP Frankenstein action from this project | save no downstream write; AP Frankenstein remains separate |

---

<!-- adapter-section: 12 run_decision_brief -->
## 12. On-demand run and decision-brief contract

### Required inputs after a separately approved lifecycle change

- Original promotion text or screenshot, including target book, jurisdiction, token count, boost type, stake/payout cap, odds range, expiry, eligible events/markets, overtime, tie, push, cancellation, void, and token-return rules.
- Exact target-book evidence for every considered candidate, including principal/alternate designation and all NFL-local identity fields.
- At least two complete same-line non-target comparison pairs with resolved pricing-origin metadata.
- Current authoritative event/flex, injury-report, availability, starting-quarterback, inactive-list, roster, venue, and operational-weather facts required by this adapter.
- User risk limits when expected-dollar or exposure ranking depends on them.

Parse multiple tokens separately unless every material term is proven identical. Evaluate the complete eligible opportunity set, rank by expected dollars subject to data quality and user limits, show shared-event/team exposure, and return fewer uses when fewer candidates pass. Never lower a gate to use a token.

### Required current behavior

For any request selecting this adapter now:

1. Parse enough supplied evidence to identify the requested profile without making a provider call.
2. Return `BLOCKED` with `ADAPTER_PROFILE_DISABLED` for a registered profile; add `PUSH_MODEL_UNAVAILABLE`, `MARKET_IDENTITY_MISMATCH`, or `SETTLEMENT_RULE_MISMATCH` when the supplied shape independently fails that structural gate.
3. Do not generate candidates, fetch sources, calculate recommendation-grade EV, create an alert, start a schedule, or claim provider validation.
4. Preserve supplied raw labels, local identity fields, lifecycle, blocker, and the human-control boundary in a local documentation/evidence snapshot only when the user explicitly asks to save one.

### Required future output contract

After activation, use `promotion_decision_brief_v2` and the human-readable brief in `PROMO_ANALYSIS_PLAYBOOK.md`, plus:

- selected adapter/profile ID and version/lifecycle;
- raw and canonical identity plus `season_phase`, `tie_possible`, `tie_treatment`, and `unsupported` AP compatibility;
- target exclusion and comparison-origin audit;
- principal-line, settlement, overtime, tie, push, void, and jurisdiction verification;
- quote ages, collection-time skew, and post-material-change synchronization state;
- current report policy/version, availability, quarterback, inactives, roster, venue, and operational-weather audit;
- unresolved blockers and exact next refresh trigger;
- meaningful passes and opportunity-cost explanation; and
- the sentence: "This report identifies candidates for human review; it has not placed or confirmed a wager."

Save only a local research/evidence snapshot. Do not call, write to, or create a bridge with AP Frankenstein and do not infer that a researched candidate became a wager.

### Reusable task prompt

```text
Evaluate the supplied NFL promotion request against adapter nfl.pregame_full_game_v0_1 version 0.1.1 and adapter_contract_v1.

First apply profile lifecycle. All registered NFL profiles are disabled_provider_validation, so return BLOCKED with ADAPTER_PROFILE_DISABLED and do not call a provider, generate a candidate, calculate recommendation-grade EV, schedule monitoring, or send an alert. Preserve the supplied raw market labels and identify any additional structural blocker.

The only documented shapes are a pregame full-game binary moneyline when tie and push are both proven impossible, a principal reciprocal half-point full-game spread, and a principal half-point full-game total. Regular-season or preseason tie-capable moneylines and whole-number lines require PUSH_MODEL_UNAVAILABLE. Three-way, tie-option, regulation-only, alternate, team-total, partial-game, prop, live, and parlay shapes are identity mismatches or unregistered.

If a later separately approved lifecycle change permits a supervised run, verify every token; exact book/jurisdiction/event/principal line/period/overtime/season-phase/tie/push/void/settlement identity; current target evidence; and at least two fresh complete exact opposing pairs from independent non-target pricing origins. Exclude the target, de-vig each comparison book separately, and apply nfl_market_consensus_mean_v1 with 180/300/300-second target/comparison/skew limits.

Apply only registered NFL event/flex, injury-report, availability, starting-quarterback, inactive-list, roster, venue, operational-weather, and post-change synchronization gates. Any material fact newer than prices invalidates the batch and requires synchronized refetching. Never create a narrative probability adjustment or use Tier D/X information.

Return promotion_decision_brief_v2 with lifecycle, raw/canonical/local NFL identity, sources, timestamps, target/origin exclusions, settlement audit, passes, blockers, next refresh condition, and the human-decision boundary. Save only a local evidence snapshot; never place or confirm a wager and make no AP Frankenstein call or write.
```

---

<!-- adapter-section: 13 activation_change_log -->
## 13. Activation checklist and change log

- [x] Adapter metadata declares `adapter_contract_v1` and version `0.1.1`.
- [x] Three exact pregame full-game profiles are specified with closed lifecycle values.
- [x] Raw/canonical identity, NFL-local tie audit, settlement, and unavailable adjacent shapes are explicit.
- [x] Shared signals are extended by reference and every NFL-specific Tier A/C signal has the ten-field contract.
- [x] The six standard refresh phases, materiality, synchronization, Tier D, Tier X, provider-evidence, contract-scenario, and run contracts are documented.
- [ ] Source access, exact provider coverage, jurisdiction, stable IDs, timestamps, principal-line mapping, and schema behavior are validated across required timing conditions.
- [ ] Target evidence and two independent non-target complete comparison origins satisfy exact identity and 180/300/300 limits.
- [ ] Moneyline tie and push behavior is proven across the applicable competition and sportsbook settlement rules.
- [ ] Credential-free recorded evidence and deterministic calculation tests are reviewed for every missing, stale, conflicting, suspended, push, material-change, and resolution case.
- [x] Governing documents agree on profile records and lifecycle.
- [ ] A separate explicit approval promotes any exact profile to `pilot_enabled` or `active`.

Unchecked items are activation blockers, not implementation permission. No item may be assumed complete from a synthetic contract scenario or a provider's marketing claim.

---

### 13.1 Change log

| date | adapter version | profiles affected | change | evidence/approval reference |
|---|---|---|---|---|
| 2026-07-13 | `0.1.1` | all registered NFL profiles | Normalized the document to the thirteen-section `adapter_contract_v1` structure; added binary outcome-set audit fields and clarified contract scenarios versus provider evidence and executable fixtures | documentation-structure and audit-only change; no lifecycle, probability, outcome, source, freshness, or activation change |
| 2026-07-12 | `0.1.0` | `nfl.full_game.moneyline`, `nfl.full_game.spread`, `nfl.full_game.total` | Created the `adapter_contract_v1` NFL pre-activation documentation contract with all profiles disabled; added tie-safe moneyline identity, principal half-point line rules, shared-signal extensions, NFL context/materiality, six refresh phases, source restrictions, and inline contract scenarios | user-approved NBA and NFL adapter contract expansion; no provider evidence or activation claimed |
