# Round 3 Notes

Instance: S(7,8,24)
Expected blocks: 43263

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
- Best known metrics across all runs for this instance before this round: none

## Admissibility gate snapshot
```json
{
  "checks": [
    {
      "denominator": 8,
      "i": 0,
      "numerator": 346104,
      "quotient": 43263,
      "remainder": 0
    },
    {
      "denominator": 7,
      "i": 1,
      "numerator": 100947,
      "quotient": 14421,
      "remainder": 0
    },
    {
      "denominator": 6,
      "i": 2,
      "numerator": 26334,
      "quotient": 4389,
      "remainder": 0
    },
    {
      "denominator": 5,
      "i": 3,
      "numerator": 5985,
      "quotient": 1197,
      "remainder": 0
    },
    {
      "denominator": 4,
      "i": 4,
      "numerator": 1140,
      "quotient": 285,
      "remainder": 0
    },
    {
      "denominator": 3,
      "i": 5,
      "numerator": 171,
      "quotient": 57,
      "remainder": 0
    },
    {
      "denominator": 2,
      "i": 6,
      "numerator": 18,
      "quotient": 9,
      "remainder": 0
    }
  ],
  "divisibility_failures": [],
  "expected_block_count": 43263,
  "instance": {
    "n": 24,
    "q": 8,
    "r": 7
  },
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 43263,
    "lambda_1": 14421,
    "lambda_2": 4389,
    "lambda_3": 1197,
    "lambda_4": 285,
    "lambda_5": 57,
    "lambda_6": 9
  }
}
```

## Research reuse
- Read steiner_logs/PAPER_NOTES.md, steiner_logs/RESEARCH_LOG.md, steiner_logs/PRACTICE_LOG.md, steiner_logs/RESEARCH_PAPER.md, steiner_logs/EXISTENCE_FRONTIER.md, then steiner_logs/run_20260222_052536/KNOWLEDGE_CACHE.md.
- Targeted web searches used this round: `0/1`.
- Local-paper-first policy kept; no new external sources added.

## Plan
- Stage A: symmetry/orbit front gate first (cyclic and dihedral diagnostics), then orbit-packed seed if tractable.
- Stage B: reserve absorber/flex capacity early and run strict add-only boosting under hard caps.
- Stage C: run strict LNS destroy/repack (`k>1`, `k -> k+1`) rather than only 1-for-1 swaps.
- Stage D: run residual exact-completion eligibility gate and attempt only if eligible.

## Proof workflow (adapted from local paper rules)
Seed directions generated before implementation:
1. Symmetry-first seed: cyclic orbit-packed strict scaffold with dihedral diagnostics as comparator.
2. Strict constructive seed: reserve-first add-only growth under hard gates `c_7<=1` and `c_6<=9`.
3. Strict LNS seed: remove `k>1` blocks and refill with local `k -> k+1` repacks around released motifs.

Drafted best attempt this round:
- Used seed 1 to build a balanced cyclic scaffold, seed 2 for large strict coverage gains, then seed 3 to push post-boost frontier improvements.

Critical-gap self-verification pass:
1. Gap A (admissibility): divisibility rechecked first; pass.
2. Gap B (engine feasibility): symmetry diagnostics showed strong compression and large orbit sizes; symmetry lane kept.
3. Gap C (strictness): accepted moves preserved `overcovered=0` and `oversubscribed_(r-1)=0`.
4. Gap D (closure): residual exact completion gate checked; ineligible due large uncovered fraction.

Revision after verification:
- First LNS implementation had a bookkeeping bug in temporary neighborhood handling; rerun with rollback-safe updates produced stable strict gains (`+24` blocks over Stage B).

## Work log
- Stage A symmetry/orbit gate (executed first, mandatory):
  - Exact orbit counts from Burnside diagnostics:
    - cyclic: `|O_7|=14421`, `|O_8|=30667`
    - dihedral: `|O_7|=7293`, `|O_8|=15581`
  - Sample orbit-size diagnostics (500 random blocks):
    - cyclic avg/min/max: `23.976 / 12 / 24`
    - dihedral avg/min/max: `47.712 / 24 / 48`
  - Orbit-packed strict probe accepted `828` cyclic orbits (`19848` blocks).
  - Decision: symmetry is tractable and strong, so cyclic lane used as primary seed.
- Stage B reserve-first strict boosting:
  - Reserved absorber/flex capacity up front: `5192` slots (12% of expected), build cap `38071`.
  - Strict add-only boosting attempts: `4,000,000`; accepted `1208`.
  - Movement: `19848 -> 21056` blocks.
- Stage C strict LNS destroy/repack (`k>1`, local `k -> k+1`):
  - Iterations: `6000`; local proposal budget: `3000` per neighborhood.
  - Accepted improving repacks: `24`; net gain: `+24` blocks.
  - Movement: `21056 -> 21080` blocks.
