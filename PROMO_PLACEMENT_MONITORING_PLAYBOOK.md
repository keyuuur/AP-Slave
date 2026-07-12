# Advantage Play Intern — Promo-Placement Monitoring Playbook

**Document status:** Active operating policy  
**Prepared:** 2026-07-10  
**Default timezone:** America/Chicago  
**Stable profile:** Pregame MLB player hits  
**Experimental pilot profiles:** Pregame WNBA full-game moneyline, non-push spread, and non-push total  
**Fair-probability method:** de-vigged, same-line market consensus

---

## 1. Purpose and authority

This playbook defines which sport and market facts the Advantage Play Intern monitors, when those facts should be refreshed, what counts as a material change, and how changes affect candidate state.

The system is a **promotion-placement assistant**, not a bet-originating model. The promotion or boost is expected to supply most of the value. The system's job is to compare eligible uses of that promotion, detect stale or mismatched prices, and identify which candidates deserve human review.

Document responsibilities:

- `PROJECT_CONTEXT.md` owns the product architecture, canonical objects, deterministic math, roadmap, and broad acceptance criteria.
- `PROMO_ANALYSIS_PLAYBOOK.md` owns intake, analysis, QA, reason codes, decision-brief structure, and alert format.
- This file owns active market profiles, signal tiers, refresh rules, material-change definitions, state effects, and explicit noise exclusions.
- `SPORT_ADAPTERS/README.md` owns the sport-adapter catalog, lifecycle vocabulary, and adapter selection rules.
- For a catalog entry whose authority is delegated under `SPORT_ADAPTERS/`, the selected adapter owns that sport's market identities, sport-specific signal registry, source policy, refresh cadence, profile-level gates, and validation fixtures. It may narrow this file's global rules but may not weaken or contradict them. The established MLB player-hits registry remains in Section 6 of this file.

AP Frankenstein remains a separate downstream system. If the user manually places a wager, its existing receipt-screenshot workflow may later handle spreadsheet logging and settlement. This project makes no AP Frankenstein edits, API calls, spreadsheet writes, or new integration contract in v0.1, and it does not treat a candidate as a placed wager.

---

## 2. Active and pilot boundaries

Stable v0.1 profile:

- pregame MLB player-hit promotions.

Experimental on-demand WNBA pilot profiles:

- pregame full-game moneyline;
- pregame full-game spreads with no push probability;
- pregame full-game totals with no push probability.

Shared active behavior:

- exact target-book quotes;
- same-line comparison markets;
- de-vigged, same-line market-consensus probability;
- deterministic boost, break-even, EV, and expected-dollar calculations;
- human-reviewed decision briefs.

Disabled until a later approved phase:

- independent statistical prediction models;
- manual probability overrides;
- NBA candidate generation;
- WNBA player points, rebounds, assists, and made-threes candidate generation until provider validation passes and activation is separately approved;
- WNBA whole-number spread/total, team-total, alternate-line, combination, partial-game, and same-game-parlay profiles;
- live betting or live game-state triggers;
- automatic wager placement;
- sportsbook account automation;
- direct AP Frankenstein integration;
- automatic closing-line or settlement workflows;
- recurring schedules or background polling;
- automatic alerts or outbound notifications.

`ACTIONABLE FOR REVIEW` always means the candidate passed the research gates. It is not a wagering instruction and does not mean a wager was placed.

---

## 3. Signal inclusion test

A signal belongs in an active profile only when at least one of these is true:

1. It determines promotion, event, player, or market eligibility.
2. It determines whether an exact quote is current and comparable.
3. A change can make previously collected prices stale.
4. It changes candidate state or the next refresh time.
5. It is a Tier B market input that changes deterministic EV or ranking.
6. It is a documented input to a named, validated probability method that is currently enabled.

If a fact has no defined consumer and no state effect, do not collect it routinely and do not include it merely to make a report look comprehensive.

Tier A and Tier C facts may gate eligibility, freshness, or candidate state and may trigger price refreshes. They may not add a narrative bonus or penalty to a numeric score or rank. Numeric rank can change only because fresh Tier B valuation inputs changed or because an enabled, validated model produced a new output.

### 3.1 Signal registry contract

Every active monitored signal must define:

| Field | Meaning |
|---|---|
| `signal_id` | Stable machine-readable identifier |
| `market_profile` | Exact sport and market family that consumes the signal |
| `tier` | `A`, `B`, `C`, `D`, or `X` |
| `source_hierarchy` | Preferred and fallback source classes |
| `refresh_trigger` | Time window or event that causes retrieval |
| `maximum_age` | Oldest recommendation-grade value |
| `material_change_rule` | Exact change that matters |
| `candidate_state_effect` | `WATCH`, `BLOCKED`, `INELIGIBLE`, re-rank from Tier B valuation, or informational only |
| `probability_use` | Consensus input, model-only, or none |
| `reporting_rule` | When the fact appears in a brief or alert |

Disabled future profiles may list signal families in prose while they remain inactive. Before any such profile can poll, generate candidates, or alert, every enabled signal must be promoted into this full registry contract.

### 3.2 Signal tiers

| Tier | Name | Operational meaning |
|---|---|---|
| A | Hard gate | Exact identity, eligibility, availability, and target-quote facts. Missing or conflicting material values block action. |
| B | Market valuation | Target and same-line comparison prices used for consensus, EV, ranking, and price-threshold alerts. |
| C | Context invalidation | Confirmed sport-state changes that may make an earlier market snapshot stale. These gate state or trigger new prices; they do not directly change probability or numeric rank. |
| D | Model-only | Potential statistical features that remain disabled until a named validated model consumes them. |
| X | Excluded noise | Narratives, weak trends, or unsupported statistics that v0.1 does not collect or report as evidence. |

---

## 4. Global valuation and state rules

