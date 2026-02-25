# Round 3 Notes

Instance: S(7,8,24)
Expected blocks: 43263

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
- Best known metrics across all runs for this instance at round open: score=28.22 run=run_20260222_052536 round=3 valid=false exact_once=168640/346104 uncovered=177464 overcovered=0

## Admissibility gate snapshot
```json
{
  "checks": [
    {"i": 0, "numerator": 346104, "denominator": 8, "remainder": 0, "quotient": 43263},
    {"i": 1, "numerator": 100947, "denominator": 7, "remainder": 0, "quotient": 14421},
    {"i": 2, "numerator": 26334, "denominator": 6, "remainder": 0, "quotient": 4389},
    {"i": 3, "numerator": 5985, "denominator": 5, "remainder": 0, "quotient": 1197},
    {"i": 4, "numerator": 1140, "denominator": 4, "remainder": 0, "quotient": 285},
    {"i": 5, "numerator": 171, "denominator": 3, "remainder": 0, "quotient": 57},
    {"i": 6, "numerator": 18, "denominator": 2, "remainder": 0, "quotient": 9}
  ],
  "divisibility_failures": [],
  "expected_block_count": 43263,
  "instance": {"n": 24, "q": 8, "r": 7},
  "is_admissible": true,
  "is_well_formed": true,
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
- Reused local/cache-first material only (`PAPER_NOTES`, `RESEARCH_LOG`, `PRACTICE_LOG`, current `KNOWLEDGE_CACHE`, latest prior run notes/transfer).
- Targeted web searches used this round: `0/1`.
- External links added this round: `0`.

## Plan
- Stage A: run symmetry/orbit compression gate first; keep only if bounded orbit-packed strict progress is real.
- Stage B: reserve absorber/flex capacity early (12% reserve, build cap `38071`) and run uncovered-driven nibble/add-only boosting.
- Stage C: run LNS repairs with `k>1` remove/refill (rollback-safe), not just 1-for-1 swaps.
- Stage D: run residual exact-completion gate and attempt only if eligible.

## Proof workflow (adapted from local paper rules)
Seed directions generated before implementation:
1. Symmetry/orbit seed: bounded cyclic full-orbit additions from uncovered-guided bases.
2. General strict seed: uncovered-driven nibble/add-only under hard gates (`overcovered=0`, `(r-1)` oversubscription `0`).
3. LNS seed: cap-motif-centered `k>1` destroy/repack with local + global refill.

Drafted best attempt in this round:
- Start from prior strict frontier (`21080`) and enforce full architecture in order.

Critical-gap self-verification pass:
1. Gap A (admissibility): divisibility gate rechecked first; pass.
2. Gap B (engine choice): symmetry lane tested first; bounded packed probe produced zero accepted full orbits; switched to general pipeline.
3. Gap C (repair correctness): every accepted move preserved `overcovered=0` and `oversubscribed_(r-1)=0`.
4. Gap D (closure): residual exact completion gate checked; ineligible due large uncovered fraction.

Revision after verification:
- Ran a second tuned pass from the new frontier to test whether add-only or cap-9-centered LNS still had headroom.
- Second pass confirmed local exhaustion at this seed/budget (`0` add accepts over `1.2M` attempts; `0` net LNS gain over `1400` neighborhoods).

## Work log
- Stage A symmetry/orbit gate (mandatory first):
  - Bounded cyclic full-orbit packed probe trials: `320`.
  - Accepted full orbits: `0`.
  - Strict block gain: `0`.
  - Decision: treat symmetry as a diagnostic gate only at this frontier; switch to general strict pipeline.
- Stage B reserve-first strict nibble/add-only:
  - Absorber/flex reserve set to `12%` (`build cap = 38071`), non-binding at this frontier.
  - Attempts: `1,400,000`.
  - Accepted strict additions: `9`.
  - Movement: `21080 -> 21089`.
- Stage C strict LNS (`k>1` remove/refill):
  - Iterations: `900`.
  - Successful positive neighborhoods: `1`.
  - Net strict gain: `+1`.
  - Movement: `21089 -> 21090`.
- Stage D residual exact gate:
  - Not attempted.
  - Gate reason: `not eligible: uncovered fraction is too large; use constructive search first`.
- Verification pass 2 (falsification run):
  - Add-only attempts: `1,200,000`, accepted `0`.
  - LNS iterations: `1400`, net `0`.
  - Final frontier unchanged at `21090`.

## Metric trend
| Checkpoint | Blocks | Score | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Oversubscribed `(r-1)` |
|---|---:|---:|---:|---:|---:|---|---|---:|
| Baseline | 21080 | 28.22 | 168640 | 177464 | 0 | gap 20 (`7019..7039`) | 8 / 9 | 0 |
| Stage A symmetry probe | 21080 | 28.22 | 168640 | 177464 | 0 | gap 20 (`7019..7039`) | 8 / 9 | 0 |
| Stage B add-only | 21089 | 28.24 | 168712 | 177392 | 0 | gap 22 (`7022..7044`) | 8 / 9 | 0 |
| Stage C LNS (final) | 21090 | 28.25 | 168720 | 177384 | 0 | gap 23 (`7022..7045`) | 9 / 9 | 0 |
| Verification pass 2 final | 21090 | 28.25 | 168720 | 177384 | 0 | gap 23 (`7022..7045`) | 9 / 9 | 0 |

Uncovered/overcovered trend:
- `177464/0 -> 177392/0 -> 177384/0`.

## Observations
- Symmetry-orbit compression remained useful as a front gate, but full-orbit strict additions were not tractable at this already dense frontier (`0/320` accepted).
- Strict uncovered reduction still occurred in the general pipeline (`-80` uncovered) while keeping `overcovered=0`.
- `(r-1)` pressure moved from `8/9` to `9/9` but oversubscription stayed zero, so strict feasibility remained transferable.
- A second independent pass showed near-term local exhaustion for this neighborhood family/budget.

## Reuse vs genuinely new (explicit)
- Reused from previous runs:
  - hard admissibility gate before any search,
  - symmetry-first engine selection,
  - reserve-first policy,
  - strict feasibility invariants (`overcovered=0`, `oversubscribed_(r-1)=0`),
  - residual exact-cover late gate only.
- Newly learned this round:
  - At `21080+` density for `S(7,8,24)`, full cyclic-orbit strict augmentation is not productive even with bounded retries.
  - Small but real gains are still available through general strict add + LNS (`+10` blocks total), setting a new repository frontier.
  - Immediate follow-up pass indicates this specific add/LNS policy family plateaus quickly once `(r-1)` load reaches cap (`9/9`).

## Core advance
- advance statement:
  - Improved the strict `S(7,8,24)` frontier from `21080` to `21090` blocks with all hard verifier gates intact.
- evidence from this round (metrics, runtime, structure):
  - Score improved `28.22 -> 28.25`.
  - Exact-once improved `168640 -> 168720`.
  - Uncovered reduced `177464 -> 177384`.
  - `overcovered=0` preserved and `oversubscribed_(r-1)=0` preserved.
  - Architecture compliance: symmetry gate first, reserve-first general pipeline, LNS `k>1`, residual gate checked and deferred.
- transfer value for next rounds:
  - Keep symmetry as a short gate, then switch quickly to strict general pipeline on this frontier.
  - Keep reserve-aware strict operations; they delivered gains without violating transferable invariants.
  - Prioritize stronger plateau-break neighborhoods once `(r-1)` reaches `9/9`.

## Next-hypothesis
- hypothesis statement:
  - Cap-9-centered coupled LNS with two-step neighborhoods (`k=3..6` then `k=2..4` on the same motif) plus short neutral rebalancing sweeps will outperform independent random neighborhoods from `21090`.
- mechanism (why this should help):
  - Current failures suggest transient slack collapses before reuse. Immediate motif reuse should exploit that slack window; neutral rebalancing should reduce point-degree tail pressure and reopen feasible fills.
- expected metric movement:
  - Improve `21090 -> 21120..21210` blocks.
  - Reduce uncovered by `240..960`.
  - Keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 9`.
- falsification / stop condition:
  - Reject if after `>=12000` coupled neighborhoods net gain is `< +15` blocks or gain-per-1000 neighborhoods does not beat this round's baseline.
