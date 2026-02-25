# Round 1 Notes (Research-Only)

Instance: `S(6,8,29)`
Expected blocks: `16965`
Date (UTC): `2026-02-22`

## Cross-run bootstrap (mandatory first read, completed)
- `steiner_logs/PAPER_NOTES.md`
- `steiner_logs/RESEARCH_LOG.md`
- `steiner_logs/PRACTICE_LOG.md`
- `steiner_logs/RESEARCH_PAPER.md`
- `steiner_logs/EXISTENCE_FRONTIER.md`
- `steiner_logs/run_20260222_052536/REPO_WIDE_HISTORY.md`
- `steiner_logs/run_20260222_012007/notes/round_0001_notes.md`
- `steiner_logs/run_20260222_012007/notes/round_0005_notes.md`
- `steiner_logs/run_20260222_012007/NEXT_GENERATION_TRANSFER.md`

## Local-paper-first check
- Checked local directory first: `papers/oai_first_proof.pdf`.
- Extraction tools are not present in this environment (`pdftotext`, `pdfinfo`, `mutool`, `gs` unavailable).
- Round1 therefore reuses local memory from `steiner_logs/PAPER_NOTES.md` and existing cached primary links.
- External search was not required in this round.

## Admissibility gate snapshot
```json
{
  "checks": [
    {
      "denominator": 28,
      "i": 0,
      "numerator": 475020,
      "quotient": 16965,
      "remainder": 0
    },
    {
      "denominator": 21,
      "i": 1,
      "numerator": 98280,
      "quotient": 4680,
      "remainder": 0
    },
    {
      "denominator": 15,
      "i": 2,
      "numerator": 17550,
      "quotient": 1170,
      "remainder": 0
    },
    {
      "denominator": 10,
      "i": 3,
      "numerator": 2600,
      "quotient": 260,
      "remainder": 0
    },
    {
      "denominator": 6,
      "i": 4,
      "numerator": 300,
      "quotient": 50,
      "remainder": 0
    },
    {
      "denominator": 3,
      "i": 5,
      "numerator": 24,
      "quotient": 8,
      "remainder": 0
    }
  ],
  "divisibility_failures": [],
  "expected_block_count": 16965,
  "instance": {
    "n": 29,
    "q": 8,
    "r": 6
  },
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 16965,
    "lambda_1": 4680,
    "lambda_2": 1170,
    "lambda_3": 260,
    "lambda_4": 50,
    "lambda_5": 8
  }
}
```

## Proof-first round1 stack (mandatory)

### Seed 1: asymptotic existence to finite obligations
- High-level proof idea: admissibility plus iterative-absorption style decomposition suggests existence for large admissible parameters.
- Solve-attempt (this round): converted asymptotic statement into finite obligations for `n=29`: near-uniform `5`-face load, bounded uncovered residual, absorber closure condition.
- Critical gap: no explicit finite constant from cached proofs certifies this exact `n`; finite bridge remains an obligation, not a theorem instance.

### Seed 2: finite bridge via Wilson/PBD/lattice decomposition
- High-level proof idea: use decomposition machinery as a finite bridge when asymptotic constants are opaque.
- Solve-attempt (this round): formalized bridge obligations as two checks: divisibility lattice compatibility and local recomposition consistency across candidate partial designs.
- Critical gap: no instantiated decomposition for this exact triple is currently encoded in repo artifacts.

### Seed 3: symmetry/Kramer-Mesner compressed lane
- High-level proof idea: if orbit compression is strong, exact-cover on orbit variables can become tractable and proof-relevant.
- Solve-attempt (this round): made symmetry lane a bounded theorem gate with diagnostics `(compression ratio, non-binary share, max coefficient)` and explicit fallback criteria.
- Critical gap: prior high-`r` runs show non-binary inflation; a weighted-orbit fallback must be available if binary mode stalls.

### Seed 4: random nibble with pressure-triggered handoff
- High-level proof idea: random greedy/nibble should cover bulk mass faster than exact mode on unstructured instances.
- Solve-attempt (this round): expressed handoff conditions in verifier terms: add-acceptance decay, high-quantile `(r-1)` pressure growth, uncovered slope flattening.
- Critical gap: thresholds for `S(6,8,29)` need calibration in round 2.

