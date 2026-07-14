# Advantage Play Intern — Non-Authoritative Roadmap

**Document status:** Future ideas and preserved planning history only

**Created:** 2026-07-13

**Authority:** None for current operation

## 1. How to use this document

This file preserves useful ideas removed from the current product specification. Nothing here is implemented, scheduled, enabled, approved, or provider-certified merely because it is documented.

Current behavior is governed by `PROJECT_CONTEXT.md`, the two playbooks, `SPORT_ADAPTERS/catalog.yaml`, `SPORT_ADAPTERS/source_registry.yaml`, and the selected adapter. A roadmap item requires a separately scoped plan, explicit approval, implementation, tests, source and license review, and synchronized governing-document updates before it can change current behavior.

Roadmap ideas must never weaken:

- human approval and the ban on sportsbook automation;
- exact market, jurisdiction, settlement, source, and provenance requirements;
- target exclusion and independent-origin consensus;
- freshness and post-material-change synchronization;
- fail-closed lifecycle and candidate-state rules;
- AP Frankenstein's separate downstream ownership.

## 2. Preserved product direction

The original product concept addressed an attention problem: prices, availability, lineups, weather, event state, and promotion eligibility can change faster than a person can repeatedly check them. The long-term idea is a disciplined local research assistant that can perform narrow, auditable jobs and surface only material changes.

Potential future modes were:

- **manual-input mode:** a local deterministic calculator using verified structured entry and screenshots;
- **provider-assisted research mode:** on-demand retrieval through approved, tested provider adapters;
- **scheduled monitoring mode:** event-relative refreshes and local alerts;
- **event-driven mode:** provider push messages or change feeds that re-evaluate only affected markets;
- **replay/backtest mode:** reconstruction from data actually available at the historical decision time;
- **live-trigger mode:** separately validated live-market conditions with measured latency.

Only the first of these is the recommended next implementation milestone. The others remain contingent on evidence and approval.

## 3. Recommended future architecture

The historical architecture remains a useful decomposition, not a build instruction:

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

The recommended design principle is still functions first, agents second. Provider-specific payloads should translate into canonical internal objects behind typed interfaces. Deterministic code should own arithmetic, validation, freshness, ranking, and state transitions. LLM use should remain limited to parsing, ambiguity detection, summarization, entity-resolution assistance, explanation, and exception handling.

Possible local implementation choices retained for later evaluation include Python 3.12+, Pydantic, httpx, SQLAlchemy with SQLite, pytest, structured JSON logging, FastAPI, and a minimal Streamlit or terminal UI. APScheduler or cron is relevant only after scheduling is approved. PostgreSQL, Redis, queues, WebSockets, containers, and a separate frontend should wait for a demonstrated requirement.

No technology in this section is selected or installed by this roadmap.

## 4. Provider and data-source discovery backlog

The original research listed possible provider categories:

| Category | Possible benefit | Required proof before use |
|---|---|---|
| General odds API | Fast multi-book integration | Exact sportsbook, jurisdiction, market, alternate-line, latency, timestamp, and origin coverage |
| Enterprise odds comparison feed | Broader prop and historical coverage | Cost, licensing, stable identifiers, source independence, and schema behavior |
| Full sports-data provider | Shared schedules, IDs, lineups, injuries, and results | Exact permitted use, update cadence, correction behavior, and separation from wagering models |
| Sportsbook/manual evidence | Exact visible target or comparison market | Timestamp, jurisdiction, identity, settlement, freshness, and user verification |
| Official league/team source | Strong operational authority | Exact access permission, season/version, timestamps, and operational-only boundary |
| Government weather source | Venue-matched operational facts | Venue mapping, validity window, identifying User-Agent where required, and versioned gate rules |

Historically named examples included The Odds API, Sportradar, SportsDataIO, OddsJam, and OpticOdds. These are evaluation leads only; no marketing page or successful request certifies a provider.

Existing reference links retained from the original specification:

- The Odds API V4 documentation: <https://the-odds-api.com/liveapi/guides/v4/>
- Sportradar Odds Comparison player props: <https://developer.sportradar.com/odds/reference/oc-player-props-overview>
- Sportradar MLB lineups and game rosters: <https://developer.sportradar.com/baseball/docs/mlb-ig-tracking-lineups-game-rosters>
- SportsDataIO betting odds overview: <https://sportsdata.io/live-odds-api>
- National Weather Service API: <https://www.weather.gov/documentation/services-web-api>
- Baseball Savant Statcast Search: <https://baseballsavant.mlb.com/statcast_search>

Before any integration, record real credential-free or approved sample evidence at board open, after material changes, and near event start. Validate exact fields, timestamps, schema changes, suspension/closure behavior, jurisdiction, market completeness, sportsbook aliases, and pricing-origin independence. Do not select a provider from price or marketing claims alone.

