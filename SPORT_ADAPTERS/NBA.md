# NBA Pregame Full-Game Sport Adapter

**Adapter ID:** `nba.pregame_full_game_v0_1`

**Version:** `0.1.0`

**Structural contract:** `adapter_contract_v1`

**Document status:** Active pre-activation documentation policy

**Sport:** Basketball

**League:** NBA

**Lifecycle:** All profiles `disabled_provider_validation`

**Last reviewed:** 2026-07-12

**Default timezone:** `America/Chicago`

**Run mode:** On-demand local decision brief after separate activation only
**Fair-probability method:** `nba_market_consensus_mean_v1`, specified but not runnable while profiles are disabled

This adapter specifies credential-free, pre-activation NBA promotion research. Promotion value is expected to create the opportunity. NBA context may verify eligibility, block stale or mismatched evidence, and trigger synchronized price refreshes; it never creates an ad hoc probability adjustment and this adapter does not predict NBA outcomes.

Apply this adapter with `PROJECT_CONTEXT.md`, `PROMO_ANALYSIS_PLAYBOOK.md`, `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md`, and `SPORT_ADAPTERS/README.md`. Those documents retain control of formulas, shared signals, reason codes, structured output, human approval, source access, and the AP Frankenstein boundary. Nothing in this document authorizes provider calls, polling, candidate generation, alerts, wagering, or downstream integration.

---

## 1. Adapter metadata

```yaml
adapter:
  adapter_id: nba.pregame_full_game_v0_1
  version: 0.1.0
  contract_version: adapter_contract_v1
  document_status: active pre-activation documentation policy
  sport: Basketball
  league: NBA
  default_timezone: America/Chicago
  last_reviewed: 2026-07-12
  review_owner: Advantage Play Intern
  run_mode: on_demand_local_brief_after_separate_activation
  probability_method: nba_market_consensus_mean_v1
  autonomous_wagering: false
  ap_frankenstein_integration: false
```

---

## 2. Profile registry

| profile_id | lifecycle | participant scope | period | allowed line shape | overtime treatment | probability method | activation blocker |
|---|---|---|---|---|---|---|---|
| `nba.full_game.moneyline` | `disabled_provider_validation` | team | full game | two-way moneyline whose tie and push outcomes are impossible | included and exactly matched across target and comparisons | `nba_market_consensus_mean_v1`, specified only | exact target/comparison coverage, source permission, tie/push/settlement identity, origin independence, cross-timing evidence, fixtures, and separate activation approval are incomplete |
| `nba.full_game.spread` | `disabled_provider_validation` | team | full game | principal reciprocal half-point spread only | included and exactly matched | `nba_market_consensus_mean_v1`, specified only | principal-line identity and complete two-origin coverage are not validated across required timing conditions |
| `nba.full_game.total` | `disabled_provider_validation` | event | full game | principal half-point over/under only | included and exactly matched | `nba_market_consensus_mean_v1`, specified only | principal-line identity and complete two-origin coverage are not validated across required timing conditions |
| `nba.player.points` | `disabled_provider_validation` | player | full game | exact non-push over/under or conditionally equivalent `N+ Points` outcome | included and exactly matched | `nba_market_consensus_mean_v1`, specified only | exact two-sided same-outcome coverage, participation/void/stat-counting settlement identity, cross-timing evidence, fixtures, and separate activation approval are incomplete |

No NBA profile is selectable for recommendation-grade candidate generation. Every structurally valid request still returns `BLOCKED` with `ADAPTER_PROFILE_DISABLED` until the exact profile receives separate activation approval and every governing document is synchronized.

The following adjacent markets are unavailable by catalog absence or identity mismatch: NBA player rebounds, assists, made threes, and all other player props; team totals; alternate spreads or totals; whole-number spreads, totals, or player-point over/unders; regulation-only markets; three-way or draw-option markets; quarters, halves, series, futures, awards, same-game parlays, and live markets. Provider exposure does not register or activate them.

---

## 3. Market identity and settlement contract

Every target and comparison quote must retain the complete identity below. Missing, unknown, or conflicting material fields fail closed and must not be inferred from a nearby market.

```yaml
market_identity:
  sportsbook_id: string
  jurisdiction: string
  league: NBA
  event_id: string
  provider_event_id: string
  home_team_id: string
  away_team_id: string
  participant_id: string | null
  provider_participant_id: string | null
  raw_market_label: string
  raw_selection_label: string
  canonical_market_key: nba.full_game.moneyline | nba.full_game.spread | nba.full_game.total | nba.player.points
  side: home | away | over | under
  line: number | null
  line_role: principal | alternate | not_applicable | unknown
  period: full_game
  overtime_treatment: included | excluded | unknown
  push_behavior: impossible | push | unknown
  participation_rule: string | not_applicable | unknown
  void_rule: string | unknown
  stat_counting_rule: string | not_applicable | unknown
  settlement_rule: string | unknown
  american_odds: integer
  decimal_odds: number
  market_status: open | suspended | closed | unknown
  retrieved_at_utc: datetime
  provider_last_update_utc: datetime | null
  source_id: string
  raw_snapshot_id: string
  ap_frankenstein_compatibility: unsupported
```

`line_role` must be proven from sportsbook-originated evidence or a reviewed provider field. A displayed half-point line is not presumed principal merely because it is the first line returned. Unknown or alternate status is `MARKET_IDENTITY_MISMATCH` for the game spread and total profiles.

### 3.1 Raw-to-canonical equivalence

