# AGENTS.md — Advantage Play Intern

## Read-first instruction

Before changing code, schemas, prompts, schedules, or analytical logic, read:

1. `PROJECT_CONTEXT.md`
2. `PROMO_ANALYSIS_PLAYBOOK.md`
3. `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md`
4. `SPORT_ADAPTERS/catalog.yaml`
5. `SPORT_ADAPTERS/source_registry.yaml`
6. `SPORT_ADAPTERS/README.md`
7. The selected adapter location named by the catalog. For a WNBA request, read `SPORT_ADAPTERS/WNBA.md`; for an NBA request, read `SPORT_ADAPTERS/NBA.md`; for an NFL request, read `SPORT_ADAPTERS/NFL.md`; for a Golf request, read `SPORT_ADAPTERS/GOLF.md`. For the established MLB player-hits profile, use Section 6 of `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md` rather than inventing a duplicate adapter file.

Treat those files as product requirements. `PROJECT_CONTEXT.md` owns the broad product specification, `PROMO_ANALYSIS_PLAYBOOK.md` owns the analysis workflow and output contract, and `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md` owns global active-profile, valuation, freshness, material-change, and candidate-state rules. `SPORT_ADAPTERS/catalog.yaml` owns adapter, profile, lifecycle, and readiness records. `SPORT_ADAPTERS/source_registry.yaml` owns source URLs, access/automation permission, exact coverage posture, pricing-origin groups, season/event scope, review triggers, and policy artifacts. `SPORT_ADAPTERS/README.md` owns the lifecycle vocabulary, adapter-selection rules, and human-readable catalog presentation. The selected sport adapter owns that sport's required facts, exact market identities, signal registry, source gates, refresh cadence, profile-level gates, and validation fixtures; it references registry IDs rather than weakening or redefining source permission. Sport adapters do not replace the formulas, schemas, or report contracts in the three governing documents.

`SPORT_ADAPTERS/ADAPTER_TEMPLATE.md` is the structural conformance contract `adapter_contract_v1` for existing and future adapters. Read it before changing adapter structure, metadata, profile records, identity fields, materiality tables, refresh phases, evidence requirements, fixtures, or run contracts. The catalog contains exactly five current adapter records—MLB, WNBA, NBA, NFL, and Golf—and twenty-one profile records; lifecycle remains profile-level. The lifecycle distribution is one `active`, three `pilot_enabled`, and seventeen `disabled_provider_validation`. Soccer/World Cup is not registered; references in `PROJECT_CONTEXT.md` are concept-only and cannot authorize a run.

The current boundary in this file and `README.md` is narrower than the broad roadmap: references to statistical/manual probability, Tier D collection, live monitoring, recurring schedules, automatic alerts, bet tracking, closing-line capture, or settlement are future-only unless separately approved. After a user manually places a wager, AP Frankenstein remains the separate downstream receipt, spreadsheet, and settlement owner; do not duplicate or integrate that workflow here. When code and documentation disagree, stop relying on the undocumented behavior, identify the conflict, and update the implementation and documentation together.

Do not run a reusable or copy-paste prompt from `PROMO_ANALYSIS_PLAYBOOK.md` by itself. Apply `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md` and the selected sport adapter as the active scope and signal constraints; broader prompt branches are roadmap context, not authorization.

## Mission

Build and maintain a local, human-supervised sports-market research system that acts as an **attention, data, and analysis intern**.

The system watches narrow conditions at a scale the user cannot manually monitor, collects current evidence, performs deterministic calculations, and hands the decision back to the user.

The system is not an oracle, a guaranteed-profit engine, or an autonomous wagering bot.

## Primary user context

