# Round 2 Notes

Instance: S(6,7,19)
Expected blocks: 3876

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: steiner_logs/run_20260222_135457/REPO_WIDE_HISTORY.md
- Global research log (all runs round1): steiner_logs/RESEARCH_LOG.md
- Global practice log (all runs round2-5): steiner_logs/PRACTICE_LOG.md
- Global research paper (paper-style synthesis): steiner_logs/RESEARCH_PAPER.md
- Existence frontier report (all admissible triples): steiner_logs/EXISTENCE_FRONTIER.md
- Local paper notes: steiner_logs/PAPER_NOTES.md
- Latest prior run: run_20260222_052536
- Latest prior round1 notes source run: run_20260222_052536
- Latest prior round1 notes: steiner_logs/run_20260222_052536/notes/round_0001_notes.md
- Latest prior round5 notes source run: run_20260222_052536
- Latest prior round5 notes: steiner_logs/run_20260222_052536/notes/round_0005_notes.md
- Latest prior transfer: steiner_logs/run_20260222_052536/NEXT_GENERATION_TRANSFER.md
- Best known metrics across all runs for this instance at round open: score=0 run=run_20260222_093016 round=1 valid=false exact_once=0/27132 uncovered=27132 overcovered=0

## Admissibility gate snapshot
```json
{
  "checks": [
    {
      "denominator": 7,
      "i": 0,
      "numerator": 27132,
      "quotient": 3876,
      "remainder": 0
    },
    {
      "denominator": 6,
      "i": 1,
      "numerator": 8568,
      "quotient": 1428,
      "remainder": 0
    },
    {
      "denominator": 5,
      "i": 2,
      "numerator": 2380,
      "quotient": 476,
      "remainder": 0
    },
    {
      "denominator": 4,
      "i": 3,
      "numerator": 560,
      "quotient": 140,
      "remainder": 0
    },
    {
      "denominator": 3,
      "i": 4,
      "numerator": 105,
      "quotient": 35,
      "remainder": 0
    },
    {
      "denominator": 2,
      "i": 5,
      "numerator": 14,
      "quotient": 7,
      "remainder": 0
    }
  ],
  "divisibility_failures": [],
  "expected_block_count": 3876,
  "instance": {
    "n": 19,
    "q": 7,
    "r": 6
  },
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 3876,
    "lambda_1": 1428,
    "lambda_2": 476,
    "lambda_3": 140,
    "lambda_4": 35,
    "lambda_5": 7
  }
}
```

## Research reuse
- Reused cached sources only (`0/1` targeted web searches used this round).
- Reused strict hard gates from prior successful rounds: keep `overcovered=0` and `oversubscribed_(r-1)=0` throughout accepted moves.
- Reused symmetry-first engine policy, then pressure-triggered LNS handoff from practice logs.

## Symmetry/orbit stage (required first)
- Cyclic diagnostics (`C19`):
  - `|O_6|=1428`, `|O_7|=2652`, KM shape `1428 x 2652`, `nonbinary_share=0.000485`, `max_coeff=2`.
- Dihedral diagnostics (`D19`):
  - `|O_6|=756`, `|O_7|=1368`, KM shape `756 x 1368`, `nonbinary_share=0.054054`, `max_coeff=2`.
- Decision:
  - Symmetry compression was tractable and used as proposal structure (cyclic-orbit-guided scoring), but not sufficient alone for frontier movement from this seed (add-only orbit-guided growth gave +0).
  - Switched to general pipeline with strict LNS repacks.

## Plan
- Stage A: run symmetry/orbit diagnostics first; keep cyclic orbit guidance because coefficients were low.
- Stage B: reserve absorber/flex capacity early (`12%` reserve = `465` blocks; growth budget capped at `3411` to avoid greedy full consumption).
- Stage C: run strict pipeline `nibble(add-only probe) -> LNS destroy/repack -> add-only sweep`.
- Stage D: attempt residual exact completion only if residual gate becomes eligible.
- Stage E: proof-style critical-gap self-verification and revision.

## Proof workflow (adapted from local paper rules)
Seed proof directions generated before implementation:
1. Orbit-compressed direction: cyclic KM diagnostics suggest tractable symmetry structure; try orbit-guided strict growth first.
2. Reserve-first direction: keep absorber/flex reserve and avoid consuming all `3876` slots greedily.
3. LNS direction: remove `k=2..4` blocks around saturated 5-subsets and refill with exact/near-exact local `k->k+1` packs.

Drafted best attempt in this round:
- Start from the existing strict seed (`2438` blocks), run cyclic-guided strict add-only probe, then large-neighborhood destroy/repack waves with strict feasibility gates.

Critical-gap self-verification pass:
1. Gap A (admissibility): divisibility gate passed before search.
2. Gap B (strict feasibility): every accepted move checked to preserve `overcovered=0`, `(r-1)` oversubscription `0`, `r_minus_1_max_degree<=7`.
3. Gap C (engine choice): symmetry was tractable but additive movement was zero; fallback to LNS was triggered.
4. Gap D (residual closure): residual exact completion not eligible (`uncovered=9576`, fraction `9576/27132 = 0.3530 > 0.10` despite `overcovered=0`).

