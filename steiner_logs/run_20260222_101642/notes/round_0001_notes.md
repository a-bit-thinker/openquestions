# Round 1 Notes (Research-Only)

Instance: `S(6,7,19)`
Expected blocks: `3876`
Date (UTC): `2026-02-22`

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: steiner_logs/run_20260222_101642/REPO_WIDE_HISTORY.md
- Global research log (all runs round1): steiner_logs/RESEARCH_LOG.md
- Global practice log (all runs round2-5): steiner_logs/PRACTICE_LOG.md
- Global research paper (paper-style synthesis): steiner_logs/RESEARCH_PAPER.md
- Existence frontier report (all admissible triples): steiner_logs/EXISTENCE_FRONTIER.md
- Local paper notes: steiner_logs/PAPER_NOTES.md
- Primary local roadmap PDF: /root/openquestions/papers/Computational and Theoretical Roadmap for Steiner Systems with Strength 6–9 and n _ 200.pdf
- Latest prior run: run_20260222_052536
- Latest prior round1 notes source run: run_20260222_052536
- Latest prior round1 notes: steiner_logs/run_20260222_052536/notes/round_0001_notes.md
- Latest prior round5 notes source run: run_20260222_052536
- Latest prior round5 notes: steiner_logs/run_20260222_052536/notes/round_0005_notes.md
- Latest prior transfer: steiner_logs/run_20260222_052536/NEXT_GENERATION_TRANSFER.md

## Admissibility gate snapshot
```json
{
  "checks": [
    {
      "denominator": 7,
      "i": 0,
      "numerator": 27132,
      "quotient": 3876,
      "remainder": 0
    },
    {
      "denominator": 6,
      "i": 1,
      "numerator": 8568,
      "quotient": 1428,
      "remainder": 0
    },
    {
      "denominator": 5,
      "i": 2,
      "numerator": 2380,
      "quotient": 476,
      "remainder": 0
    },
    {
      "denominator": 4,
      "i": 3,
      "numerator": 560,
      "quotient": 140,
      "remainder": 0
    },
    {
      "denominator": 3,
      "i": 4,
      "numerator": 105,
      "quotient": 35,
      "remainder": 0
    },
    {
      "denominator": 2,
      "i": 5,
      "numerator": 14,
      "quotient": 7,
      "remainder": 0
    }
  ],
  "divisibility_failures": [],
  "expected_block_count": 3876,
  "instance": {
    "n": 19,
    "q": 7,
    "r": 6
  },
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 3876,
    "lambda_1": 1428,
    "lambda_2": 476,
    "lambda_3": 140,
    "lambda_4": 35,
    "lambda_5": 7
  }
}
```

## Immediate nonexistence triage (high signal)
The local roadmap PDF claims a *proven* nonexistence result `S(4,5,17) ≁ exists` and highlights
**derivation veto** as a propagation rule: if `S(r,q,n)` exists then the derived design `S(r-1,q-1,n-1)` exists.

If the roadmap’s base claim is correct, then `S(6,7,19)` is eliminated by repeated derivation:
`S(6,7,19) -> S(5,6,18) -> S(4,5,17)` (two derivations).

Status for this run: treat as **provisional until primary-source verification** of `S(4,5,17)` nonexistence,
but it should be enforced as a **pre-solve gate** to avoid chasing impossible instances.

## Proof-first round1 stack (mandatory)

### Seed 1: nonexistence via derivation veto (roadmap)
- High-level proof idea: propagate a known nonexistence upward along `q=r+1` by repeated derivation.
- Solve-attempt (this round): conditional proof sketch:
  - Assume `S(6,7,19)` exists.
  - Derive once (fix point `x`): obtain `S(5,6,18)`.
  - Derive again (fix point `y`): obtain `S(4,5,17)`.
  - If `S(4,5,17)` is known not to exist, contradiction.
- Critical gap: confirm the base nonexistence fact from the primary reference (roadmap cites Östergård–Pottonen).

### Seed 2: arithmetic gate + stronger necessary sieves beyond divisibility (roadmap)
- High-level proof idea: divisibility is necessary but weak at small `n`; add cheap sieves (derivation veto,
  classical lower bounds, and “known small nonexistences” tables) before any solver spend.
- Solve-attempt (this round): turned roadmap’s sieve list into an execution contract:
  - Gate 0: divisibility witness table (already passes).
  - Gate 1: derivation-veto lookup across a maintained “known nonexistences” seed list.
  - Gate 2 (optional): quick lower-bound checks (Ray–Chaudhuri–Wilson, Tits, Cameron) to flag hopeless tiny cases.
- Critical gap: repo currently encodes only divisibility; it does not yet encode a maintained nonexistence list.