- Default timezone: `America/Chicago`.
- Stable profile: pregame MLB player-hit promotions.
- Experimental on-demand WNBA pilot profiles: pregame full-game moneyline, non-push spread, and non-push total.
- WNBA player points, rebounds, assists, and made-threes remain `disabled_provider_validation`.
- Registered NBA profiles `nba.full_game.moneyline`, `nba.full_game.spread`, `nba.full_game.total`, and `nba.player.points` remain `disabled_provider_validation`; NBA rebounds, assists, and made-threes are unavailable by catalog absence.
- Registered NFL profiles `nfl.full_game.moneyline`, `nfl.full_game.spread`, and `nfl.full_game.total` remain `disabled_provider_validation`; NFL player props, including passing- and rushing-yard props, are unregistered.
- Registered Golf profiles `golf.player.make_cut`, `golf.player.round_score_total`, `golf.player.round_matchup`, `golf.player.tournament_matchup`, `golf.player.top_n_finish`, and `golf.tournament.outright_winner` remain `disabled_provider_validation`. Their scope is Missouri promotion research for individual stroke-play tournaments offered by FanDuel or DraftKings; a book listing discovers a possible event but does not establish adapter support without exact competition, market, and settlement validation.
- Golf each-way, first-round-leader, group/3-ball/4-ball, live, parlay, team, match-play, Stableford, skins, and other absent profiles are unregistered and unavailable.
- Soccer and World Cup profiles are unregistered concept-only roadmap work. They have no lifecycle and fail closed with `ADAPTER_PROFILE_DISABLED` plus a catalog-absence audit annotation until a separate adapter-design phase registers them.
- Current fair-probability method: de-vigged, same-line market consensus.
- Expected edge source: promotion and boost value, not independent bet origination.
- Sport context is a freshness and invalidation layer. It may block a candidate or trigger new prices; it must not create an ad hoc probability adjustment.
- Live betting and live triggers are deferred until a separately validated phase.
- Current outputs are on-demand local decision briefs. Recurring schedules and automatic alerts require separate approval.
- Preferred mode: fully automated data retrieval when a documented or licensed source covers the exact market and sportsbook.
- Required fallback: screenshots or structured manual line entry.
- Final action: always belongs to the user.

## Non-negotiable operating principles

### 1. Human approval is mandatory

Never place, submit, confirm, or simulate having placed a wager. Never automate sportsbook account actions. Produce research, rankings, alerts, and logs only.

### 2. Deterministic code owns the numbers

Use tested code—not free-form LLM arithmetic—for:

- American/decimal/fractional odds conversion;
- boost application;
- implied and no-vig probabilities;
- EV and expected-dollar calculations;
- Kelly or staking math, when enabled;
- timestamps, freshness, and schedule calculations;
- aggregation, normalization, ranking, and grading;
- CLV and performance metrics.

The LLM may explain results, parse ambiguous promo text, map synonyms, summarize news, and identify missing context. It must not fabricate numerical inputs.

### 3. Every material fact needs provenance

Store or display, where applicable:

- source/provider;
- source URL or provider object identifier;
- retrieval timestamp in UTC;
- event, player, team, and market identifiers;
- sportsbook and jurisdiction/region;
- quoted line and price;
- lineup/injury status and its timestamp;
- transformation or calculation version.

No recommendation-grade output may depend on an uncited or irreproducible input.

### 4. Freshness is part of the data

A price without a timestamp is incomplete. A lineup without confirmation status is incomplete. A news item without publication time is incomplete.

Do not compare quotes that are materially asynchronous without warning. Make freshness thresholds configurable by sport, market, and workflow.

### 5. Missing data remains missing

Use explicit states such as:

- `confirmed`
- `probable`
- `unconfirmed`
- `stale`
- `conflicting`
- `not_available`
- `manual_verification_required`

Never silently impute an unknown player, line, sportsbook, promo term, lineup position, injury status, or price.

### 6. Source hierarchy

Prefer, in order:

1. official league/team/game and government sources;
2. licensed or documented sports/odds data providers;
3. sportsbook-originated quote supplied by a documented feed or the user;
4. established specialist sources;
5. secondary reporting and social media;
6. screenshot/manual input.

A lower-ranked source can be useful for speed, but confirm market-moving information with a stronger source when practical.

### 7. Narrow jobs before broad intelligence

Prefer a small number of well-defined monitors over a single vague “find good bets” agent.

Examples:

- detect a confirmed batting-order change;
- detect a player-hit price that becomes positive EV after a specified boost;
- detect an injury status change;
- detect both college-basketball teams entering the bonus during a specified first-half window;
- capture a closing line;
- grade a bet.

### 8. No hidden scraping or access circumvention

Use documented APIs, licensed feeds, approved exports, and permitted public endpoints. Do not bypass authentication, geolocation, anti-bot controls, rate limits, CAPTCHAs, paywalls, or source restrictions. Do not store sportsbook login credentials.

