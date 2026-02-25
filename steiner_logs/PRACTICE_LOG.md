# Global Practice Log (Rounds2-5)

Generated (UTC): 2026-02-22T16:50:46.240550+00:00
Log root: steiner_logs
Current run dir: /root/openquestions/steiner_logs/run_20260222_154119

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
| run_20260221_013905 | 2 | S(6,7,17) | 48.37 | false | 7812/12376 | 4564 | 0 |
| run_20260221_013905 | 3 | S(7,8,18) | 40.56 | false | 18312/31824 | 13512 | 0 |
| run_20260221_013905 | 4 | S(8,9,19) | 33.25 | false | 39546/75582 | 36036 | 0 |
| run_20260221_013905 | 5 | S(9,10,20) | 27.83 | false | 81380/167960 | 86580 | 0 |
| run_20260222_012007 | 2 | S(6,7,23) | 50.09 | false | 64960/100947 | 35987 | 0 |
| run_20260222_012007 | 3 | S(7,8,20) | 43.9 | false | 46456/77520 | 31064 | 0 |
| run_20260222_012007 | 4 | S(8,9,21) | 35.16 | false | 109242/203490 | 94248 | 0 |
| run_20260222_012007 | 5 | S(9,10,22) | 26.85 | false | 237520/497420 | 259900 | 0 |
| run_20260222_052536 | 2 | S(6,8,29) | 0 | false | 123256/475020 | 351764 | 0 |
| run_20260222_052536 | 3 | S(7,8,24) | 28.22 | false | 168640/346104 | 177464 | 0 |
| run_20260222_052536 | 4 | S(8,9,21) | 36.51 | false | 111204/203490 | 92286 | 0 |
| run_20260222_052536 | 5 | S(9,10,22) | 28.01 | false | 241650/497420 | 255770 | 0 |
| run_20260222_135457 | 2 | S(6,7,19) | 50.59 | false | 17556/27132 | 9576 | 0 |
| run_20260222_154119 | 2 | S(6,7,23) | 50.16 | false | 65009/100947 | 35938 | 0 |
| run_20260222_154119 | 3 | S(7,8,24) | 28.25 | false | 168720/346104 | 177384 | 0 |
| run_20260222_154119 | 4 | S(8,9,25) | 24.35 | false | 497106/1081575 | 584469 | 0 |
| run_20260222_154119 | 5 | S(9,10,26) | 15.44 | false | 1237250/3124550 | 1887300 | 0 |

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
- run_20260221_013905/round_0002
  - advance: Established a reproducible strict-feasible balance-improvement lane for `S(6,7,17)` that improves structural pressure metrics even when block-count augmentations are absent.
  - advance: Executed mandatory symmetry-first gate with explicit orbit/coefficient diagnostics and bounded probes before fallback.
  - advance: Ran three augmentation-focused stages (`C1..C3`) totaling `>85k` neighborhood/augmentation attempts without strict block-count gain.
  - advance: Found a strict-feasible improved certificate with unchanged coverage metrics but better balance:
  - advance: point-degree spread `24 -> 19` (`445..469 -> 449..468`),
  - next-hypothesis: Two-phase strict-feasible search (`balance-first neutral repack -> motif-coupled exact augment`) will break the `1116` plateau where augment-only scans fail.
  - next-hypothesis: Reducing point-degree and cap-tail concentration relaxes local `(r-1)` bottlenecks, increasing the chance that `k -> k+1` exact micro-packs become feasible in the same motif neighborhoods.
  - next-hypothesis: improve `1116 -> 1118..1122` blocks,
  - next-hypothesis: reduce uncovered by `14..42`,
  - next-hypothesis: keep `overcovered=0`, `oversubscribed_(r-1)=0`, `r_minus_1_max_degree <= 6`,
