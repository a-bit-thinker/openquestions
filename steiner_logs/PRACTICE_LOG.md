# Global Practice Log (Rounds2-5)

Generated (UTC): 2026-02-21T01:14:34.507924+00:00
Log root: steiner_logs
Current run dir: /root/openquestions/steiner_logs/run_20260221_011431

## Intent
- Aggregate solver behavior and metrics from rounds 2-5 across runs.
- Feed round1 research updates from real practice bottlenecks.

## Raw Redundancy
- Per-run round logs remain as source of truth under `run_*/notes/round_000{2..5}_notes.md`.

## Practice Trajectory Table
| Run | Round | Instance | Score | Valid | Exact Once | Uncovered | Overcovered |
|---|---:|---|---:|---|---|---:|---:|
| run_20260219_025532 | 2 | S(6,7,17) | 0 | ? | 0/12376 | 12376 | 0 |
| run_20260219_025532 | 3 | S(7,8,18) | 0 | ? | 0/31824 | 31824 | 0 |
| run_20260219_025532 | 4 | S(8,9,19) | 0 | ? | 0/75582 | 75582 | 0 |
| run_20260219_030101 | 2 | S(6,7,17) | 66.04 | ? | 9591/12376 | 1575 | 1210 |
| run_20260219_030101 | 3 | S(7,8,18) | 60.01 | ? | 23438/31824 | 4823 | 3563 |
| run_20260219_030101 | 4 | S(8,9,19) | 57.35 | ? | 54397/75582 | 12276 | 8909 |
| run_20260219_030101 | 5 | S(9,10,20) | 54.95 | ? | 118187/167960 | 28774 | 20999 |
| run_20260219_180444 | 2 | S(6,7,17) | 66.04 | false | 9591/12376 | 1575 | 1210 |
| run_20260219_180444 | 3 | S(7,8,18) | 60.35 | false | 23521/31824 | 4793 | 3510 |
| run_20260219_180444 | 4 | S(8,9,19) | 57.49 | false | 54475/75582 | 12247 | 8860 |
| run_20260219_180444 | 5 | S(9,10,20) | 55.44 | false | 118787/167960 | 28530 | 20643 |
| run_20260220_183105 | 2 | S(6,7,17) | 48.29 | false | 7805/12376 | 4571 | 0 |
| run_20260220_183105 | 3 | S(7,8,18) | 39.22 | false | 18008/31824 | 13816 | 0 |
| run_20260220_183105 | 4 | S(8,9,19) | 33.22 | false | 39528/75582 | 36054 | 0 |
| run_20260220_183105 | 5 | S(9,10,20) | 27.68 | false | 81200/167960 | 86760 | 0 |
| run_20260220_222225 | 2 | S(6,7,17) | 48.29 | false | 7805/12376 | 4571 | 0 |
| run_20260220_222441 | 2 | S(6,7,17) | 48.37 | false | 7812/12376 | 4564 | 0 |
| run_20260220_222441 | 3 | S(7,8,18) | 39.26 | false | 18016/31824 | 13808 | 0 |
| run_20260220_222441 | 4 | S(8,9,19) | 33.22 | false | 39528/75582 | 36054 | 0 |

## Round Highlights
- run_20260219_030101/round_0002
  - advance: Replaced empty candidate `[]` with a fully well-formed 1768-block certificate that substantially improves verifier metrics:
  - advance: Before: `score=0.00`, `exact_once=0/12376`, `uncovered=12376`, `overcovered=0`, `actual_blocks=0`.
  - advance: After: `score=66.04`, `exact_once=9591/12376`, `uncovered=1575`, `overcovered=1210`, `actual_blocks=1768`.
  - next-hypothesis: Continue local search from this 1768-block certificate with stronger neighborhood moves (multi-block trades / tabu memory) to push uncovered and overcovered down further.
