# Round 4 Notes

Instance: S(8,9,19)
Expected blocks: 8398

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: steiner_logs/run_20260221_013905/REPO_WIDE_HISTORY.md
- Global research log (all runs round1): steiner_logs/RESEARCH_LOG.md
- Global practice log (all runs round2-5): steiner_logs/PRACTICE_LOG.md
- Latest prior run: run_20260220_222441
- Latest prior round1 notes source run: run_20260220_222441
- Latest prior round1 notes: steiner_logs/run_20260220_222441/notes/round_0001_notes.md
- Latest prior round5 notes source run: run_20260220_183105
- Latest prior round5 notes: steiner_logs/run_20260220_183105/notes/round_0005_notes.md
- Latest prior transfer: steiner_logs/run_20260220_222441/NEXT_GENERATION_TRANSFER.md
- Best known metrics across all runs for this instance: score=57.49 run=run_20260219_180444 round=4 valid=false exact_once=54475/75582 uncovered=12247 overcovered=8860

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
- Read steiner_logs/RESEARCH_LOG.md, steiner_logs/PRACTICE_LOG.md, then steiner_logs/run_20260221_013905/KNOWLEDGE_CACHE.md.
- At most 1 targeted search(es) if cache is insufficient.

## Plan
- Stage A: decide engine (symmetry/orbit exact-cover vs randomized nibble pipeline).
- Stage B: reserve flex/absorber blocks up front.
- Stage C: improve via large-neighborhood repair and residual exact completion when eligible.

## Work log
- Enforced strict admissibility/divisibility gate before any search (all checks integral; `expected_block_count=8398`, `lambda_7=6`).
- No new web source used in this solve round (targeted searches used: `0/1`).
- Stage A (symmetry/orbit front gate, mandatory first):
  - Cyclic re-probe (recomputed this round):
    - `|O_8|=3978`, `|O_9|=4862`,
    - binary/non-binary orbit columns `4853/9`, `max_coeff=2`,
    - bounded binary DFS (`20s`, `200k` node cap): `solved=false`, `nodes=274`, timeout.
  - Dihedral (reused deterministic diagnostics from prior same-instance round `run_20260220_183105/round_0004`):
    - `|O_8|=2052`, `|O_9|=2494`,
    - binary/non-binary orbit columns `2368/126`, `max_coeff=2`,
    - bounded binary DFS unsolved in budget.
  - Decision: symmetry lane not tractable in bounded budget; switched to general pipeline.
- Stage B (nibble/additive boosting gate):
  - Strict add-only scan on the current seed (`4392` blocks) found `0` feasible additions.
  - Consequence: entered repair-first LNS immediately.
- Stage C (boosting/repair with absorber/flex discipline):
  - C1 motif-coupled exact micro-repack (`1->2`):
    - remove one block from saturated 7-subset motifs (load `=6`),
    - local exact pair refill from freed 8-subset neighborhoods and near-cap 7-subset extensions,
    - `1812` neighborhood trials, `2` accepted augmentations,
    - block count `4392 -> 4394`.
  - C2 motif-coupled `2->3` exact micro-repack:
    - `1393` neighborhood trials, `0` accepted augmentations.
  - C3 reserve-aware absorber/flex LNS (`k in [16,32]`):
    - reserve-first refill (`reserve=max(2,k//8)`) before flex completion,
    - `104` neighborhoods, `0` strict-feasible improvements beyond `4394`.
  - Hard move gates enforced in all stages:
    - `overcovered_r_subsets = 0` always,
    - `(r-1)` cap respected (`r_minus_1_max_degree <= lambda_7 = 6`, oversubscribed count `0`).
- Stage D (residual exact completion gate):
  - additive residual solver status: `ineligible`,
  - reason: uncovered residual too large (`36036 > 20000` threshold; uncovered ratio `0.4768`).

## Observations
- Reused from previous runs:
  - symmetry-first bounded gate and quick-switch policy,
  - strict feasibility invariants (`overcovered=0`, `(r-1)` oversubscription `=0`),
  - motif-coupled local exact augmentation lane.
- Newly learned this round:
  - the long `4392` strict-feasible plateau is not closed: motif-coupled `1->2` still yields sparse but real gains (`+2` blocks),
  - at this checkpoint, larger local windows (`2->3`) and reserve-aware `k`-destroy repacks did not add net blocks under the same strict gates,
  - cap-tail pressure improved slightly with gains (`7`-subset load `=6` count `82 -> 80`).
- Metric trend (best strict-feasible checkpoints this round):
  - uncovered/overcovered: `36054/0 -> 36045/0 -> 36036/0`.
  - point-degree spread: `1982..2176` (gap `194`) -> `1984..2177` (gap `193`).
  - `(r-1)` load vs target: max `6 / 6` throughout; oversubscribed `(r-1)` subsets `0` throughout.

## Core advance
- advance statement:
  - Broke the `S(8,9,19)` strict-feasible `4392` plateau with a symmetry-gated, motif-coupled `1->2` exact-repair lane while preserving all hard verifier invariants.
- evidence from this round (metrics, runtime, structure):
  - Mandatory symmetry gate was executed first, including a fresh cyclic orbit re-probe and bounded DFS before fallback.
  - Candidate improved `4392 -> 4394` (`+2`) with strict invariants intact.
  - Verifier moved:
    - `score 33.22 -> 33.25`,
    - `exact_once 39528 -> 39546`,
    - `uncovered 36054 -> 36036`,
    - `overcovered 0 -> 0`,
    - `oversubscribed_(r-1) 0 -> 0`.
  - Structural pressure also improved (`point_degree_gap 194 -> 193`; cap-6 tail `82 -> 80`).
- transfer value for next rounds:
  - Keep symmetry as a short mandatory gate, then switch quickly on this instance.
  - Prioritize motif-coupled `1->2` exact micro-repacks for net gains; treat `2->3` and larger reserve-aware neighborhoods as secondary diversification lanes.
  - Keep strict gates and best-checkpoint retention as non-negotiable.

## Next-hypothesis
- hypothesis statement:
  - Two-step coupled `1->2` chains around the same saturated 7-subset cluster, with short motif-taboo and canonical neighborhood dedup, will outperform uncoupled single-neighborhood scans from `4394`.
- mechanism (why this should help):
  - Successful `1->2` moves appear as sparse events; immediately reusing the same loosened motif neighborhood should exploit transient slack before cap pressure re-hardens.
- expected metric movement:
  - improve `4394 -> 4397..4406` blocks,
  - reduce uncovered by `27..108`,
  - keep `overcovered=0`, `oversubscribed_(r-1)=0`, `r_minus_1_max_degree <= 6`.
- falsification / stop condition:
  - stop this hypothesis if, after `>=3000` motif-coupled `1->2` trials, net gain is `< +2` blocks or if second-step chained success rate is `<5%` of first-step successes.