| raw market shape | canonical profile/outcome | equivalence conditions | settlement conditions | AP compatibility | status |
|---|---|---|---|---|---|
| `Moneyline`, `Game Moneyline`, or `To Win` | `nba.full_game.moneyline` | exactly two named NBA teams in the same pregame event; no draw selection; full game | overtime included; tie and push proven impossible; void/cancellation rules match | `unsupported` | conditionally specified; profile disabled |
| principal `Spread` with reciprocal team handicaps at `x.5` | `nba.full_game.spread` | same event; exact reciprocal thresholds such as `-4.5` and `+4.5`; both sides open; line proven principal | full game; overtime included; push impossible; settlement/void rules match | `unsupported` | conditionally specified; profile disabled |
| principal `Total`, `Game Total`, or exact `Over/Under x.5` | `nba.full_game.total` | same event; exact threshold; complete over/under pair; line proven principal | full game; overtime included; push impossible; settlement/void rules match | `unsupported` | conditionally specified; profile disabled |
| player `Over/Under x.5 Points` | `nba.player.points` | exact player, event, full-game period, side, and half-point threshold | overtime, participation, void, stat-counting, push, and settlement rules match | `unsupported` | conditionally specified; profile disabled |
| player `N+ Points` or `N or More Points`, including `20+ Points` | same canonical outcome as `Over N-0.5 Points`, including `Over 19.5 Points` | exact player, event, period, overtime treatment, participation rule, void rule, stat-counting rule, and outcome boundary match; every raw label remains preserved | push impossible for the normalized outcome; settlement must award the same results for every possible official point total | `unsupported` | conditional outcome equivalence only; profile disabled; a one-sided milestone still cannot supply a comparison pair without an exact opposing outcome |
| player `Over N Points`, including `Over 20 Points` | none | not equivalent to `N+ Points` or `Over N-0.5` because an exact total of `N` can push | push-capable binary EV is unavailable | `unsupported` | `BLOCKED` with `PUSH_MODEL_UNAVAILABLE`; also record `MARKET_IDENTITY_MISMATCH` if an equivalence mapping was attempted |
| whole-number game spread or total | none | not an allowed non-push line shape | push probability is not modeled | `unsupported` | `BLOCKED` with `PUSH_MODEL_UNAVAILABLE` |
| regulation-only, three-way, draw-option, alternate, team-total, partial-game, SGP, or live shape | none | not equivalent to any registered profile | period, overtime, participant, line role, or settlement differs | `unsupported` | `BLOCKED` with `MARKET_IDENTITY_MISMATCH` or absent-profile lifecycle gate |

For `N+ Points`, equivalence is an outcome mapping, not permission to invent an opposing side. A comparison book counts only when that book itself provides the exact complementary outcome under matching rules, such as a proven equivalent to `Under N-0.5 Points`. Never pair a milestone price from one book with an opposing quote from another.

Raw market and selection labels are always retained. AP compatibility defaults to `unsupported` for every NBA shape. That label is descriptive only and creates no API, receipt, spreadsheet, settlement, or handoff integration with AP Frankenstein.

---

## 4. Probability and comparison policy

`nba_market_consensus_mean_v1` extends the global exact-market consensus gate without weakening it:

1. Exclude the target sportsbook from fair probability and from usable comparison coverage.
2. Require at least two usable non-target books assigned to two distinct resolved pricing-origin groups.
3. Require each included book to provide its own complete two-sided exact market. Never create a pair across books.
4. Match jurisdiction-appropriate event identity, participant, canonical outcome, threshold, principal-line role when applicable, period, overtime, tie, push, participation, void, stat-counting, and settlement rules.
5. De-vig each comparison book separately with the project's two-way proportional method.
6. Aggregate only the included source-level fair probabilities with an unweighted arithmetic mean, version `nba_market_consensus_mean_v1`.
7. Require target-quote age no greater than 180 seconds, comparison-quote age no greater than 300 seconds, and collection-time skew no greater than 300 seconds.
8. Report target exclusion, raw/usable/origin counts, each source-level pair and fair probability, the mean, dispersion, oldest comparison age, collection skew, pricing-origin groups, and every exclusion with an existing reason code.

A one-sided `N+ Points` ladder is non-de-viggable unless that same comparison book exposes an exact complementary outcome under identical settlement rules. A target-side milestone may still be shown with its boosted break-even probability after conditional identity normalization, but it never supplies its own fair probability.

If fewer than two fresh independent complete comparison markets remain, the structural state is `WATCH` during research and `BLOCKED` at the final check with `CONSENSUS_INSUFFICIENT`. If pricing-origin independence is unresolved, also use `PRICING_ORIGIN_UNRESOLVED`. Quotes outside the 300-second collection-skew limit fail with `QUOTE_BATCH_UNSYNCHRONIZED`. While profiles are disabled, no structurally valid batch proceeds to probability, EV, ranking, or actionable output; it returns `ADAPTER_PROFILE_DISABLED` first.

---

## 5. Source and compliance policy

