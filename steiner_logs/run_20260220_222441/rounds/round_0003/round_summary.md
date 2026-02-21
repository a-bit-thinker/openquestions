# round_0003 summary

- Closed at: 2026-02-20T23:19:40.173240+00:00
- Score: 39.26
- Valid Steiner system: False
- Advance label: regressed

## Core benchmark
- Exact-once r-subsets: 18016 / 31824
- Uncovered r-subsets: 13808
- Overcovered r-subsets: 0
- Block count: 2252 (expected: 3978)
- Invalid blocks: 0
- Point-degree range: 930..1065 (target: 1768)
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
