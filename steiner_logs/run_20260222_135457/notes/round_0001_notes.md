# Round 1 Notes (Research-Only)

Instance: S(6,7,19)
Expected blocks: 3876
Date (UTC): 2026-02-22

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: steiner_logs/run_20260222_135457/REPO_WIDE_HISTORY.md
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

## Local-paper-first check (mandatory)
- Read local roadmap PDF (via extracted text when needed): `papers/Computational and Theoretical Roadmap for Steiner Systems with Strength 6–9 and n _ 200.pdf`.
- Read local PDFs: `papers/arxiv_1401.3665.pdf` (Keevash), `papers/arxiv_1611.06827.pdf` (iterative absorption), `papers/oai_first_proof.pdf` (workflow).
- External web search: not used in this round (links kept at `0` new).

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

## Proof-first round1 stack (mandatory)

### Seed 1: derivation-veto nonexistence (roadmap-first)
- High-level proof idea: **derivation closure**: `S(r,q,n) ⇒ S(r-1,q-1,n-1)` by fixing a point and deleting it from incident blocks.
- Solve-attempt (this round):
  - If `S(6,7,19)` existed then a derived design at any point would be `S(5,6,18)`.
  - Deriving again would force `S(4,5,17)`.
  - The local roadmap asserts `S(4,5,17)` is proved non-existent (Östergård–Pottonen), so this yields a clean nonexistence witness chain
    `S(6,7,19) -> S(5,6,18) -> S(4,5,17)`.
- Critical gap: the base nonexistence fact must be treated as **bibliographic** until the primary certificate/source is locally available.

### Seed 2: “divisible-but-small” necessary bounds lane (sanity gate)
- High-level proof idea: apply classical necessary lower bounds (Ray–Chaudhuri–Wilson; Tits/Cameron) to try to eliminate `n=19`.
- Solve-attempt (this round): checked the *form* of the bounds and noted they are typically weak on `q=r+1` (as roadmap states); they do not appear to rule out `S(6,7,19)` on their own.
- Critical gap: these bounds are not a decisive obstruction here; treat as a “failsafe gate”, not a proof lane.

### Seed 3: symmetry/Kramer–Mesner compressed exact-cover lane
- High-level proof idea: if a good group `G ≤ S_19` yields strong orbit compression with mostly-binary coefficients, solve `Ax=1` on orbits (KM) to either find a `G`-invariant design or cheaply certify “no solution with this symmetry”.
- Solve-attempt (this round): roadmap-driven bounded plan (no compute yet):
  - Try small menu: cyclic `C_19`, dihedral `D_38`, and one or two small transitive groups; if none, relax via subgroup chains `G0 ≥ G1 ≥ …`.
  - Diagnostics to record before any heavy solve: `|O_6|`, `|O_7|`, orbit compression ratio, non-binary coefficient share, `max_coeff`.
- Critical gap: even if KM fails for many groups, that is **not** a nonexistence proof without exhausting all symmetry assumptions.

### Seed 4: Keevash-style template → spill → local repair (existence-oriented, but operational)
- High-level proof idea: build a structured partial design (“template”) that is rich in local modifications, then cover the rest by greedy/nibble, producing a small “spill” (overcovered edges) that can be repaired/absorbed by local exchanges.
- Solve-attempt (this round): translated to a repo-usable operational lane (research-only):
  - Require explicit logging of `spill_size` and “spill fixed rate” as first-class verifier metrics.
  - Treat spill-fix as a strict local-search lane (micro exact-cover / trade moves) rather than global residual exact-cover.
- Critical gap: the algebraic template is not instantiated for `n=19` in repo; this seed is a method-transfer target, not a finite proof.

### Seed 5: iterative absorption (vortex + cover-down + absorbers) as a staged completion discipline
- High-level proof idea: reserve absorber structure early, run approximate cover, then iteratively **clean** leftovers by pushing them into smaller “vortex” sets via cover-down lemmas; finish with bounded leftovers absorbed by exclusive absorbers/transformers.
- Solve-attempt (this round): translated to a staged solver discipline:
  - Implement “vortex levels” as checkpoints (even if the literal theorem’s constants are asymptotic).
  - Use cover-down as a **repair primitive** to target high-pressure `(r-1)` faces without breaking strict caps.
