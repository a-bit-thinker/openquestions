# Round 3 Notes

Instance: S(7,8,20)
Expected blocks: 9690
Date (UTC): 2026-02-22

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: steiner_logs/run_20260222_012007/REPO_WIDE_HISTORY.md
- Global research log (all runs round1): steiner_logs/RESEARCH_LOG.md
- Global practice log (all runs round2-5): steiner_logs/PRACTICE_LOG.md
- Existence frontier report (all admissible triples): steiner_logs/EXISTENCE_FRONTIER.md
- Local paper notes: steiner_logs/PAPER_NOTES.md
- Latest prior run: run_20260221_013905
- Latest prior round1 notes source run: run_20260221_013905
- Latest prior round1 notes: steiner_logs/run_20260221_013905/notes/round_0001_notes.md
- Latest prior round5 notes source run: run_20260221_013905
- Latest prior round5 notes: steiner_logs/run_20260221_013905/notes/round_0005_notes.md
- Latest prior transfer: steiner_logs/run_20260221_013905/NEXT_GENERATION_TRANSFER.md

## Admissibility gate snapshot
```json
{
  "checks": [
    {"denominator": 8, "i": 0, "numerator": 77520, "quotient": 9690, "remainder": 0},
    {"denominator": 7, "i": 1, "numerator": 27132, "quotient": 3876, "remainder": 0},
    {"denominator": 6, "i": 2, "numerator": 8568, "quotient": 1428, "remainder": 0},
    {"denominator": 5, "i": 3, "numerator": 2380, "quotient": 476, "remainder": 0},
    {"denominator": 4, "i": 4, "numerator": 560, "quotient": 140, "remainder": 0},
    {"denominator": 3, "i": 5, "numerator": 105, "quotient": 35, "remainder": 0},
    {"denominator": 2, "i": 6, "numerator": 14, "quotient": 7, "remainder": 0}
  ],
  "divisibility_failures": [],
  "expected_block_count": 9690,
  "instance": {"n": 20, "q": 8, "r": 7},
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 9690,
    "lambda_1": 3876,
    "lambda_2": 1428,
    "lambda_3": 476,
    "lambda_4": 140,
    "lambda_5": 35,
    "lambda_6": 7
  }
}
```

## Research reuse
- Read steiner_logs/PAPER_NOTES.md, steiner_logs/RESEARCH_LOG.md, steiner_logs/PRACTICE_LOG.md, steiner_logs/EXISTENCE_FRONTIER.md, then steiner_logs/run_20260222_012007/KNOWLEDGE_CACHE.md before search.
- New web sources used this round: 0/1.

## Seeded proof directions (2-3)
1. Symmetry/orbit-compressed lane first: bounded cyclic/dihedral orbit diagnostics, then orbit-packed trial if tractable.
2. Strict feasible nibble/boost lane: conflict-free greedy packing from empty seed while preserving `overcovered=0` and `(r-1)` cap.
3. Motif-coupled LNS lane: uncovered-driven owner-set destroys (`k=1..3`) with exact local `k -> k+1` refill under strict row-owner and `(r-1)` cap gates.

Best drafted attempt selected: Seed 3 (motif-coupled strict LNS) after Seed 1 diagnostics showed symmetry quality lag on this instance in current budget.

## Plan
- Stage A: symmetry/orbit gate first and keep only if quality-competitive.
- Stage B: general pipeline entry (`nibble -> boosting`) with absorber/flex reserve discipline.
- Stage C: LNS destroy/repack (`k`-remove, exact local refill) with strict feasibility gates.
- Stage D: residual exact completion only if uncovered residual is small and overcoverage is zero.

## Work log
- Stage A (symmetry/orbit gate, mandatory first):
  - Cyclic diagnostics: `|O_7|=3876`, `|O_8|=6310`, binary/non-binary columns `6276/34`, `max_coeff=4`.
  - Dihedral diagnostics: `|O_7|=1980`, `|O_8|=3260`, binary/non-binary columns `3042/218`, `max_coeff=8`.
  - Orbit-packed bounded trials were strict-feasible but weaker than incumbent; best cyclic trial: `4635` blocks, `score=26.97`, `uncovered=40440`, `overcovered=0`.
  - Decision: symmetry lane not quality-competitive in this round budget; switch to general pipeline.
- Stage B (nibble/boosting with reserve discipline):
  - Multi-seed strict greedy baseline from empty candidate via bounded hybrid engine produced best seed at `5634` blocks (`score=41.40`, `uncovered=32448`, `overcovered=0`).
  - Add-only strict scan at this frontier: `0` feasible additions (maximal under add-only gate).
  - Absorber/flex reservation policy preserved via strict `(r-1)` cap gate (no oversubscription accepted).
