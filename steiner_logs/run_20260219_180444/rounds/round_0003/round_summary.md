# round_0003 summary

- Closed at: 2026-02-19T19:00:30.422200+00:00
- Score: 60.35
- Valid Steiner system: False
- Advance label: regressed

## Core benchmark
- Exact-once r-subsets: 23521 / 31824
- Uncovered r-subsets: 4793
- Overcovered r-subsets: 3510
- Block count: 3978 (expected: 3978)
- Invalid blocks: 0
- Point-degree range: 1756..1785 (target: 1768)
- (r-1)-subset max load: 13 (target: 6)
- Oversubscribed (r-1)-subsets: 5262
- Additive repair feasible: False
- Residual exact-repair: not eligible: overcovered subsets must be repaired first

## Issues
- certificate oversubscribes some (r-1)-subsets; completion is impossible without deletions

## Techniques used
- solve-r7-round-3

## Guidance for next round
- First remove blocks causing (r-1)-subset oversubscription before adding new ones.
- Target uncovered subsets with constructive block additions.
- Penalize collisions in local search objective.