- Critical gap: formal constants are asymptotic; the finite-instance contribution is a *search architecture*, not a theorem instance.

## Critical-gap verification loop (up to 3 rounds)
1. Verification round A (arithmetic consistency)
- Check: divisibility witness table, `b`, and `λ_i` integrality.
- Status: pass (all `6/6` remainders are `0`; `b=3876`, `λ_5=7`).
- Stop rule: any nonzero remainder is immediate impossibility certificate.

2. Verification round B (bibliographic closure for derivation-veto)
- Check: obtain a locally accessible primary source/certificate for `S(4,5,17)` nonexistence (and optionally `S(5,6,16)`).
- Status: open in this repo snapshot (roadmap asserts it, but this run does not yet store the primary certificate).
- Stop/switch rule: treat the veto as provisional until the base certificate is locally present; do not schedule heavy solve rounds for vetoed instances unless the veto is explicitly rejected.

3. Verification round C (engine compatibility and residual eligibility)
- Check: bounded symmetry diagnostics (`|O_6|,|O_7|`, non-binary share) and strict-repair readiness (pressure tail behavior).
- Status: pending (requires round2 diagnostics runs if veto is not confirmed).
- Stop/switch rule: if symmetry compression is weak or non-binary mass is material, switch early to randomized+repair lane; defer residual exact-cover while uncovered mass is large.

## Paper-to-loop method extraction (mandatory, all local PDFs)
| Source PDF | Theorem/Mechanism (explicit) | Code Delta Mapping (file:path + action) | Validation Metric |
|---|---|---|---|
| `Computational and Theoretical Roadmap for Steiner Systems with Strength 6–9 and n _ 200.pdf` | Derivation-veto propagation: `S(r,q,n) ⇒ S(r-1,q-1,n-1)` plus base nonexistences (`S(4,5,17)`, `S(5,6,16)`) to eliminate `q=r+1` low-`n` instances. | `math_proofs/steiner_portfolio.py`: add `derivation_veto()` returning a witness chain; `math_proofs/steiner_system.py`: include `nonexistence_witness` field in admissibility output | `vetoed_admissible_count`; `wasted_rounds_avoided`; vetoed instance later solved ⇒ reject |
| `Computational and Theoretical Roadmap for Steiner Systems with Strength 6–9 and n _ 200.pdf` | Kramer–Mesner orbit method: compute `G`-orbits on `r`- and `q`-subsets; solve orbit-incidence `Ax=1`; route engines by orbit diagnostics + incidence size. | add `math_proofs/steiner_kramer_mesner.py` (new) for orbit enumeration + KM matrix; update `math_proofs/steiner_exact_cover.py` to accept orbit variables; update `run_steiner_loop.sh` to run bounded KM diagnostics first | orbit compression ratio; non-binary coefficient share; solver runtime/nodes; UNSAT-under-`G` logs |
| `arxiv_1401.3665.pdf` | Randomised algebraic construction template → nibble/greedy → spill repair → absorber/cascade closure (track “spill” explicitly). | `math_proofs/steiner_exact_cover.py`: add `template_seed()` + `spill_fix()` hooks; `math_proofs/steiner_round_logger.py`: log `spill_size`, `spill_fixed_rate` | `spill_size`; uncovered slope after spill-fix; local-fix success rate |
| `arxiv_1611.06827.pdf` | Iterative absorption workflow: vortex levels + regularity boosting + cover-down lemma + exclusive absorbers via transformers. | `run_steiner_loop.sh`: add vortex scheduler + per-level checkpoints; `math_proofs/steiner_residual_repair.py`: add cover-down micro-solver stub + absorber reserve policy | leftover mass per level; cover-down hit rate; strict violations (must stay 0) |
| `oai_first_proof.pdf` | Round1 workflow: 5 seed ideas → independent solve attempts → ≤3 verify/revise loops → typeset-ready final proof outline. | `run_steiner_loop.sh`: enforce 5-seed round1 + ≤3 verification loops; `math_proofs/steiner_round_logger.py`: add verification checklist fields | #seeds explored; verification pass rate; reduced duplicated round1 essays |