- run_20260221_013905/round_0003
  - advance: Built a reproducible strict-feasible augment loop for `S(7,8,18)` that combines a bounded symmetry gate with motif-coupled `1->2` and reserve-aware `2->3` LNS repacks, yielding monotone verifier gains.
  - advance: Symmetry lane was executed first and rejected with explicit `C18/D18` orbit/coefficient diagnostics plus bounded DFS outcomes.
  - advance: Candidate improved `2252 -> 2289` blocks (`+37`) with strict invariants preserved.
  - advance: Verifier moved `score 39.26 -> 40.56`, `exact_once 18016 -> 18312`, `uncovered 13808 -> 13512`, `overcovered 0 -> 0`.
  - advance: Structural pressure also improved (`point_degree_gap 135 -> 125`).
  - next-hypothesis: Alternating motif-coupled `2->3` and small-window `3->4` exact local repacks (with canonical motif dedup) will extend strict gains beyond `2289`.
  - next-hypothesis: After `1->2` saturation, remaining improvements likely require releasing larger transient slack around the same saturated 6-subset clusters; `3->4` windows can exploit combinations that pairwise scans cannot see.
  - next-hypothesis: Improve `2289 -> 2293..2301` blocks,
  - next-hypothesis: reduce uncovered by `32..96`,
  - next-hypothesis: keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 6`.
- run_20260221_013905/round_0004
  - advance: Broke the `S(8,9,19)` strict-feasible `4392` plateau with a symmetry-gated, motif-coupled `1->2` exact-repair lane while preserving all hard verifier invariants.
  - advance: Mandatory symmetry gate was executed first, including a fresh cyclic orbit re-probe and bounded DFS before fallback.
  - advance: Candidate improved `4392 -> 4394` (`+2`) with strict invariants intact.
  - advance: Verifier moved:
  - advance: `score 33.22 -> 33.25`,
  - next-hypothesis: Two-step coupled `1->2` chains around the same saturated 7-subset cluster, with short motif-taboo and canonical neighborhood dedup, will outperform uncoupled single-neighborhood scans from `4394`.
  - next-hypothesis: Successful `1->2` moves appear as sparse events; immediately reusing the same loosened motif neighborhood should exploit transient slack before cap pressure re-hardens.
  - next-hypothesis: improve `4394 -> 4397..4406` blocks,
  - next-hypothesis: reduce uncovered by `27..108`,
  - next-hypothesis: keep `overcovered=0`, `oversubscribed_(r-1)=0`, `r_minus_1_max_degree <= 6`.
- run_20260221_013905/round_0005
  - advance: Established a practical strict-feasible `r=9` plateau-breaker for this run by combining a mandatory symmetry front gate with fast exact `1->2` micro-augment repairs after add-only exhaustion.
  - advance: Stage A symmetry was gated first and rejected using cached deterministic `C20/D20` diagnostics.
  - advance: Stage B add-only strict pass produced `0` gains.
  - advance: Stage C micro-augment lane produced `+18` strict blocks (`8120 -> 8138`) with verifier movement `score 27.68 -> 27.83`, `exact_once 81200 -> 81380`, `uncovered 86760 -> 86580`.
  - advance: Feasibility invariants remained strict: `overcovered=0`, `oversubscribed_(r-1)=0`.
  - next-hypothesis: Coupled `1->2 -> 1->2` chains on the same saturated 8-subset motif, with short motif-taboo and canonical neighborhood dedup, will outperform uncoupled random motif selection from `8138`.
  - next-hypothesis: Successful first augmentations indicate transient slack near the released motif. Reusing that motif before pressure re-hardens should increase second-step augment probability.
  - next-hypothesis: Improve `8138 -> 8155..8195` blocks,
  - next-hypothesis: reduce uncovered by `170..570`,
  - next-hypothesis: keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 6`.
