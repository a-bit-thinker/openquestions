# Next Generation Transfer

Generated (UTC): 2026-02-22T16:50:46.012448+00:00
Run directory: steiner_logs/run_20260222_154119

## Scope
- This document summarizes the latest five rounds (or fewer if run is shorter).
- Goal: preserve proven progress and pass explicit next hypotheses to the next run/agent.

## Latest Round Snapshot
- Round: 5 (solve)
- Instance: S(9,10,26)
- Score: 15.44
- Valid: false
- Exact once: 1237250/3124550
- Uncovered: 1887300
- Overcovered: 0

## Best Round So Far
- Round: 2 (solve)
- Instance: S(6,7,23)
- Score: 50.16
- Exact once: 65009/100947
- Uncovered: 35938
- Overcovered: 0

## Round Trajectory (recent)
| Round | Mode | Instance | Score | Valid | Exact Once | Uncovered | Overcovered |
|---:|---|---|---:|---|---|---:|---:|
| 1 | research | S(6,7,17) | 0 | false | 0/12376 | 12376 | 0 |
| 2 | solve | S(6,7,23) | 50.16 | false | 65009/100947 | 35938 | 0 |
| 3 | solve | S(7,8,24) | 28.25 | false | 168720/346104 | 177384 | 0 |
| 4 | solve | S(8,9,25) | 24.35 | false | 497106/1081575 | 584469 | 0 |
| 5 | solve | S(9,10,26) | 15.44 | false | 1237250/3124550 | 1887300 | 0 |

## Core Advances (Rounds 1-5 Window)
- round_0001: Converted round1 for `S(6,7,17)` into a proof-first, gate-explicit research contract with five seeded proof lanes and a 3-round critical-gap verification loop.
- round_0001: Mandatory cross-run memory and local-paper-first requirements were completed.
- round_0001: Strong search stack and concise engine selector were formalized.
- round_0001: Practice blockers were mapped to source-backed implementation deltas.
- round_0001: Rounds2+ can execute without re-deriving proof skeleton or switch logic.
- round_0001: Engine switches and residual activation are now explicit and falsifiable.
- round_0002: Broke the long-standing strict `S(6,7,23)` frontier from `9280` to `9287` blocks while preserving `overcovered=0` and zero `(r-1)` oversubscription.
- round_0002: Score improved `50.09 -> 50.16`.
- round_0002: Exact-once improved `64960 -> 65009`.
- round_0002: Uncovered reduced `35987 -> 35938` with `overcovered=0` unchanged.
- round_0002: `(r-1)` load remained at cap (`9/9`) with oversubscribed count `0` throughout.
- round_0002: Point-degree spread improved versus baseline (`413 -> 368`; best intermediate `366`).
- round_0002: Use a mandatory two-phase strict loop on this instance: neutral pressure relief first, then positive LNS.
- round_0002: Keep symmetry gate short and evidence-based; this instance should switch quickly to the general pipeline.
- round_0003: Improved the strict `S(7,8,24)` frontier from `21080` to `21090` blocks with all hard verifier gates intact.
- round_0003: Score improved `28.22 -> 28.25`.
- round_0003: Exact-once improved `168640 -> 168720`.
- round_0003: Uncovered reduced `177464 -> 177384`.
- round_0003: `overcovered=0` preserved and `oversubscribed_(r-1)=0` preserved.
- round_0003: Architecture compliance: symmetry gate first, reserve-first general pipeline, LNS `k>1`, residual gate checked and deferred.

## Knowledge Gaps / Blockers
- No fully valid certificate yet; current frontier remains partial.
- Large uncovered residual remains; prioritize structured completion over random mutation.

## Next Hypothesis Ladder (for next generation)
1. round_0001: For `S(6,7,17)`, bounded symmetry triage plus pressure-triggered repair handoff will outperform prolonged single-engine continuation while preserving strict feasibility.
2. round_0001: It aligns with observed plateau behavior in rounds2-5 and targets saturated `(r-1)` motifs directly.
3. round_0001: faster uncovered reduction slope,
4. round_0001: lower `(r-1)` pressure tail,
5. round_0001: stable `overcovered=0` and zero `(r-1)` oversubscription.
6. round_0001: Reject after 3 matched seeds if uncovered reduction per fixed budget does not beat add-only baseline or if strict feasibility is violated.
7. round_0002: A motif-coupled mixed-window strict LNS schedule (`k=2..5` core plus periodic `k=6..8` bursts) starting from the new `9287` frontier will outperform fixed-window continuation.
8. round_0002: Small windows keep acceptance rate nonzero; periodic larger windows can cross the residual local bottlenecks that blocked further `+1` gains after trial ~700.
9. round_0002: Improve `9287 -> 9300..9340` blocks.
10. round_0002: Reduce uncovered by `91..371` while keeping `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree<=9`.
11. round_0002: Reject this hypothesis if after `>=30000` neighborhoods the net gain is `< +5` blocks or if gain-per-1000 neighborhoods is not above the current round's late-stage baseline.
12. round_0003: Cap-9-centered coupled LNS with two-step neighborhoods (`k=3..6` then `k=2..4` on the same motif) plus short neutral rebalancing sweeps will outperform independent random neighborhoods from `21090`.

## Mandatory Next-Round Discipline
1. Keep notes sections non-empty: `Core advance`, `Observations`, `Next-hypothesis`.
2. Every hypothesis must include: mechanism, expected metric movement, and stop condition.
3. Preserve exactness-first artifacts (overcovered=0 candidates) even if scalar score is lower.
4. Update this transfer file at round close to avoid losing accumulated reasoning.

