# Round 1 Notes (Research-Only)

Instance: S(6,7,17)
Expected blocks: 1768

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
- Built and documented a strong search stack in `../KNOWLEDGE_CACHE.md`:
  1) hard admissibility/divisibility gate,
  2) symmetry/Kramer-Mesner exact-cover mode,
  3) nibble -> boosting/repair -> absorber -> residual exact-cover mode.
- Added high-value primary references (Keevash I/II, iterative absorption, Wilson, Kramer-Mesner, computational 6/8-design construction papers).
- Added an engine-selector rubric for when orbit compression is likely to win vs when randomized iterative absorption should be primary.

## Plan (Rounds 2+ execution)
1. Round 2: Symmetry reconnaissance and KM feasibility
   - Enumerate candidate automorphism groups and estimate orbit counts for `r`-sets and `q`-sets.
   - Build coarse KM size forecast (`rows`, `cols`, nonzeros, memory/time estimate).
   - Decision gate: run full KM only if compression is strong and matrix is tractable.
2. Round 3: Randomized baseline (nibble) with instrumentation
   - Run short nibble pilots with fixed seeds.
   - Track imbalance and conflict trajectories; identify stable acceptance schedule.
   - Output: best schedule + failure signatures.
3. Round 4: Boosting/repair + absorber sketch
   - Add explicit repair operators for overloaded `(r-1)` neighborhoods and undercovered `r`-sets.
   - Prototype absorber templates and test local absorbability rates.
4. Round 5: Residual exact-cover strategy
   - Define threshold where residual is handed to exact-cover/SAT/ILP.
   - Benchmark residual solver performance on synthetic leftovers shaped like Round 4 output.
5. Round 6+: Engine arbitration and scaling
   - Compare symmetry-first vs randomized-first by objective metrics below.
   - Freeze engine choice per instance class (`r`, `n`, symmetry profile).

## Work log
- Established research-only execution path (no certificate-first pressure this round).
- Captured source-backed strategy implications for `r in {6,7,8,9}`.
- Defined explicit metrics and round-gates for subsequent execution.

## Observations
- Current instance `S(6,7,17)` is admissible and internally consistent (`lambda_1=728`, `lambda_5=6`).
- Admissibility is necessary only; source evidence strongly favors either:
  - heavy symmetry compression (KM route), or
  - iterative-absorption pipeline with residual exact cleanup.
- High-order search should not start without metric instrumentation; blind search will hide bottlenecks.

## Core advance
- Converted this run from generic notes into a concrete, source-grounded execution program:
  - strong search stack,
  - engine-selector rubric,
  - next-round plan with measurable gates.

## Next-hypothesis
- Hypothesis A (symmetry-first): if orbit compression is strong, KM+basis reduction can beat randomized construction for `r=6,7` and may remain viable at `r=8`.
- Hypothesis B (randomized-first): if no strong group action appears, nibble+boosting+absorber with residual exact-cover is the only scalable path for `r>=8`.

## Metrics to track from Round 2 onward
- Point degree:
  - For each point `v`, track `deg(v)` and error to target `lambda_1`.
  - Report `max_abs_error`, `mean_abs_error`, and dispersion (std or p95-p50).
- `(r-1)`-pressure:
  - For each `(r-1)`-subset `S`, track load `load(S)` and pressure ratio `load(S)/lambda_{r-1}`.
  - Report tail metrics (`p95`, `p99`, max) and count above threshold (e.g., `>1.0` or `>1.1`).
- Uncovered/overcovered:
  - `uncovered_r_sets`: count of `r`-sets with coverage `0`.
  - `overcovered_r_sets`: count of `r`-sets with coverage `>=2`.
  - Also track combined conflict mass `sum_r |coverage(r)-1|` as a single objective.
