# Next Generation Transfer

Generated (UTC): 2026-02-20T22:22:28.773282+00:00
Run directory: steiner_logs/run_20260220_222225

## Scope
- This document summarizes the latest five rounds (or fewer if run is shorter).
- Goal: preserve proven progress and pass explicit next hypotheses to the next run/agent.

## Latest Round Snapshot
- Round: 2 (solve)
- Instance: S(6,7,17)
- Score: 48.29
- Valid: false
- Exact once: 7805/12376
- Uncovered: 4571
- Overcovered: 0

## Best Round So Far
- Round: 2 (solve)
- Instance: S(6,7,17)
- Score: 48.29
- Exact once: 7805/12376
- Uncovered: 4571
- Overcovered: 0

## Round Trajectory (recent)
| Round | Mode | Instance | Score | Valid | Exact Once | Uncovered | Overcovered |
|---:|---|---|---:|---|---|---:|---:|
| 1 | research | S(6,7,17) | 0 | false | 0/12376 | 12376 | 0 |
| 2 | solve | S(6,7,17) | 48.29 | false | 7805/12376 | 4571 | 0 |

## Core Advances (Rounds 1-5 Window)
- No explicit Core advance bullets captured yet. Fill notes sections to improve transfer quality.

## Knowledge Gaps / Blockers
- No fully valid certificate yet; current frontier remains partial.
- Large uncovered residual remains; prioritize structured completion over random mutation.

## Next Hypothesis Ladder (for next generation)
1. No explicit Next-hypothesis bullets captured yet. Add falsifiable hypotheses in round notes.

## Mandatory Next-Round Discipline
1. Keep notes sections non-empty: `Core advance`, `Observations`, `Next-hypothesis`.
2. Every hypothesis must include: mechanism, expected metric movement, and stop condition.
3. Preserve exactness-first artifacts (overcovered=0 candidates) even if scalar score is lower.
4. Update this transfer file at round close to avoid losing accumulated reasoning.

