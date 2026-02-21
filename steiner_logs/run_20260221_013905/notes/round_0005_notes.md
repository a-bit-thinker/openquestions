# Round 5 Notes

Instance: S(9,10,20)
Expected blocks: 16796
Date (UTC): 2026-02-21

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: steiner_logs/run_20260221_013905/REPO_WIDE_HISTORY.md
- Global research log (all runs round1): steiner_logs/RESEARCH_LOG.md
- Global practice log (all runs round2-5): steiner_logs/PRACTICE_LOG.md
- Latest prior run: run_20260220_222441
- Latest prior round1 notes source run: run_20260220_222441
- Latest prior round1 notes: steiner_logs/run_20260220_222441/notes/round_0001_notes.md
- Latest prior round5 notes source run: run_20260220_183105
- Latest prior round5 notes: steiner_logs/run_20260220_183105/notes/round_0005_notes.md
- Latest prior transfer: steiner_logs/run_20260220_222441/NEXT_GENERATION_TRANSFER.md
- Best known metrics across all runs for this instance: score=55.44 run=run_20260219_180444 round=5 valid=false exact_once=118787/167960 uncovered=28530 overcovered=20643

## Admissibility gate snapshot
```json
{
  "checks": [
    {"denominator": 10, "i": 0, "numerator": 167960, "quotient": 16796, "remainder": 0},
    {"denominator": 9, "i": 1, "numerator": 75582, "quotient": 8398, "remainder": 0},
    {"denominator": 8, "i": 2, "numerator": 31824, "quotient": 3978, "remainder": 0},
    {"denominator": 7, "i": 3, "numerator": 12376, "quotient": 1768, "remainder": 0},
    {"denominator": 6, "i": 4, "numerator": 4368, "quotient": 728, "remainder": 0},
    {"denominator": 5, "i": 5, "numerator": 1365, "quotient": 273, "remainder": 0},
    {"denominator": 4, "i": 6, "numerator": 364, "quotient": 91, "remainder": 0},
    {"denominator": 3, "i": 7, "numerator": 78, "quotient": 26, "remainder": 0},
    {"denominator": 2, "i": 8, "numerator": 12, "quotient": 6, "remainder": 0}
  ],
  "divisibility_failures": [],
  "expected_block_count": 16796,
  "instance": {"n": 20, "q": 10, "r": 9},
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 16796,
    "lambda_1": 8398,
    "lambda_2": 3978,
    "lambda_3": 1768,
    "lambda_4": 728,
    "lambda_5": 273,
    "lambda_6": 91,
    "lambda_7": 26,
    "lambda_8": 6
  }
}
```

## Research reuse
- Read steiner_logs/RESEARCH_LOG.md, steiner_logs/PRACTICE_LOG.md, steiner_logs/run_20260221_013905/REPO_WIDE_HISTORY.md, steiner_logs/run_20260220_222441/notes/round_0001_notes.md, steiner_logs/run_20260220_183105/notes/round_0005_notes.md, and steiner_logs/run_20260220_222441/NEXT_GENERATION_TRANSFER.md before search.
- Read steiner_logs/run_20260221_013905/KNOWLEDGE_CACHE.md before Stage A.
- New web sources used this round: 0/1.

## Plan
- Stage A: symmetry/orbit compression gate first.
- Stage B: general pipeline entry with strict add-only nibble/boosting from current strict-feasible seed.
- Stage C: reserve-aware repair with LNS-style local repacks (`1->2` exact micro-augment lane).
- Stage D: residual exact completion only if uncovered residual is small and `overcovered=0`.

## Work log
- Stage A symmetry gate (reused deterministic diagnostics from prior same-instance probes in cache):
  - `C20`: `|O_9|=8398`, `|O_10|=9252`, binary/non-binary columns `9215/37`, `max_coeff=10`, bounded binary DFS unsolved (`20s`, `nodes=8`).
  - `D20`: `|O_9|=4262`, `|O_10|=4752`, binary/non-binary columns `4488/264`, `max_coeff=10`, bounded binary DFS unsolved (`20s`, `nodes=113`).
  - Decision: not tractable for strict binary exact-cover in budget; switch to general pipeline.
- Stage B nibble/boosting (strict add-only):
  - Full add-only strict scan from `8120` found `0` feasible additions.
- Stage C repair (reserve-aware local repack):
  - Broad neighborhood LNS was too expensive per neighborhood for this environment.
  - Switched to exact micro-augment lane with motif/freed-face candidate generation and `1->2` strict repacks.
  - Trial summary: `1325` neighborhood trials, `18` successful strict `1->2` augmentations.
  - Net movement: `8120 -> 8138` blocks (`+18`).
- Stage D residual exact completion gate:
  - Final `overcovered=0`, but uncovered fraction `86580 / 167960 = 0.5155`.
  - Residual is not small; exact residual completion not attempted.

## Metric trend
| Stage | Blocks | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Oversubscribed `(r-1)` |
|---|---:|---:|---:|---:|---|---|---:|
| Start seed | 8120 | 81200 | 86760 | 0 | gap 251 (`3922..4173`) | 6 / 6 | 0 |
| Additive best | 8120 | 81200 | 86760 | 0 | gap 251 (`3922..4173`) | 6 / 6 | 0 |
| Final (micro-augment) | 8138 | 81380 | 86580 | 0 | gap 250 (`3931..4181`) | 6 / 6 | 0 |

Uncovered/overcovered trend (best checkpoints):
- `86760/0 -> 86580/0`.

## Reuse vs genuinely new (explicit)
- Reused from previous runs:
  - symmetry-front-gate diagnostics and quick-switch policy,
  - strict-feasible hard gates (`overcovered=0`, `(r-1)` oversubscription `=0`),
  - motif-coupled local augmenting idea (`1->2`) as the sparse-gain lane.
