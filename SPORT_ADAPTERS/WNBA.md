# WNBA Boost-Analysis Sport Adapter

<!-- adapter-section: 1 adapter_metadata -->
## 1. Adapter metadata

**Adapter ID:** `wnba.pregame_full_game_v0_1`  
**Version:** `0.2.1`
**Structural contract:** `adapter_contract_v1`  
**Document status:** Active experimental-pilot policy  
**Sport:** Basketball  
**League:** WNBA  
**Lifecycle:** Mixed; assigned per market profile  
**Last reviewed:** 2026-07-13
**Default timezone:** `America/Chicago`  
**Run mode:** On-demand local decision brief  
**Fair-probability method:** De-vigged, exact-market consensus from independent non-target pricing origins  

This adapter supports supervised placement research for WNBA promotion tokens. Promotion value is expected to create most of the opportunity. WNBA context protects the analysis from stale prices, incorrect identity, unavailable participants, and changed game conditions; it never creates an ad hoc probability adjustment.

This adapter must be applied with `PROJECT_CONTEXT.md`, `PROMO_ANALYSIS_PLAYBOOK.md`, `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md`, and `SPORT_ADAPTERS/README.md`. Global formulas, consensus gates, report contracts, human approval, source-access rules, and the AP Frankenstein boundary remain controlling.

---

<!-- adapter-section: 2 profile_registry -->
## 2. Profile registry

| profile_id | lifecycle | participant | period | allowed line shape | overtime treatment | probability method | current boundary |
|---|---|---|---|---|---|---|---|
| `wnba.full_game.moneyline` | `pilot_enabled` | team | full game | two-way moneyline | must exactly match across target and comparisons | `wnba_market_consensus_mean_v1` | pregame only |
| `wnba.full_game.spread` | `pilot_enabled` | team | full game | reciprocal half-point spread only | must exactly match across target and comparisons | `wnba_market_consensus_mean_v1` | pregame only; no push probability |
| `wnba.full_game.total` | `pilot_enabled` | event | full game | half-point over/under only | must exactly match across target and comparisons | `wnba_market_consensus_mean_v1` | pregame only; no push probability |
| `wnba.player.points` | `disabled_provider_validation` | player | full game | exact half-point over/under | must exactly match | none while disabled | two fresh independent non-target pairs not validated |
| `wnba.player.rebounds` | `disabled_provider_validation` | player | full game | exact half-point over/under | must exactly match | none while disabled | two fresh independent non-target pairs not validated |
| `wnba.player.assists` | `disabled_provider_validation` | player | full game | exact half-point over/under | must exactly match | none while disabled | two fresh independent non-target pairs not validated |
| `wnba.player.made_threes` | `disabled_provider_validation` | player | full game | exact half-point over/under | must exactly match | none while disabled | two fresh independent non-target pairs not validated |

The following are also unavailable and must not generate candidates: whole-number spreads or totals, team totals, alternate ladders, combination props, partial-game markets, quarters, halves, same-game parlays, futures, awards, and all live markets. These absent profiles are unregistered and have no lifecycle; fail closed with `ADAPTER_PROFILE_DISABLED` plus a catalog-absence audit annotation unless a later catalog revision registers one explicitly.

A provider exposing a market does not activate it. Each player-prop profile requires its own evidence and a separately approved lifecycle change.

---

<!-- adapter-section: 3 market_identity_settlement -->
## 3. Market identity and settlement contract

Every quote must retain the complete identity below. Missing or conflicting material fields produce `BLOCKED`; they must not be inferred from a nearby market.