- run_20260222_012007/round_0002
  - advance: Established a reproducible strict-feasible plateau-break path for `S(6,7,23)` by combining a mandatory symmetry front gate with uncovered-driven LNS destroy/repack intensification.
  - advance: Symmetry gate executed first with explicit orbit/coefficient diagnostics and an actual cyclic packed trial.
  - advance: Add-only strict stage confirmed plateau (`9237 -> 9237`).
  - advance: LNS stages advanced the strict frontier `9237 -> 9280` with monotone uncovered reduction `36288 -> 35987` and `overcovered=0` throughout.
  - advance: Point-degree spread improved `426 -> 413` while preserving `(r-1)` max at target (`9`).
  - next-hypothesis: Two-step motif-coupled LNS chains (reusing the same uncovered motif neighborhood across consecutive windows) with periodic neutral rebalance sweeps will outperform uncoupled random-window LNS from `9280`.
  - next-hypothesis: First-window success opens transient local slack; immediate reuse of that motif should increase second-window augment probability before constraints re-harden.
  - next-hypothesis: Periodic neutral rebalance reduces degree-tail concentration, which should increase feasible refill options in later windows.
  - next-hypothesis: Improve `9280 -> 9310..9380` blocks,
  - next-hypothesis: reduce uncovered by `210..700`,
- run_20260222_012007/round_0003
  - advance: Established a reproducible strict-feasible improvement loop for `S(7,8,20)` that combines mandatory symmetry triage with uncovered-driven `k -> k+1` LNS repacks.
  - advance: Symmetry gate executed first with explicit orbit diagnostics and bounded packed probes.
  - advance: Stage-B seed frontier improved to `5634` blocks, then Stage-C LNS improved to `5807` (`+173` from seed, `+256` from round start).
  - advance: Verifier movement: `score 40.20 -> 43.90`, `exact_once 44408 -> 46456`, `uncovered 33112 -> 31064`, `overcovered=0` unchanged.
  - advance: `(r-1)` hard gate remained strict: max `7` at target and oversubscribed count `0` throughout.
  - next-hypothesis: Two-step motif reuse with larger windows (`k=2..4`) and short motif-taboo will improve gain-per-1000 trials beyond the current `k<=3` loop from `5807`.
  - next-hypothesis: First accepted exchange releases local row/six-subset slack around the same uncovered motif; immediate reuse before re-hardening should increase second-step augment probability.
  - next-hypothesis: improve `5807 -> 5850..5920` blocks,
  - next-hypothesis: reduce uncovered by `344..904`,
  - next-hypothesis: keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 7`.
- run_20260222_012007/round_0004
  - advance: Established the first strict-feasible improving frontier for `S(8,9,21)` in this repository by executing the mandatory symmetry gate, proving add-only exhaustion, and then extracting monotone gains with larger-window motif-coupled LNS under hard verifier constraints.
  - advance: Stage A symmetry was executed first and rejected on quality, not on missing diagnostics.
  - advance: Stage B add-only produced `0` gains despite large attempt budgets.
  - advance: Stage C LNS passes yielded `+31` net strict blocks (`12107 -> 12138`) with verifier movement:
  - advance: `score 34.97 -> 35.16`,
  - next-hypothesis: Two-step motif reuse with medium-large windows (`k=4..10`) around the same capped `7`-subset cluster, interleaved with short neutral rebalance sweeps, will increase net gain-per-1000 trials beyond the current sparse baseline.
  - next-hypothesis: First accepted windows create transient local slack around the released capped motif. Immediate reuse of the same motif before re-hardening should raise second-window success probability; neutral sweeps reduce degree-tail concentration and enlarge feasible refill options.
  - next-hypothesis: Improve `12138 -> 12170..12260` blocks,
  - next-hypothesis: reduce uncovered by `288..1098`,
  - next-hypothesis: keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 7`.
