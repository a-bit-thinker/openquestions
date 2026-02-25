# Round 4 Notes

Instance: S(8,9,21)
Expected blocks: 22610

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: steiner_logs/run_20260222_052536/REPO_WIDE_HISTORY.md
- Global research log (all runs round1): steiner_logs/RESEARCH_LOG.md
- Global practice log (all runs round2-5): steiner_logs/PRACTICE_LOG.md
- Global research paper (paper-style synthesis): steiner_logs/RESEARCH_PAPER.md
- Existence frontier report (all admissible triples): steiner_logs/EXISTENCE_FRONTIER.md
- Local paper notes: steiner_logs/PAPER_NOTES.md
- Latest prior run: run_20260222_012007
- Latest prior round1 notes source run: run_20260222_012007
- Latest prior round1 notes: steiner_logs/run_20260222_012007/notes/round_0001_notes.md
- Latest prior round5 notes source run: run_20260222_012007
- Latest prior round5 notes: steiner_logs/run_20260222_012007/notes/round_0005_notes.md
- Latest prior transfer: steiner_logs/run_20260222_012007/NEXT_GENERATION_TRANSFER.md
- Best known metrics across all runs for this instance: score=35.16 run=run_20260222_012007 round=4 valid=false exact_once=109242/203490 uncovered=94248 overcovered=0

## Admissibility gate snapshot
```json
{
  "checks": [
    {
      "denominator": 9,
      "i": 0,
      "numerator": 203490,
      "quotient": 22610,
      "remainder": 0
    },
    {
      "denominator": 8,
      "i": 1,
      "numerator": 77520,
      "quotient": 9690,
      "remainder": 0
    },
    {
      "denominator": 7,
      "i": 2,
      "numerator": 27132,
      "quotient": 3876,
      "remainder": 0
    },
    {
      "denominator": 6,
      "i": 3,
      "numerator": 8568,
      "quotient": 1428,
      "remainder": 0
    },
    {
      "denominator": 5,
      "i": 4,
      "numerator": 2380,
      "quotient": 476,
      "remainder": 0
    },
    {
      "denominator": 4,
      "i": 5,
      "numerator": 560,
      "quotient": 140,
      "remainder": 0
    },
    {
      "denominator": 3,
      "i": 6,
      "numerator": 105,
      "quotient": 35,
      "remainder": 0
    },
    {
      "denominator": 2,
      "i": 7,
      "numerator": 14,
      "quotient": 7,
      "remainder": 0
    }
  ],
  "divisibility_failures": [],
  "expected_block_count": 22610,
  "instance": {
    "n": 21,
    "q": 9,
    "r": 8
  },
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 22610,
    "lambda_1": 9690,
    "lambda_2": 3876,
    "lambda_3": 1428,
    "lambda_4": 476,
    "lambda_5": 140,
    "lambda_6": 35,
    "lambda_7": 7
  }
}
```

## Research reuse
- Read steiner_logs/PAPER_NOTES.md, steiner_logs/RESEARCH_LOG.md, steiner_logs/PRACTICE_LOG.md, steiner_logs/RESEARCH_PAPER.md, steiner_logs/EXISTENCE_FRONTIER.md, then steiner_logs/run_20260222_052536/KNOWLEDGE_CACHE.md.
- Targeted web search used this round: 0/1.

## Plan
- Stage A: symmetry/orbit front gate first (cyclic + dihedral diagnostics) and keep symmetry lane if tractable.
- Stage B: reserve absorber/flex capacity early, then run strict boosting/repair.
- Stage C: run strict `k>1` LNS destroy/repack neighborhoods.
- Stage D: residual exact-completion gate check + critical-gap self-verification and revision.

## Proof workflow (adapted from local paper rules)
Seed directions generated before implementation:
1. Symmetry-first seed: cyclic/dihedral orbit compression with strict orbit-packed probe.
2. Strict constructive seed: reserve-first local repair with hard caps `c_8<=1`, `c_7<=7`.
3. Strict LNS seed: remove `k>1` blocks and refill by exact/near-exact local repack.

Drafted best attempt this round:
- Symmetry lane was executed first and was tractable.
- Cyclic strict seed was built and evaluated.
- Because cyclic seed quality was much lower than incumbent strict candidate, switched to general pipeline and ran strict local repacks from incumbent.

Critical-gap self-verification pass:
1. Gap A (admissibility): divisibility rechecked; pass.
2. Gap B (engine feasibility):
   - Cyclic diagnostics: `|O_8|=9690`, `|O_9|=14000`, non-binary columns `17/14000`, `max_coeff=3`.
   - Dihedral diagnostics: `|O_8|=4950`, `|O_9|=7105`, non-binary columns `214/7105`, `max_coeff=6`.
   - Verdict: symmetry mode is tractable (especially cyclic).
3. Gap C (strict correctness): every accepted move preserved `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree<=7`.
4. Gap D (closure): residual exact completion gate checked; ineligible (`uncovered fraction = 92286/203490 = 0.4535` >> built-in threshold).

Revision after verification:
- Tightened Stage B to repeated exact `1->2` strict local repacks around removed blocks (high-yield lane).
- Kept Stage C as `k>1` LNS exploration, but no accepted improvement under current neighborhood/budget.

