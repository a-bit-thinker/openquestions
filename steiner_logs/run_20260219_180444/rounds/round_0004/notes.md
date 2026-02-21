# Round 4 Notes

Instance: S(8,9,19)
Expected blocks: 8398

## Admissibility gate snapshot
```json
{
  "checks": [
    {
      "denominator": 9,
      "i": 0,
      "numerator": 75582,
      "quotient": 8398,
      "remainder": 0
    },
    {
      "denominator": 8,
      "i": 1,
      "numerator": 31824,
      "quotient": 3978,
      "remainder": 0
    },
    {
      "denominator": 7,
      "i": 2,
      "numerator": 12376,
      "quotient": 1768,
      "remainder": 0
    },
    {
      "denominator": 6,
      "i": 3,
      "numerator": 4368,
      "quotient": 728,
      "remainder": 0
    },
    {
      "denominator": 5,
      "i": 4,
      "numerator": 1365,
      "quotient": 273,
      "remainder": 0
    },
    {
      "denominator": 4,
      "i": 5,
      "numerator": 364,
      "quotient": 91,
      "remainder": 0
    },
    {
      "denominator": 3,
      "i": 6,
      "numerator": 78,
      "quotient": 26,
      "remainder": 0
    },
    {
      "denominator": 2,
      "i": 7,
      "numerator": 12,
      "quotient": 6,
      "remainder": 0
    }
  ],
  "divisibility_failures": [],
  "expected_block_count": 8398,
  "instance": {
    "n": 19,
    "q": 9,
    "r": 8
  },
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 8398,
    "lambda_1": 3978,
    "lambda_2": 1768,
    "lambda_3": 728,
    "lambda_4": 273,
    "lambda_5": 91,
    "lambda_6": 26,
    "lambda_7": 6
  }
}
```

## Research reuse
- Read steiner_logs/run_20260219_180444/KNOWLEDGE_CACHE.md first.
- At most 1 targeted search(es) if cache is insufficient.

## Plan
- Stage A: decide engine (symmetry/orbit exact-cover vs randomized nibble pipeline).
- Stage B: reserve flex/absorber blocks up front.
- Stage C: improve via large-neighborhood repair and residual exact completion when eligible.

## Work log
- Symmetry/orbit gate first:
  - Cyclic `C19` orbit compression estimate:
    - `r`-orbits `3978`, `q`-orbits `4862`, KM size `19,341,036`.
  - Dihedral `D19` orbit compression estimate:
    - `r`-orbits `2052`, `q`-orbits `2494`, KM size `5,117,688`.
  - Decision: symmetry exact-cover mode not tractable in bounded round budget; switched to general pipeline.
- Imported strongest local admissible seed for `S(8,9,19)`:
  - `steiner_logs/run_20260219_030101/candidates/candidate_19_9_8.json` (8398 blocks, score 57.35).
- Reserved absorber/flex capacity early:
  - Removed `180` conflict-heavy blocks before refill (intentional temporary cardinality drop to open neighborhoods).
  - Refilled the reserved slots with uncovered-biased nibble-style adds at fixed final cardinality `8398`.
- Ran LNS repairs:
  - Repeated remove/refill local repacks with `k in {3,4,5,6,7,8}`.
  - Move objective prioritized verifier proxy `1.9*uncovered + overcovered`.
  - Tie-break prioritized lower `(r-1)` oversubscription; soft degree-balance regularization used as tertiary tie-break.
- Residual exact completion gate:
  - Checked at end; not attempted because `overcovered_r_subsets > 0` (gate requires no overcoverage).

## Observations
- Reserve-remove phase sharply lowered `(r-1)` oversubscription tails, but expectedly worsened uncovered/overcovered while underfilled.
- Refill restored primary objective and provided a better launch point than seed.
- Best gains came from fixed-cardinality LNS remove-`k`/refill-`k` repacks, not from 1-for-1 swaps.
- This instance remains dominated by uncovered/overcovered reduction; `(r-1)` load can improve transiently but often trades off against primary score.
- No additional web research was required beyond cached knowledge.

## Per-round metric trend

| Stage | Blocks | Uncovered | Overcovered | Point degree spread | Max (r-1) load vs target | Oversubscribed (r-1) | Proxy `1.9U+O` |
|---|---:|---:|---:|---|---|---:|---:|
| Seed import | 8398 | 12276 | 8909 | 3957..3996 (gap 39) | 13 vs 6 | 15245 | 32233.4 |
| After reserve remove | 8218 | 13088 | 8443 | 3877..3914 (gap 37) | 13 vs 6 | 13177 | 33310.2 |
| After reserve refill | 8398 | 12260 | 8922 | 3959..3999 (gap 40) | 13 vs 6 | 15069 | 32216.0 |
| Final kept (LNS best) | 8398 | 12247 | 8860 | 3956..3999 (gap 43) | 13 vs 6 | 15046 | 32129.3 |

## Core advance
- Replaced empty round candidate with a full-size admissible 8398-block certificate candidate.
- Final evaluator metrics:
  - `score=57.49`, `is_valid=false`
  - `exact_once=54475/75582`
  - `uncovered=12247`, `overcovered=8860`
  - `oversubscribed_(r-1)=15046`, `r_minus_1_max_degree=13` (target `6`)
  - `point_degree=3956..3999` (gap `43`)
- Improvement versus imported seed:
  - `score 57.35 -> 57.49`
  - `uncovered 12276 -> 12247`
  - `overcovered 8909 -> 8860`
  - `oversubscribed_(r-1) 15245 -> 15046`

## Next-hypothesis
- Continue fixed-cardinality LNS with larger neighborhood packs (`k` occasionally >8) and candidate pools centered on both uncovered and high-multiplicity `8`-subset hotspots.
- Add an explicit delete-biased overcoverage reduction phase before refill to reduce the residual overcoverage barrier.
- Re-open residual exact completion only after achieving `overcovered=0` in a late-stage candidate.
