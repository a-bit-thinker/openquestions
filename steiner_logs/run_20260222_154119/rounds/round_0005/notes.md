# Round 5 Notes

Instance: S(9,10,26)
Expected blocks: 312455

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: steiner_logs/run_20260222_154119/REPO_WIDE_HISTORY.md
- Global research log (all runs round1): steiner_logs/RESEARCH_LOG.md
- Global practice log (all runs round2-5): steiner_logs/PRACTICE_LOG.md
- Local paper notes: steiner_logs/PAPER_NOTES.md
- Latest prior run: run_20260222_052536
- Latest prior round1 notes: steiner_logs/run_20260222_052536/notes/round_0001_notes.md
- Latest prior round5 notes: steiner_logs/run_20260222_052536/notes/round_0005_notes.md
- Latest prior transfer: steiner_logs/run_20260222_052536/NEXT_GENERATION_TRANSFER.md

## Admissibility gate snapshot
```json
{
  "checks": [
    {
      "denominator": 10,
      "i": 0,
      "numerator": 3124550,
      "quotient": 312455,
      "remainder": 0
    },
    {
      "denominator": 9,
      "i": 1,
      "numerator": 1081575,
      "quotient": 120175,
      "remainder": 0
    },
    {
      "denominator": 8,
      "i": 2,
      "numerator": 346104,
      "quotient": 43263,
      "remainder": 0
    },
    {
      "denominator": 7,
      "i": 3,
      "numerator": 100947,
      "quotient": 14421,
      "remainder": 0
    },
    {
      "denominator": 6,
      "i": 4,
      "numerator": 26334,
      "quotient": 4389,
      "remainder": 0
    },
    {
      "denominator": 5,
      "i": 5,
      "numerator": 5985,
      "quotient": 1197,
      "remainder": 0
    },
    {
      "denominator": 4,
      "i": 6,
      "numerator": 1140,
      "quotient": 285,
      "remainder": 0
    },
    {
      "denominator": 3,
      "i": 7,
      "numerator": 171,
      "quotient": 57,
      "remainder": 0
    },
    {
      "denominator": 2,
      "i": 8,
      "numerator": 18,
      "quotient": 9,
      "remainder": 0
    }
  ],
  "divisibility_failures": [],
  "expected_block_count": 312455,
  "instance": {
    "n": 26,
    "q": 10,
    "r": 9
  },
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 312455,
    "lambda_1": 120175,
    "lambda_2": 43263,
    "lambda_3": 14421,
    "lambda_4": 4389,
    "lambda_5": 1197,
    "lambda_6": 285,
    "lambda_7": 57,
    "lambda_8": 9
  }
}
```

## Research reuse
- Re-read cache before solve stage: `steiner_logs/run_20260222_154119/KNOWLEDGE_CACHE.md`.
- Reused cached local-paper and cross-run strategy only; no new web search executed in this round (`0/1` targeted searches used).
- Reused strict invariants from prior rounds: hard admissibility gate, strict `overcovered=0`, strict `(r-1)` oversubscription `=0`, residual exact-cover late gate only.

## Plan
- Stage A: symmetry/orbit compression first (cyclic and dihedral diagnostics), then bounded cyclic full-orbit strict probe.
- Stage B: reserve absorber/flex capacity early (`12%` reserve, build cap `274960`) before generalized growth.
- Stage C: general strict pipeline (`nibble/boosting` then `k>1` LNS remove/refill repacks).
- Stage D: exact residual completion only if residual is small with no overcoverage.

## Proof workflow (adapted from local paper rules)
Seed proof directions generated before implementation:
1. Symmetry-orbit direction: use cyclic orbit packing if diagnostics show near-binary behavior.
2. Reserve-first constructive direction: preserve future absorber/flex headroom and avoid greedy cap saturation.
3. LNS direction: use `k>1` remove/refill around pressure motifs, not only `1-for-1` swaps.

Drafted best attempt:
- Run full architecture in order from empty start: admissibility gate -> symmetry probe -> reserve-first nibble -> `k>1` LNS -> post-LNS revision sweep.

