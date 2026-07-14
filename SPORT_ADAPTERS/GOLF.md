# Golf Pregame Stroke-Play Sport Adapter

<!-- adapter-section: 1 adapter_metadata -->
## 1. Adapter metadata

**Adapter ID:** `golf.pregame_stroke_play_v0_1`

**Version:** `0.1.1`

**Structural contract:** `adapter_contract_v1`

**Document status:** Active pre-activation documentation policy

**Sport:** Golf

**Competition scope:** Multi-organizer individual stroke play offered by FanDuel or DraftKings in Missouri

**Lifecycle:** All registered profiles are `disabled_provider_validation`

**Last reviewed:** 2026-07-13

**Default timezone:** `America/Chicago`

**Run mode:** On-demand local decision brief only after separately approved schema evolution and a lifecycle change

**Fair-probability method:** Profile-specific exact-market consensus after separate deterministic-method and provider validation

```yaml
adapter:
  adapter_id: golf.pregame_stroke_play_v0_1
  version: 0.1.1
  contract_version: adapter_contract_v1
  document_status: active pre-activation documentation policy
  sport: Golf
  league: multi_organizer_individual_stroke_play
  default_timezone: America/Chicago
  last_reviewed: 2026-07-13
  review_owner: Advantage Play Intern
  run_mode: on_demand_local_brief_after_schema_evolution_and_separate_activation
  probability_method: profile_specific_exact_market_consensus_after_separate_activation
  autonomous_wagering: false
  ap_frankenstein_integration: false
```

This adapter specifies a credential-free, pre-activation contract for supervised Missouri golf-promotion research. Promotion value is expected to create most of any future opportunity. Golf context may verify competition, participant, period, course, settlement, and availability identity; invalidate an older price batch; or block a scenario. It never creates an ad hoc probability adjustment, and this adapter does not predict golf performance.

The eligible discovery slate is limited to individual stroke-play tournaments for which FanDuel or DraftKings displays a market to the user in Missouri. Sportsbook availability creates only a slate candidate. It does not prove competition format, source permission, exact market identity, settlement treatment, comparison coverage, or adapter support. Every event still requires a verified event-specific competition and house-rule source pack.

This adapter must be applied with `PROJECT_CONTEXT.md`, `PROMO_ANALYSIS_PLAYBOOK.md`, `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md`, and `SPORT_ADAPTERS/README.md`. It does not authorize provider calls, sportsbook access, candidate generation, recurring monitoring, alerts, scheduling, code, wager action, or AP Frankenstein integration. Every registered profile remains blocked until separately reviewed schema evolution, provider evidence, exact settlement identity, source permission, deterministic calculation path, credential-free validation, and separate activation approval all exist.

---

<!-- adapter-section: 2 profile_registry -->
## 2. Profile registry

| profile_id | lifecycle | participant scope | period | allowed line shape | completion, tie, and settlement treatment | probability method | activation blocker |
|---|---|---|---|---|---|---|---|
| `golf.player.make_cut` | `disabled_provider_validation` | player | tournament through the first official cut | exact Yes/No pair for the same player and first official cut, with every possible settlement state assigned to Yes or No | cut must exist and match every source; DNS, WD, DQ, shortened-event, and incomplete-cut treatment must be exact; no unmodeled refund/void state | `golf_binary_market_consensus_mean_v1` after activation | real Missouri promotion evidence, exact cut/settlement identity, target coverage, two independent comparison origins, cross-timing freshness, and separate approval are absent |
| `golf.player.round_score_total` | `disabled_provider_validation` | player | exact scheduled round and course | exact reciprocal 18-hole Over/Under pair at `x.5`, with no third refund/void outcome | selected round must not have started; completion, par, course, tee, DNS, WD, DQ, and void rules must match; score push impossible and no refund state remains unmodeled | `golf_binary_market_consensus_mean_v1` after activation | exact round/course identity, completion rules, target coverage, two independent comparison origins, and separate approval are unvalidated |
| `golf.player.round_matchup` | `disabled_provider_validation` | exactly two players | exact scheduled round and course | exact exhaustive two-way no-push/no-refund pair or complete three-way player/player/tie set; tie-refund remains structurally blocked | selected players must not have started the round; participant, tie, completion, DNS, WD, DQ, and void rules must match | binary or future `golf_multiway_market_consensus_mean_v1` according to the exact outcome set | exact variant, tie/completion treatment, complete outcome-set coverage, deterministic method, and separate approval are unvalidated |
| `golf.player.tournament_matchup` | `disabled_provider_validation` | exactly two players | whole tournament | exact exhaustive two-way no-push/no-refund pair or complete three-way player/player/tie set; tie-refund remains structurally blocked | cut, minimum action, completion, tie, DNS, WD, DQ, shortened-event, and void rules must match | binary or future `golf_multiway_market_consensus_mean_v1` according to the exact outcome set | exact cut/completion/tie treatment, complete outcome-set coverage, deterministic method, and separate approval are unvalidated |
| `golf.player.top_n_finish` | `disabled_provider_validation` | player | whole tournament | exact Top 5, Top 10, or Top 20 wrapper; standard dead heat, including-ties, OddsBoost, and Tourney Special shapes remain distinct | threshold, tie/dead-heat payout, playoff, minimum action, DNS, WD, DQ, and shortened-event rules must match; any binary pair must leave no unmodeled refund/void state | binary consensus only for a proven exhaustive full-pay Yes/No pair; otherwise unavailable | wrapper-specific settlement, dead-heat method, complete complementary coverage, target evidence, and separate approval are unvalidated |
| `golf.tournament.outright_winner` | `disabled_provider_validation` | player within an exhaustive event field | whole tournament | exact pre-tournament winner outcome set for one field version | all-in/DNS, WD, DQ, playoff, co-winner/dead-heat, minimum action, official-result, and shortened-event rules must match | future `golf_multiway_market_consensus_mean_v1` only | exhaustive field coverage, stable field version, deterministic multiway implementation, target/comparison evidence, and separate approval are absent |

No registered golf profile is selectable for recommendation-grade candidate generation. Every otherwise structurally valid request returns `BLOCKED` with `ADAPTER_PROFILE_DISABLED` and produces no probability, EV, allocation, ranking, alert, or actionable candidate.

Each-way, first-round leader, group/3-ball/4-ball, team, match-play, Stableford, skins, nationality, finishing-position bands other than the registered Top-N thresholds, player scoring props other than exact round totals, parlays, same-game parlays, and in-play markets are unavailable by catalog absence. A provider displaying one of those markets does not make it equivalent to a registered profile.

For round profiles, “pregame” means before the exact selected round and before either selected participant has started that round. Prior tournament rounds may already be complete, but no in-play quote, on-course state, or market captured after the relevant participant starts is registered.

---

<!-- adapter-section: 3 market_identity_settlement -->
## 3. Market identity and settlement contract

Every target and comparison record must retain the standard identity fields plus the golf-local audit fields below. During this disabled contract phase these fields remain adapter-local audit annotations; they do not change `promotion_decision_brief_v2`, a persisted schema, a global formula, or AP Frankenstein. The current team-event and single-outcome structures cannot canonically carry complete Golf field, identity, and outcome vectors, so separately reviewed schema evolution is a mandatory activation blocker.

```yaml
market_identity:
  sportsbook_id: string
  jurisdiction: Missouri
  sport: Golf
  organizer_id: string
  tour_id: string
  event_id: string
  provider_event_id: string
  event_edition_id: string
  event_name_raw: string
  venue_id: string
  course_id: string | null
  event_format: individual_stroke_play
  scheduled_rounds: integer
  scheduled_holes: integer
  field_version: string
  participant_set_id: string
  participant_set_version: string
  outcome_set_id: string
  outcome_set_type: binary_pair | mutually_exclusive_exhaustive_multiway | other
  outcome_set_completeness: complete | incomplete | unknown
  participant_id: string | null
  provider_participant_id: string | null
  opponent_participant_id: string | null
  player_entry_status: entered | alternate | did_not_start | withdrawn | disqualified | unknown
  tee_time_status: published | changed | not_published | started | unknown
  round_id: string | null
  round_number: integer | null
  round_course_id: string | null
  tee_id: string | null
  round_par: integer | null
  cut_rule_id: string | null
  cut_structure: single_cut | multiple_cuts | no_cut | other | unknown
  cut_stage_count: integer | null
  cut_size_rule: string | unknown
  cut_ties_rule: string | unknown
  cut_stage: first_official_cut | other | none | unknown
  cut_status: not_reached | in_progress | complete | not_applicable | unknown
  raw_market_label: string
  raw_selection_label: string
  canonical_market_key: string
  market_wrapper: standard | including_ties | oddsboost | tourney_special | other | unknown
  side: yes | no | over | under | participant_a | participant_b | tie | player | other
  line: number | null
  position_threshold: 5 | 10 | 20 | null
  period: tournament | exact_round
  overtime_treatment: not_applicable
  period_start_status: not_started | started | complete | unknown
  push_behavior: impossible | push | unknown
  tie_or_dead_heat_treatment: not_applicable | refund | dead_heat | full_pay | separate_tie_outcome | unknown
  minimum_action_rule: string | unknown
  dns_treatment: string | unknown
  withdrawal_treatment: string | unknown
  disqualification_treatment: string | unknown
  tie_treatment: string | unknown
  playoff_treatment: string | unknown
  dead_heat_treatment: string | unknown
  shortened_event_treatment: string | unknown
  void_and_participation_rule: string | unknown
  house_rule_source: string | unknown
  house_rule_version: string | unknown
  official_result_finality: not_applicable_pregame | pending | official | corrected | unknown
  american_odds: integer
  decimal_odds: number
  market_status: open | suspended | closed | unknown
  retrieved_at_utc: datetime
  provider_last_update_utc: datetime | null
  source_id: string
  raw_snapshot_id: string
  ap_frankenstein_compatibility: unsupported

binary_outcome_set_audit:
  applies: true | false
  source_sportsbook_id: string | null
  source_pricing_origin_id: string | null
  candidate_outcome_id: string | null
  opposing_outcome_id: string | null
  candidate_retrieved_at_utc: datetime | null
  opposing_retrieved_at_utc: datetime | null
  same_book: true | false | not_applicable
  same_market_identity: true | false | not_applicable
  same_line: true | false | not_applicable
  same_settlement_contract: true | false | not_applicable
  complete: true | false | not_applicable
  exclusion_reason_codes: list[string]
```