1. Fair probability comes from de-vigged comparison prices at the **same market and line**.
2. Never compare different thresholds as though they were identical.
3. If no valid same-line consensus exists, show the promotion's boosted price and break-even probability, but do not label the candidate positive EV or `ACTIONABLE FOR REVIEW`.
4. Never modify probability free-form because of weather, injury news, bullpen news, lineup changes, or other narratives.
5. Never apply a separate context adjustment after retrieving post-change consensus prices. That would double-count the same information.
6. A material sport fact newer than the target or comparison snapshot changes the candidate to `WATCH` and triggers synchronized target/comparison refreshes.
7. If post-change prices remain unavailable near placement time, change the candidate to `BLOCKED`.
8. A lineup or role fact is a hard gate only when the selected market profile defines it as critical. An unconfirmed MLB batting lineup remains `WATCH`; missing league-wide WNBA starting-five confirmation alone does not block a full-game WNBA market.
9. A confirmed player scratch is `INELIGIBLE` when it clearly violates the promotion or market rules; otherwise it is `BLOCKED` pending exact book treatment.
10. A candidate can become `ACTIONABLE FOR REVIEW` only when promotion eligibility, exact market identity, target price, same-line consensus, critical sport state, freshness, and QA all pass.
11. Tier A or Tier C context may never add or subtract ranking points. Any post-change re-rank must be caused by refreshed Tier B prices or an enabled, validated model.

Every candidate snapshot must record `next_refresh_at` and `next_refresh_reason`.

For the documentation pilot, represent the monitoring-only values as `monitoring_metadata.next_refresh_at`, `monitoring_metadata.next_refresh_reason`, `market_identity.raw_market_label`, `market_identity.canonical_market_key`, and `market_identity.ap_frankenstein_compatibility`. These are local decision-brief/audit annotations, not changes to the canonical persisted schemas and not an AP Frankenstein integration contract. Persisting them later requires a separately reviewed schema update; an implementation must not silently drop or conflate them.

The normalized local structured output is `promotion_decision_brief_v2` from `PROMO_ANALYSIS_PLAYBOOK.md`. It adds adapter/profile/version, raw/canonical identity, consensus-origin audit, settlement, and next-refresh metadata while retaining existing v1 fields. It does not change the canonical persisted data model.

### 4.1 Valid same-line consensus gate

This gate operationalizes the existing market-consensus method without replacing the formulas or probability contracts in `PROJECT_CONTEXT.md` and `PROMO_ANALYSIS_PLAYBOOK.md`.

For every active or pilot-enabled profile, the target sportsbook is excluded from both the fair-probability calculation and the usable comparison-source count. A valid consensus requires at least two usable comparison books assigned to two distinct pricing-origin groups in a named, versioned configuration. Multiple providers, feeds, skins, aliases, or jurisdictions representing the same underlying sportsbook or configured pricing origin count once. A source whose independence is unresolved does not satisfy the two-source actionability gate until its pricing-origin group is resolved.

A usable comparison book must provide both:

- the candidate outcome; and
- the exact opposing outcome required by the configured de-vig method.

Both outcomes must refer to the same event, participant, canonical market, threshold, and settlement rules. Raw labels may differ only where an explicit equivalence mapping exists, and every raw label must still be retained. Both quotes must be open, current, correctly identified, and within the configured collection-time limits. Never create a synthetic two-way market by pairing one book's candidate price with another book's opposing price.

De-vig each comparison book's two-sided market separately using the named, versioned method. Aggregate only the resulting source-level fair probabilities using the named, versioned aggregation method. Never aggregate raw prices or raw implied probabilities before source-level de-vigging, and never include the target book's implied or de-vigged probability in the consensus used to evaluate that target price.

A one-sided ladder such as `1+ Hits` without an exact `No Hit` or equivalent opposing quote is non-de-viggable. Do not infer the missing side from an adjacent threshold, another sportsbook, a sportsbook-margin assumption, or the complement of the displayed price. It may support target-price and boosted break-even reporting, but it does not count toward recommendation-grade consensus.

The versioned consensus configuration must define:

- eligible comparison books and provider source IDs;
- each source's pricing-origin group and duplicate or related-source treatment;
- a pilot minimum of two usable comparison books from two distinct pricing-origin groups;
- raw-to-canonical market equivalence, exact threshold matching, and settlement-rule matching;
- the source-level de-vig method and required opposing-side inputs;
- the source-level fair-probability aggregation method;
- maximum comparison-quote age; and
- maximum collection-time skew across all included quotes.

Every consensus report or audit snapshot must show:

- the target book and confirmation that it was excluded from consensus;
- raw comparison-source count;
- usable comparison-book count;
- distinct pricing-origin-group count;
- included and excluded sources with reason codes;
- each included book's two-sided inputs and source-level de-vigged probability;
- aggregation method and version;
- consensus fair probability;
- dispersion as the maximum minus minimum included source-level fair probability, in percentage points;
- oldest included comparison-quote age in seconds; and
- collection-time skew in seconds, measured from the earliest and latest included retrieval timestamps.

Closed, suspended, stale, line-mismatched, unidentified, one-sided, duplicate, or otherwise ineligible quotes do not count toward coverage. If fewer than two usable independent comparison books remain, consensus is invalid: use `WATCH` during research and `BLOCKED` at the final placement check. The brief may still show the target price, boosted price, break-even probability, and non-consensus comparisons, but it may not label the candidate positive EV or `ACTIONABLE FOR REVIEW`.

Phase 0 provider validation still determines the eligible source set, pricing-origin grouping, aggregation method, and time-skew limits. The minimum comparison coverage is no longer deferred: the pilot default is two usable comparison books from two distinct configured pricing-origin groups.

---

## 5. Shared promotion and market signals