- run_20260222_012007/round_0005
  - advance: Established a symmetry-led strict construction path for `S(9,10,22)` that reaches a strong no-collision frontier and then improves it with strict `k -> k+1` LNS repacks.
  - advance: Stage A symmetry diagnostics were executed first and passed tractability checks (`C22` non-binary columns only `48/29414`).
  - advance: Cyclic orbit-packed seed immediately produced `23716` strict-feasible blocks with `score=26.75`, `overcovered=0`, `oversubscribed_(r-1)=0`.
  - advance: Stage B strict add-only raised this to `23738` (`score=26.81`).
  - advance: Stage C strict LNS raised to `23752` (`score=26.85`, `exact_once=237520`, `uncovered=259900`) while preserving all hard invariants.
  - next-hypothesis: Medium-window strict local exact repacks (`k=4..10`) centered on cap-7 `8`-subset tails will outperform the current small-window strict LNS at this frontier.
  - next-hypothesis: Current accepted moves are sparse because small windows expose too little combinational slack.
  - next-hypothesis: Releasing slightly larger coupled neighborhoods around tight `8`-faces should expose additional strict `k -> k+1` augment opportunities while keeping `overcovered=0`.
  - next-hypothesis: Improve `23752 -> 23810..23960` blocks.
  - next-hypothesis: Reduce uncovered by `580..2080`.
- run_20260222_052536/round_0002
  - advance: Established a strict symmetry-seeded construction path for `S(6,8,29)` and moved the instance from empty start to a reusable strict frontier (`4402` blocks) with zero collisions.
  - advance: Stage A symmetry was executed first and accepted as tractable (`C29` sample non-binary share `0.83%`, `max_coeff=2`; `117` accepted cyclic orbits).
  - advance: Stage B + continuations improved strict frontier `3393 -> 4402` while keeping `overcovered=0` and `(r-1)` oversubscription `0`.
  - advance: Verifier movement: `exact_once 0 -> 123256`, `uncovered 475020 -> 351764`, `overcovered 0 -> 0`.
  - advance: Stage C LNS was explicitly tested (`k>1`) but delivered sparse net gains at this frontier.
  - next-hypothesis: For `S(6,8,29)`, a two-phase strict policy (`cyclic orbit seed -> long uncovered-driven add-only continuation`) will outperform short-window strict LNS in uncovered reduction under matched compute budgets.
  - next-hypothesis: The current candidate still has substantial strict slack (`r_minus_1_max_degree=6 < 8`), so strict additions can continue to harvest uncovered 6-subsets efficiently.
  - next-hypothesis: Short LNS windows are currently opening little additional local slack relative to their search cost.
  - next-hypothesis: Improve `4402 -> 5000..5800` blocks.
  - next-hypothesis: Reduce uncovered by `16800..39200`.
- run_20260222_052536/round_0003
  - advance: Established the first strong strict-feasible certificate frontier for `S(7,8,24)` in this repo using a symmetry-seeded + strict-LNS pipeline.
  - advance: Candidate improved from empty to `21080` strict-feasible blocks.
  - advance: Verifier moved to `score=28.22`, `exact_once=168640/346104`, `uncovered=177464`, while preserving `overcovered=0` and zero `(r-1)` oversubscription.
  - advance: Mandatory architecture was executed in full order: symmetry gate -> reserve-first boosting -> LNS repack -> residual gate.
  - advance: Reuse cyclic orbit seed generation as default Stage A for this instance.
  - next-hypothesis: On this frontier, hotspot-guided medium-window strict repacks (`k=4..10`) targeted at near-cap 6-subsets will outperform current mixed local/global LNS neighborhoods.
  - next-hypothesis: Current LNS acceptance is low because neighborhoods are broad and weakly coupled to pressure motifs.
  - next-hypothesis: Centering destroy/repack windows on high-load 6-subsets should expose more feasible `k -> k+1` opportunities while preserving strict gates.
  - next-hypothesis: Improve `21080 -> 21250..21650` blocks.
  - next-hypothesis: Reduce uncovered by `1360..4560`.