Revision after verification:
- Continued strict LNS continuation waves after first improvement (`2504 -> 2505 -> 2508`) until continuation plateaued.

## Work log
- Baseline candidate check:
  - Start from non-empty strict candidate: `2438` blocks, `score=48.06`, `overcovered=0`, `(r-1)` oversubscription `0`.
- Stage A symmetry/orbit:
  - Computed cyclic and dihedral orbit/KM diagnostics.
  - Kept cyclic guidance (better non-binary profile), but add-only orbit-guided probe produced `+0` from this frontier.
- Stage B reserve policy:
  - Reserved `465` blocks (`12%` of `3876`) for absorber/flex capacity; reserve never became binding at this frontier.
- Stage C strict constructive + LNS:
  - Applied repeated LNS neighborhoods (`k=2..4` remove, local exact/near-exact refill up to `k+1`).
  - Acceptance rule: strict feasibility hard gate + positive block gain, with limited neutral pressure-relief accepts.
  - Best strict progression: `2438 -> 2504 -> 2505 -> 2508` blocks.
- Stage D residual exact completion:
  - Gate checked and rejected as ineligible (residual fraction too large), so no residual exact-cover run was executed.

## Metric trend
| Checkpoint | Blocks | Score | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Oversubscribed `(r-1)` | 5-subset cap-hit count |
|---|---:|---:|---:|---:|---:|---|---|---:|---:|
| Baseline start | 2438 | 48.06 | 17066 | 10066 | 0 | gap 156 (`813..969`) | 7 / 7 | 0 | 137 |
| After LNS wave 1 | 2504 | 50.44 | 17528 | 9604 | 0 | gap 102 (`866..968`) | 7 / 7 | 0 | 70 |
| After continuation 1 | 2505 | 50.48 | 17535 | 9597 | 0 | gap 98 (`869..967`) | 7 / 7 | 0 | 65 |
| Final | 2508 | 50.59 | 17556 | 9576 | 0 | gap 97 (`871..968`) | 7 / 7 | 0 | 67 |

Uncovered/overcovered trend:
- `10066/0 -> 9604/0 -> 9597/0 -> 9576/0`.

## Observations
- Strict add-only growth is saturated at this frontier (`+0` under large sampled add-only probes).
- LNS `k=2..4 -> k+1` repacks remain productive under strict gates, including from already improved frontiers.
- `(r-1)` cap remains tight (`7/7`) but controllable: oversubscription stayed `0`; cap-hit count dropped materially vs baseline.
- Point-degree balance improved while coverage increased (gap `156 -> 97`).

## Reuse vs genuinely new (explicit)
- Reused from previous runs:
  - hard admissibility gate before search,
  - symmetry-first engine selection,
  - strict feasibility invariants (`overcovered=0`, `oversubscribed_(r-1)=0`),
  - late residual exact-cover gate discipline.
- Newly learned this round:
  - On `S(6,7,19)` at this seed, cyclic symmetry is useful for diagnostics/proposals but not enough by add-only growth.
  - Multi-block strict repacks continue to unlock coverage after add-only stalls.
  - Pressure relief around capped 5-subsets is the key mechanism for reopening strict growth opportunities here.

## Core advance
- advance statement:
  - Established the first strict-feasible constructive frontier for `S(6,7,19)` in this run, moving from `2438` to `2508` blocks while preserving zero collisions and zero `(r-1)` oversubscription.
- evidence from this round (metrics, runtime, structure):
  - Score improved `48.06 -> 50.59`.
  - Exact-once increased `17066 -> 17556`.
  - Uncovered reduced `10066 -> 9576` with `overcovered=0` maintained.
  - `(r-1)` load stayed at cap `7/7` with oversubscribed count always `0`.
  - Point-degree spread tightened `156 -> 97`.
- transfer value for next rounds:
  - Keep symmetry diagnostics as front gate, but trigger LNS early when strict add-only acceptance is zero.
  - Reuse pressure-targeted `k=2..4 -> k+1` repacks as the default mover for this instance frontier.

## Next-hypothesis
- hypothesis statement:
  - A two-tier strict schedule (pressure-relief neutral repacks followed by improvement-only repacks) will continue improving this frontier beyond `2508` blocks without violating strict gates.
- mechanism (why this should help):
  - Neutral repacks lower local 5-subset saturation, creating new feasible `k->k+1` repack opportunities that add-only cannot see.
- expected metric movement:
  - Move `2508 -> 2518..2558` blocks under unchanged strict gates.
  - Reduce uncovered by `70..350` while keeping `overcovered=0` and `(r-1)` oversubscription `0`.
  - Keep `r_minus_1_max_degree=7` and hold point-degree gap near or below `~110`.
- falsification / stop condition:
  - Reject this hypothesis if after `>=60000` strict LNS neighborhoods net gain is `< +8` blocks, or if any strict violation appears (`overcovered>0` or oversubscribed `(r-1)>0`).
