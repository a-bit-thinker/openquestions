# Round 2 Notes

Instance: S(6,7,17)
Expected blocks: 1768

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
- Best known metrics across all runs for this instance: score=66.04 run=run_20260219_030101 round=2 valid=? exact_once=9591/12376 uncovered=1575 overcovered=1210

## Admissibility gate snapshot
```json
{
  "checks": [
    {"denominator": 7, "i": 0, "numerator": 12376, "quotient": 1768, "remainder": 0},
    {"denominator": 6, "i": 1, "numerator": 4368, "quotient": 728, "remainder": 0},
    {"denominator": 5, "i": 2, "numerator": 1365, "quotient": 273, "remainder": 0},
    {"denominator": 4, "i": 3, "numerator": 364, "quotient": 91, "remainder": 0},
    {"denominator": 3, "i": 4, "numerator": 78, "quotient": 26, "remainder": 0},
    {"denominator": 2, "i": 5, "numerator": 12, "quotient": 6, "remainder": 0}
  ],
  "divisibility_failures": [],
  "expected_block_count": 1768,
  "instance": {"n": 17, "q": 7, "r": 6},
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 1768,
    "lambda_1": 728,
    "lambda_2": 273,
    "lambda_3": 91,
    "lambda_4": 26,
    "lambda_5": 6
  }
}
```

## Research reuse
- Read steiner_logs/RESEARCH_LOG.md, steiner_logs/PRACTICE_LOG.md, then steiner_logs/run_20260221_013905/KNOWLEDGE_CACHE.md before search.
- New web sources used this round: 0/1 (cache was sufficient).

## Reuse vs genuinely new (explicit)
- Reused from prior runs:
  - hard admissibility/divisibility gate as strict pre-search invariant,
  - symmetry front gate with bounded cyclic/dihedral diagnostics,
  - reserve-first LNS + motif-coupled exact augmentation attempts,
  - strict hard move gates for this lane (`overcovered=0`, `(r-1)` cap respected).
- Newly learned this round:
  - for `S(6,7,17)` at current frontier, strict-feasible block-count growth appears stalled at `1116` across three independent high-trial repair programs,
  - neutral strict-feasible repacks can still materially improve structural quality: point-degree spread improved `24 -> 19` at fixed coverage,
  - cap-tail pressure reduced at fixed block count (`5`-subset load-6 count `72 -> 69`), giving a better-conditioned seed even without immediate block-count gain.

## Plan
1. Stage A: symmetry/orbit compression front gate (cyclic/dihedral), use only if tractable.
2. Stage B: general pipeline handoff (`nibble/additive boost -> reserve-aware repair`).
3. Stage C: absorber/flex LNS destroy/repack + exact local augment (`k -> k+1`).
4. Stage D: residual exact completion only if residual is small and overcoverage is zero.

## Work log
- Stage A (symmetry/orbit diagnostics first):
  - Cyclic `C17`: `|O_6|=728`, `|O_7|=1144`; binary columns `1136`, non-binary columns `8`, max orbit coefficient `2`.
  - Cyclic bounded binary DFS (`~8s`, `120k` nodes budget): explored `32385` nodes, `solved=false`.
  - Dihedral `D17`: `|O_6|=392`, `|O_7|=600`; binary columns `352`, non-binary columns `248`, max orbit coefficient `2`.
  - Dihedral bounded binary DFS (`~16s`, `120k` nodes budget): `nodes=0`, `solved=false` (no viable binary front).
  - Decision: symmetry lane not tractable in-budget; switched to general pipeline.
- Stage B (nibble/additive boost with strict gates):
  - Strict add-only probe found no admissible additions (`stageB direct additions = 0`).
