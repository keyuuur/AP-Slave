# Promotion Decision Brief

## Run

| Field | Value |
|---|---|
| Run ID | run-wnba-golden |
| Created | 2026-07-14T04:00:00Z |
| Timezone | America/Chicago |
| Jurisdiction | US-MO |
| Adapter | wnba.pregame_full_game_v0_1 v0.2.1 |
| Profile | wnba.full_game.moneyline (pilot_enabled) |
| Overall status | actionable_for_review |

## Promotion

| Field | Value |
|---|---|
| Promotion ID | promo-wnba-golden |
| Sportsbook | FanDuel (US-MO) |
| Boost | profit_boost at 30% |
| Maximum stake | 25 |
| Expires | 2026-07-14T05:00:00Z |
| Verification | confirmed |
| Ambiguities | none |

## Ranked candidates

| Rank | Candidate | Market / side | Target price | Boosted decimal | Break-even p | Estimated p | EV/unit | Expected dollars | State |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | wnba-home-moneyline | wnba.full_game.moneyline / home | -110 | 2.181818181818181818181818182 | 0.4583333333333333333333333333 | 0.510869565217391304347826087 | 0.114624505928853754940711463 | 2.865612648221343873517786575 | actionable_for_review |

## Candidate audits

### wnba-home-moneyline

- Identity: event `wnba-game-1`, participant `wnba-team-home`, raw market `Game Moneyline`, raw selection `Home`.
- Settlement: period `full_game`; overtime/extra innings `included`; push `impossible`; participation `participant must start`; void `void if event is canceled`; stat counting `official league statistics`; settlement `official full-game result including overtime`.
- Pricing audit: target `FanDuel` excluded `True`; raw sources `2`; usable books `2`; resolved origins `2`; method `wnba_market_consensus_mean_v1`.
- Source-level probabilities: Comparison A/origin_a: 0.5217391304347826086956521739, Comparison B/origin_b: 0.5.
- Comparison timing: oldest age `50` seconds; collection skew `20` seconds; dispersion `2.173913043478260869565217390` percentage points.
- Excluded sources: none.
- Freshness/refresh: post-change synchronized `True`; next refresh `—`; reason `—`.
- Reason codes: none.
- Blockers: none.
- Invalidation conditions: Any promotion, quote, identity, settlement, market-status, or material-context change requires a new evaluation..
- Source references: evidence:target:wnba-home-moneyline, evidence:comparison:wnba-home-moneyline:a, evidence:comparison:wnba-home-moneyline:b.

## Freshness

- Maximum target-quote age observed: `30` seconds.
- Oldest material-input age observed: `—` seconds.
- Stale inputs: none.

## Run blockers

| Reason code | Candidate | Field | Message |
|---|---|---|---|
| none | — | — | No blockers recorded. |

## QA and changes

- QA: `pass`; issues: none.
- Prior run: `—`; material change: `False`; changes: none.

## Human decision boundary

No wager has been placed or confirmed.