### 9. Model claims must be calibrated

Do not call a feature “predictive” merely because it is plausible. Distinguish:

- hypothesis;
- backtested association;
- out-of-sample result;
- live production result.

Track calibration and error. Avoid over-weighting recent streaks, batter-versus-pitcher samples, tiny splits, or narrative trends.

### 10. Auditability beats cleverness

A user should be able to reconstruct why a candidate was ranked from stored inputs and versioned formulas. Prefer transparent calculations and simple models until they are proven inadequate.

## Preferred system structure

Implement provider-agnostic modules behind typed interfaces.

- `promo_parser`
- `odds_ingestion`
- `sports_data_ingestion`
- `lineup_injury_monitor`
- `weather_ingestion`
- `news_monitor`
- `entity_resolution`
- `normalization`
- `feature_registry`
- `pricing_engine`
- `candidate_ranker`
- `alert_engine`
- `bet_tracker`
- `closing_line_capture`
- `settlement`
- `reporting`
- `backtesting`
- `observability`

Do not bind core logic directly to one vendor's response format. Each provider adapter must translate into canonical internal models.

For the current stable profile and experimental pilot, `alert_engine`, `bet_tracker`, `closing_line_capture`, and `settlement` are not active modules. AP Frankenstein owns the downstream post-placement workflow, and no bridge is part of this milestone.

## Suggested local stack for the MVP

Unless the existing repository dictates otherwise:

- Python 3.12+
- Pydantic for schemas and validation
- httpx for HTTP clients
- SQLAlchemy with SQLite for the MVP; migration path to PostgreSQL
- APScheduler or cron for local scheduling
- FastAPI for a local API
- Streamlit or a minimal web UI for the first dashboard
- pytest for unit and integration tests
- structured JSON logging
- `.env` or an OS secret store for API keys

Avoid adding infrastructure that is not needed for the current milestone. Redis, queues, WebSockets, containers, and a separate frontend are later additions unless a provider or live use case requires them.

## Canonical workflow

For each promotion or scan request:

1. **Parse the promotion.** Extract sportsbook, sport, market, boost type, boost amount, stake cap, payout cap, eligible odds range, eligible events, expiry, token rules, and void/push rules.
2. **Validate the request.** Identify missing or ambiguous terms. Continue with explicit assumptions only when they do not materially affect calculations; otherwise mark the run blocked.
3. **Build the eligible slate.** Resolve games, players, market labels, and start times.
4. **Collect prices.** Retrieve the exact target-book quote and comparison-book or consensus quotes. Record timestamps.
5. **Collect context.** Retrieve only the features registered for that sport and market.
6. **Normalize entities.** Map provider-specific player, team, event, sportsbook, and market identifiers to canonical IDs.
7. **Apply data-quality gates.** Reject or downgrade stale, missing, contradictory, suspended, or unverified inputs.
8. **Calculate.** Apply boost math, no-vig logic, model or consensus probability, EV, expected dollars, and uncertainty.
9. **Rank.** Compare every eligible candidate, including the opportunity cost of using a one-time token.
10. **Quality-check.** Verify arithmetic, quote/book/market matching, lineup status, and promo eligibility.
11. **Report.** Present ranked candidates, passes, blockers, timestamps, sources, and sensitivity.
12. **Hand off.** Save only the local research snapshot. If the user later places a wager manually, AP Frankenstein separately handles receipt logging, spreadsheet work, and settlement; this project makes no API or write call to it.

## Promotion math

### American to decimal

For positive American odds `A > 0`:

`decimal = 1 + A / 100`

For negative American odds `A < 0`:

`decimal = 1 + 100 / abs(A)`

### Profit boost

For a profit boost of `r` percent, define:

`multiplier = 1 + r / 100`

If the promotion multiplies **profit only**:

`boosted_decimal = 1 + multiplier * (base_decimal - 1)`

Do not use this formula for an odds boost, payout boost, parlay boost, bonus bet, insured bet, or token with different terms. Parse the actual promotion.

### Break-even probability

`break_even_probability = 1 / boosted_decimal`

### Two-way no-vig probability

For two opposing decimal prices `D1` and `D2`:

`raw1 = 1 / D1`

`raw2 = 1 / D2`

