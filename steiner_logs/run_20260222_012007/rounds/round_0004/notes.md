# Round 4 Notes

Instance: S(8,9,21)
Expected blocks: 22610
Date (UTC): 2026-02-22

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
- Best known metrics across all runs for this instance at round start: none

## Admissibility gate snapshot
```json
{
  "checks": [
    {"denominator": 9, "i": 0, "numerator": 203490, "quotient": 22610, "remainder": 0},
    {"denominator": 8, "i": 1, "numerator": 77520, "quotient": 9690, "remainder": 0},
    {"denominator": 7, "i": 2, "numerator": 27132, "quotient": 3876, "remainder": 0},
    {"denominator": 6, "i": 3, "numerator": 8568, "quotient": 1428, "remainder": 0},
    {"denominator": 5, "i": 4, "numerator": 2380, "quotient": 476, "remainder": 0},
    {"denominator": 4, "i": 5, "numerator": 560, "quotient": 140, "remainder": 0},
    {"denominator": 3, "i": 6, "numerator": 105, "quotient": 35, "remainder": 0},
    {"denominator": 2, "i": 7, "numerator": 14, "quotient": 7, "remainder": 0}
  ],
  "divisibility_failures": [],
  "expected_block_count": 22610,
  "instance": {"n": 21, "q": 9, "r": 8},
  "is_admissible": true,
  "is_well_formed": true,
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
- Read steiner_logs/PAPER_NOTES.md, steiner_logs/RESEARCH_LOG.md, steiner_logs/PRACTICE_LOG.md, steiner_logs/EXISTENCE_FRONTIER.md, steiner_logs/run_20260222_012007/REPO_WIDE_HISTORY.md, steiner_logs/run_20260221_013905/notes/round_0001_notes.md, steiner_logs/run_20260221_013905/notes/round_0005_notes.md, steiner_logs/run_20260221_013905/NEXT_GENERATION_TRANSFER.md, and steiner_logs/run_20260222_012007/KNOWLEDGE_CACHE.md before search.
- New web sources used this round: 0/1.

## Plan
- Stage A: mandatory symmetry/orbit gate first.
- Stage B: strict add-only nibble/boosting with early reserved flex capacity.
- Stage C: LNS destroy/repack (`k>=2`) with motif-coupled windows and strict gates.
- Stage D: residual exact-cover gate only if uncovered residual is small and overcoverage is zero.

## Work log
- Stage A (symmetry/orbit diagnostics first):
  - `C21`: `|O_8|=9690`, `|O_9|=14000`, binary/non-binary columns `13983/17`, `max_coeff=3`.
  - `D21`: `|O_8|=4950`, `|O_9|=7105`, binary/non-binary columns `6891/214`, `max_coeff=6`.
  - Bounded cyclic orbit-packed trial (3 seeds) best:
    - `9793` blocks, `score=20.64`, `uncovered=115353`, `overcovered=0`, `(r-1)` max `7/7`.
  - Decision: symmetry lane is diagnosable but quality-inferior to incumbent strict seed in this budget; switch to general strict pipeline.
- Stage B (strict add-only with reserve):
  - Round-start seed: `12107` blocks (`score=34.97`, `uncovered=94527`, `overcovered=0`).
  - Reserved flex/absorber capacity early: `reserve_blocks=904` (do not greedily consume all slots).
  - Add-only strict scan attempts:
    - pass1: `258609` attempts, `0` accepted;
    - pass2: `120000` attempts, `0` accepted.
  - Conclusion: add-only growth is exhausted at this frontier.
- Stage C (LNS destroy/repack, strict-feasible throughout):
  - Pass1 (`3000` trials): `14` accepted gain windows, `+14` net blocks (`12107 -> 12121`), uncovered `94527 -> 94401`, score `34.97 -> 35.05`.
  - Pass2 (`5000` trials, larger windows): `11` accepted gain windows, `+12` net blocks (`12121 -> 12133`), uncovered `94401 -> 94293`, score `35.05 -> 35.13`.
  - Pass3 (`3000` trials, bounded confirmation): `5` accepted gain windows, `+5` net blocks (`12133 -> 12138`), uncovered `94293 -> 94248`, score `35.13 -> 35.16`.
- Stage D (residual exact completion gate):
  - Gate check at final checkpoint: `overcovered=0`, but uncovered fraction `94248/203490=0.4634`.
  - Decision: residual not small; exact residual completion not attempted.

## Proof-workflow adaptation (this round)
- Seed direction 1 (symmetry-compressed lane): cyclic/dihedral orbit diagnostics + bounded orbit-packed trial.
- Seed direction 2 (reserve-aware additive lane): strict add-only with explicit reserved capacity for late repair.
- Seed direction 3 (best attempt): motif-coupled larger-window LNS destroy/repack with strict row-owner and `(r-1)` cap gates.
- Drafted best attempt: Seed 3 was selected after Seed 1 underperformed and Seed 2 plateaued.
- Critical-gap self-verification pass:
  - Gap A (admissibility): pass.
  - Gap B (strict feasibility): pass at all accepted checkpoints (`overcovered=0`, oversubscribed `(r-1)` subsets `=0`, `r_minus_1_max_degree=7` at target).
  - Gap C (late exact closure eligibility): fail this round due to large residual uncovered mass.
- Revision within budget:
  - Increased LNS window sizes and repeated motif-coupled passes (pass2/pass3), yielding additional strict gains after pass1 plateau.

## Metric trend
| Stage | Blocks | Score | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Oversubscribed `(r-1)` |
|---|---:|---:|---:|---:|---:|---|---|---:|
| Start seed | 12107 | 34.97 | 108963/203490 | 94527 | 0 | gap 713 (`4811..5524`) | 7 / 7 | 0 |
| Symmetry packed best (bounded) | 9793 | 20.64 | 88137/203490 | 115353 | 0 | gap 0 (`4197..4197`) | 7 / 7 | 0 |
| Add-only strict best | 12107 | 34.97 | 108963/203490 | 94527 | 0 | gap 713 (`4811..5524`) | 7 / 7 | 0 |
| After LNS pass1 | 12121 | 35.05 | 109089/203490 | 94401 | 0 | gap 702 (`4823..5525`) | 7 / 7 | 0 |
| After LNS pass2 | 12133 | 35.13 | 109197/203490 | 94293 | 0 | gap 697 (`4832..5529`) | 7 / 7 | 0 |
| Final (LNS pass3) | 12138 | 35.16 | 109242/203490 | 94248 | 0 | gap 692 (`4837..5529`) | 7 / 7 | 0 |

Uncovered/overcovered trend (best checkpoints):
- `94527/0 -> 94401/0 -> 94293/0 -> 94248/0`.

## Reuse vs genuinely new (explicit)
- Reused from previous runs:
  - mandatory symmetry-front gate and quick fallback policy,
  - strict-feasible invariants (`overcovered=0`, no `(r-1)` oversubscription),
  - motif-coupled destroy/repack as primary plateau-breaker after add-only stalls,
  - reserve-first discipline before aggressive refill.
- Newly learned this round:
  - For `S(8,9,21)`, cyclic symmetry diagnostics are relatively clean (`17` non-binary columns) but bounded orbit-packed quality is still much weaker than incumbent strict LNS seed in this runtime budget.
  - Add-only growth is fully exhausted at this frontier even with substantial search budget; gains are sparse and almost entirely LNS-mediated.
  - Larger-window motif-coupled LNS remains productive but sparse (`30` accepted gain windows over `11000` trials total across passes), with monotone strict improvements and gradual degree-spread contraction.

## Observations
- Hard gates remained stable for all accepted moves:
  - `overcovered_r_subsets = 0`,
  - `oversubscribed_r_minus_1_subsets = 0`,
  - `r_minus_1_max_degree = 7` (target `lambda_7=7`).
- Verifier improvements are currently tied to small strict gains in block count; each accepted net block gives predictable uncovered reduction (`9` per block at `overcovered=0`).
- Residual exact-cover remains far from eligibility; this is still a constructive/LNS-dominated phase.

## Core advance
- advance statement:
  - Established the first strict-feasible improving frontier for `S(8,9,21)` in this repository by executing the mandatory symmetry gate, proving add-only exhaustion, and then extracting monotone gains with larger-window motif-coupled LNS under hard verifier constraints.
- evidence from this round (metrics, runtime, structure):
  - Stage A symmetry was executed first and rejected on quality, not on missing diagnostics.
  - Stage B add-only produced `0` gains despite large attempt budgets.
  - Stage C LNS passes yielded `+31` net strict blocks (`12107 -> 12138`) with verifier movement:
    - `score 34.97 -> 35.16`,
    - `exact_once 108963 -> 109242`,
    - `uncovered 94527 -> 94248`,
    - `overcovered 0 -> 0`, oversubscribed `(r-1)` `0 -> 0`.
  - Structural pressure also improved (`point_degree_gap 713 -> 692`) while keeping `(r-1)` max at target (`7`).
- transfer value for next rounds:
  - Keep symmetry diagnostics as mandatory front gate but avoid long orbit-packed budgets for this instance.
  - Skip long add-only scans once plateau is confirmed; invest budget directly in motif-coupled larger-window LNS.
  - Preserve strict feasibility as a hard acceptance filter and use periodic neutral balancing when gain windows become sparse.

## Next-hypothesis
- hypothesis statement:
  - Two-step motif reuse with medium-large windows (`k=4..10`) around the same capped `7`-subset cluster, interleaved with short neutral rebalance sweeps, will increase net gain-per-1000 trials beyond the current sparse baseline.
- mechanism (why this should help):
  - First accepted windows create transient local slack around the released capped motif. Immediate reuse of the same motif before re-hardening should raise second-window success probability; neutral sweeps reduce degree-tail concentration and enlarge feasible refill options.
- expected metric movement:
  - Improve `12138 -> 12170..12260` blocks,
  - reduce uncovered by `288..1098`,
  - keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 7`.
- falsification / stop condition:
  - Stop this hypothesis for a setting if after `>=6000` motif-coupled trials either:
  - net gain is `< +8` blocks,
  - or accepted-gain rate is `< 0.15%` without concurrent point-gap reduction of at least `5`.
