# Round 1 Notes (Research-Only)

Instance: S(6,7,19)
Expected blocks: 3876
Date (UTC): 2026-02-22

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: steiner_logs/run_20260222_110632/REPO_WIDE_HISTORY.md
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

## Local-paper-first check
- Read local roadmap first via extracted text: `papers/_extracted_text/Computational and Theoretical Roadmap for Steiner Systems with Strength 6–9 and n _ 200.txt`.
- Also read local extracted texts for: `papers/_extracted_text/arxiv_1401.3665.txt`, `papers/_extracted_text/arxiv_1611.06827.txt`, `papers/_extracted_text/oai_first_proof.txt`.
- No external web search was required in this round (research-only synthesis).

## Proof-first round1 stack (mandatory)

### Seed 1: derivation-veto nonexistence (roadmap core)
- High-level proof idea: derivation closure `S(r,q,n) ⇒ S(r-1,q-1,n-1)` turns any verified base nonexistence into a nonexistence proof for larger parameters.
- Solve-attempt (this round): roadmap reports `S(4,5,17)` does not exist; therefore
  `S(6,7,19) -> S(5,6,18) -> S(4,5,17)` would contradict existence.
- Critical gap: the base nonexistence must be verified from the primary source (Östergård–Pottonen) before we treat this as a hard veto in portfolio selection.

### Seed 2: derivation-veto portfolio rewrite via `S(5,6,16)` (roadmap + van der Pol)
- High-level proof idea: if `S(5,6,16)` is non-existent, then `S(6,7,17)` is non-existent by a single derivation step; similarly this knocks out the smallest admissible instances on the `q=r+1` line across `r=6..9`.
- Solve-attempt (this round): roadmap reports the eliminations:
  - `S(6,7,17)` derives to `S(5,6,16)`,
  - `S(7,8,18)` derives to `S(6,7,17)`,
  - `S(8,9,19)` and `S(9,10,20)` are eliminated by a longer derivation chain.
  If correct, the smallest not-yet-eliminated `q=r+1` starts become: `S(6,7,23)`, `S(7,8,24)`, `S(8,9,25)`, `S(9,10,26)`.
- Critical gap: `S(5,6,16)` is described as “tabulated” in the roadmap; we must locate a citable primary record before using it as a hard gate.

### Seed 3: symmetry/Kramer–Mesner compressed lane (KM orbit reduction)
- High-level proof idea: if a moderate group action yields strong orbit compression, solve `Ax=1` at orbit level to search for a `G`-invariant design (or certify “no solution under this `G`” quickly).
- Solve-attempt (this round): for `n=19`, the first diagnostic menu is `C19`, `D38`, and `AGL(1,19)` (difference-method inspired and easy to enumerate), with strict early-stop if:
  - `|O_q|` is large (weak compression), or
  - non-binary orbit coefficients are frequent / large (weighted-orbit inflation).
- Critical gap: KM failure under a chosen `G` is not nonexistence; it only triggers engine fallback. To turn this into a proof lane, we need either full “all groups” exhaustion (not feasible) or a derivation/nonexistence certificate.

### Seed 4: randomized bulk + strict repair as an evidence generator (not a proof)
- High-level proof idea: nibble/greedy can quickly build a strict-feasible partial (no collisions) that exposes the geometry of bottlenecks via verifier metrics (degree tails, `(r-1)` pressure saturation, uncovered slope).
- Solve-attempt (this round): specify the measurable handoff: when strict add acceptance collapses and `(r-1)` pressure tails hit cap (`λ_{r-1}`), switch to destroy/repack neighborhoods (motif-coupled).
- Critical gap: plateau/pressure witnesses are not a nonexistence proof; they only justify switching engines or changing instance selection.

### Seed 5: Keevash template+spill / iterative-absorption translation to finite search deltas
- High-level proof idea: use an initial structured “template” (algebraic or symmetry-seeded), then allow controlled spill/repair and absorber-style closure rather than monolithic exact cover.
- Solve-attempt (this round): treat “template → greedy cover → spill-fix” (Keevash framing) and “vortex → cover-down → absorber” (iterative absorption framing) as a staged schedule for finite solver policies, with explicit residual eligibility gates.
- Critical gap: asymptotic proofs give no explicit `n≤200` threshold; all finite success must be demonstrated by measured verifier movement and/or exact-cover completion, not by citation.