- run_20260222_052536/round_0004
  - advance: Established a reproducible strict frontier lift for `S(8,9,21)` by coupling a mandatory symmetry gate with high-yield exact local repacks from the incumbent candidate.
  - advance: Score improved `35.16 -> 36.51`.
  - advance: Exact-once improved `109242 -> 111204`.
  - advance: Uncovered reduced `94248 -> 92286` with `overcovered=0` unchanged.
  - advance: `(r-1)` hard cap stayed tight (`7/7`) with zero oversubscription.
  - next-hypothesis: Conflict-core-guided `k>1` repacks (remove blocks around the same low-conflict 8-subset interaction graph, then solve local refill exactly) will outperform the current generic overlap-based `k>1` neighborhoods at the `12356` strict frontier.
  - next-hypothesis: Stage B gains indicate many profitable moves are very local and structured; targeting neighborhoods built from actual conflict-1/conflict-2 block interactions should raise refill quality and unlock true `k -> k+1` gains.
  - next-hypothesis: Improve to `12380..12440` blocks,
  - next-hypothesis: reduce uncovered by `216..756`,
  - next-hypothesis: keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree<=7`.
- run_20260222_052536/round_0005
  - advance: Established a high-yield strict improvement regime for `S(9,10,22)` that pushes the certified zero-collision frontier from `23752` to `24165` blocks without violating `(r-1)` caps.
  - advance: Score improved `26.85 -> 28.01`.
  - advance: Exact-once increased `237520 -> 241650`.
  - advance: Uncovered reduced `259900 -> 255770` with `overcovered=0` maintained.
  - advance: `(r-1)` load stayed `7/7` with `oversubscribed_(r-1)=0` throughout.
  - next-hypothesis: Two-tier strict neighborhoods (`1->2` for rapid gains plus periodic `k=2..4 -> k+1` exact micro-packs) will improve gain-per-time over `1->2`-only continuation from this new frontier.
  - next-hypothesis: `1->2` quickly exploits immediate local slack; periodic larger windows should unlock motifs that single-block release cannot expose.
  - next-hypothesis: Move `24165 -> 24350..24750` blocks under unchanged strict gates.
  - next-hypothesis: Reduce uncovered by `1850..5850` while keeping `overcovered=0` and `(r-1)` oversubscription `0`.
  - next-hypothesis: Reject if after `>=12000` mixed neighborhoods the net gain is `< +120` blocks or if gain-per-1000 neighborhoods under mixed windows is not above `1->2`-only baseline.
- run_20260222_135457/round_0002
  - advance: Established the first strict-feasible constructive frontier for `S(6,7,19)` in this run, moving from `2438` to `2508` blocks while preserving zero collisions and zero `(r-1)` oversubscription.
  - advance: Score improved `48.06 -> 50.59`.
  - advance: Exact-once increased `17066 -> 17556`.
  - advance: Uncovered reduced `10066 -> 9576` with `overcovered=0` maintained.
  - advance: `(r-1)` load stayed at cap `7/7` with oversubscribed count always `0`.
  - next-hypothesis: A two-tier strict schedule (pressure-relief neutral repacks followed by improvement-only repacks) will continue improving this frontier beyond `2508` blocks without violating strict gates.
  - next-hypothesis: Neutral repacks lower local 5-subset saturation, creating new feasible `k->k+1` repack opportunities that add-only cannot see.
  - next-hypothesis: Move `2508 -> 2518..2558` blocks under unchanged strict gates.
  - next-hypothesis: Reduce uncovered by `70..350` while keeping `overcovered=0` and `(r-1)` oversubscription `0`.
  - next-hypothesis: Keep `r_minus_1_max_degree=7` and hold point-degree gap near or below `~110`.
- run_20260222_154119/round_0002
  - advance: Broke the long-standing strict `S(6,7,23)` frontier from `9280` to `9287` blocks while preserving `overcovered=0` and zero `(r-1)` oversubscription.
  - advance: Score improved `50.09 -> 50.16`.
  - advance: Exact-once improved `64960 -> 65009`.
  - advance: Uncovered reduced `35987 -> 35938` with `overcovered=0` unchanged.
  - advance: `(r-1)` load remained at cap (`9/9`) with oversubscribed count `0` throughout.
  - next-hypothesis: A motif-coupled mixed-window strict LNS schedule (`k=2..5` core plus periodic `k=6..8` bursts) starting from the new `9287` frontier will outperform fixed-window continuation.
  - next-hypothesis: Small windows keep acceptance rate nonzero; periodic larger windows can cross the residual local bottlenecks that blocked further `+1` gains after trial ~700.
  - next-hypothesis: Improve `9287 -> 9300..9340` blocks.
  - next-hypothesis: Reduce uncovered by `91..371` while keeping `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree<=9`.
  - next-hypothesis: Reject this hypothesis if after `>=30000` neighborhoods the net gain is `< +5` blocks or if gain-per-1000 neighborhoods is not above the current round's late-stage baseline.
- run_20260222_154119/round_0003
  - advance: Improved the strict `S(7,8,24)` frontier from `21080` to `21090` blocks with all hard verifier gates intact.
  - advance: Score improved `28.22 -> 28.25`.
  - advance: Exact-once improved `168640 -> 168720`.
  - advance: Uncovered reduced `177464 -> 177384`.
  - advance: `overcovered=0` preserved and `oversubscribed_(r-1)=0` preserved.
  - next-hypothesis: Cap-9-centered coupled LNS with two-step neighborhoods (`k=3..6` then `k=2..4` on the same motif) plus short neutral rebalancing sweeps will outperform independent random neighborhoods from `21090`.
  - next-hypothesis: Current failures suggest transient slack collapses before reuse. Immediate motif reuse should exploit that slack window; neutral rebalancing should reduce point-degree tail pressure and reopen feasible fills.
  - next-hypothesis: Improve `21090 -> 21120..21210` blocks.
  - next-hypothesis: Reduce uncovered by `240..960`.
  - next-hypothesis: Keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 9`.
