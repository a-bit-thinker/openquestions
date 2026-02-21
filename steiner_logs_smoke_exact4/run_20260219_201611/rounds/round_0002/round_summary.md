# round_0002 summary

- Closed at: 2026-02-19T20:16:22.926861+00:00
- Score: 0.00
- Valid Steiner system: False
- Advance label: flat

## Core benchmark
- Exact-once r-subsets: 245 / 12376
- Uncovered r-subsets: 12131
- Overcovered r-subsets: 0
- Block count: 35 (expected: 1768)
- Invalid blocks: 0
- Point-degree range: 1..31 (target: 728)
- (r-1)-subset max load: 6 (target: 6)
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
