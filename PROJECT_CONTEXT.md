# Advantage Play Intern — Current Product Requirements

**Document status:** Authoritative current-state product specification

**Version:** 0.2.0

**Reviewed:** 2026-07-13

**Default timezone:** `America/Chicago`

## 1. Purpose and present state

Advantage Play Intern is a local, human-supervised sports-promotion research system. It acts as an attention, evidence, and calculation intern: it interprets a narrowly defined promotion, collects or accepts current evidence, applies deterministic pricing rules, and returns an auditable decision brief for the user to review.

The repository now contains a narrow **credential-free manual-input runtime** plus its offline validator and tests. The runtime performs deterministic promotion math only for `mlb.player_hits` and the three pilot-enabled WNBA full-game profiles after exact supplied evidence passes every gate. It contains no provider integration, retrieval client, scheduler, polling service, automated alert channel, statistical model, persistent database, sportsbook automation, or settlement system. Profile lifecycle still describes policy eligibility rather than source certification; `SPORT_ADAPTERS/catalog.yaml` records lifecycle, contract, implementation, and source readiness separately.

The only approved operating modes are:

- on-demand local research from current, permitted evidence;
- timestamped screenshot or structured manual entry when an approved feed is unavailable;
- deterministic calculation and a local `promotion_decision_brief_v2` result;
- a human decision after independent verification of the sportsbook screen.

Recurring schedules, background monitoring, automatic alerts, live betting, closing-line capture, wager tracking, settlement, statistical prediction models, and provider automation are not current capabilities. They remain non-authoritative ideas in `ROADMAP.md` until separately approved.

## 2. Authority and compatibility

Apply the requirements in this order:

1. `PROJECT_CONTEXT.md` owns the broad current product boundary, canonical data concepts, deterministic formulas, and human-control rules.
2. `PROMO_ANALYSIS_PLAYBOOK.md` owns promotion intake, analysis workflow, QA, reason codes, and `promotion_decision_brief_v2`.
3. `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md` owns active-profile valuation, target exclusion, comparison-origin requirements, freshness, material-change handling, and candidate-state rules. MLB authority remains in its Section 6.
4. `SPORT_ADAPTERS/catalog.yaml` is the canonical machine-readable adapter and profile catalog. `SPORT_ADAPTERS/README.md` owns catalog interpretation and adapter selection.
5. `SPORT_ADAPTERS/source_registry.yaml` owns normalized source identity, access and permission posture, coverage status, health-check method, pricing-origin identity, and season artifacts. A registered source never activates a profile or certifies a provider by itself.
6. The selected adapter owns that sport's exact market identities, settlement rules, signals, source restrictions, refresh phases, profile gates, and fixtures.
7. `SPORT_ADAPTERS/ADAPTER_TEMPLATE.md` owns structural conformance for `adapter_contract_v1`.

`ROADMAP.md` is historical and exploratory. It cannot authorize a run, source call, lifecycle change, schema migration, schedule, alert, model, integration, or deployment. When it conflicts with a governing document, ignore the roadmap.

## 3. Mission, goals, and non-goals

### 3.1 Current goals

1. Parse exact promotion terms without inventing missing values.
2. Match the request to exactly one registered profile and fail closed on ambiguous identity or settlement.
3. Accept current target and comparison evidence from permitted sources, including verified screenshots or structured manual entry.
4. Normalize sportsbooks, events, participants, markets, sides, lines, and source identities.
5. Enforce provenance, jurisdiction, freshness, pricing-origin independence, and material-change gates.
6. Calculate promotion effects, break-even probability, no-vig consensus, EV, and expected dollars deterministically.
7. Rank every eligible use of a one-time token without forcing a selection.
8. Explain candidates, passes, blockers, uncertainty, and invalidation conditions in an auditable local brief.
9. Keep the final decision and every sportsbook action under human control.

### 3.2 Non-goals and prohibited behavior

