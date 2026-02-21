# Next Round Brief

Generated at: 2026-02-19T19:50:08.465373+00:00

## Latest round
- Round: round_0005
- Score: 55.44
- Valid: False
- Exact-once subsets: 118787 / 167960
- Uncovered subsets: 28530
- Overcovered subsets: 20643
- Advance label: regressed

## Best rounds so far
- round_0002: score=66.04, valid=False, exact_once=9591/12376
- round_0003: score=60.35, valid=False, exact_once=23521/31824
- round_0004: score=57.49, valid=False, exact_once=54475/75582

## Actionable next priorities
- Reduce (r-1)-subset oversubscription; completion is impossible without deletions.
- Prioritize moves that increase uncovered-subset coverage.
- Reduce collisions: avoid reusing already covered r-subsets.
- Residual exact-repair status: not eligible: overcovered subsets must be repaired first.
- Align block count toward expected 16796 (current 16796).