## Work log
- Stage A symmetry/orbit gate (executed first, mandatory):
  - Cyclic and dihedral diagnostics completed (see Gap B above).
  - Strict cyclic orbit-packed probe (best of 12 seeds):
    - blocks `9982`, `score=21.81`, `exact_once=89838`, `uncovered=113652`, `overcovered=0`.
    - point-degree spread `4278..4278` (gap `0`), `(r-1)` max/target `7/7`.
  - Decision: symmetry is tractable, but cyclic strict seed is weaker than incumbent strict frontier (`12138` blocks), so switch to general pipeline.
- Stage B reserve-first strict boosting/repair:
  - Absorber/flex reserve set early to `2713` slots (12% of expected size), operational block cap `19897`; reserve remained non-binding.
  - Started from incumbent strict candidate: `12138` blocks, `score=35.16`, `uncovered=94248`, `overcovered=0`.
  - Strict local repack (`1->2`) passes:
    - pass1: `12339` blocks, `score=36.40`, `uncovered=92439`, `overcovered=0`.
    - pass2: `12354` blocks, `score=36.50`, `uncovered=92304`, `overcovered=0`.
    - pass3: `12356` blocks, `score=36.51`, `uncovered=92286`, `overcovered=0`.
    - pass4: no further improvement.
  - Net Stage B movement: `+218` strict blocks.
- Stage C strict LNS destroy/repack (`k>1`):
  - Neighborhood sizes `k in {2,3,4,5,6}`; bounded budget `5000` attempts.
  - Accepted improving repacks: `0` (no net gain beyond Stage B frontier).
- Stage D residual exact completion gate:
  - Strict gates passed (`overcovered=0`, `(r-1)` oversubscribed `0`), but residual remains too large for exact completion.

## Metric trend
| Checkpoint | Blocks | Score | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Oversubscribed `(r-1)` |
|---|---:|---:|---:|---:|---:|---|---|---:|
| Start incumbent | 12138 | 35.16 | 109242 | 94248 | 0 | gap 692 (`4837..5529`) | 7 / 7 | 0 |
| Stage A cyclic strict probe | 9982 | 21.81 | 89838 | 113652 | 0 | gap 0 (`4278..4278`) | 7 / 7 | 0 |
| Stage B final | 12356 | 36.51 | 111204 | 92286 | 0 | gap 567 (`5002..5569`) | 7 / 7 | 0 |
| Stage C final | 12356 | 36.51 | 111204 | 92286 | 0 | gap 567 (`5002..5569`) | 7 / 7 | 0 |

Uncovered/overcovered trend (best strict checkpoints):
- `94248/0 -> 92439/0 -> 92304/0 -> 92286/0`.

## Observations
- Symmetry front gate remains useful as a tractability test; here cyclic compression was strong but yielded an inferior strict seed versus incumbent frontier quality.
- The dominant mover was strict local exact repack (`1->2`) under hard gates, not broad `k>1` random neighborhoods.
- Strict invariants stayed fully intact throughout:
  - `overcovered_r_subsets=0`,
  - `oversubscribed_r_minus_1_subsets=0`,
  - `r_minus_1_max_degree` stayed at target (`7`).

## Reuse vs genuinely new (explicit)
- Reused from previous runs:
  - hard admissibility/divisibility gate before search,
  - symmetry-first diagnostics and bounded decision rule,
  - strict feasibility invariants,
  - reserve-first discipline and residual exact-cover eligibility gate.
- Newly learned this round:
  - For `S(8,9,21)`, symmetry is tractable but lower-yield than incumbent strict frontier for immediate coverage gain.
  - Repeated strict `1->2` local repacks can deliver substantial monotone gains (`+218` blocks) while preserving all hard constraints.
  - Current `k>1` neighborhood generation is too weak at this frontier (0 accepted improving repacks in 5000 attempts).

## Core advance
- advance statement:
  - Established a reproducible strict frontier lift for `S(8,9,21)` by coupling a mandatory symmetry gate with high-yield exact local repacks from the incumbent candidate.
- evidence from this round (metrics, runtime, structure):
  - Score improved `35.16 -> 36.51`.
  - Exact-once improved `109242 -> 111204`.
  - Uncovered reduced `94248 -> 92286` with `overcovered=0` unchanged.
  - `(r-1)` hard cap stayed tight (`7/7`) with zero oversubscription.
  - Improvement was monotone and strict (`+218` blocks, `12138 -> 12356`).
- transfer value for next rounds:
  - Keep symmetry diagnostics as mandatory Stage A, but choose seed by measured strict quality, not by tractability alone.
  - Use exact `1->2` repack lane as first post-seed augmenter on this instance.
  - Treat current generic `k>1` neighborhoods as secondary until conflict-core targeting is improved.

## Next-hypothesis
- hypothesis statement:
  - Conflict-core-guided `k>1` repacks (remove blocks around the same low-conflict 8-subset interaction graph, then solve local refill exactly) will outperform the current generic overlap-based `k>1` neighborhoods at the `12356` strict frontier.
- mechanism (why this should help):
  - Stage B gains indicate many profitable moves are very local and structured; targeting neighborhoods built from actual conflict-1/conflict-2 block interactions should raise refill quality and unlock true `k -> k+1` gains.
- expected metric movement:
  - Improve to `12380..12440` blocks,
  - reduce uncovered by `216..756`,
  - keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree<=7`.
- falsification / stop condition:
  - Stop this hypothesis if after `>=1500` conflict-core neighborhoods, net gain is `< +5` blocks or strict local refill succeeds in `<10%` of neighborhoods.
