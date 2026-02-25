# Repo-Wide Steiner History

Generated (UTC): 2026-02-22T10:16:43.045741+00:00
Log root: steiner_logs
Current run dir: /root/openquestions/steiner_logs/run_20260222_101642

- Total run dirs found: 25
- Prior run dirs found: 24
- Meaningful prior run dirs found: 7
- Latest prior run: run_20260222_052536

## Best Known By Instance (across all runs)
| Instance | Score | Run | Round | Valid | Exact Once | Uncovered | Overcovered |
|---|---:|---|---:|---|---|---:|---:|
| S(6,7,17) | 66.04 | run_20260219_030101 | 2 | ? | 9591/12376 | 1575 | 1210 |
| S(6,7,19) | 0.00 | run_20260222_093016 | 1 | false | 0/27132 | 27132 | 0 |
| S(6,7,23) | 50.09 | run_20260222_012007 | 2 | false | 64960/100947 | 35987 | 0 |
| S(6,8,29) | 0.00 | run_20260222_043844 | 1 | false | 0/475020 | 475020 | 0 |
| S(7,8,18) | 60.35 | run_20260219_180444 | 3 | false | 23521/31824 | 4793 | 3510 |
| S(7,8,20) | 43.90 | run_20260222_012007 | 3 | false | 46456/77520 | 31064 | 0 |
| S(7,8,24) | 28.22 | run_20260222_052536 | 3 | false | 168640/346104 | 177464 | 0 |
| S(8,9,19) | 57.49 | run_20260219_180444 | 4 | false | 54475/75582 | 12247 | 8860 |
| S(8,9,21) | 36.51 | run_20260222_052536 | 4 | false | 111204/203490 | 92286 | 0 |
| S(9,10,20) | 55.44 | run_20260219_180444 | 5 | false | 118787/167960 | 28530 | 20643 |
| S(9,10,22) | 28.01 | run_20260222_052536 | 5 | false | 241650/497420 | 255770 | 0 |

## Latest Prior Run Key Notes
- Latest prior run: run_20260222_052536
- Latest run with round1 notes: run_20260222_052536
- Latest run with round5 notes: run_20260222_052536
- Round1 notes: steiner_logs/run_20260222_052536/notes/round_0001_notes.md
- Round5 notes: steiner_logs/run_20260222_052536/notes/round_0005_notes.md

### Round1 Core advance excerpt
- advance statement:
-   - Converted round1 for `S(6,8,29)` into a proof-first, gate-explicit execution contract with five seeded proof lanes and a 3-round critical-gap verification loop.
- evidence from this round (metrics, runtime, structure):
-   - Mandatory cross-run memory and local-paper-first conditions were completed.
-   - Strong search stack and concise engine selector were formalized.
-   - Practice blockers are mapped to explicit implementation changes for rounds2+.
- transfer value for next rounds:
-   - Future rounds can execute without re-deriving proof structure.
-   - Engine switches and residual exact-cover activation are now gate-based and falsifiable.

### Round5 Core advance excerpt
- advance statement:
-   - Established a high-yield strict improvement regime for `S(9,10,22)` that pushes the certified zero-collision frontier from `23752` to `24165` blocks without violating `(r-1)` caps.
- evidence from this round (metrics, runtime, structure):
-   - Score improved `26.85 -> 28.01`.
-   - Exact-once increased `237520 -> 241650`.
-   - Uncovered reduced `259900 -> 255770` with `overcovered=0` maintained.
-   - `(r-1)` load stayed `7/7` with `oversubscribed_(r-1)=0` throughout.
- transfer value for next rounds:
-   - Re-use alternating strict add-only sweeps and motif-coupled strict repack waves as default late-stage policy for this instance.
-   - Keep strict gates hard; they did not block progress and preserved transferability.