Golf remains a deliberate manual-first exception. Its wager volume does not justify a paid Golf API. Each actual promotion should use a user-supplied Missouri target screen, exact book rules, an event-specific organizer/source pack, and manually verified comparison evidence when available. Lack of two independent complete comparisons means no recommendation-grade EV.

## 5. Automation and monitoring backlog

### 5.1 Event-relative scheduling

The historical scheduling idea used sport- and event-relative phases rather than one global interval. A future scheduler could implement the six existing adapter phase IDs:

- `intake`
- `distant_pregame`
- `official_release_window`
- `material_change`
- `shortlist_check`
- `final_sync`

The prior illustrative MLB cadence was an early slate build, hourly distant refresh, 15-minute refresh inside six hours, five-minute checks around lineup release and first pitch, and immediate synchronized refresh after a material change. These are planning examples, not current schedules or defaults.

Any scheduler milestone must add:

- a global kill switch;
- per-provider rate limits, backoff, and health reporting;
- event-relative configuration rather than hard-coded times;
- durable last-success and staleness state;
- duplicate suppression;
- visibility when the monitor itself is stale;
- no sportsbook authentication or wagering action.

### 5.2 Material-change detection

Possible future triggers include promotion changes, target-price movement, lineup or injury updates, starting-pitcher changes, quarterback or inactive-list changes, flex or venue changes, Golf field/tee/cut/course changes, operational-weather threshold changes, postponement, and market suspension.

The selected adapter must already define the materiality rule. A trigger invalidates affected prices and requests a synchronized batch; it never directly changes probability.

### 5.3 Alerts

Future alerts should be local and change-based. They should contain what changed, the old and new values, timestamps, the candidate-state effect, stale or missing dependencies, and the next refresh condition. Identical state should not produce repeated noise.

No outbound alert channel is approved. Email, text, push, chat, and webhook delivery require a separate privacy, authentication, reliability, and cost review.

## 6. Statistical-model and feature hypotheses

All statistical features below remain hypotheses or `disabled_model_only` concepts. None may be fetched routinely, scored, narrated as support, blended with consensus, or used to alter probability until a named consumer, licensed/permitted source, deterministic transformation, leak-free dataset, out-of-sample evaluation, calibration, uncertainty treatment, and monitoring plan are approved.

### 6.1 MLB player hits

Historical candidate features included expected plate appearances, batting slot, home/away and ninth-inning opportunity, contact and strikeout rates, shrunk platoon splits, expected batting average, batted-ball quality, starter handedness and pitch mix, bullpen availability, park, roof, and calibrated weather effects.

A transparent model concept was:

1. estimate plate appearances;
2. estimate hit probability per plate appearance;
3. model total hits with a validated binomial-like or beta-binomial process;
4. derive threshold probabilities;
5. calibrate on held-out data and compare with market prices.

Independence and identical-distribution assumptions must be tested rather than assumed. Current MLB valuation remains exact-market consensus.

### 6.2 Basketball

NBA/WNBA hypotheses included minutes and rotation distributions, usage and shot opportunity, pace and possession efficiency, personnel-aware lineup redistribution, matchup shot profiles, travel/rest, foul and blowout tails, and overtime distributions. Recent averages, defense-vs-position ranks, tiny on/off samples, referee stories, or generic coach quotes are not models.

Official NBA/WNBA statistics remain subject to the governing terms restrictions. A future model needs a separately licensed or expressly permitted statistical source.

### 6.3 Football

NFL concepts included quarterback availability, offensive-line continuity, pass/run rates, pressure and protection, pace, neutral-situation tendencies, venue and roof, operational weather, and calibrated injury effects. Whole-number lines and tie-capable moneylines additionally require explicit push/tie probability and settlement treatment.

Passing- and rushing-yard props remain unregistered. A feature hypothesis cannot create a profile.

### 6.4 Golf

Historical Golf hypotheses included long-run strokes-gained components, calibrated recency, course and field strength, tee-wave/weather interaction, cut/finish distributions, and withdrawal uncertainty. Top-N and outright valuation additionally require exact field versions and tie/dead-heat-aware probability distributions.

Leaderboards, rankings, course-history anecdotes, recent finishes, and weather stories cannot substitute for a licensed model. No paid Golf data subscription is planned.

### 6.5 Other sports and live concepts

NHL goalie confirmations, lines, special teams, rest, travel, and shot-quality concepts; college-basketball bonus-state triggers; soccer schedule, lineup, travel, weather, set-piece, and tournament-format ideas; and all other unregistered sports remain discovery notes only. They require a new adapter-design phase before data collection or analysis.

## 7. Replay, backtesting, and model evaluation

A future replay system should reconstruct a decision using only evidence available at the historical timestamp. It must prevent look-ahead leakage from confirmed lineups, closing prices, corrections, or final results that were not known at decision time.

Potential evaluation metrics include:

- Brier score, log loss, and calibration plots;
- coverage and abstention rate;
- quote-age and source-failure distributions;
- extraction and entity-resolution correction rate;
- candidate-state precision;
- model-versus-consensus comparison;
- process time saved.

