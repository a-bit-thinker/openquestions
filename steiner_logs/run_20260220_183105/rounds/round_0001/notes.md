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
- URL: https://arxiv.org/abs/1401.3665
  - Takeaway: divisibility/integrality is the first hard filter for admissibility.
  - Applied change from source: formalized hard gate as mandatory pre-search invariant.
- URL: https://arxiv.org/abs/1611.06827
  - Takeaway: iterative absorption stack (nibble -> boosting/repair -> absorber -> completion).
  - Applied change from source: defined randomized engine phases and residual exact-cover handoff.
- URL: https://eudml.org/doc/247869
  - Takeaway: practical Kramer-Mesner orbit compression with automorphism groups.
  - Applied change from source: added symmetry/orbit-compressed exact-cover mode and viability checks.
- URL: https://arxiv.org/abs/cs/0011047
  - Takeaway: DLX is an efficient sparse exact-cover backend.
  - Applied change from source: position DLX as residual solver, not global engine for large `r`.

## Plan
- Build a reusable knowledge cache for unknown large Steiner systems.
- Keep strict admissibility as a hard gate.
- Define when to use symmetry/exact-cover vs nibble/absorption engines.

## Work log
- Converted `Round 1` from placeholder to executable research protocol.
- Added strong-search-stack note: admissibility gate, symmetry/Kramer-Mesner mode, randomized iterative-absorption mode.
- Added engine-selector rubric to decide between orbit compression and randomized construction.
- Added source-grounded implementation consequences for `r=6,7,8,9`.

## Observations
- Admissibility for `S(6,7,17)` is clean (`lambda_1=728`, `lambda_5=6`, expected blocks `1768`), so failures now are algorithmic, not arithmetic.
- For `r >= 7`, global exact-cover is likely intractable without strong orbit compression; residual-only exact-cover is the stable path.
- Metrics must be tracked continuously during construction, not only at end-state.

## Core advance
- advance statement: Established a dual-engine search strategy with a mandatory divisibility gate and phase-structured randomized completion.
- evidence from this round (metrics, runtime, structure):
  - Structure: hard gate + symmetry mode + randomized mode now explicitly specified.
  - Metrics selected for rounds 2+: point degree, `(r-1)`-pressure, uncovered/overcovered counts.
  - Source support: Keevash + iterative absorption + Kramer-Mesner + DLX references linked.
- transfer value for next rounds:
  - Future rounds can run measurable experiments instead of ad hoc search.
  - Engine switching condition is now explicit and testable.

## Next-hypothesis
- hypothesis statement: A hybrid policy (symmetry pre-scan, then randomized iterative absorption, then residual DLX) will dominate single-engine attempts for `r=6..9`.
- mechanism (why this should help): orbit compression wins when structure exists; randomized absorption handles unstructured bulk; DLX resolves only tiny residue.
- expected metric movement:
  - point degree max deviation should contract toward `0` after boosting.
  - `(r-1)`-pressure tail should flatten before absorber phase.
  - uncovered and overcovered `r`-sets should both approach `0` in residual stage.
- falsification / stop condition:
  - No viable group with material orbit reduction and randomized mode fails to reduce pressure tails over repeated seeds.
  - Residual exact-cover size remains too large for DLX after repair/absorption.

## Rounds 2+ Execution (Research-Only)
1. Round 2: Engine viability scan
- Symmetry lane:
  - Enumerate candidate groups/actions and compute orbit counts for `r`- and `q`-subsets.
  - Build orbit-incidence dimensions and sparsity estimates.
  - Keep only groups with strong compression and feasible exact-cover matrix scale.
- Randomized lane:
  - Run nibble-only pilot seeds; record drift and pressure growth.
  - Add boosting/repair and compare metric deltas vs nibble-only.

2. Round 3: Full iterative-absorption dry runs
- Enable absorber/reservoir logic and run multi-seed trials.
- Hand residual to DLX only when residual columns/rows are below a predefined cutoff.
- Compare outcomes against best symmetry-lane candidate.

3. Round 4+: Hybridization and parameter search
- If symmetry lane is promising, lock a compressed backbone then randomized-fill remainder.
- Otherwise run pure randomized iterative-absorption with adaptive penalties.
- Keep certificate construction out of scope until one policy is consistently stable.

## Metrics To Track Every Round
- `point_degree_deviation`: `max_v |deg(v) - lambda_1|` and mean absolute deviation.
- `(r-1)_pressure`:
  - for each `(r-1)`-set `S`, `pressure(S) = target_{r-1}(S) - covered_{r-1}(S)`.
  - log max, p95, and count of high-pressure sets.
- `uncovered_r_sets`: number of `r`-sets with coverage `0`.
- `overcovered_r_sets`: number of `r`-sets with coverage `>1`.
- `residual_exact_cover_size`: rows/cols/nonzeros in residual matrix before DLX.
