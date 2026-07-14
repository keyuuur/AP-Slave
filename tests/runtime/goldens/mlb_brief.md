# Promotion Decision Brief

## Run

| Field | Value |
|---|---|
| Run ID | run-mlb-golden |
| Created | 2026-07-14T04:00:00Z |
| Timezone | America/Chicago |
| Jurisdiction | US-MO |
| Adapter | mlb.player_hits_v0_1 v0.1.1 |
| Profile | mlb.player_hits (active) |
| Overall status | no_qualifying_candidate |

## Promotion

| Field | Value |
|---|---|
| Promotion ID | promo-mlb-golden |
| Sportsbook | FanDuel (US-MO) |
| Boost | profit_boost at 30% |
| Maximum stake | 25 |
| Expires | 2026-07-14T05:00:00Z |
| Verification | confirmed |
| Ambiguities | none |

## Ranked candidates

| Rank | Candidate | Market / side | Target price | Boosted decimal | Break-even p | Estimated p | EV/unit | Expected dollars | State |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | mlb-player-over | mlb.player_hits / over 0.5 | -150 | 1.866666666666666666666666667 | 0.5357142857142857142857142856 | 0.510869565217391304347826087 | -0.0463768115942028985507246374 | -1.159420289855072463768115935 | pass |

## Candidate audits

### mlb-player-over

- Identity: event `mlb-game-1`, participant `player-1`, raw market `Player Hits`, raw selection `Over 0.5`.
- Settlement: period `full_game`; overtime/extra innings `included`; push `impossible`; participation `participant must start`; void `void if event is canceled`; stat counting `official league statistics`; settlement `official full-game result including extra periods`.
- Pricing audit: target `FanDuel` excluded `True`; raw sources `2`; usable books `2`; resolved origins `2`; method `mlb_market_consensus_mean_v1`.
- Source-level probabilities: Comparison A/origin_a: 0.5217391304347826086956521739, Comparison B/origin_b: 0.5.
- Comparison timing: oldest age `50` seconds; collection skew `20` seconds; dispersion `2.173913043478260869565217390` percentage points.
- Excluded sources: none.
- Freshness/refresh: post-change synchronized `True`; next refresh `—`; reason `—`.
- Reason codes: EV_BELOW_THRESHOLD.
- Blockers: none.
- Invalidation conditions: Any promotion, quote, identity, settlement, market-status, or material-context change requires a new evaluation..
- Source references: evidence:target:mlb-player-over, evidence:comparison:mlb-player-over:a, evidence:comparison:mlb-player-over:b.

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
