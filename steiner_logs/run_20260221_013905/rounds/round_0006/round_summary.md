# round_0006 summary

- Closed at: 2026-02-22T01:05:23.599204+00:00
- Score: 28.02
- Valid Steiner system: False
- Advance label: improved_vs_previous

## Core benchmark
- Exact-once r-subsets: 81610 / 167960
- Uncovered r-subsets: 86350
- Overcovered r-subsets: 0
- Block count: 8161 (expected: 16796)
- Invalid blocks: 0
- Point-degree range: 3944..4190 (target: 8398)
- (r-1)-subset max load: 6 (target: 6)
- Oversubscribed (r-1)-subsets: 0
- Additive repair feasible: True
- Residual exact-repair: not eligible: uncovered fraction is too large; use constructive search first

## Issues
- none

## Techniques used
- chained-motif-1to2
- multiseed-search

## Guidance for next round
- Target uncovered subsets with constructive block additions.