```yaml
market_identity:
  sportsbook_id: string
  jurisdiction: string
  league: WNBA
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
  outcome_set_type: binary_pair
  outcome_set_completeness: complete | incomplete | unknown
  participant_set_version: string | null
  market_wrapper: standard | other | unknown
  side: home | away | over | under
  line: number | null
  period: full_game
  overtime_treatment: included | excluded | unknown
  push_behavior: impossible | push | unknown
  tie_or_dead_heat_treatment: not_applicable | refund | unknown
  void_and_participation_rule: string | unknown
  american_odds: integer
  decimal_odds: number
  market_status: open | suspended | closed | unknown
  retrieved_at_utc: datetime
  provider_last_update_utc: datetime | null
  source_id: string
  raw_snapshot_id: string
  ap_frankenstein_compatibility: direct | equivalent_but_not_supported | unsupported

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

### 3.1 Raw-to-canonical equivalence

| raw market shape | canonical profile | equivalence conditions | settlement conditions | default AP compatibility | status |
|---|---|---|---|---|---|
| `Moneyline`, `Game Moneyline`, or `To Win` | `wnba.full_game.moneyline` | exactly two named teams in the same event; pregame full game | overtime and void rules match every included source | `direct` only for the reviewed standard full-game shape; otherwise `unsupported` | approved conditionally |
| `Spread`, reciprocal team handicaps at `x.5` | `wnba.full_game.spread` | same event, exact reciprocal threshold, both sides available | full game, overtime treatment matches, push impossible | `direct` only for the reviewed standard full-game shape; otherwise `unsupported` | approved conditionally |
| `Total`, `Game Total`, exact `Over/Under x.5` | `wnba.full_game.total` | same event and threshold, complete over/under pair | full game, overtime treatment matches, push impossible | `direct` only for the reviewed standard full-game shape; otherwise `unsupported` | approved conditionally |
| player `Points` at `x.5` | `wnba.player.points` | exact player, event, threshold, period, and opposing sides | participation, overtime, void, and push rules match | `direct` only when the raw shape matches AP Frankenstein's reviewed `wnba_points_threshold` lane | blocked while profile is disabled |
| player `Rebounds`, `Assists`, or `Made Threes` at `x.5` | corresponding player profile | exact player, event, threshold, period, and opposing sides | participation, overtime, void, and push rules match | `equivalent_but_not_supported` pending a WNBA-specific downstream taxonomy review | blocked while profile is disabled |

Raw sportsbook labels and selections are always preserved even when equivalence is approved. Do not equate regulation-only with overtime-included, a team total with a game total, an alternate with a main line, a one-sided ladder with a two-sided market, or one player's quote with another player's quote.

Whole-number spreads and totals are blocked because the active binary EV framework does not model push probability. Do not silently treat push probability as zero. A future push-aware implementation requires deterministic calculation tests and separate activation.

AP compatibility is descriptive metadata only. This adapter creates no API, spreadsheet, settlement, receipt, or handoff integration with AP Frankenstein.

---

### 3.2 Probability and comparison policy

`wnba_market_consensus_mean_v1` applies the global same-line consensus gate with these pilot defaults:

1. Exclude the target sportsbook from fair probability and from comparison coverage.
2. Require at least two usable non-target books assigned to two distinct resolved pricing-origin groups.
3. Require a complete two-sided market from each included book. Never construct a pair across books.
4. Match event, participant, canonical market, threshold, period, overtime, push, void, and participation rules exactly.
5. De-vig each book separately with the project's two-way proportional method.
6. Aggregate the included source-level fair probabilities with an unweighted arithmetic mean, version `wnba_market_consensus_mean_v1`.
7. Require target-quote age no greater than 180 seconds, comparison-quote age no greater than 300 seconds, and collection-time skew no greater than 300 seconds.
8. Report the source-level probabilities, mean, dispersion, oldest quote age, collection skew, target exclusion, pricing-origin groups, and every excluded source with a reason.

If fewer than two usable independent comparison books remain, the candidate is `WATCH` during research and `BLOCKED` at the final placement check. The brief may show the target price, boosted price, break-even probability, and labeled non-consensus comparisons, but it may not report positive EV or `ACTIONABLE FOR REVIEW`.

---

<!-- adapter-section: 4 source_compliance -->
## 4. Source and compliance policy

Source IDs resolve through `source_registry_v1` in `SPORT_ADAPTERS/source_registry.yaml`. That registry owns URLs, access/automation permission, coverage posture, review dates, and triggers; this adapter owns the WNBA facts and gates that those sources must satisfy. URL health alone clears none of those gates.

| source_id/class | facts supplied | authority | access mode | jurisdiction coverage | timestamp rule | terms/license review | permitted use | status |
|---|---|---:|---|---|---|---|---|---|
| `wnba_official_injury_report` | official submission state and player availability | 1 | registry-owned | league-wide operational facts | retain report version/publication time when available plus local UTC retrieval | see registry | operational eligibility and price invalidation | registry posture controls |
| `wnba_official_schedule` | event identity, date, teams, and scheduled tip | 1 | registry-owned | league-wide event facts | retain local UTC retrieval and provider event time | see registry | operational event identity | registry posture controls |
| `wnba_official_roster_tracker` | team membership and roster state | 1 | registry-owned | league-wide roster facts | retain local UTC retrieval | see registry | operational identity/eligibility | registry posture controls |
| `wnba_official_transactions` | signings, waivers, trades, releases, and related changes | 1 | registry-owned | league-wide transaction facts | retain transaction date plus local UTC retrieval | see registry | operational identity/eligibility and price invalidation | registry posture controls |
| `source_class_official_team_announcement` | confirmed starting five or concrete role/availability change | 2 | registry-owned | named team/event only | publication and retrieval times required | see registry | early confirmation and price invalidation | exact instance required |
| `source_class_licensed_sports_data_provider` | schedule, status, roster, or availability | 2 | registry-owned | contract-defined | provider and local UTC timestamps retained | see registry | operational facts within reviewed license | exact instance required |
| `sportsbook_target_manual_evidence`, `source_class_permitted_sportsbook_feed` | exact target quote and promotion terms | 1 for the target screen | registry-owned | exact displayed book and state only | local UTC capture required; provider time retained if present | see registry | target quote and promotion identity | manual default; feed requires registration |
| `source_class_licensed_multi_book_odds_provider` | comparison markets | 1 for quoted markets | registry-owned | contract-defined books and jurisdictions | provider and local UTC timestamps retained | see registry | exact comparison quotes within reviewed license | exact instance required |
| `sportsbook_comparison_manual_evidence`, `source_class_permitted_sportsbook_feed` | one comparison book | 2 | registry-owned | exact displayed book and state only | local UTC capture required | see registry | exact comparison pair | manual conditional; feed requires registration |
| `source_class_secondary_reporting_lead` | possible material-change lead | 4 | registry-owned | named event/team; not an odds jurisdiction source | publication and retrieval times required | see registry | may create `WATCH` pending stronger confirmation | never recommendation-grade alone |

The WNBA's current injury policy says teams ordinarily report by 5 p.m. local time the day before a game and by 1 p.m. local time on the day of the second game of a back-to-back, with reports updated continually. Store these as season-specific configurable values, `wnba_injury_deadlines_2026_v1`, and reverify them from the official page before each new season or after a policy change.

The `wnba_terms_of_use` registry record preserves the current restriction against using the site's defined NBA Statistics in connection with gambling activity. Therefore WNBA.com or stats.wnba.com statistical fields must not be collected, stored as model inputs, scored, or used to support a candidate in this workflow. A future Tier D model requires a separately licensed/permitted statistical source and documented legal/license review. Official schedule, injury, roster, and transaction pages are used only as operational facts under permitted manual/on-demand access; do not scrape, reproduce, or republish them beyond source-referenced local evidence allowed by the source terms.

Do not automate authenticated sportsbook pages, spoof location, bypass geolocation or anti-bot controls, evade rate limits, or depend on an undocumented endpoint as an approved production source.

### 4.1 Pilot sportsbook posture

- Default target assumption: FanDuel Missouri, only when the supplied promotion and target evidence confirm both book and jurisdiction.
- Until a permitted documented FanDuel feed passes validation, the target quote comes from a current user screenshot or structured manual verification. Do not substitute a national or another-state quote.
- `draftkings_wnba_market_page` may count as at most the single `sportsbook_draftkings` non-target pricing origin when an exact current two-sided market and Missouri applicability can be verified.
- One additional independent non-target pricing origin is mandatory. An aggregator record does not create independence by itself; count underlying resolved book origins once.
- If source permission, jurisdiction, identity, timestamp, or pricing-origin independence is unresolved, fail closed.

---

<!-- adapter-section: 5 signal_registry -->
## 5. Active signal registry

The shared `promo_terms`, `target_quote`, `comparison_quotes_same_line`, `market_status`, and `promo_expiration` signals inherit their only authoritative ten-field contracts from Section 5 of `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md`. For this adapter they apply to all `pilot_enabled` profiles and must also satisfy Sections 2-4 above. The extensions below add constraints; they do not create second signal IDs or collection paths.

### 5.1 Inherited shared-signal extensions

| shared_signal_id | profiles | WNBA-specific extension | maximum-age override | reporting extension |
|---|---|---|---|---|
| `promo_terms` | all WNBA profiles | verify eligible event/market/odds, token count, cap, expiry, overtime, push, void, participation, and token-return rules | inherit; reverify at final check | show every material term, confidence, and ambiguity |
| `target_quote` | all `pilot_enabled` profiles | require exact target book/jurisdiction, raw market/selection, event, participant, period, line, overtime, push, settlement, status, and timestamp | inherit 180 seconds | show raw/canonical identity, jurisdiction, status, age, and AP compatibility |
| `comparison_quotes_same_line` | all `pilot_enabled` profiles | require two complete exact pairs from distinct resolved non-target pricing origins and apply `wnba_market_consensus_mean_v1` | inherit 300 seconds and 300-second skew | show target exclusion, source-level fair probabilities, dispersion, ages/skew, origins, and exclusions |
| `market_status` | all `pilot_enabled` profiles | a post-material-change batch must demonstrate suspension/reopening and quote synchronization | inherit | show non-open state, change time, and synchronization result |
| `promo_expiration` | all WNBA profiles | no additional collection path | inherit | show time remaining |

### 5.2 Sport-specific signal registry

The player-prop rows below are complete future contracts but are dormant while their profiles remain `disabled_provider_validation`. Their presence does not authorize polling or candidate generation.

| signal_id | market_profile | tier | source_hierarchy | refresh_trigger | maximum_age | material_change_rule | candidate_state_effect | probability_use | reporting_rule |
|---|---|---|---|---|---|---|---|---|---|
| `wnba_event_identity_status` | all WNBA profiles | A/C | `wnba_official_schedule`; `source_class_licensed_sports_data_provider` | baseline, T-6h, T-30m, final check, and change event | 600 seconds inside T-2h; event identity retained for run | opponent, venue, tip time, event ID, scheduled/delayed/postponed/canceled status, or neutral-site state changes | conflict/cancellation `BLOCKED`; delay or material change `WATCH` and refetch | none | always show identity; changes and blockers emphasized |
| `wnba_injury_submission_state` | all WNBA profiles | A/C | `wnba_official_injury_report`; `source_class_licensed_sports_data_provider` | baseline, applicable submission deadline, T-2h through final check, and report update | current report version; retrieval <=600 seconds inside T-2h; must postdate latest known update | report becomes due/submitted/revised; team row or report version changes | before/during research `WATCH` when required report is missing; final missing report `BLOCKED`; revision newer than quotes `WATCH` and refetch | none | show applicable deadline, submission/version state, and changes affecting either team |
| `wnba_team_availability_delta` | all WNBA profiles | C | `wnba_official_injury_report`; `source_class_official_team_announcement`; `source_class_licensed_sports_data_provider` | every official report revision and candidate-relevant confirmation | same current-report rule as submission signal | player added/removed or participation status/reason changes after price retrieval | `WATCH` and synchronized target/comparison refetch; may clear only with a current post-change batch | none | report exact old/new official status and timestamps; no narrative adjustment |
| `wnba_starting_five_role_event` | all WNBA profiles | C | `source_class_official_team_announcement`; `source_class_licensed_sports_data_provider`; `source_class_secondary_reporting_lead` as unconfirmed only | T-90m, confirmed publication, and change event | latest confirmed event; retrieval <=600 seconds when used near tip | confirmed starter added/removed or concrete starting-role change after quotes | `WATCH` and refetch when confirmed; absence alone does not block full-game game lines | none | change-only for game lines; never describe a projection as confirmed |
| `wnba_roster_transaction_eligibility` | all WNBA profiles | A/C | `wnba_official_roster_tracker`; `wnba_official_transactions`; `source_class_official_team_announcement` | baseline, T-6h, T-2h, and confirmed change | retrieval <=3600 seconds distant and <=600 seconds inside T-2h | target/team membership, waiver, trade, release, signing, suspension, or assignment changes after quotes | identity conflict `BLOCKED`; clear promotion violation `INELIGIBLE`; other material change `WATCH` and refetch | none | report candidate-relevant transaction and timestamps only |
| `wnba_target_player_availability` | all WNBA player profiles | A/C | `wnba_official_injury_report`; `wnba_official_roster_tracker`; `source_class_licensed_sports_data_provider` | report deadline, every revision, T-30m, and final check | current report/inactive state; retrieval <=600 seconds inside T-2h | target becomes available/probable/questionable/doubtful/out/inactive or changes participation state | out/inactive `INELIGIBLE` or `BLOCKED` per terms; questionable/doubtful `WATCH`; probable may clear only with current post-change quotes and verified rules | none | always for a future prop candidate; dormant while profiles disabled |
| `wnba_game_market_context_for_props` | all WNBA player profiles | C | `source_class_licensed_multi_book_odds_provider`; `sportsbook_comparison_manual_evidence` | after material availability news or full-game threshold/movement event | same synchronized price-batch limits | configured full-game market move occurs after prop quotes | `WATCH` and prop-price refetch only | none; never substitutes for prop consensus | report only as refetch cause; dormant while profiles disabled |

<!-- adapter-section: 6 materiality_state -->
## 6. Materiality and state rules

| rule_id | profiles | source fields / qualifying change | effective-time rule | state effect | required refetch | resolution rule | probability effect |
|---|---|---|---|---|---|---|---|
| `wnba_event_state_materiality_v1` | all WNBA profiles | event ID, opponents, venue, tip, neutral site, delay, postponement, cancellation, or status changes | any authoritative change newer than an affected quote invalidates that quote | conflict/cancellation `BLOCKED`; resolvable change `WATCH` | shared target and complete comparison signals | current event state plus synchronized post-change batch | none |
| `wnba_injury_submission_materiality_v1` | all WNBA profiles | report becomes due, submitted, missing, or revised; team row/version changes | compare applicable deadline/report publication with quote retrieval | missing required report `WATCH`, then `BLOCKED` at final check; revision newer than quotes `WATCH` | shared target and complete comparison signals | current submission/version plus synchronized post-change batch | none |
| `wnba_availability_role_materiality_v1` | all WNBA profiles | player added/removed or official availability/confirmed starting-role status changes | any confirmed candidate-relevant change newer than quotes invalidates them | `WATCH`; player-profile out/inactive becomes `INELIGIBLE` or `BLOCKED` under exact terms | shared target and complete comparison signals | current official fact plus synchronized post-change batch | none |
| `wnba_roster_transaction_materiality_v1` | all WNBA profiles | membership, signing, waiver, release, trade, suspension, eligibility, or assignment changes | qualifying official effective/publication time compared with quote retrieval | identity conflict `BLOCKED`; clear promo violation `INELIGIBLE`; otherwise `WATCH` | shared target and complete comparison signals | resolved identity/eligibility plus synchronized post-change batch | none |
| `wnba_post_change_price_sync_v1` | all `pilot_enabled` profiles | market suspension/reopening or any target/comparison quote older than a registered material fact | all included quotes must postdate the material fact and meet age/skew rules | remain `WATCH`; unavailable/suspended final batch `BLOCKED`; valid batch re-ranks from Tier B only | shared target, comparison, and market-status signals | synchronized open batch with valid consensus | none |

### 6.1 State-resolution rules

- Before the applicable injury-report deadline, label the submission `not_due`; a preliminary ranking may be shown as `WATCH`, but it cannot clear the final availability gate.
- After the deadline, a missing required team submission is `WATCH` during research and `BLOCKED` at the final placement check.
- A current official availability report plus a synchronized post-change game-line price batch may clear the availability gate even when no league-wide confirmed starting-five feed exists.
- A confirmed starting-five or availability change newer than any affected quote always returns the candidate to `WATCH` until every affected target/comparison quote is refreshed.
- A still-questionable team player does not create a manual game-line penalty. If the official report and market batch are current, the game-line candidate is evaluated from consensus; the unresolved status and invalidation condition remain visible.
- A future player-prop candidate with a questionable or doubtful target remains `WATCH`. An out/inactive target is `INELIGIBLE` when the promotion/book rule is clear and otherwise `BLOCKED`.
- Context facts never add or subtract probability or ranking points. Refreshed Tier B prices are the only active numerical valuation input.

### 6.2 Signal migration map

The version `0.2.0` normalization removes duplicate shared-policy signal definitions. Historical briefs remain interpretable through this mapping; new briefs emit the authoritative shared signal ID and the applicable WNBA extension/materiality rule.

| former signal ID | normalized authority | migration behavior |
|---|---|---|
| `wnba_promo_settlement_terms` | shared `promo_terms` plus Section 5.1 WNBA extension | preserve former ID only when reading a historical brief |
| `wnba_consensus_quality` | shared `comparison_quotes_same_line` plus `wnba_market_consensus_mean_v1` | preserve former ID only when reading a historical brief |
| `wnba_post_news_market_state` | shared quote/status signals plus `wnba_post_change_price_sync_v1` | preserve former ID only when reading a historical brief |

---

<!-- adapter-section: 7 refresh_policy -->
## 7. Refresh policy

This cadence defines the evidence an on-demand run or user-requested refresh must obtain. It does not install a scheduler or authorize background polling.

| phase_id | WNBA window or trigger | required refresh | maximum ages | state if unavailable | next refresh reason |
|---|---|---|---|---|---|
| `intake` | promotion intake | each token's terms, eligible slate, event identity, initial report state, target, comparison pairs, and source/jurisdiction metadata | source/event scoped; quote pilot limits apply | material term or target missing `BLOCKED`; incomplete context/consensus `WATCH` | applicable injury deadline, provider refresh, or material fact |
| `distant_pregame` | around T-6h | event/tip, roster/transaction, official availability, target, and comparison batches | roster <=3600 seconds distant; quote pilot limits | `WATCH` when a required current fact or valid consensus is unavailable | T-2h availability window or source event |
| `official_release_window` | applicable injury deadline through final check, including T-2h checks | submission/version for both teams, changed rows, and candidate-relevant roster/role facts every 10-15 minutes when event data is unavailable | current report; <=600 seconds inside T-2h | missing after deadline `WATCH`; unresolved final requirement `BLOCKED` | next report revision/check or confirmed change |
| `material_change` | any registered material change | invalidate quotes; refresh target, complete comparisons, market status, and synchronization audit | target <=180 seconds; comparisons <=300 seconds; skew <=300 seconds | `WATCH`; final unavailable batch `BLOCKED` | synchronized post-change price batch |
| `shortlist_check` | around T-30m | shortlist eligibility, event, availability, confirmed role event if published, target, comparisons, and consensus | registry ages and quote pilot limits | `WATCH` or `BLOCKED` according to failed gate | final synchronized check |
| `final_sync` | immediately before human placement | promotion, event, availability, target, comparisons, jurisdiction, settlement, and QA | all final recommendation-grade limits | any fatal, stale, or conflicting input `BLOCKED` | none; new evidence requires a new run |

Target quotes must be no older than 180 seconds and comparisons no older than 300 seconds at actionability. If permitted sources cannot meet these ages or the 300-second collection-skew limit, fail closed rather than relaxing the thresholds.

---

<!-- adapter-section: 8 tier_d_registry -->
## 8. Tier D model-only registry

All groups below are `disabled_model_only`. They are hypotheses, not active metrics, and must not be routinely fetched, scored, narrated, or used to change probability, state, or rank.

| group_id | potential consumers | candidate future inputs | required source permission | named model consumer | activation evidence | anti-noise boundary | lifecycle |
|---|---|---|---|---|---|---|---|
| `wnba_model_minutes_rotation` | player props and team markets | projected minutes, substitution pattern, starting/bench role, rotation depth | separately licensed/permitted data | none | named model, leak-free history, out-of-sample calibration, uncertainty and monitoring | no projection from one recent game or generic coach quote | `disabled_model_only` |
| `wnba_model_scoring_opportunity` | points and team totals | usage, field-goal/free-throw attempts, touches, shot-location opportunity | separately licensed/permitted data | none | same full model requirements | no raw recent average or last-N overs | `disabled_model_only` |
| `wnba_model_three_point_opportunity` | made threes and totals | three-point attempt share, shot type/location, expected minutes | separately licensed/permitted data | none | same full model requirements | no short hot/cold shooting streak | `disabled_model_only` |
| `wnba_model_assist_opportunity` | assists | potential assists, passes, touches, possession role | separately licensed/permitted data | none | same full model requirements | no tiny teammate-on/off or recent box-score narrative | `disabled_model_only` |
| `wnba_model_rebound_opportunity` | rebounds | rebound chances, position, missed-shot environment, expected minutes | separately licensed/permitted data | none | same full model requirements | no defense-vs-position rank or raw recent rebounds | `disabled_model_only` |
| `wnba_model_pace_efficiency` | sides, totals, and props | projected possessions and calibrated offensive/defensive efficiency | separately licensed/permitted data | none | same full model requirements | no standalone season rank or pace narrative | `disabled_model_only` |
| `wnba_model_lineup_redistribution` | all player props and team markets | shrunk lineup/on-off role redistribution with personnel identity | separately licensed/permitted data | none | same full model requirements | exclude tiny lineup samples and double-counting post-news market movement | `disabled_model_only` |
| `wnba_model_participation_tail` | all profiles | rest, travel, workload, foul, blowout, overtime, and minutes-tail distributions | separately licensed/permitted data | none | same full model requirements | no manual penalty from travel, fatigue, foul, or blowout stories | `disabled_model_only` |

WNBA.com and stats.wnba.com are not approved sources for these model inputs under the current terms. A later licensed source must identify exact permitted fields and uses.

---

<!-- adapter-section: 9 tier_x_exclusions -->
## 9. Tier X exclusions

Do not collect or present these groups as recommendation evidence:

| excluded group | examples | reason excluded | permitted operational use |
|---|---|---|---|
| recent-results narratives | hot/cold streaks, last-five/ten, recent overs, raw recent averages | no enabled calibrated consumer | none |
| motivation and arbitrary splits | head-to-head, revenge, must-win, homecoming, birthday, milestone, national TV, home/away, day, ATS, or venue splits | narrative or unstable association | none |
| unsupported market narratives | public percentages, social sentiment, unsupported sharp-money claims | unresolved provenance and no probability contract | none |
| weak matchup/model proxies | defense-vs-position rankings and tiny lineup/on-off/opponent/role samples | disabled or inadequately validated model inputs | none |
| quotes, rumors, and officials trends | generic confidence quotes, unverified injury/lineup/trade/suspension/rest rumors, referee trends | insufficient authority or validated consumer | lower-authority material-change lead may create `WATCH` pending confirmation |
| participation-tail speculation | foul, blowout, travel, rest, or overtime stories | model-only family remains disabled | none |
| LLM-authored adjustment | any manually invented probability or ranking change | violates deterministic valuation boundary | none |

A lower-authority report may create `WATCH` only when it plausibly signals a registered material change. It must be confirmed or rejected by an approved source; it cannot create positive-EV language.

---

<!-- adapter-section: 10 provider_evidence -->
## 10. Provider evidence

### 10.1 Game-line pilot

Validate FanDuel Missouri target retrieval against timestamped user-visible app evidence under at least these conditions:

1. board open or distant pregame;
2. after an official availability or material status update; and
3. near tip.

For every capture, require exact agreement on jurisdiction, event, teams, market, side, line, period, overtime/settlement, market status, and price. A price difference is acceptable only when retrieval timestamps demonstrate an explainable market move rather than an identity failure. Retain local UTC request start/end, provider timestamp when present, raw snapshot/content hash, screenshot timestamp, and discrepancy resolution.

Validate each comparison origin independently. Each must expose a complete exact pair and meet the age/skew gates. Resolve underlying pricing-origin identity before counting an aggregator or duplicate provider record.

Current evidence state: no recommendation-grade automated FanDuel Missouri adapter or two-origin comparison configuration is certified by this document. `pilot_enabled` analysis therefore relies on verified screenshot/manual target evidence and only becomes actionable when the run itself obtains two valid independent comparison pairs.

| evidence_id | profile scope | role | timing conditions required | current evidence state | certification effect |
|---|---|---|---|---|---|
| `wnba_game_line_target_cross_timing` | three `pilot_enabled` game-line profiles | target | board open, post-material-change, and near tip | incomplete; per-run screenshot/manual validation remains required | none |
| `wnba_game_line_comparison_origins` | three `pilot_enabled` game-line profiles | comparison | same three timing conditions with exact complete pairs and resolved origins | no two-origin configuration certified by this document | none |
| `wnba_player_prop_cross_timing` | four disabled player profiles | target and comparison | exact-profile evidence at all required timing conditions | not satisfied | profiles remain `disabled_provider_validation` |

### 10.2 Player-prop promotion gate

A player profile remains `disabled_provider_validation` until all of the following are recorded for that exact profile:

- complete target and two-sided comparison identity, including player participation and void rules;
- at least two fresh independent non-target complete over/under pairs at the exact threshold;
- evidence at board open, after material availability news, and near tip across representative events;
- successful timestamp, status, jurisdiction, entity, period, overtime, and settlement validation;
- missing, stale, suspended, one-sided, and mismatched contract scenarios;
- deterministic calculation tests for the exact line shape; and
- a separate explicit lifecycle approval reflected in the adapter catalog, monitoring playbook, `AGENTS.md`, and `README.md`.

Provider availability alone does not satisfy this gate.

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

These Markdown rows are synthetic contract scenarios, not provider evidence or executable fixtures. Real timestamped captures belong in Section 10. Future machine-readable test inputs must be labeled executable fixtures and validated against an approved schema.

| scenario | required outcome |
|---|---|
| Exact eligible FanDuel Missouri game-line target, two fresh independent complete comparison books, current official report, matching settlement, and all QA gates | deterministic EV ranking may produce `ACTIONABLE FOR REVIEW` |
| Target evidence comes from another state or cannot establish jurisdiction | `BLOCKED`; do not substitute it |
| FanDuel is target and DraftKings is the only usable comparison | `WATCH` during research; `BLOCKED` at final check; break-even only |
| One comparison record duplicates another pricing origin | count the origin once; downgrade if fewer than two independent origins remain |
| Comparison lacks the opposing side or uses a different line, period, overtime, or settlement rule | exclude it; never create a synthetic pair |
| Required injury report is not yet due | preliminary result may remain `WATCH`; it cannot clear the final availability gate |
| Required report is overdue or missing | `WATCH`, becoming `BLOCKED` at final check |
| Official availability, roster, transaction, game, or confirmed-role fact is newer than prices | invalidate affected quotes, set `WATCH`, and refetch without changing probability directly |
| Post-change target and two independent comparison pairs are current | clear the context blocker and rank from refreshed Tier B prices only |
| Starting five is not confirmed but the official report and post-change game-line prices are current | do not block solely for missing starting-five confirmation |
| Whole-number spread or total | `BLOCKED`; push-aware math is inactive |
| Suspended, stale, closed, or unknown target market | `BLOCKED` |
| WNBA points, rebounds, assists, or made-threes request | `BLOCKED` with `ADAPTER_PROFILE_DISABLED`; lifecycle remains `disabled_provider_validation`; no candidate generation |
| Future player target becomes questionable or doubtful | `WATCH`; dormant while player profiles are disabled |
| Future player target becomes out/inactive | `INELIGIBLE` or `BLOCKED` under exact terms; dormant while player profiles are disabled |
| A recent streak, defense-vs-position rank, public betting claim, or generic quote is supplied | ignore as Tier X; no probability, state, or rank effect |
| Three tokens exist but only one or two candidates pass | recommend only the passing uses; do not lower gates |
| Live WNBA request | `BLOCKED`; live profiles are unavailable |
| User manually places a researched wager | no AP Frankenstein action from this project; downstream workflow remains separate |

---

<!-- adapter-section: 12 run_decision_brief -->
## 12. On-demand run and decision-brief contract

### 12.1 Three-token allocation workflow

1. Parse and verify each token separately. Do not assume identical boost type, percentage, eligible markets/events, odds range, cap, expiry, overtime, push, void, or token-return terms.
2. Build a token-by-candidate eligibility matrix across the complete eligible WNBA slate and only `pilot_enabled` profiles.
3. For every eligible token/candidate pair, deterministically calculate the actual boosted price, break-even probability, consensus fair probability, EV per unit, permitted stake, and expected dollars.
4. Exclude `WATCH`, `BLOCKED`, `INELIGIBLE`, stale, suspended, mismatched, or consensus-invalid pairs from the actionable allocation.
5. Select the allocation that maximizes total expected dollars subject to each token being used no more than once, the same wager not receiving multiple tokens unless the terms explicitly allow it, promotion restrictions, and user exposure limits.
6. Do not apply a hidden correlation penalty. Show shared-game/team exposure and obey configured correlation or exposure limits; when no limit is supplied, leave the tradeoff for human review.
7. Report meaningful passes and the opportunity cost of each selected token use. If fewer than three candidates pass, recommend fewer than three uses.

The decision brief must include adapter/profile version, raw and canonical market labels, AP compatibility, target exclusion, comparison-origin audit, settlement/overtime/push verification, official availability state, quote ages/skew, EV and expected dollars, correlation warnings, passes, blockers, and the next refresh condition.

Save a local research/evidence snapshot only. Never place or confirm a wager and never call or write to AP Frankenstein.

### 12.2 Reusable on-demand task contract

```text
Evaluate the supplied WNBA promotion tokens using WNBA adapter wnba.pregame_full_game_v0_1 version 0.2.1 and adapter_contract_v1.