`ap_frankenstein_compatibility` is `unsupported` for every golf market in this milestone. The field is descriptive only. It creates no receipt, spreadsheet, settlement, write, API, or handoff integration.

### 3.1 Raw-to-canonical equivalence

| raw market shape | canonical profile | equivalence conditions | settlement conditions | AP compatibility | status |
|---|---|---|---|---|---|
| `Make Cut - Yes/No` or `To Make the Cut` | `golf.player.make_cut` | exact player, event edition, first official cut, field version, and complete same-book Yes/No pair | event has a verified cut; book and competition identify the same first cut; every DNS/WD/DQ, incomplete-cut, multiple-cut, and shortening state maps to Yes or No with no unmodeled refund/void state | `unsupported` | structurally approved only; profile remains disabled |
| `Round N Score Over/Under x.5` | `golf.player.round_score_total` | exact player, round, course, 18-hole period, half-point line, and complete same-book pair | period not started; par, completion, DNS/WD/DQ, and void rules match; score push is impossible and every action state maps to Over or Under | `unsupported` | structurally approved only; profile remains disabled |
| whole-number round score total | none | exact integer score can push | push-aware probability and EV are unavailable | `unsupported` | `BLOCKED` with `PUSH_MODEL_UNAVAILABLE` |
| two-player round matchup with two exhaustive no-push outcomes | `golf.player.round_matchup` | exact players, round, course, participant set, and complete same-book binary pair | a verified rule assigns every possible result to exactly one outcome; no push/tie refund/void state; completion/DNS/WD/DQ rules match | `unsupported` | structurally approved only; profile remains disabled |
| two-player round matchup with Player A / Player B / Tie | `golf.player.round_matchup` | exact players, round, course, and complete same-book three-outcome set | tie is a separate outcome; completion/DNS/WD/DQ rules match without another refund/void outcome | `unsupported` | future multiway shape only; profile remains disabled |
| two-player whole-tournament matchup | `golf.player.tournament_matchup` | exact players, event edition, field version, period, and complete binary or three-way set | cut, minimum-action, completion, tie, DNS/WD/DQ, void, and shortening rules match; the selected set is exhaustive | `unsupported` | structurally approved only; profile remains disabled |
| any matchup whose tie or other possible state is refunded or pushes | registered matchup profile with structural blocker | identity may match, but the outcome contract includes a push/refund | requires independent `p_push` support and push-aware deterministic EV | `unsupported` | `BLOCKED` with `PUSH_MODEL_UNAVAILABLE` |
| `Top 5`, `Top 10`, or `Top 20` standard | `golf.player.top_n_finish` | exact player, N, event edition, field version, and raw wrapper retained | standard dead-heat fraction, minimum action, DNS/WD/DQ, and shortening rules must be exact | `unsupported` | registered but `PROBABILITY_METHOD_UNAVAILABLE` until dead-heat valuation is implemented |
| Top-N `including ties` or verified full-pay Yes/No | `golf.player.top_n_finish` | exact player/N and wrapper; comparison use additionally requires a complete same-book complementary Yes/No pair | full payout and tie treatment must be proven identical across target and comparisons; every possible action state maps to Yes or No | `unsupported` | structurally approved only; profile remains disabled |
| FanDuel OddsBoost or Tourney Special Top-N | `golf.player.top_n_finish` | preserve exact product label; do not normalize to standard or including-ties without rule-by-rule proof | full-win/dead-heat boundary, eligibility, and all settlement rules must match | `unsupported` | structurally approved only when exact; profile remains disabled |
| complete pre-tournament winner field | `golf.tournament.outright_winner` | every possible winner in the same official field version appears once in each source outcome set | all-in/DNS, WD/DQ, playoff, co-winner/dead-heat, minimum-action, finality, and shortening rules match without an extra refund outcome | `unsupported` | future multiway shape only; profile remains disabled |
| partial outright board or mixed field versions | none for valuation | an exhaustive mutually exclusive set is not proven | missing entrants or changed field invalidate normalization | `unsupported` | `BLOCKED` with `OUTCOME_SET_INCOMPLETE` |
| round versus tournament matchup, nearby Top-N threshold, different round/course, or different wrapper | none | period, participants, threshold, course, or product identity differs | settlement cannot be assumed equivalent | `unsupported` | `BLOCKED` with `MARKET_IDENTITY_MISMATCH` and/or `SETTLEMENT_RULE_MISMATCH` |

Never manufacture a complementary outcome, combine outcomes from different books into one source market, infer an omitted golfer, use a nearby threshold, or collapse standard, including-ties, OddsBoost, Tourney Special, tie-refund, and three-way products into one market.

---

### 3.2 Probability and comparison policy

All methods in this section are inactive specifications. Lifecycle enforcement occurs before probability, EV, or ranking. No contract scenario, formula, provider field, or complete-looking market activates a profile.

| profile | source-level outcome-set requirement | de-vig method | push requirement | dead-heat requirement | current status |
|---|---|---|---|---|---|
| `golf.player.make_cut` | exhaustive same-book Yes/No pair for the first official cut; every action state maps to one side | `golf_binary_market_consensus_mean_v1` | no refund/void state remains outside the pair | not applicable | inactive specification; method/evidence not validated and profile disabled |
| `golf.player.round_score_total` | exhaustive same-book half-point Over/Under pair for the exact player/round/course | `golf_binary_market_consensus_mean_v1` | score push impossible and no completion/refund state remains outside the pair | not applicable | inactive specification; method/evidence not validated and profile disabled |
| `golf.player.round_matchup` | exhaustive no-push/no-refund binary pair or complete Player A/Player B/Tie set | binary method or future `golf_multiway_market_consensus_mean_v1` according to the exact set | tie-refund or any other push state is unavailable without independent `p_push` | not applicable | inactive specification; method/evidence not validated and profile disabled |
| `golf.player.tournament_matchup` | exhaustive no-push/no-refund binary pair or complete Player A/Player B/Tie set | binary method or future `golf_multiway_market_consensus_mean_v1` according to the exact set | tie-refund or any other push state is unavailable without independent `p_push` | not applicable | inactive specification; method/evidence not validated and profile disabled |
| `golf.player.top_n_finish` | exhaustive full-pay Yes/No pair only; ordinary Top-N propositions are overlapping | binary method only for the proven exhaustive full-pay pair | no refund/void state remains outside the pair | exact full-pay rule required; standard dead-heat distribution unavailable | full-pay pair remains unvalidated; standard dead-heat shape has no supported method; profile disabled |
| `golf.tournament.outright_winner` | complete mutually exclusive and exhaustive winner field under one field version | future `golf_multiway_market_consensus_mean_v1` | no refund state remains outside the set | exact single-winner/playoff rule required; co-winner/dead-heat path unavailable | inactive specification; method/evidence not validated and profile disabled |

#### 3.2.1 Binary exact-market consensus

`golf_binary_market_consensus_mean_v1` is the only planned path for exact make-cut Yes/No, half-point round totals, a proven exhaustive no-push binary matchup, or a proven full-pay Top-N Yes/No pair:

1. Exclude the target sportsbook from probability and comparison coverage.
2. Require at least two usable non-target books from two distinct resolved pricing-origin groups.
3. Require each included book to supply its own complete exact binary pair under one event, participant set, line, period, course, wrapper, and settlement contract; every possible action state must map to one side, with no unmodeled push, refund, or void state.
4. De-vig each book separately with the project's existing two-way proportional method.
5. Aggregate only source-level fair probabilities using an unweighted arithmetic mean, version `golf_binary_market_consensus_mean_v1`.
6. Require target age no greater than 180 seconds, comparison age no greater than 300 seconds, and total collection skew no greater than 300 seconds.
7. Report target exclusion, raw/usable/origin counts, source pairs and probabilities, mean, dispersion, oldest age, skew, and every exclusion.

#### 3.2.2 Dormant multiway exact-outcome consensus

`golf_multiway_market_consensus_mean_v1` is a future deterministic method for a complete three-way matchup or exhaustive outright-winner field. It is documented but not implemented or active.

For every outcome `i` within one book's complete mutually exclusive outcome set:

`q_i = 1 / D_i`

`p_i = q_i / sum(q)`

