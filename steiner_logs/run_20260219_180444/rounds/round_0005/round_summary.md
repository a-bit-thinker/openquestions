# round_0005 summary

- Closed at: 2026-02-19T19:50:08.463455+00:00
- Score: 55.44
- Valid Steiner system: False
- Advance label: regressed

## Core benchmark
- Exact-once r-subsets: 118787 / 167960
- Uncovered r-subsets: 28530
- Overcovered r-subsets: 20643
- Block count: 16796 (expected: 16796)
- Invalid blocks: 0
- Point-degree range: 8373..8435 (target: 8398)
- (r-1)-subset max load: 15 (target: 6)
- Oversubscribed (r-1)-subsets: 38551
- Additive repair feasible: False
- Residual exact-repair: not eligible: overcovered subsets must be repaired first

## Issues
- certificate oversubscribes some (r-1)-subsets; completion is impossible without deletions

## Techniques used
- solve-r9-round-5

## Guidance for next round
- First remove blocks causing (r-1)-subset oversubscription before adding new ones.
- Target uncovered subsets with constructive block additions.
- Penalize collisions in local search objective.
