# round_0002 summary

- Closed at: 2026-02-19T18:32:40.658946+00:00
- Score: 66.04
- Valid Steiner system: False
- Advance label: new_best

## Core benchmark
- Exact-once r-subsets: 9591 / 12376
- Uncovered r-subsets: 1575
- Overcovered r-subsets: 1210
- Block count: 1768 (expected: 1768)
- Invalid blocks: 0
- Point-degree range: 715..734 (target: 728)
- (r-1)-subset max load: 10 (target: 6)
- Oversubscribed (r-1)-subsets: 1730
- Additive repair feasible: False
- Residual exact-repair: not eligible: overcovered subsets must be repaired first

## Issues
- certificate oversubscribes some (r-1)-subsets; completion is impossible without deletions

## Techniques used
- solve-r6-round-2

## Guidance for next round
- First remove blocks causing (r-1)-subset oversubscription before adding new ones.
- Target uncovered subsets with constructive block additions.
- Penalize collisions in local search objective.
