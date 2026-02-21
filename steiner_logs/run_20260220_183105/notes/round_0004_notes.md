# Round 4 Notes

Instance: S(8,9,19)
Expected blocks: 8398

## Admissibility gate snapshot
```json
{
  "checks": [
    {"i": 0, "numerator": 75582, "denominator": 9, "remainder": 0, "quotient": 8398},
    {"i": 1, "numerator": 31824, "denominator": 8, "remainder": 0, "quotient": 3978},
    {"i": 2, "numerator": 12376, "denominator": 7, "remainder": 0, "quotient": 1768},
    {"i": 3, "numerator": 4368, "denominator": 6, "remainder": 0, "quotient": 728},
    {"i": 4, "numerator": 1365, "denominator": 5, "remainder": 0, "quotient": 273},
    {"i": 5, "numerator": 364, "denominator": 4, "remainder": 0, "quotient": 91},
    {"i": 6, "numerator": 78, "denominator": 3, "remainder": 0, "quotient": 26},
    {"i": 7, "numerator": 12, "denominator": 2, "remainder": 0, "quotient": 6}
  ],
  "divisibility_failures": [],
  "expected_block_count": 8398,
  "instance": {"n": 19, "q": 9, "r": 8},
  "is_admissible": true,
  "is_well_formed": true,
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
- Read `steiner_logs/run_20260220_183105/KNOWLEDGE_CACHE.md` first.
- No new external/web source used in this round.

## Plan
- Stage A: symmetry/orbit compression attempt first.
- Stage B: if not tractable, run nibble -> boosting/repair -> absorber/flex-aware completion.
- Stage C: LNS destroy/repack neighborhoods and residual exact-completion gate check.

## Work log
- Enforced strict admissibility gate before any search.
- Stage A (symmetry/orbit compression) diagnostics:
  - Cyclic `Z_19`:
    - `|O_8|=3978`, `|O_9|=4862`.
    - Binary orbit-columns: `4853`; non-binary columns: `9`; max coefficient `2`.
    - Bounded binary-only orbit DFS (`20s`, `200k` node cap): `nodes=266`, timeout, no completion.
  - Dihedral `D_19`:
    - `|O_8|=2052`, `|O_9|=2494`.
    - Binary orbit-columns: `2368`; non-binary columns: `126`; max coefficient `2`.
    - Binary-only orbit DFS: `nodes=192`, no solution found; plus non-binary columns require generalized multiplicity handling.
  - Decision: symmetry mode not tractable in this round budget; switched to general pipeline.
- Stage B/C (general pipeline on strict-feasible seed):
  - Start seed: `4371` blocks with `overcovered=0` and `(r-1)` oversubscription `=0`.
  - Nibble/additive pass from seed produced `0` feasible one-step additions under hard gates.
  - LNS destroy/repack used multi-block neighborhoods (`k in [24,96]`), not 1-for-1 swaps.
  - Reserve-then-flex order was enforced each iteration:
    - refill to `old_count - reserve` first,
    - then flex-complete from local pool and global boost.
  - Hard move gates (always enforced):
    - all 8-subsets unique (`row_owner` gate),
    - all 7-subset loads `<= lambda_7 = 6`.
  - Plateau handling: accepted neutral and occasional small negative deltas (annealed) to traverse the flat `delta=0` surface, while retaining best snapshot.
- Residual exact completion gate check:
  - Final state has `overcovered=0`, but uncovered is `36054` (`36054/75582 = 0.4770`), not small.
  - Residual exact completion not attempted because gate remains ineligible.

## Observations
- Under strict gates, this instance has a broad plateau where many destroy/repair moves return exactly the removed block count.
- Allowing controlled neutral/worse accepted moves was necessary to escape local plateaus and find net-positive bests.
- Strict feasibility was preserved throughout accepted best checkpoints:
  - `overcovered_r_subsets = 0`,
  - `oversubscribed_r_minus_1_subsets = 0`,
  - `r_minus_1_max_degree = 6` (target `lambda_7 = 6`).

## Metric trend
| Stage | Blocks | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Oversubscribed `(r-1)` |
|---|---:|---:|---:|---:|---|---|---:|
| Start seed | 4371 | 39339 | 36243 | 0 | gap 298 (`1925..2223`) | 6 / 6 | 0 |
| Final (this round) | 4392 | 39528 | 36054 | 0 | gap 194 (`1982..2176`) | 6 / 6 | 0 |

Best-checkpoint uncovered/overcovered trend (strict-feasible):
- `4371/36243/0 -> 4378/36180/0 -> 4386/36108/0 -> 4392/36054/0`.

## Core advance
- advance statement:
  - Implemented a symmetry-first gate plus plateau-crossing LNS pipeline that improves strict-feasible coverage on `S(8,9,19)` while preserving all hard local invariants.
- evidence from this round (metrics, runtime, structure):
  - Symmetry lane was attempted first (cyclic + dihedral orbit diagnostics + bounded DFS) and rejected with explicit tractability evidence.
  - Candidate improved `4371 -> 4392` blocks (`+21`) with `overcovered=0` and `(r-1)` oversubscription `=0` unchanged.
  - Uncovered improved `36243 -> 36054` (`-189`); point-degree gap improved `298 -> 194`.
- transfer value for next rounds:
  - Keep symmetry-first diagnostics as a short front gate, then switch quickly.
  - Keep reserve-then-flex LNS ordering.
  - Preserve strict row-owner and `(r-1)` cap gates as non-negotiable move filters.
  - Keep best-snapshot tracking while accepting neutral/worse moves for exploration.

## Next-hypothesis
- hypothesis statement:
  - Motif-targeted destroys centered on saturated 7-subsets (load `=6`) plus bounded local exact re-pack on those neighborhoods will outperform pressure-only destroys.
- mechanism (why this should help):
  - The current plateau is driven by tight 7-subset bottlenecks; explicitly removing blocks incident to those bottlenecks should unlock larger local candidate pools where exact/near-exact re-pack can recover more blocks than removed.
- expected metric movement:
  - `+10..35` blocks from `4392`,
  - uncovered reduction by `90..315`,
  - keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 6`.
- falsification / stop condition:
  - Stop this hypothesis if after `>=500` accepted motif-targeted LNS iterations there is no net gain of at least `+5` blocks, or if >85% of neighborhoods produce local pools too small (`<40` candidates) for exact/near-exact re-pack.
