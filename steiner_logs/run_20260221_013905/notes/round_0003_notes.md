# Round 3 Notes

Instance: S(7,8,18)
Expected blocks: 3978

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: `steiner_logs/run_20260221_013905/REPO_WIDE_HISTORY.md`
- Global research log (all runs round1): `steiner_logs/RESEARCH_LOG.md`
- Global practice log (all runs round2-5): `steiner_logs/PRACTICE_LOG.md`
- Latest prior run: `run_20260220_222441`
- Latest prior round1 notes source run: `run_20260220_222441`
- Latest prior round1 notes: `steiner_logs/run_20260220_222441/notes/round_0001_notes.md`
- Latest prior round5 notes source run: `run_20260220_183105`
- Latest prior round5 notes: `steiner_logs/run_20260220_183105/notes/round_0005_notes.md`
- Latest prior transfer: `steiner_logs/run_20260220_222441/NEXT_GENERATION_TRANSFER.md`
- Best known metrics across all runs for this instance: `score=60.35` (`run_20260219_180444`, round 3, `valid=false`, `exact_once=23521/31824`, `uncovered=4793`, `overcovered=3510`)

## Admissibility gate snapshot
```json
{
  "checks": [
    {"denominator": 8, "i": 0, "numerator": 31824, "quotient": 3978, "remainder": 0},
    {"denominator": 7, "i": 1, "numerator": 12376, "quotient": 1768, "remainder": 0},
    {"denominator": 6, "i": 2, "numerator": 4368, "quotient": 728, "remainder": 0},
    {"denominator": 5, "i": 3, "numerator": 1365, "quotient": 273, "remainder": 0},
    {"denominator": 4, "i": 4, "numerator": 364, "quotient": 91, "remainder": 0},
    {"denominator": 3, "i": 5, "numerator": 78, "quotient": 26, "remainder": 0},
    {"denominator": 2, "i": 6, "numerator": 12, "quotient": 6, "remainder": 0}
  ],
  "divisibility_failures": [],
  "expected_block_count": 3978,
  "instance": {"n": 18, "q": 8, "r": 7},
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
- Read `steiner_logs/RESEARCH_LOG.md`, `steiner_logs/PRACTICE_LOG.md`, and `steiner_logs/run_20260221_013905/KNOWLEDGE_CACHE.md` before solve.
- New targeted web searches this round: `0/1`.

## Plan
1. Stage A: run symmetry/orbit compression diagnostics first (cyclic + dihedral), keep only if tractable.
2. Stage B: if symmetry stalls, switch to general pipeline from current strict-feasible seed.
3. Stage C: reserve-aware LNS repairs with motif-coupled exact micro-augments (`1->2`, then `2->3`).
4. Stage D: residual exact completion only if uncovered is small and overcoverage is zero.

## Work log
- Enforced admissibility as a strict pre-search gate.
- Stage A (symmetry front gate, bounded):
  - `C18` diagnostics: `|O_7|=1768`, `|O_8|=2438`, binary/non-binary columns `2409/29`, `max_coeff=2`.
  - `C18` bounded binary DFS (`20s`, `200k` nodes): `nodes=330`, `solved=false`, timeout reached.
  - `D18` diagnostics: `|O_7|=912`, `|O_8|=1282`, binary/non-binary columns `1147/135`, `max_coeff=4`.
  - `D18` bounded binary DFS (`20s`, `200k` nodes): unsolved within budget (timeout; no tractable exact progress).
  - Decision: symmetry lane remains non-tractable in this budget; switched to Stage B/C.
- Stage B (general pipeline entry):
  - Start strict-feasible seed: `2252` blocks, `overcovered=0`, `oversubscribed_(r-1)=0`.
  - Add-only strict check across all `C(18,8)=43758` blocks found `0` feasible additions; entered destroy/repack immediately.
- Stage C (reserve-aware LNS + micro exact augment):
  - Phase C1: motif-coupled `1->2` strict augment loop around saturated 6-subset pressure motifs.
  - Net movement: `2252 -> 2288` (`+36`) while keeping strict feasibility.
  - Phase C2: motif-coupled `2->3` local repack with reserve-first refill (`reserve=1`, then flex completion).
  - Net movement: `2288 -> 2289` (`+1`) while keeping strict feasibility.
  - Post-check: no additional `1->2` or `2->3` augment found under the same neighborhood definitions.
- Stage D (residual exact completion gate):
  - Final `overcovered=0`, but uncovered ratio `13512/31824 = 0.4246`.
  - Residual not small; exact residual completion not attempted.

## Reused vs new this round
### Reused from previous runs
- Symmetry-first mandatory front gate with explicit orbit/coefficient diagnostics before fallback.
- Strict move gates: keep `overcovered_r_subsets=0`, `oversubscribed_r_minus_1_subsets=0`, and `r_minus_1_max_degree <= 6`.
- Motif-targeted neighborhood design around saturated `(r-1)` (here 6-subset) pressure motifs.

### Newly learned this round
- A deterministic motif-coupled `1->2` lane is still highly productive from the `2252` plateau for this instance (`+36` blocks before exhaustion).
- A follow-up reserve-aware `2->3` local repack can add another strict increment after `1->2` saturation.
- This run produced a new strict-feasible best for this run line: `2289` blocks with `overcovered=0` and zero `(r-1)` oversubscription.

## Observations
- Strict feasibility invariants held in all accepted checkpoints:
  - `overcovered_r_subsets = 0`
  - `oversubscribed_r_minus_1_subsets = 0`
  - `r_minus_1_max_degree = 6` with target `lambda_6 = 6`
- Add-only search is fully blocked at this frontier; improvements require destroy/repack augmentation.
- Point-balance improved alongside coverage gain (`gap 135 -> 125`).

## Metric trend (required)
| Stage | Blocks | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Cap-tail (`load=6`) | Oversubscribed `(r-1)` |
|---|---:|---:|---:|---:|---|---|---:|---:|
| Start seed | 2252 | 18016 | 13808 | 0 | `930..1065` (gap `135`) | `6 / 6` | 113 | 0 |
| After C1 (`1->2` pass) | 2288 | 18304 | 13520 | 0 | `950..1075` (gap `125`) | `6 / 6` | 120 | 0 |
| Final kept (C2 `2->3`) | 2289 | 18312 | 13512 | 0 | `950..1075` (gap `125`) | `6 / 6` | 119 | 0 |

Uncovered/overcovered trend:
- `13808/0 -> 13520/0 -> 13512/0`.

## Core advance
- advance statement:
  - Built a reproducible strict-feasible augment loop for `S(7,8,18)` that combines a bounded symmetry gate with motif-coupled `1->2` and reserve-aware `2->3` LNS repacks, yielding monotone verifier gains.
- evidence from this round (metrics, runtime, structure):
  - Symmetry lane was executed first and rejected with explicit `C18/D18` orbit/coefficient diagnostics plus bounded DFS outcomes.
  - Candidate improved `2252 -> 2289` blocks (`+37`) with strict invariants preserved.
  - Verifier moved `score 39.26 -> 40.56`, `exact_once 18016 -> 18312`, `uncovered 13808 -> 13512`, `overcovered 0 -> 0`.
  - Structural pressure also improved (`point_degree_gap 135 -> 125`).
- transfer value for next rounds:
  - Keep symmetry as a short mandatory gate, then switch quickly.
  - Run `1->2` motif-coupled augment pass to exhaustion first, then a reserve-aware `2->3` pass.
  - Preserve strict feasibility throughout to keep residual exact-completion eligibility open for later stages.

## Next-hypothesis
- hypothesis statement:
  - Alternating motif-coupled `2->3` and small-window `3->4` exact local repacks (with canonical motif dedup) will extend strict gains beyond `2289`.
- mechanism (why this should help):
  - After `1->2` saturation, remaining improvements likely require releasing larger transient slack around the same saturated 6-subset clusters; `3->4` windows can exploit combinations that pairwise scans cannot see.
- expected metric movement:
  - Improve `2289 -> 2293..2301` blocks,
  - reduce uncovered by `32..96`,
  - keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 6`.
- falsification / stop condition:
  - Stop this hypothesis if after `>=1200` tested motif-coupled neighborhoods (`2->3` + `3->4`) net gain is `< +2` blocks or if `3->4` success stays `<2%`.
