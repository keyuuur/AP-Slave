# Sport Adapter Template

**Structural contract version:** `adapter_contract_v1`

Use this template for a new sport or market family. Replace every bracketed value. Delete examples that do not apply, but do not omit a required decision or silently leave it unknown.

The completed adapter is subordinate to `PROJECT_CONTEXT.md`, `PROMO_ANALYSIS_PLAYBOOK.md`, `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md`, and `SPORT_ADAPTERS/README.md`. It may narrow global policy for an exact profile; it may not weaken global consensus, freshness, provenance, source-access, deterministic-math, human-approval, or AP Frankenstein boundaries.

---

## 1. Adapter metadata

```yaml
adapter:
  adapter_id: "[sport_or_league.market_family]"
  version: "[semantic or date version]"
  contract_version: "adapter_contract_v1"
  document_status: "[draft|active operating policy]"
  sport: "[sport]"
  league: "[league]"
  default_timezone: "America/Chicago"
  last_reviewed: "[YYYY-MM-DD]"
  review_owner: "[role or project]"
  run_mode: "[on_demand_local_brief]"
  probability_method: "[de_vigged_same_line_market_consensus]"
  autonomous_wagering: false
  ap_frankenstein_integration: false
```

State the intended job in one sentence. State what creates expected value, what context is allowed to do, and what the adapter explicitly does not predict.

## 2. Profile registry

Use only lifecycle values defined in `SPORT_ADAPTERS/README.md`.

| profile_id | lifecycle | participant scope | period | allowed line shape | overtime treatment | probability method | activation blocker or approval |
|---|---|---|---|---|---|---|---|
| `[league.market]` | `[active, pilot_enabled, disabled_provider_validation, disabled_model_only, or retired]` | `[team/player/event]` | `[full game/period]` | `[moneyline/half point/other exact shape]` | `[included/excluded/must match source]` | `[named method or none]` | `[none or exact blocker]` |

List adjacent markets that are not equivalent and therefore remain unavailable. A profile exposed by a provider stays disabled until its own validation passes.

## 3. Market identity and settlement contract

Every candidate and comparison quote must preserve:

```yaml
market_identity:
  sportsbook_id: "[canonical book]"
  jurisdiction: "[state/region]"
  event_id: "[canonical event]"
  provider_event_id: "[raw provider event ID]"
  participant_id: "[canonical team/player or null]"
  provider_participant_id: "[raw provider ID or null]"
  raw_market_label: "[verbatim sportsbook label]"
  raw_selection_label: "[verbatim outcome label]"
  canonical_market_key: "[profile key]"
  side: "[home|away|over|under|yes|no|other]"
  line: "[number or null]"
  period: "[full game or exact period]"
  overtime_treatment: "[included|excluded|unknown]"
  push_behavior: "[impossible|push|unknown]"
  void_and_participation_rule: "[verified rule or unknown]"
  american_odds: "[integer]"
  decimal_odds: "[number]"
  market_status: "[open|suspended|closed|unknown]"
  retrieved_at_utc: "[timestamp]"
  provider_last_update_utc: "[timestamp or null]"
  source_id: "[source]"
  raw_snapshot_id: "[snapshot/hash reference]"
  ap_frankenstein_compatibility: "[direct|equivalent_but_not_supported|unsupported]"
```

Define all approved raw-to-canonical equivalences in a table. Retain both raw values even when equivalence is approved.

| raw market shape | canonical profile | equivalence conditions | settlement conditions | AP compatibility | status |
|---|---|---|---|---|---|
| `[raw example]` | `[profile]` | `[exact conditions]` | `[period/overtime/push/void match]` | `[label]` | `[approved or blocked]` |

Reject mismatched thresholds, periods, participants, overtime rules, push behavior, or void/participation rules. Never manufacture an opposing side, combine opposite sides from different books, or treat a nearby threshold as the same line.

AP compatibility is descriptive only. It creates no API, write, spreadsheet, settlement, or handoff integration with AP Frankenstein.

## 4. Source and compliance policy

List preferred sources in authority order for each fact class. Official or licensed sources normally lead; screenshots or structured manual entry are explicit fallbacks for visible sportsbook facts.

