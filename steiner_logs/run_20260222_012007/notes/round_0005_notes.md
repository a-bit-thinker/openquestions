# Round 5 Notes

Instance: S(9,10,22)
Expected blocks: 49742

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
- Best known metrics across all runs for this instance: score=26.85 run=run_20260222_012007 round=5 valid=false exact_once=237520/497420 uncovered=259900 overcovered=0

## Admissibility gate snapshot
```json
{
  "checks": [
    {
      "denominator": 10,
      "i": 0,
      "numerator": 497420,
      "quotient": 49742,
      "remainder": 0
    },
    {
      "denominator": 9,
      "i": 1,
      "numerator": 203490,
      "quotient": 22610,
      "remainder": 0
    },
    {
      "denominator": 8,
      "i": 2,
      "numerator": 77520,
      "quotient": 9690,
      "remainder": 0
    },
    {
      "denominator": 7,
      "i": 3,
      "numerator": 27132,
      "quotient": 3876,
      "remainder": 0
    },
    {
      "denominator": 6,
      "i": 4,
      "numerator": 8568,
      "quotient": 1428,
      "remainder": 0
    },
    {
      "denominator": 5,
      "i": 5,
      "numerator": 2380,
      "quotient": 476,
      "remainder": 0
    },
    {
      "denominator": 4,
      "i": 6,
      "numerator": 560,
      "quotient": 140,
      "remainder": 0
    },
    {
      "denominator": 3,
      "i": 7,
      "numerator": 105,
      "quotient": 35,
      "remainder": 0
    },
    {
      "denominator": 2,
      "i": 8,
      "numerator": 14,
      "quotient": 7,
      "remainder": 0
    }
  ],
  "divisibility_failures": [],
  "expected_block_count": 49742,
  "instance": {
    "n": 22,
    "q": 10,
    "r": 9
  },
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 49742,
    "lambda_1": 22610,
    "lambda_2": 9690,
    "lambda_3": 3876,
    "lambda_4": 1428,
    "lambda_5": 476,
    "lambda_6": 140,
    "lambda_7": 35,
    "lambda_8": 7
  }
}
```

## Research reuse
- Read steiner_logs/PAPER_NOTES.md, steiner_logs/RESEARCH_LOG.md, steiner_logs/PRACTICE_LOG.md, steiner_logs/EXISTENCE_FRONTIER.md, then steiner_logs/run_20260222_012007/KNOWLEDGE_CACHE.md.
- At most 1 targeted search(es) if cache is insufficient.

## Plan
- Stage A: execute symmetry/orbit diagnostics first and keep symmetry lane if quality is competitive.
- Stage B: reserve absorber/flex capacity early, then run strict add-only boosting from the chosen seed.
- Stage C: run strict LNS destroy/repack (`k>1`) with local `k -> k+1` refill attempts.
- Stage D: run residual exact-completion gate check and critical-gap self-verification before finalizing.

## Proof workflow (adapted from local paper rules)
Seed directions generated before implementation:
1. Symmetry-first seed: cyclic/dihedral orbit compression with binary-first orbit packing.
2. Strict constructive seed: reserve-first add-only growth under hard caps `c_9 <= 1` and `c_8 <= 7`.
3. Strict LNS seed: remove `k>1` blocks near tight motifs and refill with local exact `k -> k+1` repacks.

Drafted best attempt this round:
- Combined seed 1 for the initial scaffold and seeds 2-3 for post-scaffold improvements.

Critical-gap self-verification pass:
1. Gap A (admissibility): rechecked divisibility; pass.
2. Gap B (engine feasibility): symmetry diagnostics + bounded cyclic packed probe executed first; tractable and high quality, so symmetry lane kept.
3. Gap C (repair correctness): every accepted add/repack preserved `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 7`.
4. Gap D (closure): residual exact completion gate checked; ineligible because uncovered residual is still too large.

Revision after verification:
- Tightened Stage C to strict `k -> k+1` local repacks around released rows from removed blocks; this gave additional net gains after Stage B.

