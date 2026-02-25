# Round 2 Notes

Instance: S(6,7,23)
Expected blocks: 14421

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: steiner_logs/run_20260222_154119/REPO_WIDE_HISTORY.md
- Global research log (all runs round1): steiner_logs/RESEARCH_LOG.md
- Global practice log (all runs round2-5): steiner_logs/PRACTICE_LOG.md
- Local paper notes: steiner_logs/PAPER_NOTES.md
- Latest prior run: run_20260222_052536
- Latest prior round1 notes: steiner_logs/run_20260222_052536/notes/round_0001_notes.md
- Latest prior round5 notes: steiner_logs/run_20260222_052536/notes/round_0005_notes.md
- Latest prior transfer: steiner_logs/run_20260222_052536/NEXT_GENERATION_TRANSFER.md
- Best known open metric for this instance at round start: score=50.09 exact_once=64960/100947 uncovered=35987 overcovered=0

## Admissibility gate snapshot
```json
{
  "checks": [
    {"i": 0, "numerator": 100947, "denominator": 7, "quotient": 14421, "remainder": 0},
    {"i": 1, "numerator": 26334, "denominator": 6, "quotient": 4389, "remainder": 0},
    {"i": 2, "numerator": 5985, "denominator": 5, "quotient": 1197, "remainder": 0},
    {"i": 3, "numerator": 1140, "denominator": 4, "quotient": 285, "remainder": 0},
    {"i": 4, "numerator": 171, "denominator": 3, "quotient": 57, "remainder": 0},
    {"i": 5, "numerator": 18, "denominator": 2, "quotient": 9, "remainder": 0}
  ],
  "divisibility_failures": [],
  "expected_block_count": 14421,
  "instance": {"n": 23, "q": 7, "r": 6},
  "is_admissible": true,
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
- Reused local-paper/cache policy and all mandatory cross-run memory first.
- New web search used this round: 0/1 (none needed).
- Reused strict feasibility policy from prior runs: keep `overcovered=0` and zero `(r-1)` oversubscription.

## Plan
- Stage A: symmetry/orbit compression gate first (cyclic/dihedral diagnostics + packed probe).
- Stage B: reserve absorber/flex capacity early (12% of expected blocks) before any greedy growth.
- Stage C: general strict pipeline `nibble -> boosting/repair -> absorber/flex completion` with LNS (`k`-destroy + local refill).
- Stage D: residual exact completion only if uncovered is small and strict gate is eligible.
- Stage E: proof-style critical-gap self-verification and revise-on-gap within round budget.

## Proof workflow (adapted from local paper rules)
Seed proof directions generated before implementation:
1. Symmetry/orbit direction: try cyclic/dihedral compression first and keep lane only if coefficients are mostly binary and probe is competitive.
2. Reserve-first neutral-balance direction: reduce point-degree and saturated 5-face pressure before aggressive positive repacks.
3. Motif-coupled LNS direction: remove local conflicting block sets, then refill with exact/near-exact local packs around uncovered and cap-tight motifs.

Drafted best attempt:
- Start from incumbent strict frontier (`9280` blocks), execute Stage A gate, then run strict constructive cycles with a revise step if positive-gain LNS stalls.

Critical-gap self-verification pass:
1. Gap A (admissibility): pass (all 6 divisibility checks remainder 0).
2. Gap B (engine choice): symmetry gate failed tractability-quality threshold (`sample_nonbinary_share=1.0` in both cyclic/dihedral diagnostics; cyclic packed probe only `5267` blocks), so switched to general pipeline.
3. Gap C (repair correctness): all accepted moves preserved `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree=9` at target.
4. Gap D (closure): residual exact completion rejected by gate (`uncovered=35938`, uncovered fraction `0.3560` > 0.10).

Revision after verification:
- First strict LNS pass had no net gain.
- Revised to a two-phase loop: neutral 1->1 balance first, then positive-gain LNS only.
- This revision produced the accepted frontier lift (`9280 -> 9287`).

## Work log
- Stage A symmetry/orbit gate:
  - Cyclic diagnostics: estimated orbit counts `rows=4389`, `cols=10659`, sampled non-binary share `1.0`, sampled max coefficient `23`.
  - Dihedral diagnostics: sampled non-binary share `1.0`, sampled max coefficient `92`.
  - Cyclic packed strict probe (1500 orbit trials): `229` accepted orbits, `5267` blocks, `(r-1)` max load `7`.
  - Decision: symmetry lane not tractable/productive for this frontier.
- Stage B reserve-first setup:
  - Reserved 12% of expected block count (`1731` slots) as absorber/flex budget (explicitly kept non-greedy).
- Stage C strict constructive pipeline:
  - C1 nibble/add-only probe from incumbent: `+0` blocks.
  - C2 first strict LNS run: `51788` neighborhoods, many neutral accepts, net `+0` blocks.
  - C3 neutral-balance revision (`1->1` strict swaps): point-degree gap `413 -> 366`, cap-9 5-faces `83 -> 82` at fixed `9280` blocks.
  - C4 positive strict LNS from balanced state: `21155` neighborhoods, `6` positive accepts, net `+7` blocks.
  - Final strict frontier: `9287` blocks.
- Stage D residual exact completion gate:
  - Not attempted (ineligible due large uncovered residual).

## Metric trend
| Checkpoint | Blocks | Score | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Oversubscribed `(r-1)` |
|---|---:|---:|---:|---:|---:|---|---|---:|
| Baseline start | 9280 | 50.09 | 64960 | 35987 | 0 | gap 413 (`2597..3010`) | 9 / 9 | 0 |
| After nibble probe | 9280 | 50.09 | 64960 | 35987 | 0 | gap 413 (`2597..3010`) | 9 / 9 | 0 |
| After neutral balance | 9280 | 50.09 | 64960 | 35987 | 0 | gap 366 (`2623..2989`) | 9 / 9 | 0 |
| Final strict frontier | 9287 | 50.16 | 65009 | 35938 | 0 | gap 368 (`2624..2992`) | 9 / 9 | 0 |

Uncovered/overcovered trend:
- `35987/0 -> 35987/0 -> 35987/0 -> 35938/0`.

## Observations
- Symmetry compression was tested first as required and rejected on measured quality, not skipped.
- Neutral rebalancing was not sufficient alone, but it unlocked subsequent positive strict repacks (`+7` blocks).
- Hard feasibility gates remained intact across all accepted moves.
- Residual exact completion remains structurally premature for this instance at current uncovered fraction.

## Reuse vs genuinely new (explicit)
- Reused from previous runs:
  - hard admissibility gate before search,
  - symmetry-first engine selection contract,
  - strict feasibility invariants (`overcovered=0`, zero `(r-1)` oversubscription),
  - late residual exact-cover gate discipline.
- Newly learned this round:
  - For `S(6,7,23)` at the `9280` plateau, direct positive LNS was too weak unless preceded by neutral balance pressure relief.
  - A two-phase strict schedule (`neutral balance -> positive LNS`) can strictly improve this frontier (`+7`) while preserving all hard gates.
  - Symmetry diagnostics for this instance show heavy non-binary orbit incidence (`share=1.0` in sampled cyclic/dihedral orbit matrices), supporting early fallback.

## Core advance
- advance statement:
  - Broke the long-standing strict `S(6,7,23)` frontier from `9280` to `9287` blocks while preserving `overcovered=0` and zero `(r-1)` oversubscription.
- evidence from this round (metrics, runtime, structure):
  - Score improved `50.09 -> 50.16`.
  - Exact-once improved `64960 -> 65009`.
  - Uncovered reduced `35987 -> 35938` with `overcovered=0` unchanged.
  - `(r-1)` load remained at cap (`9/9`) with oversubscribed count `0` throughout.
  - Point-degree spread improved versus baseline (`413 -> 368`; best intermediate `366`).
- transfer value for next rounds:
  - Use a mandatory two-phase strict loop on this instance: neutral pressure relief first, then positive LNS.
  - Keep symmetry gate short and evidence-based; this instance should switch quickly to the general pipeline.

## Next-hypothesis
- hypothesis statement:
  - A motif-coupled mixed-window strict LNS schedule (`k=2..5` core plus periodic `k=6..8` bursts) starting from the new `9287` frontier will outperform fixed-window continuation.
- mechanism (why this should help):
  - Small windows keep acceptance rate nonzero; periodic larger windows can cross the residual local bottlenecks that blocked further `+1` gains after trial ~700.
- expected metric movement:
  - Improve `9287 -> 9300..9340` blocks.
  - Reduce uncovered by `91..371` while keeping `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree<=9`.
- falsification / stop condition:
  - Reject this hypothesis if after `>=30000` neighborhoods the net gain is `< +5` blocks or if gain-per-1000 neighborhoods is not above the current round's late-stage baseline.
