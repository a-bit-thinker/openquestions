# round_0004 summary

- Closed at: 2026-02-20T20:12:44.032345+00:00
- Score: 33.22
- Valid Steiner system: False
- Advance label: regressed

## Core benchmark
- Exact-once r-subsets: 39528 / 75582
- Uncovered r-subsets: 36054
- Overcovered r-subsets: 0
- Block count: 4392 (expected: 8398)
- Invalid blocks: 0
- Point-degree range: 1982..2176 (target: 3978)
- (r-1)-subset max load: 6 (target: 6)
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