- run_20260219_030101/round_0003
  - advance: Replaced empty candidate with a full 3978-block certificate candidate.
  - advance: Metrics improved from:
  - advance: score=0.00, exact_once=0/31824, uncovered=31824, overcovered=0, actual_blocks=0
  - advance: to:
  - advance: score=60.01, exact_once=23438/31824, uncovered=4823, overcovered=3563, overflow_multiplicity=4823, actual_blocks=3978
  - next-hypothesis: Keep block count fixed at 3978 and run conflict-directed swaps focused on 7-subsets with multiplicity >= 2.
  - next-hypothesis: Try occasional neutral/annealed swaps to escape local plateaus while preserving format-validity and block-count constraints.
- run_20260219_030101/round_0004
  - advance: Replaced empty candidate `[]` with a well-formed 8398-block certificate candidate and substantially improved verifier metrics.
  - advance: Before: `score=0.00`, `exact_once=0/75582`, `uncovered=75582`, `overcovered=0`, `actual_blocks=0`.
  - advance: After: `score=57.35`, `exact_once=54397/75582`, `uncovered=12276`, `overcovered=8909`, `overflow_multiplicity=12276`, `actual_blocks=8398`.
  - next-hypothesis: Continue local search from this certificate with larger add-sample neighborhoods and occasional multi-block (2-for-2 / ejection-chain) moves to escape local plateaus.
  - next-hypothesis: Prioritize swaps touching highest-multiplicity `8`-subsets and uncovered hotspots to reduce both uncovered and overcovered counts together.
- run_20260219_030101/round_0005
  - advance: Replaced empty candidate `[]` with a full-size, format-valid 16796-block certificate candidate that substantially improves verifier metrics.
  - advance: Before: `score=0.00`, `exact_once=0/167960`, `uncovered=167960`, `overcovered=0`, `actual_blocks=0`.
  - advance: After: `score=54.95`, `exact_once=118187/167960`, `uncovered=28774`, `overcovered=20999`, `overflow_multiplicity=28774`, `actual_blocks=16796`.
  - next-hypothesis: Continue fixed-size local search with larger add-neighborhood samples and occasional multi-block exchanges to escape local plateaus.
  - next-hypothesis: Target hotspots: 9-subsets currently uncovered and high-multiplicity collisions in the `[0..18]` projection while preserving exact block count.
- run_20260219_180444/round_0002
  - advance: Replaced empty candidate with a high-signal 1768-block admissible certificate and documented symmetry-gate evidence plus LNS repair behavior under this instance.
  - next-hypothesis: Push beyond score 66.04 by targeting moves that reduce `uncovered` without re-inflating `(r-1)` pressure:
  - next-hypothesis: favor remove-sets centered on repeated 6-subsets with high 5-subset tail load,
  - next-hypothesis: solve larger local re-pack neighborhoods (e.g., `k=7..10`) near conflict cores,
  - next-hypothesis: keep a small protected flex pool for late uncovered hotspots.
- run_20260219_180444/round_0003
  - advance: Replaced empty round candidate with a high-signal admissible 3978-block certificate candidate and improved score over prior local seed (`60.01 -> 60.35`) while reducing both uncovered and overcovered 7-subsets.
  - next-hypothesis: Keep fixed block count and continue conflict-directed LNS, but add a secondary balancing term for point-degree spread to control the widened `1756..1785` tail while preserving uncovered/overcovered gains.
- run_20260219_180444/round_0004
  - advance: Replaced empty round candidate with a full-size admissible 8398-block certificate candidate.
  - advance: Final evaluator metrics:
  - advance: `score=57.49`, `is_valid=false`
  - advance: `exact_once=54475/75582`
  - advance: `uncovered=12247`, `overcovered=8860`
  - next-hypothesis: Continue fixed-cardinality LNS with larger neighborhood packs (`k` occasionally >8) and candidate pools centered on both uncovered and high-multiplicity `8`-subset hotspots.
  - next-hypothesis: Add an explicit delete-biased overcoverage reduction phase before refill to reduce the residual overcoverage barrier.
  - next-hypothesis: Re-open residual exact completion only after achieving `overcovered=0` in a late-stage candidate.
