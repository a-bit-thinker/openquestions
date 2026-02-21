# Next Generation Transfer

Generated (UTC): 2026-02-21T00:28:07.874545+00:00
Run directory: steiner_logs/run_20260220_222441

## Scope
- This document summarizes the latest five rounds (or fewer if run is shorter).
- Goal: preserve proven progress and pass explicit next hypotheses to the next run/agent.

## Latest Round Snapshot
- Round: 4 (solve)
- Instance: S(8,9,19)
- Score: 33.22
- Valid: false
- Exact once: 39528/75582
- Uncovered: 36054
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
| 3 | solve | S(7,8,18) | 39.26 | false | 18016/31824 | 13808 | 0 |
| 4 | solve | S(8,9,19) | 33.22 | false | 39528/75582 | 36054 | 0 |

## Core Advances (Rounds 1-5 Window)
- round_0001: Converted prior heuristic policy into a source-backed, transfer-ready dual-engine protocol with explicit switch rules and per-`r` consequences.
- round_0001: Mandatory cross-run reads completed first, then targeted paper search.
- round_0001: Added six primary sources to the cache and linked each to concrete implementation actions for `r=6,7,8,9`.
- round_0001: Captured round-2+ stage execution order and mandatory metric set.
- round_0001: Next rounds can execute directly from the stage protocol without re-deriving theory.
- round_0001: Engine selection now has explicit criteria instead of ad-hoc switching.
- round_0002: Added an exact local augmenting-repack lane (`1->2`, `2->3`, `3->4`) on top of the strict-feasible LNS pipeline and obtained a verified strict-feasible improvement beyond the long-standing `1115` plateau.
- round_0002: Symmetry front gate was executed first and rejected by bounded diagnostics (`Z_17` and `D_17` both unsolved).
- round_0002: Reserve-aware LNS preserved feasibility but did not improve block count.
- round_0002: Exact local augmentation found one successful strict augmenting move over `19846` trials: `1115 -> 1116` blocks.
- round_0002: Verifier moved `score 48.29 -> 48.37`, `exact_once 7805 -> 7812`, `uncovered 4571 -> 4564`, while keeping `overcovered=0` and `(r-1)` oversubscription `=0`.
- round_0002: Keep symmetry diagnostics as mandatory Stage A, then switch quickly when bounded probes stall.
- round_0002: Preserve strict gates and reserve-aware refill, but add exact local augmentation as a required Stage C component.
- round_0002: Treat augmenting moves as sparse events; run high-trial-count motif-targeted neighborhoods rather than broad random LNS only.
- round_0003: Achieved a new strict-feasible best for this run/instance (`2251 -> 2252`) under the mandated symmetry-first then reserve-aware LNS architecture.
- round_0003: Stage A symmetry lane was explicitly gated first (reused deterministic `C18/D18` diagnostics, non-tractable in budget).
- round_0003: Stage B/C pipeline produced net strict gain with hard invariants preserved.
- round_0003: Verifier movement: `score 39.22 -> 39.26`, `exact_once 18008 -> 18016`, `uncovered 13816 -> 13808`, `overcovered=0` unchanged, `(r-1)` oversubscription `0` unchanged.
- round_0003: Keep strict gates and reserve-first refill.
- round_0003: Keep motif-targeted destroy + local near-exact repack, but treat gains as sparse and require many neighborhoods.

## Knowledge Gaps / Blockers
- No fully valid certificate yet; current frontier remains partial.
- Large uncovered residual remains; prioritize structured completion over random mutation.

## Next Hypothesis Ladder (for next generation)
1. round_0001: A fixed symmetry budget plus early fallback into absorber-aware repair will outperform symmetry-heavy attempts on `r=8,9` while preserving strict feasibility.
2. round_0001: Prior diagnostics show non-binary orbit inflation at larger `r`; longer symmetry search has low marginal value compared with repair passes that directly reduce uncovered mass.
3. round_0001: `r=6,7`: better early exact-once growth from selective symmetry wins.
4. round_0001: `r=8,9`: lower uncovered at fixed compute budget; maintain `overcovered=0` and `oversubscribed_(r-1)=0`.
5. round_0001: Reject the hypothesis if bounded symmetry probes consistently produce high-quality binary reductions (or exact progress) for `r=8,9` within the same budget.
6. round_0002: Chain two motif-coupled exact augmentations around the same saturated 5-subset cluster to convert sparse single-step gains into repeated gains.
7. round_0002: The successful `+1` move indicates hidden augmenting structure still exists; coupling consecutive destroy sets to the same saturated motif should preserve released slack long enough for a second augmentation before pressure re-hardens.
8. round_0002: Improve from `1116` to `1118..1124` blocks,
9. round_0002: reduce uncovered by `14..56`,
10. round_0002: keep `overcovered=0`, `oversubscribed_(r-1)=0`, `r_minus_1_max_degree <= 6`.
11. round_0002: Stop this hypothesis if after `>=60000` exact local augmentation trials the gain is `< +2` blocks total, or if successful augmentations remain isolated with no second-step chain in the same motif neighborhood.
12. round_0003: Two-step coupled motif neighborhoods (reuse the same saturated 6-subset cluster across consecutive destroys) plus a bounded exact micro-augment (`1->2`, `2->3`) will break the `2252` plateau.

## Mandatory Next-Round Discipline
1. Keep notes sections non-empty: `Core advance`, `Observations`, `Next-hypothesis`.
2. Every hypothesis must include: mechanism, expected metric movement, and stop condition.
3. Preserve exactness-first artifacts (overcovered=0 candidates) even if scalar score is lower.
4. Update this transfer file at round close to avoid losing accumulated reasoning.