## Critical-gap verification loop (up to 3 rounds)
1. Verification round A (arithmetic consistency)
- Check: divisibility, replication numbers, and expected block count.
- Status: pass (`6/6` remainders are `0`).
- Stop rule: any nonzero remainder is an immediate arithmetic impossibility witness.

2. Verification round B (derivation-veto base facts)
- Check: confirm the roadmap’s base nonexistence claims in primary sources:
  - `S(4,5,17)` nonexistence (Östergård–Pottonen),
  - `S(5,6,16)` nonexistence (van der Pol table / cited provenance).
- Status: not yet verified in this round (research-only, local-first, no web fetch).
- Stop rule: if verified, mark `S(6,7,19)` as non-existent with explicit derivation chain; skip all solve rounds for it.

3. Verification round C (engine compatibility, only if not vetoed)
- Check: bounded symmetry diagnostics (`|O_q|,|O_r|`, non-binary share, max coefficient) and early strict seed behavior (add acceptance vs pressure growth).
- Status: deferred (should not invest in construction until veto status is settled).
- Stop/switch rule: if KM compression is weak or coefficients inflate, switch immediately to randomized+repair; never open residual exact-cover unless residual eligibility gate is met.

## Typeset-ready final proof outline (conditional nonexistence)
1. Proposition (Admissibility): `S(6,7,19)` satisfies the Steiner divisibility constraints, with `b=3876` and `λ_5=7`.
2. Lemma (Derivation): if `S(r,q,n)` exists then `S(r-1,q-1,n-1)` exists (fix a point and delete it from incident blocks).
3. Theorem (Nonexistence from base case): if `S(4,5,17)` does not exist, then `S(6,7,19)` does not exist because
   `S(6,7,19) -> S(5,6,18) -> S(4,5,17)` by repeated derivation.
4. Corollary (Portfolio rewrite): if `S(5,6,16)` does not exist, then `S(6,7,17)` does not exist (and similarly eliminates the smallest admissible `q=r+1` instances for `r=7,8,9` by derivation chains).
5. If either base fact is unverified, treat `S(6,7,19)` as open-but-low-priority and switch portfolio to the roadmap’s smallest not-yet-eliminated starts: `S(6,7,23)`, `S(7,8,24)`, `S(8,9,25)`, `S(9,10,26)`.

## Strong search stack (mandatory)

### 1) Hard admissibility/divisibility gate
- Compute and record `b = \binom{n}{r} / \binom{q}{r}` and `λ_i = \binom{n-i}{r-i}/\binom{q-i}{r-i}` for all `i<r`.
- Reject immediately on the first non-integer `λ_i` (store the witness tuple).

### 2) Derivation-veto + classical lower-bound gate (roadmap)
- Apply derivation propagation from verified base nonexistences (fast eliminate families before solver spend).
- Apply Ray–Chaudhuri–Wilson and Tits/Cameron bounds as additional necessary filters, especially when `q−r>1`.

### 3) Symmetry/Kramer–Mesner exact-cover mode (orbit-compressed)
- Choose `G ≤ S_n` from a pragmatic menu (cyclic/dihedral/affine/transitive groups; relax along subgroup chains if needed).
- Build orbit incidence `A` between `G`-orbits on `r`- and `q`-subsets; solve `Ax=1` with `x∈{0,1}^{|O_q|}` (SAT/ILP/DLX).
- Early-switch if orbit counts are large or coefficient structure is heavily non-binary.

### 4) Randomized mode: nibble → boosting/repair → absorber → residual exact-cover
- Bulk: random greedy/nibble to cover most `r`-subsets quickly (strict-feasible if possible).
- Repair: pressure-triggered destroy/repack neighborhoods once `(r-1)` tails harden (avoid add-only plateau).
- Absorber discipline: reserve flexibility early; only spend it to close stubborn residual structure.
- Residual exact-cover: open only under explicit residual eligibility thresholds (uncovered small, pressure under control).

## Engine selector rubric (concise)
- Use symmetry/orbit compression when `|O_q|,|O_r|` are tiny, coefficients are mostly binary/low-weight, and a quick KM feasibility probe finds structure.
- Use general randomized construction when orbit compression is weak, non-binary mass inflates, or early strict add-only behavior saturates `(r-1)` pressure tails.

