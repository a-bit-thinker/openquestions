# Round 2 Notes

Instance: S(6,7,17)
Expected blocks: 1768

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: steiner_logs/run_20260220_222441/REPO_WIDE_HISTORY.md
- Latest prior run: run_20260220_222329
- Latest prior round1 notes source run: run_20260220_222329
- Latest prior round1 notes: steiner_logs/run_20260220_222329/notes/round_0001_notes.md
- Latest prior round5 notes source run: run_20260220_183105
- Latest prior round5 notes: steiner_logs/run_20260220_183105/notes/round_0005_notes.md
- Latest prior transfer: steiner_logs/run_20260220_222329/NEXT_GENERATION_TRANSFER.md
- Best known metrics across all runs for this instance: score=66.04 run=run_20260219_030101 round=2 valid=? exact_once=9591/12376 uncovered=1575 overcovered=1210

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
- Read `steiner_logs/run_20260220_222441/KNOWLEDGE_CACHE.md` first.
- New targeted web searches used in this round: `0/1`.

## Plan
- Stage A: run symmetry/orbit compression diagnostics first (cyclic + dihedral) and keep only if tractable.
- Stage B: run general pipeline fallback if symmetry stalls: nibble/boosting from strict seed, then reserve-aware repair.
- Stage C: run LNS destroy/repack neighborhoods with exact/near-exact local micro-pack (not only 1-for-1 swaps).
- Stage D: attempt residual exact completion only if strict feasibility holds and residual gate passes.

## Work log
- Enforced hard admissibility gate before any search.
- Stage A (symmetry/orbit front gate):
  - Cyclic `Z_17`: `|O_6|=728`, `|O_7|=1144`; binary columns `1136`, non-binary columns `8`, `max_coeff=2`.
  - Cyclic bounded binary DFS (`20s`, `200k` nodes): `nodes=137349`, `solved=false`, timeout reached.
  - Dihedral `D_17`: `|O_6|=392`, `|O_7|=600`; binary columns `544`, non-binary columns `56`, `max_coeff=2`.
  - Dihedral bounded binary DFS (`20s`, `200k` nodes): `nodes=45`, `solved=false`.
  - Decision: symmetry lane not tractable in current budget; switched to general pipeline.
- Stage B (nibble/boosting fallback from strict seed):
  - Start strict seed: `1115` blocks, `uncovered=4571`, `overcovered=0`, `(r-1)` oversubscription `=0`.
  - Additive boost attempt (no deletions): no net additions found.
- Stage C (reserve-aware LNS + exact/near-exact local repack):
  - Reserve-first refill was enforced per neighborhood (`reserve=max(4,k//7)`).
  - Large-neighborhood destroy/repack (`k in [24,96]`) maintained strict gates but produced no net gain in this pass budget.
  - Added exact local augmentation lane (`1->2`, `2->3`, `3->4`) using bounded DFS on local candidate pools.
  - Exact local augmentation produced one strict-feasible gain: `1115 -> 1116` blocks.
- Stage D (residual exact completion gate):
  - Final state remains strict-feasible (`overcovered=0`, oversubscribed `(r-1)=0`) but residual additive exact cover is infeasible in current state:
  - status: `infeasible_residual`, reason: `some uncovered subsets have no feasible additive block`.

## Observations
- Reused from previous runs:
  - symmetry-first mandatory gate;
  - strict move gates (`overcovered=0`, `(r-1)` load cap `<= 6`);
  - reserve-then-flex refill order before global boost.
- Newly learned this round:
  - broad reserve-aware LNS alone can plateau at `1115` on this seed,
  - but exact local augmenting neighborhoods can still unlock sparse strict-feasible `+1` moves.
- Strict invariants held at every retained checkpoint:
  - `overcovered_r_subsets = 0`,
  - `oversubscribed_r_minus_1_subsets = 0`,
  - `r_minus_1_max_degree = 6` (target `lambda_5=6`).

## Metric trend
| Stage | Blocks | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Oversubscribed `(r-1)` |
|---|---:|---:|---:|---:|---|---|---:|
| Start seed | 1115 | 7805 | 4571 | 0 | 445..469 (gap 24) | 6 / 6 | 0 |
| Additive boost | 1115 | 7805 | 4571 | 0 | 445..469 (gap 24) | 6 / 6 | 0 |
| LNS pass (reserve-aware) | 1115 | 7805 | 4571 | 0 | 445..469 (gap 24) | 6 / 6 | 0 |
| Final (with exact local augmentation) | 1116 | 7812 | 4564 | 0 | 445..469 (gap 24) | 6 / 6 | 0 |

Uncovered/overcovered trend (best checkpoints):
- `4571/0 -> 4571/0 -> 4571/0 -> 4564/0`.

## Core advance
- advance statement:
  - Added an exact local augmenting-repack lane (`1->2`, `2->3`, `3->4`) on top of the strict-feasible LNS pipeline and obtained a verified strict-feasible improvement beyond the long-standing `1115` plateau.
- evidence from this round (metrics, runtime, structure):
  - Symmetry front gate was executed first and rejected by bounded diagnostics (`Z_17` and `D_17` both unsolved).
  - Reserve-aware LNS preserved feasibility but did not improve block count.
  - Exact local augmentation found one successful strict augmenting move over `19846` trials: `1115 -> 1116` blocks.
  - Verifier moved `score 48.29 -> 48.37`, `exact_once 7805 -> 7812`, `uncovered 4571 -> 4564`, while keeping `overcovered=0` and `(r-1)` oversubscription `=0`.
- transfer value for next rounds:
  - Keep symmetry diagnostics as mandatory Stage A, then switch quickly when bounded probes stall.
  - Preserve strict gates and reserve-aware refill, but add exact local augmentation as a required Stage C component.
  - Treat augmenting moves as sparse events; run high-trial-count motif-targeted neighborhoods rather than broad random LNS only.

## Next-hypothesis
- hypothesis statement:
  - Chain two motif-coupled exact augmentations around the same saturated 5-subset cluster to convert sparse single-step gains into repeated gains.
- mechanism (why this should help):
  - The successful `+1` move indicates hidden augmenting structure still exists; coupling consecutive destroy sets to the same saturated motif should preserve released slack long enough for a second augmentation before pressure re-hardens.
- expected metric movement:
  - Improve from `1116` to `1118..1124` blocks,
  - reduce uncovered by `14..56`,
  - keep `overcovered=0`, `oversubscribed_(r-1)=0`, `r_minus_1_max_degree <= 6`.
- falsification / stop condition:
  - Stop this hypothesis if after `>=60000` exact local augmentation trials the gain is `< +2` blocks total, or if successful augmentations remain isolated with no second-step chain in the same motif neighborhood.