| source_id/class | facts or markets supplied | authority rank | access method | jurisdiction coverage | timestamp behavior | terms/license reviewed | permitted use | current status |
|---|---|---:|---|---|---|---|---|---|
| `[source]` | `[facts]` | `[1-N]` | `[documented API/public page/manual evidence]` | `[scope]` | `[provider/local timestamps]` | `[date and evidence]` | `[operational facts/odds comparison/licensed model input]` | `[approved/fallback/blocked/unverified]` |

For every run, retain the source identifier or URL, retrieval time in UTC, provider object IDs, and raw snapshot reference or content hash. State-specific sportsbook hosts or feeds must not be treated as another jurisdiction without verification.

Do not automate authenticated sportsbook pages, spoof location, bypass access controls, evade rate limits, or use a source outside its documented permission. Statistical availability does not establish permission for wagering-related model use. A source with unclear terms, provenance, timestamp behavior, or pricing-origin independence cannot support `ACTIONABLE FOR REVIEW` until resolved.

Document season-specific official URLs and deadlines as configurable, annually reverified values rather than permanent assumptions.

## 5. Active signal registry

Every enabled Tier A, B, or C signal requires all ten fields below. Use the shared signals in the monitoring playbook by reference when their behavior is unchanged; do not copy them into a competing definition.

### 5.1 Inherited shared-signal extensions

Use this table only to add profile-specific constraints to a shared signal. It does not create another signal ID or collection path.

| shared_signal_id | profiles | additional identity/settlement constraint | maximum-age override | reporting extension |
|---|---|---|---|---|
| `[promo_terms, target_quote, comparison_quotes_same_line, market_status, or promo_expiration]` | `[profiles]` | `[exact additional constraint or none]` | `[stricter value or inherit]` | `[additional adapter-specific audit field or none]` |

### 5.2 Sport-specific signals

| signal_id | market_profile | tier | source_hierarchy | refresh_trigger | maximum_age | material_change_rule | candidate_state_effect | probability_use | reporting_rule |
|---|---|---|---|---|---|---|---|---|---|
| `[stable_id]` | `[exact profile(s)]` | `[A/B/C]` | `[ordered sources]` | `[event/time trigger]` | `[seconds or event-scoped rule]` | `[exact old-to-new condition]` | `[WATCH/BLOCKED/INELIGIBLE/re-rank from Tier B/informational]` | `[consensus input or none]` | `[always, change-only, blocker-only]` |

Apply these invariants:

- Tier A owns identity, eligibility, availability, exact target quote, and settlement gates.
- Tier B owns numeric valuation. De-vig each complete comparison book separately, exclude the target book, then aggregate source-level fair probabilities under a named versioned method.
- Tier C may invalidate an older price batch or change state. It never modifies probability or rank directly.
- A material Tier A/C fact newer than any affected quote changes the candidate to `WATCH` and triggers a synchronized target/comparison refresh. If fresh quotes remain unavailable at the final check, use `BLOCKED`.
- Do not double-count a fact already reflected in refreshed Tier B prices.

Define profile-specific critical gates. Do not assume that a lineup, starter, weather, or role fact has the same state effect across sports or markets.

## 6. Materiality and state rules

For every configurable materiality rule, record:

```yaml
materiality_rule:
  rule_id: "[stable versioned ID]"
  profiles: ["[profile]"]
  source_fields: ["[field]"]
  comparison_operator: "[changed|equals|threshold crossing]"
  qualifying_values: ["[values]"]
  effective_time_rule: "[how fact time is compared with quote time]"
  state_effect: "[WATCH|BLOCKED|INELIGIBLE]"
  required_refetch: ["target_quote", "comparison_quotes_same_line"]
  resolution_rule: "[facts required to clear state]"
  probability_effect: "none"
```

Enumerate exact results for missing, stale, conflicting, unconfirmed, suspended, canceled, scratched/inactive, and resolved facts. Every candidate snapshot must include:

```yaml
monitoring_metadata:
  next_refresh_at: "[timestamp or null]"
  next_refresh_reason: "[registered signal or final-check reason]"
```

These are local brief/audit annotations until a separately reviewed persisted-schema change is approved.

## 7. Refresh policy

Define an event-relative, on-demand research cadence. At minimum specify:

