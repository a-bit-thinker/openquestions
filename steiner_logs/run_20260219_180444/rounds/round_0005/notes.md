# Round 5 Notes

Instance: S(9,10,20)
Expected blocks: 16796

## Admissibility gate snapshot
```json
{
  "checks": [
    {
      "denominator": 10,
      "i": 0,
      "numerator": 167960,
      "quotient": 16796,
      "remainder": 0
    },
    {
      "denominator": 9,
      "i": 1,
      "numerator": 75582,
      "quotient": 8398,
      "remainder": 0
    },
    {
      "denominator": 8,
      "i": 2,
      "numerator": 31824,
      "quotient": 3978,
      "remainder": 0
    },
    {
      "denominator": 7,
      "i": 3,
      "numerator": 12376,
      "quotient": 1768,
      "remainder": 0
    },
    {
      "denominator": 6,
      "i": 4,
      "numerator": 4368,
      "quotient": 728,
      "remainder": 0
    },
    {
      "denominator": 5,
      "i": 5,
      "numerator": 1365,
      "quotient": 273,
      "remainder": 0
    },
    {
      "denominator": 4,
      "i": 6,
      "numerator": 364,
      "quotient": 91,
      "remainder": 0
    },
    {
      "denominator": 3,
      "i": 7,
      "numerator": 78,
      "quotient": 26,
      "remainder": 0
    },
    {
      "denominator": 2,
      "i": 8,
      "numerator": 12,
      "quotient": 6,
      "remainder": 0
    }
  ],
  "divisibility_failures": [],
  "expected_block_count": 16796,
  "instance": {
    "n": 20,
    "q": 10,
    "r": 9
  },
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 16796,
    "lambda_1": 8398,
    "lambda_2": 3978,
    "lambda_3": 1768,
    "lambda_4": 728,
    "lambda_5": 273,
    "lambda_6": 91,
    "lambda_7": 26,
    "lambda_8": 6
  }
}
```

## Research reuse
- Read `steiner_logs/run_20260219_180444/KNOWLEDGE_CACHE.md` first.
- No new web sources were required this round.

## Plan
- Stage A: decide engine (symmetry/orbit exact-cover vs randomized nibble pipeline).
- Stage B: reserve flex/absorber blocks up front.
- Stage C: improve via large-neighborhood repair and residual exact completion when eligible.

## Work log
- Enforced strict admissibility gate first; search proceeded only after divisibility passed.
- Symmetry/orbit reconnaissance (Burnside counts):
  - Cyclic `C20`: `r`-orbits `8398`, `q`-orbits `9252`, KM size `77,698,296` entries.
  - Dihedral `D20`: `r`-orbits `4262`, `q`-orbits `4752`, KM size `20,253,024` entries.
  - Decision: orbit-compressed exact mode not tractable in bounded round budget; switched to general pipeline.
- Imported best local seed for this instance:
  - `steiner_logs/run_20260219_030101/candidates/candidate_20_10_9.json` (`score=54.95`).
- Reserved absorber/flex capacity early:
  - Removed `180` conflict-heavy blocks before refill.
  - Refilled exactly `180` slots with uncovered-biased greedy adds (fixed final cardinality `16796`).
- Ran LNS repairs (not 1-for-1):
  - Repeated remove-`k`/refill-`k` repacks with `k` in `{3,4,5,6,7,8,9,10,12}`.
  - Primary accept objective: reduce uncovered/overcovered proxy `19*U + 10*O`.
  - Tie-break: lower oversubscribed `(r-1)` subsets (`8`-subset loads above target `6`).
  - Performed three passes; kept globally best verifier score candidate.
- Residual exact completion gate:
  - Not attempted; gate blocked by persistent `overcovered_r_subsets > 0`.

## Per-round metric trend

| Stage | Blocks | Uncovered | Overcovered | Point degree spread | Max (r-1) load vs target | Oversubscribed (r-1) | Proxy `19U+10O` |
|---|---:|---:|---:|---|---|---:|---:|
| Seed import | 16796 | 28774 | 20999 | 8380..8418 (gap 38) | 14 vs 6 | 38926 | 756696 |
| After reserve remove | 16616 | 29671 | 20412 | 8277..8340 (gap 63) | 14 vs 6 | 36819 | 767869 |
| After reserve refill | 16796 | 28726 | 20977 | 8374..8440 (gap 66) | 14 vs 6 | 38826 | 755564 |
| LNS pass 1 best | 16796 | 28559 | 20662 | 8371..8438 (gap 67) | 15 vs 6 | 38607 | 749241 |
| LNS pass 2 best | 16796 | 28535 | 20649 | 8371..8441 (gap 70) | 16 vs 6 | 38542 | 748655 |
| Final kept | 16796 | 28530 | 20643 | 8373..8435 (gap 62) | 15 vs 6 | 38551 | 748500 |

## Observations
- Symmetry compression was not enough to make a bounded exact solve practical for `S(9,10,20)` this round.
- Early reserve/remove decreased `(r-1)` oversubscription sharply, but worsened primary coverage metrics until refill completed.
- Fixed-cardinality remove-`k`/refill-`k` LNS consistently outperformed simple 1-for-1 style updates.
- Final pass improved primary verifier drivers (`U`, `O`) at slight `(r-1)` oversubscription tradeoff vs one intermediate pass; kept due better score and better uncovered/overcovered.

## Core advance
- Replaced empty candidate with a full-size, format-valid `16796`-block certificate candidate.
- Final evaluator metrics:
  - `score=55.44`, `is_valid=false`
  - `exact_once=118787/167960`
  - `uncovered=28530`, `overcovered=20643`, `overflow_multiplicity=28530`
  - `oversubscribed_(r-1)=38551`, `r_minus_1_max_degree=15` (target `6`)
  - `point_degree=8373..8435` (gap `62`)
- Improvement versus imported seed:
  - `score 54.95 -> 55.44`
  - `uncovered 28774 -> 28530`
  - `overcovered 20999 -> 20643`
  - `oversubscribed_(r-1) 38926 -> 38551`

## Next-hypothesis
- Keep fixed-cardinality LNS, but bias removals further toward `c=2` heavy 9-subset collisions before refill.
- Add a dedicated delete-biased overcoverage-burn phase before uncovered-biased refill.
- Re-open residual exact completion only after driving `overcovered_r_subsets` to `0` in late-stage candidates.
