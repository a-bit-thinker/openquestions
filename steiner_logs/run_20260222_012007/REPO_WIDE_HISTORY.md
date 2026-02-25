# Repo-Wide Steiner History

Generated (UTC): 2026-02-22T02:23:03.798416+00:00
Log root: steiner_logs
Current run dir: /root/openquestions/steiner_logs/run_20260222_012007

- Total run dirs found: 16
- Prior run dirs found: 15
- Meaningful prior run dirs found: 5
- Latest prior run: run_20260221_013905

## Best Known By Instance (across all runs)
| Instance | Score | Run | Round | Valid | Exact Once | Uncovered | Overcovered |
|---|---:|---|---:|---|---|---:|---:|
| S(6,7,17) | 66.04 | run_20260219_030101 | 2 | ? | 9591/12376 | 1575 | 1210 |
| S(6,7,23) | 50.09 | run_20260222_012007 | 2 | false | 64960/100947 | 35987 | 0 |
| S(7,8,18) | 60.35 | run_20260219_180444 | 3 | false | 23521/31824 | 4793 | 3510 |
| S(7,8,20) | 43.90 | run_20260222_012007 | 3 | false | 46456/77520 | 31064 | 0 |
| S(8,9,19) | 57.49 | run_20260219_180444 | 4 | false | 54475/75582 | 12247 | 8860 |
| S(8,9,21) | 35.16 | run_20260222_012007 | 4 | false | 109242/203490 | 94248 | 0 |
| S(9,10,20) | 55.44 | run_20260219_180444 | 5 | false | 118787/167960 | 28530 | 20643 |
| S(9,10,22) | 26.85 | run_20260222_012007 | 5 | false | 237520/497420 | 259900 | 0 |

## Latest Prior Run Key Notes
- Latest prior run: run_20260221_013905
- Latest run with round1 notes: run_20260221_013905
- Latest run with round5 notes: run_20260221_013905
- Round1 notes: steiner_logs/run_20260221_013905/notes/round_0001_notes.md
- Round5 notes: steiner_logs/run_20260221_013905/notes/round_0005_notes.md

### Round1 Core advance excerpt
- advance statement:
-   - Converted round-1 research into a blocker-driven execution contract: bounded symmetry gate, monitored randomized pipeline, weighted-orbit fallback, and explicit handoff triggers.
- evidence from this round (metrics, runtime, structure):
-   - Mandatory cross-run files were read first.
-   - Added five web/arXiv references tied to explicit `r=6..9` consequences.
-   - Captured round-2+ stage order and metric requirements with concrete switch signals.
- transfer value for next rounds:
-   - Future rounds can execute without re-deriving engine choice rules.
-   - Practice blockers now map directly to source-backed implementation changes.

### Round5 Core advance excerpt
- advance statement:
-   - Established a practical strict-feasible `r=9` plateau-breaker for this run by combining a mandatory symmetry front gate with fast exact `1->2` micro-augment repairs after add-only exhaustion.
- evidence from this round (metrics, runtime, structure):
-   - Stage A symmetry was gated first and rejected using cached deterministic `C20/D20` diagnostics.
-   - Stage B add-only strict pass produced `0` gains.
-   - Stage C micro-augment lane produced `+18` strict blocks (`8120 -> 8138`) with verifier movement `score 27.68 -> 27.83`, `exact_once 81200 -> 81380`, `uncovered 86760 -> 86580`.
-   - Feasibility invariants remained strict: `overcovered=0`, `oversubscribed_(r-1)=0`.
- transfer value for next rounds:
-   - Keep symmetry diagnostics as front gate, but do not spend long budgets there for this instance.
-   - Use fast motif/freed-face exact `1->2` augmentation as the default first repair lane at the `8120+` strict frontier.
-   - Treat broad-window LNS as secondary diversification unless runtime budget is significantly larger.