- Stage C (reserve-aware LNS + exact micro-augment):
  - Pass C1 (reserve-aware LNS neighborhoods): `40` iterations, `0` accepted gains.
  - Pass C2 (exact augment trials `1->2`, `2->3`, `3->4`, `4->5`): `59132` trials, `0` successful augmentations, `4027` unique motif signatures.
  - Pass C3 (neutral/gain random walk with motif coupling): `26043` moves, `761` neutral accepts, `0` gain accepts.
  - Pass C4 (strict neutral re-pack for balance): `14950` iterations, `1849` accepts; improved point-degree spread while preserving all hard constraints.
- Stage D (residual exact completion gate):
  - Gate not met (`uncovered=4564`, fraction `0.369`) so residual exact completion not attempted.

## Metric trend
| Stage | Blocks | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Oversubscribed `(r-1)` |
|---|---:|---:|---:|---:|---|---|---:|
| Start seed | 1116 | 7812 | 4564 | 0 | gap 24 (`445..469`) | 6 / 6 | 0 |
| Post Stage A/B | 1116 | 7812 | 4564 | 0 | gap 24 (`445..469`) | 6 / 6 | 0 |
| Post C1/C2/C3 | 1116 | 7812 | 4564 | 0 | gap 24 (`445..469`) | 6 / 6 | 0 |
| Final (C4 best) | 1116 | 7812 | 4564 | 0 | gap 19 (`449..468`) | 6 / 6 | 0 |

Additional `(r-1)` pressure-tail metric:
- `5`-subset load `=6` count improved `72 -> 69` at fixed block count.

Uncovered/overcovered trend (best checkpoints):
- `4564/0 -> 4564/0 -> 4564/0 -> 4564/0`.

## Observations
- Symmetry compression remains useful as a diagnostic, but bounded binary-orbit exact search still did not close even with small non-binary share in `C17`.
- Under strict feasibility (`overcovered=0`, `(r-1)` cap respected), additive growth from the current seed is exhausted.
- High-trial exact augmenting neighborhoods were sparse-to-empty this round; however, neutral strict repacks improved degree balance and reduced cap-tail concentration.

## Core advance
- advance statement:
  - Established a reproducible strict-feasible balance-improvement lane for `S(6,7,17)` that improves structural pressure metrics even when block-count augmentations are absent.
- evidence from this round (metrics, runtime, structure):
  - Executed mandatory symmetry-first gate with explicit orbit/coefficient diagnostics and bounded probes before fallback.
  - Ran three augmentation-focused stages (`C1..C3`) totaling `>85k` neighborhood/augmentation attempts without strict block-count gain.
  - Found a strict-feasible improved certificate with unchanged coverage metrics but better balance:
    - point-degree spread `24 -> 19` (`445..469 -> 449..468`),
    - cap-6 `5`-subset count `72 -> 69`,
    - preserved `overcovered=0`, `oversubscribed_(r-1)=0`, `r_minus_1_max_degree=6`.
- transfer value for next rounds:
  - Keep this balanced `1116`-block checkpoint as the default strict-feasible seed (better-conditioned than prior `1116` seed).
  - Treat balance-first neutral repacks as a preparatory phase before expensive exact augmenting scans.

## Next-hypothesis
- hypothesis statement:
  - Two-phase strict-feasible search (`balance-first neutral repack -> motif-coupled exact augment`) will break the `1116` plateau where augment-only scans fail.
- mechanism (why this should help):
  - Reducing point-degree and cap-tail concentration relaxes local `(r-1)` bottlenecks, increasing the chance that `k -> k+1` exact micro-packs become feasible in the same motif neighborhoods.
- expected metric movement:
  - improve `1116 -> 1118..1122` blocks,
  - reduce uncovered by `14..42`,
  - keep `overcovered=0`, `oversubscribed_(r-1)=0`, `r_minus_1_max_degree <= 6`,
  - keep point-degree gap `<= 20`.
- falsification / stop condition:
  - reject this hypothesis if, after `>=80,000` motif-coupled exact augment trials from a balanced seed (gap `<=20`), net gain remains `< +1` block and cap-6 `5`-subset count does not fall below `60`.
