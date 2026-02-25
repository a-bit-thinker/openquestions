# Steiner Knowledge Cache

Run ID: 20260222_012007
Updated (UTC): 2026-02-22T02:10:00Z

## Round Scope
- Mode: research-only (no certificate construction in this round).
- Target instance: `S(6,7,23)`.
- Expected block count: `14421`.
- Local-first status: completed (cross-run memory and local paper notes read before any external search).
- New external links added this round: `0` (reused cached links only).

## Hard Admissibility/Divisibility Gate
- Instance parameters: `n=23`, `q=7`, `r=6`.
- Integrality checks all pass for `i=0..5`.
- Replication numbers: `lambda_0=14421`, `lambda_1=4389`, `lambda_2=1197`, `lambda_3=285`, `lambda_4=57`, `lambda_5=9`.
- Gate decision: admissible and well-formed; heavy search is allowed.

## Proof-First Round1 Stack

### Seeded proof ideas with solve-attempts
| Seed | High-level proof idea | Solve-attempt in this round | Critical gap |
|---|---|---|---|
| A | Keevash-style existence skeleton (divisibility -> approximate decomposition -> absorption) | Mapped to an execution skeleton for `S(6,7,23)` with explicit admissibility and residual-closure obligations | Asymptotic threshold is not instantiated at `n=23`; requires finite-size bridge argument |
| B | Wilson/PBD bridge for finite-size handling | Framed as a finite-size reduction route when asymptotic constants are unclear | Concrete decomposition schedule for this instance is still missing |
| C | Symmetry-compressed Kramer-Mesner with weighted-orbit fallback | Defined as bounded front gate (cyclic/dihedral probes) with weighted fallback if non-binary coefficients appear | Need practical threshold for "too non-binary" before hard switching |
| D | Random nibble with pressure-aware potential descent | Defined potential-guided handoff rule from additive growth to repair (`(r-1)` pressure aware) | Need calibrated trigger values tied to observed acceptance rates |
| E | Absorber + motif-coupled local trades | Converted prior sparse-gain micro-augment results into a formal late-stage closure lane | Need explicit absorber template compatible with `r=6`, `q=7`, `n=23` |

### Critical-gap verification loop (max 3 rounds)
1. Loop 1: arithmetic and invariant loop
- Verify divisibility, expected block count, and `lambda_i` consistency.
- Status: pass.
2. Loop 2: engine-feasibility loop
- Run bounded symmetry diagnostics; if weak compression or non-binary inflation appears, force early switch to randomized pipeline.
- Status: specified with decision thresholds; to execute in round 2.
3. Loop 3: closure loop
- Require `overcovered=0`, no oversubscribed `(r-1)` subsets, and sufficiently small uncovered residual before residual exact-cover.
- Status: proof obligation defined; numerical threshold to be tuned from first pilot run.

### Typeset-ready final proof outline (blueprint)
1. Proposition (Admissibility): `S(6,7,23)` satisfies all necessary divisibility constraints.
2. Lemma (Engine dichotomy): either orbit compression is strong enough for symmetry-compressed exact-cover, or bounded diagnostics certify early fallback to randomized construction.
3. Lemma (Monotone repair potential): under strict feasibility (`overcovered=0`, no `(r-1)` oversubscription), accepted repair steps do not increase cap pressure tails and improve covered mass in expectation.
4. Lemma (Absorber/residual closure gate): once uncovered residual and pressure tails are below threshold, a micro exact-cover phase is tractable on the residual.
5. Theorem schema (operational): combining 1-4 yields a finite, falsifiable construction protocol for this instance; either an exact design is produced or a bounded obstruction report is emitted at a named gate.

## Strong Search Stack (Mandatory)
1. Hard admissibility/divisibility gate.
- Recompute all `lambda_i` and target block count first.
- Abort search immediately if any integrality check fails.
2. Symmetry/Kramer-Mesner exact-cover mode (bounded front gate).
- Run short cyclic/dihedral orbit diagnostics and coefficient histogram.
- Keep this lane only with strong orbit compression and mostly binary coefficients.
3. General randomized mode.
- `nibble -> boosting/repair -> absorber -> residual exact-cover`.
- Residual exact-cover is a late microphase only.

## Engine-Selector Rubric (Concise)
- Use symmetry/orbit compression when orbit count drops strongly (about `>=10x`), non-binary coefficients are rare, and bounded probes show quick progress.
- Use generalized randomized construction when compression is weak, non-binary coefficients are material, or `(r-1)` pressure plateaus appear early.