- run_20260219_180444/round_0005
  - advance: Replaced empty candidate with a full-size, format-valid `16796`-block certificate candidate.
  - advance: Final evaluator metrics:
  - advance: `score=55.44`, `is_valid=false`
  - advance: `exact_once=118787/167960`
  - advance: `uncovered=28530`, `overcovered=20643`, `overflow_multiplicity=28530`
  - next-hypothesis: Keep fixed-cardinality LNS, but bias removals further toward `c=2` heavy 9-subset collisions before refill.
  - next-hypothesis: Add a dedicated delete-biased overcoverage-burn phase before uncovered-biased refill.
  - next-hypothesis: Re-open residual exact completion only after driving `overcovered_r_subsets` to `0` in late-stage candidates.
- run_20260220_183105/round_0002
  - advance: Established a working symmetry-first then LNS fallback loop that makes monotone progress under strict admissibility and strict collision/`(r-1)` constraints.
  - advance: Symmetry compression was attempted first and diagnosed as currently intractable in bounded budget.
  - advance: LNS destroy/repack raised block count `1088 -> 1115` with no overcoverage and no `(r-1)` oversubscription.
  - advance: Uncovered dropped `4760 -> 4571`; point-degree gap contracted `86 -> 24`.
  - advance: Keep the same strict-feasibility move filter and large-neighborhood repack backbone.
  - next-hypothesis: A cap-aware local exact re-pack on saturated 5-subset neighborhoods will outperform pure greedy local refill and push beyond 1115 blocks.
  - next-hypothesis: Many stalled states are constrained by clusters of 5-subsets already at load 6; targeted destroy around those clusters plus bounded exact local solve should recover more than removed blocks while preserving global feasibility.
  - next-hypothesis: Target `+15..40` blocks from 1115,
  - next-hypothesis: uncovered reduction by `105..280`,
  - next-hypothesis: keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 6`.
- run_20260220_183105/round_0003
  - advance: Implemented a symmetry-first gate plus absorber-reserved LNS pipeline that produced monotone strict-feasible gains for `S(7,8,18)`.
  - advance: Symmetry mode was attempted first and rejected only after concrete orbit diagnostics + bounded search timeout.
  - advance: LNS multi-block destroy/repack improved `2239 -> 2251` blocks (`+12`) with `overcovered=0` and `(r-1)` oversubscription `=0` throughout.
  - advance: Uncovered improved `13912 -> 13816` and point-degree gap improved `179 -> 141`.
  - advance: Keep the same strict row-owner feasibility gate.
  - next-hypothesis: Destroy neighborhoods chosen around saturated `6`-subset motifs (load exactly `6`) will unlock larger positive repacks than pressure-only block destruction.
  - next-hypothesis: Current plateaus are caused by local frozen structures where many candidate blocks are blocked by a small set of tight `(r-1)` faces; targeting those faces should free higher-quality local orbit of alternatives for exact re-pack.
  - next-hypothesis: `+10..25` blocks from `2251`,
  - next-hypothesis: uncovered reduction by `80..200`,
  - next-hypothesis: maintain `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 6`.
- run_20260220_183105/round_0004
  - advance: Implemented a symmetry-first gate plus plateau-crossing LNS pipeline that improves strict-feasible coverage on `S(8,9,19)` while preserving all hard local invariants.
  - advance: Symmetry lane was attempted first (cyclic + dihedral orbit diagnostics + bounded DFS) and rejected with explicit tractability evidence.
  - advance: Candidate improved `4371 -> 4392` blocks (`+21`) with `overcovered=0` and `(r-1)` oversubscription `=0` unchanged.
  - advance: Uncovered improved `36243 -> 36054` (`-189`); point-degree gap improved `298 -> 194`.
  - advance: Keep symmetry-first diagnostics as a short front gate, then switch quickly.
  - next-hypothesis: Motif-targeted destroys centered on saturated 7-subsets (load `=6`) plus bounded local exact re-pack on those neighborhoods will outperform pressure-only destroys.
  - next-hypothesis: The current plateau is driven by tight 7-subset bottlenecks; explicitly removing blocks incident to those bottlenecks should unlock larger local candidate pools where exact/near-exact re-pack can recover more blocks than removed.
  - next-hypothesis: `+10..35` blocks from `4392`,
  - next-hypothesis: uncovered reduction by `90..315`,
  - next-hypothesis: keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 6`.
