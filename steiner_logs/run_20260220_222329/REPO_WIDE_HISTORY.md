# Repo-Wide Steiner History

Generated (UTC): 2026-02-20T22:23:31.312112+00:00
Log root: steiner_logs
Current run dir: /root/openquestions/steiner_logs/run_20260220_222329

- Total run dirs found: 8
- Prior run dirs found: 7
- Latest prior run: run_20260220_222225

## Best Known By Instance (across all runs)
| Instance | Score | Run | Round | Valid | Exact Once | Uncovered | Overcovered |
|---|---:|---|---:|---|---|---:|---:|
| S(6,7,17) | 66.04 | run_20260219_030101 | 2 | ? | 9591/12376 | 1575 | 1210 |
| S(7,8,18) | 60.35 | run_20260219_180444 | 3 | false | 23521/31824 | 4793 | 3510 |
| S(8,9,19) | 57.49 | run_20260219_180444 | 4 | false | 54475/75582 | 12247 | 8860 |
| S(9,10,20) | 55.44 | run_20260219_180444 | 5 | false | 118787/167960 | 28530 | 20643 |

## Latest Prior Run Key Notes
- Latest prior run: run_20260220_222225
- Latest run with round1 notes: run_20260220_222225
- Latest run with round5 notes: run_20260220_183105
- Round1 notes: steiner_logs/run_20260220_222225/notes/round_0001_notes.md
- Round5 notes: steiner_logs/run_20260220_183105/notes/round_0005_notes.md

### Round1 Core advance excerpt
- advance statement:
- evidence from this round (metrics, runtime, structure):
- transfer value for next rounds:

### Round5 Core advance excerpt
- advance statement:
-   - Established a reproducible strict-feasible improvement loop for `S(9,10,20)` that combines a symmetry front gate with reserve-aware multi-pass LNS and yields monotone best-checkpoint progress.
- evidence from this round (metrics, runtime, structure):
-   - Symmetry lane was evaluated first with explicit orbit/multiplicity diagnostics and bounded DFS before fallback.
-   - Candidate improved from `5897` to `8120` blocks (`+2223`) while preserving `overcovered=0` and `(r-1)` oversubscription `=0`.
-   - Uncovered reduced by `22230` (`108990 -> 86760`); point-degree gap reduced by `1260` (`1511 -> 251`).
- transfer value for next rounds:
-   - Keep symmetry diagnostics as mandatory front gate, then switch quickly when non-binary orbit coefficients dominate.
-   - Keep reserve-then-flex refill order and strict hard gates in every neighborhood.
-   - Use repeated LNS passes; single-pass improvement leaves significant recoverable slack.