## Practice Blockers -> Research Deltas
1. Blocker: binary-only symmetry probes stall once non-binary orbit coefficients appear.
- Source: Kramer-Mesner formulation (cached).
- Change: add weighted-orbit micro-ILP fallback immediately after bounded binary probe failure.
2. Blocker: add-only growth plateaus at saturated `(r-1)` motifs.
- Source: iterative absorption pipeline (cached).
- Change: enforce pressure-triggered handoff from nibble/add-only stage to motif-targeted destroy/repack.
3. Blocker: micro-augment gains are sparse and duplicate neighborhoods waste budget.
- Source: symmetry-aware canonicalization guidance from prior cache.
- Change: canonical motif signatures and taboo windows before local exact repair.

## Source Notes (reused cached links)
1. https://arxiv.org/abs/1401.3665
- Takeaway: divisibility is a non-negotiable existence gate.
- Strategy change: keep admissibility as an unconditional pre-search gate.
2. https://arxiv.org/abs/1611.06827
- Takeaway: iterative absorption supports staged construction.
- Strategy change: keep `nibble -> boosting/repair -> absorber -> residual exact-cover` as default non-symmetry pipeline.
3. https://www.sciencedirect.com/science/article/pii/0097316586900944
- Takeaway: orbit systems can be non-binary under automorphisms.
- Strategy change: do not persist with binary-only exact-cover when coefficient inflation is detected.

## Reuse vs Genuinely New
- Reused from prior runs:
  - hard admissibility gate,
  - short symmetry front gate then quick fallback,
  - strict feasibility invariants (`overcovered=0`, no `(r-1)` oversubscription).
- Genuinely new in this round:
  - five-seed proof-first stack for `S(6,7,23)` with per-seed gap labels,
  - three-loop critical-gap verification contract,
  - typeset-ready theorem/lemma blueprint tied to solver gates,
  - explicit finite-size caution (`n=23`) in the proof skeleton.

## Incremental Additions (Round2 Solve, 2026-02-22)
- Admissibility gate was rechecked before solve; still pass.
- Symmetry diagnostics executed first (mandatory gate):
  - `C23`: `|O_6|=4389`, `|O_7|=10659`, binary/non-binary columns `10648/11`, `max_coeff=2`.
  - `D23`: `|O_6|=2277`, `|O_7|=5412`, binary/non-binary columns `5247/165`, `max_coeff=2`.
- Symmetry quality check:
  - Cyclic packed trial gave a strict-feasible but weaker candidate (`7912` blocks, `score=36.81`, `uncovered=45563`, `overcovered=0`).
  - Decision: symmetry lane is tractable but not quality-competitive in this budget; fallback to randomized/LNS lane.
- Add-only strict boosting from incumbent seed is exhausted at `9237` blocks.
- LNS destroy/repack progression (strict-feasible throughout):
  - `9237 -> 9249 -> 9259 -> 9280` blocks,
  - `uncovered 36288 -> 35987`,
  - `score 49.67 -> 50.09`,
  - `overcovered=0`, `oversubscribed_(r-1)=0` preserved.
- New practical takeaway for this instance:
  - Larger LNS windows (`k` up to ~16) produce higher gain frequency than small-window passes once add-only is exhausted.

## Incremental Additions (Round3 Solve, 2026-02-22)
- Target instance: `S(7,8,20)` (`expected_blocks=9690`).
- Admissibility gate was rechecked before solve; pass.
- Symmetry diagnostics executed first (mandatory gate):
  - `C20`: `|O_7|=3876`, `|O_8|=6310`, binary/non-binary columns `6276/34`, `max_coeff=4`.
  - `D20`: `|O_7|=1980`, `|O_8|=3260`, binary/non-binary columns `3042/218`, `max_coeff=8`.
- Symmetry quality check:
  - Best bounded cyclic orbit-packed trial: `4635` blocks, `score=26.97`, `uncovered=40440`, `overcovered=0`.
  - Decision: symmetry lane is diagnosable but weaker than generalized strict pipeline in this budget.
- General pipeline progression:
  - Round-start strict candidate: `5551` blocks (`score=40.20`, `uncovered=33112`, `overcovered=0`).
  - Stage-B seed sweep best: `5634` blocks (`score=41.40`, `uncovered=32448`, `overcovered=0`).
  - Add-only strict scan at `5634`: `0` feasible additions.
  - Stage-C motif-coupled LNS (`k=1..3`, strict row-owner + `(r-1)` cap gate): `5634 -> 5807` blocks over `35000` trials (`170` accepted gains), `uncovered 32448 -> 31064`, `score 41.40 -> 43.90`, `overcovered=0` preserved.