- run_20260220_183105/round_0005
  - advance: Established a reproducible strict-feasible improvement loop for `S(9,10,20)` that combines a symmetry front gate with reserve-aware multi-pass LNS and yields monotone best-checkpoint progress.
  - advance: Symmetry lane was evaluated first with explicit orbit/multiplicity diagnostics and bounded DFS before fallback.
  - advance: Candidate improved from `5897` to `8120` blocks (`+2223`) while preserving `overcovered=0` and `(r-1)` oversubscription `=0`.
  - advance: Uncovered reduced by `22230` (`108990 -> 86760`); point-degree gap reduced by `1260` (`1511 -> 251`).
  - advance: Keep symmetry diagnostics as mandatory front gate, then switch quickly when non-binary orbit coefficients dominate.
  - next-hypothesis: 8-subset motif-targeted destroy selection plus two-tier refill (local exact micro-pack + global flex) will outperform the current pressure-only remove scoring.
  - next-hypothesis: Current plateaus are driven by dense clusters of 8-subsets already at load `5/6`; explicitly targeting those motifs should free larger compatible local repack opportunities before global fill.
  - next-hypothesis: Improve from `8120` to `8180..8280` blocks,
  - next-hypothesis: reduce uncovered by `600..1600`,
  - next-hypothesis: keep `overcovered=0`, `oversubscribed_(r-1)=0`, `r_minus_1_max_degree <= 6`.
- run_20260220_222441/round_0002
  - advance: Added an exact local augmenting-repack lane (`1->2`, `2->3`, `3->4`) on top of the strict-feasible LNS pipeline and obtained a verified strict-feasible improvement beyond the long-standing `1115` plateau.
  - advance: Symmetry front gate was executed first and rejected by bounded diagnostics (`Z_17` and `D_17` both unsolved).
  - advance: Reserve-aware LNS preserved feasibility but did not improve block count.
  - advance: Exact local augmentation found one successful strict augmenting move over `19846` trials: `1115 -> 1116` blocks.
  - advance: Verifier moved `score 48.29 -> 48.37`, `exact_once 7805 -> 7812`, `uncovered 4571 -> 4564`, while keeping `overcovered=0` and `(r-1)` oversubscription `=0`.
  - next-hypothesis: Chain two motif-coupled exact augmentations around the same saturated 5-subset cluster to convert sparse single-step gains into repeated gains.
  - next-hypothesis: The successful `+1` move indicates hidden augmenting structure still exists; coupling consecutive destroy sets to the same saturated motif should preserve released slack long enough for a second augmentation before pressure re-hardens.
  - next-hypothesis: Improve from `1116` to `1118..1124` blocks,
  - next-hypothesis: reduce uncovered by `14..56`,
  - next-hypothesis: keep `overcovered=0`, `oversubscribed_(r-1)=0`, `r_minus_1_max_degree <= 6`.
- run_20260220_222441/round_0003
  - advance: Achieved a new strict-feasible best for this run/instance (`2251 -> 2252`) under the mandated symmetry-first then reserve-aware LNS architecture.
  - advance: Stage A symmetry lane was explicitly gated first (reused deterministic `C18/D18` diagnostics, non-tractable in budget).
  - advance: Stage B/C pipeline produced net strict gain with hard invariants preserved.
  - advance: Verifier movement: `score 39.22 -> 39.26`, `exact_once 18008 -> 18016`, `uncovered 13816 -> 13808`, `overcovered=0` unchanged, `(r-1)` oversubscription `0` unchanged.
  - advance: Keep strict gates and reserve-first refill.
  - next-hypothesis: Two-step coupled motif neighborhoods (reuse the same saturated 6-subset cluster across consecutive destroys) plus a bounded exact micro-augment (`1->2`, `2->3`) will break the `2252` plateau.
  - next-hypothesis: Single neighborhoods often release slack that is immediately re-hardened by refill; chaining a second destroy around the same motif should exploit transient slack before it collapses.
  - next-hypothesis: `2252 -> 2253..2256` blocks,
  - next-hypothesis: uncovered reduction by `8..32`,
  - next-hypothesis: keep `overcovered=0`, `oversubscribed_(r-1)=0`, `r_minus_1_max_degree <= 6`.
