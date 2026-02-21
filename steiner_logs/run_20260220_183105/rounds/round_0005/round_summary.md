# round_0005 summary

- Closed at: 2026-02-20T21:03:01.644776+00:00
- Score: 27.68
- Valid Steiner system: False
- Advance label: regressed

## Core benchmark
- Exact-once r-subsets: 81200 / 167960
- Uncovered r-subsets: 86760
- Overcovered r-subsets: 0
- Block count: 8120 (expected: 16796)
- Invalid blocks: 0
- Point-degree range: 3922..4173 (target: 8398)
- (r-1)-subset max load: 6 (target: 6)
- Oversubscribed (r-1)-subsets: 0
- Additive repair feasible: True
- Residual exact-repair: not eligible: uncovered fraction is too large; use constructive search first

## Issues
- none

## Techniques used
- solve-r9-round-5
- exact-backbone-hybrid_conflict_free_then_exact-search_exhausted

## Guidance for next round
- Target uncovered subsets with constructive block additions.
