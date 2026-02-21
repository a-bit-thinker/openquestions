# Round 5 Notes

Instance: S(9,10,20)
Expected blocks: 16796

## Admissibility gate snapshot
```json
{
  "instance": {"n": 20, "q": 10, "r": 9},
  "is_admissible": true,
  "divisibility_failures": [],
  "expected_block_count": 16796,
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
- Read `steiner_logs/run_20260220_183105/KNOWLEDGE_CACHE.md` before search.
- No new web source used in this round (targeted searches used: 0/1).

## Plan
- Stage A: run symmetry/orbit compression front gate (cyclic + dihedral) and only keep it if tractable.
- Stage B: run general pipeline (nibble/additive boost -> reserve-aware repair).
- Stage C: run absorber/flex LNS destroy/repack with strict move gates.
- Stage D: attempt residual exact completion only if residual is small and overcoverage is zero.

## Work log
- Enforced strict admissibility gate before any search.
- Stage A (symmetry/orbit compression diagnostics):
  - Cyclic `Z_20`: `|O_9|=8398`, `|O_10|=9252`; binary columns `9215`, non-binary columns `37`, max orbit coefficient `10`.
  - Cyclic bounded binary-only DFS (`20s`, `200k` nodes): `nodes=8`, `solved=false`.
  - Dihedral `D_20`: `|O_9|=4262`, `|O_10|=4752`; binary columns `4488`, non-binary columns `264`, max orbit coefficient `10`.
  - Dihedral bounded binary-only DFS (`20s`, `200k` nodes): `nodes=113`, `solved=false`.
  - Decision: symmetry lane not tractable for strict binary exact-cover in this budget; switched to general pipeline.
- Stage B (nibble/additive boost from strict-feasible seed):
  - Start seed (from current candidate): `5897` blocks, `uncovered=108990`, `overcovered=0`, `(r-1)` oversubscription `=0`.
  - Multi-seed additive boosting gave best strict-feasible checkpoint at `7693` blocks (`uncovered=91030`).
- Stage C (absorber/flex LNS, multi-pass):
  - Repeated destroy/repack passes with `k in [24,72]`.
  - Reserve-first refill enforced each neighborhood: `reserve = max(4, k//7)` before flex completion.
  - Hard move gates always enforced:
    - unique 9-subset ownership (`overcovered_r_subsets` stays `0`),
    - 8-subset load cap `<= lambda_8 = 6` (`oversubscribed_r_minus_1_subsets` stays `0`).
  - Pass checkpoints:
    - pass1: `7866` blocks (`uncovered=89300`)
    - pass2: `7934` blocks (`uncovered=88620`)
    - pass3: `8019` blocks (`uncovered=87770`)
    - pass4: `8070` blocks (`uncovered=87260`)
    - pass5: `8120` blocks (`uncovered=86760`)
- Stage D (residual exact completion gate):
  - Final `overcovered=0`, but uncovered fraction `86760 / 167960 = 0.5166`.
  - Residual is not small; exact residual completion not attempted.

## Observations
- Symmetry compression did reduce dimensions, but non-binary orbit coefficients (up to `10`) block strict `A x = 1` binary exact-cover use.
- For this instance, additive-only growth plateaus quickly; repeated LNS passes continue to make steady net gains.
- Reserve-then-flex refill was important for avoiding greedy overfill and preserving neighborhood repair capacity.
- Strict feasibility remained invariant at every best checkpoint:
  - `overcovered_r_subsets = 0`
  - `oversubscribed_r_minus_1_subsets = 0`
  - `r_minus_1_max_degree = 6` with target `lambda_8 = 6`.

## Metric trend
| Stage | Blocks | Exact-once | Uncovered | Overcovered | Point degree spread | `(r-1)` max / target | Oversubscribed `(r-1)` |
|---|---:|---:|---:|---:|---|---|---:|
| Start seed | 5897 | 58970 | 108990 | 0 | gap 1511 | 6 / 6 | 0 |
| Additive best | 7693 | 76930 | 91030 | 0 | gap 579 | 6 / 6 | 0 |
| Pass 1 | 7866 | 78660 | 89300 | 0 | gap 415 (`3740..4155`) | 6 / 6 | 0 |
| Pass 2 | 7934 | 79340 | 88620 | 0 | gap 345 (`3797..4142`) | 6 / 6 | 0 |
| Pass 3 | 8019 | 80190 | 87770 | 0 | gap 302 (`3855..4157`) | 6 / 6 | 0 |
| Pass 4 | 8070 | 80700 | 87260 | 0 | gap 281 (`3895..4176`) | 6 / 6 | 0 |
| Final (Pass 5) | 8120 | 81200 | 86760 | 0 | gap 251 (`3922..4173`) | 6 / 6 | 0 |

Uncovered/overcovered trend (best checkpoints):
- `108990/0 -> 91030/0 -> 89300/0 -> 88620/0 -> 87770/0 -> 87260/0 -> 86760/0`.

## Core advance
- advance statement:
  - Established a reproducible strict-feasible improvement loop for `S(9,10,20)` that combines a symmetry front gate with reserve-aware multi-pass LNS and yields monotone best-checkpoint progress.
- evidence from this round (metrics, runtime, structure):
  - Symmetry lane was evaluated first with explicit orbit/multiplicity diagnostics and bounded DFS before fallback.
  - Candidate improved from `5897` to `8120` blocks (`+2223`) while preserving `overcovered=0` and `(r-1)` oversubscription `=0`.
  - Uncovered reduced by `22230` (`108990 -> 86760`); point-degree gap reduced by `1260` (`1511 -> 251`).
- transfer value for next rounds:
  - Keep symmetry diagnostics as mandatory front gate, then switch quickly when non-binary orbit coefficients dominate.
  - Keep reserve-then-flex refill order and strict hard gates in every neighborhood.
  - Use repeated LNS passes; single-pass improvement leaves significant recoverable slack.

## Next-hypothesis
- hypothesis statement:
  - 8-subset motif-targeted destroy selection plus two-tier refill (local exact micro-pack + global flex) will outperform the current pressure-only remove scoring.
- mechanism (why this should help):
  - Current plateaus are driven by dense clusters of 8-subsets already at load `5/6`; explicitly targeting those motifs should free larger compatible local repack opportunities before global fill.
- expected metric movement:
  - Improve from `8120` to `8180..8280` blocks,
  - reduce uncovered by `600..1600`,
  - keep `overcovered=0`, `oversubscribed_(r-1)=0`, `r_minus_1_max_degree <= 6`.
- falsification / stop condition:
  - Stop this hypothesis if, after `>=400` accepted LNS neighborhoods, net gain is `< +20` blocks or if local exact micro-pack succeeds in `<15%` of neighborhoods.

## Rounds 1-5 Synthesis
### Strongest advances by round
1. Round 1: established the hard admissibility/divisibility gate and the dual-engine policy (symmetry-first, then randomized/absorption pipeline).
2. Round 2: first working strict-feasible LNS recipe (`S(6,7,17)`), proving monotone gains with `overcovered=0` and `(r-1)` cap respected.
3. Round 3: confirmed symmetry-first + absorber-reserved LNS transferability to `S(7,8,18)`.
4. Round 4: demonstrated plateau-crossing behavior on `S(8,9,19)` with neutral/annealed acceptance while preserving hard invariants.
5. Round 5: extended the same strict-feasible strategy to `S(9,10,20)` and achieved `5897 -> 8120` blocks with zero overcoverage and zero `(r-1)` oversubscription.

### Failed directions and why they failed
1. Binary-only global orbit exact-cover on `r=9`: failed because non-binary orbit coefficients are substantial (`max_coeff=10`), so strict binary `A x = 1` is structurally mismatched.
2. One-shot additive boosting as a final strategy: stalls at local maxima (no feasible additions remain), leaving LNS-only improvement headroom.
3. Purely random/global destroy neighborhoods: underperform motif-aware neighborhoods because they do not reliably release saturated `(r-1)` pressure clusters.

### Top 3 next hypotheses with round-6 test protocol
1. Hypothesis: motif-targeted destroy on 8-subsets with load `5/6` plus local exact micro-pack improves block gain per accepted move.
Test protocol: run `3` seeds, `>=500` accepted neighborhoods each, compare `delta blocks / 100 accepted moves` against current baseline.
2. Hypothesis: mixed neighborhood sizes (`k` schedule alternating small and large windows) reduces plateau recurrence.
Test protocol: evaluate schedules `{24-48}`, `{48-72}`, `{24-72}` on identical seeds and compare final uncovered with hard gates fixed.
3. Hypothesis: selective orbit-aware refill (prefer candidates from binary orbit columns) improves compatibility under strict gates.
Test protocol: inject orbit-aware candidates into `30%` of refill samples and A/B against current refill policy over equal compute budgets.