| signal_id | market_profile | tier | source hierarchy | refresh trigger | maximum age | material change rule | candidate-state effect | probability use | reporting rule |
|---|---|---|---|---|---|---|---|---|---|
| `promo_terms` | all active profiles | A | sportsbook-originated terms or verified user evidence | intake, new terms evidence, final pre-use check | through stated expiry; reverify before use | any eligibility, cap, odds-range, market, token, or expiry change | `INELIGIBLE` or `BLOCKED` | none | always show material terms and confidence |
| `target_quote` | all active profiles | A/B | documented target-book provider; verified screenshot/manual entry fallback | every run and immediately before human placement | 180 seconds for pilot actionability | line, side, price, status, or book changes | re-rank; stale/missing becomes `BLOCKED` | target return and EV | always show price, status, source, and age |
| `comparison_quotes_same_line` | all active profiles | B | documented comparison provider(s) from configured pricing-origin groups | every run and after any material sport change | 300 seconds for pilot actionability | price, line, source set, independence, or market status changes | re-rank; invalid consensus becomes `WATCH` or `BLOCKED` | source-level de-vig followed by configured aggregation | show target exclusion, raw/usable/origin counts, included and excluded sources, per-source fair probabilities, dispersion, oldest age, and collection-time skew |
| `market_status` | all active profiles | A | target and comparison providers | every quote refresh | same as quote | open, suspended, closed, or unknown changes | suspended/closed becomes `BLOCKED` | none | report only non-open state or change |
| `promo_expiration` | all active profiles | A | verified promotion terms | every run | current | enters warning window or expires | warning or `INELIGIBLE` | none | show time remaining |

Pilot freshness limits are safety defaults, not proven optimal thresholds. Measure provider behavior before changing them, and never relax them merely to produce a recommendation.

---

## 6. Active profile: `mlb.player_hits`

### 6.1 Adapter metadata and profile registry

```yaml
adapter:
  adapter_id: mlb.player_hits_v0_1
  version: 0.1.0
  contract_version: adapter_contract_v1
  document_status: active operating policy
  sport: Baseball
  league: MLB
  default_timezone: America/Chicago
  last_reviewed: 2026-07-12
  run_mode: on_demand_local_brief
  probability_method: configured_de_vigged_same_line_market_consensus
  autonomous_wagering: false
  ap_frankenstein_integration: false
```

| profile_id | lifecycle | participant | period | allowed line shape | extra-innings treatment | probability method | current boundary |
|---|---|---|---|---|---|---|---|
| `mlb.player_hits` | `active` | player | full game | exact sportsbook player-hits threshold; recommendation-grade comparison requires a complete opposing pair at that threshold | must exactly match target and every comparison source | global configured versioned same-line consensus | pregame only |

Shared signal behavior is inherited from Section 5. MLB adds no second definition of `promo_terms`, `target_quote`, `comparison_quotes_same_line`, `market_status`, or `promo_expiration`.

| shared_signal_id | profiles | MLB-specific extension | age override | reporting extension |
|---|---|---|---|---|
| `promo_terms` | `mlb.player_hits` | verify player-hits eligibility, event window, odds range, cap, expiry, participation, void, and cancellation terms | inherit | show every material term and unresolved ambiguity |
| `target_quote` | `mlb.player_hits` | retain player, game number, raw market/selection, side, threshold, jurisdiction, participation rule, and status | inherit 180 seconds | show raw and canonical identity plus AP compatibility |
| `comparison_quotes_same_line` | `mlb.player_hits` | require exact player, event/game number, threshold, period, extra-innings, push, void, and participation match | inherit 300 seconds and configured skew | show source-level pairs, pricing-origin audit, aggregation version, dispersion, ages, and exclusions |
| `market_status` | `mlb.player_hits` | no additional collection path | inherit | show non-open or changed state only |
| `promo_expiration` | `mlb.player_hits` | no additional collection path | inherit | show time remaining |

### 6.2 Market identity and settlement contract

The canonical candidate must retain:

- sportsbook and jurisdiction;
- event and game number;
- player identity;
- raw market label;
- canonical market key;
- side and line;
- American and decimal price;
- market status;
- source and retrieval timestamp;
- AP Frankenstein compatibility state.

The normalized local evidence contract is:

```yaml
market_identity:
  sportsbook_id: string
  jurisdiction: string
  league: MLB
  event_id: string
  provider_event_id: string
  game_number: integer | null
  home_team_id: string
  away_team_id: string
  participant_id: string
  provider_participant_id: string | null
  raw_market_label: string
  raw_selection_label: string
  canonical_market_key: mlb.player_hits
  side: over | under | yes | no | other
  line: number
  period: full_game
  extra_innings_treatment: included | excluded | unknown
  push_behavior: impossible | push | unknown
  void_and_participation_rule: string | unknown
  american_odds: integer
  decimal_odds: number
  market_status: open | suspended | closed | unknown
  retrieved_at_utc: datetime
  provider_last_update_utc: datetime | null
  source_id: string
  raw_snapshot_id: string
  ap_frankenstein_compatibility: direct | equivalent_but_not_supported | unsupported
```

Preserve raw and canonical meanings separately. For example, `Over 0.5 Hits` may be mathematically equivalent to `1+ Hits`, but the raw sportsbook products must never be silently rewritten.

Use one of these compatibility labels:

- `direct` — the raw market shape matches a current AP Frankenstein canonical lane;
- `equivalent_but_not_supported` — mathematical equivalence exists, but the raw shape is not currently accepted by AP Frankenstein;
- `unsupported` — no reviewed equivalence or compatible lane exists.

Compatibility is descriptive only. It does not authorize AP Frankenstein settlement or change this project's ranking.

Approved equivalence remains conditional on exact identity and settlement:

| raw market shape | canonical profile | equivalence conditions | settlement conditions | AP compatibility | status |
|---|---|---|---|---|---|
| `Over 0.5 Hits` | `mlb.player_hits` | exact player, event/game number, threshold, period, and side | extra innings, push, participation, and void rules match | `direct` only when the reviewed AP lane accepts the raw shape | conditionally approved |
| `1+ Hits` | `mlb.player_hits` | mathematically equivalent target outcome to over 0.5 only when exact player/event/period match | extra innings, participation, and void rules match; still non-de-viggable unless an exact opposing outcome exists | preserve reviewed compatibility value | target-only unless an exact opposing pair exists |
| any nearby threshold, alternate ladder, partial-game, SGP, or live shape | none | not equivalent | not applicable | `unsupported` | blocked |

### 6.3 Probability and comparison policy

MLB inherits the global valid same-line consensus gate in Section 4.1 without weakening it. The target book is excluded; each usable non-target book must supply its own exact complete opposing pair; each book is de-vigged separately; and only source-level fair probabilities are aggregated under the configured named version. Target age remains at most 180 seconds, comparison age at most 300 seconds, and collection skew must satisfy the configured pilot limit. One-sided `1+ Hits` target ladders never count as a comparison pair by themselves.

