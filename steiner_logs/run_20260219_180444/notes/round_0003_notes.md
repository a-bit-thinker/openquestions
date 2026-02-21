# Round 3 Notes

Instance: S(7,8,18)
Expected blocks: 3978

## Admissibility gate snapshot
```json
{
  "checks": [
    {
      "denominator": 8,
      "i": 0,
      "numerator": 31824,
      "quotient": 3978,
      "remainder": 0
    },
    {
      "denominator": 7,
      "i": 1,
      "numerator": 12376,
      "quotient": 1768,
      "remainder": 0
    },
    {
      "denominator": 6,
      "i": 2,
      "numerator": 4368,
      "quotient": 728,
      "remainder": 0
    },
    {
      "denominator": 5,
      "i": 3,
      "numerator": 1365,
      "quotient": 273,
      "remainder": 0
    },
    {
      "denominator": 4,
      "i": 4,
      "numerator": 364,
      "quotient": 91,
      "remainder": 0
    },
    {
      "denominator": 3,
      "i": 5,
      "numerator": 78,
      "quotient": 26,
      "remainder": 0
    },
    {
      "denominator": 2,
      "i": 6,
      "numerator": 12,
      "quotient": 6,
      "remainder": 0
    }
  ],
  "divisibility_failures": [],
  "expected_block_count": 3978,
  "instance": {
    "n": 18,
    "q": 8,
    "r": 7
  },
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 3978,
    "lambda_1": 1768,
    "lambda_2": 728,
    "lambda_3": 273,
    "lambda_4": 91,
    "lambda_5": 26,
    "lambda_6": 6
  }
}
```

## Research reuse
- Read `steiner_logs/run_20260219_180444/KNOWLEDGE_CACHE.md` first.
- No new web lookup used in this round.

## Plan executed
1. Symmetry/orbit compression first (`C18`, `D18`) and only continue there if tractable.
2. Otherwise run general pipeline: nibble-style refill -> boosting/repair -> absorber/flex completion.
3. Use LNS repairs (`k`-block remove/refill local repacks), then gate residual exact completion if residual is small with no overcoverage.

## Work log
- Symmetry reconnaissance (engine selector):
  - `C18`: `r`-orbits `1768`, `q`-orbits `2438`, KM estimate `4,310,384` entries; clean orbit-columns `2409`, dirty `29`.
  - `D18`: `r`-orbits `912`, `q`-orbits `1282`, KM estimate `1,169,184` entries; clean orbit-columns `1147`, dirty `135`, with `1` dead row-orbit on clean columns.
  - Decision: symmetry exact mode not tractable in this round budget (large KM + nontrivial dirty-column handling), so switched to general pipeline.
- General pipeline:
  - Imported strongest admissible 3978-block seed from local run history (`score=60.01`).
  - Reserved absorber/flex capacity early: removed `220` conflict-heavy blocks before refill.
  - Refilled reserved slots via uncovered-biased nibble-style adds (temporary anti-immediate-readd for first half).
  - Ran LNS local re-pack passes (`k in {3..10}`) with remove-by-conflict and uncovered-biased refill candidates.
  - Kept acceptance centered on verifier objective (`1.9*uncovered + overcovered`) and used `(r-1)` oversubscription as tie-break.
- Residual exact completion gate:
  - Attempted residual exact-repair builder on final kept candidate.
  - Status: ineligible (`overcovered subsets present; additive residual repair is not applicable`).

## Metric trend (required)
| Stage | Blocks | Score | Uncovered | Overcovered | Point degree spread (min..max, gap) | (r-1) max load vs target | Oversubscribed (r-1)-subsets |
|---|---:|---:|---:|---:|---|---|---:|
| Empty start | 0 | 0.00 | 31824 | 0 | 0..0, gap 0 | 0 vs 6 | 0 |
| Imported seed | 3978 | 60.01 | 4823 | 3563 | 1757..1781, gap 24 | 13 vs 6 | 5420 |
| Reserve remove (220 blocks) | 3758 | 58.62 | 5730 | 3163 | 1659..1680, gap 21 | 11 vs 6 | 3627 |
| Reserve refill (back to 3978) | 3978 | 59.79 | 4805 | 3667 | 1757..1779, gap 22 | 12 vs 6 | 5215 |
| Final kept candidate (LNS best) | 3978 | 60.35 | 4793 | 3510 | 1756..1785, gap 29 | 13 vs 6 | 5262 |

### Uncovered/overcovered trend
- Against empty baseline, both coverage and score improved substantially.
- Against imported seed, final candidate improved both primary verifier terms:
  - `uncovered: 4823 -> 4793` (down 30)
  - `overcovered: 3563 -> 3510` (down 53)
- Reserve/remove-refill alone did not improve score; the gain came from subsequent LNS local repacks.

## Final round output
- Wrote `steiner_logs/run_20260219_180444/candidates/candidate_18_8_7.json` as a 3978-block candidate.
- Final evaluator summary:
  - `score=60.35`, `is_valid=false`
  - `exact_once=23521/31824`
  - `uncovered=4793`, `overcovered=3510`, `overflow_multiplicity=4793`
  - `point_degree_gap=29` (target point degree `1768`)
  - `(r-1)` max load `13` vs target `6`
  - `oversubscribed_(r-1)=5262`

## Core advance
- Replaced empty round candidate with a high-signal admissible 3978-block certificate candidate and improved score over prior local seed (`60.01 -> 60.35`) while reducing both uncovered and overcovered 7-subsets.

## Next-hypothesis
- Keep fixed block count and continue conflict-directed LNS, but add a secondary balancing term for point-degree spread to control the widened `1756..1785` tail while preserving uncovered/overcovered gains.
