# Round 1 Notes (Research-Only)

Instance: `S(6,7,17)`
Expected blocks: `1768`

## Admissibility gate snapshot
```json
{
  "checks": [
    {
      "denominator": 7,
      "i": 0,
      "numerator": 12376,
      "quotient": 1768,
      "remainder": 0
    },
    {
      "denominator": 6,
      "i": 1,
      "numerator": 4368,
      "quotient": 728,
      "remainder": 0
    },
    {
      "denominator": 5,
      "i": 2,
      "numerator": 1365,
      "quotient": 273,
      "remainder": 0
    },
    {
      "denominator": 4,
      "i": 3,
      "numerator": 364,
      "quotient": 91,
      "remainder": 0
    },
    {
      "denominator": 3,
      "i": 4,
      "numerator": 78,
      "quotient": 26,
      "remainder": 0
    },
    {
      "denominator": 2,
      "i": 5,
      "numerator": 12,
      "quotient": 6,
      "remainder": 0
    }
  ],
  "divisibility_failures": [],
  "expected_block_count": 1768,
  "instance": {
    "n": 17,
    "q": 7,
    "r": 6
  },
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 1768,
    "lambda_1": 728,
    "lambda_2": 273,
    "lambda_3": 91,
    "lambda_4": 26,
    "lambda_5": 6
  }
}
```

## Research (this round)
- Added high-signal references for:
  - asymptotic existence + divisibility gate,
  - iterative absorption pipeline,
  - lattice-constrained decomposition,
  - random-threshold completion behavior,
  - symmetry/Kramer-Mesner exact-cover practice.
- Consolidated a two-engine strategy:
  - symmetry/KM exact-cover,
  - randomized nibble->repair->absorber->residual exact-cover.

## Rounds 2+ execution plan
1. Round 2: Engine triage + symmetry probe
- Enumerate plausible automorphism groups and compute orbit compression ratios.
- Build pilot Kramer-Mesner matrices and run short exact-cover probes.
- Decision output: `symmetry-first` or `randomized-first` for the instance family.

2. Round 3: Randomized pilot sweep
- Run multi-seed nibble trajectories with strict admissibility preserved.
- Log residual structure every epoch and early-stop poor seeds.
- Keep top seeds by low uncovered and low pressure variance.

3. Round 4: Boosting/repair + absorber placement
- Apply local balancing moves to flatten degree and `(r-1)` pressure tails.
- Add absorber templates around persistent high-pressure neighborhoods.
- Target residual small enough for deterministic exact-cover finish.

4. Round 5: Residual exact-cover finish + postmortem
- Solve residual exactly (DLX/SAT/ILP depending on sparsity).
- Compare successful vs failed runs to tighten engine selector thresholds.
- Emit transferable heuristics keyed by `r` and compression statistics.

## Metrics to track each round
- Point degree (`point_degree(v)`): number of selected `q`-blocks containing point `v`.
- Point degree error: `target_lambda_1 - point_degree(v)`; track max, mean absolute error, and variance.
- `(r-1)`-pressure (`pressure(T)`): for each `(r-1)`-subset `T`, remaining demand
  `target_lambda_{r-1} - current_coverage(T)`; track max and upper quantiles.
- Uncovered count: number of `r`-subsets with coverage `0`.
- Overcovered count: number of `r`-subsets with coverage `>1`.
- Residual exact-cover size: remaining rows/columns after repair/absorber stage.

## Work log
- Built strong-search-stack notes and source-backed engine rubric.
- Prepared transfer-ready guidance for future rounds.

## Observations
- Current instance is admissible, so downstream quality is now engine-dependent.
- Source consensus supports hybridization: random construction plus deterministic residual closure.
- Symmetry methods remain high-leverage when orbit compression is strong.

## Core advance
- advance statement: Established a concrete dual-engine construction stack with explicit selector rules and measurable diagnostics.
- evidence from this round (metrics, runtime, structure): Admissibility snapshot confirmed; six high-value references mapped to direct implementation consequences for `r=6..9`.
- transfer value for next rounds: Future rounds can execute immediately without re-deriving theory-to-implementation links.

## Next-hypothesis
- hypothesis statement: Early symmetry triage plus pressure-aware seed selection will dominate either single-engine baseline.
- mechanism (why this should help): It avoids expensive wrong-engine runs and filters randomized trajectories before hard local bottlenecks harden.
- expected metric movement: Lower high-quantile `(r-1)` pressure, reduced overcoverage, smaller residual exact-cover instance.
- falsification / stop condition: If symmetry compression is weak and pressure tails stay high across many seeds, switch to absorber-heavy randomized path only.