If the aggregation configuration, pricing-origin mapping, exact opposing side, settlement match, or required freshness is missing, use `WATCH` during research and `BLOCKED` at the final placement check. Show break-even and labeled comparisons only; do not report positive EV.

### 6.4 MLB hard-gate and context registry

| signal_id | market_profile | tier | source hierarchy | refresh trigger | maximum age | material change rule | candidate-state effect | probability use | reporting rule |
|---|---|---|---|---|---|---|---|---|---|
| `mlb_game_identity` | `mlb.player_hits` | A | official MLB schedule; licensed provider | slate build and every identity conflict | event-scoped | opponent, venue, start time, or doubleheader game number differs | `BLOCKED` | none | show identity conflicts and game number |
| `mlb_game_status` | `mlb.player_hits` | A/C | official MLB game status; licensed provider | baseline, near game, and status change | 600 seconds; immediate after change | scheduled, delayed, postponed, canceled, or start-time change | delay becomes `WATCH`; unresolved postponement/cancellation becomes `BLOCKED` | none | alert only on material status change |
| `mlb_player_status` | `mlb.player_hits` | A/C | official lineup/roster source; official team confirmation | baseline, lineup window, and change event | 600 seconds; final check before placement | inactive, scratched, substituted, or role changes | `WATCH`, `BLOCKED`, or `INELIGIBLE` | none | report only candidate-relevant status |
| `mlb_starting_lineup` | `mlb.player_hits` | A/C | official MLB starting lineup; official team fallback | baseline, lineup window, confirmation, and change | 600 seconds after confirmation; must postdate latest change | unconfirmed to confirmed, player removed, or lineup amended | unconfirmed remains `WATCH`; removal blocks | none | show confirmation status and timestamp |
| `mlb_batting_slot` | `mlb.player_hits` | A/C | confirmed lineup source | with lineup refresh | same as confirmed lineup | batting slot changes | `WATCH` and refresh prices; any re-rank comes only from fresh Tier B prices | none in v0.1 | report change for shortlisted candidates |
| `mlb_opposing_starter` | `mlb.player_hits` | A/C | official probable-pitcher page; official game source | baseline, lineup window, and pitcher change | 600 seconds; must postdate latest change | starter/opener identity or handedness changes | `WATCH` until post-change prices refresh | none in v0.1 | alert on identity/handedness change |
| `mlb_roof_status` | `mlb.player_hits` | A/C | official venue/team/game source; trusted venue report fallback | baseline, T-90, T-30, and change event | 900 seconds near game | roof open/closed/unknown changes | unknown with material weather risk becomes `WATCH` or `BLOCKED` | none | report only when relevant |
| `mlb_operational_weather` | `mlb.player_hits` | A/C | NWS for U.S. venues; configured authoritative local source elsewhere | early outlook, T-90, T-30, and threshold risk | 900 seconds near game | derived gate changes among `CLEAR`, `WATCH`, and `BLOCKED` under `mlb_operational_weather_rules` | `WATCH` or `BLOCKED`; refresh prices after resolution | none | report venue, rule version, timestamp, and operational risk only |
| `mlb_material_bullpen_change` | `mlb.player_hits` | C | official transactions/status plus confirmed team reporting | confirmed candidate-relevant change only | latest confirmed change; not routinely polled | confirmed event matches `mlb_material_bullpen_rules` after the price snapshot | `WATCH` and refresh prices; no direct probability or rank adjustment | none in v0.1 | report the matched rule only when it invalidates a shortlisted snapshot |

### 6.5 MLB materiality and state rules

`mlb_operational_weather_rules` must be a versioned configuration that names the source field, operator, and value for every `WATCH`, `BLOCKED`, and resolution condition; the venue/time matching window; and roof-state handling. A new or changed official game, venue, or team operational notice may also satisfy a named rule. General forecasts or prose such as “good hitting weather” never satisfy a rule. If the configuration is missing or cannot be evaluated, a candidate at an outdoor or roof-unknown venue stays `WATCH` and becomes `BLOCKED` at the final placement check. A confirmed closed roof satisfies the external-weather gate, while roof status remains separately monitored.

`mlb_material_bullpen_rules` must be a versioned allowlist that names the affected team, player or defined bullpen role, qualifying availability or transaction event, and required confirmation source. Without a matching rule, do not collect, alert on, or narrate bullpen news. If no rules are configured, this conditional signal is disabled; it does not block a candidate. A matched post-snapshot event changes the candidate to `WATCH` only long enough to refresh Tier B prices.

These rule sets are pilot configuration, not probability inputs. Their versions must be shown whenever they create or resolve a blocker.

| rule_id | profiles | source fields / qualifying change | effective-time rule | state effect | required refetch | resolution rule | probability effect |
|---|---|---|---|---|---|---|---|
| `mlb_event_state_materiality_v1` | `mlb.player_hits` | opponent, venue, start time, game number, delay, postponement, cancellation, or status changes | compare official effective/publication time with every affected quote retrieval | identity conflict/cancellation `BLOCKED`; resolvable change `WATCH` | target and complete comparisons | current authoritative state plus synchronized post-change quotes | none |
| `mlb_lineup_starter_materiality_v1` | `mlb.player_hits` | lineup confirmation/amendment, target removal, batting-slot change, or starter/opener identity/handedness change | any qualifying fact newer than a quote invalidates that quote | `WATCH`; target removal becomes `BLOCKED` or `INELIGIBLE` under exact terms | target and complete comparisons | confirmed current lineup/starter plus synchronized post-change quotes | none |
| `mlb_roof_operational_weather_rules` | `mlb.player_hits` | configured roof, delay, postponement, or operational-weather state crosses `CLEAR`, `WATCH`, or `BLOCKED` | latest matched official/configured observation must postdate prior state and be venue/time matched | configured `WATCH` or `BLOCKED` | target and complete comparisons after resolution | current roof/operational state and post-resolution quotes | none |
| `mlb_material_bullpen_rules` | `mlb.player_hits` | allowlisted confirmed player/role availability or transaction event | only a qualifying confirmed event newer than quotes is material | `WATCH` | target and complete comparisons | current post-change price batch; no separate bullpen score | none |