The future method would normalize each book separately, then aggregate the same candidate outcome's source-level fair probabilities across at least two independent non-target pricing origins with an unweighted arithmetic mean. It must never pool raw odds across books before source-level de-vigging. Participant/outcome set, event edition, field version, wrapper, and settlement must be complete and exact at every source. A missing outcome, unresolved field member, duplicated entrant, or field-version mismatch is `OUTCOME_SET_INCOMPLETE` and cannot contribute to consensus.

Documenting this formula does not add executable math, change an existing formula, or authorize recommendation-grade use. Because the nominal structural method exists but lacks deterministic implementation and validation, a complete three-way or single-winner exhaustive field also returns `NO_VALIDATED_PROBABILITY` and `ADAPTER_PROFILE_DISABLED`. Use `PROBABILITY_METHOD_UNAVAILABLE` only when the exact payoff shape has no supported structural method, such as an unresolved co-winner/dead-heat path.

#### 3.2.3 Push and dead-heat boundaries

A tie-refund matchup or other push-capable shape requires an independently supported push probability. Its future expected-return identity is:

`EV_per_unit = p_win * D + p_push - 1`

Do not assume `p_push=0`, infer it from a two-way display, or renormalize win prices as though a push were impossible. Whole-number round totals and tie-refund matchups return `PUSH_MODEL_UNAVAILABLE`.

For a standard dead-heat Top-N payout, retain:

`h = remaining_places / tied_players`

The return depends on the tied-player count and the remaining paid places. A known settlement fraction formula is not a pre-event distribution for `h`. Standard dead-heat Top-N valuation therefore remains `PROBABILITY_METHOD_UNAVAILABLE` until a validated deterministic distribution and exact settlement implementation exist. If the rule itself is unknown or conflicting, also use `DEAD_HEAT_RULE_UNRESOLVED`.

`PROBABILITY_METHOD_UNAVAILABLE` means the exact market, payoff, or settlement shape has no supported structural probability method. `OUTCOME_SET_INCOMPLETE` means the required same-source exhaustive set is missing or mismatched. `NO_VALIDATED_PROBABILITY` means a nominal method exists but its evidence, implementation, output, or validation is not approved for use.

If FanDuel is the target, DraftKings can count as at most one non-target pricing origin; if DraftKings is the target, FanDuel can count as at most one. A second resolved independent non-target origin remains mandatory.

---

<!-- adapter-section: 4 source_compliance -->
## 4. Source and compliance policy

Source IDs resolve through `source_registry_v1` in `SPORT_ADAPTERS/source_registry.yaml`. The registry owns URLs, access/automation permission, coverage posture, review dates, pricing-origin groups, and event/season artifacts; this adapter owns the Golf facts and gates. URL health or a sportsbook listing alone clears none of them.

| source_id/class | facts or markets supplied | authority rank | access method | jurisdiction coverage | timestamp behavior | terms/license review | permitted use | current status |
|---|---|---:|---|---|---|---|---|---|
| `fanduel_mo_house_rules`, `sportsbook_target_manual_evidence` | Missouri promotion terms; golf market labels; minimum odds; standard, OddsBoost, Tourney Special, tie, dead-heat, DNS/WD/DQ, and settlement terms | 1 for FanDuel target display/rules | registry-owned | FanDuel Missouri only | retain rule effective/version date when visible, capture time, local UTC retrieval, raw label, and content hash | see registry | target identity and settlement evidence only | exact current capture required; no automated path |
| `draftkings_golf_rules`, `sportsbook_target_manual_evidence` | golf product and settlement reference; exact Missouri market/promotion terms only when separately captured | 1 for exact DraftKings display; general rules are supporting reference | registry-owned | exact displayed Missouri product only after verification | retain rule/effective date, market title, bet-slip wording, capture time, and local UTC retrieval | see registry | target identity and settlement evidence only | general rules supporting only; Missouri certification absent |
| `golf_official_event_source_pack` | organizer/tour identity, event edition, format, rounds/holes, field/alternates, tee times, course, cut, event status, WD/DQ, shortening, and official finality | 1 for competition facts | registry-owned | named competition/event only | retain publication/effective time, field/version identifier, source ID, and local UTC retrieval | see registry | competition identity and material operational facts only | event-specific source pack required |
| `pga_tour_event_operational_pages`, `pga_tour_terms_of_use` | PGA TOUR schedule, field, tee-time, leaderboard, cut, WD/DQ, and event-status reference | 1 for applicable PGA TOUR facts | registry-owned | applicable PGA TOUR-operated event | retain page/publication state and local UTC retrieval | see registry | manual operational verification only | exact event page required; no automated retrieval |
| `source_class_licensed_golf_data_provider` | event, field, tee time, status, cut, participant, course, result, or permitted odds facts | 2 | registry-owned | contract-defined tours/events/markets | provider update and local UTC timestamps retained | see registry | only facts within a separately approved license | no paid or other provider certified |
| `nws_weather_api` | U.S. venue-matched observations, forecasts, and alerts | 1 for U.S. public weather facts | registry-owned | mapped U.S. venue only | observation/forecast validity and local UTC retrieval required | see registry | operational delay/suspension gate under a versioned rule; never a probability input | venue/rule mapping required |
| `source_class_official_non_us_operational` | non-U.S. weather or venue operating status | 1 when exact authority and access terms are reviewed | registry-owned | mapped named venue | publication/validity and local UTC retrieval required | see registry | operational gate only | unverified until configured |
| `source_class_licensed_multi_book_odds_provider` | target or comparison outcome sets | 1-2 for quoted markets | registry-owned | contract-defined books and jurisdictions | provider update plus local request/capture timestamps retained | see registry | exact quotes within approved permission | no provider certified |
| `sportsbook_comparison_manual_evidence`, `source_class_permitted_sportsbook_feed` | one non-target source market | 2 | registry-owned | exact displayed book/jurisdiction only | local UTC capture required; provider time retained when present | see registry | one complete exact binary or multiway source market | origin relationship unresolved until configured |
| `source_class_secondary_reporting_lead` | possible field, withdrawal, format, course, or weather lead | 4 | registry-owned | named event/player only | publication and retrieval times required | see registry | may create future `WATCH` pending authoritative confirmation | never recommendation-grade alone |

FanDuel or DraftKings offering a tournament does not establish that the event uses individual stroke play, has a cut, uses one course, has a stable field, or fits a registered profile. Majors, PGA TOUR events, DP World Tour events, LIV events, and other organizer products may enter discovery only when the displayed market exists in Missouri; each remains blocked until its exact organizer, format, competition rules, house rules, and source permissions are resolved. Team, match-play, Stableford, skins, and other non-individual-stroke-play formats never map to this adapter.

For every source retain source ID or URL, local UTC retrieval, provider timestamps/object IDs when present, event edition, field version, exact jurisdiction, raw snapshot/content hash, and discrepancy resolution. Never automate an authenticated sportsbook page, spoof location, bypass geolocation or anti-bot controls, evade rate limits, or treat one state, organizer, tour, event edition, or house-rule version as evidence for another.

---

<!-- adapter-section: 5 signal_registry -->
## 5. Active signal registry

The shared `promo_terms`, `target_quote`, `comparison_quotes_same_line`, `market_status`, and `promo_expiration` signals retain their only authoritative ten-field definitions in `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md`. The following rows extend those signals; they do not redefine them. Every golf-specific row is a dormant pre-activation contract and authorizes contract-scenario review only.

### 5.1 Inherited shared-signal extensions

| shared_signal_id | profiles | golf-specific identity/settlement constraint | maximum-age override | reporting extension |
|---|---|---|---|---|
| `promo_terms` | all golf profiles | verify FanDuel/DraftKings Missouri, token count, market/event eligibility, boost type, stake/payout cap, exact minimum/maximum odds and whether applied pre- or post-boost, expiry, wrapper, tie/push/dead-heat, DNS/WD/DQ, shortening, void, and token-return terms | inherit; reverify at final check after activation | show every material term, odds-basis interpretation, confidence, source, and ambiguity |
| `target_quote` | all golf profiles | require exact book/jurisdiction, organizer/tour, event edition, field version, participant set, player, raw market/selection, wrapper, threshold/line, period/round/course, completion, tie/push/dead-heat, DNS/WD/DQ, shortening, settlement, status, and timestamp | inherit 180 seconds | show raw/canonical and golf-local identity, house-rule version, age/status, and unsupported AP compatibility |
| `comparison_quotes_same_line` | all golf profiles | require each source's complete exact binary pair or complete mutually exclusive outcome set as required by the profile; require identical field/participant version and settlement; apply only the approved profile method | inherit 300 seconds and 300-second skew | show target exclusion, source outcome sets, origin audit, per-source probabilities only when method is active, dispersion, ages/skew, and exclusions |
| `market_status` | all golf profiles | selected period must be pre-start and every post-change source market must be open and synchronized | inherit | show non-open state, period-start status, change time, and synchronization result |
| `promo_expiration` | all golf profiles | no additional collection path | inherit | show time remaining |

### 5.2 Golf-specific signal registry