- autonomous wager placement, confirmation, or simulation of placement;
- sportsbook login automation, credential storage, or authenticated-page automation;
- bypassing geolocation, anti-bot controls, CAPTCHAs, paywalls, authentication, or rate limits;
- substituting another jurisdiction, sportsbook, event, participant, market, line, period, or settlement rule;
- inventing odds, promotion terms, availability, lineup, weather, event status, or probability;
- treating social reports, narratives, streaks, or LLM judgment as recommendation-grade probability;
- using an absent profile merely because a provider exposes a similarly named market;
- claiming guaranteed profit, certainty, or predictive value without validated evidence;
- duplicating AP Frankenstein's downstream receipt, spreadsheet, wager-tracking, or settlement ownership.

## 4. Human-control boundary

The strongest research state is **ACTIONABLE FOR REVIEW**. It is not a wagering instruction.

The user alone:

- confirms the final sportsbook display and jurisdiction;
- decides whether to act;
- chooses a stake within personal and promotion limits;
- submits or declines the wager;
- supplies a receipt to AP Frankenstein after manual placement, if desired.

Advantage Play Intern never logs in, clicks, submits, confirms, or represents that a wager was placed.

## 5. Registered capability boundary

The canonical catalog owns the registered adapters, profiles, lifecycle distribution, and readiness fields; `SPORT_ADAPTERS/README.md` presents that data for humans. Numeric totals are not maintained independently here. Only `mlb.player_hits` and the three pilot-enabled WNBA full-game profiles have `implementation_status: manual_input_runtime`; every other profile remains `documentation_only`.

| Group | Registered profiles | Lifecycle and current behavior |
|---|---|---|
| MLB | `mlb.player_hits` | `active`; pregame player hits only; manual-input runtime; on-demand evidence remains required |
| WNBA game lines | `wnba.full_game.moneyline`, `wnba.full_game.spread`, `wnba.full_game.total` | `pilot_enabled`; manual-input runtime for exact pregame full-game non-push identities; each run must independently clear every evidence gate |
| WNBA player props | `wnba.player.points`, `wnba.player.rebounds`, `wnba.player.assists`, `wnba.player.made_threes` | `disabled_provider_validation`; no candidate generation |
| NBA | `nba.full_game.moneyline`, `nba.full_game.spread`, `nba.full_game.total`, `nba.player.points` | `disabled_provider_validation`; specification and fixtures only |
| NFL | `nfl.full_game.moneyline`, `nfl.full_game.spread`, `nfl.full_game.total` | `disabled_provider_validation`; specification and fixtures only |
| Golf | `golf.player.make_cut`, `golf.player.round_score_total`, `golf.player.round_matchup`, `golf.player.tournament_matchup`, `golf.player.top_n_finish`, `golf.tournament.outright_winner` | `disabled_provider_validation`; Missouri FanDuel/DraftKings individual-stroke-play specification and manual evidence planning only |

An absent profile is unregistered and has no lifecycle. It is unavailable for selection and cannot be inferred from provider exposure. Explicitly unregistered examples include:

- NBA rebounds, assists, and made-threes;
- every NFL player prop, including passing- and rushing-yard props;
- Golf each-way, first-round leader, groups, 3-ball/4-ball, live, parlay, team, match-play, Stableford, and skins;
- soccer and World Cup concepts;
- NHL, college-sport, live-trigger, and other profiles not listed in the catalog.

Only the canonical catalog and the selected adapter can establish the exact current boundary. A sportsbook listing is discovery evidence, not profile support.

## 6. Current on-demand workflow

For each request:

1. Parse sportsbook, Missouri or other applicable jurisdiction, sport, market, promotion type, boost, stake/payout caps, odds range and basis, event window, expiry, token rules, and void/push terms.
2. Preserve raw labels and map the request to exactly one registered profile through a documented equivalence rule.
3. Stop with `BLOCKED` when the profile is disabled, identity is unresolved, required evidence is unavailable, or a fatal gate fails. Use `INELIGIBLE` when the promotion clearly excludes the candidate.
4. Build only the eligible slate supported by the selected profile.
5. Capture the exact target quote and promotion evidence with source and UTC timestamp.
6. Capture the method-required complete comparison markets from non-target pricing origins.
7. Capture only the sport facts registered by the selected adapter.
8. Normalize identities and apply jurisdiction, source, freshness, settlement, market-status, and material-change gates.
9. For the four `manual_input_runtime` profiles, calculate with the local deterministic engine after every gate passes. For all other profiles, contract scenarios and fixtures specify behavior but do not produce recommendation-grade results.
10. Rank all eligible candidates, run independent QA, and return `promotion_decision_brief_v2` with passes and blockers.
11. Save only the local research/evidence snapshot. Do not call or write to AP Frankenstein.