### Seed 3: symmetry/Kramer–Mesner compressed lane (roadmap)
- High-level proof idea: if orbit compression is strong under some group `G <= S_n`, solve `Ax=1` on orbit variables
  (KM method), which can be proof-relevant (existence/nonexistence with prescribed symmetry) and compute-relevant.
- Solve-attempt (this round): drafted a bounded symmetry triage:
  - Choose `G` from a small menu (cyclic/dihedral/transitive small groups).
  - Measure orbit counts for `r`- and `q`-subsets; record compression ratio.
  - If compression is large: build orbit-incidence matrix `A` and solve `Ax=1` via SAT/ILP/DLX on orbit variables.
  - Else: fall back immediately to non-symmetry engines.
- Critical gap: repo lacks an orbit generator / KM matrix builder; integration design is needed (e.g., GAP/PAG wrapper).

### Seed 4: direct exact-cover feasibility / UNSAT lane (roadmap + existing exact-cover module)
- High-level proof idea: for smallish instances, model as exact cover with rows `C(n,r)` and columns `C(n,q)` and use DLX;
  in nonexistence cases, exhaustive search can provide an UNSAT proof transcript (or at least strong evidence).
- Solve-attempt (this round): feasibility-size sanity:
  - Rows `= C(19,6)=27132`, cols `= C(19,7)=50388`.
  - Row degree `= C(19-6,7-6)=C(13,1)=13`, column degree `= C(7,6)=7`.
  - Total incidences `= 27132*13 = 352716` (memory-feasible).
- Critical gap: (i) compute budget for full UNSAT search may be large; (ii) if using symmetry, need orbit reduction first.

### Seed 5: nibble -> boosting/repair -> absorber -> residual exact-cover (Keevash + iterative absorption)
- High-level proof idea: treat construction as staged: cover most constraints quickly (nibble/greedy), then repair/absorb,
  then exact-solve only a small residual.
- Solve-attempt (this round): aligned staged language with repo practice gates:
  - Keep strict feasibility invariants when searching partial packings (`overcovered=0`, no `(r-1)` oversubscription).
  - Use pressure-triggered handoff from add-only to destroy/repack neighborhoods once acceptance decays.
  - Only attempt residual exact-cover when uncovered is below explicit eligibility thresholds.
- Critical gap: for `n=19` the direct exact-cover lane may dominate; for larger instances, absorber templates are not yet encoded.

## Critical-gap verification loop (up to 3 rounds)
1. Verification round A (arithmetic + derivation-veto gate)
- Check: divisibility table + derived-nonexistence propagation.
- Status: divisibility passes; derivation-veto nonexistence is **provisional** pending primary-source verification of `S(4,5,17)`.
- Stop rule: if a verified nonexistence chain applies, abort solve rounds and pivot instance selection.

2. Verification round B (engine compatibility)
- Check: symmetry compression diagnostics (orbit counts, non-binary coefficients if KM built) versus raw exact-cover size.
- Status: raw exact-cover size for `S(6,7,19)` is feasible; KM is optional unless seeking symmetry-certified UNSAT/existence.
- Stop/switch rule: if orbit compression is weak, do not spend on KM; run DLX/SAT/ILP directly or pivot to larger frontier.

3. Verification round C (closure eligibility discipline)
- Check: residual exact-cover gate is only meaningful once uncovered mass is small; otherwise prefer constructive repair/absorption.
- Status: practice-log evidence shows “early residual exact-cover” is consistently wasteful at large residual ratios.
- Stop/switch rule: enforce residual eligibility thresholds before activating residual exact-cover on large instances.

## Typeset-ready final proof outline (conditional nonexistence)
**Theorem (conditional)**. If there is no Steiner system `S(4,5,17)`, then there is no Steiner system `S(6,7,19)`.

**Proof sketch**. Assume for contradiction that a Steiner system `S(6,7,19)` exists on point set `[19]`. Fix a point `x`.
Derive at `x` (delete `x` from every block containing `x`) to obtain a Steiner system `S(5,6,18)`. Fix a point `y` in the
derived system and derive again to obtain `S(4,5,17)`. This contradicts the assumed nonexistence of `S(4,5,17)`. ∎

**Corollary (portfolio gate)**. If `S(4,5,17)` nonexistence is verified, then every `S(t,t+1,t+13)` (hence `(6,7,19)`,
`(7,8,20)`, `(8,9,21)`, `(9,10,22)` in this repo’s portfolio band) is eliminated by derivation veto.

## Strong search stack (mandatory)

### Hard gates (always first)
1. Divisibility/admissibility: compute the witness table for `i=0..r-1` and stop on first nonzero remainder.
2. Derivation veto: maintain a small seed list of verified nonexistences, and propagate upward by repeated derivation.
3. Residual eligibility: do not launch residual exact-cover unless uncovered mass is below explicit thresholds.