- Stage C (LNS destroy/repack, strict):
  - Motif-coupled remove sets from uncovered 7-subset owner signatures, with random diversification.
  - Windows: `k=1..3`; refill required exact local gain (`k -> k+1` minimum), then greedy local extension if still strict-feasible.
  - Trial summary: `35000` neighborhoods, `170` accepted strict gains, runtime `19.21s`.
  - Net movement: `5634 -> 5807` blocks, `uncovered 32448 -> 31064`, `score 41.40 -> 43.90`, with `overcovered=0` and oversubscribed `(r-1)=0` throughout.
- Stage D (residual exact completion gate):
  - Residual repair check status: `ineligible`.
  - Reason: uncovered residual too large (`31064 > 20000` budget threshold) despite `overcovered=0`.

## Metric trend
| Stage | Blocks | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Oversubscribed `(r-1)` |
|---|---:|---:|---:|---:|---|---|---:|
| Start candidate | 5551 | 44408 | 33112 | 0 | gap 308 (`2064..2372`) | 7 / 7 | 0 |
| Symmetry best trial (cyclic) | 4635 | 37080 | 40440 | 0 | weaker quality lane | 7 / 7 | 0 |
| Stage-B best seed | 5634 | 45072 | 32448 | 0 | gap 361 (`2052..2413`) | 7 / 7 | 0 |
| Final (Stage-C LNS) | 5807 | 46456 | 31064 | 0 | gap 242 (`2185..2427`) | 7 / 7 | 0 |

Uncovered/overcovered trend (strict checkpoints):
- `33112/0 -> 32448/0 -> 31064/0`.

## Critical-gap self-verification pass
1. Arithmetic/invariant loop:
- Rechecked admissibility/divisibility and expected block count first.
- Result: pass.
2. Engine-feasibility loop:
- Ran symmetry diagnostics and bounded orbit-packed probes before fallback.
- Result: fallback justified by concrete quality gap.
3. Closure loop:
- Verified hard strict invariants at final checkpoint: `overcovered=0`, oversubscribed `(r-1)=0`, `(r-1)` max at target.
- Residual exact phase gate checked and rejected only due residual size.

Revision applied after verification:
- Moved from symmetry-front candidate generation to motif-coupled LNS as primary solve lane for this instance/round budget.

## Reuse vs genuinely new (explicit)
- Reused from previous runs:
  - hard admissibility gate before any search,
  - symmetry-first bounded gate then quick fallback,
  - strict feasibility acceptance (`overcovered=0`, no `(r-1)` oversubscription),
  - motif-coupled local exchange framing.
- Newly learned this round:
  - On `S(7,8,20)`, strict uncovered-driven owner-set LNS (`k=1..3`) gives high gain frequency from a maximal add-only frontier (`+173` from Stage-B seed, `+256` from round start).
  - Enforcing the 6-subset cap gate during refill can simultaneously preserve strictness and improve degree balance (`gap 361 -> 242`).

## Observations
- Add-only growth is exhausted at both the original frontier (`5551`) and the stronger Stage-B frontier (`5634`).
- Symmetry compression exists but bounded orbit-packed quality is materially worse than generalized strict LNS in this budget.
- Strict LNS gains remain sparse per neighborhood but accumulate reliably with motif-coupled proposals and exact local refill.

## Core advance
- advance statement:
  - Established a reproducible strict-feasible improvement loop for `S(7,8,20)` that combines mandatory symmetry triage with uncovered-driven `k -> k+1` LNS repacks.
- evidence from this round (metrics, runtime, structure):
  - Symmetry gate executed first with explicit orbit diagnostics and bounded packed probes.
  - Stage-B seed frontier improved to `5634` blocks, then Stage-C LNS improved to `5807` (`+173` from seed, `+256` from round start).
  - Verifier movement: `score 40.20 -> 43.90`, `exact_once 44408 -> 46456`, `uncovered 33112 -> 31064`, `overcovered=0` unchanged.
  - `(r-1)` hard gate remained strict: max `7` at target and oversubscribed count `0` throughout.
- transfer value for next rounds:
  - Keep symmetry diagnostics as front gate, but do not spend long budgets on orbit-packed construction for this instance.
  - Start from `5807` and continue motif-coupled strict LNS with explicit `k=2..4` windows and periodic neutral balance sweeps.

## Next-hypothesis
- hypothesis statement:
  - Two-step motif reuse with larger windows (`k=2..4`) and short motif-taboo will improve gain-per-1000 trials beyond the current `k<=3` loop from `5807`.
- mechanism (why this should help):
  - First accepted exchange releases local row/six-subset slack around the same uncovered motif; immediate reuse before re-hardening should increase second-step augment probability.
- expected metric movement:
  - improve `5807 -> 5850..5920` blocks,
  - reduce uncovered by `344..904`,
  - keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 7`.
- falsification / stop condition:
  - Stop this hypothesis if after `>=12000` motif-coupled trials the net gain is `< +12` blocks or if accepted-move rate drops below `0.2%` for two consecutive windows.