## 7. Source, provenance, and evidence requirements

Every material fact must retain, when applicable:

- source ID and source URL or provider object ID;
- source class, access mode, permission posture, and exact permitted use;
- local UTC retrieval or capture time and provider/publication/effective time;
- sportsbook and jurisdiction;
- event, participant, market, side, line, period, and settlement identity;
- raw snapshot reference or content hash;
- transformation and calculation version;
- discrepancy, exclusion, and manual-correction audit.

Source properties are independent:

- URL reachability does not prove permission.
- Permission does not prove exact market or jurisdiction coverage.
- Coverage does not prove freshness or identity equivalence.
- Multiple records do not prove independent pricing origins.
- A healthy source does not activate a disabled profile.

Use `SPORT_ADAPTERS/source_registry.yaml` for normalized source policy and the selected adapter for the facts required to clear a profile. Official league/team/game and government facts rank above licensed providers, sportsbook/user evidence, specialist sources, secondary reporting, and social leads. Lower-authority reports may create a review dependency but cannot clear an authoritative gate alone.

Screenshots and structured manual entries are the credential-free fallback. Preserve the original artifact locally, its hash and timestamp, the extraction, confidence per field, and any user correction. A material low-confidence field requires verification before recommendation-grade calculation.

League-owned statistical restrictions remain controlling. Operational schedule, injury, roster, transaction, competition, and status facts may be used only within the documented access posture. NWS data is an operational weather gate, never an ad hoc probability adjustment. Golf remains manual and event-specific; no paid Golf API is required or approved.

## 8. Canonical data concepts

The persisted design is not yet implemented. These objects define compatibility expectations for a future runtime; `promotion_decision_brief_v2` remains a local output contract rather than a persisted-schema migration.

### 8.1 Promotion

```yaml
promotion:
  promo_id: string
  sportsbook_id: string
  jurisdiction: string | null
  title: string
  sport_keys: [string]
  market_keys: [string]
  boost_type: profit_boost | odds_boost | payout_boost | bonus_bet | insured_bet | other
  boost_percent: number | null
  max_stake: number | null
  payout_cap: number | null
  min_american_odds: integer | null
  max_american_odds: integer | null
  odds_range_basis: base_odds | boosted_odds | unknown
  eligible_event_ids: [string] | null
  eligible_start_time_min: datetime | null
  eligible_start_time_max: datetime | null
  expires_at: datetime
  token_count: integer
  reusable: boolean
  parlay_rules: object | null
  void_push_rules: string | null
  raw_terms_source: string
  parsed_confidence: number
  verification_status: confirmed | needs_review
```

The manual runtime supports minimum/maximum odds gates only when `odds_range_basis` is explicitly `base_odds`. `boosted_odds` or `unknown` fails closed with `PROMO_TERMS_AMBIGUOUS`; the runtime never guesses which price the promotion restricts.

### 8.2 Event

```yaml
event:
  event_id: string
  sport: string
  league: string
  season: string
  start_time_utc: datetime
  home_team_id: string
  away_team_id: string
  venue_id: string
  status: scheduled | delayed | postponed | in_progress | final | canceled
  provider_ids: object
```

### 8.3 Market quote

```yaml
market_quote:
  quote_id: string
  event_id: string
  sportsbook_id: string
  jurisdiction: string | null
  market_key: string
  participant_id: string | null
  side: string
  line: number | null
  american_odds: integer
  decimal_odds: number
  status: open | suspended | closed | unknown
  retrieved_at_utc: datetime
  provider_last_update_utc: datetime | null
  source_id: string
  raw_snapshot_id: string
```

### 8.4 Context fact

```yaml
context_fact:
  fact_id: string
  event_id: string | null
  entity_id: string | null
  fact_type: string
  value: object
  status: confirmed | probable | unconfirmed | conflicting | stale
  effective_at_utc: datetime | null
  retrieved_at_utc: datetime
  source_id: string
  raw_snapshot_id: string
```

### 8.5 Candidate evaluation