1. Promotion intake/baseline capture.
2. Distant pregame slate refresh.
3. Official report, lineup, roster, or other sport-specific release windows.
4. Immediate refresh after every registered material change.
5. Shortlist refresh near event start.
6. One synchronized promotion, event-status, target-price, and comparison-price refresh immediately before human placement.

Use only these shared phase IDs: `intake`, `distant_pregame`, `official_release_window`, `material_change`, `shortlist_check`, and `final_sync`.

| phase_id | sport-specific window/trigger | facts refreshed | maximum ages | state if unavailable | next refresh reason |
|---|---|---|---|---|---|
| `[standard phase ID]` | `[baseline/T-N/material event/final check]` | `[signals]` | `[thresholds]` | `[WATCH or BLOCKED]` | `[reason code]` |

The documentation pilot does not authorize a recurring scheduler, background poller, automatic alert, closing-line job, or settlement job. Cadence defines what an on-demand run or human-requested refresh must obtain.

## 8. Tier D model-only registry

Tier D fields are hypotheses, not active context or persuasive narrative.

| group_id | potential profile consumers | candidate inputs | required source permission | named model consumer | activation evidence | anti-noise boundary | lifecycle |
|---|---|---|---|---|---|---|---|
| `[sport_model_family]` | `[profiles]` | `[versioned inputs]` | `[licensed/permitted source]` | `[none until implemented]` | `[leak-free history, out-of-sample result, calibration, uncertainty, monitoring]` | `[excluded proxy/narrative]` | `disabled_model_only` |

Until activation, do not routinely fetch, score, narrate, rank with, or change state from Tier D data. Activation requires an exact market consumer, documented transformations, licensed/permitted fields, versioned model, leak-free historical test, out-of-sample and calibration results, uncertainty treatment, and production monitoring rule.

## 9. Tier X exclusions

| excluded signal or narrative | reason excluded | permitted operational use, if any |
|---|---|---|
| `[hot streak, tiny split, rumor, unsupported sharp claim, etc.]` | `[no defined consumer or validation]` | `[none, or early WATCH signal requiring authoritative confirmation]` |

Tier X material must not supply probability, rank, positive-EV language, or persuasive candidate support. If a lower-authority report plausibly signals a registered material change, it may create `WATCH` only until an approved source confirms or rejects it.

## 10. Provider-validation evidence

Record evidence without embedding credentials or relying on an undocumented live claim.

| evidence_id | profile | target/comparison role | source and jurisdiction | captured_at_utc | event timing condition | exact identity result | line/price result | status/timestamp result | raw evidence reference | discrepancy/resolution |
|---|---|---|---|---|---|---|---|---|---|---|
| `[id]` | `[profile]` | `[target or comparison]` | `[book/feed/state]` | `[time]` | `[board open/post-news/near start]` | `[pass/fail]` | `[match/explainable movement/fail]` | `[pass/fail]` | `[snapshot/hash/screenshot]` | `[notes]` |

Recommendation-grade validation must demonstrate:

- target-book event, market, side, line, price, status, and jurisdiction agreement with timestamped user-visible evidence across the adapter's required timing conditions;
- local retrieval timestamps even when provider update timestamps exist;
- exact opposing outcomes from each comparison book at one threshold and settlement contract;
- at least two usable non-target books from two resolved pricing-origin groups;
- target exclusion, per-book de-vigging, configured aggregation, quote-age limits, and maximum collection-time skew;
- explicit exclusions for stale, suspended, duplicate, one-sided, mismatched, or unidentified records; and
- visible behavior when a provider changes schema, loses coverage, or cannot satisfy freshness.

## 11. Recorded fixtures and acceptance scenarios

Create immutable, credential-free fixtures for every approved provider and material state. Tests must not require paid or live calls by default.

| fixture/scenario | required input condition | required outcome | reason code / audit evidence |
|---|---|---|---|
| Exact current target and valid consensus | all identity, eligibility, freshness, and critical context gates pass | deterministic EV/ranking may run | calculation and source versions shown |
| Missing same-line consensus | fewer than two usable independent comparison books | `WATCH` during research; `BLOCKED` at final check; break-even only | source exclusions shown |
| Material context newer than price batch | registered Tier A/C change after quote retrieval | `WATCH` and synchronized refetch; no manual probability change | old/new timestamps shown |
| Stale or suspended quote | quote exceeds age or is non-open | exclude quote and downgrade as coverage requires | freshness/status reason |
| Market or settlement mismatch | line, period, overtime, participant, push, or void rule differs | reject equivalence and block affected evaluation | raw and canonical identities shown |
| Promotion violation | exact term makes candidate ineligible | `INELIGIBLE` | term and source shown |
| Provider/jurisdiction mismatch | feed or screen is not the target jurisdiction | `BLOCKED` | source jurisdiction shown |
| Disabled profile requested | profile is not `active` or `pilot_enabled` | `BLOCKED`; no candidate generation | lifecycle and blocker shown |