### Seed 5: absorber reserve and motif-coupled closure
- High-level proof idea: reserve flexibility early, then use local destroy/repack and micro exact-cover only for late residual.
- Solve-attempt (this round): specified closure lane as `nibble -> boosting/repair -> absorber -> residual exact-cover` with strict invariants.
- Critical gap: absorber templates are not yet materialized for this instance; closure remains operational, not constructive.

## Critical-gap verification loop (up to 3 rounds)
1. Verification round A (arithmetic consistency)
- Check: divisibility, replication numbers, and expected block count.
- Status: pass (`6/6` remainders are `0`).
- Stop rule: any nonzero remainder is immediate arithmetic impossibility certificate.

2. Verification round B (engine compatibility)
- Check: bounded symmetry diagnostics and early packed probe quality.
- Status: unresolved for this instance; must be measured in round 2 before engine commitment.
- Stop/switch rule: if compression is weak or non-binary share is material, switch early to randomized lane.

3. Verification round C (closure eligibility)
- Check: strict invariants and residual threshold before residual exact-cover.
- Status: by cross-run evidence, residual exact-cover is structurally premature unless uncovered mass is already small.
- Stop/switch rule: defer exact residual closure while uncovered remains large; continue strict repair/absorber passes.

## Typeset-ready final proof outline
1. Proposition 1 (Admissibility): `S(6,8,29)` satisfies all necessary divisibility conditions, with `b=16965` and `lambda_5=8`.
2. Lemma 2 (Finite-bridge obligation): asymptotic existence reduces the finite case to explicit local-balance and recomposition obligations.
3. Lemma 3 (Bounded engine dichotomy): bounded symmetry diagnostics either produce a tractable compressed exact-cover model or certify fallback to randomized mode.
4. Lemma 4 (Strict monotone repair): under `c_6<=1` and `c_5<=8`, accepted local operations preserve feasibility and can reduce uncovered mass.
5. Lemma 5 (Residual closure gate): residual exact-cover is admissible only after strict feasibility and a small uncovered threshold.
6. Operational theorem schema: combining 1-5 yields a finite proof/search protocol that outputs either impossibility witness, strict-feasible partial certificate, or full certificate.

## Strong search stack (mandatory)
1. Hard admissibility/divisibility gate.
- Recompute all `lambda_i`, `b`, and integrality checks first.
- Abort constructive search on first arithmetic failure witness.

2. Symmetry/Kramer-Mesner exact-cover mode (bounded front gate).
- Run cyclic/dihedral orbit diagnostics and coefficient histogram.
- Keep this lane only if compression is strong and columns are mostly binary.

3. General randomized construction mode.
- Execute `nibble -> boosting/repair -> absorber -> residual exact-cover`.
- Maintain strict feasibility (`overcovered=0`, no `(r-1)` oversubscription).
- Open residual exact-cover only after explicit residual-size gate.

## Engine-selector rubric (concise)
- Use symmetry/orbit compression when orbit model compression is large, non-binary coefficients are rare, and a bounded packed probe gives immediate strict progress.
- Use general randomized construction when compression is weak, non-binary mass is high, or early strict add-only behavior shows `(r-1)` pressure saturation.

## Practice-log failures -> research deltas (mandatory)
1. Blocker: add-only strict growth plateaus once `(r-1)` faces saturate.
- Source likely to address it: iterative absorption framing (`https://arxiv.org/abs/1611.06827`).
- Concrete implementation change: trigger destroy/repack once add acceptance drops below calibrated threshold in a fixed trial window.

2. Blocker: binary-only symmetry probes stall under non-binary orbit coefficients.
- Source likely to address it: Kramer-Mesner framework (`https://www.sciencedirect.com/science/article/pii/0097316586900944`).
- Concrete implementation change: add weighted-orbit micro-ILP neighborhoods after binary probe failure, rather than extending binary search budget.

3. Blocker: residual exact-cover invoked too early wastes runtime with no frontier movement.
- Source likely to address it: asymptotic-to-finite staging discipline (Keevash + practice evidence) (`https://arxiv.org/abs/1401.3665`).
- Concrete implementation change: enforce uncovered-fraction eligibility gate before launching residual exact solver.

4. Blocker: repeated motif neighborhoods produce duplicate low-yield local attempts.
- Source likely to address it: cross-run strict LNS observations in `steiner_logs/PRACTICE_LOG.md`.
- Concrete implementation change: canonical motif signatures with short taboo cache for recent failed neighborhoods.

