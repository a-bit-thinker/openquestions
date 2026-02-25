# Round 4 Notes

Instance: S(8,9,25)
Expected blocks: 120175

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: steiner_logs/run_20260222_154119/REPO_WIDE_HISTORY.md
- Global research log (all runs round1): steiner_logs/RESEARCH_LOG.md
- Global practice log (all runs round2-5): steiner_logs/PRACTICE_LOG.md
- Local paper notes: steiner_logs/PAPER_NOTES.md
- Latest prior run: run_20260222_052536
- Latest prior round1 notes source run: run_20260222_052536
- Latest prior round1 notes: steiner_logs/run_20260222_052536/notes/round_0001_notes.md
- Latest prior round5 notes source run: run_20260222_052536
- Latest prior round5 notes: steiner_logs/run_20260222_052536/notes/round_0005_notes.md
- Latest prior transfer: steiner_logs/run_20260222_052536/NEXT_GENERATION_TRANSFER.md
- Best known metrics across all runs for this instance at round open: none

## Admissibility gate snapshot
```json
{
  "checks": [
    {
      "denominator": 9,
      "i": 0,
      "numerator": 1081575,
      "quotient": 120175,
      "remainder": 0
    },
    {
      "denominator": 8,
      "i": 1,
      "numerator": 346104,
      "quotient": 43263,
      "remainder": 0
    },
    {
      "denominator": 7,
      "i": 2,
      "numerator": 100947,
      "quotient": 14421,
      "remainder": 0
    },
    {
      "denominator": 6,
      "i": 3,
      "numerator": 26334,
      "quotient": 4389,
      "remainder": 0
    },
    {
      "denominator": 5,
      "i": 4,
      "numerator": 5985,
      "quotient": 1197,
      "remainder": 0
    },
    {
      "denominator": 4,
      "i": 5,
      "numerator": 1140,
      "quotient": 285,
      "remainder": 0
    },
    {
      "denominator": 3,
      "i": 6,
      "numerator": 171,
      "quotient": 57,
      "remainder": 0
    },
    {
      "denominator": 2,
      "i": 7,
      "numerator": 18,
      "quotient": 9,
      "remainder": 0
    }
  ],
  "divisibility_failures": [],
  "expected_block_count": 120175,
  "instance": {
    "n": 25,
    "q": 9,
    "r": 8
  },
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 120175,
    "lambda_1": 43263,
    "lambda_2": 14421,
    "lambda_3": 4389,
    "lambda_4": 1197,
    "lambda_5": 285,
    "lambda_6": 57,
    "lambda_7": 9
  }
}
```

## Research reuse
- Reused cache-first material only (`PAPER_NOTES`, `RESEARCH_LOG`, `PRACTICE_LOG`, current `KNOWLEDGE_CACHE`, latest prior run notes/transfer).
- Targeted web searches used this round: `0/1`.
- External links added this round: `0`.

## Plan
- Stage A: run symmetry/orbit compression first (cyclic full-orbit probe) and keep the lane only if tractable.
- Stage B: reserve absorber/flex capacity early (`12%` reserve; build cap `105754`) before generalized greedy growth.
- Stage C: run general strict pipeline (`nibble -> boosting -> LNS repair`) with hard feasibility gates.
- Stage D: run residual exact completion only if uncovered residual is small and strict gate is eligible.

## Proof workflow (adapted from local paper rules)
Seed directions generated before implementation:
1. Symmetry/orbit seed: cyclic orbit-packing first; keep it only when sampled coefficients stay binary-like and bounded packed probes produce strict gains.
2. Reserve-first nibble seed: uncovered-8-subset-driven additions under `overcovered=0` and `(r-1)` cap enforcement, while preserving flex reserve.
3. LNS seed: motif-coupled `k>1` remove/refill around high-load 7-subset motifs using local near-exact repacks.

Drafted best attempt in this round:
- Start from empty candidate and execute the mandatory architecture in order: symmetry gate -> reserve-first growth -> LNS repair -> residual gate.

Critical-gap self-verification pass:
1. Gap A (admissibility): divisibility gate rechecked before search; pass.
2. Gap B (engine choice): symmetry lane remained tractable and productive (`sample_nonbinary_share=0.0`, `sample_max_coeff=1`, probe accepted `255/320` orbits), so symmetry was used as primary engine rather than immediate fallback.
3. Gap C (repair correctness): all accepted operations preserved `overcovered=0` and `oversubscribed_(r-1)=0`.
4. Gap D (closure): residual exact completion gate failed (`uncovered=584469`, uncovered fraction `0.5404`), so exact residual was not attempted.

Revision after verification:
- After the first nibble+LNS cycle, add-only acceptance decayed sharply (`575` accepts in first million attempts, then only `15` in second million).
- Revised schedule inside budget to a second LNS wave after the second nibble pass; this recovered additional strict gains (`+95` blocks over Stage E).

## Work log
- Stage A symmetry/orbit diagnostics + bounded probe:
  - sample diagnostics: `120` cyclic orbits, sampled non-binary share `0.0`, sampled max coefficient `1`.
  - packed strict probe: `320` orbit trials, `255` accepted full orbits, `6375` strict blocks.
  - decision: symmetry lane is tractable on this instance, keep as primary engine.
- Stage B reserve-first orbit continuation:
  - absorber/flex reserve fixed at `12%` (`14421` blocks); build cap `105754` (non-binding this round).
  - continuation trials: `199680`.
  - accepted full orbits: `1924`.
  - movement: `6375 -> 54475` blocks.
