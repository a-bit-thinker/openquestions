# Next Generation Transfer

Generated (UTC): 2026-02-20T21:03:02.917395+00:00
Run directory: steiner_logs/run_20260220_183105

## Scope
- This document summarizes the latest five rounds (or fewer if run is shorter).
- Goal: preserve proven progress and pass explicit next hypotheses to the next run/agent.

## Latest Round Snapshot
- Round: 5 (solve)
- Instance: S(9,10,20)
- Score: 27.68
- Valid: false
- Exact once: 81200/167960
- Uncovered: 86760
- Overcovered: 0

## Best Round So Far
- Round: 2 (solve)
- Instance: S(6,7,17)
- Score: 48.29
- Exact once: 7805/12376
- Uncovered: 4571
- Overcovered: 0

## Round Trajectory (recent)
| Round | Mode | Instance | Score | Valid | Exact Once | Uncovered | Overcovered |
|---:|---|---|---:|---|---|---:|---:|
| 1 | research | S(6,7,17) | 0 | false | 0/12376 | 12376 | 0 |
| 2 | solve | S(6,7,17) | 48.29 | false | 7805/12376 | 4571 | 0 |
| 3 | solve | S(7,8,18) | 39.22 | false | 18008/31824 | 13816 | 0 |
| 4 | solve | S(8,9,19) | 33.22 | false | 39528/75582 | 36054 | 0 |
| 5 | solve | S(9,10,20) | 27.68 | false | 81200/167960 | 86760 | 0 |

## Core Advances (Rounds 1-5 Window)
- round_0001: advance statement: Established a dual-engine search strategy with a mandatory divisibility gate and phase-structured randomized completion.
- round_0001: Structure: hard gate + symmetry mode + randomized mode now explicitly specified.
- round_0001: Metrics selected for rounds 2+: point degree, `(r-1)`-pressure, uncovered/overcovered counts.
- round_0001: Source support: Keevash + iterative absorption + Kramer-Mesner + DLX references linked.
- round_0001: Future rounds can run measurable experiments instead of ad hoc search.
- round_0001: Engine switching condition is now explicit and testable.
- round_0002: Established a working symmetry-first then LNS fallback loop that makes monotone progress under strict admissibility and strict collision/`(r-1)` constraints.
- round_0002: Symmetry compression was attempted first and diagnosed as currently intractable in bounded budget.
- round_0002: LNS destroy/repack raised block count `1088 -> 1115` with no overcoverage and no `(r-1)` oversubscription.
- round_0002: Uncovered dropped `4760 -> 4571`; point-degree gap contracted `86 -> 24`.
- round_0002: Keep the same strict-feasibility move filter and large-neighborhood repack backbone.
- round_0002: The search space responds to multi-block repacks, not micro-swaps.
- round_0003: Implemented a symmetry-first gate plus absorber-reserved LNS pipeline that produced monotone strict-feasible gains for `S(7,8,18)`.
- round_0003: Symmetry mode was attempted first and rejected only after concrete orbit diagnostics + bounded search timeout.
- round_0003: LNS multi-block destroy/repack improved `2239 -> 2251` blocks (`+12`) with `overcovered=0` and `(r-1)` oversubscription `=0` throughout.
- round_0003: Uncovered improved `13912 -> 13816` and point-degree gap improved `179 -> 141`.
- round_0003: Keep the same strict row-owner feasibility gate.
- round_0003: Keep explicit reserve-then-flex refill order.
- round_0003: Keep bounded local exact re-pack inside LNS neighborhoods; this is where net positive moves were found.
- round_0004: Implemented a symmetry-first gate plus plateau-crossing LNS pipeline that improves strict-feasible coverage on `S(8,9,19)` while preserving all hard local invariants.

## Knowledge Gaps / Blockers
- No fully valid certificate yet; current frontier remains partial.
- Large uncovered residual remains; prioritize structured completion over random mutation.

## Next Hypothesis Ladder (for next generation)
1. round_0001: hypothesis statement: A hybrid policy (symmetry pre-scan, then randomized iterative absorption, then residual DLX) will dominate single-engine attempts for `r=6..9`.
2. round_0001: mechanism (why this should help): orbit compression wins when structure exists; randomized absorption handles unstructured bulk; DLX resolves only tiny residue.
3. round_0001: point degree max deviation should contract toward `0` after boosting.
4. round_0001: `(r-1)`-pressure tail should flatten before absorber phase.
5. round_0001: uncovered and overcovered `r`-sets should both approach `0` in residual stage.
6. round_0001: No viable group with material orbit reduction and randomized mode fails to reduce pressure tails over repeated seeds.
7. round_0001: Residual exact-cover size remains too large for DLX after repair/absorption.
8. round_0002: A cap-aware local exact re-pack on saturated 5-subset neighborhoods will outperform pure greedy local refill and push beyond 1115 blocks.
9. round_0002: Many stalled states are constrained by clusters of 5-subsets already at load 6; targeted destroy around those clusters plus bounded exact local solve should recover more than removed blocks while preserving global feasibility.
10. round_0002: Target `+15..40` blocks from 1115,
11. round_0002: uncovered reduction by `105..280`,
12. round_0002: keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 6`.

## Mandatory Next-Round Discipline
1. Keep notes sections non-empty: `Core advance`, `Observations`, `Next-hypothesis`.
2. Every hypothesis must include: mechanism, expected metric movement, and stop condition.
3. Preserve exactness-first artifacts (overcovered=0 candidates) even if scalar score is lower.
4. Update this transfer file at round close to avoid losing accumulated reasoning.