Every candidate retains `monitoring_metadata.next_refresh_at` and `next_refresh_reason`. Missing, stale, conflicting, suspended, scratched, canceled, and resolved cases follow the global state rules and the fixtures in Section 6.10 below.

### 6.6 MLB source and compliance policy

Preferred source classes:

1. Official MLB starting lineups: <https://www.mlb.com/starting-lineups/>
2. Official MLB probable pitchers: <https://www.mlb.com/probable-pitchers/>
3. Official MLB transactions: <https://www.mlb.com/roster/transactions>
4. Documented or licensed sports-data provider carrying stable IDs and timestamps.
5. Official team announcement.
6. Established secondary source as an early signal only.
7. User screenshot/manual confirmation when provider coverage is missing.

For U.S. operational weather, use the National Weather Service API: <https://www.weather.gov/documentation/services-web-api>. Roof status is a separate fact and must not be inferred from weather alone.

| source class | facts supplied | authority | access mode | timestamp behavior | permitted use | current status |
|---|---|---:|---|---|---|---|
| official MLB schedule/game source | event identity, game number, venue, start and game status | 1 | public official page or permitted licensed feed | retain official/provider and local UTC retrieval times | operational identity and status | conditional approved use; reverify access terms |
| official MLB starting lineups | confirmed lineup and batting slot | 1 | public official page or permitted licensed feed | publication/confirmation and local UTC retrieval required | operational eligibility and price invalidation | conditional approved use; reverify access terms |
| official MLB probable pitchers | starter/opener identity and handedness | 1 | public official page or permitted licensed feed | source effective time and local UTC retrieval required | operational identity and price invalidation | conditional approved use; reverify access terms |
| official MLB transactions/team confirmation | roster, availability, and allowlisted bullpen changes | 1-2 | public official page/announcement or permitted licensed feed | publication/effective and local UTC retrieval required | operational eligibility and price invalidation | conditional; source-specific review required |
| NWS or configured authoritative local weather source | venue-matched operational delay/postponement risk | 1 for U.S. operational weather | documented public API or reviewed official source | observation/forecast validity and local UTC retrieval required | operational gate only | conditional approved use; rule configuration required |
| sportsbook-originated evidence | target quote and promotion terms | 1 for displayed target | permitted documented feed or timestamped screenshot/manual evidence | local UTC capture required; provider time retained when present | target identity and promotion evidence | provider-specific validation or manual fallback |
| licensed/documented odds provider or sportsbook comparison evidence | complete comparison pairs | 1-2 for quoted markets | reviewed API/feed or timestamped manual evidence | provider and local UTC timestamps required | exact market comparison within reviewed permission | provider-specific validation required |
| established secondary report | possible registered material-change lead | 4 | public report | publication and retrieval times required | may create `WATCH` pending stronger confirmation | never recommendation-grade alone |

No source in this table is a generic provider certification. Jurisdiction, permission, exact identity, timestamp behavior, and pricing-origin independence must be validated for the run or recorded provider configuration.

### 6.7 MLB refresh policy

| phase_id | MLB window/trigger | facts refreshed | maximum ages | state if unavailable | next refresh reason |
|---|---|---|---|---|---|
| `intake` | promotion detected | terms, eligible slate, target/comparisons, game identity, probable pitcher, lineup state, roof and early operational risk | source/event scoped; quote pilot limits apply | material term/target missing `BLOCKED`; context/consensus incomplete `WATCH` | T-6h or registered source event |
| `distant_pregame` | around T-6h | slate, pitcher, game status, target/comparisons, registered operational risk | quote pilot limits; sport facts per registry | `WATCH` when required evidence is unavailable | lineup/pitcher release window |
| `official_release_window` | T-4h until confirmed lineup | lineup and pitcher every 10-15 minutes when event data is unavailable; no unrelated static polling | lineup/starter 600 seconds and postdate latest change | unconfirmed lineup `WATCH`; unresolved final requirement `BLOCKED` | confirmation, amendment, or next check |
| `material_change` | any registered material event | invalidate affected quotes; refresh target, complete comparisons, and affected status facts | target 180 seconds; comparisons 300 seconds; configured skew | `WATCH`; final unavailable synchronized batch `BLOCKED` | synchronized post-change batch |
| `shortlist_check` | around T-30m | shortlist, lineup, pitcher, game/roof, operational weather, target/comparisons | registry ages and quote pilot limits | `WATCH` or `BLOCKED` under failed gate | final synchronized check |
| `final_sync` | immediately before human placement | promotion, event/player/lineup/starter/roof/weather status, target, comparisons, jurisdiction, settlement, and QA | all final recommendation-grade limits | any fatal, stale, or conflicting input `BLOCKED` | none; new evidence requires a new run |

Closing-price capture remains future evaluation work and is not active in this adapter.

If provider limits prevent the required cadence or freshness, keep the candidate `WATCH` or `BLOCKED`. Do not silently substitute older data.

### 6.8 MLB 18-group signal map and Tier D boundaries

The MLB design recognizes 18 conceptual baseball signal groups. The six active groups below summarize existing Section 6.2 registry entries; they do not create duplicate signals or additional polling. The remaining 12 groups are disabled Tier D model families.

Shared promotion and Tier B quote signals in Section 5 are separate from these baseball-specific groups. Consumer mappings beyond `mlb.player_hits` document future compatibility only; they do not activate another market profile.

#### Active gate and refresh groups

| group_id | Existing registry signals | Potential market consumers | v0.1 behavior |
|---|---|---|---|
| `mlb_event_state` | `mlb_game_identity`, `mlb_game_status` | all MLB markets | verify identity and game state; gate or refresh prices |
| `mlb_participant_availability` | `mlb_player_status` | player props; team markets only when a registered change is material | gate eligibility and refresh prices |
| `mlb_confirmed_lineup_role` | `mlb_starting_lineup`, `mlb_batting_slot` | batter props, team markets, first-inning and First Five markets | unconfirmed remains `WATCH`; confirmed changes refresh prices |
| `mlb_starting_pitcher_identity` | `mlb_opposing_starter` | all pitcher-sensitive player and team markets | starter, opener, or handedness change refreshes prices |
| `mlb_roof_and_operational_weather` | `mlb_roof_status`, `mlb_operational_weather` | all venue-affected markets | gate delay, postponement, or roof risk and refresh after resolution |
| `mlb_confirmed_bullpen_availability` | `mlb_material_bullpen_change` | full-game markets and affected player props | a registered confirmed change refreshes prices only |

