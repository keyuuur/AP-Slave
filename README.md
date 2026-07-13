# Advantage Play Intern — Context Pack

**Version:** 0.1  
**Prepared:** 2026-07-10  
**Default timezone:** America/Chicago

## Purpose

This repository defines a local, human-supervised sports-market research system. Its job is to monitor narrow, explicitly defined conditions; collect and normalize current information; calculate deterministic pricing and KPI outputs; surface changes; and present a ranked decision brief before the user acts.

The governing idea is:

> The AI is an attention and research intern, not an oracle and not an autonomous bettor.

The system should reduce screen-watching and bookkeeping. It should not invent probabilities, claim guaranteed profit, or place wagers.

## Files in this pack

- **`AGENTS.md`** — root instructions for Codex or another local coding/agent host. Keep this file at the project root.
- **`PROJECT_CONTEXT.md`** — product specification, architecture, data model, sport-specific KPI registry, automation design, and phased roadmap.
- **`PROMO_ANALYSIS_PLAYBOOK.md`** — comprehensive operating prompt and runbook for evaluating a sportsbook promotion or market opportunity.
- **`PROMO_PLACEMENT_MONITORING_PLAYBOOK.md`** — authoritative global active-profile, valuation, refresh, material-change, candidate-state, and anti-noise policy.
- **`SPORT_ADAPTERS/README.md`** — sport-adapter catalog, lifecycle vocabulary, authority boundaries, and adapter-selection rules.
- **`SPORT_ADAPTERS/ADAPTER_TEMPLATE.md`** — required contract for adding a sport or market capability.
- **`SPORT_ADAPTERS/WNBA.md`** — authoritative WNBA market identities, signal registry, source policy, refresh cadence, gates, and validation fixtures.
- **`SPORT_ADAPTERS/NBA.md`** — authoritative NBA specification for registered disabled full-game and player-points profiles, including credential-free fixtures.
- **`SPORT_ADAPTERS/NFL.md`** — authoritative NFL specification for registered disabled full-game profiles, tie handling, operational context, and credential-free fixtures.
- **`SPORT_ADAPTERS/GOLF.md`** — authoritative Golf specification for registered disabled Missouri individual-stroke-play profiles, settlement variants, operational context, and credential-free fixtures.

`SPORT_ADAPTERS/ADAPTER_TEMPLATE.md` is also the structural conformance contract for existing adapters, version `adapter_contract_v1`. The catalog separates five adapter records from their twenty-one profile records so adapter versioning cannot be confused with profile lifecycle. The closed lifecycle distribution is one `active`, three `pilot_enabled`, and seventeen `disabled_provider_validation`.

For an active run, never use the reusable prompt in `PROMO_ANALYSIS_PLAYBOOK.md` alone. Pair it with `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md`, `SPORT_ADAPTERS/README.md`, and the selected sport adapter. Statistical/manual probability, Tier D feature collection, live monitoring, automated alerts, and settlement language in the broad prompt remain future roadmap context.

The monitoring playbook owns global valuation, freshness, material-change, and candidate-state rules. The adapter location named by the catalog owns sport-specific market identity, sources, signals, cadence, gates, and fixtures. WNBA, NBA, NFL, and Golf authority is delegated to `SPORT_ADAPTERS/WNBA.md`, `SPORT_ADAPTERS/NBA.md`, `SPORT_ADAPTERS/NFL.md`, and `SPORT_ADAPTERS/GOLF.md`; the established MLB player-hits registry remains in Section 6 of the monitoring playbook. An adapter may narrow global rules but cannot replace existing formulas, canonical schemas, decision-brief contracts, or human-control boundaries.

## Stable product and experimental pilot

The stable workflow remains deliberately narrow:

**Stable profile: MLB player-hits profit-boost scanner**