- Stage D residual exact completion gate:
  - Strict gates pass (`overcovered=0`, no `(r-1)` oversubscription), but residual gate ineligible.
  - Gate reason: `not eligible: uncovered fraction is too large; use constructive search first`.

## Metric trend
| Checkpoint | Blocks | Score | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Oversubscribed `(r-1)` |
|---|---:|---:|---:|---:|---:|---|---|---:|
| Baseline | 0 | 0.00 | 0 | 346104 | 0 | gap 0 (`0..0`) | 0 / 9 | 0 |
| Stage A cyclic seed | 19848 | 24.23 | 158784 | 187320 | 0 | gap 0 (`6616..6616`) | 8 / 9 | 0 |
| Stage B final | 21056 | 28.14 | 168448 | 177656 | 0 | gap 13 (`7013..7026`) | 8 / 9 | 0 |
| Stage C iter 1000 | 21059 | 28.15 | 168472 | 177632 | 0 | gap 16 (`7013..7029`) | 8 / 9 | 0 |
| Stage C iter 3000 | 21071 | 28.19 | 168568 | 177536 | 0 | gap 18 (`7017..7035`) | 8 / 9 | 0 |
| Stage C iter 6000 (final) | 21080 | 28.22 | 168640 | 177464 | 0 | gap 20 (`7019..7039`) | 8 / 9 | 0 |

Uncovered/overcovered trend (best checkpoints):
- `346104/0 -> 187320/0 -> 177656/0 -> 177632/0 -> 177536/0 -> 177464/0`.

## Observations
- Symmetry-first gate was decisive: cyclic orbit packing produced a large strict scaffold immediately and kept point degrees perfectly flat at seed stage.
- Strict add-only remained the dominant mover for coarse gains, while LNS delivered smaller but real monotone gains after add-only slowed.
- Hard invariants remained strict at all checkpoints:
  - `overcovered_r_subsets=0`,
  - `oversubscribed_r_minus_1_subsets=0`,
  - `r_minus_1_max_degree=8 <= 9`.
- Residual exact closure is still structurally premature (`177464 / 346104 = 0.5127` uncovered fraction).

## Reuse vs genuinely new (explicit)
- Reused from previous runs:
  - hard admissibility gate before search,
  - symmetry-first bounded engine selection,
  - strict feasibility invariants (`overcovered=0`, no `(r-1)` oversubscription),
  - LNS `k>1` destroy/repack as post-boost augmenter,
  - residual exact-cover only behind eligibility gate.
- Newly learned this round:
  - For `S(7,8,24)`, cyclic symmetry is not only diagnostic; it yields a very strong strict seed (`19848` blocks).
  - This instance has meaningful strict headroom under `c_6<=9` after symmetry seeding (`r_minus_1_max_degree` stayed at `8`).
  - Bounded strict LNS can continue improving after add-only slowdown, but gains are sparse and need focused neighborhoods.

## Core advance
- advance statement:
  - Established the first strong strict-feasible certificate frontier for `S(7,8,24)` in this repo using a symmetry-seeded + strict-LNS pipeline.
- evidence from this round (metrics, runtime, structure):
  - Candidate improved from empty to `21080` strict-feasible blocks.
  - Verifier moved to `score=28.22`, `exact_once=168640/346104`, `uncovered=177464`, while preserving `overcovered=0` and zero `(r-1)` oversubscription.
  - Mandatory architecture was executed in full order: symmetry gate -> reserve-first boosting -> LNS repack -> residual gate.
- transfer value for next rounds:
  - Reuse cyclic orbit seed generation as default Stage A for this instance.
  - Keep strict add-only as the first post-seed mover, then handoff to focused LNS around released motifs.
  - Continue deferring residual exact cover until uncovered fraction is much smaller.

## Next-hypothesis
- hypothesis statement:
  - On this frontier, hotspot-guided medium-window strict repacks (`k=4..10`) targeted at near-cap 6-subsets will outperform current mixed local/global LNS neighborhoods.
- mechanism (why this should help):
  - Current LNS acceptance is low because neighborhoods are broad and weakly coupled to pressure motifs.
  - Centering destroy/repack windows on high-load 6-subsets should expose more feasible `k -> k+1` opportunities while preserving strict gates.
- expected metric movement:
  - Improve `21080 -> 21250..21650` blocks.
  - Reduce uncovered by `1360..4560`.
  - Keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 9`.
- falsification / stop condition:
  - Reject this hypothesis if after `>=8000` hotspot-guided neighborhoods:
  - net gain is `< +60` blocks, or
  - strict invariants are violated in any accepted move.
