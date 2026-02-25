# round_0004 summary

- Closed at: 2026-02-22T16:40:03.390335+00:00
- Score: 24.35
- Valid Steiner system: False
- Advance label: regressed

## Core benchmark
- Exact-once r-subsets: 497106 / 1081575
- Uncovered r-subsets: 584469
- Overcovered r-subsets: 0
- Block count: 55234 (expected: 120175)
- Invalid blocks: 0
- Point-degree range: 19866..19898 (target: 43263)
- (r-1)-subset max load: 8 (target: 9)
- Oversubscribed (r-1)-subsets: 0
- Additive repair feasible: True
- Residual exact-repair: not eligible: uncovered fraction is too large; use constructive search first

## Issues
- none

## Techniques used
- solve-r8-round-4
- exact-backbone-none-too_large

## Guidance for next round
- Target uncovered subsets with constructive block additions.