Critical-gap self-verification pass:
1. Gap A (admissibility): divisibility checks re-run before any search; pass.
2. Gap B (engine choice): cyclic diagnostics were clean and bounded full-orbit probe had high strict acceptance, so symmetry was used as primary Stage A.
3. Gap C (repair correctness): every accepted move preserved strict feasibility (`overcovered=0`, `oversubscribed_(r-1)=0`).
4. Gap D (closure): residual exact completion remained ineligible because uncovered fraction stayed high.

Revision after verification:
- After Stage B, add-only acceptance decayed; inserted explicit `k>1` LNS wave (700 neighborhoods), then reran a post-LNS add-only revision sweep.

## Work log
- Stage A symmetry diagnostics:
  - cyclic sampled non-binary share `0.0`, sampled max coeff `1`, sampled orbit size `26`.
  - dihedral sampled non-binary share `0.00293`, sampled max coeff `2`, sampled orbit size `52`.
  - decision: keep cyclic symmetry lane as tractable and productive.
- Stage A cyclic full-orbit strict probe/continuation:
  - trials: `2200`.
  - accepted full orbits: `1246`.
  - movement: `0 -> 32383` blocks.
- Stage B reserve-first nibble/boosting:
  - reserve: `37495` blocks (12%); build cap `274960` (non-binding).
  - attempts: `4,200,000`.
  - accepted strict adds: `87590`.
  - movement: `32383 -> 119973` blocks.
- Stage C `k>1` LNS repair:
  - neighborhoods: `700`.
  - positive neighborhoods: `692`.
  - neutral accepted neighborhoods: `2`.
  - net gain: `+692`.
  - movement: `119973 -> 120665` blocks.
- Stage D post-LNS add-only revision:
  - attempts: `1,200,000`.
  - accepted strict adds: `3060`.
  - movement: `120665 -> 123725` blocks.
- Stage E residual exact gate:
  - not attempted; ineligible (`uncovered=1887300`, uncovered fraction `0.6040`, `overcovered=0`).

## Metric trend
| Checkpoint | Blocks | Score | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Oversubscribed `(r-1)` |
|---|---:|---:|---:|---:|---:|---|---|---:|
| Baseline | 0 | 0.00 | 0 | 3124550 | 0 | gap 0 (`0..0`) | 0 / 9 | 0 |
| Stage A final | 32383 | 0.00 | 323830 | 2800720 | 0 | gap 0 (`12455..12455`) | 6 / 9 | 0 |
| Stage B final | 119973 | 13.76 | 1199730 | 1924820 | 0 | gap 165 (`46061..46226`) | 9 / 9 | 0 |
| Stage C final | 120665 | 14.07 | 1206650 | 1917900 | 0 | gap 159 (`46334..46493`) | 8 / 9 | 0 |
| Final | 123725 | 15.44 | 1237250 | 1887300 | 0 | gap 183 (`47518..47701`) | 9 / 9 | 0 |

Uncovered/overcovered trend:
- `3124550/0 -> 2800720/0 -> 1924820/0 -> 1917900/0 -> 1887300/0`.

## Observations
- Symmetry-orbit compression is tractable and high-yield on this instance; cyclic full-orbit packing produced the first `32383` strict blocks with perfectly balanced point degrees.
- Strict constructive growth remains strong even after cap contact at `(r-1)=9/9`; overcoverage did not appear.
- `k>1` LNS repacks were not just compliance steps: they produced measurable strict net gain (`+692`) before the final revision sweep.
- Residual exact completion is still structurally premature at this frontier.

## Reuse vs genuinely new (explicit)
- Reused from previous runs:
  - hard admissibility gate as strict front gate,
  - symmetry-first selector,
  - reserve-first discipline,
  - strict feasibility invariants,
  - residual late-gate rule.
- Newly learned this round:
  - `S(9,10,26)` supports a productive cyclic full-orbit strict seed (`1246/2200` accepted orbits).
  - Score crosses from `0.00` to `15.44` once strict block count passes ~`100k`; this makes this instance practically optimizable under strict gates.
  - Mixed schedule (`nibble` + `k>1` LNS + revision sweep) keeps strict gains available after initial cap contact.

## Core advance
- advance statement:
  - Established the first strict-feasible frontier for `S(9,10,26)` in this repository by moving from empty candidate to `123725` blocks while preserving `overcovered=0` and zero `(r-1)` oversubscription.
