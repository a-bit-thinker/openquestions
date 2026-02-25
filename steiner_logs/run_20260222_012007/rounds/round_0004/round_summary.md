# round_0004 summary

- Closed at: 2026-02-22T02:02:34.655741+00:00
- Score: 35.16
- Valid Steiner system: False
- Advance label: regressed

## Core benchmark
- Exact-once r-subsets: 109242 / 203490
- Uncovered r-subsets: 94248
- Overcovered r-subsets: 0
- Block count: 12138 (expected: 22610)
- Invalid blocks: 0
- Point-degree range: 4837..5529 (target: 9690)
- (r-1)-subset max load: 7 (target: 7)
- Oversubscribed (r-1)-subsets: 0
- Additive repair feasible: True
- Residual exact-repair: not eligible: uncovered fraction is too large; use constructive search first

## Issues
- none

## Techniques used
- solve-r8-round-4
- exact-backbone-hybrid_conflict_free_then_exact-search_exhausted

## Guidance for next round
- Target uncovered subsets with constructive block additions.