## Work log
- Stage A symmetry/orbit gate (executed first, mandatory):
  - `C22`: `|O_9|=22610`, `|O_10|=29414`, binary/non-binary columns `29366/48`, `max_coeff=2`.
  - `D22`: `|O_9|=11410`, `|O_10|=14938`, binary/non-binary columns `14460/478`, `max_coeff=4`.
  - Bounded cyclic orbit-packed probe (binary row-orbit proxy expanded to full cyclic orbits):
    - `23716` blocks, `score=26.75`, `exact_once=237160`, `uncovered=260260`, `overcovered=0`.
  - Decision: symmetry is tractable and quality-competitive for this instance, so it is used as the primary seed (no fallback to random-first baseline).
- Stage B reserve-first strict boosting:
  - Reserved absorber/flex budget early (`5969` slots, 12% of expected size); this reserve was non-binding at the current strict frontier.
  - Strict add-only scan from symmetry seed with hard gates `c_9<=1`, `c_8<=7`: accepted `22/500000` attempts.
  - Movement: `23716 -> 23738` blocks, `score 26.75 -> 26.81`, `uncovered 260260 -> 260040`, `overcovered=0`.
- Stage C strict LNS destroy/repack (`k=2..7`, local `k -> k+1`):
  - Iterations: `5000`; accepted improving repacks: `14`.
  - Net movement from Stage B: `23738 -> 23752` blocks.
  - Checkpoints:
    - `iter 1000`: `23745` blocks, `score=26.83`, `uncovered=259970`.
    - `iter 2000`: `23747` blocks, `score=26.84`, `uncovered=259950`.
    - `iter 3000`: `23749` blocks, `score=26.84`, `uncovered=259930`.
    - `iter 4000`: `23752` blocks, `score=26.85`, `uncovered=259900`.
    - `iter 5000`: unchanged best.
- Stage D residual exact completion gate:
  - `overcovered=0` and `(r-1)` strict gates pass, but residual gate is ineligible:
  - uncovered fraction `259900 / 497420 = 0.5225` is too large for residual exact cover.

## Metric trend
| Checkpoint | Blocks | Score | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Oversubscribed `(r-1)` |
|---|---:|---:|---:|---:|---:|---|---|---:|
| Stage A cyclic probe | 23716 | 26.75 | 237160 | 260260 | 0 | gap 0 (`10780..10780`) | 7 / 7 | 0 |
| Stage B strict add-only | 23738 | 26.81 | 237380 | 260040 | 0 | gap 5 (`10788..10793`) | 7 / 7 | 0 |
| Stage C final | 23752 | 26.85 | 237520 | 259900 | 0 | gap 6 (`10793..10799`) | 7 / 7 | 0 |

Uncovered/overcovered trend (best checkpoints):
- `260260/0 -> 260040/0 -> 259900/0`.

## Observations
- Strict admissibility was preserved as a hard pre-search gate and remained satisfied throughout.
- In contrast to recent `r=8,9` rounds where symmetry was mostly diagnostic, this instance had a tractable cyclic lane that produced a strong strict-feasible seed immediately.
- The strict scaffold stayed structurally balanced:
  - `r_minus_1_max_degree` remained exactly at target (`7`),
  - `oversubscribed_r_minus_1_subsets` stayed `0`,
  - point-degree spread remained very small (`<=9` during checkpoints).
- Post-seed gains are sparse but real: strict LNS delivered incremental monotone improvements after add-only acceptance became rare.
- No new web sources were needed (`0/1` targeted searches used).

## Reuse vs genuinely new (explicit)
- Reused from previous runs:
  - hard admissibility gate before any search,
  - symmetry-first engine selection discipline,
  - strict feasibility invariants (`overcovered=0`, no `(r-1)` oversubscription),
  - LNS `k>1` destroy/repack as the main late-stage mover.
- Newly learned this round:
  - For `S(9,10,22)`, cyclic symmetry is not just diagnostic; it yields a high-quality strict seed (`score=26.75`) in bounded budget.
  - A strict symmetry seed plus strict LNS outperforms random strict construction from empty starts in this environment.
  - Point-degree balancing becomes an automatic side effect of the cyclic scaffold, reducing the need for separate neutral rebalance passes.

## Core advance
- advance statement:
  - Established a symmetry-led strict construction path for `S(9,10,22)` that reaches a strong no-collision frontier and then improves it with strict `k -> k+1` LNS repacks.