| signal_id | market_profile | tier | source_hierarchy | refresh_trigger | maximum_age | material_change_rule | candidate_state_effect | probability_use | reporting_rule |
|---|---|---|---|---|---|---|---|---|---|
| `golf_event_identity_status` | all golf profiles | A/C | `golf_official_event_source_pack`; `source_class_licensed_golf_data_provider` | intake, field publication, T-48h, T-24h, T-90m, final check, and official status/venue change | event identity retained for run; mutable status retrieval <=600 seconds inside T-2h; latest official notice controls | organizer/tour, event edition, format, scheduled rounds/holes, venue/course set, start, delayed/suspended/postponed/canceled/shortened status, or official result policy changes | identity/format conflict, cancellation, or unresolved event state `BLOCKED`; resolvable change future `WATCH` plus synchronized refetch | none | always show exact event edition/format/status; emphasize changes and blockers |
| `golf_competition_format_cut_state` | all profiles; cut details critical for make-cut, tournament matchup, Top-N, and outright | A/C | `golf_official_event_source_pack`; `source_class_licensed_golf_data_provider` | intake, official field/rule release, before each round, cut approach/completion, and any format/cut change | current event-specific rule/version; reverify each run and after every official notice | format, rounds/holes, cut existence/stage/size/ties, multiple-cut structure, no-cut status, minimum action, or shortening rule changes | unresolved competition rule `BLOCKED`; material change future `WATCH` and synchronized refetch | none | always show rule/source version for cut-dependent profiles; change/blocker only otherwise |
| `golf_field_entry_status` | all golf profiles | A/C | `golf_official_event_source_pack`; `source_class_licensed_golf_data_provider` | field publication, every field version, alternate substitution, DNS/WD/DQ notice, T-24h, T-90m, and final check | <=3600 seconds distant; <=600 seconds inside T-2h; latest official field/status version controls | player added/removed, alternate substituted, field version changes, or player becomes DNS/WD/DQ/unknown after quotes | identity conflict `BLOCKED`; exact promo violation `INELIGIBLE`; otherwise future `WATCH` and synchronized refetch | none | show field version and candidate-relevant old/new status only |
| `golf_player_tee_time_status` | all player profiles | A/C | `golf_official_event_source_pack`; `source_class_licensed_golf_data_provider` | tee-time publication/change, daily round pairings, T-90m, T-30m, and final check | current official assignment; <=600 seconds inside T-2h; must postdate latest correction | tee time, pairing, course, tee, round assignment, start/delay status, or participant start state changes | missing/conflicting required assignment `BLOCKED` at final check; started period outside scope `BLOCKED`; resolvable change future `WATCH` and refetch | none | show exact selected-player assignment and pre-start proof; change/blocker only otherwise |
| `golf_round_course_status` | round-score total and round matchup | A/C | `golf_official_event_source_pack`; `source_class_licensed_golf_data_provider` | round board intake, assignment publication, course/tee/par change, suspension/resumption, T-90m, T-30m, final check | current exact round/course state; <=600 seconds inside T-2h; latest official correction controls | round ID/number, course, tee, par, scheduled holes, shotgun/wave assignment, suspension/resumption, or period-start state changes | mismatch or already-started period `BLOCKED`; resolvable pre-start change future `WATCH` and synchronized refetch | none | always show round/course/par/start identity for round profiles |
| `golf_market_settlement_rule_state` | all golf profiles | A/C | `fanduel_mo_house_rules`; `draftkings_golf_rules`; `sportsbook_target_manual_evidence`; `source_class_permitted_sportsbook_feed` | intake, rule/version or product-label change, market reopen, and final check | exact current house-rule/product version for captured market; reverify at final check | minimum action, cut, completion, tie, playoff, dead heat, wrapper, DNS/WD/DQ, void, official finality, or shortened-event treatment changes | unknown/conflict `BLOCKED`; clear promo violation `INELIGIBLE`; newer resolved change future `WATCH` and synchronized refetch | none | always show rule source/version and exact unresolved treatment |
| `golf_operational_weather` | all golf profiles | C | `nws_weather_api`; `source_class_official_non_us_operational`; `golf_official_event_source_pack` | early outlook, T-24h, T-6h, T-90m, T-30m, final check, and configured alert/operational change | 900 seconds inside T-2h; latest official operational notice controls | venue-matched configured state changes among `CLEAR`, `WATCH`, and `BLOCKED` for suspension, unsafe conditions, postponement, course closure, or relocation | configured future `WATCH`/`BLOCKED`; resolution requires synchronized prices; no narrative adjustment | none | report venue, validity time, rule version, and operational state only |

---

<!-- adapter-section: 6 materiality_state -->
## 6. Materiality and state rules

| rule_id | profiles | source fields / qualifying change | effective-time rule | state effect | required refetch | resolution rule | probability effect |
|---|---|---|---|---|---|---|---|
| `golf_event_state_materiality_v1` | all golf profiles | organizer/tour, event edition, format, rounds/holes, venue/course set, start, suspension, postponement, cancellation, shortening, or official correction | authoritative effective/publication time newer than any affected quote invalidates it | conflict/cancellation/unresolved state `BLOCKED`; resolvable change future `WATCH` | target, complete comparisons, market status | current authoritative event state plus synchronized post-change batch | none |
| `golf_format_cut_materiality_v1` | all golf profiles | format, cut existence/stage/size/ties, multiple cuts, no-cut status, minimum action, or shortening rule | compare current official rule/version and publication time with every affected quote | unresolved rule `BLOCKED`; change future `WATCH` | target, complete comparisons, market status | exact competition and book rule alignment plus synchronized batch | none |
| `golf_field_participant_materiality_v1` | all golf profiles | field version, addition/removal, alternate substitution, DNS, WD, DQ, entry or tee-time status change | official effective/publication/correction time newer than a quote invalidates it | identity conflict `BLOCKED`; exact promo violation `INELIGIBLE`; otherwise future `WATCH` | target, complete comparisons, market status | current field/player/tee-time state and synchronized batch | none |
| `golf_round_course_materiality_v1` | round-score total and round matchup | round ID/number, course, tee, par, holes, pairing, start, suspension, or resumption changes | latest official assignment/correction time compared with affected quotes | mismatch/already started `BLOCKED`; resolvable pre-start change future `WATCH` | target, complete comparisons, market status | exact pre-start round/course identity plus synchronized batch | none |
| `golf_settlement_rule_materiality_v1` | all golf profiles | wrapper, threshold, minimum action, completion, tie/playoff/dead heat, cut, DNS/WD/DQ, shortening, void, or finality rule changes | current house-rule/product effective time and capture compared with every affected quote | unknown/conflict `BLOCKED`; clear ineligibility `INELIGIBLE`; resolved change future `WATCH` | target, complete comparisons, market status | matching exact rule/product version and synchronized batch | none |
| `golf_operational_weather_materiality_v1` | all golf profiles | configured operational state crosses `CLEAR`, `WATCH`, or `BLOCKED` or official suspension/resumption/closure/relocation occurs | latest venue-matched fact/notice time compared with affected quotes | configured `WATCH`/`BLOCKED` | target and complete comparisons after resolution | current operational state plus synchronized post-resolution batch | none |
| `golf_post_change_price_sync_v1` | all golf profiles | any target/comparison outcome predates the newest applicable material fact or a market suspends/reopens | every included quote must postdate the newest material fact and meet 180/300/300 limits | remain future `WATCH`; final missing/suspended/unsynchronized batch `BLOCKED` | target, complete comparisons, market status | synchronized open batch, valid configured consensus, and `post_material_change_synchronized=true` | none |

State resolution is fail closed:

- Lifecycle is checked before provider retrieval or candidate generation. A registered, otherwise structurally valid golf request returns `BLOCKED` with `ADAPTER_PROFILE_DISABLED` and makes no provider or sportsbook call.
- A clearly failed promotion minimum-odds, market, event-window, or expiry term is `INELIGIBLE` with the applicable promotion reason code. The disabled lifecycle remains recorded and no candidate is generated.
- Parse the exact minimum odds from each promotion. For a minimum of `-200`, `-200` is eligible and `-201` is not; for a minimum of `-100`, `-100` is eligible and `-110` is not. Apply the restriction to the exact base/post-boost basis stated by the promotion. Ambiguous basis is `PROMO_TERMS_AMBIGUOUS`.
- Any target evidence outside Missouri is `BLOCKED` with `JURISDICTION_MISMATCH`. Another jurisdiction's line or rule cannot be substituted.
- A no-cut event, ambiguous first cut, unresolved multiple-cut treatment, incomplete cut, or conflicting cut rule blocks `golf.player.make_cut` with `COMPETITION_RULE_UNRESOLVED`.
- Missing or conflicting field, participant, tee-time, round, course, format, settlement, DNS/WD/DQ, shortened-event, or official-finality identity is `BLOCKED` with the most specific identity, settlement, competition-rule, or source reason.
- A selected round or participant that has started is outside this adapter's pre-round boundary and is `BLOCKED` with `MARKET_IDENTITY_MISMATCH`. Do not reinterpret it as a live market.
- Suspended, closed, stale, unknown-status, or settlement-mismatched targets are `BLOCKED`. Excluded comparison sources can also cause `CONSENSUS_INSUFFICIENT`.
- Every material fact newer than a quote invalidates that quote. Resolution requires all included quotes to postdate the newest fact, remain open, meet 180/300/300 limits, and still satisfy the configured exact-outcome consensus.
- Tier A/C facts never add or subtract probability or ranking points. Only refreshed Tier B prices may change future valuation.

Every contract scenario or future local validation snapshot includes:

```yaml
monitoring_metadata:
  next_refresh_at: datetime | null
  next_refresh_reason: registered signal or final-check reason
  post_material_change_synchronized: boolean
```

---

<!-- adapter-section: 7 refresh_policy -->
## 7. Refresh policy

These phases define credential-free contract-scenario cadence and the evidence a future separately approved on-demand run would need. They do not install or authorize a scheduler, poller, automatic alert, closing-line job, result collector, or settlement job.

| phase_id | golf window or trigger | required refresh after activation | maximum ages | state if unavailable after activation | next refresh reason |
|---|---|---|---|---|---|
| `intake` | promotion or market intake | each token's terms; Missouri/book evidence; discovery slate; organizer/event/format; field/cut/round/course identity; target; required comparison outcome sets; rule/source pack | source/event scoped; 180/300/300 quote limits apply when valuation is attempted | material term, target, jurisdiction, competition, or settlement identity missing `BLOCKED`; incomplete comparison coverage `WATCH` | field/rule/tee-time release, source clarification, or next provider/manual refresh |
| `distant_pregame` | tournament T-7d, T-48h, and T-24h; for later-round markets, when the exact pre-round board opens | event/format, field/alternates, course, cut/minimum-action rules, participant status, early operational weather, target, and comparisons | field <=3600 seconds when used; current event-rule version; quote limits apply | `WATCH` when required future evidence is not current; fatal identity/rule conflict `BLOCKED` | next field version, organizer notice, tee-time/pairing release, or T-6h check |
| `official_release_window` | official field and alternate updates, tee-time/pairing publication, daily course/round assignment, cut/format notice, and withdrawal correction windows | current official release/version, candidate player/tee-time/round/course state, settlement terms, target, and comparisons after a material release | current official version; sport facts <=600 seconds inside T-2h; quote limits apply | missing/conflicting required release `WATCH` then final `BLOCKED` | next official release/correction or synchronized price batch |
| `material_change` | any registered field, format, cut, participant, tee-time, course, weather, suspension/resumption, shortening, or rule change | changed fact, target, complete comparison outcome sets, market status, and synchronization audit | target <=180 seconds; comparisons <=300 seconds; skew <=300 seconds; facts per registry | future `WATCH`; final unavailable/suspended synchronized batch `BLOCKED` | synchronized post-change price batch |
| `shortlist_check` | T-90m and T-30m relative to tournament start or the selected player's/round's start | shortlist eligibility/identity, event/format, field/player, tee time, exact round/course, cut/rules, operational weather, target, comparisons, and outcome-set audit | registry ages plus 180/300/300 quote limits | `WATCH` or `BLOCKED` according to failed gate | next official correction, participant start, operational update, or final sync |
| `final_sync` | immediately before human placement and before the selected period starts | promotion, Missouri jurisdiction, event/format, field/player, tee time, round/course, cut/rules, weather/operations, target, complete comparisons, settlement, market status, synchronization, and QA | every final recommendation-grade limit | any disabled, fatal, stale, missing, conflicting, incomplete, or already-started input `BLOCKED` | none; new evidence requires a new run |

While lifecycle remains disabled, every phase stops at `BLOCKED` with `ADAPTER_PROFILE_DISABLED` before any provider call. The table exists only to make later provider evidence, contract scenarios, and executable fixtures testable.

---

<!-- adapter-section: 8 tier_d_registry -->
## 8. Tier D model-only registry

All groups are `disabled_model_only`. They are not routinely fetched, scored, narrated, or used to change probability, state, or rank.

| group_id | potential profile consumers | candidate future inputs | required source permission | named model consumer | activation evidence | anti-noise boundary | lifecycle |
|---|---|---|---|---|---|---|---|
| `golf_model_player_skill_form` | all player profiles and outright | versioned strokes-gained components, scoring distribution, long-run skill, calibrated recency, health/availability uncertainty | separately licensed or expressly permitted data | none | exact-market model, leak-free history, out-of-sample result, calibration, uncertainty, and monitoring | no leaderboard rank, last-five result, hot streak, or isolated round narrative | `disabled_model_only` |
| `golf_model_course_fit` | all profiles | versioned course setup, yardage, grass/surface, hole mix, player-skill interaction, and uncertainty | separately licensed/permitted course and player data | none | same complete model evidence | no raw course-history average, “horse for course,” or tiny event sample | `disabled_model_only` |
| `golf_model_round_wave_weather` | round total and round matchup | tee wave, venue-matched wind/precipitation/temperature, course setup, suspension risk, calibrated scoring effects | separately licensed/permitted data; NWS only within permitted U.S. operational use unless approved for the model | none | same complete model evidence | operational weather remains a separate gate; no weather edge narrative | `disabled_model_only` |
| `golf_model_cut_finish_distribution` | make cut, Top-N, outright, tournament matchup | calibrated hole/round scoring distribution, field strength, cut rule, finish-position and tie/dead-heat distributions | separately licensed/permitted event/player data | none | exact settlement-aware model, leak-free history, OOS/calibration, tie/dead-heat validation, uncertainty | no implied finish chance from rankings or anecdotal field strength | `disabled_model_only` |
| `golf_model_field_entry_uncertainty` | make cut, matchups, Top-N, outright | alternate probabilities, late-entry/withdrawal risk, participation/completion uncertainty | separately licensed/permitted status history | none | versioned consumer, calibration, and production monitoring | no rumor, social post, or injury guess as probability input | `disabled_model_only` |

PGA TOUR public-page availability is not permission for systematic model use. A future model must name an exact licensed/permitted source, fields, transformations, consumer, settlement contract, and complete activation evidence.

---

<!-- adapter-section: 9 tier_x_exclusions -->
## 9. Tier X exclusions

| excluded group | examples | reason excluded | permitted operational use |
|---|---|---|---|
| recent results and streaks | last five finishes, consecutive cuts, recent round under par, hot/cold putter | no enabled calibrated consumer; unstable and selection-biased | none |
| course-history narratives | prior winner, loves the course, event specialist, hometown familiarity | tiny and confounded samples without a named model | none |
| ranking and stat-table claims | raw world ranking, strokes-gained rank, driving-distance rank, putting rank | disabled Tier D inputs rather than active evidence | none |
| matchup and motivation stories | revenge, confidence, pressure, major pedigree, needs points, travel fatigue | narrative rather than validated input | none |
| unsupported market claims | public betting, steam, sharp money, ownership, social sentiment | unresolved provenance and no probability contract | none |
| withdrawal/injury rumors | social post, broadcast speculation, unnamed report, visible discomfort | insufficient authority for participant state | lower-authority lead may create future `WATCH` pending official confirmation |
| weather and wave stories | morning-wave advantage, wind player, rain specialist, soft-course narrative | no configured operational rule or validated model | authoritative lead may create future `WATCH` for an operational check only |
| dead-heat shortcut | assuming ties are rare, full payout, or a fixed haircut | ignores exact settlement and outcome distribution | none |
| LLM-authored adjustment | invented win/cut/finish probability, score, or ranking penalty/bonus | violates deterministic valuation boundary | none |

Tier X material cannot supply probability, rank, positive-EV language, or persuasive candidate support.

---

<!-- adapter-section: 10 provider_evidence -->
## 10. Provider evidence

No target, comparison-origin configuration, organizer feed, source permission, house-rule interpretation, or deterministic golf valuation method is certified by this document. Contract scenarios prove expected documentation behavior only. Real timestamped captures belong in provider evidence; future machine-readable inputs belong in executable fixture files backed by a test runner.

| evidence_id | profile scope | role | timing conditions required | current evidence state | certification effect |
|---|---|---|---|---|---|
| `golf_fanduel_mo_target_cross_timing` | all six profiles as offered | target | distant board, after field/tee-time/WD or format change, after suspension/reopen, and near period start | not recorded | none; all profiles remain disabled |
| `golf_draftkings_mo_target_cross_timing` | all six profiles as offered | target | same conditions with exact Missouri terms, rule version, market title, and bet-slip wording | not recorded | none; all profiles remain disabled |
| `golf_binary_comparison_origins` | binary-eligible shapes | comparison | exact complete pairs at board open, after material change, and near period start with 180/300/300 compliance | no two-origin configuration certified | none |
| `golf_multiway_outcome_sets` | three-way matchups and outright | comparison/method | complete same-source three-way or exhaustive field sets across field versions and timing conditions | deterministic method and live evidence absent | none |
| `golf_top_n_wrapper_dead_heat` | Top-N | identity/settlement/method | standard, including-ties, OddsBoost, and Tourney Special examples with exact tie/dead-heat/minimum-action rules | not recorded | none |
| `golf_competition_context_cross_timing` | all profiles | sport facts | event/format/field release, alternate substitution, tee-time change, cut/no-cut/multiple-cut, WD/DQ, course reassignment, suspension/resumption, shortening, and official correction | not recorded | none |
| `golf_source_permission_review` | all profiles | compliance | each organizer/provider/source class and intended wagering-related use | no provider or organizer automation approved | none |
| `golf_schema_evolution` | all profiles | canonical identity/output | tournament event, field/participant version, profile-specific identity, and complete source-level outcome vectors represented without overloading team-event or single-outcome fields | not designed or approved | mandatory blocker for any lifecycle activation |