Add sport-specific fixtures for lineup/availability, event postponement, participant scratches, report-release deadlines, weather/venue state, push-capable lines, and any other registered critical facts.

## 12. On-demand run and decision-brief contract

### Required inputs

- Original promotion text or screenshot, including book, jurisdiction, token count, boost type, stake/payout cap, odds range, expiry, eligible markets/events, overtime, push, cancellation, and void rules.
- Exact target-book quote evidence for every considered candidate.
- Complete same-line comparison pairs and pricing-origin metadata.
- Current authoritative Tier A/C sport facts required by the selected profile.
- User risk limits when expected-dollar or exposure ranking depends on them.

Parse multiple tokens separately unless their complete terms are proven identical. Evaluate the whole eligible opportunity set, rank by expected dollars subject to data quality and user limits, show correlation/exposure warnings, and recommend fewer uses when fewer candidates pass. Never lower gates to use every token.

### Required output

Use the decision-brief and JSON contracts in `PROMO_ANALYSIS_PLAYBOOK.md`, plus:

- selected adapter/profile ID and version;
- raw and canonical market identities and AP compatibility label;
- target exclusion and comparison-origin audit;
- settlement, overtime, push, and jurisdiction verification;
- quote ages, collection-time skew, and post-material-change synchronization state;
- unresolved blockers and the exact next refresh trigger;
- meaningful passes and opportunity-cost explanation; and
- one explicit sentence that no wager was placed or confirmed.

Save only a local research/evidence snapshot. Do not write to AP Frankenstein or infer that a researched candidate became a placed wager.

### Reusable task prompt

```text
Evaluate the supplied [SPORT/LEAGUE] promotion using [ADAPTER_ID] version [VERSION].

Parse and verify every token separately. Select only active or pilot-enabled profiles whose raw and canonical market, period, overtime, push, and settlement identities match. Retrieve or verify current target quotes, then build fair probability only from at least two fresh, complete, same-line opposing pairs from independent non-target pricing origins. Apply the adapter's authoritative Tier A/C gates and immediately invalidate prices older than a material change. Do not create a narrative probability adjustment or use disabled Tier D/X information.

Use deterministic boost, de-vig, EV, expected-dollar, freshness, and ranking calculations. Return the standard Promotion Decision Brief with adapter version, sources, timestamps, exclusions, passes, blockers, next refresh condition, and human-decision boundary. If the evidence supports fewer qualifying candidates than available tokens, return fewer. Never place or confirm a wager and make no AP Frankenstein call or write.
```

## 13. Activation checklist and change log

Before changing a profile lifecycle:

- [ ] Raw/canonical/settlement identities are complete.
- [ ] Every enabled Tier A/B/C signal has the ten-field contract.
- [ ] Source access, terms, provenance, jurisdiction, and timestamps are reviewed.
- [ ] For `pilot_enabled`, a verified per-run evidence path exists and unfinished cross-timing validation blockers are named; for `active`, recorded provider evidence covers all required timing conditions.
- [ ] Independent same-line consensus can satisfy the global gate.
- [ ] Missing, stale, conflicting, suspended, material-change, and disabled cases have exact expected outcomes; credential-free recorded fixtures exist before `active` status.
- [ ] Deterministic calculations and report behavior are verified.
- [ ] Tier D and Tier X boundaries are explicit.
- [ ] Monitoring playbook, adapter catalog, `AGENTS.md`, and `README.md` agree.
- [ ] Adapter metadata declares `adapter_contract_v1` and every standard refresh phase is represented.
- [ ] Activation received separate explicit approval.

| date | adapter version | profiles affected | change | evidence/approval reference |
|---|---|---|---|---|
| `[YYYY-MM-DD]` | `[version]` | `[profiles]` | `[description]` | `[reference]` |