These groups affect eligibility, freshness, or candidate state. They never create a manual probability adjustment or ranking bonus.

#### Disabled Tier D model families

| group_id | Potential market consumers | Allowed future inputs | Anti-noise boundary |
|---|---|---|---|
| `mlb_model_starter_workload` | pitcher strikeouts/outs, First Five, first inning, sides, and totals | projected pitches, batters faced, innings, times-through-order exposure, rest, role, and pull hazard | no conclusion from one recent pitch count, vague "short leash" commentary, or manager narrative |
| `mlb_model_batter_plate_appearances` | hits, total bases, HR, walks, batter strikeouts, runs, and RBI | confirmed slot, team plate-appearance environment, home ninth-inning probability, substitution risk, and modeled extra innings | batting slot alone is not a hit probability; do not narrate unsupported opportunity guesses |
| `mlb_model_pitcher_strikeout_command` | pitcher strikeouts/walks/outs, batter strikeouts/walks, early and full-game totals | regressed strikeout, walk, whiff, chase, zone, and called-strike measures | exclude wins, raw ERA, last-start results, and recent strikeout streaks |
| `mlb_model_pitcher_contact_suppression` | hits allowed, earned runs, batter hits/total bases/HR, and totals | regressed expected outcomes allowed, contact quality allowed, and batted-ball distribution | exclude recent ERA/BABIP narratives and small-sample matchup splits |
| `mlb_model_batter_contact_discipline` | hits, batter strikeouts, walks, and team offense | regressed strikeout, walk, contact, zone-contact, chase, and whiff measures | exclude recent batting average, last-N overs, and hot/cold streaks |
| `mlb_model_batter_batted_ball_quality` | hits, total bases, HR, and run totals | xBA, xSLG, xwOBA, barrel rate, exit-velocity, and launch-angle distributions | exclude isolated maximum exit velocity, single-game Statcast readings, and unsupported short-term spikes |
| `mlb_model_platoon_arsenal_matchup` | batter and pitcher props, first inning, First Five, and team totals | shrunk handedness splits, projected pitch mix, velocity/movement, measured stuff, and stabilized pitch-type response | exclude batter-versus-pitcher history, unshrunk platoon splits, tiny pitch samples, and "sees him well" narratives |
| `mlb_model_bullpen_projection` | full-game moneyline/run line/totals, team totals, and late-opportunity batter props | role-specific quality, availability, workload, handedness distribution, and entry probability | exclude generic bullpen ERA/rankings; never apply a confirmed availability change both manually and through refreshed prices |
| `mlb_model_outcome_park_factors` | hits, doubles, triples, HR, total bases, walks, strikeouts, and run totals | versioned, shrunk, outcome-specific park effects | exclude generic "hitter's park" labels and unstable raw single-season factors |
| `mlb_model_atmospheric_environment` | HR, total bases, and run totals; hits only if validated | venue- and game-time-matched temperature, wind vector, air density, and roof-conditioned environment | exclude "good hitting weather" prose; operational weather remains a separate gate and must not be double-counted |
| `mlb_model_defense_catcher` | hits/runs, pitcher outcomes, and stolen bases | lineup-specific fielding projection, range, framing, blocking, and throwing measures | exclude errors, fielding percentage, reputation, and tiny catcher/defender samples |
| `mlb_model_stolen_base_opportunity` | stolen-base props; runs only if validated | reach-base probability, runner attempt/speed, pitcher hold or time-to-plate, pickoff environment, and catcher throwing | exclude career stolen-base totals, generic manager aggression, and tiny runner-pitcher-catcher histories |

None of these Tier D groups may be routinely fetched, scored, narrated, used to change candidate state, or used to modify probability in v0.1. Before activation, a group must name its exact market consumer, source fields, transformations, model version, leak-free historical test, out-of-sample result, calibration result, uncertainty treatment, and monitoring rule.

Baseball Savant expected-statistics documentation is a possible source for later validated models: <https://baseballsavant.mlb.com/expected_statistics?type=batter>. Provider availability or intuitive plausibility alone is not evidence that a feature is predictive.

Every Tier D group in the table has lifecycle `disabled_model_only`, named model consumer `none`, and requires a separately licensed/permitted source plus the activation evidence stated above. Section 8 supplies the authoritative shared Tier X exclusions; the anti-noise column above adds MLB-specific examples without creating active signals.

### 6.9 MLB provider-validation evidence requirements

For every target or comparison source configuration, record timestamped evidence at board open/distant pregame, after a registered material change, and near first pitch. Evidence must verify jurisdiction, event/game number, player, raw market and selection, canonical equivalence, threshold, period, extra-innings, push, void/participation, price, status, provider object identity, and local/provider timestamps.

Each comparison origin must expose its own complete exact pair and resolved pricing-origin group. Record local request start/end, provider update time when present, raw snapshot/hash, user-visible agreement where available, exclusions, and discrepancy resolution. Provider exposure or one successful request does not certify future coverage.

### 6.10 MLB fixtures and required outcomes

| scenario | required outcome | audit evidence |
|---|---|---|
| confirmed current lineup/starter and valid synchronized consensus | deterministic EV ranking may run | adapter/profile/version, source pairs, context timestamps, and calculation version |
| lineup unconfirmed | `WATCH`; never actionable | `LINEUP_UNCONFIRMED` and next confirmation check |
| starter, lineup, slot, game, roof/weather, or allowlisted bullpen fact newer than quotes | `WATCH` and synchronized target/comparison refetch; no probability adjustment | old/new fact and quote timestamps plus matched materiality rule |
| target player scratched | `INELIGIBLE` when exact terms decide treatment; otherwise `BLOCKED` | official status and promotion/book rule |
| outdoor operational risk unresolved or roof state required but unknown | `WATCH`, becoming `BLOCKED` at final check | rule version, venue/time match, and current state |
| fewer than two usable independent exact comparison pairs | `WATCH` during research; `BLOCKED` at final check; break-even only | source and pricing-origin exclusions |
| `1+ Hits` target has no exact opposing quote | target/break-even reporting only; no consensus contribution | preserved raw label and non-de-viggable reason |
| generic trend, BvP sample, weather narrative, or bullpen ranking | ignore as Tier X | no probability, state, or rank effect |