Each target capture must agree with timestamped user-visible evidence on book, Missouri jurisdiction, organizer/tour, event edition, field version, participant set, player, market/selection, wrapper, line/threshold, period/round/course, price, status, minimum action, cut, tie/push/dead heat, DNS/WD/DQ, shortening, void, and settlement. A price difference is explainable only when timestamps prove market movement rather than identity failure.

Each comparison source must provide its own complete required outcome set and resolved pricing-origin identity. Retain capture start/end times, provider time when present, local UTC retrieval, raw snapshot/hash, field/outcome membership, source-level exclusions, and discrepancy resolution. Validate stale, suspended, duplicated, one-sided, incomplete-field, wrong-wrapper, wrong-round/course, schema-change, provider-failure, and post-material-change behavior.

Promotion to `pilot_enabled` requires separately reviewed canonical-schema and decision-brief evolution, a verified per-run screenshot/manual or approved feed path, exact Missouri house rules, approved source permissions, deterministic method implementation and tests for the exact profile, two independent non-target origins, complete credential-free recorded evidence, synchronized governing documents, and separate explicit approval.

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

These Markdown rows are synthetic contract scenarios, not provider evidence, executable fixtures, or claims about a current FanDuel, DraftKings, organizer, or provider market. The structural column records future behavior after activation; the current outcome remains controlling. Every otherwise structurally valid case is `BLOCKED` with `ADAPTER_PROFILE_DISABLED` and performs no recommendation-grade calculation.

### 11.1 Lifecycle, promotion, and jurisdiction scenarios

| scenario_id | credential-free input condition | structural expectation | current required outcome |
|---|---|---|---|
| `golf_valid_registered_profile_disabled` | exact registered profile and identity; current Missouri target; required complete outcome sets and context otherwise pass | future exact-profile gates would pass | `BLOCKED` with `ADAPTER_PROFILE_DISABLED`; no probability, EV, rank, alert, candidate, or provider call |
| `golf_min_minus_200_boundary` | promotion minimum odds `-200`; target price exactly `-200` | eligible boundary | `BLOCKED` with `ADAPTER_PROFILE_DISABLED` after recording boundary pass |
| `golf_min_minus_200_fail` | promotion minimum odds `-200`; target price `-201` | promotion ineligible | `INELIGIBLE` with `PROMO_MIN_ODDS_FAIL` and `ADAPTER_PROFILE_DISABLED`; lifecycle remains disabled; no candidate |
| `golf_min_minus_100_boundary` | promotion minimum odds `-100`; target price exactly `-100` | eligible boundary | `BLOCKED` with `ADAPTER_PROFILE_DISABLED` after recording boundary pass |
| `golf_min_minus_100_fail` | promotion minimum odds `-100`; target price `-110` | promotion ineligible | `INELIGIBLE` with `PROMO_MIN_ODDS_FAIL` and `ADAPTER_PROFILE_DISABLED`; lifecycle remains disabled; no candidate |
| `golf_min_odds_basis_ambiguous` | token does not establish whether restriction applies to base or boosted odds | cannot establish eligibility | `BLOCKED` with `PROMO_TERMS_AMBIGUOUS` and `ADAPTER_PROFILE_DISABLED` |
| `golf_jurisdiction_mismatch` | target screen/feed is not proven Missouri | target cannot be substituted | `BLOCKED` with `JURISDICTION_MISMATCH` and `ADAPTER_PROFILE_DISABLED` |
| `golf_non_stroke_play_event` | offered event is team, match play, Stableford, or skins | outside adapter format | `BLOCKED` with `MARKET_IDENTITY_MISMATCH` and `ADAPTER_PROFILE_DISABLED` |

### 11.2 Make-cut and round-total scenarios

| scenario_id | credential-free input condition | structural expectation | current required outcome |
|---|---|---|---|
| `golf_make_cut_complete_pair` | exact player/event/first cut; verified cut exists; complete Yes/No pair; every action state maps to Yes or No with no refund/void outcome | binary identity would pass after activation | `BLOCKED` with `ADAPTER_PROFILE_DISABLED` |
| `golf_make_cut_no_cut_event` | competition officially has no cut | registered make-cut identity unavailable | `BLOCKED` with `COMPETITION_RULE_UNRESOLVED` and `ADAPTER_PROFILE_DISABLED` |
| `golf_make_cut_multiple_cut_exact` | event has multiple cuts; target/book/competition all explicitly identify the same first official cut | exact first-cut identity would pass | `BLOCKED` with `ADAPTER_PROFILE_DISABLED`; preserve every cut-stage field |
| `golf_make_cut_multiple_cut_ambiguous` | event has multiple cuts but market does not identify which | cannot map cut stage | `BLOCKED` with `COMPETITION_RULE_UNRESOLVED`, `MARKET_IDENTITY_MISMATCH`, and `ADAPTER_PROFILE_DISABLED` |
| `golf_make_cut_incomplete_or_shortened` | first cut is incomplete, removed, or changed by shortening and book treatment is unresolved | settlement cannot clear | `BLOCKED` with `COMPETITION_RULE_UNRESOLVED`, `SETTLEMENT_RULE_MISMATCH`, and `ADAPTER_PROFILE_DISABLED` |
| `golf_make_cut_wd_dq_timing_exact` | book rule separately proves WD and DQ treatment before versus after the cut, timestamps are exact, and every state maps to Yes or No | binary settlement identity could pass after activation | `BLOCKED` with `ADAPTER_PROFILE_DISABLED`; audit WD/DQ time, cut time, and rule |
| `golf_make_cut_wd_dq_refund_state` | exact WD or DQ rule returns stake rather than settling Yes or No | binary set is not exhaustive for expected return | `BLOCKED` with `PUSH_MODEL_UNAVAILABLE` and `ADAPTER_PROFILE_DISABLED` |
| `golf_make_cut_wd_dq_timing_unknown` | WD or DQ occurred but timing or treatment is unknown | settlement unresolved | `BLOCKED` with `SETTLEMENT_RULE_MISMATCH` and `ADAPTER_PROFILE_DISABLED` |
| `golf_round_total_half_point` | exact player, round, course, 18 holes, `Over/Under 70.5`, period not started, exact completion rules, and no refund/void outcome outside the pair | binary identity would pass after activation | `BLOCKED` with `ADAPTER_PROFILE_DISABLED` |
| `golf_round_total_whole_number` | exact `Over/Under 70` | push possible | `BLOCKED` with `PUSH_MODEL_UNAVAILABLE` and `ADAPTER_PROFILE_DISABLED` |
| `golf_round_total_wrong_round_course` | target is Round 2/course A; comparison is Round 3 or course B | identity mismatch | `BLOCKED` with `MARKET_IDENTITY_MISMATCH` and `ADAPTER_PROFILE_DISABLED` |
| `golf_round_total_par_change` | official par/course assignment changes after quotes | batch invalid; future `WATCH` and refetch | `BLOCKED` with `MATERIAL_CONTEXT_NEWER_THAN_QUOTES` and `ADAPTER_PROFILE_DISABLED`; synchronization false |
| `golf_round_total_refund_exact` | exact completion rule refunds an incomplete round rather than settling Over or Under | binary pair is not exhaustive for expected return | `BLOCKED` with `PUSH_MODEL_UNAVAILABLE` and `ADAPTER_PROFILE_DISABLED` |
| `golf_round_total_incomplete_round` | player does not complete 18 holes and exact book treatment is missing | completion settlement unresolved | `BLOCKED` with `SETTLEMENT_RULE_MISMATCH` and `ADAPTER_PROFILE_DISABLED` |
| `golf_round_period_started` | selected player has teed off before target capture | outside pre-round boundary | `BLOCKED` with `MARKET_IDENTITY_MISMATCH` and `ADAPTER_PROFILE_DISABLED` |

### 11.3 Matchup scenarios

| scenario_id | credential-free input condition | structural expectation | current required outcome |
|---|---|---|---|
| `golf_round_matchup_binary_no_push` | exact two players/round/course; verified exhaustive two-outcome rule; complete pair; no push, refund, or void outcome | binary method could apply after activation | `BLOCKED` with `ADAPTER_PROFILE_DISABLED` |
| `golf_round_matchup_tie_refund` | exact two-way matchup refunds a tied score | push probability required | `BLOCKED` with `PUSH_MODEL_UNAVAILABLE` and `ADAPTER_PROFILE_DISABLED` |
| `golf_round_matchup_three_way_complete` | exact Player A / Player B / Tie set from each source | future multiway identity is complete | `BLOCKED` with `NO_VALIDATED_PROBABILITY` and `ADAPTER_PROFILE_DISABLED` until multiway implementation and validation |
| `golf_round_matchup_missing_tie` | three-way product omits the tie outcome at a comparison source | source outcome set incomplete | `BLOCKED` with `OUTCOME_SET_INCOMPLETE`, `CONSENSUS_INSUFFICIENT`, and `ADAPTER_PROFILE_DISABLED` |
| `golf_tournament_matchup_exact` | exact two players/event/period; cut, completion, tie, WD/DQ, and shortening rules match; exhaustive no-push/no-refund pair | binary identity would pass after activation | `BLOCKED` with `ADAPTER_PROFILE_DISABLED` |
| `golf_matchup_round_vs_tournament` | target is one round; comparison is whole tournament | periods differ | `BLOCKED` with `MARKET_IDENTITY_MISMATCH` and `ADAPTER_PROFILE_DISABLED` |
| `golf_matchup_participant_mismatch` | one comparison replaces either player or uses a group market | participant set differs | `BLOCKED` with `MARKET_IDENTITY_MISMATCH` and `ADAPTER_PROFILE_DISABLED` |
| `golf_tournament_matchup_both_miss_cut_winner_exact` | both miss cut and exact book rule deterministically selects one player using the same measurement, with no void/refund state | exhaustive binary settlement could pass after activation | `BLOCKED` with `ADAPTER_PROFILE_DISABLED` |
| `golf_tournament_matchup_both_miss_cut_void_exact` | both miss cut and exact book rule voids/refunds the matchup | binary pair is not exhaustive for expected return | `BLOCKED` with `PUSH_MODEL_UNAVAILABLE` and `ADAPTER_PROFILE_DISABLED` |
| `golf_tournament_matchup_both_miss_cut_unknown` | both miss cut but winner/void rule is absent or conflicts | settlement unresolved | `BLOCKED` with `SETTLEMENT_RULE_MISMATCH` and `ADAPTER_PROFILE_DISABLED` |
| `golf_matchup_wd_dq_timing` | one player WD/DQ timing changes settlement and exact timing/rule is unavailable | settlement unresolved | `BLOCKED` with `SETTLEMENT_RULE_MISMATCH` and `ADAPTER_PROFILE_DISABLED` |