## Paper-to-loop method extraction (mandatory, all local PDFs)
| Source PDF | Theorem/Mechanism (explicit) | Code Delta Mapping (file:path + action) | Validation Metric |
|---|---|---|---|
| roadmap | Workflow mechanism: derivation-veto nonexistence propagation along `q=r+1` from verified bases (`S(4,5,17)` and `S(5,6,16)`). | `math_proofs/steiner_portfolio.py`: add verified-base list + derivation propagation + veto witness chain; `math_proofs/steiner_system.py`: include witness chain in reports | % of portfolio vetoed; #solve rounds avoided; vetoed instance later solved ⇒ reject |
| roadmap | Kramer–Mesner orbit method (`Ax=1` on orbit-incidence for prescribed `G`) + group-menu workflow | `math_proofs/steiner_exact_cover.py`: add orbit-variable mode; `math_proofs/steiner_round_logger.py`: log `|O_r|,|O_q|`, non-binary share, max coeff | Compression ratio; KM nnz; runtime/nodes; early-switch correctness |
| arxiv_1401.3665 | Theorem mechanism: randomized-algebraic template, spill repair, robust fractional extendability, and absorber-style closure. | `math_proofs/steiner_residual_repair.py`: add template/spill accounting + local trade library hooks; `math_proofs/steiner_round_logger.py`: log spill size + fix hit-rate | Spill size vs time; uncovered slope; local-fix success rate |
| arxiv_1611.06827 | Iterative absorption: vortex + Cover down lemma + cleaners + transformers/absorbers | `run_steiner_round.sh`: add staged “vortex-level” scheduler; `math_proofs/steiner_residual_repair.py`: cover-down micro-solver stage | Leftover mass per level; cover-down hit rate; strict violations (must be 0) |
| oai_first_proof | Protocol mechanism: seed ideas fanout, repeat up to 3 verify loops, explicit gap checks, and typeset-ready final pass. | `run_steiner_round.sh`: emit 5 seed configs in round1; `math_proofs/steiner_round_logger.py`: enforce verification checklist + reuse-vs-new block | #seeds explored; % verification passes; reduction in duplicated round1 essays |

## Practice-log failures -> research deltas (mandatory)
1. Blocker: **divisibility-only portfolio selection** wastes solve rounds on derivation-vetoed triples.
- Source likely to address it: roadmap derivation-veto propagation.
- Concrete implementation change: add a verified-base-nonexistence ledger to `math_proofs/steiner_portfolio.py` and propagate vetoes by derivation before ranking instances.

2. Blocker: **add-only strict growth plateaus** once `(r-1)` faces saturate at cap.
- Source likely to address it: iterative absorption staging (vortex/cover-down/absorber framing).
- Concrete implementation change: trigger motif-coupled destroy/repack once `(r-1)` max hits `λ_{r-1}` and strict add acceptance falls below a calibrated threshold per 1000 trials.

3. Blocker: **binary-only symmetry probes stall** under non-binary orbit coefficients.
- Source likely to address it: roadmap KM workflow (diagnostics-first, then orbit-level SAT/ILP).
- Concrete implementation change: add non-binary-mass diagnostics and switch from binary-KM to weighted-orbit ILP neighborhoods after a bounded failure budget.

4. Blocker: **early residual exact-cover** wastes runtime at large uncovered fraction.
- Source likely to address it: Keevash “template then spill-fix” + repo practice retirement of early residual.
- Concrete implementation change: enforce an uncovered-fraction eligibility gate before building residual exact-cover instances (and log the rejection).

5. Blocker: **duplicate motif neighborhoods** waste local-search budget.
- Source likely to address it: practice-log strict-LNS evidence (hit-rate depends on neighborhood source ratios).
- Concrete implementation change: canonical motif signatures + short taboo cache in `math_proofs/steiner_residual_repair.py` to avoid immediate repeats.

## External references used (minimal)
- New links introduced in this round: `0`.
- Reused cached links: `0` (local PDFs only; see paths in “Local-paper-first check”).
- New round1 PDFs saved under `/root/openquestions/papers`: `none`.

## Reuse vs genuinely new (explicit)
- Reused from prior runs:
  - hard divisibility gate before any expensive search,
  - staged engine policy (bounded symmetry triage, then randomized/repair, then late residual),
  - strict feasibility invariants and practice-derived metric contract (point degree, `(r-1)` pressure, uncovered/overcovered).