### Symmetry/Kramer–Mesner exact-cover mode
1. Pick candidate group `G` (start with cyclic `C_n`, then dihedral, then small transitive groups).
2. Compute orbits of `G` on `r`-subsets and `q`-subsets; assemble orbit-incidence `A`.
3. Solve `Ax=1` over `x in {0,1}` using SAT/ILP/DLX on orbit variables.
4. If binary KM stalls, switch to weighted-orbit / relaxed feasibility rather than extending binary-only budget.

### Randomized construction mode (iterative absorption-inspired)
1. Nibble/greedy bulk: build a large partial packing quickly.
2. Boosting/repair: keep strict caps; use pressure-triggered handoff from add-only to destroy/repack.
3. Absorber reserve: reserve flexibility early to avoid irreversible `(r-1)` saturation.
4. Residual exact-cover: only when the uncovered set is small enough to build/solve.

## Engine-selector rubric (concise)
- Symmetry/orbit compression is plausible when orbit counts are tiny relative to raw rows/cols (orders-of-magnitude reduction),
  and KM coefficients remain mostly binary/low-weight under a chosen `G`.
- General randomized construction is better when compression is weak, KM non-binary mass is high, or when strict add-only
  progress shows early `(r-1)` pressure saturation (then switch to destroy/repack + absorber discipline).

## Paper-to-loop method extraction (mandatory, all local PDFs)
| Source PDF | Theorem/Mechanism (explicit) | Code Delta Mapping (file:path + action) | Validation Metric |
|---|---|---|---|
| roadmap | Workflow mechanism: derivation-veto nonexistence propagation (`S(4,5,17)` blocks `S(t,t+1,t+13)`) with repeated derivation chain checks. | update `math_proofs/steiner_portfolio.py` to add derived-nonexistence veto before ranking; modify `math_proofs/steiner_system.py` to emit `nonexistence_veto` witness chains. | % of portfolio candidates vetoed; #solve rounds avoided; correctness: vetoed instance later solved => reject |
| roadmap | Workflow mechanism: Kramer orbit reduction (`Ax=1` on orbit-incidence) with SAT/ILP/DLX routing after compression metrics. | add `math_proofs/steiner_kramer_mesner.py` for orbit enumeration and KM matrix building; update `math_proofs/steiner_exact_cover.py` to accept orbit variables and route by compression ratio. | Compression ratio (`|O_q|/C(n,q)`), KM matrix nnz, solver runtime/nodes |
| arxiv_1401.3665 | Theorem mechanism: randomized-algebraic template, spill repair, robust fractional extendability, and absorber closure phase. | update `math_proofs/steiner_exact_cover.py` to add template-seed -> greedy-cover -> spill-fix stages; modify `steiner_logs/RESEARCH_PAPER.md` to log spill size and local-fix counters. | Spill size, uncovered slope, local-fix success rate per 1k moves |
| arxiv_1611.06827 | Workflow mechanism: vortex levels, cover down lemma, transformer/absorber transitions, and regularity boosting phase before closure. | modify `run_steiner_loop.sh` to enforce vortex stage order; add `math_proofs/steiner_exact_cover.py` cover-down micro-solver hooks; update `STEINER_LOOP_LOGGING.md` with per-level residual tracking. | Leftover mass per vortex level; acceptance rate of cover-down packs; strict violations (must be 0) |
| oai_first_proof | Protocol mechanism: seed ideas fanout, repeat up to 3 verify loops, explicit gaps checks, solution refinement, and typeset-ready closure. | update `run_steiner_loop.sh` to enforce 5-seed generation and <=3 verify loops; modify `steiner_logs/RESEARCH_PAPER.md` to require gap-check checklists; update `README.md` close criteria for typeset-ready artifact. | #seeds explored; % verification passes; reduction in repeated round1 essay content |

## External references used (minimal)
- New links introduced in this round: `0`.
- Reused cached external links: `0` (local PDFs used instead).
- New PDFs saved under `/root/openquestions/papers`: `none`.

## Practice-log failures -> research deltas (mandatory)
1. Blocker: portfolio chooses divisibility-admissible but *derivation-veto eliminated* instances (wasted solve rounds).
- Source likely to address it: roadmap (derivation veto + small nonexistence results).
- Concrete implementation change: add a verified nonexistence seed list + repeated-derivation veto in `math_proofs/steiner_portfolio.py`.

2. Blocker: add-only strict growth plateaus once `(r-1)` faces saturate (pressure tail hardens).
- Source likely to address it: iterative absorption framing (vortex/cover-down/absorbers).
- Concrete implementation change: pressure-triggered switch from add-only to motif-coupled destroy/repack + absorber reserve.

3. Blocker: binary-only symmetry probes stall under non-binary orbit coefficients.
- Source likely to address it: roadmap’s KM workflow + weighted-orbit solver suggestion.
- Concrete implementation change: after bounded binary KM, fall back to weighted-orbit ILP neighborhoods rather than extending binary budget.