| source_id/class | facts or markets supplied | authority rank | access method | jurisdiction coverage | timestamp behavior | terms/license reviewed | permitted use | current status |
|---|---|---:|---|---|---|---|---|---|
| [official NBA injury-report page](https://official.nba.com/nba-injury-report-2025-26-season/) | season-specific submission policy, report version, and player availability | 1 | manual/on-demand official page or permitted licensed feed | league-wide operational facts for the named season | retain publication/version time when available and local UTC retrieval | NBA Terms posture recorded 2026-07-12; page, season, deadlines, and access permission must be reverified | operational eligibility and price invalidation only | conditional manual/on-demand reference; no automated collection approved |
| [official NBA schedule](https://www.nba.com/schedule) | event identity, date, teams, venue, and scheduled tip | 1 | manual/on-demand official page or permitted licensed feed | league-wide event facts | retain event time and local UTC retrieval | access and exact use must be reverified under current NBA Terms | operational event identity only | conditional manual/on-demand reference |
| official NBA/team roster, transaction, and announcement source | roster identity, transaction, availability, and confirmed role changes | 1-2 | permitted public announcement or licensed feed | named league/team/event | publication/effective and local UTC retrieval times required | exact source/platform terms must be reviewed | operational identity, eligibility, and price invalidation | conditional; source-specific review required |
| licensed/documented sports-data provider | schedule, event status, roster, official-report, availability, or confirmed role facts | 2 | documented API/feed | contract-defined | provider and local UTC timestamps retained | exact contract and gambling-related use must be reviewed; no provider is approved generically | operational facts within reviewed license | provider-specific validation required |
| sportsbook-originated target evidence | promotion terms and exact target quote | 1 for the displayed target | timestamped user screenshot/structured manual verification or permitted documented feed | exact displayed book and jurisdiction only | local UTC capture required; provider time retained if present | manual evidence is the credential-free fallback; any feed needs documented permission | target identity and promotion evidence | no source certified by this document |
| licensed/documented multi-book odds provider | exact target or comparison markets | 1-2 for quoted markets | documented API/feed | contract-defined books and jurisdictions | provider and local UTC timestamps retained | exact contract, book coverage, and pricing-origin relationships must be reviewed | exact market evidence within reviewed license | provider-specific validation required |
| sportsbook-originated comparison evidence | one exact comparison book | 2 | timestamped screenshot/structured manual verification or permitted documented feed | exact displayed book and jurisdiction | local UTC capture required | automated access requires documented permission | one complete exact comparison pair | conditional credential-free fallback |
| established secondary report | possible registered material-change lead | 4 | manual/on-demand public report | named player/team/event only | publication and retrieval times required | exact source terms unverified for systematic collection | may create `WATCH` pending authoritative confirmation | never recommendation-grade alone |

The [NBA Terms of Use](https://www.nba.com/termsofuse) currently restrict using the site's defined NBA Statistics in connection with gambling activity. Therefore NBA.com, stats.nba.com, or other NBA-owned statistical fields must not be collected, stored as gambling-model inputs, scored, narrated as candidate support, or used to change probability or ranking in this workflow. A future Tier D model requires a separately licensed/permitted statistical source and documented legal/license review.

Official schedule, injury-report, roster, transaction, and team-announcement facts are operational identity and availability references only. Use them manually/on demand unless the exact source or licensed feed explicitly permits systematic retrieval for this use. Do not scrape, reproduce, or republish source content beyond source-referenced local evidence allowed by applicable terms.

Injury-report deadlines are season-specific configuration, never permanent adapter constants. Before any run could clear the structural injury gate, record and reverify `nba_injury_deadlines_[season]_v1` from the official season page, including the applicable deadline logic, report/version identity, effective date, source URL, and review timestamp. The linked 2025-26 page is a current reference named by this version, not authority for a later season.

Do not automate authenticated sportsbook pages, spoof location, bypass geolocation, authentication, anti-bot controls, or rate limits, or treat undocumented endpoints as approved sources. Any unresolved permission, jurisdiction, provenance, timestamp, schema, or pricing-origin question fails closed.

---

## 6. Active signal registry

There are no active NBA profiles. This section is the complete pre-activation Tier A/C contract required for validation. Its presence does not authorize polling or candidate generation.

The shared `promo_terms`, `target_quote`, `comparison_quotes_same_line`, `market_status`, and `promo_expiration` signals inherit their only authoritative ten-field definitions from Section 5 of `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md`. The extensions below add NBA constraints and do not create duplicate signal IDs or collection paths.

### 6.1 Inherited shared-signal extensions

| shared_signal_id | profiles | NBA-specific extension | maximum-age override | reporting extension |
|---|---|---|---|---|
| `promo_terms` | all NBA profiles | verify event/market/odds eligibility, token count, cap, expiry, period, overtime, tie, push, participation, void, stat-counting, settlement, cancellation, and token-return rules | inherit; reverify at final check | show every material term, confidence, and unresolved ambiguity |
| `target_quote` | all NBA profiles | require exact target book/jurisdiction, raw market/selection, event, participant, side, threshold, line role, period, overtime, tie, push, settlement, status, and timestamp | inherit 180 seconds | show raw/canonical outcome, principal-line evidence, status, age, jurisdiction, and `unsupported` AP compatibility |
| `comparison_quotes_same_line` | all NBA profiles | require two complete exact pairs from distinct resolved non-target origins and apply `nba_market_consensus_mean_v1`; milestone equivalence must satisfy Section 3.1 | inherit 300 seconds and 300-second skew | show target exclusion, source pairs/probabilities, origin audit, mean, dispersion, ages/skew, and exclusions |
| `market_status` | all NBA profiles | post-material-change evidence must show open status and synchronization for target and every included comparison | inherit | show non-open state, change time, and synchronization result |
| `promo_expiration` | all NBA profiles | no additional collection path | inherit | show time remaining |

### 6.2 NBA-specific signal registry

Each row contains the required ten fields. Every row remains dormant while its consuming profile is `disabled_provider_validation`.

| signal_id | market_profile | tier | source_hierarchy | refresh_trigger | maximum_age | material_change_rule | candidate_state_effect | probability_use | reporting_rule |
|---|---|---|---|---|---|---|---|---|---|
| `nba_event_identity_status` | all NBA profiles | A/C | official NBA schedule/game source; licensed provider | intake, T-6h, T-30m, final check, and event change | 600 seconds inside T-2h; identity event-scoped | opponent, venue, tip time, event ID, scheduled/delayed/postponed/canceled status, or neutral-site state changes | identity conflict/cancellation `BLOCKED`; resolvable change `WATCH` and synchronized refetch | none | always show identity; emphasize conflicts, changes, and blockers |
| `nba_injury_submission_state` | all NBA profiles | A/C | season-current official NBA injury report; licensed official-report feed | intake, applicable configured deadline, report update, T-2h through final check | current report version; retrieval no older than 600 seconds inside T-2h; must postdate latest update | report becomes due/submitted/revised/missing; team row, player row, or report version changes | not due or incomplete `WATCH`; missing required final report `BLOCKED`; newer revision `WATCH` and refetch | none | show season/deadline config version, due state, report version, publication, and retrieval time |
| `nba_team_availability_delta` | all NBA profiles | C | official NBA injury report; official team confirmation; licensed provider | every official report revision and candidate-relevant confirmation | same current-report rule as submission signal | player added/removed or official participation designation/reason changes after any affected quote | `WATCH` and synchronized target/comparison refetch; no direct rank change | none | report exact old/new official state and timestamps for affected teams only |
| `nba_starting_five_role_event` | all NBA profiles | C | official team announcement; licensed confirmed-lineup feed; projections only as unconfirmed leads | T-90m, confirmed publication, and role change | latest confirmed event; retrieval no older than 600 seconds when used near tip | confirmed starter added/removed or concrete starting/bench role change after quotes | confirmed change `WATCH` and refetch; lack of league-wide confirmed five alone does not block game-line profiles | none | change-only for game lines; for points, show target-player role dependency; never label a projection confirmed |
| `nba_roster_transaction_eligibility` | all NBA profiles | A/C | official league/team roster or transaction source; licensed provider | intake, T-6h, T-2h, final check, and confirmed transaction | no older than 3600 seconds distant or 600 seconds inside T-2h | membership, signing, waiver, release, trade, suspension, assignment, or eligibility state changes after quotes | identity conflict `BLOCKED`; clear promotion violation `INELIGIBLE`; otherwise `WATCH` and refetch | none | report candidate-relevant transaction, effective/publication time, and source only |
| `nba_target_player_status` | `nba.player.points` | A/C | official NBA injury report; official inactive/team status; licensed provider | applicable report deadline, every revision, confirmed active/inactive change, T-30m, and final check | current report/player state; retrieval no older than 600 seconds inside T-2h | target changes among available, probable, questionable, doubtful, out, inactive, suspended, or participation status | questionable/doubtful `WATCH`; out/inactive/suspended `INELIGIBLE` when exact terms decide treatment and otherwise `BLOCKED`; available/probable clears only after rule verification and post-change sync | none | always show exact official target-player status, participation/void rule, and timestamps |
| `nba_post_change_price_sync` | all NBA profiles | A/C | registered material-fact timestamps plus shared target/comparison/market-status evidence | immediately after every registered material change and at final check | target no older than 180 seconds; comparisons no older than 300 seconds; skew no greater than 300 seconds; every affected quote newer than the material fact | any included quote predates the newest material fact, is non-open, exceeds age/skew, or lacks exact identity | remain `WATCH`; unavailable or invalid final batch `BLOCKED`; a valid batch clears only the synchronization blocker | none; refreshed shared Tier B quotes own valuation | always show newest material-fact time, quote times, open status, ages/skew, and `post_material_change_synchronized` |

---

## 7. Materiality and state rules

| rule_id | profiles | source fields / qualifying change | effective-time rule | state effect | required refetch | resolution rule | probability effect |
|---|---|---|---|---|---|---|---|
| `nba_event_state_materiality_v1` | all NBA profiles | event ID, opponents, venue, tip, neutral site, delay, postponement, cancellation, or status | any authoritative change newer than an affected quote invalidates that quote | identity conflict/cancellation `BLOCKED`; resolvable change `WATCH` | shared target, comparison, and market-status signals | current event state plus synchronized post-change batch | none |
| `nba_injury_submission_materiality_v1` | all NBA profiles | configured report deadline; report due, submitted, missing, or revised; team/player row or version changes | compare season-specific deadline and report publication/version with every affected quote | not due/missing during research `WATCH`; required final report missing `BLOCKED`; newer revision `WATCH` | shared target and complete comparison signals | verified season config, current report/version, and synchronized post-change batch | none |
| `nba_availability_role_materiality_v1` | all NBA profiles | player added/removed; official availability designation; confirmed starting/bench role changes | any confirmed affected-team change newer than quotes invalidates them | `WATCH`; exact player ineligibility may become `INELIGIBLE` or `BLOCKED` under terms | shared target and complete comparison signals | current official fact plus synchronized post-change batch | none |
| `nba_roster_transaction_materiality_v1` | all NBA profiles | membership, signing, waiver, release, trade, suspension, assignment, or eligibility | official effective/publication time compared with quote retrieval | identity conflict `BLOCKED`; clear promo violation `INELIGIBLE`; otherwise `WATCH` | shared target and complete comparison signals | resolved identity/eligibility plus synchronized post-change batch | none |
| `nba_player_status_materiality_v1` | `nba.player.points` | target official status, active/inactive state, participation eligibility, or verified role changes | any qualifying target-player fact newer than a quote invalidates it | questionable/doubtful `WATCH`; out/inactive/suspended `INELIGIBLE` or `BLOCKED` under exact terms | shared target and complete comparison signals | current target status, verified participation/void rules, and synchronized post-change batch | none |
| `nba_post_change_price_sync_v1` | all NBA profiles | newest registered material-fact timestamp; target/comparison retrieval times; open status; age and skew | every affected included quote must postdate the fact and satisfy 180/300/300 limits | unsynchronized `WATCH`; invalid or unavailable final batch `BLOCKED`; valid batch removes only the context-sync blocker | shared target, comparison, and market-status signals | exact open post-change target plus two independent complete comparisons and valid audit | none |

### 7.1 State-resolution rules

- A profile lifecycle check occurs before candidate generation. Because every NBA profile is disabled, a structurally valid request returns `BLOCKED` with `ADAPTER_PROFILE_DISABLED` and produces no probability, EV, ranking, or actionable candidate.
- Before the applicable season-configured injury-report deadline, the report state is `not_due`; the structural context state is `WATCH` with `OFFICIAL_REPORT_NOT_DUE`. It cannot clear a final pre-use gate.
- After the applicable deadline, a missing required report or team/player row is `WATCH` during research and `BLOCKED` at final check with `OFFICIAL_REPORT_MISSING`.
- A current official report plus a synchronized post-change market batch can clear the structural availability blocker; it does not override disabled lifecycle.
- Missing league-wide starting-five confirmation alone does not block a game moneyline, spread, or total when official availability and synchronized prices are current. A confirmed role change newer than prices always invalidates the affected batch.
- For `nba.player.points`, a questionable or doubtful target remains structurally `WATCH`. An out, inactive, or suspended target is `INELIGIBLE` only when the exact promotion/book treatment is proven and otherwise `BLOCKED`.
- Any registered event, injury, availability, roster, role, or player-status fact newer than an affected quote produces `WATCH` with `MATERIAL_CONTEXT_NEWER_THAN_QUOTES` and requires a synchronized target/comparison refetch. Unavailable final evidence becomes `BLOCKED`.
- Missing, stale, conflicting, unidentified, wrong-jurisdiction, or non-open target evidence is `BLOCKED`. Comparison defects exclude the source and produce `WATCH`/`BLOCKED` if coverage falls below two independent complete markets.
- Context never adds or subtracts probability or ranking points. After synchronization, only refreshed Tier B prices could change valuation in a future activated profile.

Every structural fixture and future brief must retain:

```yaml
monitoring_metadata:
  next_refresh_at: datetime | null
  next_refresh_reason: string | null
  post_material_change_synchronized: false
```

These remain local `promotion_decision_brief_v2` audit fields and do not change a persisted schema.

---

## 8. Refresh policy

This cadence specifies what a future on-demand run or human-requested refresh would need. It does not install a scheduler, background poller, automatic alert, closing-line job, or settlement job.

| phase_id | NBA window or trigger | facts refreshed | maximum ages | structural state if unavailable | next refresh reason |
|---|---|---|---|---|---|
| `intake` | promotion intake | each token's terms, eligible slate, event identity, season/deadline configuration, initial injury/report state, target, complete comparisons, and source/jurisdiction metadata | source/event scoped; quote limits apply | material term or target missing `BLOCKED`; report/consensus incomplete `WATCH`; lifecycle remains `BLOCKED` | applicable report deadline, provider refresh, or registered material fact |
| `distant_pregame` | around T-6h | event/tip, roster/transaction, official availability, target, and comparison batches | roster no older than 3600 seconds; target 180, comparisons 300, skew 300 seconds | `WATCH` when a required current fact or valid consensus is unavailable; lifecycle remains `BLOCKED` | T-2h official-report window or source event |
| `official_release_window` | applicable season-configured injury deadline through final check, including T-2h | submission/version, changed team/player rows, target status, roster, and confirmed role events at the next permitted on-demand check | current report; no older than 600 seconds inside T-2h | not due/missing `WATCH`; unresolved final report/status requirement `BLOCKED` | next report revision/check or confirmed change |
| `material_change` | any registered event, injury, availability, roster, role, or player-status change | invalidate quotes; refresh target, complete comparisons, market status, affected facts, and synchronization audit | target 180 seconds; comparisons 300 seconds; skew 300 seconds; all affected quotes postdate change | `WATCH`; unavailable/invalid final synchronized batch `BLOCKED` | synchronized post-change price batch |
| `shortlist_check` | around T-30m | profile identity, event, current report/availability, target-player status when applicable, confirmed role event if published, target, comparisons, and consensus audit | registry ages plus 180/300/300 quote limits | `WATCH` or `BLOCKED` according to structural failure; lifecycle always `BLOCKED` | final synchronized check |
| `final_sync` | immediately before hypothetical human review after activation | promotion, profile lifecycle, event, availability, roster/role/player status, target, comparisons, jurisdiction, identity/settlement, synchronization, and QA | every final recommendation-grade limit | any fatal, stale, conflicting, unsynchronized, or disabled input `BLOCKED` | none; new evidence requires a new run |

No cadence may be relaxed to make a disabled profile runnable or to manufacture a qualifying result.

---

## 9. Tier D model-only registry

Every group below is `disabled_model_only`. The groups are hypotheses, not active signals, and may not be routinely fetched, stored, scored, narrated, used for probability, or used to change state or rank.

| group_id | potential profile consumers | candidate inputs | required source permission | named model consumer | activation evidence | anti-noise boundary | lifecycle |
|---|---|---|---|---|---|---|---|
| `nba_model_minutes_rotation` | `nba.player.points`; future team markets only if separately registered | projected minutes, substitution distribution, starting/bench role, rotation depth | separately licensed/permitted non-NBA-statistics source | none | exact consumer, transformations, leak-free history, out-of-sample calibration, uncertainty, and monitoring | no projection from one recent game, speculative lineup, or generic coach quote | `disabled_model_only` |
| `nba_model_scoring_opportunity` | `nba.player.points` | usage, field-goal/free-throw attempts, touches, shot-location opportunity, expected minutes | separately licensed/permitted non-NBA-statistics source | none | same full activation evidence | no raw recent average, last-N overs, or hot/cold scoring narrative | `disabled_model_only` |
| `nba_model_pace_efficiency` | game spreads/totals and points | calibrated possession and offensive/defensive efficiency projections | separately licensed/permitted non-NBA-statistics source | none | same full activation evidence | no standalone rankings or pace narrative | `disabled_model_only` |
| `nba_model_lineup_redistribution` | all registered NBA profiles | shrunk personnel-aware on/off and role redistribution | separately licensed/permitted non-NBA-statistics source | none | same full activation evidence | exclude tiny lineup samples and double-counting after market refresh | `disabled_model_only` |
| `nba_model_matchup_shot_profile` | `nba.player.points` and future totals | calibrated opponent scheme, shot-location, foul, and transition opportunity | separately licensed/permitted non-NBA-statistics source | none | same full activation evidence | no defense-vs-position rank or one-matchup narrative | `disabled_model_only` |
| `nba_model_participation_tail` | all registered NBA profiles | rest, travel, workload, foul, blowout, overtime, and minutes-tail distributions | separately licensed/permitted non-NBA-statistics source | none | same full activation evidence | no manual penalty from fatigue, travel, foul, blowout, or overtime stories | `disabled_model_only` |

NBA.com and stats.nba.com statistics are explicitly unavailable to these model families under the current terms posture. Provider availability or intuitive relevance does not prove source permission, predictive value, or activation.

---

## 10. Tier X exclusions

| excluded signal or narrative | reason excluded | permitted operational use, if any |
|---|---|---|
| hot/cold streaks, last-five/ten results, recent overs, or raw recent averages | no enabled calibrated consumer | none |
| head-to-head, revenge, must-win, birthday, milestone, national-TV, home/away, day, ATS, or venue narratives | narrative or unstable association | none |
| public betting percentages, social sentiment, or unsupported sharp-money claims | unresolved provenance and no probability contract | none |
| defense-vs-position rankings and tiny lineup/on-off/opponent/role samples | disabled or inadequately validated model proxies | none |
| generic confidence quotes, unverified injury/lineup/trade/suspension/rest rumors, or referee trends | insufficient authority or validated consumer | a plausible registered material-change lead may create `WATCH` pending approved-source confirmation |
| foul, blowout, travel, rest, fatigue, or overtime speculation | participation-tail model remains disabled | none |
| NBA-owned statistical fields | excluded from gambling-related model use under current NBA Terms posture | operational non-statistical official facts remain subject to Section 5 |
| LLM-authored probability or ranking adjustment | violates deterministic valuation boundary | none |

Tier X material never supplies probability, rank, positive-EV language, or persuasive candidate support. A lower-authority report may create `WATCH` only when it plausibly identifies a registered material change; it must be confirmed or rejected by an approved source.

---

## 11. Provider-validation evidence requirements

No provider or sportsbook is certified by this document. Evidence must be credential-free or captured under a separately reviewed permitted source path, and it must not claim real promotion or provider coverage from synthetic fixtures.

### 11.1 Evidence matrix

| evidence_id | profile scope | target/comparison role | timing conditions required | exact fields required | current evidence state | certification effect |
|---|---|---|---|---|---|---|
| `nba_game_line_target_cross_timing` | moneyline, spread, and total | target | board open/distant pregame, after a registered material change, and near tip | jurisdiction, event, teams, raw/canonical market, side, principal line when applicable, period, overtime, tie, push, void, settlement, price, status, and timestamps | not satisfied | none; profiles remain disabled |
| `nba_game_line_comparison_origins` | moneyline, spread, and total | comparison | same three timing conditions | two independent non-target complete exact markets, pricing origins, target exclusion, per-book de-vig inputs, age, status, and skew | not satisfied | none; profiles remain disabled |
| `nba_player_points_target_cross_timing` | player points | target | board open, after availability/role/player-status change, and near tip | player/event identity, raw outcome, half-point or conditionally equivalent milestone, participation, void, stat-counting, overtime, push, settlement, price, status, and timestamps | not satisfied | none; profile remains disabled |
| `nba_player_points_comparison_origins` | player points | comparison | same three timing conditions | two independent complete exact pairs at the canonical outcome, including equivalence and complementary-outcome proof | not satisfied | none; profile remains disabled |
| `nba_operational_source_permission` | all profiles | context | season review and before any activation | official-report URL/deadline version, permitted access mode, source timestamps, operational/statistics boundary, and license record | not satisfied | none |

For every proposed target or comparison source, retain local UTC request/capture start and end, provider timestamp when present, provider object IDs, raw snapshot or content hash, user-visible agreement where available, exact jurisdiction, pricing-origin mapping, exclusions, schema discrepancies, and resolution. A price difference is acceptable only when timestamps demonstrate an explainable market move rather than identity failure.

Recommendation-grade promotion would additionally require:

- exact agreement across every identity and settlement field at all required timing conditions;
- two usable non-target books from two resolved pricing origins, each with its own complete exact market;
- target exclusion, per-book de-vigging, `nba_market_consensus_mean_v1`, 180/300/300 age/skew enforcement, and complete consensus audit;
- missing, stale, suspended, closed, one-sided, duplicate, mismatched, unknown, and provider-regression evidence;
- season-current injury-report deadline/version validation and candidate-relevant availability/roster/role/player-status evidence;
- deterministic calculation tests for each exact non-push shape and milestone equivalence; and
- separate explicit lifecycle approval synchronized across all governing documents.

Synthetic fixtures below prove only expected documentation behavior. They do not prove source access, provider coverage, sportsbook agreement, pricing-origin independence, or promotion readiness.

---

## 12. Inline credential-free fixtures and expected outcomes

The repository has no executable adapter schema or test runner, so these fixtures remain inline documentation tables. Do not invent machine-readable fixture files for this milestone.

The `structural expectation` column describes the gate outcome that a future implementation must reproduce before lifecycle enforcement. The `current required outcome` column is controlling now: the selected NBA profile is disabled, no recommendation-grade candidate is created, and `ADAPTER_PROFILE_DISABLED` is always retained. Invalid fixtures also retain their specific structural reason codes.

### 12.1 Identity, normalization, and lifecycle fixtures

| fixture_id | credential-free input condition | structural expectation | current required outcome / audit evidence |
|---|---|---|---|
| `nba_valid_moneyline_disabled` | exact two-team full-game moneyline; overtime included; tie/push impossible; target and two independent exact pairs otherwise current | identity and consensus gates would pass after activation | `BLOCKED` with `ADAPTER_PROFILE_DISABLED`; no probability, EV, ranking, or candidate generation |
| `nba_valid_principal_spread_disabled` | proven principal reciprocal `-4.5/+4.5` full-game spread with exact settlement and valid price batch | non-push spread identity would pass after activation | `BLOCKED` with `ADAPTER_PROFILE_DISABLED`; preserve principal-line evidence |
| `nba_valid_principal_total_disabled` | proven principal full-game `Over/Under 223.5` with exact settlement and valid price batch | non-push total identity would pass after activation | `BLOCKED` with `ADAPTER_PROFILE_DISABLED` |
| `nba_points_half_point_disabled` | exact player `Over/Under 19.5 Points`; full game with matching overtime, participation, void, stat-counting, and settlement rules | points identity would pass after activation | `BLOCKED` with `ADAPTER_PROFILE_DISABLED`; raw labels preserved |
| `nba_points_20_plus_equivalent` | target raw label `20+ Points`; exact player/event/period; same overtime, participation, void, stat-counting, and settlement as `Over 19.5 Points` | normalize the outcome to `over 19.5` while preserving `20+ Points`; push impossible; a one-sided target does not itself count as a comparison pair | `BLOCKED` with `ADAPTER_PROFILE_DISABLED`; equivalence audit lists every matched rule and both raw/canonical labels |
| `nba_points_20_plus_rule_mismatch` | `20+ Points` differs from `Over 19.5` on participation, void, stat-counting, overtime, or settlement | reject equivalence | `BLOCKED` with `MARKET_IDENTITY_MISMATCH`, `SETTLEMENT_RULE_MISMATCH`, and `ADAPTER_PROFILE_DISABLED` as applicable |
| `nba_points_over_20_push` | raw selection `Over 20 Points` | not equivalent to `20+` or `Over 19.5`; exact 20 can push | `BLOCKED` with `PUSH_MODEL_UNAVAILABLE` and `ADAPTER_PROFILE_DISABLED`; raw label preserved |
| `nba_whole_number_game_line` | principal or alternate spread/total has a whole-number threshold | push-capable shape rejected | `BLOCKED` with `PUSH_MODEL_UNAVAILABLE` and `ADAPTER_PROFILE_DISABLED` |
| `nba_alternate_not_principal` | spread or total is half-point but proven alternate or principal status is unknown | registered principal-line identity fails | `BLOCKED` with `MARKET_IDENTITY_MISMATCH` and `ADAPTER_PROFILE_DISABLED` |
| `nba_regulation_or_three_way` | regulation-only, three-way, or draw-option moneyline | period/tie/settlement identity fails | `BLOCKED` with `MARKET_IDENTITY_MISMATCH` or `SETTLEMENT_RULE_MISMATCH`, plus `ADAPTER_PROFILE_DISABLED` |
| `nba_absent_prop_profile` | rebounds, assists, made threes, or any unregistered NBA prop requested | no catalog profile exists | `BLOCKED` with `ADAPTER_PROFILE_DISABLED`; do not map it to points |

### 12.2 Consensus, freshness, status, and source fixtures

| fixture_id | credential-free input condition | structural expectation | current required outcome / audit evidence |
|---|---|---|---|
| `nba_target_excluded_two_origins` | target book also exposes both sides; two other complete comparison books come from two resolved independent origins | exclude target entirely; de-vig each non-target book separately; mean only source-level probabilities | `BLOCKED` with `ADAPTER_PROFILE_DISABLED`; audit target exclusion, raw/usable/origin counts, pairs, mean, and dispersion |
| `nba_only_one_comparison_origin` | exact target plus only one usable non-target complete market | consensus invalid; break-even only; structural `WATCH` then final `BLOCKED` | `BLOCKED` with `CONSENSUS_INSUFFICIENT` and `ADAPTER_PROFILE_DISABLED` |
| `nba_duplicate_or_unresolved_origin` | two records are one underlying origin or independence is unresolved | count known duplicate once; exclude unresolved origin | `BLOCKED` with `PRICING_ORIGIN_UNRESOLVED`, `CONSENSUS_INSUFFICIENT` when coverage falls below two, and `ADAPTER_PROFILE_DISABLED` |
| `nba_one_sided_comparison` | a comparison book provides candidate side or `N+ Points` but no exact complementary outcome | exclude as non-de-viggable; never combine across books | `BLOCKED` with `CONSENSUS_INSUFFICIENT` and `ADAPTER_PROFILE_DISABLED` |
| `nba_stale_target` | target quote age exceeds 180 seconds | target unusable | `BLOCKED` with `TARGET_QUOTE_STALE` and `ADAPTER_PROFILE_DISABLED` |
| `nba_stale_or_suspended_comparison` | a comparison exceeds 300 seconds or is suspended/closed | exclude source; downgrade when fewer than two origins remain | `BLOCKED` with `COMPARISON_QUOTE_STALE` or `MARKET_SUSPENDED`, `CONSENSUS_INSUFFICIENT` when applicable, and `ADAPTER_PROFILE_DISABLED` |
| `nba_collection_skew` | included quote timestamps span more than 300 seconds | batch invalid | `BLOCKED` with `QUOTE_BATCH_UNSYNCHRONIZED` and `ADAPTER_PROFILE_DISABLED` |
| `nba_jurisdiction_mismatch` | target evidence is not proven for the promotion's sportsbook jurisdiction | target cannot be substituted | `BLOCKED` with `JURISDICTION_MISMATCH` and `ADAPTER_PROFILE_DISABLED` |
| `nba_settlement_mismatch` | target or comparison differs on period, overtime, tie, push, participation, void, stat-counting, or settlement | exclude mismatched evidence and reject equivalence | `BLOCKED` with `SETTLEMENT_RULE_MISMATCH`, plus `CONSENSUS_INSUFFICIENT` if coverage fails and `ADAPTER_PROFILE_DISABLED` |

### 12.3 Injury, availability, roster, role, player-status, and synchronization fixtures

| fixture_id | credential-free input condition | structural expectation | current required outcome / audit evidence |
|---|---|---|---|
| `nba_report_not_due` | season-current deadline configuration proves the applicable report is not yet due | structural `WATCH`; final availability gate cannot clear | `BLOCKED` lifecycle with `OFFICIAL_REPORT_NOT_DUE` and `ADAPTER_PROFILE_DISABLED`; record next deadline/check |
| `nba_report_overdue_missing` | applicable deadline passed and required report/team row is missing | structural `WATCH`, becoming final `BLOCKED` | `BLOCKED` with `OFFICIAL_REPORT_MISSING` and `ADAPTER_PROFILE_DISABLED` |
| `nba_availability_newer_than_quotes` | official report revision or team availability change postdates any affected quote | invalidate batch; structural `WATCH`; synchronized refetch; no direct probability adjustment | `BLOCKED` lifecycle with `MATERIAL_CONTEXT_NEWER_THAN_QUOTES` and `ADAPTER_PROFILE_DISABLED`; show old/new timestamps |
| `nba_roster_or_role_newer_than_quotes` | official roster/transaction or confirmed starting-role change postdates prices | invalidate affected batch and refetch; no narrative adjustment | `BLOCKED` lifecycle with `MATERIAL_CONTEXT_NEWER_THAN_QUOTES` and `ADAPTER_PROFILE_DISABLED` |
| `nba_points_target_questionable` | points target is officially questionable or doubtful | structural `WATCH`; cannot clear player-status gate | `BLOCKED` lifecycle with `ADAPTER_PROFILE_DISABLED`; retain exact official status and next refresh |
| `nba_points_target_out` | points target becomes out/inactive/suspended | structural `INELIGIBLE` when exact terms prove treatment, otherwise `BLOCKED` | no candidate generation; retain `ADAPTER_PROFILE_DISABLED` plus exact status and promotion/book rule |
| `nba_starting_five_unconfirmed_game_line` | league-wide starting five is unconfirmed, but official availability report and synchronized full-game line batch are current | do not block the game line solely for missing starting five | still `BLOCKED` with `ADAPTER_PROFILE_DISABLED`; show that no separate lineup blocker was added |
| `nba_post_change_sync_missing` | material fact is current but one or more affected quotes predate it or final market is suspended | structural `WATCH`, final `BLOCKED` | `BLOCKED` with `MATERIAL_CONTEXT_NEWER_THAN_QUOTES` or `MARKET_SUSPENDED` and `ADAPTER_PROFILE_DISABLED`; `post_material_change_synchronized: false` |
| `nba_post_change_sync_valid_disabled` | official material fact is followed by open target and two independent complete comparison markets within 180/300/300 limits | clear only the structural context-sync blocker and value from refreshed Tier B prices after activation | `BLOCKED` with `ADAPTER_PROFILE_DISABLED`; `post_material_change_synchronized: true`; no EV or ranking runs |
| `nba_tier_d_or_x_supplied` | NBA-owned statistic, recent streak, matchup rank, rest story, or LLM adjustment is supplied | ignore as Tier D/X; no probability, state, or rank effect | profile remains `BLOCKED` with `ADAPTER_PROFILE_DISABLED`; audit that excluded material was not consumed |

---

## 13. Reusable on-demand run contract

This prompt is a future validation contract, not current run authorization:

```text
Validate the supplied NBA promotion evidence against NBA adapter nba.pregame_full_game_v0_1 version 0.1.0 and adapter_contract_v1.

Parse every token separately and verify the exact target sportsbook and jurisdiction, eligible event and profile, boost type, percentage, cap, odds range, expiry, period, overtime, tie, push, participation, void, stat-counting, settlement, cancellation, and token-return terms. Preserve raw labels. For player points, normalize N+ Points to Over N-0.5 only when player, event, period, overtime, participation, void, stat-counting, and settlement rules all match. Never equate Over N with N+ because the whole-number over can push.

Validate only the registered full-game moneyline, principal reciprocal half-point spread, principal half-point total, and exact non-push player-points shapes. Use current target evidence and at least two fresh complete exact opposing markets from independent non-target pricing origins. Exclude the target, de-vig each comparison book separately, and apply nba_market_consensus_mean_v1 with target/comparison/skew limits of 180/300/300 seconds. Never manufacture an opposing side or treat an alternate as principal.

Validate the current event, season-specific official injury-report submission/version, affected-team availability, roster/transaction identity, confirmed role events, target-player status for points, and post-change price synchronization. Any registered material fact newer than prices invalidates the batch and requires synchronized target/comparison refreshes. Never change probability directly for context and never consume disabled Tier D/X or NBA-owned statistics.

Every profile is disabled_provider_validation. Return BLOCKED with ADAPTER_PROFILE_DISABLED for every otherwise structurally valid scenario, produce no recommendation-grade candidate, probability, EV, allocation, ranking, or actionable state, and name every additional structural blocker. Return only a credential-free promotion_decision_brief_v2 validation snapshot with adapter/profile/version, raw/canonical identity, sources, timestamps, target exclusion, pricing-origin audit, settlement checks, ages/skew, post-change synchronization, exclusions, next refresh condition, and the human-decision boundary.

Never call a provider, schedule polling, create an alert, place or confirm a wager, or call or write to AP Frankenstein.
```

---

## 14. Activation checklist and change log

Before any NBA profile lifecycle change, all adapter-template checklist items must pass, recorded cross-timing evidence and credential-free fixtures must exist, source permissions and pricing-origin independence must be resolved, deterministic behavior must be tested, and separate explicit approval must be reflected consistently in the adapter catalog, monitoring playbook, `AGENTS.md`, and project `README.md`. Specification completeness alone is not activation evidence.

| date | adapter version | profiles affected | change | evidence/approval reference |
|---|---|---|---|---|
| 2026-07-12 | `0.1.0` | `nba.full_game.moneyline`, `nba.full_game.spread`, `nba.full_game.total`, `nba.player.points` | Created `adapter_contract_v1` pre-activation NBA contract with exact non-push identities, conditional milestone normalization, source/compliance boundaries, dormant signals, refresh phases, and inline credential-free fixtures; activated no profile | user-approved NBA and NFL adapter contract expansion plan; provider validation and activation remain unsatisfied |