### 6.11 MLB reusable on-demand run contract

```text
Evaluate the supplied MLB player-hits promotion using adapter mlb.player_hits_v0_1 version 0.1.0 and adapter_contract_v1.

Parse every token separately and verify the target sportsbook and jurisdiction, exact event/game number, player, raw and canonical market identity, threshold, period, extra-innings, push, void/participation, odds restrictions, cap, expiry, and market status. Preserve raw labels and AP compatibility metadata.

Use a current exact target quote and at least two fresh complete exact opposing pairs from independent non-target pricing origins. Exclude the target book, de-vig each comparison book separately, and aggregate only source-level fair probabilities under the configured named version. If consensus fails, show boosted break-even only and use WATCH/BLOCKED as required.

Retrieve only the registered MLB event/player, confirmed lineup/slot, opposing starter, roof/operational-weather, and allowlisted material-bullpen facts. Any material fact newer than prices invalidates the batch and triggers synchronized refetching. Never create a narrative probability adjustment or use disabled Tier D/X information.

Use deterministic promotion, odds, no-vig, EV, expected-dollar, freshness, and ranking calculations. Return promotion_decision_brief_v2 with sources, timestamps, exclusions, passes, blockers, next refresh condition, and the human-decision boundary. Save only a local evidence snapshot; never place or confirm a wager and make no AP Frankenstein call or write.
```

### 6.12 MLB change log

| date | adapter version | profiles affected | change | evidence/approval reference |
|---|---|---|---|---|
| 2026-07-12 | `0.1.0` | `mlb.player_hits` | Added explicit `adapter_contract_v1` metadata and normalized the existing authoritative policy without changing behavior or lifecycle | approved sport-adapter contract normalization plan |

---

## 7. Basketball profile registry

`SPORT_ADAPTERS/WNBA.md` is the authoritative WNBA capability contract. It defines exact market identities, the complete ten-field Tier A/B/C signal registry, source compliance, WNBA-specific refresh behavior, model-only and noise boundaries, provider-validation evidence, and fixtures. This section records lifecycle state only; do not duplicate or weaken the adapter's rules here.

| Profile | Status | Active boundary |
|---|---|---|
| `wnba.full_game.moneyline` | `pilot_enabled` | pregame, full game, exact overtime/settlement match |
| `wnba.full_game.spread` | `pilot_enabled` | pregame, full game, no push probability |
| `wnba.full_game.total` | `pilot_enabled` | pregame, full game, no push probability |
| `wnba.player.points` | `disabled_provider_validation` | no polling or candidate generation |
| `wnba.player.rebounds` | `disabled_provider_validation` | no polling or candidate generation |
| `wnba.player.assists` | `disabled_provider_validation` | no polling or candidate generation |
| `wnba.player.made_threes` | `disabled_provider_validation` | no polling or candidate generation |
| `nba.player_points` | `disabled_provider_validation` | future profile |
| `nba.player_rebounds` | `disabled_provider_validation` | future profile |
| `nba.player_assists` | `disabled_provider_validation` | future profile |
| `nba.player_threes` | `disabled_provider_validation` | future profile |

No disabled profile may poll sources, produce candidates, generate alerts, or become actionable. WNBA pilot profiles run only on demand and produce a local decision brief; their `pilot_enabled` state does not activate recurring schedules, background monitoring, or outbound alerts.

For WNBA game lines, a current official injury-report submission and post-change price batch are critical, while a league-wide confirmed starting five is not. Any official availability, roster, transaction, game-status, or confirmed role change newer than the quote batch changes affected candidates to `WATCH` and triggers synchronized target/comparison refreshes. The fact itself never changes probability. Exact WNBA player availability becomes a hard gate when a player-prop profile is later activated.

Whole-number spread and total lines remain disabled until deterministic push-aware fair-probability and EV math is separately implemented and tested. The binary win/loss calculation must not silently treat push probability as zero.

All WNBA statistical features remain Tier D and uncollected until a named, calibrated model, licensed/permitted source, leak-free historical evaluation, and separate activation approval exist. Game-line movement may be registered as a future player-prop refresh trigger, but it may not substitute for exact prop consensus or create a narrative adjustment.

The current official NBA injury-report entry point must be reverified by season before any NBA activation: <https://official.nba.com/nba-injury-report-2025-26-season/>. The WNBA adapter contains the current official WNBA sources and their compliance rules.

---

## 8. Explicitly excluded noise

Do not collect, score, or present these as recommendation evidence:

- hot or cold streaks;
- last-five or recent over/under records;
- batter-versus-pitcher history and tiny or unshrunk handedness, lineup, on/off, or pitch-type samples;
- isolated Statcast readings, leaderboard ranks, maximum-exit-velocity events, or short-term spikes without a named model consumer;
- pitcher wins, RBI, errors, fielding percentage, and other context-heavy counting statistics used as standalone evidence;
- revenge, motivation, birthday, milestone, homecoming, national-TV, or “must win” narratives;
- generic manager, coach, or player confidence quotes and unsupported managerial-tendency claims;
- public betting percentages or social sentiment;
- anonymous or unverified rumors;
- generic injury headlines without a confirmed availability or role change;
- unsupported “sharp money” labels;
- referee or umpire trends without an enabled validated model;
- arbitrary day-of-week or venue trends;
- generic bullpen ERA, rankings, or guessed fatigue;
- raw lineup splits without sample size and comparable personnel;
- spring-training or tiny current-season samples treated as established true talent;
- generic weather narratives;
- any probability adjustment authored by an LLM.

Secondary or social reporting may create `WATCH` only when it plausibly invalidates a candidate. It cannot create an actionable edge.

---

## 9. Local decision briefs and future alerts

