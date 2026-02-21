# round_0003 summary

- Closed at: 2026-02-20T19:31:25.770389+00:00
- Score: 39.22
- Valid Steiner system: False
- Advance label: regressed

## Core benchmark
- Exact-once r-subsets: 18008 / 31824
- Uncovered r-subsets: 13816
- Overcovered r-subsets: 0
- Block count: 2251 (expected: 3978)
- Invalid blocks: 0
- Point-degree range: 927..1068 (target: 1768)
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
