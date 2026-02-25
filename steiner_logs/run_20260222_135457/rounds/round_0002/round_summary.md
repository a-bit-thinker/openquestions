# round_0002 summary

- Closed at: 2026-02-22T14:31:05.548466+00:00
- Score: 50.59
- Valid Steiner system: False
- Advance label: new_best

## Core benchmark
- Exact-once r-subsets: 17556 / 27132
- Uncovered r-subsets: 9576
- Overcovered r-subsets: 0
- Block count: 2508 (expected: 3876)
- Invalid blocks: 0
- Point-degree range: 871..968 (target: 1428)
- (r-1)-subset max load: 7 (target: 7)
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