- Genuinely new in this round:
  - roadmap-expanded derivation-veto set (`S(4,5,17)` + `S(5,6,16)`) and the resulting portfolio pivot to `S(6,7,23)` etc.,
  - explicit “conditional nonexistence” typeset-ready proof outline for `S(6,7,19)` via derivation,
  - a filled source-to-method transfer table aligned to concrete repo file paths and validation metrics.

## Rounds 2+ execution summary and metric contract (mandatory)

### Execution order (updated by roadmap veto risk)
1. Round 2 (research+gate): verify base nonexistence sources for `S(4,5,17)` and `S(5,6,16)`; then implement derivation-veto propagation in portfolio selection.
2. Round 2 (solve, if veto confirmed): skip `S(6,7,19)`; start smallest not-yet-eliminated `q=r+1` targets: `S(6,7,23)` then `S(7,8,24)` with bounded KM triage and exact-cover (seed-and-extend) workflows.
3. Round 3+: for larger `r` (`8,9`), require orbit compression or distributed search; keep randomized+repair as default when symmetry compression is weak.

### Metrics to track every checkpoint
- Point degree: `min`, `max`, `gap`, and high-quantile tail.
- `(r-1)`-pressure: max load, cap-hit count, oversubscribed count.
- Coverage quality: `exact_once`, `uncovered`, `overcovered`.
- Efficiency: accepted move rate, uncovered reduction per 1000 trials, micro-augment hit rate.

## Plan
- Build a reusable knowledge cache for unknown large Steiner systems.
- Keep strict admissibility as a hard gate.
- Define when to use symmetry/exact-cover vs nibble/absorption engines.
- Add new references only if practice logs expose a gap not already covered in global research log.

## Work log
- Completed mandatory cross-run reads before any external lookup.
- Extracted roadmap mechanisms: derivation-veto propagation, frontier re-ranking, KM orbit workflow, and classical bounds.
- Updated global synthesis paper (`steiner_logs/RESEARCH_PAPER.md`) to reflect the pivot and add claim/evidence blocks.
- Drafted a proof-first stack with explicit gap checks for base-nonexistence verification.

## Observations
- `S(6,7,19)` is admissible but plausibly non-existent if roadmap base results are correct; construction should not be prioritized until base verification is done.
- If derivation-veto is correct, several previously “top unresolved admissible” instances on `q=r+1` are dead targets; portfolio must pivot to `n=23,24,25,26`.
- Practice logs reinforce: strict invariants are transferable; early residual exact-cover is structurally premature; add-only plateaus are real and require repack/absorber-inspired lanes.

## Core advance
- advance statement:
  - Converted this run’s round1 into a proof-first, veto-aware execution contract for `S(6,7,19)` and rewired the portfolio logic around roadmap derivation-veto results.
- evidence from this round (metrics, runtime, structure):
  - Admissibility verified (all divisibility remainders `0`); expected blocks `3876`, `λ_5=7`.
  - Roadmap-derived nonexistence propagation identified a high-leverage pre-sieve that may eliminate `S(6,7,19)` and other smallest `q=r+1` admissible instances.
  - Practice-derived metrics reused: strict invariants (`overcovered=0`, `(r-1)` oversubscription `0`) and residual ineligibility at uncovered fraction `≈0.51` for `S(9,10,22)`.
- transfer value for next rounds:
  - Rounds 2+ can avoid solve spend on provably eliminated triples once base nonexistences are verified.
  - The run now has an explicit 5-seed proof stack + 3-stage verification loop + strong search stack to execute without re-deriving theory.

## Next-hypothesis
- hypothesis statement:
  - Verifying and implementing roadmap derivation-veto propagation (`S(4,5,17)`, `S(5,6,16)`) will measurably increase useful solve yield by eliminating impossible `q=r+1` triples before any solver work.
- mechanism (why this should help):
  - Derivation is a closure property, so each verified base nonexistence wipes out an infinite family; in our finite window it removes the smallest admissible targets that otherwise look most tempting by size.
- expected metric movement:
  - Reduce “attempts on dead instances” to `0`.
  - Shift solver budget to `S(6,7,23)`/`S(7,8,24)` where a full certificate is not pre-eliminated by the roadmap.
- falsification / stop condition:
  - Reject if any instance vetoed by the implemented derivation gate later achieves a valid certificate in this repo; immediately downgrade the veto to “soft” and require explicit source re-verification.
