# round_0002 summary

- Closed at: 2026-02-22T01:40:50.833709+00:00
- Score: 50.09
- Valid Steiner system: False
- Advance label: new_best

## Core benchmark
- Exact-once r-subsets: 64960 / 100947
- Uncovered r-subsets: 35987
- Overcovered r-subsets: 0
- Block count: 9280 (expected: 14421)
- Invalid blocks: 0
- Point-degree range: 2597..3010 (target: 4389)
- (r-1)-subset max load: 9 (target: 9)
- Oversubscribed (r-1)-subsets: 0
- Additive repair feasible: True
- Residual exact-repair: not eligible: uncovered fraction is too large; use constructive search first

## Issues
- none

## Techniques used
- solve-r6-round-2
- exact-backbone-hybrid_conflict_free_then_exact-search_exhausted

## Guidance for next round
- Target uncovered subsets with constructive block additions.
