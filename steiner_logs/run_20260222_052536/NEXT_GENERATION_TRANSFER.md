# Next Generation Transfer

Generated (UTC): 2026-02-22T06:43:36.415020+00:00
Run directory: steiner_logs/run_20260222_052536

## Scope
- This document summarizes the latest five rounds (or fewer if run is shorter).
- Goal: preserve proven progress and pass explicit next hypotheses to the next run/agent.

## Latest Round Snapshot
- Round: 5 (solve)
- Instance: S(9,10,22)
- Score: 28.01
- Valid: false
- Exact once: 241650/497420
- Uncovered: 255770
- Overcovered: 0

## Best Round So Far
- Round: 4 (solve)
- Instance: S(8,9,21)
- Score: 36.51
- Exact once: 111204/203490
- Uncovered: 92286
- Overcovered: 0

## Round Trajectory (recent)
| Round | Mode | Instance | Score | Valid | Exact Once | Uncovered | Overcovered |
|---:|---|---|---:|---|---|---:|---:|
| 1 | research | S(6,8,29) | 0 | false | 0/475020 | 475020 | 0 |
| 2 | solve | S(6,8,29) | 0 | false | 123256/475020 | 351764 | 0 |
| 3 | solve | S(7,8,24) | 28.22 | false | 168640/346104 | 177464 | 0 |
| 4 | solve | S(8,9,21) | 36.51 | false | 111204/203490 | 92286 | 0 |
| 5 | solve | S(9,10,22) | 28.01 | false | 241650/497420 | 255770 | 0 |

## Core Advances (Rounds 1-5 Window)
- round_0001: Converted round1 for `S(6,8,29)` into a proof-first, gate-explicit execution contract with five seeded proof lanes and a 3-round critical-gap verification loop.
- round_0001: Mandatory cross-run memory and local-paper-first conditions were completed.
- round_0001: Strong search stack and concise engine selector were formalized.
- round_0001: Practice blockers are mapped to explicit implementation changes for rounds2+.
- round_0001: Future rounds can execute without re-deriving proof structure.
- round_0001: Engine switches and residual exact-cover activation are now gate-based and falsifiable.
- round_0002: Established a strict symmetry-seeded construction path for `S(6,8,29)` and moved the instance from empty start to a reusable strict frontier (`4402` blocks) with zero collisions.
- round_0002: Stage A symmetry was executed first and accepted as tractable (`C29` sample non-binary share `0.83%`, `max_coeff=2`; `117` accepted cyclic orbits).
- round_0002: Stage B + continuations improved strict frontier `3393 -> 4402` while keeping `overcovered=0` and `(r-1)` oversubscription `0`.
- round_0002: Verifier movement: `exact_once 0 -> 123256`, `uncovered 475020 -> 351764`, `overcovered 0 -> 0`.
- round_0002: Stage C LNS was explicitly tested (`k>1`) but delivered sparse net gains at this frontier.
- round_0002: Keep cyclic orbit-packed seeding as default Stage A on this instance.
- round_0002: Keep strict uncovered-driven add-only continuation as the primary mover after symmetry seed.
- round_0002: Treat short-window LNS as secondary diversification unless acceptance can be improved.
- round_0003: Established the first strong strict-feasible certificate frontier for `S(7,8,24)` in this repo using a symmetry-seeded + strict-LNS pipeline.
- round_0003: Candidate improved from empty to `21080` strict-feasible blocks.
- round_0003: Verifier moved to `score=28.22`, `exact_once=168640/346104`, `uncovered=177464`, while preserving `overcovered=0` and zero `(r-1)` oversubscription.
- round_0003: Mandatory architecture was executed in full order: symmetry gate -> reserve-first boosting -> LNS repack -> residual gate.
- round_0003: Reuse cyclic orbit seed generation as default Stage A for this instance.
- round_0003: Keep strict add-only as the first post-seed mover, then handoff to focused LNS around released motifs.

## Knowledge Gaps / Blockers
- No fully valid certificate yet; current frontier remains partial.
- Large uncovered residual remains; prioritize structured completion over random mutation.

## Next Hypothesis Ladder (for next generation)
1. round_0001: For `S(6,8,29)`, bounded symmetry triage followed by pressure-triggered strict repair handoff will outperform prolonged symmetry-only or add-only policies under matched budgets while keeping strict feasibility.
2. round_0001: It matches prior evidence that add-only phases plateau near saturated `(r-1)` motifs and that symmetry quality is highly instance-dependent.
3. round_0001: faster uncovered reduction slope,
4. round_0001: flatter point-degree spread,
5. round_0001: lower `(r-1)` pressure tail,
6. round_0001: `overcovered=0` and zero `(r-1)` oversubscription maintained.
7. round_0001: Reject after 3 matched seeds if uncovered reduction per fixed budget does not beat add-only baseline or if strict feasibility is violated.
8. round_0002: For `S(6,8,29)`, a two-phase strict policy (`cyclic orbit seed -> long uncovered-driven add-only continuation`) will outperform short-window strict LNS in uncovered reduction under matched compute budgets.
9. round_0002: The current candidate still has substantial strict slack (`r_minus_1_max_degree=6 < 8`), so strict additions can continue to harvest uncovered 6-subsets efficiently.
10. round_0002: Short LNS windows are currently opening little additional local slack relative to their search cost.
11. round_0002: Improve `4402 -> 5000..5800` blocks.
12. round_0002: Reduce uncovered by `16800..39200`.

## Mandatory Next-Round Discipline
1. Keep notes sections non-empty: `Core advance`, `Observations`, `Next-hypothesis`.
2. Every hypothesis must include: mechanism, expected metric movement, and stop condition.
3. Preserve exactness-first artifacts (overcovered=0 candidates) even if scalar score is lower.
4. Update this transfer file at round close to avoid losing accumulated reasoning.