## Typeset-ready final proof outline (conditional nonexistence + fallback)
1. Proposition 1 (Admissibility): `S(6,7,19)` satisfies all divisibility conditions; forced parameters are `b=3876`, `λ_5=7`.
2. Lemma 2 (Derivation): If `S(6,7,19)` exists then `S(5,6,18)` exists (derive at a point).
3. Lemma 3 (Iterated derivation): If `S(5,6,18)` exists then `S(4,5,17)` exists (derive again).
4. Theorem 4 (Derivation-veto nonexistence, conditional): If `S(4,5,17)` does not exist, then `S(6,7,19)` does not exist.
5. Fallback (if bibliographic closure fails): run bounded KM diagnostics on `S(6,7,19)` and immediately pivot portfolio to the smallest not-yet-vetoed `q=r+1` frontier (`n=23,24,25,26`) to avoid repeated dead-end spend.

## Strong search stack notes (mandatory)
1. Hard admissibility/divisibility gate (must pass)
   - Check all `\binom{q-i}{r-i} | \binom{n-i}{r-i}` (`i=0..r-1`), compute `b` and `λ_i`.
   - Apply derivation-veto propagation: reject any instance whose derived chain hits a verified nonexistence.
2. Symmetry/Kramer–Mesner exact-cover mode (bounded triage)
   - Choose `G` from a menu (cyclic/dihedral/transitive/affine; subgroup chains to relax).
   - Compute orbits `O_r`, `O_q`; build orbit-incidence matrix; solve `Ax=1` over `{0,1}` (or low-weight integer) variables.
   - Keep symmetry lane only if diagnostics pass: strong compression + low non-binary mass + small `max_coeff`.
3. Randomized lane: nibble → boosting/repair → absorber → residual exact-cover
   - Nibble/greedy to cover bulk while logging pressure on `(r-1)` faces; stop add-only when pressure tails saturate.
   - Boost/repair by destroy/repack neighborhoods that free saturated motifs; maintain strict invariants (`overcovered=0`, no `(r-1)` oversubscription) whenever running “strict mode”.
   - Maintain absorber reserve (explicit budget) for late-stage closure; use micro exact-cover only on tiny residuals.
   - Residual exact-cover is eligible only when uncovered mass is below an explicit threshold (both absolute and fraction).

## Engine selector rubric (concise)
- Use symmetry/orbit compression when orbit counts are tiny and the KM coefficient profile is mostly binary/low (`non-binary` rare; `max_coeff` small), or when a known high-symmetry template exists (difference-method style).
- Use general randomized construction when compression is weak, non-binary mass is high, or early strict add-only shows `(r-1)` pressure saturation and low acceptance.

## Practice-log failures -> research deltas (mandatory)
1. Blocker: divisibility-only portfolio selection wastes rounds on derivation-veto eliminations.
- Source: roadmap derivation-veto + base nonexistences.
- Concrete implementation change: implement `derivation_veto()` in `math_proofs/steiner_portfolio.py` and refuse scheduling solve rounds for vetoed instances unless veto is explicitly rejected.

2. Blocker: add-only strict growth plateaus once `(r-1)` faces saturate (pressure tail hardens).
- Source: iterative absorption (vortex/cover-down) + Keevash spill/repair framing.
- Concrete implementation change: pressure-triggered switch from add-only to destroy/repack; log `(r-1)` tail quantiles and acceptance decay to drive switching.

3. Blocker: binary-orbit symmetry stalls under non-binary coefficients.
- Source: roadmap KM orbit method + group-menu iteration.
- Concrete implementation change: after bounded binary KM fails, fall back to weighted-orbit ILP neighborhoods (do not extend binary-only budget).

4. Blocker: residual exact-cover invoked too early (large uncovered mass) produces no frontier movement.
- Source: Keevash/absorption staging discipline + repo practice (explicitly retired).
- Concrete implementation change: enforce a residual eligibility gate (uncovered fraction + absolute uncovered) before building any residual exact instance.

5. Blocker: repeated motif neighborhoods waste local-search budget (duplicate failures).
- Source: cross-run strict-LNS practice evidence.
- Concrete implementation change: motif signature canonicalization + short taboo cache for recent failed neighborhoods.

## Reuse vs genuinely new (explicit)
- Reused from prior runs:
  - hard divisibility gate + forced `λ_i` accounting,
  - strict feasibility invariants as backbone,
  - bounded symmetry triage + early fallback rules,
  - residual exact-cover late-gate discipline,
  - practice-derived plateau/falsification thresholds.
