# Round 2 Notes

Instance: S(6,7,23)
Expected blocks: 14421
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
    {"denominator": 7, "i": 0, "numerator": 100947, "quotient": 14421, "remainder": 0},
    {"denominator": 6, "i": 1, "numerator": 26334, "quotient": 4389, "remainder": 0},
    {"denominator": 5, "i": 2, "numerator": 5985, "quotient": 1197, "remainder": 0},
    {"denominator": 4, "i": 3, "numerator": 1140, "quotient": 285, "remainder": 0},
    {"denominator": 3, "i": 4, "numerator": 171, "quotient": 57, "remainder": 0},
    {"denominator": 2, "i": 5, "numerator": 18, "quotient": 9, "remainder": 0}
  ],
  "divisibility_failures": [],
  "expected_block_count": 14421,
  "instance": {"n": 23, "q": 7, "r": 6},
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 14421,
    "lambda_1": 4389,
    "lambda_2": 1197,
    "lambda_3": 285,
    "lambda_4": 57,
    "lambda_5": 9
  }
}
```

## Research reuse
- Read and reused cache and cross-run files first; no new web source was needed (`0/1` targeted searches used).
- Reused from previous runs:
  - strict admissibility as a hard pre-search gate,
  - symmetry front-gate then quick fallback,
  - strict feasibility invariants (`overcovered=0`, no `(r-1)` oversubscription),
  - motif-coupled LNS/augment style for plateau breaking.

## Proof workflow (seed -> draft -> critical-gap -> revise)
### Seed proof directions (2-3)
1. Symmetry-compressed orbit lane:
- Use cyclic/dihedral orbit compression first and keep it only if both tractable and quality-competitive.
2. Strict add-only lane:
- If current strict seed still has feasible additions, expand without deletions.
3. LNS destroy/repack lane:
- Remove `k` conflict blocks around uncovered motifs, then strict refill; accept only strict improvements.

### Draft best attempt
- Executed Seed 1 first (mandatory symmetry gate), then Seed 2, then Seed 3 as the main improvement engine.
- Selected Seed 3 as the best draft because Seed 1 underperformed and Seed 2 was exhausted.

### Critical-gap self-verification pass
1. Gap A: admissibility/integrality gate
- Result: pass.
2. Gap B: symmetry tractability and competitiveness
- Diagnostics:
  - `C23`: `|O_6|=4389`, `|O_7|=10659`, binary/non-binary columns `10648/11`, `max_coeff=2`.
  - `D23`: `|O_6|=2277`, `|O_7|=5412`, binary/non-binary columns `5247/165`, `max_coeff=2`.
- Symmetry candidate (cyclic orbit pack) was strict-feasible but weaker:
  - `7912` blocks, `score=36.81`, `uncovered=45563`, `overcovered=0`.
- Decision: symmetry is tractable but not quality-competitive for this round budget; switch to general pipeline.
3. Gap C: strict add-only feasibility
- Multi-seed add-only boosting from current strict seed produced `0` net additions (`9237 -> 9237`).
- Decision: additive lane exhausted; escalate to LNS.
4. Gap D: late residual exact completion gate
- Final candidate has `overcovered=0` but residual uncovered is large (`35987/100947`), so residual exact completion is not eligible.

### Revision applied after verification
- Increased LNS window size (`k` up to `16`) and refill budget (`0.35s`) after observing sparse-event gains in smaller windows.
- This revision yielded the best round result (`9259 -> 9280` blocks).

## Plan (executed)
- Stage A: symmetry/orbit compression gate first.
- Stage B: strict add-only nibble/boosting from current strict seed.
- Stage C: reserve-aware LNS repairs (remove `k`, strict global refill).
- Stage D: residual exact completion gate only if residual is small and `overcovered=0`.

## Work log
- Stage A (symmetry gate):
  - Ran cyclic/dihedral orbit diagnostics and coefficient histograms.
  - Built one cyclic-orbit packed candidate for an actual tractability+quality check.
  - Outcome: tractable but underperforms incumbent strict seed.
- Stage B (add-only):
  - Refill from incumbent strict seed found no feasible additions.
- Stage C (LNS repair):
  - Executed uncovered-driven remove/refill windows with strict acceptance.
  - Progression:
    - `9237 -> 9249` (first pass),
    - `9249 -> 9259` (restart pass),
    - `9259 -> 9280` (intensified pass).
- Stage D (residual exact completion):
  - Gate checked and not opened due large residual uncovered set.

## Metric trend
| Stage | Blocks | Score | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Oversubscribed `(r-1)` |
|---|---:|---:|---:|---:|---:|---|---|---:|
| Start seed | 9237 | 49.67 | 64659 | 36288 | 0 | gap 426 (`2578..3004`) | 9 / 9 | 0 |
| Symmetry cyclic test | 7912 | 36.81 | 55384 | 45563 | 0 | gap 0 (`2408..2408`) | 8 / 9 | 0 |
| Add-only best | 9237 | 49.67 | 64659 | 36288 | 0 | gap 426 (`2578..3004`) | 9 / 9 | 0 |
| LNS pass 1 best | 9249 | 49.79 | 64743 | 36204 | 0 | gap 425 (`2582..3007`) | 9 / 9 | 0 |
| LNS pass 2 best | 9259 | 49.89 | 64813 | 36134 | 0 | gap 423 (`2585..3008`) | 9 / 9 | 0 |
| Final (intensified LNS) | 9280 | 50.09 | 64960 | 35987 | 0 | gap 413 (`2597..3010`) | 9 / 9 | 0 |

Uncovered/overcovered trend (best checkpoints):
- `36288/0 -> 36204/0 -> 36134/0 -> 35987/0`.

## Reuse vs genuinely new (explicit)
- Reused this round:
  - mandatory symmetry gate-first discipline,
  - strict-feasible acceptance (`overcovered=0`, no `(r-1)` oversubscription),
  - motif-coupled LNS destroy/repack pattern.
- Newly learned this round:
  - For `S(6,7,23)`, symmetry compression is strong but direct cyclic-orbit packing is quality-inferior to non-invariant strict LNS from the current seed.
  - Add-only expansion is exhausted at `9237`; gains now come from multi-block destroy/repack windows.
  - Larger LNS windows (`k` up to ~16) materially improve gain frequency versus smaller windows.

## Observations
- The frontier is sparse-gain but still improvable under strict feasibility.
- Strict feasibility stayed intact through all accepted moves:
  - `overcovered_r_subsets=0`,
  - `oversubscribed_r_minus_1_subsets=0`,
  - `r_minus_1_max_degree=9` (target `lambda_5=9`).
- Point-degree balance improved while block count increased (`gap 426 -> 413`).

## Core advance
- advance statement:
  - Established a reproducible strict-feasible plateau-break path for `S(6,7,23)` by combining a mandatory symmetry front gate with uncovered-driven LNS destroy/repack intensification.
- evidence from this round (metrics, runtime, structure):
  - Symmetry gate executed first with explicit orbit/coefficient diagnostics and an actual cyclic packed trial.
  - Add-only strict stage confirmed plateau (`9237 -> 9237`).
  - LNS stages advanced the strict frontier `9237 -> 9280` with monotone uncovered reduction `36288 -> 35987` and `overcovered=0` throughout.
  - Point-degree spread improved `426 -> 413` while preserving `(r-1)` max at target (`9`).
- transfer value for next rounds:
  - Keep symmetry diagnostics as a front gate, but use it as a bounded quality test for this instance.
  - Use intensified uncovered-driven LNS as the default first repair lane from `9280`.
  - Continue strict acceptance discipline and checkpoint best strict candidate frequently.

## Next-hypothesis
- hypothesis statement:
  - Two-step motif-coupled LNS chains (reusing the same uncovered motif neighborhood across consecutive windows) with periodic neutral rebalance sweeps will outperform uncoupled random-window LNS from `9280`.
- mechanism (why this should help):
  - First-window success opens transient local slack; immediate reuse of that motif should increase second-window augment probability before constraints re-harden.
  - Periodic neutral rebalance reduces degree-tail concentration, which should increase feasible refill options in later windows.
- expected metric movement:
  - Improve `9280 -> 9310..9380` blocks,
  - reduce uncovered by `210..700`,
  - keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 9`.
- falsification / stop condition:
  - Stop this hypothesis if after `>=500` intensified windows:
  - net gain is `< +6` blocks,
  - or second-window success rate after a first-window gain is `< 8%`,
  - or any accepted move violates strict feasibility gates.