- Residual exact-cover gate:
  - `ineligible` (`uncovered=31064` exceeds residual budget), despite strict feasibility.
- New practical takeaway for this instance:
  - Uncovered-owner-signature remove proposals plus exact local `k -> k+1` refill produce reliable strict gains after add-only exhaustion while improving degree balance (`point_gap 361 -> 242`).

## Incremental Additions (Round4 Solve, 2026-02-22)
- Target instance: `S(8,9,21)` (`expected_blocks=22610`).
- Admissibility gate was rechecked before solve; pass.
- Symmetry diagnostics executed first (mandatory gate):
  - `C21`: `|O_8|=9690`, `|O_9|=14000`, binary/non-binary columns `13983/17`, `max_coeff=3`.
  - `D21`: `|O_8|=4950`, `|O_9|=7105`, binary/non-binary columns `6891/214`, `max_coeff=6`.
- Symmetry quality check:
  - Best bounded cyclic orbit-packed trial: `9793` blocks, `score=20.64`, `uncovered=115353`, `overcovered=0`.
  - Decision: symmetry lane is tractable/diagnosable but quality-inferior in this budget; fallback to strict generalized pipeline.
- General pipeline progression:
  - Round-start strict candidate: `12107` blocks (`score=34.97`, `uncovered=94527`, `overcovered=0`).
  - Reserve-first additive stage: reserved `904` block slots; add-only strict scans found `0` accepted additions (plateau confirmed).
  - LNS destroy/repack (strict, larger windows) over 3 passes:
    - `12107 -> 12121 -> 12133 -> 12138` blocks,
    - `uncovered 94527 -> 94401 -> 94293 -> 94248`,
    - `score 34.97 -> 35.05 -> 35.13 -> 35.16`,
    - `overcovered=0`, `oversubscribed_(r-1)=0` preserved throughout.
- Residual exact-cover gate:
  - `ineligible` (`uncovered=94248` too large; fraction `0.4634`), despite strict feasibility.
- New practical takeaway for this instance:
  - Add-only growth is exhausted early at this frontier; monotone gains come from sparse motif-coupled LNS windows.
  - Larger windows (`k` up to low double digits) remain useful but have sparse acceptance, so coupling and bounded reuse around capped `7`-subset motifs is preferable to uncoupled broad random windows.

## Incremental Additions (Round5 Solve, 2026-02-22)
- Target instance: `S(9,10,22)` (`expected_blocks=49742`).
- Admissibility gate was rechecked before solve; pass.
- Symmetry diagnostics executed first (mandatory gate):
  - `C22`: `|O_9|=22610`, `|O_10|=29414`, binary/non-binary columns `29366/48`, `max_coeff=2`.
  - `D22`: `|O_9|=11410`, `|O_10|=14938`, binary/non-binary columns `14460/478`, `max_coeff=4`.
- Symmetry quality check:
  - Bounded cyclic orbit-packed probe produced a strong strict seed (`23716` blocks, `score=26.75`, `uncovered=260260`, `overcovered=0`, `oversubscribed_(r-1)=0`).
  - Decision: symmetry lane is tractable and quality-competitive here; keep symmetry seed and continue with strict constructive refinement.
- General strict pipeline progression (from symmetry seed):
  - Stage-B strict add-only: `23716 -> 23738` (`+22` accepted adds over `500000` attempts), `uncovered 260260 -> 260040`, `overcovered=0` preserved.
  - Stage-C strict LNS (`k=2..7`, local `k -> k+1`): `23738 -> 23752`, `uncovered 260040 -> 259900`, `score 26.81 -> 26.85`, `overcovered=0` and `oversubscribed_(r-1)=0` preserved.
- Final strict candidate metrics:
  - `blocks=23752`, `score=26.85`, `exact_once=237520`, `uncovered=259900`, `overcovered=0`.
  - `point_gap=6` (`10793..10799`), `r_minus_1_max_degree=7` (target `7`).
- Residual exact-cover gate:
  - `ineligible` (uncovered fraction `0.5225` too large), despite strict feasibility.
- New practical takeaway for this instance:
  - Unlike recent `r=8,9` cases where symmetry was mostly diagnostic, `S(9,10,22)` benefits from a symmetry-first strict scaffold as the primary seed; strict LNS then provides sparse monotone gains.
