# round_0003 summary

- Closed at: 2026-02-21T02:24:56.844718+00:00
- Score: 40.56
- Valid Steiner system: False
- Advance label: regressed

## Core benchmark
- Exact-once r-subsets: 18312 / 31824
- Uncovered r-subsets: 13512
- Overcovered r-subsets: 0
- Block count: 2289 (expected: 3978)
- Invalid blocks: 0
- Point-degree range: 950..1075 (target: 1768)
- (r-1)-subset max load: 6 (target: 6)
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