- evidence from this round (metrics, runtime, structure):
  - Score improved `0.00 -> 15.44`.
  - Exact-once improved `0 -> 1237250`.
  - Uncovered reduced `3124550 -> 1887300`.
  - `(r-1)` cap discipline held (`max 9`, target `9`, oversubscribed count `0`).
  - Required architecture was followed in order: symmetry gate first, reserve set early, `k>1` LNS executed, residual gate checked and deferred.
- transfer value for next rounds:
  - Keep cyclic orbit seeding as default Stage A on this exact instance.
  - Continue mixed strict schedule after Stage B; add-only alone leaves recoverable gains.
  - Preserve strict feasibility artifacts as the transferable baseline for round 6.

## Next-hypothesis
- hypothesis statement:
  - A four-phase strict loop (`short cyclic orbit micro-burst -> uncovered-driven add-only -> motif-coupled mixed-window LNS (k=3..7) -> short revision sweep`) will outperform the current fixed-budget schedule from `123725`.
- mechanism (why this should help):
  - orbit micro-bursts refresh global balance; add-only captures easy uncovered mass; larger-window repacks release local cap bottlenecks that small windows miss; revision sweep harvests reopened slack.
- expected metric movement:
  - Improve `123725 -> 127000..134000` blocks.
  - Reduce uncovered by `32750..102750`.
  - Keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 9`.
- falsification / stop condition:
  - Reject if after `>=2.0M` extra add attempts and `>=1200` mixed-window LNS neighborhoods net gain is `< +1500` blocks, or if gain-per-1000 neighborhoods is not above this round's Stage C baseline.

## Rounds 1-5 Synthesis
### Practice trajectory (rounds 2-5)
- Round 2 (`S(6,7,23)`): strict frontier improved `9280 -> 9287` with neutral-then-positive LNS and strict invariants preserved.
- Round 3 (`S(7,8,24)`): strict frontier improved `21080 -> 21090`; symmetry became a short gate, then general strict repair dominated.
- Round 4 (`S(8,9,25)`): symmetry became primary engine again and produced a large strict frontier (`0 -> 55234`).
- Round 5 (`S(9,10,26)`): same architecture scaled to a new instance and produced `0 -> 123725` strict blocks.

### Connection back to round1 priorities
- Round1 mandated: admissibility-first, symmetry triage first, reserve-first construction, strict feasibility, residual late gate.
- Rounds 2-5 confirm that this contract is operationally correct: engine choice is instance-specific, strict gates do not block progress, and residual exact-cover remains a late-stage only tool.

### Strongest advances by round
- Round 1: converted process into a gate-explicit proof workflow with critical-gap verification loops.
- Round 2: proved neutral `k->k` repacks can unlock later positive gains under strict gates.
- Round 3: confirmed plateau behavior at cap and need for coupled neighborhoods.
- Round 4: identified a symmetry-tractable frontier where full-orbit packing is a high-yield primary engine.
- Round 5: achieved first high-mass strict candidate for `S(9,10,26)` with positive score and clean strict invariants.

### Failed directions and why they failed
- Early residual exact completion failed repeatedly because uncovered fraction remained far above eligibility thresholds.
- Single-phase continuation (add-only only, or repack-only only) underperformed mixed schedules.
- Treating symmetry as always-primary failed on some prior instances with high non-binary inflation; bounded diagnostics are required before commitment.

### Top 3 next hypotheses for round 6 (with test protocol)
1. Mixed four-phase strict loop beats current schedule on net gain.
Test protocol: run two equal-budget arms from `123725` (`current schedule` vs `four-phase`) and compare net blocks and uncovered reduction.
2. Larger-window repacks (`k=5..9`) around cap-9 8-subset motifs improve gain-per-time over `k<=4`.
Test protocol: matched 1000-neighborhood ablation (`small-window` vs `mixed-window`) with identical strict gates.
3. Degree-balance neutral passes before positive LNS increase later accept rates.
Test protocol: matched-budget A/B from same seed (`direct positive LNS` vs `neutral-balance then positive`) and compare accepted adds in the following 500k-attempt revision sweep.
