# Round 2 Notes

Instance: S(6,7,17)
Expected blocks: 1768

## Admissibility gate snapshot (strict pre-check)
```json
{
  "checks": [
    {"i": 0, "numerator": 12376, "denominator": 7, "remainder": 0, "quotient": 1768},
    {"i": 1, "numerator": 4368, "denominator": 6, "remainder": 0, "quotient": 728},
    {"i": 2, "numerator": 1365, "denominator": 5, "remainder": 0, "quotient": 273},
    {"i": 3, "numerator": 364, "denominator": 4, "remainder": 0, "quotient": 91},
    {"i": 4, "numerator": 78, "denominator": 3, "remainder": 0, "quotient": 26},
    {"i": 5, "numerator": 12, "denominator": 2, "remainder": 0, "quotient": 6}
  ],
  "divisibility_failures": [],
  "expected_block_count": 1768,
  "replication_numbers": {
    "lambda_0": 1768,
    "lambda_1": 728,
    "lambda_2": 273,
    "lambda_3": 91,
    "lambda_4": 26,
    "lambda_5": 6
  },
  "is_admissible": true
}
```

## Research reuse
- Read `steiner_logs/run_20260219_180444/KNOWLEDGE_CACHE.md` first.
- No new web lookup used in this round.

## Plan executed
1. Symmetry/orbit compression gate first (cyclic KM-style feasibility screen).
2. If symmetry solve is not tractable in bounded time, run nibble -> boosting/repair -> absorber/flex -> LNS repairs.
3. Keep residual exact completion as late-stage step only when `overcovered=0` and residual is small.

## Work log
- Symmetry-first gate:
  - Built cyclic-orbit compression summary for `C17`.
  - `r`-orbits = 728, `q`-orbits = 1144, estimated KM entries = 832,832.
  - Usable 0/1 incidence orbit-columns = 1136 (`8` columns had duplicate orbit-row hits).
  - Ran bounded orbit-level exact-cover DFS (~49s, 109,515 nodes); no completion found (best depth 35/104 orbit-columns).
  - Decision: treat symmetry exact solve as not tractable for this round budget; switch to general pipeline.
- General pipeline:
  - Seeded from the strongest available admissible 1768-block candidate in local logs (score 66.04).
  - Reserved absorber/flex capacity early by removing conflict-heavy blocks, then refilled reserved slots using uncovered-focused nibble/boosting heuristics.
  - Ran LNS repairs (`k`-block remove/refill, `k in {2..6}`) with randomized near-exact local repack restarts.
  - Ran an additional mixed swap/LNS pass emphasizing verifier objective (`uncovered/overcovered`) with soft `(r-1)`-load regularization.
  - Attempted late-stage residual exact logic gate; not eligible because `overcovered > 0` in best retained state.

## Metric trend (required)
| Stage | Blocks | Score | Uncovered | Overcovered | Point degree spread (min..max, gap) | (r-1) max load vs target | Oversubscribed (r-1)-subsets |
|---|---:|---:|---:|---:|---|---|---:|
| Empty start | 0 | 0.00 | 12376 | 0 | 0..0, gap 0 | 0 vs 6 | 0 |
| Imported seed | 1768 | 66.04 | 1575 | 1210 | 715..734, gap 19 | 10 vs 6 | 1730 |
| Reserve+refill attempt (220-slot flex) | 1768 | 64.80 | 1606 | 1305 | 720..736, gap 16 | 8 vs 6 | 1692 |
| Final kept candidate | 1768 | 66.04 | 1575 | 1210 | 715..734, gap 19 | 10 vs 6 | 1730 |

### Uncovered/overcovered trend
- Primary objective improved massively from empty baseline to non-empty candidate (`uncovered: 12376 -> 1575`).
- Within round-2 search variants, regularity-improved states (lower `(r-1)` max load) increased uncovered/overcovered enough to reduce verifier score.
- Final selection therefore kept the best verifier score state.

## Final round output
- Wrote `steiner_logs/run_20260219_180444/candidates/candidate_17_7_6.json` as a 1768-block candidate.
- Final evaluator summary:
  - `score=66.04`, `is_valid=false`
  - `exact_once=9591/12376`
  - `uncovered=1575`, `overcovered=1210`
  - `point_degree_gap=19` (target point degree 728)
  - `(r-1)` max load `10` vs target `6`
  - `oversubscribed_(r-1)=1730`
  - residual exact repair status: not eligible (`overcovered subsets must be repaired first`).

## Core advance
- Replaced empty candidate with a high-signal 1768-block admissible certificate and documented symmetry-gate evidence plus LNS repair behavior under this instance.

## Next-hypothesis
- Push beyond score 66.04 by targeting moves that reduce `uncovered` without re-inflating `(r-1)` pressure:
  - favor remove-sets centered on repeated 6-subsets with high 5-subset tail load,
  - solve larger local re-pack neighborhoods (e.g., `k=7..10`) near conflict cores,
  - keep a small protected flex pool for late uncovered hotspots.
