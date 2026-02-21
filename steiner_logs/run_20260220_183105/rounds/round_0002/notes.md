# Round 2 Notes

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

## Research reuse
- Read `steiner_logs/run_20260220_183105/KNOWLEDGE_CACHE.md` first.
- No new external/web source used in this round.

## Plan
- Stage A: symmetry/orbit compression attempt first.
- Stage B: if not tractable, run nibble -> boosting/repair -> absorber/flex-aware completion.
- Stage C: use LNS destroy/repair and check residual exact-completion gate.

## Work log
- Enforced hard admissibility gate before search; only proceeded because divisibility checks were all integral.
- Symmetry mode attempt (cyclic orbit compression on `Z_17`):
  - `(r=6)` orbit rows: 728.
  - `(q=7)` orbit columns: 1144.
  - Usable binary orbit-columns: 1136 (8 had multiplicity-2 incidence entries and were excluded).
  - Bounded orbit DFS (`20s`, `200k` node cap) hit time cap at `17271` nodes; depth remained shallow; not tractable for this round budget.
- Switched to general pipeline:
  - Nibble seed: current collision-free 1088-block candidate.
  - Boosting/repair objective: reduce uncovered while keeping `overcovered=0` and `(r-1)` cap (`lambda_5=6`) intact.
  - Absorber/flex reservation: used staged short fills (multiple local passes + global boost) rather than single greedy saturation, keeping a large structured residual for later exact phase.
- LNS repair (not 1-for-1): repeated destroy/repack cycles with `k in [18,84]`:
  - destroy: remove `k` blocks, biased toward high point-pressure blocks;
  - near-exact local repack: refill from affected-row neighborhood under strict row-disjoint + 5-subset cap constraints;
  - global boost: add feasible low-pressure blocks from full pool.
- Residual exact completion gate check at end:
  - `overcovered=0`, but uncovered fraction `4571/12376 = 0.3694` > built-in threshold `0.10`; exact residual completion not eligible yet.

## Observations
- Hard constraints stayed preserved through all accepted moves:
  - `overcovered_r_subsets = 0`.
  - `oversubscribed_r_minus_1_subsets = 0`.
  - `r_minus_1_max_degree = 6` (exactly target).
- Larger-neighborhood repairs (`k` around `42..84`) produced the net block gains; strict 1-for-1 edits were insufficient.
- Point-degree regularity improved strongly while adding blocks, indicating reduced local pressure spikes.

## Metric trend
| Stage | Blocks | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Oversubscribed `(r-1)` |
|---|---:|---:|---:|---:|---|---|---:|
| Start candidate | 1088 | 7616 | 4760 | 0 | 396..482 (gap 86) | 6 / 6 | 0 |
| LNS pass 1 | 1109 | 7763 | 4613 | 0 | 437..470 (gap 33) | 6 / 6 | 0 |
| LNS pass 2 | 1112 | 7784 | 4592 | 0 | 440..469 (gap 29) | 6 / 6 | 0 |
| Final (this round) | 1115 | 7805 | 4571 | 0 | 445..469 (gap 24) | 6 / 6 | 0 |

## Core advance
- advance statement:
  - Established a working symmetry-first then LNS fallback loop that makes monotone progress under strict admissibility and strict collision/`(r-1)` constraints.
- evidence from this round (metrics, runtime, structure):
  - Symmetry compression was attempted first and diagnosed as currently intractable in bounded budget.
  - LNS destroy/repack raised block count `1088 -> 1115` with no overcoverage and no `(r-1)` oversubscription.
  - Uncovered dropped `4760 -> 4571`; point-degree gap contracted `86 -> 24`.
- transfer value for next rounds:
  - Keep the same strict-feasibility move filter and large-neighborhood repack backbone.
  - The search space responds to multi-block repacks, not micro-swaps.

## Next-hypothesis
- hypothesis statement:
  - A cap-aware local exact re-pack on saturated 5-subset neighborhoods will outperform pure greedy local refill and push beyond 1115 blocks.
- mechanism (why this should help):
  - Many stalled states are constrained by clusters of 5-subsets already at load 6; targeted destroy around those clusters plus bounded exact local solve should recover more than removed blocks while preserving global feasibility.
- expected metric movement:
  - Target `+15..40` blocks from 1115,
  - uncovered reduction by `105..280`,
  - keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 6`.
- falsification / stop condition:
  - Stop this hypothesis if after `>=300` accepted LNS iterations there is no net gain of at least `+5` blocks, or if maintaining `overcovered=0` and `(r-1)` cap requires rejecting >95% of candidate repairs.
