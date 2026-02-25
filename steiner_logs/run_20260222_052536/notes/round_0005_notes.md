# Round 5 Notes

Instance: S(9,10,22)
Expected blocks: 49742

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: steiner_logs/run_20260222_052536/REPO_WIDE_HISTORY.md
- Global research log (all runs round1): steiner_logs/RESEARCH_LOG.md
- Global practice log (all runs round2-5): steiner_logs/PRACTICE_LOG.md
- Global research paper (paper-style synthesis): steiner_logs/RESEARCH_PAPER.md
- Existence frontier report (all admissible triples): steiner_logs/EXISTENCE_FRONTIER.md
- Local paper notes: steiner_logs/PAPER_NOTES.md
- Latest prior run: run_20260222_012007
- Latest prior round1 notes: steiner_logs/run_20260222_012007/notes/round_0001_notes.md
- Latest prior round5 notes: steiner_logs/run_20260222_012007/notes/round_0005_notes.md
- Latest prior transfer: steiner_logs/run_20260222_012007/NEXT_GENERATION_TRANSFER.md
- Best known startpoint for this instance at round open: score=26.85 exact_once=237520/497420 uncovered=259900 overcovered=0

## Admissibility gate snapshot
```json
{
  "instance": {"n": 22, "q": 10, "r": 9},
  "is_admissible": true,
  "expected_block_count": 49742,
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
- Reused cached/literature policy only; no new web search executed in this round (`0/1` targeted searches used).
- Reused symmetry diagnostics from prior successful round on this exact instance: cyclic lane remains tractable and productive.

## Plan
- Stage A: run symmetry/orbit engine selection first; keep symmetry lane if tractable.
- Stage B: reserve absorber/flex capacity early (12% reserve) before any greedy growth.
- Stage C: strict constructive search with add-only plus LNS `k -> k+1` repacks under hard gates.
- Stage D: residual exact completion only if strict residual gate becomes eligible.
- Stage E: proof-style critical-gap verification and revision loop.

## Proof workflow (adapted from local paper rules)
Seed proof directions generated before implementation:
1. Symmetry/orbit seed direction: keep cyclic lane because prior `C22` diagnostics were strong and produced the current strict seed.
2. Reserve-first strict growth direction: exploit zero-collision slack without consuming all long-horizon flexibility.
3. LNS direction: remove local conflicting block sets and refill with exact `k -> k+1` micro-packs around saturated 8-face motifs.

Drafted best attempt in this round:
- Start from the symmetry-derived strict baseline and run repeated strict add/repack cycles.

Critical-gap self-verification pass:
1. Gap A (admissibility): divisibility gate rechecked before search; pass.
2. Gap B (engine choice): symmetry lane kept (tractable on this instance), randomized fallback not selected.
3. Gap C (repair correctness): every accepted move preserved `overcovered=0`, `oversubscribed_(r-1)=0`, `r_minus_1_max_degree<=7`.
4. Gap D (closure): residual exact completion ineligible; uncovered fraction remained far above gate.

Revision after verification:
- Continued bounded strict cycles because the same LNS motif family kept giving monotone improvements.

## Work log
- Stage A symmetry/orbit selection:
  - Reused prior cyclic tractability witness for this instance (`C22` had very low non-binary mass in previous round diagnostics).
  - Confirmed current starting candidate is the same strict symmetry-seeded frontier used previously.
- Stage B reserve-first policy:
  - Reserved 12% of expected blocks as absorber/flex budget (`5969` slots); reserve remained non-binding at this frontier.
- Stage C strict constructive improvement:
  - Initial global add-only from baseline: `+1` strict block.
  - Repeated strict LNS repack cycles (`1 -> 2` exact local packs, motif-coupled around saturated 8-faces) plus follow-up strict add-only sweeps.
  - Net movement this round: `23752 -> 24165` blocks (`+413`).
  - Composition of gains: add-only `+33`; strict repacks `+380`.
- Stage D residual exact-completion gate:
  - Not attempted; residual remained ineligible (`uncovered=255770`, fraction `0.5142`).

## Metric trend
| Checkpoint | Blocks | Score | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Oversubscribed `(r-1)` |
|---|---:|---:|---:|---:|---:|---|---|---:|
| Baseline start | 23752 | 26.85 | 237520 | 259900 | 0 | gap 6 (`10793..10799`) | 7 / 7 | 0 |
| After cycle 1 | 23773 | 26.91 | 237730 | 259690 | 0 | gap 14 (`10801..10815`) | 7 / 7 | 0 |
| After cycle 2 | 23809 | 27.01 | 238090 | 259330 | 0 | gap 11 (`10816..10827`) | 7 / 7 | 0 |
| After cycle 3 | 23880 | 27.21 | 238800 | 258620 | 0 | gap 12 (`10848..10860`) | 7 / 7 | 0 |
| After cycle 4 | 24007 | 27.57 | 240070 | 257350 | 0 | gap 16 (`10904..10920`) | 7 / 7 | 0 |
| Final | 24165 | 28.01 | 241650 | 255770 | 0 | gap 27 (`10968..10995`) | 7 / 7 | 0 |

Uncovered/overcovered trend (best checkpoints):
- `259900/0 -> 259690/0 -> 259330/0 -> 258620/0 -> 257350/0 -> 255770/0`.

## Observations
- Strict zero-collision growth remains available well past the prior frontier when repacks are centered on saturated 8-face motifs.
- `(r-1)` pressure stayed exactly at cap but never crossed it (`7/7`, oversubscribed count always `0`).
- Point-degree spread widened as coverage increased, but remained small relative to target degree.
- Residual exact cover is still structurally premature for this instance at this frontier.

## Reuse vs genuinely new (explicit)
- Reused from previous runs:
  - hard admissibility gate before search,
  - symmetry-first engine selector,
  - strict feasibility invariants (`c_9<=1`, `c_8<=7`),
  - residual exact-cover late-gate discipline.
- Newly learned this round:
  - The previously reported strict frontier (`23752`) was not near local exhaustion under motif-coupled strict repacks.
  - Repeated strict `1 -> 2` repack cycles can continue yielding monotone gains for this instance far beyond prior expectations.
  - Add-only opportunities reappear after each repack wave, so alternating add/repack beats single-phase continuation.

## Core advance
- advance statement:
  - Established a high-yield strict improvement regime for `S(9,10,22)` that pushes the certified zero-collision frontier from `23752` to `24165` blocks without violating `(r-1)` caps.
- evidence from this round (metrics, runtime, structure):
  - Score improved `26.85 -> 28.01`.
  - Exact-once increased `237520 -> 241650`.
  - Uncovered reduced `259900 -> 255770` with `overcovered=0` maintained.
  - `(r-1)` load stayed `7/7` with `oversubscribed_(r-1)=0` throughout.
- transfer value for next rounds:
  - Re-use alternating strict add-only sweeps and motif-coupled strict repack waves as default late-stage policy for this instance.
  - Keep strict gates hard; they did not block progress and preserved transferability.

## Next-hypothesis
- hypothesis statement:
  - Two-tier strict neighborhoods (`1->2` for rapid gains plus periodic `k=2..4 -> k+1` exact micro-packs) will improve gain-per-time over `1->2`-only continuation from this new frontier.
- mechanism (why this should help):
  - `1->2` quickly exploits immediate local slack; periodic larger windows should unlock motifs that single-block release cannot expose.
- expected metric movement:
  - Move `24165 -> 24350..24750` blocks under unchanged strict gates.
  - Reduce uncovered by `1850..5850` while keeping `overcovered=0` and `(r-1)` oversubscription `0`.
- falsification / stop condition:
  - Reject if after `>=12000` mixed neighborhoods the net gain is `< +120` blocks or if gain-per-1000 neighborhoods under mixed windows is not above `1->2`-only baseline.

## Rounds 1-5 Synthesis
### Vital advances and decisive failures
- Vital advance: round1 converted the process into a gate-first theorem-style protocol (admissibility, engine selector, strict repair, residual eligibility).
- Vital advance: this round shows the `S(9,10,22)` strict frontier was materially extendable; new best strict candidate is now `24165` blocks.
- Decisive failure: early residual exact-cover remains a dead lane at high uncovered fraction; still not close to eligibility.
- Decisive failure: single-phase continuation (add-only only, or repack-only only) leaves measurable gains uncollected.

### Retired hypotheses (stop repeating)
- Retired: "current strict frontier near exhaustion" for `S(9,10,22)`.
Reason: this round delivered `+413` strict blocks from the prior frontier.
- Retired: "residual exact cover may help at ~50% uncovered".
Reason: eligibility gate remains strongly violated and prior attempts showed no practical movement.
- Retired: "need to relax strict caps for major gains".
Reason: large gains were achieved while holding strict caps exactly.

### Active hypotheses (top 3) with falsification
1. Alternating strict add-only and motif-coupled repack waves dominates any single-phase policy at this frontier.
Falsification test: run matched compute budgets (`add-only`, `repack-only`, `alternating`) and reject if alternating is not best on net block gain.
2. Mixed-window strict LNS (`1->2` plus periodic `k=2..4 -> k+1`) improves gain-per-time over `1->2` alone.
Falsification test: reject if mixed-window gain per 1000 neighborhoods is not at least 10% above `1->2` baseline.
3. Saturated-8-face targeting is the right proposal bias for this instance.
Falsification test: reject if random-uncovered-9 targeting matches or beats saturated-8 targeting under matched budgets.

### One next-round experiment (best separator)
- Run a 3-arm ablation from the current `24165` frontier under equal neighborhood budget and identical strict gates:
  - Arm A: add-only only,
  - Arm B: `1->2` repacks only,
  - Arm C: alternating add-only + periodic `k=2..4 -> k+1` repacks.
- Compare by net block gain, uncovered reduction, and strict violation count (must remain zero).
