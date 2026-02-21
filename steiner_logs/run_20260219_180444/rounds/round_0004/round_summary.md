# round_0004 summary

- Closed at: 2026-02-19T19:19:02.540843+00:00
- Score: 57.49
- Valid Steiner system: False
- Advance label: regressed

## Core benchmark
- Exact-once r-subsets: 54475 / 75582
- Uncovered r-subsets: 12247
- Overcovered r-subsets: 8860
- Block count: 8398 (expected: 8398)
- Invalid blocks: 0
- Point-degree range: 3956..3999 (target: 3978)
- (r-1)-subset max load: 13 (target: 6)
- Oversubscribed (r-1)-subsets: 15046
- Additive repair feasible: False
- Residual exact-repair: not eligible: overcovered subsets must be repaired first

## Issues
- certificate oversubscribes some (r-1)-subsets; completion is impossible without deletions

## Techniques used
- solve-r8-round-4

## Guidance for next round
- First remove blocks causing (r-1)-subset oversubscription before adding new ones.
- Target uncovered subsets with constructive block additions.
- Penalize collisions in local search objective.