- run_20260222_154119/round_0004
  - advance: Established the first strict-feasible frontier for `S(8,9,25)` in this repository by moving from empty candidate to `55234` blocks while preserving zero collisions and zero `(r-1)` oversubscription.
  - advance: Score improved `0.00 -> 24.35`.
  - advance: Exact-once improved `0 -> 497106`.
  - advance: Uncovered reduced `1081575 -> 584469` with `overcovered=0` throughout.
  - advance: `(r-1)` load stayed below cap (`max 8` vs target `9`), oversubscribed count `0`.
  - next-hypothesis: An alternating tri-phase loop (`short orbit micro-burst -> uncovered-driven nibble -> motif-coupled LNS with larger windows k=4..7`) will outperform repeating nibble+LNS alone from `55234`.
  - next-hypothesis: Orbit micro-bursts inject globally balanced fresh structure; nibble captures low-hanging uncovered 8-subsets; larger-window LNS can repack local bottlenecks that block single-block additions once acceptance decays.
  - next-hypothesis: Improve `55234 -> 56000..57500` blocks.
  - next-hypothesis: Reduce uncovered by `6900..20300`.
  - next-hypothesis: Keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 9`.
- run_20260222_154119/round_0005
  - advance: Established the first strict-feasible frontier for `S(9,10,26)` in this repository by moving from empty candidate to `123725` blocks while preserving `overcovered=0` and zero `(r-1)` oversubscription.
  - advance: Score improved `0.00 -> 15.44`.
  - advance: Exact-once improved `0 -> 1237250`.
  - advance: Uncovered reduced `3124550 -> 1887300`.
  - advance: `(r-1)` cap discipline held (`max 9`, target `9`, oversubscribed count `0`).
  - next-hypothesis: A four-phase strict loop (`short cyclic orbit micro-burst -> uncovered-driven add-only -> motif-coupled mixed-window LNS (k=3..7) -> short revision sweep`) will outperform the current fixed-budget schedule from `123725`.
  - next-hypothesis: orbit micro-bursts refresh global balance; add-only captures easy uncovered mass; larger-window repacks release local cap bottlenecks that small windows miss; revision sweep harvests reopened slack.
  - next-hypothesis: Improve `123725 -> 127000..134000` blocks.
  - next-hypothesis: Reduce uncovered by `32750..102750`.
  - next-hypothesis: Keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 9`.