Parse every token separately and verify FanDuel Missouri or the actual supplied target jurisdiction, exact eligible events/markets, boost type, percentage, cap, odds range, expiry, overtime, push, void, and token-return terms. Consider only pregame full-game moneyline and half-point spread/total profiles. Player props, whole-number lines, alternate/team/partial markets, SGPs, live betting, and statistical models are disabled.

Preserve raw sportsbook labels and exact canonical identity. Use current verified target evidence and at least two fresh, complete exact opposing markets from independent non-target pricing origins. Exclude the target book, de-vig each comparison book separately, and apply wnba_market_consensus_mean_v1. If the consensus gate fails, report boosted break-even only and use WATCH/BLOCKED as required.

Retrieve the current official WNBA schedule/event state, injury-report submission and relevant availability rows, roster/transaction identity, and any confirmed starting-role event. Any material fact newer than prices invalidates the batch and triggers synchronized target/comparison refreshes. Do not manually change probability for injuries, lineups, rest, travel, narratives, or other context.

Use deterministic promotion, odds, no-vig, EV, expected-dollar, freshness, and allocation calculations. Rank the whole eligible slate and allocate up to three tokens to maximize expected dollars under the exact terms and user limits. Return fewer uses when fewer candidates pass.

Return the standard Promotion Decision Brief with adapter version, promotion interpretation, ranked candidates, passes, official availability state, quote/source/origin audit, settlement and jurisdiction checks, ages/skew, blockers, next refresh condition, and human-decision boundary. Save only a local evidence snapshot. Never place or confirm a wager and make no AP Frankenstein call or write.
```

---

<!-- adapter-section: 13 activation_change_log -->
## 13. Activation checklist and change log

Before any WNBA profile lifecycle change, the adapter-template checklist must pass. Contract scenarios document expected behavior; real cross-timing captures belong in provider evidence, and an executable runtime must use machine-readable executable fixtures plus deterministic tests. Source permissions, exact identity and settlement, pricing-origin independence, six-phase refresh coverage, and separate explicit approval must be reflected consistently in the canonical catalog and governing documents. Specification completeness alone is not activation evidence.

| date | version | change | approval/evidence |
|---|---|---|---|
| 2026-07-12 | `0.1.0` | Created experimental WNBA full-game game-line adapter; documented but did not activate four player-prop profiles | User-approved WNBA adapter implementation plan; provider validation remains run-time and profile-gated |
| 2026-07-12 | `0.2.0` | Conformed to `adapter_contract_v1`, normalized refresh/materiality/model/noise/evidence tables, and replaced duplicate shared-policy signals with extensions plus a migration map | approved sport-adapter contract normalization plan; no lifecycle or analytical behavior change |
| 2026-07-13 | `0.2.1` | Normalized the document to the 13-section `adapter_contract_v1` layout, added binary outcome-set audit fields, nested token allocation under the run contract, and clarified scenario/evidence/fixture terminology | governance cleanup; no lifecycle, probability, outcome, freshness, source, or run-behavior change |
