# Round 6 Notes

Instance: S(9,10,20)
Expected blocks: 16796
Date (UTC): 2026-02-22

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: steiner_logs/run_20260221_013905/REPO_WIDE_HISTORY.md
- Global research log (all runs round1): steiner_logs/RESEARCH_LOG.md
- Global practice log (all runs round2-5): steiner_logs/PRACTICE_LOG.md
- Latest round1 notes source: steiner_logs/run_20260221_013905/notes/round_0001_notes.md
- Latest round5 notes source: steiner_logs/run_20260221_013905/notes/round_0005_notes.md

## Plan
- Continue from strict-feasible r=9 frontier (`8138` blocks, `overcovered=0`).
- Run chained motif-coupled `1->2` micro-augment trials only.
- Keep hard invariants at every accepted move: `overcovered=0`, `oversubscribed_(r-1)=0`, `r_minus_1_max_degree<=6`.

## Work log
- Re-verified baseline from prior best candidate:
  - blocks `8138`, score `27.83`, exact_once `81380`, uncovered `86580`, overcovered `0`.
- Confirmed exact-backbone add-only stage still plateaus on this frontier (multi-seed rechecks stayed flat at `8138`).
- Executed optimized chained `1->2` strict micro-augment search over multiple seeds (`6000` trials each):
  - seed `3`: `+22` strict moves -> `8160` blocks.
  - seed `7`: `+21` strict moves -> `8159` blocks.
  - seed `11`: `+22` strict moves -> `8160` blocks.
  - seed `17`: `+22` strict moves -> `8160` blocks.
  - seed `23`: `+23` strict moves -> `8161` blocks (best).
- Promoted seed `23` candidate to run best/current for `S(9,10,20)`.

## Metric trend
| Stage | Blocks | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Oversubscribed `(r-1)` |
|---|---:|---:|---:|---:|---|---|---:|
| Start seed | 8138 | 81380 | 86580 | 0 | gap 250 (`3931..4181`) | 6 / 6 | 0 |
| Final (best seed=23) | 8161 | 81610 | 86350 | 0 | gap 246 | 6 / 6 | 0 |

Uncovered/overcovered trend (best checkpoints):
- `86580/0 -> 86350/0`.

## Reuse vs genuinely new (explicit)
- Reused from previous runs:
  - strict-feasible invariants and symmetry-front-gate conclusions,
  - motif/freed-face `1->2` augment framework.
- Newly learned this round:
  - chained micro-augment lane remains productive beyond `8138` and reaches `8161` under the same hard invariants,
  - multi-seed search diversity gives stable gains (`+21..+23`) for this stage.

## Observations
- Add-only strict growth is still exhausted; improvements come from remove-then-double-add exact micro-repacks.
- No overcoverage was introduced in any accepted move.
- `(r-1)` cap remained tight but feasible (`max=6`, oversubscribed count `0`).

## Core advance
- advance statement:
  - Extended the strict-feasible `r=9` frontier from `8138` to `8161` using chained motif-coupled `1->2` micro-augment repairs.
- evidence from this round (metrics, runtime, structure):
  - Best seed (`23`) achieved `+23` strict moves over `6000` trials.
  - Verifier moved `score 27.83 -> 28.02`, `exact_once 81380 -> 81610`, `uncovered 86580 -> 86350`, with `overcovered=0` unchanged.
- transfer value for next rounds:
  - Keep chained `1->2` as first repair lane at `8160` frontier.
  - Continue multi-seed batches and retain only strict-feasible improvements.

## Next-hypothesis
- hypothesis statement:
  - Mixed source ratios for neighborhood generation (`freed-9` vs `hot-8` vs random uncovered-9) will improve gain-per-1000 trials beyond current chained baseline.
- mechanism (why this should help):
  - Different sources unlock different local slack structures; fixed ratios likely under-sample one of the productive motif classes.
- expected metric movement:
  - Improve `8161 -> 8180..8210` blocks while keeping `overcovered=0` and zero `(r-1)` oversubscription.
- falsification / stop condition:
  - Stop the current ratio set if after `>=10000` trials net gain is `< +6` blocks.