- Genuinely new in this round:
  - instance-specific derivation-veto proof lane for `S(6,7,19)` with an explicit witness chain and a bibliographic verification gate,
  - paper-to-loop extraction table filled for *all* local PDFs (roadmap/Keevash/iterative absorption/first-proof workflow),
  - explicit rounds2+ pivot rule: if veto is confirmed, stop spending on `n=17,19,20,22` along `q=r+1` and jump to the `n=23,24,25,26` frontier.

## External references used (minimal)
- New links introduced in this round: `0`.
- New round1 PDFs saved under `/root/openquestions/papers`: `none`.

## Plan
- Build a reusable knowledge cache for unknown large Steiner systems.
- Keep strict admissibility and derivation-veto as the front gate.
- Define when to use symmetry/KM exact-cover vs randomized/repair/absorption engines.
- Add new references only if practice logs expose a missing blocker not covered by local PDFs.

## Work log
- Completed mandatory cross-run reads before any external lookup.
- Parsed local roadmap extracted text for: derivation-veto eliminations, admissibility counts, KM orbit method, group-menu guidance.
- Transferred one concrete mechanism from each local PDF into the paper-to-loop mapping table.
- Wrote a proof-first 5-seed stack + 3-stage critical-gap verification loop + typeset-ready outline.

## Observations
- For `S(6,7,19)`, the dominant research value is *nonexistence triage* (derivation-veto) and bibliographic closure, not computational partials.
- Practice evidence strongly supports strict invariants + early pressure-triggered handoff over long add-only continuation.
- Residual exact-cover remains a theorem-sized late phase; it must stay gated by residual size.

## Core advance
- advance statement:
-   - Converted the `S(6,7,19)` round1 into a proof-first, veto-aware execution contract: derivation-veto lane + bounded symmetry triage + staged randomized fallback.
- evidence from this round (metrics, runtime, structure):
-   - Divisibility gate is explicitly recorded (`b=3876`, `λ_5=7`, all remainders `0`).
-   - Roadmap mechanisms (derivation-veto + KM orbit method) are transferred into an implementation-mapped table for all local PDFs.
-   - Practice-derived blockers are mapped to concrete code deltas and explicit switch/stop rules.
- transfer value for next rounds:
-   - Future rounds can immediately (i) close the bibliographic veto gap and (ii) pivot portfolio to frontier instances without rewriting round1 theory notes.

## Next-hypothesis
- hypothesis statement:
-   - A verified derivation-veto gate (plus bounded KM diagnostics) will reduce wasted solve spend on `q=r+1` small-`n` instances and improve “useful progress per round” on the remaining unknown set.
- mechanism (why this should help):
-   - It cheaply eliminates impossible instances and routes compute to the smallest not-yet-vetoed frontier (`n=23,24,25,26`) where exact-cover + bounded symmetry has the best chance to matter.
- expected metric movement:
-   - Near-term: fewer solve rounds scheduled on vetoed instances (target: `0`), more rounds allocated to frontier instances; improved log yield (new strict candidates or certified veto witnesses).
- falsification / stop condition:
-   - Reject if a vetoed instance later obtains a valid certificate in this repo, or if adding the gate does not reduce wasted rounds in a matched-budget ablation.

## Rounds 2+ execution summary and metric contract (mandatory)

### Execution order (if veto remains provisional)
1. Round 2: implement/activate derivation-veto gate + record explicit witness chain; run bounded KM diagnostics on a single group menu item to measure compression on the current focus instance.
2. Round 3: pivot to `S(6,7,23)` (smallest not-yet-eliminated `q=r+1` frontier) and run Stage A (KM diagnostics) then Stage B (strict randomized bulk + repair).
3. Round 4: scale-check on `S(7,8,24)` with identical gates; compare orbit compression and pressure-tail behavior.
4. Round 5: only after strict partials show meaningful uncovered reduction slopes, consider absorber-reserve experiments; keep residual exact-cover gated.

### Metrics to track every checkpoint
- Point degree: `min`, `max`, `gap`, and high-quantile tail.
- `(r-1)`-pressure: max load vs cap (`λ_{r-1}`), cap-hit count, oversubscribed count.
- Coverage quality: `exact_once`, `uncovered`, `overcovered`.
- Efficiency: accepted move rate, uncovered reduction per 1000 trials, micro-augment hit rate.
