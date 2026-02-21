# round_0005 summary

- Closed at: 2026-02-21T03:46:01.805726+00:00
- Score: 27.83
- Valid Steiner system: False
- Advance label: regressed

## Core benchmark
- Exact-once r-subsets: 81380 / 167960
- Uncovered r-subsets: 86580
- Overcovered r-subsets: 0
- Block count: 8138 (expected: 16796)
- Invalid blocks: 0
- Point-degree range: 3931..4181 (target: 8398)
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
