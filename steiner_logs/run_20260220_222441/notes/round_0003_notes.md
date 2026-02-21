# Round 3 Notes

Instance: S(7,8,18)
Expected blocks: 3978

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: `steiner_logs/run_20260220_222441/REPO_WIDE_HISTORY.md`
- Latest prior run: `run_20260220_222329`
- Latest prior round1 notes source run: `run_20260220_222329`
- Latest prior round1 notes: `steiner_logs/run_20260220_222329/notes/round_0001_notes.md`
- Latest prior round5 notes source run: `run_20260220_183105`
- Latest prior round5 notes: `steiner_logs/run_20260220_183105/notes/round_0005_notes.md`
- Latest prior transfer: `steiner_logs/run_20260220_222329/NEXT_GENERATION_TRANSFER.md`
- Best known metrics across all runs for this instance: `score=60.35` (`run_20260219_180444`, round 3, `valid=false`, `exact_once=23521/31824`, `uncovered=4793`, `overcovered=3510`)

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
- Read `steiner_logs/run_20260220_222441/KNOWLEDGE_CACHE.md` before search.
- New targeted web searches used this round: `0/1`.

## Plan executed
1. Stage A: symmetry/orbit compression front gate first; continue only if tractable.
2. Stage B: general constructive pipeline (`nibble -> boosting/repair`) with reserve held back.
3. Stage C: absorber/flex LNS destroy/repack (`k`-block neighborhoods, local near-exact repack, then global flex fill).
4. Stage D: exact residual completion attempt only if residual gate is eligible.

## Work log
- Enforced admissibility as a strict pre-search gate.
- Stage A (symmetry/orbit front gate):
  - Reused deterministic diagnostics already established for the same instance in `run_20260220_183105`:
    - Cyclic `C18`: `|O_7|=1768`, `|O_8|=2438`, non-binary columns `29`, max coefficient `2`.
    - Dihedral `D18`: `|O_7|=912`, `|O_8|=1282`, non-binary columns `135`, max coefficient `4`.
    - Bounded binary-orbit DFS previously timed out/unsolved in budget.
  - Decision: symmetry lane is not tractable in this budget; switched to general pipeline.
- Stage B (`nibble -> boosting/repair`, reserve-aware):
  - Start strict-feasible seed: `2251` blocks (`overcovered=0`, `oversubscribed_(r-1)=0`).
  - Warm neighborhoods (`k in [36,96]`) with reserve `max(4, k//7)` held before flex refill.
  - Refill sequence per neighborhood:
    - reserve-phase refill to `start_count - reserve`,
    - local near-exact repack over freed 7-subset neighborhood,
    - global flex fill.
  - First strict improvement reached `2252` blocks.
- Stage C (absorber/flex LNS):
  - Additional motif-targeted neighborhoods (`k in [24,108]`) around saturated 6-subsets.
  - Same strict move gates enforced in every accepted state:
    - `overcovered_r_subsets = 0`
    - `oversubscribed_r_minus_1_subsets = 0`
    - `r_minus_1_max_degree <= 6`
  - No further block-count increase beyond `2252`, but point-degree spread improved (`gap 141 -> 135`).
- Stage D (residual exact completion gate):
  - Final `overcovered=0`, but uncovered ratio `13808/31824 = 0.4339`.
  - Residual gate not eligible (`uncovered fraction too large`), so no exact residual completion attempt.

## Reused vs new this round
### Reused from previous runs
- Symmetry-first engine selection policy and tractability criteria.
- Strict feasibility invariants for accepted moves (`overcovered=0`, `(r-1)` cap `<= 6`).
- Reserve-then-flex refill order and motif-targeted destroy neighborhoods.

### Newly learned this round
- Multi-seed reserve-aware LNS can still produce sparse strict gains from this plateau (`2251 -> 2252`) without violating hard gates.
- Same-count neighborhoods can materially reduce pressure imbalance (`point gap 141 -> 135`) while keeping coverage fixed.
- At the current frontier, strict states repeatedly end with `feasible_left=0` and ~`113` saturated 6-subsets, indicating a hard local plateau signature.

## Observations
- Final candidate remains strictly feasible:
  - `overcovered_r_subsets = 0`
  - `oversubscribed_r_minus_1_subsets = 0`
  - `r_minus_1_max_degree = 6` (target `lambda_6 = 6`).
- Improvement is sparse and comes from LNS destroy/repack, not additive-only growth.
- Residual exact completion remains unavailable at current uncovered fraction.

## Metric trend (required)
| Stage | Blocks | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Oversubscribed `(r-1)` |
|---|---:|---:|---:|---:|---|---|---:|
| Start seed | 2251 | 18008 | 13816 | 0 | `927..1068` (gap `141`) | `6 / 6` | 0 |
| Warm best (`+1`) | 2252 | 18016 | 13808 | 0 | gap `138` | `6 / 6` | 0 |
| Final kept | 2252 | 18016 | 13808 | 0 | `930..1065` (gap `135`) | `6 / 6` | 0 |

Uncovered/overcovered trend:
- `13816/0 -> 13808/0` (strict feasibility preserved throughout accepted moves).

## Core advance
- advance statement:
  - Achieved a new strict-feasible best for this run/instance (`2251 -> 2252`) under the mandated symmetry-first then reserve-aware LNS architecture.
- evidence from this round (metrics, runtime, structure):
  - Stage A symmetry lane was explicitly gated first (reused deterministic `C18/D18` diagnostics, non-tractable in budget).
  - Stage B/C pipeline produced net strict gain with hard invariants preserved.
  - Verifier movement: `score 39.22 -> 39.26`, `exact_once 18008 -> 18016`, `uncovered 13816 -> 13808`, `overcovered=0` unchanged, `(r-1)` oversubscription `0` unchanged.
- transfer value for next rounds:
  - Keep strict gates and reserve-first refill.
  - Keep motif-targeted destroy + local near-exact repack, but treat gains as sparse and require many neighborhoods.
  - Use point-gap reduction as secondary tie-break only after block-count gains.

## Next-hypothesis
- hypothesis statement:
  - Two-step coupled motif neighborhoods (reuse the same saturated 6-subset cluster across consecutive destroys) plus a bounded exact micro-augment (`1->2`, `2->3`) will break the `2252` plateau.
- mechanism (why this should help):
  - Single neighborhoods often release slack that is immediately re-hardened by refill; chaining a second destroy around the same motif should exploit transient slack before it collapses.
- expected metric movement:
  - `2252 -> 2253..2256` blocks,
  - uncovered reduction by `8..32`,
  - keep `overcovered=0`, `oversubscribed_(r-1)=0`, `r_minus_1_max_degree <= 6`.
- falsification / stop condition:
  - Stop if after `>=500` accepted coupled neighborhoods there is `< +1` net block gain, or if exact micro-augment success rate stays `<10%`.
