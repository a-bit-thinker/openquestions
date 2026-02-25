# round_0005 summary

- Closed at: 2026-02-22T16:50:38.616424+00:00
- Score: 15.44
- Valid Steiner system: False
- Advance label: regressed

## Core benchmark
- Exact-once r-subsets: 1237250 / 3124550
- Uncovered r-subsets: 1887300
- Overcovered r-subsets: 0
- Block count: 123725 (expected: 312455)
- Invalid blocks: 0
- Point-degree range: 47518..47701 (target: 120175)
- (r-1)-subset max load: 9 (target: 9)
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
