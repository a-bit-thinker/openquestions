# Next Generation Transfer

Generated (UTC): 2026-02-21T03:46:03.799897+00:00
Run directory: steiner_logs/run_20260221_013905

## Scope
- This document summarizes the latest five rounds (or fewer if run is shorter).
- Goal: preserve proven progress and pass explicit next hypotheses to the next run/agent.

## Latest Round Snapshot
- Round: 5 (solve)
- Instance: S(9,10,20)
- Score: 27.83
- Valid: false
- Exact once: 81380/167960
- Uncovered: 86580
- Overcovered: 0

## Best Round So Far
- Round: 2 (solve)
- Instance: S(6,7,17)
- Score: 48.37
- Exact once: 7812/12376
- Uncovered: 4564
- Overcovered: 0

## Round Trajectory (recent)
| Round | Mode | Instance | Score | Valid | Exact Once | Uncovered | Overcovered |
|---:|---|---|---:|---|---|---:|---:|
| 1 | research | S(6,7,17) | 0 | false | 0/12376 | 12376 | 0 |
| 2 | solve | S(6,7,17) | 48.37 | false | 7812/12376 | 4564 | 0 |
| 3 | solve | S(7,8,18) | 40.56 | false | 18312/31824 | 13512 | 0 |
| 4 | solve | S(8,9,19) | 33.25 | false | 39546/75582 | 36036 | 0 |
| 5 | solve | S(9,10,20) | 27.83 | false | 81380/167960 | 86580 | 0 |

## Core Advances (Rounds 1-5 Window)
- round_0001: Converted round-1 research into a blocker-driven execution contract: bounded symmetry gate, monitored randomized pipeline, weighted-orbit fallback, and explicit handoff triggers.
- round_0001: Mandatory cross-run files were read first.
- round_0001: Added five web/arXiv references tied to explicit `r=6..9` consequences.
- round_0001: Captured round-2+ stage order and metric requirements with concrete switch signals.
- round_0001: Future rounds can execute without re-deriving engine choice rules.
- round_0001: Practice blockers now map directly to source-backed implementation changes.
- round_0002: Established a reproducible strict-feasible balance-improvement lane for `S(6,7,17)` that improves structural pressure metrics even when block-count augmentations are absent.
- round_0002: Executed mandatory symmetry-first gate with explicit orbit/coefficient diagnostics and bounded probes before fallback.
- round_0002: Ran three augmentation-focused stages (`C1..C3`) totaling `>85k` neighborhood/augmentation attempts without strict block-count gain.
- round_0002: Found a strict-feasible improved certificate with unchanged coverage metrics but better balance:
- round_0002: point-degree spread `24 -> 19` (`445..469 -> 449..468`),
- round_0002: cap-6 `5`-subset count `72 -> 69`,
- round_0002: preserved `overcovered=0`, `oversubscribed_(r-1)=0`, `r_minus_1_max_degree=6`.
- round_0002: Keep this balanced `1116`-block checkpoint as the default strict-feasible seed (better-conditioned than prior `1116` seed).
- round_0002: Treat balance-first neutral repacks as a preparatory phase before expensive exact augmenting scans.
- round_0003: Built a reproducible strict-feasible augment loop for `S(7,8,18)` that combines a bounded symmetry gate with motif-coupled `1->2` and reserve-aware `2->3` LNS repacks, yielding monotone verifier gains.
- round_0003: Symmetry lane was executed first and rejected with explicit `C18/D18` orbit/coefficient diagnostics plus bounded DFS outcomes.
- round_0003: Candidate improved `2252 -> 2289` blocks (`+37`) with strict invariants preserved.
- round_0003: Verifier moved `score 39.26 -> 40.56`, `exact_once 18016 -> 18312`, `uncovered 13808 -> 13512`, `overcovered 0 -> 0`.
- round_0003: Structural pressure also improved (`point_degree_gap 135 -> 125`).

## Knowledge Gaps / Blockers
- No fully valid certificate yet; current frontier remains partial.
- Large uncovered residual remains; prioritize structured completion over random mutation.

## Next Hypothesis Ladder (for next generation)
1. round_0001: A short symmetry front gate plus pressure-triggered early handoff to motif-targeted reserve-aware repair will outperform longer symmetry-heavy or additive-only runs for `r=8,9`, while preserving strict feasibility for all `r=6..9`.
2. round_0001: Practice logs show plateaus at saturated `(r-1)` motifs and sparse augmenting moves; early switch avoids wasting budget on structurally mismatched binary-orbit search.
3. round_0001: `r=6,7`: modest but consistent block-count gains from symmetry-aided local exact neighborhoods.
4. round_0001: `r=8,9`: larger uncovered reduction at fixed budget via earlier repair entry and better motif targeting.
5. round_0001: Maintain `overcovered=0` and zero `(r-1)` oversubscription.
6. round_0001: Reject if bounded symmetry probes produce better gain-per-time than early repair across at least three matched seeds, or if early handoff does not improve uncovered reduction rate over baseline.
7. round_0002: Two-phase strict-feasible search (`balance-first neutral repack -> motif-coupled exact augment`) will break the `1116` plateau where augment-only scans fail.
8. round_0002: Reducing point-degree and cap-tail concentration relaxes local `(r-1)` bottlenecks, increasing the chance that `k -> k+1` exact micro-packs become feasible in the same motif neighborhoods.
9. round_0002: improve `1116 -> 1118..1122` blocks,
10. round_0002: reduce uncovered by `14..42`,
11. round_0002: keep `overcovered=0`, `oversubscribed_(r-1)=0`, `r_minus_1_max_degree <= 6`,
12. round_0002: keep point-degree gap `<= 20`.

## Mandatory Next-Round Discipline
1. Keep notes sections non-empty: `Core advance`, `Observations`, `Next-hypothesis`.
2. Every hypothesis must include: mechanism, expected metric movement, and stop condition.
3. Preserve exactness-first artifacts (overcovered=0 candidates) even if scalar score is lower.
4. Update this transfer file at round close to avoid losing accumulated reasoning.