Backtests must include transaction and eligibility constraints and must not tune thresholds merely to force recommendations.

## 8. Tracking, CLV, and settlement history

The original concept included a distinction among candidate evaluation, user decision, wager record, closing line, result, and settlement. Potential fields included actual price and line, stake, action time, promotion, calculation version, closing comparison, CLV method, outcome, and reason codes.

Possible future CLV measures included entry implied probability versus closing no-vig probability, decimal-price difference, log-odds difference, and percentage CLV. The reference source and formula would have to be fixed before outcomes are observed.

These concepts are not current AP Slave responsibilities. AP Frankenstein owns the downstream receipt, spreadsheet, tracking, and settlement workflow after manual placement. Any future reconsideration requires an explicit cross-project ownership decision and may not silently duplicate or bridge that workflow.

## 9. Long-term build sequence

The recommended order is deliberately incremental:

### Phase 0 — Documentation integrity

- Maintain one canonical adapter catalog and source registry.
- Normalize adapter structure and governing references.
- Validate counts, closed vocabularies, formulas, links/review dates, and internal references offline.
- Keep lifecycle, implementation status, and source readiness separate.

### Phase 1 — Manual-input deterministic runtime

- Implement typed promotion and quote entry.
- Implement odds, boost, no-vig, EV, freshness, and eligibility calculations.
- Produce `promotion_decision_brief_v2` locally.
- Use recorded fixtures and screenshots; require no paid API.
- Start with `mlb.player_hits` and preserve every existing fail-closed gate.

### Phase 2 — Provider validation and one narrow integration

- Test one source against exact target/comparison identities and timing conditions.
- Record raw fixtures, hashes, timestamps, jurisdiction, schema behavior, and pricing origins.
- Introduce provider-agnostic adapters only after permissions and coverage pass.
- Do not change profile lifecycle automatically.

### Phase 3 — Supervised sport expansion

- Validate WNBA pilot runs and source evidence.
- Consider NBA or NFL activation one profile at a time.
- Keep Golf manual and disabled until its schema, probability, settlement, and evidence requirements are independently justified.

### Phase 4 — Scheduling and local change alerts

- Add event-relative jobs, state comparison, duplicate suppression, provider health, and a kill switch.
- Keep operation local and human supervised.
- Require a separate approval for every source cadence and alert channel.

### Phase 5 — Backtesting and optional models

- Build leak-free historical snapshots and calibration evaluation.
- Activate only named, licensed, exact-market models with out-of-sample evidence.
- Compare models against market consensus without narrative overrides.

### Phase 6 — Tracking or live features, only after ownership review

- Revisit CLV, settlement, or live triggers only after data quality, latency, compliance, and AP Frankenstein ownership are explicitly resolved.
- Live betting and autonomous wagering remain outside the intended boundary.

Progress through phases requires explicit user approval. Completion of one phase does not authorize the next.

## 10. Historical configuration sketch

The original specification included this illustrative configuration shape. It is not an active file, schema, or default:

```yaml
app:
  timezone: America/Chicago
  mode: local
  currency: USD

sportsbooks:
  target_books:
    - id: USER_CONFIGURES
      jurisdiction: USER_CONFIGURES

providers:
  odds:
    primary: USER_CONFIGURES
    fallback: manual_screenshot
  sports_data:
    primary: USER_CONFIGURES
  weather:
    primary: nws

freshness_seconds:
  target_quote_pregame: 180
  comparison_quote_pregame: 300
  collection_skew: 300

thresholds:
  minimum_ev_per_unit: USER_CONFIGURES
  minimum_data_quality: USER_CONFIGURES
  max_probability_uncertainty: USER_CONFIGURES

risk_controls:
  max_stake_per_promo: USER_CONFIGURES
  max_daily_exposure: USER_CONFIGURES
  max_weekly_exposure: USER_CONFIGURES
  autonomous_wagering: false

future_schedules:
  enabled: false

future_alerts:
  enabled: false
```

Actual configuration must be defined by the separately approved implementation and cannot weaken the governing contracts.

## 11. Promotion gates for any roadmap item

Before a roadmap capability becomes current, require:

1. a narrow user-approved scope and owner;
2. canonical interfaces and migration/compatibility review;
3. exact source, license, jurisdiction, season, and provider evidence;
4. deterministic implementation and offline fixtures;
5. unit, integration, golden, failure, and regression tests proportional to risk;
6. freshness, missing, stale, conflicting, suspended, and correction behavior;
7. audit fields, observability, and a kill or rollback path;
8. synchronized updates to the catalog, source registry, adapters, playbooks, `AGENTS.md`, `README.md`, and `PROJECT_CONTEXT.md` as applicable;
9. explicit lifecycle or implementation-status approval when relevant;
10. confirmation that AP Frankenstein and sportsbook-action boundaries remain intact.

Until every applicable gate is complete, the item stays in this roadmap and has no authority.