```yaml
candidate_evaluation:
  evaluation_id: string
  run_id: string
  promotion_id: string
  quote_id: string
  probability_method: market_consensus | statistical_model | blended | manual
  estimated_probability: number
  probability_low: number | null
  probability_high: number | null
  base_decimal_odds: number
  boosted_decimal_odds: number
  break_even_probability: number
  ev_per_unit: number
  expected_dollars: number
  permitted_stake: number
  data_quality_score: number
  state: actionable_for_review | watch | pass | blocked | ineligible
  reason_codes: [string]
  calculation_version: string
  created_at_utc: datetime
```

Only `market_consensus` is enabled by current analytical policy. Other enum values are compatibility reservations and require separate activation. The current event and quote shapes are team-event and single-outcome oriented. Golf field, participant-set, event-edition, cut, course/round, and complete outcome-vector fields remain adapter-local audit annotations; Golf activation requires separately reviewed canonical schema evolution.

## 9. Entity resolution and missing data

Prefer stable provider IDs. Name matching is a fallback and must account for punctuation, accents, initials, suffixes, abbreviated team names, traded players, duplicate names, event-date context, and explicit market aliases.

Mapping confidence is one of:

- exact provider-ID mapping;
- verified manual mapping;
- high-confidence fuzzy match;
- ambiguous and requires review;
- unresolved.

Never merge entities solely because an LLM says they look similar. Missing inputs remain explicitly missing using states such as `confirmed`, `probable`, `unconfirmed`, `stale`, `conflicting`, `not_available`, and `manual_verification_required`.

## 10. Deterministic pricing formulas

These formulas are unchanged. Recommendation-grade arithmetic belongs to tested deterministic code, not free-form LLM calculation.

### 10.1 American odds to decimal

For positive American odds `A`:

`D = 1 + A / 100`

For negative American odds `A`:

`D = 1 + 100 / |A|`

### 10.2 Profit boost

For an `r%` profit boost:

`m = 1 + r / 100`

`D_boosted = 1 + m(D_base - 1)`

This applies only when the promotion multiplies profit. Odds boosts, payout boosts, bonus bets, insured bets, parlays, and other tokens require their own explicitly supported calculation strategy.

### 10.3 Break-even probability

`p_break_even = 1 / D_boosted`

### 10.4 Two-way no-vig probability

For opposing decimal prices `D1` and `D2` from one exact book market:

`q1 = 1 / D1`

`q2 = 1 / D2`

`p1 = q1 / (q1 + q2)`

Normalize each comparison book independently. Never combine one side from one book with the opposing side from another.

### 10.5 Expected value

`EV_per_unit = p * D - 1`

`expected_dollars = permitted_stake * EV_per_unit`

Here `D` includes returned stake and any valid promotion transformation.

### 10.6 Fail-closed mathematical boundaries

For a push-capable outcome:

`EV_per_unit = p_win * D + p_push - 1`

A two-way display does not identify `p_push`. Without an independently validated push probability, return `PUSH_MODEL_UNAVAILABLE` and do not calculate recommendation-grade EV.

For one sportsbook's mutually exclusive, collectively exhaustive multiway outcome set:

`q_i = 1 / D_i`

`p_i = q_i / sum(q_j)`

This is an inactive Golf specification. It requires one exact field version and settlement contract per book; outcomes may not be pooled across books. Standard Top-N propositions overlap and are not one multiway-normalizable field.

For a dead heat:

`h = remaining_places / tied_players`

The settlement fraction is not a pre-event distribution. Without exact rules and a validated distribution for `h`, return `DEAD_HEAT_RULE_UNRESOLVED` or `PROBABILITY_METHOD_UNAVAILABLE` and do not calculate recommendation-grade EV.

## 11. Consensus, freshness, and material change

Current fair probability is de-vigged exact-market consensus.