4. Blocker: residual exact-cover invoked too early wastes runtime with no frontier movement.
- Source likely to address it: Keevash staging (template/spill/absorb) + repo practice evidence.
- Concrete implementation change: enforce uncovered-count/ratio eligibility gates before building residual exact-cover instances.

5. Blocker: repeated motif neighborhoods produce duplicate low-yield local attempts.
- Source likely to address it: cross-run strict LNS observations in `steiner_logs/PRACTICE_LOG.md`.
- Concrete implementation change: canonical motif signatures + short taboo cache for recently failed neighborhoods.

## Reuse vs genuinely new (explicit)
- Reused from prior runs:
  - hard divisibility gate before expensive search,
  - staged “symmetry triage -> repair/absorb -> residual gate” architecture,
  - strict feasibility invariants as transfer backbone,
  - falsification/stop-condition discipline from `steiner_logs/PRACTICE_LOG.md`.
- Genuinely new in this round:
  - roadmap-driven **derivation-veto nonexistence triage** specialized to the `q=r+1` line (eliminates `S(6,7,19)` if base fact verified),
  - filled “paper-to-loop” transfer table with concrete code-delta mappings,
  - an explicit conditional nonexistence proof outline suitable for typesetting.

## Plan
Round mode is research-only. Next rounds should:
1. Verify/encode roadmap nonexistence seed facts (`S(4,5,17)`, `S(5,6,16)` if confirmed) and propagate by derivation.
2. Re-run portfolio selection excluding vetoed triples; likely next targets start at `S(6,7,23)`, `S(7,8,24)`, `S(8,9,25)`, `S(9,10,26)`.
3. Execute the hybrid engine protocol only on instances that pass both divisibility and derivation-veto gates.

## Work log
- Completed mandatory cross-run reads before any external lookup.
- Read the local roadmap PDF and extracted concrete gates/mechanisms (derivation veto; KM orbit reduction; exact-cover size metrics).
- Converted these into a proof-first stack, strong search stack, engine-selector rubric, and blocker-driven code deltas.

## Observations
- Divisibility alone is an insufficient selector in `n<200`; derivation-veto propagation can eliminate apparently admissible “portfolio picks.”
- For `S(6,7,19)`, the raw exact-cover instance is small enough to attempt direct DLX/SAT if we need an independent check,
  but the first priority is verifying the base nonexistence fact behind the derivation veto.

## Core advance
- advance statement:
-   - Added a nonexistence-aware front gate (derivation veto) and rewrote round1 as a proof-first stack for `S(6,7,19)`.
- evidence from this round (metrics, runtime, structure):
-   - Incorporated roadmap mechanisms (derivation veto; KM; size metrics) into an explicit pipeline and code-delta table.
-   - Mapped practice blockers to concrete implementation changes (portfolio veto, pressure-triggered handoff, weighted-orbit fallback).
- transfer value for next rounds:
-   - Future rounds can avoid wasted solve cycles on derivation-veto eliminated triples and pivot to the smallest *not eliminated* frontier.

## Next-hypothesis
- hypothesis statement:
  - Adding a verified derivation-veto nonexistence gate before portfolio selection will measurably increase “useful solve yield per compute”
    by avoiding impossible triples, while preserving the existing hybrid engine benefits on the remaining unknown set.
- mechanism (why this should help):
  - It prevents compute from being spent on instances eliminated by known small nonexistences and focuses effort on the true frontier.
- expected metric movement:
  - fewer solve rounds that terminate with “plateau with no closure” on inherently impossible instances,
  - higher best-coverage movement per wall-time on remaining instances,
  - unchanged strict-feasibility discipline (`overcovered=0`, no `(r-1)` oversubscription) when constructing partials.
- falsification / stop condition:
  - Reject if any vetoed instance later obtains a valid certificate in this repo (gate is wrong), or if vetoing does not improve
    coverage-per-time on the remaining instance set over a fixed-budget ablation.

## Rounds 2+ execution summary and metric contract (mandatory)
### Stage order (per instance)
1. Stage A: arithmetic + derivation-veto gate.
2. Stage B: bounded symmetry triage (KM orbit compression) vs direct exact-cover sizing.
3. Stage C: strict constructive bulk (nibble/greedy or symmetry seed, depending on Stage B).
4. Stage D: pressure-triggered destroy/repack + absorber reserve discipline.
5. Stage E: residual exact-cover only after eligibility thresholds.

### Metrics to track every checkpoint
- Point degree: min/max/gap vs target `λ1`.
- `(r-1)`-pressure: max load, cap-hit count, oversubscribed count.
- Coverage quality: exact-once, uncovered, overcovered.
- Efficiency: accepted move rate, uncovered reduction per 1000 trials, and (when using LNS) micro-pack hit rate.
