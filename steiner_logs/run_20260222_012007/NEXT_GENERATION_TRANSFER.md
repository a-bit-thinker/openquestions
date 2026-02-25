# Next Generation Transfer

Generated (UTC): 2026-02-22T02:23:03.590156+00:00
Run directory: steiner_logs/run_20260222_012007

## Scope
- This document summarizes the latest five rounds (or fewer if run is shorter).
- Goal: preserve proven progress and pass explicit next hypotheses to the next run/agent.

## Latest Round Snapshot
- Round: 5 (solve)
- Instance: S(9,10,22)
- Score: 26.85
- Valid: false
- Exact once: 237520/497420
- Uncovered: 259900
- Overcovered: 0

## Best Round So Far
- Round: 2 (solve)
- Instance: S(6,7,23)
- Score: 50.09
- Exact once: 64960/100947
- Uncovered: 35987
- Overcovered: 0

## Round Trajectory (recent)
| Round | Mode | Instance | Score | Valid | Exact Once | Uncovered | Overcovered |
|---:|---|---|---:|---|---|---:|---:|
| 1 | research | S(6,7,23) | 0 | false | 0/100947 | 100947 | 0 |
| 2 | solve | S(6,7,23) | 50.09 | false | 64960/100947 | 35987 | 0 |
| 3 | solve | S(7,8,20) | 43.9 | false | 46456/77520 | 31064 | 0 |
| 4 | solve | S(8,9,21) | 35.16 | false | 109242/203490 | 94248 | 0 |
| 5 | solve | S(9,10,22) | 26.85 | false | 237520/497420 | 259900 | 0 |

## Core Advances (Rounds 1-5 Window)
- round_0001: Converted round1 into a proof-first, gate-explicit execution contract for `S(6,7,23)` with five seeded proof lanes and a 3-loop gap verification routine.
- round_0001: Mandatory cross-run memory and local-paper-first requirements were completed.
- round_0001: Strong search stack and concise engine selector were formalized for immediate round2 use.
- round_0001: Practice blockers now map to source-backed implementation deltas.
- round_0001: Rounds2+ can execute without re-deriving proof/search structure.
- round_0001: Each stage has explicit stop/switch criteria and required metrics.
- round_0002: Established a reproducible strict-feasible plateau-break path for `S(6,7,23)` by combining a mandatory symmetry front gate with uncovered-driven LNS destroy/repack intensification.
- round_0002: Symmetry gate executed first with explicit orbit/coefficient diagnostics and an actual cyclic packed trial.
- round_0002: Add-only strict stage confirmed plateau (`9237 -> 9237`).
- round_0002: LNS stages advanced the strict frontier `9237 -> 9280` with monotone uncovered reduction `36288 -> 35987` and `overcovered=0` throughout.
- round_0002: Point-degree spread improved `426 -> 413` while preserving `(r-1)` max at target (`9`).
- round_0002: Keep symmetry diagnostics as a front gate, but use it as a bounded quality test for this instance.
- round_0002: Use intensified uncovered-driven LNS as the default first repair lane from `9280`.
- round_0002: Continue strict acceptance discipline and checkpoint best strict candidate frequently.
- round_0003: Established a reproducible strict-feasible improvement loop for `S(7,8,20)` that combines mandatory symmetry triage with uncovered-driven `k -> k+1` LNS repacks.
- round_0003: Symmetry gate executed first with explicit orbit diagnostics and bounded packed probes.
- round_0003: Stage-B seed frontier improved to `5634` blocks, then Stage-C LNS improved to `5807` (`+173` from seed, `+256` from round start).
- round_0003: Verifier movement: `score 40.20 -> 43.90`, `exact_once 44408 -> 46456`, `uncovered 33112 -> 31064`, `overcovered=0` unchanged.
- round_0003: `(r-1)` hard gate remained strict: max `7` at target and oversubscribed count `0` throughout.
- round_0003: Keep symmetry diagnostics as front gate, but do not spend long budgets on orbit-packed construction for this instance.

## Knowledge Gaps / Blockers
- No fully valid certificate yet; current frontier remains partial.
- Large uncovered residual remains; prioritize structured completion over random mutation.

## Next Hypothesis Ladder (for next generation)
1. round_0001: For `S(6,7,23)`, bounded symmetry triage plus pressure-triggered early repair handoff will beat prolonged symmetry-only or add-only runs while preserving strict feasibility.
2. round_0001: Practice history shows plateau formation at saturated `(r-1)` motifs and diminishing additive returns; early handoff targets the actual bottleneck.
3. round_0001: Improved uncovered reduction slope per fixed trial budget,
4. round_0001: reduced point-degree gap and `(r-1)` cap-tail concentration,
5. round_0001: keep `overcovered=0` and zero `(r-1)` oversubscription.
6. round_0001: Reject this hypothesis if three matched seeds show no improvement in uncovered reduction rate versus add-only baseline.
7. round_0002: Two-step motif-coupled LNS chains (reusing the same uncovered motif neighborhood across consecutive windows) with periodic neutral rebalance sweeps will outperform uncoupled random-window LNS from `9280`.
8. round_0002: First-window success opens transient local slack; immediate reuse of that motif should increase second-window augment probability before constraints re-harden.
9. round_0002: Periodic neutral rebalance reduces degree-tail concentration, which should increase feasible refill options in later windows.
10. round_0002: Improve `9280 -> 9310..9380` blocks,
11. round_0002: reduce uncovered by `210..700`,
12. round_0002: keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 9`.

## Mandatory Next-Round Discipline
1. Keep notes sections non-empty: `Core advance`, `Observations`, `Next-hypothesis`.
2. Every hypothesis must include: mechanism, expected metric movement, and stop condition.
3. Preserve exactness-first artifacts (overcovered=0 candidates) even if scalar score is lower.
4. Update this transfer file at round close to avoid losing accumulated reasoning.