## Reuse vs genuinely new (explicit)
- Reused from prior runs:
  - hard divisibility gate before all expensive search,
  - bounded symmetry triage with explicit fallback,
  - strict feasibility invariants as mandatory constraints,
  - staged pipeline ending with late residual exact-cover gate.
- Genuinely new in this round:
  - proof-first stack specialized to `S(6,8,29)` with per-seed solve-attempt and explicit gap statements,
  - a 3-round critical-gap verification loop written as gate tests,
  - a typeset-ready proposition/lemma theorem skeleton targeted to this instance,
  - blocker-to-implementation delta mapping tied to rounds2-5 failures.

## External references used (minimal)
- New links introduced in this round: `0`.
- Reused cached links:
  - `https://arxiv.org/abs/1401.3665`
  - `https://arxiv.org/abs/1611.06827`
  - `https://www.sciencedirect.com/science/article/pii/0097316586900944`
- New round1 PDFs saved under `/root/openquestions/papers`: `none` (no new links added).

## Rounds 2+ execution summary and metric contract (mandatory)

### Execution order
1. Round 2: run full stage protocol on `S(6,8,29)` to calibrate selector thresholds and pressure triggers.
2. Round 3: run `S(7,8,24)` as transfer check for selector robustness at higher expected block count.
3. Round 4: revisit `S(8,9,21)` with early handoff and motif-coupled repair emphasis.
4. Round 5: refine `S(9,10,22)` from symmetry seed with medium-window strict repacks and residual gate discipline.

### Stage protocol
1. Stage A: arithmetic gate (`lambda_i`, `b`, divisibility witness table).
2. Stage B: bounded symmetry diagnostics and packed probe.
3. Stage C: randomized bulk (`nibble`, strict add/repair).
4. Stage D: absorber reserve + motif-coupled destroy/repack.
5. Stage E: residual exact-cover only after eligibility gate.

### Metrics to track every checkpoint
- Point degree: `min`, `max`, `gap`, and high-quantile tail.
- `(r-1)`-pressure: max load, cap-hit count, oversubscribed count.
- Coverage quality: `exact_once`, `uncovered`, `overcovered`.
- Efficiency: accepted move rate, uncovered reduction per 1000 trials, micro-augment hit rate.

## Plan
- Keep round1 research-only and proof-first.
- Use local-paper-first memory and avoid link churn.
- Carry a single canonical hybrid hypothesis into solve rounds.

## Work log
- Completed all mandatory cross-run reads before any external lookup.
- Verified local-paper-first status from `papers/` and tool availability.
- Wrote proof-first stack, strong search stack, engine selector, and blocker-driven deltas.
- Consolidated rounds2+ stage and metric contract for transfer.

## Observations
- The main unresolved issue is finite constructive closure, not arithmetic admissibility.
- Practice evidence across runs supports early pressure-aware handoff over long add-only phases.
- Residual exact-cover should remain a theorem-level late phase, not a default early action.

## Core advance
- advance statement:
  - Converted round1 for `S(6,8,29)` into a proof-first, gate-explicit execution contract with five seeded proof lanes and a 3-round critical-gap verification loop.
- evidence from this round (metrics, runtime, structure):
  - Mandatory cross-run memory and local-paper-first conditions were completed.
  - Strong search stack and concise engine selector were formalized.
  - Practice blockers are mapped to explicit implementation changes for rounds2+.
- transfer value for next rounds:
  - Future rounds can execute without re-deriving proof structure.
  - Engine switches and residual exact-cover activation are now gate-based and falsifiable.

## Next-hypothesis
- hypothesis statement:
  - For `S(6,8,29)`, bounded symmetry triage followed by pressure-triggered strict repair handoff will outperform prolonged symmetry-only or add-only policies under matched budgets while keeping strict feasibility.
- mechanism (why this should help):
  - It matches prior evidence that add-only phases plateau near saturated `(r-1)` motifs and that symmetry quality is highly instance-dependent.
- expected metric movement:
  - faster uncovered reduction slope,
  - flatter point-degree spread,
  - lower `(r-1)` pressure tail,
  - `overcovered=0` and zero `(r-1)` oversubscription maintained.
- falsification / stop condition:
  - Reject after 3 matched seeds if uncovered reduction per fixed budget does not beat add-only baseline or if strict feasibility is violated.
