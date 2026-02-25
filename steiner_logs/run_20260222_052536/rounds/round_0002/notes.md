# Round 2 Notes

Instance: S(6,8,29)
Expected blocks: 16965

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
- Best known metrics across all runs for this instance: score=0 run=run_20260222_043844 round=1 valid=false exact_once=0/475020 uncovered=475020 overcovered=0

## Admissibility gate snapshot
```json
{
  "checks": [
    {
      "denominator": 28,
      "i": 0,
      "numerator": 475020,
      "quotient": 16965,
      "remainder": 0
    },
    {
      "denominator": 21,
      "i": 1,
      "numerator": 98280,
      "quotient": 4680,
      "remainder": 0
    },
    {
      "denominator": 15,
      "i": 2,
      "numerator": 17550,
      "quotient": 1170,
      "remainder": 0
    },
    {
      "denominator": 10,
      "i": 3,
      "numerator": 2600,
      "quotient": 260,
      "remainder": 0
    },
    {
      "denominator": 6,
      "i": 4,
      "numerator": 300,
      "quotient": 50,
      "remainder": 0
    },
    {
      "denominator": 3,
      "i": 5,
      "numerator": 24,
      "quotient": 8,
      "remainder": 0
    }
  ],
  "divisibility_failures": [],
  "expected_block_count": 16965,
  "instance": {
    "n": 29,
    "q": 8,
    "r": 6
  },
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 16965,
    "lambda_1": 4680,
    "lambda_2": 1170,
    "lambda_3": 260,
    "lambda_4": 50,
    "lambda_5": 8
  }
}
```

## Research reuse
- Read steiner_logs/PAPER_NOTES.md, steiner_logs/RESEARCH_LOG.md, steiner_logs/PRACTICE_LOG.md, steiner_logs/RESEARCH_PAPER.md, steiner_logs/EXISTENCE_FRONTIER.md, then steiner_logs/run_20260222_052536/KNOWLEDGE_CACHE.md.
- At most 1 targeted search(es) if cache is insufficient.
- Targeted web searches used this round: `0/1`.

## Plan
- Stage A: decide engine (symmetry/orbit exact-cover vs randomized nibble pipeline).
- Stage B: reserve flex/absorber blocks up front.
- Stage C: improve via large-neighborhood repair and residual exact completion when eligible.
- Stage D: run critical-gap self-verification and revise before close.

## Proof workflow (adapted from local paper rules)
Seed directions generated before implementation:
1. Symmetry-first seed: cyclic orbit-packed strict construction, with dihedral as diagnostics comparator.
2. Strict constructive seed: reserve-first uncovered-driven nibble/boosting under hard gates `c_6<=1`, `c_5<=8`.
3. Strict LNS seed: remove `k>1` blocks near tight 5-subset motifs and attempt local `k -> k+1` refill.

Drafted best attempt this round:
- Combined seed 1 for the scaffold (`117` accepted cyclic orbits) and seed 2 for frontier growth, then used seed 3 as a bounded plateau test.

Critical-gap self-verification pass:
1. Gap A (admissibility): divisibility rechecked first; pass.
2. Gap B (engine tractability): cyclic/dihedral orbit diagnostics executed first; cyclic lane was tractable and productive, so kept as seed lane.
3. Gap C (strictness): all accepted operations preserved `overcovered=0` and `oversubscribed_(r-1)=0`.
4. Gap D (closure): residual exact completion gate checked and rejected (residual too large).

Revision after verification:
- Initial larger budgets were reduced to bounded windows due runtime pressure, then two short continuation boosts were run to keep strict gains while staying within round budget.

## Work log
- Stage A symmetry/orbit gate (mandatory first):
  - Cyclic `C29` diagnostics:
    - `|O_6|=16380`, `|O_8|=148005`,
    - sample binary/non-binary columns `1190/10` (sample size `1200`), sample `max_coeff=2`.
  - Dihedral `D29` diagnostics:
    - `|O_6|=8372`, `|O_8|=74503`,
    - sample binary/non-binary columns `1133/67` (sample size `1200`), sample `max_coeff=3`.
  - Orbit-packed strict probe:
    - accepted cyclic orbits: `117`,
    - produced strict seed `3393` blocks (`overcovered=0`, `(r-1)` oversubscription `0`).
  - Decision: symmetry lane is tractable for seeding and quality-competitive, so retained as Stage-A constructor.
- Stage B reserve-first strict boosting:
  - Reserved absorber/flex capacity early: `2036` block slots (12% of `16965`), build cap `14929`.
  - Uncovered-driven strict nibble/boosting raised:
    - `3393 -> 3973` blocks in main pass (`accepted_nibble=580`),
    - `3973 -> 4288` in continuation pass 1 (`+314`),
    - `4288 -> 4402` in continuation pass 2 (`+114`).
  - Strict invariants preserved throughout.