### 11.4 Top-N and outright scenarios

| scenario_id | credential-free input condition | structural expectation | current required outcome |
|---|---|---|---|
| `golf_top_n_thresholds_exact` | for each `N` in `{5, 10, 20}`, target and comparisons all use that exact N for the same player/event/wrapper | every registered threshold identity passes independently | `BLOCKED` with `ADAPTER_PROFILE_DISABLED` for Top 5, Top 10, and Top 20 |
| `golf_top_n_threshold_mismatch` | target Top 10; comparison Top 5 or Top 20 | nearby threshold is not equivalent | `BLOCKED` with `MARKET_IDENTITY_MISMATCH` and `ADAPTER_PROFILE_DISABLED` |
| `golf_top_n_standard_dead_heat_known` | standard dead-heat rule is exact but future distribution of payout fraction is unavailable | identity known; valuation method unavailable | `BLOCKED` with `PROBABILITY_METHOD_UNAVAILABLE` and `ADAPTER_PROFILE_DISABLED` |
| `golf_top_n_dead_heat_rule_unknown` | standard Top-N treatment is missing or conflicting | settlement and method unavailable | `BLOCKED` with `DEAD_HEAT_RULE_UNRESOLVED`, `PROBABILITY_METHOD_UNAVAILABLE`, and `ADAPTER_PROFILE_DISABLED` |
| `golf_top_n_including_ties_yes_no` | exact full-pay including-ties wrapper, complete Yes/No pair at each source, and every action state maps to one side with no refund/void outcome | binary shape could pass after activation | `BLOCKED` with `ADAPTER_PROFILE_DISABLED`; raw wrapper preserved |
| `golf_top_n_fanduel_special_exact` | exact OddsBoost or Tourney Special market and full-win boundary are captured with matching comparisons | distinct wrapper identity could pass | `BLOCKED` with `ADAPTER_PROFILE_DISABLED`; do not normalize to standard |
| `golf_top_n_wrapper_conflation` | standard target compared with including-ties, OddsBoost, or Tourney Special | settlement products differ | `BLOCKED` with `SETTLEMENT_RULE_MISMATCH` and `ADAPTER_PROFILE_DISABLED` |
| `golf_top_n_one_sided` | comparison source shows only player Yes price | no complete complementary market | `BLOCKED` with `OUTCOME_SET_INCOMPLETE`, `CONSENSUS_INSUFFICIENT`, and `ADAPTER_PROFILE_DISABLED` |
| `golf_outright_complete_field` | every official entrant in one field version appears once in each source; exact single-winner settlement | future multiway identity complete | `BLOCKED` with `NO_VALIDATED_PROBABILITY` and `ADAPTER_PROFILE_DISABLED` until deterministic implementation and validation |
| `golf_outright_incomplete_field` | one or more entrants missing or duplicated | exhaustive set absent | `BLOCKED` with `OUTCOME_SET_INCOMPLETE` and `ADAPTER_PROFILE_DISABLED` |
| `golf_outright_field_version_change` | alternate replaces withdrawn player after quotes | old outcome sets invalid; future `WATCH` and refetch | `BLOCKED` with `MATERIAL_CONTEXT_NEWER_THAN_QUOTES`, `OUTCOME_SET_INCOMPLETE` when old set remains, and `ADAPTER_PROFILE_DISABLED` |
| `golf_outright_dns_all_in_exact` | exact all-in/DNS treatment and field version are verified | structural settlement could pass | `BLOCKED` with `ADAPTER_PROFILE_DISABLED` |
| `golf_outright_dns_all_in_unknown` | player DNS and book treatment is absent/conflicting | settlement unresolved | `BLOCKED` with `SETTLEMENT_RULE_MISMATCH` and `ADAPTER_PROFILE_DISABLED` |
| `golf_outright_playoff_single_winner` | official playoff produces one winner and every source uses exact matching playoff rules | future outcome identity resolves to one winner | `BLOCKED` with `NO_VALIDATED_PROBABILITY` and `ADAPTER_PROFILE_DISABLED` until the nominal multiway method is implemented and validated |
| `golf_outright_cowinner_dead_heat` | official/book path can produce co-winner or dead-heat adjustment and rule/method is unresolved | settlement/valuation unavailable | `BLOCKED` with `DEAD_HEAT_RULE_UNRESOLVED`, `PROBABILITY_METHOD_UNAVAILABLE`, and `ADAPTER_PROFILE_DISABLED` |
| `golf_shortened_event_exact` | event is shortened; exact competition finality and book minimum-action/settlement match | future structural settlement may resolve after synchronized prices | `BLOCKED` with `ADAPTER_PROFILE_DISABLED`; record shortening and synchronization audit |
| `golf_shortened_event_unknown` | event shortened but minimum action or official finality is unresolved | competition/settlement cannot clear | `BLOCKED` with `COMPETITION_RULE_UNRESOLVED`, `SETTLEMENT_RULE_MISMATCH`, and `ADAPTER_PROFILE_DISABLED` |

### 11.5 Consensus, freshness, material-change, and exclusion scenarios

| scenario_id | credential-free input condition | structural expectation | current required outcome |
|---|---|---|---|
| `golf_target_excluded_two_origins` | target also exposes complete set; two other exact complete sources come from origins A/B | exclude target; de-vig each non-target source separately | `BLOCKED` with `ADAPTER_PROFILE_DISABLED`; audit counts, sets, origins, and exclusions |
| `golf_only_one_comparison_origin` | FanDuel target plus DraftKings as only usable comparison, or inverse | consensus invalid; break-even only after activation | `BLOCKED` with `CONSENSUS_INSUFFICIENT` and `ADAPTER_PROFILE_DISABLED` |
| `golf_duplicate_or_unresolved_origin` | two records share an underlying origin or independence is unknown | count duplicate once; unresolved source excluded | `BLOCKED` with `PRICING_ORIGIN_UNRESOLVED`, `CONSENSUS_INSUFFICIENT` when applicable, and `ADAPTER_PROFILE_DISABLED` |
| `golf_stale_target` | target age exceeds 180 seconds | target unusable | `BLOCKED` with `TARGET_QUOTE_STALE` and `ADAPTER_PROFILE_DISABLED` |
| `golf_stale_or_suspended_comparison` | comparison exceeds 300 seconds or is suspended/closed | exclude source; coverage may fail | `BLOCKED` with `COMPARISON_QUOTE_STALE` or `MARKET_SUSPENDED`, `CONSENSUS_INSUFFICIENT` when applicable, and `ADAPTER_PROFILE_DISABLED` |
| `golf_collection_skew` | included retrieval timestamps span over 300 seconds | batch invalid | `BLOCKED` with `QUOTE_BATCH_UNSYNCHRONIZED` and `ADAPTER_PROFILE_DISABLED` |
| `golf_settlement_mismatch` | any source differs on cut, round/course, wrapper, push, tie/dead heat, DNS/WD/DQ, shortening, minimum action, or finality | mismatched source excluded | `BLOCKED` with `SETTLEMENT_RULE_MISMATCH`, `CONSENSUS_INSUFFICIENT` when applicable, and `ADAPTER_PROFILE_DISABLED` |
| `golf_material_change_after_quotes` | field, tee time, course, cut, WD/DQ, suspension, shortening, weather operation, or rule fact postdates quotes | future `WATCH`; invalidate and refetch synchronously | `BLOCKED` with `MATERIAL_CONTEXT_NEWER_THAN_QUOTES` and `ADAPTER_PROFILE_DISABLED`; synchronization false |
| `golf_post_change_sync_valid_disabled` | all open target/comparison sets postdate newest material fact and meet 180/300/300 | clear only future synchronization blocker | `BLOCKED` with `ADAPTER_PROFILE_DISABLED`; synchronization true; no EV/rank |
| `golf_operational_weather_unresolved` | configured venue rule is `WATCH`/`BLOCKED` or event is suspended and resolution is missing | future state follows configured operational gate | `BLOCKED` with `WEATHER_RISK_UNRESOLVED` or event-state reason plus `ADAPTER_PROFILE_DISABLED` |
| `golf_tier_d_or_x_supplied` | recent form, course history, ranking, strokes-gained table, weather story, sharp claim, or LLM adjustment supplied | ignore; no probability/state/rank effect | `BLOCKED` with `ADAPTER_PROFILE_DISABLED`; audit that excluded material was not consumed |
| `golf_unregistered_market` | first-round leader, 3-ball, each-way, match play, live, parlay, or other absent profile | no catalog mapping | `BLOCKED` with `ADAPTER_PROFILE_DISABLED` and exact catalog-absence note |

