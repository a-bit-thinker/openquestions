# round_0003 summary

- Closed at: 2026-02-22T16:20:56.794444+00:00
- Score: 28.25
- Valid Steiner system: False
- Advance label: regressed

## Core benchmark
- Exact-once r-subsets: 168720 / 346104
- Uncovered r-subsets: 177384
- Overcovered r-subsets: 0
- Block count: 21090 (expected: 43263)
- Invalid blocks: 0
- Point-degree range: 7022..7045 (target: 14421)
- (r-1)-subset max load: 9 (target: 9)
- Oversubscribed (r-1)-subsets: 0
- Additive repair feasible: True
- Residual exact-repair: not eligible: uncovered fraction is too large; use constructive search first

## Issues
- none

## Techniques used
- solve-r7-round-3
- exact-backbone-none-too_large

## Guidance for next round
- Target uncovered subsets with constructive block additions.