- Stage C strict LNS (`k>1`) destroy/repack:
  - Main LNS window: `700` iterations, `1` accepted neighborhood.
  - Net movement from Stage-B frontier: `3973 -> 3974` (local gain exists but sparse).
  - Continuation LNS net gain from `4288` frontier: `0`.
- Stage D residual exact completion gate:
  - Not eligible; residual uncovered fraction remains too large.
  - Gate reason: `not eligible: uncovered fraction is too large; use constructive search first`.

## Metric trend
| Checkpoint | Blocks | Score | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Oversubscribed `(r-1)` |
|---|---:|---:|---:|---:|---:|---|---|---:|
| Baseline | 0 | 0.00 | 0 | 475020 | 0 | gap 0 (`0..0`) | 0 / 8 | 0 |
| Stage A symmetry seed | 3393 | 0.00 | 95004 | 380016 | 0 | gap 0 (`936..936`) | 5 / 8 | 0 |
| Stage B main | 3973 | 0.00 | 111244 | 363776 | 0 | gap 24 (`1084..1108`) | 6 / 8 | 0 |
| Stage C main LNS | 3974 | 0.00 | 111272 | 363748 | 0 | gap 24 (`1084..1108`) | 6 / 8 | 0 |
| Final (after continuations) | 4402 | 0.00 | 123256 | 351764 | 0 | gap 31 (`1200..1231`) | 6 / 8 | 0 |

Uncovered/overcovered trend (best checkpoints):
- `475020/0 -> 380016/0 -> 363776/0 -> 363748/0 -> 351764/0`.

## Observations
- Symmetry-first gate materially helped this instance: cyclic orbit seeding gave a large strict scaffold quickly (`3393` blocks) while dihedral diagnostics showed higher non-binary pressure.
- At the current frontier, strict add-only boosting still dominates strict LNS in gain-per-runtime.
- Hard feasibility remained strong:
  - `overcovered=0` at every checkpoint,
  - `oversubscribed_r_minus_1_subsets=0` at every checkpoint,
  - `r_minus_1_max_degree=6 <= 8` (headroom remained).
- Residual exact-cover remains structurally premature for this residual size.

## Reuse vs genuinely new (explicit)
- Reused from previous runs:
  - mandatory admissibility gate before search,
  - bounded symmetry-front diagnostics and reversible engine switch,
  - reserve-first strict construction discipline (`c_6<=1`, `c_5<=8`),
  - `k>1` LNS as a post-boost lane.
- Newly learned this round:
  - For `S(6,8,29)`, cyclic orbit-packing is immediately productive as a strict seed (`117` orbits -> `3393` blocks).
  - Dihedral compression is stronger in dimension but noisier in coefficients (higher non-binary share), so cyclic is the better primary symmetry lane here.
  - At this frontier, incremental strict gains are coming from uncovered-driven add-only continuation, not from short LNS windows.

## Core advance
- advance statement:
  - Established a strict symmetry-seeded construction path for `S(6,8,29)` and moved the instance from empty start to a reusable strict frontier (`4402` blocks) with zero collisions.
- evidence from this round (metrics, runtime, structure):
  - Stage A symmetry was executed first and accepted as tractable (`C29` sample non-binary share `0.83%`, `max_coeff=2`; `117` accepted cyclic orbits).
  - Stage B + continuations improved strict frontier `3393 -> 4402` while keeping `overcovered=0` and `(r-1)` oversubscription `0`.
  - Verifier movement: `exact_once 0 -> 123256`, `uncovered 475020 -> 351764`, `overcovered 0 -> 0`.
  - Stage C LNS was explicitly tested (`k>1`) but delivered sparse net gains at this frontier.
- transfer value for next rounds:
  - Keep cyclic orbit-packed seeding as default Stage A on this instance.
  - Keep strict uncovered-driven add-only continuation as the primary mover after symmetry seed.
  - Treat short-window LNS as secondary diversification unless acceptance can be improved.

## Next-hypothesis
- hypothesis statement:
  - For `S(6,8,29)`, a two-phase strict policy (`cyclic orbit seed -> long uncovered-driven add-only continuation`) will outperform short-window strict LNS in uncovered reduction under matched compute budgets.
- mechanism (why this should help):
  - The current candidate still has substantial strict slack (`r_minus_1_max_degree=6 < 8`), so strict additions can continue to harvest uncovered 6-subsets efficiently.
  - Short LNS windows are currently opening little additional local slack relative to their search cost.
- expected metric movement:
  - Improve `4402 -> 5000..5800` blocks.
  - Reduce uncovered by `16800..39200`.
  - Keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 8`.
- falsification / stop condition:
  - Reject this hypothesis if two matched continuation runs (`>=250k` attempts each) both produce `< +150` net blocks, or if strict invariants are violated in any accepted move.