`fair1 = raw1 / (raw1 + raw2)`

Use a named alternative de-vig method only when configured. Store the method and version.

### Expected value

For estimated win probability `p` and decimal return `D`:

`EV_per_unit = p * D - 1`

`expected_dollars = permitted_stake * EV_per_unit`

Report both EV percentage and expected dollars. A one-time token should generally be ranked by expected dollars subject to risk, data quality, and eligibility—not EV percentage alone.

### Uncertainty

A point estimate is insufficient. When possible, calculate sensitivity across a plausible probability interval and report whether the candidate remains positive under conservative assumptions.

## Candidate states

Use these labels consistently:

- **ACTIONABLE FOR REVIEW** — all required data-quality gates pass and the candidate exceeds configured thresholds.
- **WATCH** — near threshold or waiting on a specific event such as confirmed lineup or price refresh.
- **PASS** — eligible but below threshold or dominated by a better token use.
- **BLOCKED** — cannot evaluate due to missing, ambiguous, stale, or conflicting material inputs.
- **INELIGIBLE** — violates a promotion term.

These are research states, not wagering commands.

## Required report fields

Every decision brief must include:

- run time and timezone;
- promotion interpretation;
- exact sportsbook and market;
- data freshness summary;
- ranked candidate table;
- base and boosted prices;
- break-even probability;
- probability source and method;
- EV percentage and expected dollars;
- lineup/injury/game status;
- key supporting factors;
- key invalidation risks;
- data-quality score or flags;
- passes and why they failed;
- unresolved ambiguities;
- source/audit references.

Structured local output uses additive contract `promotion_decision_brief_v2`. It must include adapter/profile/version and lifecycle, raw/canonical market identity, jurisdiction/settlement/push metadata, target-exclusion and pricing-origin audit, and `monitoring_metadata.next_refresh_at` / `next_refresh_reason`. These are local output fields, not persisted-schema changes.

When no candidate clears the threshold, state that directly. Do not force a selection.

## LLM responsibilities

The LLM may:

- parse promotion screenshots or text;
- identify ambiguous terms;
- summarize official news and lineup changes;
- explain KPI movements;
- resolve likely entity-name variants with confidence and review flags;
- write concise alerts and decision briefs;
- propose hypotheses for backtesting;
- assist with code, tests, and documentation.

The LLM must not:

- invent a current line or sportsbook price;
- invent a confirmed lineup, injury, weather reading, or game status;
- present a heuristic probability as a model output;
- conceal contradictory sources;
- substitute a different sportsbook or market without explicit disclosure;
- calculate recommendation-grade values from unreadable screenshots;
- use the user's prior win/loss outcome to rationalize a current candidate.

## Screenshot/manual quote workflow

When API coverage is unavailable:

1. Save the original screenshot with a content hash and timestamp.
2. Extract sportsbook, sport, event, player, market, side, line, price, and visible promo terms.
3. Assign confidence to each field.
4. Highlight any field below the verification threshold.
5. Require user verification before recommendation-grade calculations when a low-confidence field is material.
6. Preserve both the original extraction and any corrected value.

## Future scheduling reference — inactive in the current scope

Active profiles run on demand and produce local decision briefs. Do not create a recurring schedule, background poller, automatic alert, closing-line job, or settlement job until that automation is separately approved. When automation is activated later, `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md` and the selected sport adapter own the applicable refresh cadence.

Schedules are configuration, not hard-coded assumptions.

A reasonable MLB pregame default is:

- daily slate build in the early morning;
- hourly refresh while games are distant;
- 15-minute refresh inside six hours;
- 5-minute refresh near expected lineup release and before first pitch;
- faster polling only where provider terms, rate limits, and the use case justify it;
- immediate re-evaluation on a material change event;
- closing-line capture near market close;
- settlement after final status is authoritative.

Use event-relative scheduling rather than a single global interval wherever possible.

## Data quality gates for MLB player hits

Recommendation-grade output normally requires:

- exact target sportsbook quote with a recent timestamp;
- exact player, game, side, line, and price mapping;
- promotion eligibility confirmed;
- player active and expected to start, or clearly labeled otherwise;
- batting order confirmed when the evaluation occurs near game time;
- probable/confirmed starting pitcher status;
- no unresolved postponement or severe weather issue;
- probability source identified;
- sufficient same-line comparison prices for the configured market-consensus method; independent statistical models are disabled in the current scope;
- arithmetic and market matching tests passed.