1. User enters or uploads the exact promotion terms and selects the sportsbook.
2. System fetches eligible MLB player-hit lines from a configured odds provider.
3. System fetches exact two-sided same-line markets from at least two independent comparison books, excludes the target book from its own fair-source count, and collects only the registered MLB gates: game and player status, confirmed lineup and batting slot, opposing starter, roof state, operational delay/postponement risk, and registered material bullpen availability.
4. Deterministic code converts the target price, applies the boost correctly, de-vigs each usable comparison book separately, aggregates the source-level fair probabilities under the named method, and calculates break-even probability and expected value. If the consensus gate fails, the brief reports boosted break-even and non-consensus comparisons only; it cannot label the candidate positive EV or actionable.
5. The system ranks candidates, exposes stale or missing data, and explains the key drivers and risks.
6. The user makes the final decision.
7. The system saves the local research snapshot. If the user manually places a wager, AP Frankenstein separately handles its existing receipt, spreadsheet, and settlement workflow.

The additional experimental pilot covers on-demand WNBA promotion analysis for pregame full-game moneylines, non-push spreads, and non-push totals. It uses the same exact-market consensus and deterministic EV requirements. WNBA player points, rebounds, assists, and made-threes remain `disabled_provider_validation`, and no WNBA statistical model is active.

NBA and NFL now have standalone `adapter_contract_v1` specifications, but no profile in either adapter is runnable. The registered NBA profiles are full-game moneyline, principal half-point spread, principal half-point total, and exact non-push player points. The registered NFL profiles are full-game moneyline, principal half-point spread, and principal half-point total. All seven remain `disabled_provider_validation` pending real promotion evidence, exact source and settlement validation, and separate activation approval. NBA rebounds, assists, and made-threes are unavailable by catalog absence; NFL player props, including passing- and rushing-yard props, are unregistered.

Golf has a standalone `adapter_contract_v1` specification for `golf.player.make_cut`, `golf.player.round_score_total`, `golf.player.round_matchup`, `golf.player.tournament_matchup`, `golf.player.top_n_finish`, and `golf.tournament.outright_winner`. All six remain `disabled_provider_validation`. The discovery scope is an individual stroke-play tournament offered by FanDuel or DraftKings in Missouri, but a book listing does not establish adapter support: exact organizer, event format, field, competition, market-wrapper, and settlement rules still must pass the Golf contract. Each-way, first-round-leader, group/3-ball/4-ball, live, parlay, team, match-play, Stableford, skins, and other absent Golf profiles remain unavailable by catalog absence.

There is no registered soccer or World Cup adapter. Soccer references in `PROJECT_CONTEXT.md` are concept-only roadmap hypotheses and cannot produce a run or candidate. World Cup discovery/design remains a separate future phase.

## Current operating posture

- Pregame MLB player-hit promotions are the stable market profile.
- Pregame WNBA full-game moneyline, non-push spread, and non-push total are `pilot_enabled` for supervised, on-demand analysis.
- NBA `nba.full_game.moneyline`, `nba.full_game.spread`, `nba.full_game.total`, and `nba.player.points` are registered but `disabled_provider_validation`; their contract and fixtures do not authorize candidate generation.
- NFL `nfl.full_game.moneyline`, `nfl.full_game.spread`, and `nfl.full_game.total` are registered but `disabled_provider_validation`; their contract and fixtures do not authorize candidate generation.
- Golf `golf.player.make_cut`, `golf.player.round_score_total`, `golf.player.round_matchup`, `golf.player.tournament_matchup`, `golf.player.top_n_finish`, and `golf.tournament.outright_winner` are registered but `disabled_provider_validation`; Missouri book availability is discovery evidence only, and their contract and fixtures do not authorize candidate generation.
- Fair probability comes from de-vigged, same-line market consensus. The pilot requires at least two usable comparison books from two distinct configured pricing-origin groups, and the target sportsbook never counts toward that minimum.
- One comparison book is an outlier or staleness cross-check, not consensus. A one-sided ladder without an exact opposing price at that source is non-de-viggable and cannot count as a recommendation-grade comparison pair. A conditionally equivalent target milestone still requires complete exact pairs from two independent non-target pricing origins.
- The promotion or boost is expected to supply most of the opportunity value.
- The active MLB context groups are event state, participant availability, confirmed lineup role, starting-pitcher identity, roof/operational weather, and registered material bullpen availability. They determine whether the market snapshot is trustworthy; they do not create narrative probability adjustments.
- Starter-workload, plate-appearance, player-skill, matchup, bullpen-projection, park/atmosphere, defense/catcher, and stolen-base features remain disabled Tier D inputs until a named validated model consumes them.
- The WNBA pilot uses official availability and game-state facts to invalidate stale price batches; missing league-wide starting-five confirmation alone does not block a full-game market.
- WNBA points, rebounds, assists, and made-threes remain `disabled_provider_validation`; whole-number spread/total and other unavailable WNBA profiles must not generate candidates.
- Every structurally valid NBA, NFL, or Golf case still returns `BLOCKED` with `ADAPTER_PROFILE_DISABLED` until its exact profile receives separate activation approval. Synthetic fixtures document fail-closed behavior and never establish provider certification or promotion evidence.
- All independent statistical models and manual probability overrides remain disabled.
- Live-betting monitoring is deferred.
- The active surface is an on-demand local decision brief. Scheduled/background polling and automatic alerts require separate approval.
- AP Frankenstein remains a separate downstream receipt, spreadsheet, and settlement system. This project makes no edits, API calls, spreadsheet writes, or new integration contract with it.
- Local structured briefs use additive contract `promotion_decision_brief_v2`, including adapter/profile/version, raw/canonical identity, comparison-origin audit, settlement, and next-refresh metadata. This is not a persisted-schema migration.