The active profiles and experimental WNBA pilot produce on-demand local decision briefs only. They do not run a scheduler, background poller, automatic alert, or outbound notification. The alert contract below is reserved for a later approved phase and also defines which changes deserve emphasis when a human requests a refreshed brief.

When separately activated, generate an alert only when at least one registered event occurs:

- candidate state changes;
- ranking leader changes;
- price or break-even threshold is crossed;
- a blocker appears or resolves;
- a registered material sport fact changes;
- provider health or freshness fails;
- promotion expiration enters a configured warning window.

Deduplicate by candidate, signal, and new value. Every alert must state what changed from the previous snapshot.

The decision brief is a promotion-placement brief, not a sports-news digest. For sport context, include only:

- confirmed critical state;
- material changes since the prior snapshot;
- unresolved blockers;
- the reason for the next refresh;
- candidate-specific invalidation conditions.

Do not include Tier D or Tier X material as persuasive narrative.

---

## 10. Adding a new sport or market profile

A new profile must be registered in `SPORT_ADAPTERS/README.md` and implemented from `SPORT_ADAPTERS/ADAPTER_TEMPLATE.md`. It remains disabled until it defines:

1. exact canonical and raw market identity;
2. promotion eligibility inputs;
3. same-line fair-probability method;
4. Tier A, B, and C signals with source hierarchy;
5. freshness and material-change rules;
6. candidate-state effects;
7. explicit Tier D and Tier X boundaries;
8. event-relative refresh cadence;
9. defined missing, stale, conflicting, and material-change scenarios for `pilot_enabled`, with credential-free recorded fixtures required before `active` status;
10. report and alert language;
11. a separate approval to activate the profile.

Do not activate a profile merely because a provider exposes a field. Changing an adapter lifecycle state requires the validation evidence named by that adapter plus a consistent update to this file, the adapter catalog, `AGENTS.md`, and `README.md`.

---

## 11. Required validation scenarios

The documentation and later implementation must preserve these outcomes:

| Scenario | Required outcome |
|---|---|
| MLB lineup unconfirmed | `WATCH`; never actionable |
| Starting pitcher changes after quotes were collected | invalidate quotes, set `WATCH`, refresh target/comparisons, make no direct probability adjustment |
| Target player scratched | `BLOCKED` or `INELIGIBLE` according to exact promotion/book rules |
| Outdoor delay or postponement risk unresolved | `WATCH` or `BLOCKED` |
| Ordinary wind/temperature narrative with no enabled model | ignored for probability and ranking |
| Confirmed material bullpen change after price snapshot | refresh prices only; no manual probability adjustment |
| Same-line consensus unavailable | show break-even only; no positive-EV or actionable label |
| Target book supplies a complete two-sided market | exclude the target book from fair probability and comparison coverage |
| FanDuel target plus DraftKings as the only usable comparison | `WATCH` during research and `BLOCKED` at the final placement check; show break-even only |
| Multiple provider records represent one sportsbook or pricing origin | count the configured pricing-origin group once; duplicate records do not satisfy coverage |
| Comparison-source independence is unresolved | do not count the source toward the two-origin minimum |
| One comparison book lacks the exact opposing side | exclude it as one-sided and non-de-viggable |
| Candidate side comes from one book and opposing side from another | reject the synthetic pair; do not de-vig across books |
| `1+ Hits` has no exact `No Hit` equivalent | do not infer the missing side; no fair probability or positive-EV label |
| Two independent books supply fresh complete same-line markets | de-vig each book separately, then aggregate the source-level fair probabilities |
| A comparison quote becomes stale, suspended, mismatched, or outside the collection-time skew | exclude it; downgrade to `WATCH` or `BLOCKED` if usable coverage falls below two |
| Consensus is reported | show target exclusion, raw/usable/origin counts, source exclusions, per-source fair probabilities, dispersion, oldest age, and collection-time skew |
| Post-change prices current and all critical gates pass | allow deterministic EV calculation and normal ranking |
| `Over 0.5 Hits` versus `1+ Hits` | retain distinct raw labels plus explicit canonical equivalence and AP compatibility |
| Disabled Tier D statistic is available from a provider | do not fetch, score, narrate, or use it; provider availability does not activate a model input |
| Confirmed context change also appears in refreshed consensus prices | use the refreshed Tier B valuation only; do not apply the context fact again |
| Generic bullpen ranking, recent trend, tiny matchup split, or weather narrative is supplied | ignore it as Tier X; no probability, state, or ranking effect |
| Future MLB market has no named consumer-specific validated model | keep its Tier D groups disabled and do not generate candidates |
| WNBA full-game moneyline with exact settlement terms, fresh target quote, two independent complete comparison markets, current official availability submission, and all QA gates passing | permit normal deterministic EV ranking under the experimental on-demand pilot |
| WNBA half-point full-game spread or total with the same gates passing | permit normal deterministic EV ranking under the experimental on-demand pilot |
| WNBA whole-number spread or total | `BLOCKED`; push-aware probability and EV math are not active |
| WNBA injury report is not yet submitted by the applicable deadline | `WATCH` during research and `BLOCKED` at the final placement check |
| Official WNBA availability or roster fact is newer than the quote batch | invalidate affected quotes, set `WATCH`, refresh target/comparisons, and make no direct probability adjustment |
| WNBA starting five is not confirmed but the official availability submission and post-change game-line quotes are current | do not block solely for missing starting-five confirmation |
| FanDuel target plus DraftKings as the only usable WNBA comparison | `WATCH` during research and `BLOCKED` at the final placement check; show break-even only |
| WNBA player points, rebounds, assists, or made-threes request | `BLOCKED` with `disabled_provider_validation`; do not generate candidates |
| NBA candidate request | `BLOCKED` with a clear note that the profile is disabled |
| Live-betting request during v0.1 | `BLOCKED` with a clear note that live monitoring is deferred |

---

## 12. Final operating principle

The system should know less, but know why every collected fact matters.

Market consensus supplies the baseline. Promotions supply most of the expected opportunity. Sport context protects the analysis from stale prices, wrong identities, and changed circumstances. If a fact cannot change eligibility, freshness, state, a configured Tier B valuation, or an enabled model input, leave it out.