---

<!-- adapter-section: 12 run_decision_brief -->
## 12. On-demand run and decision-brief contract

### 12.1 Required inputs after a separately approved lifecycle change

- A separately reviewed canonical schema and versioned decision-brief contract that can represent tournament events, field/participant versions, profile-specific identities, and complete source-level outcome vectors without overloading the current team-event or single-outcome fields.
- Original promotion text or screenshot, including FanDuel or DraftKings, Missouri jurisdiction, token count, boost type, stake/payout cap, exact odds range and basis, expiry, eligible events/markets, wrapper, push/tie/dead-heat, DNS/WD/DQ, cancellation, shortening, void, and token-return rules.
- Exact target-book evidence for every candidate with all golf-local identity and house-rule fields.
- At least two complete exact non-target source markets from two resolved pricing origins, using the binary pair or mutually exclusive outcome set required by the profile.
- Current authoritative organizer/event/format, field/player, tee-time, round/course, cut/minimum-action, settlement, operational-weather, and post-change synchronization facts.
- User risk limits when future expected-dollar or exposure ranking depends on them.

Parse multiple tokens separately unless every material term is proven identical. Evaluate the complete eligible slate rather than the first visible golfer. Rank only after an exact profile is separately activated and every deterministic/source gate passes. Return fewer uses when fewer candidates qualify, and never lower a gate to use a token.

### 12.2 Required current behavior

For a request selecting this adapter now:

1. Parse only enough user-supplied evidence to identify the requested profile, jurisdiction, and obvious structural blockers.
2. Do not call a provider, visit or automate a sportsbook, retrieve a live board, generate a candidate, calculate recommendation-grade probability/EV, schedule work, or send an alert.
3. For a registered and otherwise structurally valid profile, return `BLOCKED` with `ADAPTER_PROFILE_DISABLED`.
4. Add `PUSH_MODEL_UNAVAILABLE`, `PROBABILITY_METHOD_UNAVAILABLE`, `NO_VALIDATED_PROBABILITY`, `OUTCOME_SET_INCOMPLETE`, `DEAD_HEAT_RULE_UNRESOLVED`, `COMPETITION_RULE_UNRESOLVED`, `MARKET_IDENTITY_MISMATCH`, or `SETTLEMENT_RULE_MISMATCH` when supplied evidence independently proves that blocker.
5. Return `INELIGIBLE` only when an exact promotion term clearly fails; retain the disabled lifecycle audit.
6. Preserve supplied raw labels, golf-local identity, lifecycle, blocker, next refresh condition, and human boundary in a local documentation/evidence snapshot only when the user explicitly asks to save one.

### 12.3 Required future output after schema evolution

Only after both separately reviewed schema evolution and separate profile activation, use the then-approved versioned decision-brief contract while preserving the existing `promotion_decision_brief_v2` fields for compatibility. The evolved contract must canonically carry:

- adapter/profile/version/lifecycle and exact raw/canonical golf identity;
- organizer/tour, event edition/format, field version, participant/outcome set, round/course/cut, and pre-start audit;
- Missouri book/rule version, wrapper, minimum-action, DNS/WD/DQ, tie/playoff/dead heat, shortening, void, and official-finality verification;
- target exclusion and comparison-origin/outcome-set audit;
- quote ages, skew, post-material-change synchronization, and every source exclusion;
- exact disabled/unresolved blocker and next refresh trigger;
- meaningful passes and opportunity-cost explanation; and
- “This report identifies candidates for human review; it has not placed or confirmed a wager.”

Save only a local research/evidence snapshot. Do not call or write to AP Frankenstein and do not infer that a researched candidate became a wager.

### 12.4 Reusable task prompt

```text
Evaluate the supplied Missouri golf promotion request against adapter golf.pregame_stroke_play_v0_1 version 0.1.1 and adapter_contract_v1.

First apply profile lifecycle. All six registered profiles are disabled_provider_validation. Return BLOCKED with ADAPTER_PROFILE_DISABLED for every otherwise structurally valid shape. Do not call a provider or sportsbook, generate a candidate, calculate recommendation-grade probability or EV, schedule monitoring, or send an alert. Preserve supplied raw labels and identify every additional structural blocker.

The registered shapes are exact first-cut Yes/No, exact half-point 18-hole round score total, exact two-player round matchup, exact two-player tournament matchup, exact Top 5/10/20, and exhaustive outright winner. Keep binary, three-way, tie-refund, standard dead-heat, including-ties, OddsBoost, and Tourney Special products distinct. Whole-number totals and tie-refund matchups require PUSH_MODEL_UNAVAILABLE. Incomplete multiway sets require OUTCOME_SET_INCOMPLETE. A complete three-way or single-winner exhaustive field with a nominal but unimplemented method requires NO_VALIDATED_PROBABILITY; an unsupported dead-heat or other payoff shape requires PROBABILITY_METHOD_UNAVAILABLE.

If later separately approved schema evolution and a lifecycle change permit a supervised run, verify the exact FanDuel or DraftKings Missouri promotion and odds basis; organizer/event/format/field/participant/round/course/cut/wrapper identity; settlement and completion rules; current target; and two fresh complete exact source markets from independent non-target pricing origins. Exclude the target and use only the profile's approved deterministic method with 180/300/300-second limits.

Apply only registered event, competition/cut, field/player, tee-time, round/course, settlement, operational-weather, and post-change synchronization gates. Any material fact newer than prices invalidates the batch. Never create a narrative probability adjustment or use Tier D/X information.

For the current disabled phase, preserve existing `promotion_decision_brief_v2` fields and keep complete Golf vectors explicitly adapter-local; do not claim canonical schema support. A future enabled run must use the separately approved evolved output contract with lifecycle, canonical Golf identity, sources, timestamps, origin/outcome exclusions, settlement audit, blockers, next refresh condition, and the human-decision boundary. Never place or confirm a wager and make no AP Frankenstein call or write.
```

---

<!-- adapter-section: 13 activation_change_log -->
## 13. Activation checklist and change log

- [x] Adapter metadata declares `adapter_contract_v1` and version `0.1.1`.
- [x] Exactly six profiles use the closed lifecycle value `disabled_provider_validation`.
- [x] Raw/canonical/golf-local identity, settlement variants, and unavailable adjacent shapes are explicit.
- [x] Binary, multiway, push, and dead-heat boundaries fail closed without activating an engine.
- [x] Shared signals are extended by reference and every golf-specific Tier A/C signal has all ten contract fields.
- [x] Materiality, synchronization, six refresh phases, Tier D, Tier X, provider evidence, contract scenarios, and run contracts are documented.
- [x] Every otherwise structurally valid contract scenario retains `ADAPTER_PROFILE_DISABLED` and prohibits candidate generation.
- [ ] Canonical event/market schemas and the versioned decision-brief contract can represent complete Golf identity, field, participant, and outcome vectors without overloading current fields.
- [ ] Exact current FanDuel and DraftKings Missouri house rules, promotion evidence, market titles, settlement behavior, and target coverage are recorded across required timing conditions.
- [ ] Two independent non-target pricing origins provide exact complete source markets under 180/300/300 limits for the selected profile.
- [ ] Organizer/event source access, terms, format, field, tee-time, cut, WD/DQ, shortening, and official-finality behavior are approved and validated.
- [ ] Binary, multiway, push-aware, and/or dead-heat deterministic calculations required by the selected profile are implemented and tested.
- [ ] Credential-free recorded evidence covers every identity, missing, stale, suspended, incomplete-set, material-change, and resolution case required by the profile.
- [x] The adapter catalog, monitoring playbook, template, `PROMO_ANALYSIS_PLAYBOOK.md`, `PROJECT_CONTEXT.md`, `AGENTS.md`, and `README.md` agree for the disabled version `0.1.1` contract.
- [ ] A separate explicit approval promotes one exact profile to `pilot_enabled` or `active`.

Unchecked items are activation blockers, not permission to infer provider coverage or run a disabled profile.

| date | adapter version | profiles affected | change | evidence/approval reference |
|---|---|---|---|---|
| 2026-07-13 | `0.1.1` | all six registered golf profiles | Normalized the document to the thirteen-section `adapter_contract_v1` structure and clarified contract scenarios versus provider evidence and executable fixtures; existing outcome-set audit fields remain controlling | documentation-structure and audit-only change; no lifecycle, probability, outcome, source, freshness, schema-activation, or provider-evidence change |
| 2026-07-13 | `0.1.0` | all six registered golf profiles | Created the Missouri multi-organizer individual-stroke-play `adapter_contract_v1` with binary/multiway/push/dead-heat boundaries, golf-local audit fields, dormant signals, six phases, provider/source policy, and inline credential-free contract scenarios | user-approved Missouri Golf Adapter Contract; no provider evidence or activation claimed |
