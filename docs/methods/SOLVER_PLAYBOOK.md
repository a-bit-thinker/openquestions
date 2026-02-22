# Solver Playbook

## Baseline Search Stack
1. Hard gates: divisibility, derivation-veto, residual eligibility.
2. Symmetry lane: bounded Kramer/orbit reduction, then SAT/ILP/DLX if diagnostics pass.
3. Randomized lane: nibble -> boosting/repair -> absorber reserve.
4. Closure lane: residual exact-cover when uncovered/pressure thresholds pass.

## Required Checkpoint Metrics
- exact_once
- uncovered
- overcovered
- point_degree_gap
- r_minus_1_cap_hits
- accepted_moves_per_1k

## Stop Conditions
- repeated non-improving checkpoints under fixed budget,
- strict infeasibility increase,
- violated boundary contract.