- Newly learned this round:
  - On this `r=9` frontier, exact `1->2` micro-augment chains can still produce monotone strict gains (`+18`) after add-only exhaustion.
  - Wider LNS neighborhoods are still useful conceptually, but in this environment their per-neighborhood cost is too high; targeted micro-augment neighborhoods are higher gain-per-runtime.

## Observations
- Add-only strict growth is exhausted at this frontier (`0` feasible additions from `8120`).
- Strict gains are sparse but real: `18` successful `1->2` moves over `1325` trials.
- Hard invariants remained intact throughout accepted moves:
  - `overcovered_r_subsets = 0`,
  - `oversubscribed_r_minus_1_subsets = 0`,
  - `r_minus_1_max_degree = 6` (target `lambda_8=6`).
- Structural side effect: cap-6 `8`-subset tail count rose from `53` to `58`; strict block gain came from trading local tail pressure for additional coverage.

## Core advance
- advance statement:
  - Established a practical strict-feasible `r=9` plateau-breaker for this run by combining a mandatory symmetry front gate with fast exact `1->2` micro-augment repairs after add-only exhaustion.
- evidence from this round (metrics, runtime, structure):
  - Stage A symmetry was gated first and rejected using cached deterministic `C20/D20` diagnostics.
  - Stage B add-only strict pass produced `0` gains.
  - Stage C micro-augment lane produced `+18` strict blocks (`8120 -> 8138`) with verifier movement `score 27.68 -> 27.83`, `exact_once 81200 -> 81380`, `uncovered 86760 -> 86580`.
  - Feasibility invariants remained strict: `overcovered=0`, `oversubscribed_(r-1)=0`.
- transfer value for next rounds:
  - Keep symmetry diagnostics as front gate, but do not spend long budgets there for this instance.
  - Use fast motif/freed-face exact `1->2` augmentation as the default first repair lane at the `8120+` strict frontier.
  - Treat broad-window LNS as secondary diversification unless runtime budget is significantly larger.

## Next-hypothesis
- hypothesis statement:
  - Coupled `1->2 -> 1->2` chains on the same saturated 8-subset motif, with short motif-taboo and canonical neighborhood dedup, will outperform uncoupled random motif selection from `8138`.
- mechanism (why this should help):
  - Successful first augmentations indicate transient slack near the released motif. Reusing that motif before pressure re-hardens should increase second-step augment probability.
- expected metric movement:
  - Improve `8138 -> 8155..8195` blocks,
  - reduce uncovered by `170..570`,
  - keep `overcovered=0`, `oversubscribed_(r-1)=0`, and `r_minus_1_max_degree <= 6`.
- falsification / stop condition:
  - Stop this hypothesis if after `>=3000` chained trials either:
  - net gain is `< +8` blocks,
  - or second-step success rate after a first-step success is `< 10%`.

## Rounds 1-5 Synthesis
### Practice trajectory (Rounds 2-5)
- Round 2 (`S(6,7,17)`): strict-feasible balance-first repacks improved structure (`cap-tail` and degree spread) even when augment count stalled.
- Round 3 (`S(7,8,18)`): motif-coupled exact augment lanes scaled and produced meaningful strict gains (`2252 -> 2289`).
- Round 4 (`S(8,9,19)`): strict gains became sparse (`+2`), confirming higher-order bottleneck hardening and the need for high-trial sparse-event tactics.
- Round 5 (`S(9,10,20)`): strict frontier advanced from `8120` to `8138` through exact micro-augment chains after add-only exhaustion.

### Connection back to Round 1 research priorities
- Round 1 prioritized a dual-engine workflow: bounded symmetry triage then iterative repair/absorption.
- Practice from Rounds 2-5 confirms that priority directly:
  - symmetry is valuable as a cheap reject/accept gate,
  - durable progress at `r>=8` is repair-driven,
  - strict feasibility gates are stable and should remain hard invariants.
- The observed sparse-gain regime at `r=8,9` matches the cache guidance to prefer motif-targeted repair over long additive-only continuation.

### Strongest advances by round
1. Round 1: established admissibility-first + symmetry/front-gate + staged repair architecture with explicit switch criteria.
2. Round 2: showed strict-feasible neutral repacks are valuable conditioning moves before augmentation attempts.
3. Round 3: validated motif-coupled strict augment loops as a reproducible gain engine.
4. Round 4: confirmed sparse-event behavior at higher `r` and kept strict invariants while still finding gains.
5. Round 5: converted sparse-event lane into `+18` strict gains at `r=9` from the `8120` plateau.

### Failed directions and why they failed
1. Long binary-only symmetry DFS on `r=9`: non-binary orbit coefficients (`max_coeff=10`) make pure binary exact-cover mismatched in this budget.
2. Add-only continuation at `8120+`: no feasible strict additions remain.
3. Large-window LNS-first execution in this environment: per-neighborhood runtime too high relative to sparse gain frequency.

### Top 3 next hypotheses with round-6 test protocol
1. Hypothesis: chained motif reuse (`same motif` two-step `1->2`) increases gain-per-1000 trials.
Test protocol: run `3` seeds, `>=3000` chained trials each, compare net block gains and second-step hit rate against uncoupled motif baseline.
2. Hypothesis: mixed neighborhood source ratios (`freed-9` vs `hot-8` vs random uncovered-9) materially affect strict augment hit rate.
Test protocol: A/B/C on ratios `{60/30/10, 40/40/20, 25/50/25}` over matched trial budgets and fixed hard gates.
3. Hypothesis: periodic neutral balance sweeps (every `N` successful augments) reduce later augment droughts.
Test protocol: compare `N in {4, 8, 16}` versus no-balance control; measure block gain slope in the next `1000` trials.
