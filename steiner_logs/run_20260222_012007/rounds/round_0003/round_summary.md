# round_0003 summary

- Closed at: 2026-02-22T01:51:33.274205+00:00
- Score: 43.90
- Valid Steiner system: False
- Advance label: regressed

## Core benchmark
- Exact-once r-subsets: 46456 / 77520
- Uncovered r-subsets: 31064
- Overcovered r-subsets: 0
- Block count: 5807 (expected: 9690)
- Invalid blocks: 0
- Point-degree range: 2185..2427 (target: 3876)
- (r-1)-subset max load: 7 (target: 7)
- Oversubscribed (r-1)-subsets: 0
- Additive repair feasible: True
- Residual exact-repair: not eligible: uncovered fraction is too large; use constructive search first

## Issues
- none

## Techniques used
- solve-r7-round-3
- exact-backbone-hybrid_conflict_free_then_exact-search_exhausted

## Guidance for next round
- Target uncovered subsets with constructive block additions.