See `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md` for global active-profile rules and `SPORT_ADAPTERS/` for sport-specific capabilities.

## Automation options after the current pilots

The following are future deployment options, not active behavior. Current analysis is manual/on-demand and does not install a scheduler or send automatic alerts.

There are three practical operating modes:

### 1. Local scheduler — preferred for frequent monitoring

Use a local scheduler such as cron, APScheduler, or a queue worker. This supports sub-hour polling, precise game-relative windows, retries, provider rate limits, and event-driven feeds.

### 2. ChatGPT or ChatGPT Work scheduled tasks — useful for broader monitoring

Use this for hourly or less frequent digests, change monitoring, and reports. It is not the primary mechanism for low-latency market scanning.

### 3. Manual or screenshot-assisted mode — required fallback

When the exact sportsbook or market is not available from an API, accept screenshots or typed lines. Preserve the original image, extract the quote, flag low-confidence fields, and require verification before calculating or ranking.

## Live-odds acquisition ladder

Use the first available compliant method:

1. **Licensed or documented odds API** with the exact sportsbook, jurisdiction, market, and update frequency needed.
2. **Provider export, webhook, WebSocket, spreadsheet integration, or approved browser access.**
3. **Manual screenshot or structured entry.**
4. **Public-page scraping only when permitted by the source's terms and robots/access rules.** Never bypass authentication, geolocation, anti-bot controls, or technical restrictions.

Coverage must be tested rather than assumed. A provider may cover MLB props but not the user's exact book, market label, alternate line, or state-specific price.

## Broader roadmap boundaries

After a separately approved phase, the broader system may:

- retrieve and normalize data;
- monitor lineups, injuries, weather, line movement, live game states, and other defined triggers;
- compute odds conversions, no-vig probabilities, break-even points, EV, expected dollars, CLV, and tracking metrics;
- rank opportunities under user-defined rules;
- send alerts and produce audit-ready reports.

The system must not:

- place, submit, or confirm a wager;
- log in to a sportsbook account or handle sportsbook credentials;
- evade geolocation, access, anti-bot, or jurisdictional controls;
- present a model output as fact or guaranteed profit;
- use stale, unverified, or mismatched lines without prominent warnings;
- silently fill missing data with guesses.

## Success definition

The first version succeeds when it reliably answers this question:

> “Given this exact promotion, sportsbook, eligible slate, current prices, and current game context, which candidates deserve human review right now, why, and what data could invalidate the ranking?”

Performance should be evaluated through data freshness, quote accuracy, alert precision, time saved, closing-line value, calibration, and realized results over a sufficiently large sample—not by a short winning streak.
