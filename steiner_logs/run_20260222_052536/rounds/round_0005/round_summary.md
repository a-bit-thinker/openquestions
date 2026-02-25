# round_0005 summary

- Closed at: 2026-02-22T06:43:34.721824+00:00
- Score: 28.01
- Valid Steiner system: False
- Advance label: regressed

## Core benchmark
- Exact-once r-subsets: 241650 / 497420
- Uncovered r-subsets: 255770
- Overcovered r-subsets: 0
- Block count: 24165 (expected: 49742)
- Invalid blocks: 0
- Point-degree range: 10968..10995 (target: 22610)
- (r-1)-subset max load: 7 (target: 7)
- Oversubscribed (r-1)-subsets: 0
- Additive repair feasible: True
- Residual exact-repair: not eligible: uncovered fraction is too large; use constructive search first

## Issues
- none

## Techniques used
- solve-r9-round-5
- exact-backbone-none-too_large

## Guidance for next round
- Target uncovered subsets with constructive block additions.