- evidence from this round (metrics, runtime, structure):
  - Stage A symmetry diagnostics were executed first and passed tractability checks (`C22` non-binary columns only `48/29414`).
  - Cyclic orbit-packed seed immediately produced `23716` strict-feasible blocks with `score=26.75`, `overcovered=0`, `oversubscribed_(r-1)=0`.
  - Stage B strict add-only raised this to `23738` (`score=26.81`).
  - Stage C strict LNS raised to `23752` (`score=26.85`, `exact_once=237520`, `uncovered=259900`) while preserving all hard invariants.
- transfer value for next rounds:
  - Use cyclic orbit-packed strict seed as default starting point for this instance, not empty/random starts.
  - Keep strict LNS windows as the post-seed augmenter; gains are sparse but stable.
  - Preserve strict cap gates (`c_9<=1`, `c_8<=7`) as first-line invariants for this instance.

## Next-hypothesis
- hypothesis statement:
  - Medium-window strict local exact repacks (`k=4..10`) centered on cap-7 `8`-subset tails will outperform the current small-window strict LNS at this frontier.
- mechanism (why this should help):
  - Current accepted moves are sparse because small windows expose too little combinational slack.
  - Releasing slightly larger coupled neighborhoods around tight `8`-faces should expose additional strict `k -> k+1` augment opportunities while keeping `overcovered=0`.
- expected metric movement:
  - Improve `23752 -> 23810..23960` blocks.
  - Reduce uncovered by `580..2080`.
  - Keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 7`.
- falsification / stop condition:
  - Reject this hypothesis if after `>=8000` medium-window trials:
  - net block gain is `< +20`, or
  - gain-per-1000 trials is not better than the current small-window baseline.

## Rounds 1-5 Synthesis
### Practice trajectory (Rounds 2-5)
- Round 2 (`S(6,7,23)`): strict LNS progression from `9237 -> 9280` validated reserve-first destroy/repack under hard gates.
- Round 3 (`S(7,8,20)`): motif-coupled strict LNS scaled to larger gains (`5634 -> 5807`) with strict `(r-1)` control.
- Round 4 (`S(8,9,21)`): add-only exhaustion was confirmed early; sparse strict LNS gains remained the only improving lane (`12107 -> 12138`).
- Round 5 (`S(9,10,22)`): symmetry lane became tractable and strong; strict symmetry seed + strict LNS reached `23752` with `overcovered=0`.

### Connection back to Round 1 research priorities
- Round 1 prioritized: hard admissibility gate, bounded symmetry triage, then staged constructive repair.
- Rounds 2-5 outcomes confirm the policy:
  - admissibility stayed a necessary gate,
  - engine selection had to remain empirical by instance,
  - strict repair layers were the persistent improvement engine after initial seeding.
- Round 5 specifically refines the selector: for this instance, keep symmetry as the default seed generator rather than a quick reject-only probe.

### Strongest advances by round
1. Round 1: formalized the dual-engine + strict-gate solve contract with explicit verification loops.
2. Round 2: proved strict reserve-aware LNS can move a large admissible instance frontier.
3. Round 3: validated scalable strict motif-coupled repacks for `r=7`.
4. Round 4: confirmed sparse-gain high-`r` behavior and preserved hard invariants under pressure.
5. Round 5: converted symmetry from diagnostic to productive seed lane for `S(9,10,22)`, then added strict LNS gains.

### Failed directions and why they failed
1. Dihedral-heavy continuation:
Reason: higher non-binary inflation (`478` non-binary columns, `max_coeff=4`) reduced binary-orbit tractability compared with cyclic.
2. Empty-start random strict construction:
Reason: lower score frontier in bounded budget than symmetry-seeded strict construction.
3. Residual exact completion attempt:
Reason: uncovered residual (`259900`) is far above eligibility threshold; exact residual lane is structurally premature.

### Top 3 next hypotheses with test protocol for round 6
1. Hypothesis: strict medium-window repacks (`k=4..10`) beat small-window strict repacks.
Test protocol: run `3` seeds with `>=8000` windows each; compare net blocks and uncovered reduction against current `k<=7` baseline.
2. Hypothesis: mixed neighborhood sources improve strict hit rate.
Test protocol: A/B/C ratios for proposal sources `{impacted-row, random-uncovered, random-global}` as `{70/20/10, 50/30/20, 35/45/20}` over matched trial budgets.
3. Hypothesis: two-step coupled repacks on the same released motif increase second-step success.
Test protocol: compare coupled vs uncoupled scheduling for matched `>=3000` accepted first-step opportunities; measure second-step success and net block gain.
