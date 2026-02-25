# round_0004 summary

- Closed at: 2026-02-22T06:26:13.677066+00:00
- Score: 36.51
- Valid Steiner system: False
- Advance label: new_best

## Core benchmark
- Exact-once r-subsets: 111204 / 203490
- Uncovered r-subsets: 92286
- Overcovered r-subsets: 0
- Block count: 12356 (expected: 22610)
- Invalid blocks: 0
- Point-degree range: 5002..5569 (target: 9690)
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
