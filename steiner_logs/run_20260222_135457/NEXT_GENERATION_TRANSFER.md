# Next Generation Transfer

Generated (UTC): 2026-02-22T16:45:00Z
Run directory: steiner_logs/run_20260222_135457

## Scope
- This document summarizes the latest five rounds (or fewer if run is shorter).
- Goal: preserve proven progress and pass explicit next hypotheses to the next run/agent.

## Latest Round Snapshot
- Round: 2 (solve)
- Instance: S(6,7,19)
- Score: 50.59
- Valid: false
- Exact once: 17556/27132
- Uncovered: 9576
- Overcovered: 0

## Best Round So Far
- Round: 2 (solve)
- Instance: S(6,7,19)
- Score: 50.59
- Exact once: 17556/27132
- Uncovered: 9576
- Overcovered: 0

## Round Trajectory (recent)
| Round | Mode | Instance | Score | Valid | Exact Once | Uncovered | Overcovered |
|---:|---|---|---:|---|---|---:|---:|
| 1 | research | S(6,7,19) | 0.00 | false | 0/27132 | 27132 | 0 |
| 2 | solve | S(6,7,19) | 50.59 | false | 17556/27132 | 9576 | 0 |

## Core Advances (Rounds 1-5 Window)
- round_0001: Converted the `S(6,7,19)` round1 into a proof-first, veto-aware execution contract (derivation-veto lane + bounded symmetry triage + staged randomized fallback).
- round_0001: Divisibility gate is explicitly recorded (`b=3876`, `lambda_5=7`, all remainders `0`).
- round_0002: Established the first strict constructive frontier for this run on `S(6,7,19)` and improved candidate size `2438 -> 2508` while preserving `overcovered=0` and `oversubscribed_(r-1)=0`.
- round_0002: Symmetry-first requirement was executed; cyclic KM diagnostics were tractable and used for proposal structure, then strict LNS produced the net movement.
- round_0002: Point-degree spread improved `156 -> 97`; uncovered reduced `10066 -> 9576` under unchanged strict gates.

## Knowledge Gaps / Blockers
- No fully valid certificate yet; current frontier remains partial.
- Residual exact-cover remains ineligible at this frontier (`uncovered fraction ~0.353 > 0.10`).
- Add-only strict growth is exhausted from this seed; gains require repack-based neighborhoods.

## Next Hypothesis Ladder (for next generation)
1. round_0002: Alternating strict pressure-relief repacks (`k->k`) and strict improvement repacks (`k->k+1`, `k=2..4`) will outperform improvement-only repacks from this frontier.
2. round_0002: Mechanism: neutral repacks reduce capped 5-subset pressure and reopen feasible `k->k+1` windows that add-only cannot access.
3. round_0002: Expected movement: `2508 -> 2518..2558` blocks with `overcovered=0` and `oversubscribed_(r-1)=0` preserved.
4. round_0002: Falsify if after `>=60000` strict neighborhoods net gain is `< +8` blocks or if any strict violation appears.

## Mandatory Next-Round Discipline
1. Keep notes sections non-empty: `Core advance`, `Observations`, `Next-hypothesis`.
2. Every hypothesis must include: mechanism, expected metric movement, and stop condition.
3. Preserve exactness-first artifacts (overcovered=0 candidates) even if scalar score is lower.
4. Update this transfer file at round close to avoid losing accumulated reasoning.
