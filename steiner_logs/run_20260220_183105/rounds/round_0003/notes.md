# Round 3 Notes

Instance: S(7,8,18)
Expected blocks: 3978

## Admissibility gate snapshot
```json
{
  "checks": [
    {"i": 0, "numerator": 31824, "denominator": 8, "remainder": 0, "quotient": 3978},
    {"i": 1, "numerator": 12376, "denominator": 7, "remainder": 0, "quotient": 1768},
    {"i": 2, "numerator": 4368, "denominator": 6, "remainder": 0, "quotient": 728},
    {"i": 3, "numerator": 1365, "denominator": 5, "remainder": 0, "quotient": 273},
    {"i": 4, "numerator": 364, "denominator": 4, "remainder": 0, "quotient": 91},
    {"i": 5, "numerator": 78, "denominator": 3, "remainder": 0, "quotient": 26},
    {"i": 6, "numerator": 12, "denominator": 2, "remainder": 0, "quotient": 6}
  ],
  "divisibility_failures": [],
  "expected_block_count": 3978,
  "instance": {"n": 18, "q": 8, "r": 7},
  "is_admissible": true,
  "is_well_formed": true,
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
- Read `steiner_logs/run_20260220_183105/KNOWLEDGE_CACHE.md` first.
- No new external/web source used in this round.

## Plan
- Stage A: symmetry/orbit compression attempt first.
- Stage B: fallback to nibble -> boosting/repair -> absorber/flex completion.
- Stage C: LNS destroy/repack neighborhoods and residual exact-completion gate check.

## Work log
- Enforced strict admissibility gate before all search steps.
- Symmetry/orbit diagnostics first:
  - Cyclic (`Z_18`): `|O_7|=1768`, `|O_8|=2438`; non-binary orbit-columns `29/2438`, max orbit coefficient `2`.
  - Dihedral (`D_18`): `|O_7|=912`, `|O_8|=1282`; non-binary orbit-columns `135/1282`, max coefficient `4`.
  - Cyclic bounded orbit DFS on binary-only columns (`20s`, `200k` node cap): `rows=1768`, `cols=2409`, `nodes=2097`, timeout; no usable completion. Declared non-tractable for this round budget.
- Switched to general pipeline from current strict-feasible seed (`2239` blocks):
  - Nibble/boosting with strict row-owner gate (`7`-subset uniqueness) and `(r-1)` load guard.
  - Reserved absorber/flex capacity early in every LNS iteration: destroy `k`, refill only to `k-reserve` first, then flex-complete.
  - LNS repairs used multi-block destroy/repack (`k in [24,96]`), not 1-for-1 swaps.
  - Local near-exact re-pack used bounded branch-and-bound on neighborhood pool (`<=120` local candidates) before greedy tail fill.
- Residual exact completion gate check:
  - `overcovered=0`, but uncovered ratio `13816/31824 = 0.4341`; residual exact repair not eligible (threshold `<=0.10`).

## Observations
- All accepted states preserved hard feasibility:
  - `overcovered_r_subsets = 0`.
  - `oversubscribed_r_minus_1_subsets = 0`.
  - `r_minus_1_max_degree = 6` equals target `lambda_6=6`.
- Improvement came from larger neighborhoods and local exact re-pack; single-add or micro-swap moves were already exhausted at start (`0` one-step feasible adds).
- Point-pressure flattened while coverage increased (gap `179 -> 141`).

## Metric trend
| Stage | Blocks | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Oversubscribed `(r-1)` |
|---|---:|---:|---:|---:|---|---|---:|
| Start seed | 2239 | 17912 | 13912 | 0 | gap 179 (`901..1080`) | 6 / 6 | 0 |
| Phase 1 best | 2247 | 17976 | 13848 | 0 | gap 145 | 6 / 6 | 0 |
| Phase 2 best | 2250 | 18000 | 13824 | 0 | gap 143 | 6 / 6 | 0 |
| Final (this round) | 2251 | 18008 | 13816 | 0 | gap 141 (`927..1068`) | 6 / 6 | 0 |

## Core advance
- advance statement:
  - Implemented a symmetry-first gate plus absorber-reserved LNS pipeline that produced monotone strict-feasible gains for `S(7,8,18)`.
- evidence from this round (metrics, runtime, structure):
  - Symmetry mode was attempted first and rejected only after concrete orbit diagnostics + bounded search timeout.
  - LNS multi-block destroy/repack improved `2239 -> 2251` blocks (`+12`) with `overcovered=0` and `(r-1)` oversubscription `=0` throughout.
  - Uncovered improved `13912 -> 13816` and point-degree gap improved `179 -> 141`.
- transfer value for next rounds:
  - Keep the same strict row-owner feasibility gate.
  - Keep explicit reserve-then-flex refill order.
  - Keep bounded local exact re-pack inside LNS neighborhoods; this is where net positive moves were found.

## Next-hypothesis
- hypothesis statement:
  - Destroy neighborhoods chosen around saturated `6`-subset motifs (load exactly `6`) will unlock larger positive repacks than pressure-only block destruction.
- mechanism (why this should help):
  - Current plateaus are caused by local frozen structures where many candidate blocks are blocked by a small set of tight `(r-1)` faces; targeting those faces should free higher-quality local orbit of alternatives for exact re-pack.
- expected metric movement:
  - `+10..25` blocks from `2251`,
  - uncovered reduction by `80..200`,
  - maintain `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 6`.
- falsification / stop condition:
  - Stop this hypothesis if after `>=400` accepted LNS iterations with motif-targeted destroys there is no net gain of at least `+4` blocks, or if feasible local candidate pool size repeatedly collapses below `30` in >80% of iterations.
