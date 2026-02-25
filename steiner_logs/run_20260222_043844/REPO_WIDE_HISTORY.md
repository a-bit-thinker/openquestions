# Repo-Wide Steiner History

Generated (UTC): 2026-02-22T04:38:45.788122+00:00
Log root: steiner_logs
Current run dir: /root/openquestions/steiner_logs/run_20260222_043844

- Total run dirs found: 17
- Prior run dirs found: 16
- Meaningful prior run dirs found: 6
- Latest prior run: run_20260222_012007

## Best Known By Instance (across all runs)
| Instance | Score | Run | Round | Valid | Exact Once | Uncovered | Overcovered |
|---|---:|---|---:|---|---|---:|---:|
| S(6,7,17) | 66.04 | run_20260219_030101 | 2 | ? | 9591/12376 | 1575 | 1210 |
| S(6,7,23) | 50.09 | run_20260222_012007 | 2 | false | 64960/100947 | 35987 | 0 |
| S(6,8,29) | 0.00 | run_20260222_043844 | 1 | false | 0/475020 | 475020 | 0 |
| S(7,8,18) | 60.35 | run_20260219_180444 | 3 | false | 23521/31824 | 4793 | 3510 |
| S(7,8,20) | 43.90 | run_20260222_012007 | 3 | false | 46456/77520 | 31064 | 0 |
| S(8,9,19) | 57.49 | run_20260219_180444 | 4 | false | 54475/75582 | 12247 | 8860 |
| S(8,9,21) | 35.16 | run_20260222_012007 | 4 | false | 109242/203490 | 94248 | 0 |
| S(9,10,20) | 55.44 | run_20260219_180444 | 5 | false | 118787/167960 | 28530 | 20643 |
| S(9,10,22) | 26.85 | run_20260222_012007 | 5 | false | 237520/497420 | 259900 | 0 |

## Latest Prior Run Key Notes
- Latest prior run: run_20260222_012007
- Latest run with round1 notes: run_20260222_012007
- Latest run with round5 notes: run_20260222_012007
- Round1 notes: steiner_logs/run_20260222_012007/notes/round_0001_notes.md
- Round5 notes: steiner_logs/run_20260222_012007/notes/round_0005_notes.md

### Round1 Core advance excerpt
- advance statement:
-   - Converted round1 into a proof-first, gate-explicit execution contract for `S(6,7,23)` with five seeded proof lanes and a 3-loop gap verification routine.
- evidence from this round (metrics, runtime, structure):
-   - Mandatory cross-run memory and local-paper-first requirements were completed.
-   - Strong search stack and concise engine selector were formalized for immediate round2 use.
-   - Practice blockers now map to source-backed implementation deltas.
- transfer value for next rounds:
-   - Rounds2+ can execute without re-deriving proof/search structure.
-   - Each stage has explicit stop/switch criteria and required metrics.

### Round5 Core advance excerpt
- advance statement:
-   - Established a symmetry-led strict construction path for `S(9,10,22)` that reaches a strong no-collision frontier and then improves it with strict `k -> k+1` LNS repacks.
- evidence from this round (metrics, runtime, structure):
-   - Stage A symmetry diagnostics were executed first and passed tractability checks (`C22` non-binary columns only `48/29414`).
-   - Cyclic orbit-packed seed immediately produced `23716` strict-feasible blocks with `score=26.75`, `overcovered=0`, `oversubscribed_(r-1)=0`.
-   - Stage B strict add-only raised this to `23738` (`score=26.81`).
-   - Stage C strict LNS raised to `23752` (`score=26.85`, `exact_once=237520`, `uncovered=259900`) while preserving all hard invariants.
- transfer value for next rounds:
-   - Use cyclic orbit-packed strict seed as default starting point for this instance, not empty/random starts.
-   - Keep strict LNS windows as the post-seed augmenter; gains are sparse but stable.
-   - Preserve strict cap gates (`c_9<=1`, `c_8<=7`) as first-line invariants for this instance.