- Stage C uncovered-driven nibble/boosting:
  - attempts: `1,000,000`.
  - strict accepts: `575`.
  - movement: `54475 -> 55050` blocks.
- Stage D LNS repair (`k>1` remove/refill):
  - iterations: `200`.
  - positive neighborhoods: `56`.
  - movement: `55050 -> 55124` blocks.
- Stage E second nibble + second LNS wave:
  - second nibble attempts: `1,000,000`, strict accepts: `15`.
  - second LNS iterations: `200`, positive neighborhoods: `70`.
  - movement: `55124 -> 55234` blocks.
- Stage F residual exact gate:
  - not attempted; reason: `not eligible: uncovered residual too large`.

## Metric trend
| Checkpoint | Blocks | Score | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Oversubscribed `(r-1)` |
|---|---:|---:|---:|---:|---:|---|---|---:|
| Baseline | 0 | 0.00 | 0 | 1081575 | 0 | gap 0 (`0..0`) | 0 / 9 | 0 |
| Stage A symmetry probe | 6375 | 0.00 | 57375 | 1024200 | 0 | gap 0 (`2295..2295`) | 4 / 9 | 0 |
| Stage B orbit continuation | 54475 | 23.46 | 490275 | 591300 | 0 | gap 0 (`19611..19611`) | 8 / 9 | 0 |
| Stage C nibble/boosting | 55050 | 24.13 | 495450 | 586125 | 0 | gap 0 (`19818..19818`) | 8 / 9 | 0 |
| Stage D LNS repair | 55124 | 24.22 | 496116 | 585459 | 0 | gap 20 (`19836..19856`) | 8 / 9 | 0 |
| Stage E nibble revisit | 55139 | 24.24 | 496251 | 585324 | 0 | gap 22 (`19838..19860`) | 8 / 9 | 0 |
| Final frontier | 55234 | 24.35 | 497106 | 584469 | 0 | gap 32 (`19866..19898`) | 8 / 9 | 0 |

Uncovered/overcovered trend:
- `1081575/0 -> 1024200/0 -> 591300/0 -> 586125/0 -> 585459/0 -> 585324/0 -> 584469/0`.

## Observations
- This instance is materially different from recent high-`r` frontiers where symmetry failed: cyclic orbit compression is clean here (binary sampled coefficients) and produced the bulk of progress.
- Strict feasibility remained robust throughout: `overcovered` never rose above `0`, and `(r-1)` max stayed below cap (`8/9`), leaving headroom.
- Add-only/nibble quickly decays after orbit seeding, while motif-coupled `k>1` LNS continues to harvest additional strict gains.
- Residual exact completion remains structurally premature at this frontier.

## Reuse vs genuinely new (explicit)
- Reused from previous runs:
  - hard admissibility gate before any constructive work,
  - symmetry-first engine gate,
  - reserve-first discipline,
  - strict feasibility invariants (`overcovered=0`, `oversubscribed_(r-1)=0`),
  - residual exact-cover late gate.
- Newly learned this round:
  - For `S(8,9,25)`, cyclic full-orbit strict packing is tractable and high-yield (`2179` accepted full orbits across probe+continuation).
  - Alternating nibble and LNS is still useful after a strong orbit seed: LNS supplied most late gains when add-only acceptance collapsed.
  - Current frontier remains strictly below `(r-1)` cap (`8/9`), so cap-pressure is not yet the primary blocker at this scale.

## Core advance
- advance statement:
  - Established the first strict-feasible frontier for `S(8,9,25)` in this repository by moving from empty candidate to `55234` blocks while preserving zero collisions and zero `(r-1)` oversubscription.
- evidence from this round (metrics, runtime, structure):
  - Score improved `0.00 -> 24.35`.
  - Exact-once improved `0 -> 497106`.
  - Uncovered reduced `1081575 -> 584469` with `overcovered=0` throughout.
  - `(r-1)` load stayed below cap (`max 8` vs target `9`), oversubscribed count `0`.
  - Required architecture was executed in order: symmetry gate first; reserve set early; `k>1` LNS used; residual exact gate checked and deferred.
- transfer value for next rounds:
  - Keep symmetry/orbit lane as default Stage A for this exact instance; it is not just a diagnostic here.
  - Keep alternating nibble/LNS waves after orbit seeding; add-only alone underuses remaining strict headroom.
  - Maintain strict gates hard; they did not block progress and preserved certificate transferability.

## Next-hypothesis
- hypothesis statement:
  - An alternating tri-phase loop (`short orbit micro-burst -> uncovered-driven nibble -> motif-coupled LNS with larger windows k=4..7`) will outperform repeating nibble+LNS alone from `55234`.
- mechanism (why this should help):
  - Orbit micro-bursts inject globally balanced fresh structure; nibble captures low-hanging uncovered 8-subsets; larger-window LNS can repack local bottlenecks that block single-block additions once acceptance decays.
- expected metric movement:
  - Improve `55234 -> 56000..57500` blocks.
  - Reduce uncovered by `6900..20300`.
  - Keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 9`.
- falsification / stop condition:
  - Reject if after `>=250000` extra orbit trials and `>=400` extra LNS neighborhoods net gain is `< +250` blocks, or if gain-per-1000 neighborhoods is not above this round's Stage D+E baseline.