A candidate may remain `WATCH` before lineups are confirmed, but the report must show the dependency.

## Testing requirements

### Unit tests

Cover at minimum:

- odds conversions;
- every supported promotion type;
- no-vig methods;
- EV and expected-dollar math;
- timezone and daylight-saving behavior;
- data freshness rules;
- promo eligibility logic;
- player/team/market normalization;
- ranking tie-breakers;
- push/void/settlement rules.

### Integration tests

Use recorded fixtures for each provider. Tests must not require paid API calls by default.

### Golden tests

Maintain representative end-to-end cases with expected reports, including:

- valid 30% profit boost;
- minimum-odds failure;
- stale target quote;
- lineup change after initial ranking;
- player scratched;
- conflicting player mapping;
- screenshot extraction error;
- no candidate above threshold;
- closing-line and CLV capture.

### Backtesting discipline

Prevent look-ahead bias. Store the data that was actually available at the historical decision timestamp. Do not backfill confirmed lineups, closing prices, or final stats into pre-decision feature sets.

## Observability

Track:

- provider uptime and latency;
- request counts and rate-limit responses;
- quote age;
- entity-resolution failures;
- alert counts and duplicate suppression;
- calculation version;
- number of candidates by state;
- data-quality failures;
- model calibration and drift;
- CLV and realized outcomes;
- manual corrections to screenshot extraction.

An alerting system that cannot report its own staleness is not production-ready.

## Security and compliance

- Never commit API keys or personal credentials.
- Use least-privilege access.
- Respect provider licenses and source terms.
- Do not automate sportsbook login or bet placement.
- Do not bypass regional or age restrictions.
- Keep user bankroll and exposure controls configurable and visible.
- Provide a global kill switch for scheduled jobs and alerts.

## Bankroll and risk controls

The core system is an information tool, but it must support user-defined controls such as:

- maximum stake per promotion;
- maximum daily and weekly exposure;
- maximum exposure by sport, player, team, and correlated event;
- fractional Kelly cap, if staking guidance is enabled;
- no increase in stake merely because of recent losses;
- pause/kill switch.

Do not recommend exceeding the promotion cap, user cap, or available bankroll rule.

## Broad roadmap build order — not active in the current scope

The on-demand provider-validation workflow comes first. This sequence is retained as later roadmap context, not authorization to build scheduling, alerts, closing capture, settlement, sport or market profiles beyond the exact registered MLB, WNBA, NBA, NFL, and Golf boundaries, or live features. The NBA, NFL, and Golf documents are credential-free specifications only and do not activate their profiles. AP Frankenstein remains the settlement owner.

1. Canonical schemas and database.
2. Promo parser with structured manual entry.
3. One odds-provider adapter plus screenshot fallback.
4. MLB schedule, probable pitcher, lineup, and weather adapters.
5. Deterministic boost/no-vig/EV engine.
6. Ranked terminal or simple web report.
7. Scheduler and change detection.
8. Immutable snapshot logging.
9. Optional closing-market/CLV evaluation after a separately approved boundary; no settlement ownership in this project.
10. Backtest and calibration harness.
11. Additional sportsbooks/providers.
12. Additional sports and live triggers.

Do not begin with a large multi-agent orchestration framework. First implement reliable typed functions and jobs. Introduce separate agents only where independent context, tools, or review materially improves reliability.

## Definition of done for an analytical feature

A feature is complete only when:

- its source and update cadence are documented;
- its canonical schema is defined;
- missing/stale/conflicting states are handled;
- calculations are unit-tested;
- it appears in the audit trail;
- the user-facing report explains its effect without overstating causality;
- historical evaluation avoids leakage;
- failure behavior is visible.

## Working style for coding agents

- Inspect the repository before proposing architecture changes.
- Prefer small, reversible changes.
- Add or update tests with every behavior change.
- Run relevant tests and report actual results.
- Preserve existing user data and migrations.
- Document assumptions and provider-specific caveats.
- Do not claim a provider covers a sportsbook or market until verified from current documentation or a live test.
- When blocked by unavailable credentials, build and test against fixtures and leave a precise integration checklist.