- Exclude the target sportsbook and every target alias from probability and comparison coverage.
- Require at least two usable non-target comparison books assigned to two resolved independent pricing-origin groups.
- Count aliases, skins, feeds, or provider records from one origin once. An unresolved origin counts zero.
- Require each source's complete method-required outcome set with matching event, participant, market, line, period, overtime, push, void, participation, and settlement identity.
- De-vig each source separately, then aggregate only source-level fair probabilities under the selected adapter's named method.
- Target quote age is at most 180 seconds, comparison quote age at most 300 seconds, and included collection skew at most 300 seconds unless a stricter adapter rule applies.
- Closed, suspended, stale, incomplete, duplicated, mismatched, or unidentified quotes do not count.
- A registered material fact newer than the affected prices invalidates the batch and requires synchronized post-change evidence.
- Injury, lineup, roster, quarterback, weather, field, cut, or other context may block, invalidate, or trigger refresh; it must not create an ad hoc probability adjustment.

When consensus fails, the brief may show the exact target price, transformed price, break-even probability, and labeled comparisons. It may not claim positive EV or `ACTIONABLE FOR REVIEW`.

## 12. Candidate states and output

Use these research states exactly:

- **ACTIONABLE FOR REVIEW** — every required gate passes and configured thresholds are met.
- **WATCH** — near threshold or waiting for a specific resolvable event or refresh.
- **PASS** — eligible but below threshold or dominated by a better token use.
- **BLOCKED** — a required material input, identity, permission, method, or lifecycle gate prevents evaluation.
- **INELIGIBLE** — promotion terms clearly exclude the candidate.

`PROMO_ANALYSIS_PLAYBOOK.md` owns the unchanged reason-code vocabulary and `promotion_decision_brief_v2`. Every brief must include run time/timezone, promotion interpretation, exact sportsbook and market, adapter/profile/version/lifecycle, raw and canonical identity, jurisdiction and settlement metadata, freshness, target exclusion, pricing origins, source-level probability audit, prices, break-even, probability method, EV and expected dollars when permitted, context state, data-quality flags, ranked candidates, passes, blockers, unresolved ambiguity, source references, next refresh condition, and the human boundary.

When no candidate qualifies, say so directly. Never force a selection.

## 13. Quality, security, and failure behavior

Before any future candidate becomes `ACTIONABLE FOR REVIEW`, independently verify:

1. sportsbook and jurisdiction;
2. event and participant;
3. market, side, line, period, and settlement;
4. quote freshness and synchronization;
5. promotion eligibility and calculation strategy;
6. probability method, source-level inputs, and target exclusion;
7. registered lineup/injury/event/competition context;
8. deterministic arithmetic and expected-dollar ranking;
9. source permission, provenance, and pricing-origin resolution;
10. absence of unresolved contradictions or fatal quality flags.

A composite data-quality score never overrides a fatal gate.

On source or provider failure, retain the last snapshot only as stale evidence, attempt only an approved fallback, and visibly return `WATCH` or `BLOCKED`. Never silently reuse old evidence as current.

Never commit credentials or personal sportsbook data. Use least privilege, respect licensing and jurisdiction, keep raw screenshots local and redacted where appropriate, and retain auditable hashes and correction records.

## 14. AP Frankenstein separation

Advantage Play Intern ends at the local research brief and evidence snapshot. It does not create a wager record, capture a receipt, write a spreadsheet, grade a bet, or settle an outcome.

After the user manually places a wager, AP Frankenstein may separately receive the user's receipt and perform its established downstream workflow. `market_identity.ap_frankenstein_compatibility` is descriptive metadata only and never authorizes a call, file write, schema bridge, or integration.

## 15. Current acceptance boundary

The current repository milestone is complete only when its documentation and offline validation can demonstrate that:

- catalog counts, lifecycle values, readiness fields, and adapter references agree;
- exact registered and absent profile boundaries are unambiguous;
- adapter contracts conform structurally without changing behavior;
- source permission, coverage, health, jurisdiction, season, and pricing-origin concepts remain distinct;
- formulas, freshness gates, state labels, reason codes, and report compatibility remain unchanged;
- disabled profiles fail closed and documentation fixtures make no live-coverage claim;
- no roadmap feature is represented as implemented or approved;
- no sportsbook, provider, deployment, scheduler, AP Frankenstein, or external side effect is required for validation.

A future manual-input runtime, provider integration, scheduler, model, or dashboard requires its own approved milestone from `ROADMAP.md` and must update the implementation-status and source-readiness records truthfully.

## 16. Product principle

Judge the system by whether it reliably identifies, validates, calculates, explains, and preserves the right evidence—not by whether it can produce a confident-sounding pick on demand.
