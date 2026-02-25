# Round 1 Notes (Research-Only)

Instance: `S(6,7,17)`
Expected blocks: `1768`
Date (UTC): `2026-02-22`

## Cross-run bootstrap (mandatory first read, completed)
- `steiner_logs/PAPER_NOTES.md`
- `steiner_logs/RESEARCH_LOG.md`
- `steiner_logs/PRACTICE_LOG.md`
- `steiner_logs/run_20260222_154119/REPO_WIDE_HISTORY.md`
- `steiner_logs/run_20260222_052536/notes/round_0001_notes.md`
- `steiner_logs/run_20260222_052536/notes/round_0005_notes.md`
- `steiner_logs/run_20260222_052536/NEXT_GENERATION_TRANSFER.md`

## Local-paper-first check
- Checked local papers before any web search:
- `papers/Computational and Theoretical Roadmap for Steiner Systems with Strength 6–9 and n _ 200.pdf`
- `papers/arxiv_1401.3665.pdf`
- `papers/arxiv_1611.06827.pdf`
- `papers/oai_first_proof.pdf`
- Read corresponding local extracts under `papers/_extracted_text/`.
- External web search used in this round: `none`.
- New external links added: `0`.

## Admissibility gate snapshot
```json
{
  "checks": [
    {
      "denominator": 7,
      "i": 0,
      "numerator": 12376,
      "quotient": 1768,
      "remainder": 0
    },
    {
      "denominator": 6,
      "i": 1,
      "numerator": 4368,
      "quotient": 728,
      "remainder": 0
    },
    {
      "denominator": 5,
      "i": 2,
      "numerator": 1365,
      "quotient": 273,
      "remainder": 0
    },
    {
      "denominator": 4,
      "i": 3,
      "numerator": 364,
      "quotient": 91,
      "remainder": 0
    },
    {
      "denominator": 3,
      "i": 4,
      "numerator": 78,
      "quotient": 26,
      "remainder": 0
    },
    {
      "denominator": 2,
      "i": 5,
      "numerator": 12,
      "quotient": 6,
      "remainder": 0
    }
  ],
  "divisibility_failures": [],
  "expected_block_count": 1768,
  "instance": {
    "n": 17,
    "q": 7,
    "r": 6
  },
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

## Proof-first round1 stack (mandatory)

### Seed 1: arithmetic feasibility as theorem front gate
- High-level proof idea: any candidate must satisfy full divisibility and forced replication identities.
- Solve-attempt: recomputed `b` and all `lambda_i`; all arithmetic checks pass.
- Critical gap: arithmetic is necessary only, so this seed does not settle existence.

### Seed 2: derivation-veto nonexistence lane
- High-level proof idea: if `S(6,7,17)` exists, derivation implies `S(5,6,16)` exists.
- Solve-attempt: imported derivation chain from local roadmap extraction and marked this as a parallel proof lane.
- Critical gap: base nonexistence certificate for `S(5,6,16)` must be verified from primary citation before declaring impossibility.

### Seed 3: symmetry/Kramer-Mesner compressed existence lane
- High-level proof idea: strong orbit compression can transform construction into tractable exact-cover over orbit variables.
- Solve-attempt: fixed bounded triage diagnostics (`orbit compression ratio`, `non-binary share`, `max coefficient`) as pass/fail gates.
- Critical gap: binary-only orbit mode can stall when coefficient structure is non-binary.

### Seed 4: nibble to iterative absorption lane
- High-level proof idea: random greedy covers bulk constraints; iterative absorption handles late structured residual.
- Solve-attempt: formalized staged route `nibble -> boosting/repair -> absorber reserve -> residual exact-cover`.
- Critical gap: asymptotic guarantees do not provide finite closure constants for this exact `n`.

### Seed 5: strict constructive certificate lane
- High-level proof idea: build monotone strict-feasible partial certificates, then attempt closure under hard caps.
- Solve-attempt: encoded strict invariants (`overcovered=0`, no `(r-1)` oversubscription) plus motif-coupled micro-repacks.
- Critical gap: practice shows frequent plateau at saturated `(r-1)` motifs without adaptive neighborhood scaling.

## Critical-gap verification loop (up to 3 rounds)
1. Verification round A (arithmetic + derivation source integrity)
- Check: divisibility and replication identities; derivation chain assumptions.
- Status: arithmetic pass; derivation-base citation still an explicit bibliographic obligation.
- Stop rule: any arithmetic failure is immediate impossibility; unresolved derivation source blocks nonexistence certification.

2. Verification round B (engine compatibility)
- Check: short symmetry diagnostics and packed probe quality.
- Status: unresolved until round 2 instrumentation executes.
- Stop/switch rule: weak compression or material non-binary mass triggers immediate fallback to randomized lane.

3. Verification round C (closure eligibility)
- Check: strict invariants and residual-size gate.
- Status: by practice history, residual exact-cover is premature unless uncovered mass is already small.
- Stop/switch rule: keep residual solver disabled while uncovered remains large; continue strict repair/absorber steps.

## Typeset-ready final proof outline
1. Proposition 1 (Admissibility): `S(6,7,17)` satisfies all standard divisibility conditions, with `b=1768` and `lambda_5=6`.
2. Lemma 2 (Derivation alternative): existence of `S(6,7,17)` would imply existence of `S(5,6,16)` by derivation.
3. Lemma 3 (Bounded engine dichotomy): symmetry compression either yields a tractable orbit exact-cover model or certifies early handoff to randomized construction.
4. Lemma 4 (Strict monotone repair): under strict caps, accepted local moves preserve feasibility while reducing uncovered mass.
5. Lemma 5 (Residual closure gate): residual exact-cover is admissible only after strict feasibility and a small uncovered threshold.
6. Theorem schema (round protocol): combining 1-5 yields a falsifiable finite workflow that returns either a verified nonexistence chain, a strict partial certificate, or a full certificate.

## Strong search stack (mandatory)
1. Hard admissibility/divisibility gate.
- Recompute `b`, all `lambda_i`, and integrality checks before any expensive search.
- Abort immediately on first arithmetic witness.

2. Symmetry/Kramer-Mesner exact-cover mode.
- Run bounded cyclic/dihedral orbit diagnostics and an early packed probe.
- Keep this mode only if orbit compression is strong and coefficients are mostly binary.

3. General randomized construction mode.
- Execute `nibble -> boosting/repair -> absorber -> residual exact-cover`.
- Maintain strict invariants throughout.
- Open residual exact-cover only after explicit residual gate passes.

## Engine-selector rubric (concise)
- Use symmetry/orbit compression when orbit reduction is large, non-binary share is low, and short packed probes yield strict progress.
- Use general randomized construction when compression is weak, non-binary mass is high, or add-only acceptance decays under rising `(r-1)` pressure.

## Practice-log failures -> research deltas (mandatory)
1. Blocker seen in rounds2-5: add-only plateau after `(r-1)` saturation.
- Source likely to address it: iterative absorption workflow (`papers/_extracted_text/arxiv_1611.06827.pdftotext.txt`).
- Concrete implementation change: pressure-triggered handoff from add-only to motif-coupled destroy/repack after fixed-window acceptance collapse.

2. Blocker seen in rounds2-5: binary orbit search stalls on non-binary coefficient structure.
- Source likely to address it: roadmap KM sections (`papers/_extracted_text/Computational and Theoretical Roadmap for Steiner Systems with Strength 6–9 and n _ 200.pdftotext.txt`).
- Concrete implementation change: activate weighted-orbit micro-ILP neighborhoods instead of extending binary-only search budget.

3. Blocker seen in rounds2-5: residual exact-cover launched at high uncovered fraction with no practical movement.
- Source likely to address it: template/spill/absorb staging (`papers/_extracted_text/arxiv_1401.3665.pdftotext.txt`).
- Concrete implementation change: hard residual gate requiring strict feasibility plus low uncovered fraction before residual solver launch.

4. Blocker seen in rounds2-5: repeated low-yield neighborhood reuse.
- Source likely to address it: verify-revise protocol (`papers/_extracted_text/oai_first_proof.pdftotext.txt`) and practice highlights.
- Concrete implementation change: canonical motif signatures + short taboo cache + bounded 3-loop revise cycle.

## Reuse vs genuinely new (explicit)
- Reused from prior runs:
- hard admissibility front gate,
- bounded symmetry triage before deep search,
- strict feasibility invariants as transfer artifacts,
- late residual exact-cover discipline.
- Genuinely new in this round:
- derivation-veto lane elevated to seed-level proof branch for `S(6,7,17)`,
- five-seed proof stack with per-seed solve-attempt and explicit gaps,
- blocker-to-source-to-code-delta map anchored to rounds2-5 behavior,
- round2+ metric contract focused on point degree, `(r-1)` pressure, and uncovered/overcovered dynamics.

## External references used (minimal)
- New links introduced in this round: `0`.
- Reused cached links:
- `https://arxiv.org/abs/1401.3665`
- `https://arxiv.org/abs/1611.06827`

## Rounds 2+ execution summary and metric contract (mandatory)

### What rounds 2+ should execute
1. Round 2: run bounded symmetry triage and derivation-veto bibliographic verification in parallel lanes; pick engine by measured diagnostics, not by default.
2. Round 3: execute selected primary engine under strict caps and compare against a matched-budget alternate lane.
3. Round 4: apply motif-coupled medium-window repair with periodic neutral rebalance sweeps.
4. Round 5: open residual exact-cover only if gate passes; otherwise continue strict repair and report gate failure as a theorem obligation.

### Metrics to track at every checkpoint
- Point degree: `min`, `max`, `gap`, and tail concentration.
- `(r-1)`-pressure: max load, cap-hit count, oversubscribed count.
- Coverage quality: `uncovered` and `overcovered` counts.
- Supporting diagnostics: acceptance rate, uncovered reduction per 1000 attempts.

## Plan
- Keep round1 research-only and proof-first.
- Preserve local-paper-first discipline with minimal external links.
- Use explicit gate tests so rounds2+ are falsifiable and reproducible.

## Work log
- Completed mandatory cross-run bootstrap in required order.
- Scanned local paper extracts before any web lookup.
- Built proof-first stack, strong search stack, and engine-selector rubric.
- Mapped practice blockers to concrete implementation deltas.
- Added rounds2+ execution/metrics contract for direct handoff.

## Observations
- Arithmetic admissibility is settled; the unresolved bottlenecks are structural (derivation certification and closure mechanics).
- Practice evidence consistently supports early pressure-aware handoff over prolonged add-only phases.
- Residual exact-cover remains a late theorem gate, not a default progress engine.

## Core advance
- advance statement:
- Converted round1 for `S(6,7,17)` into a proof-first, gate-explicit research contract with five seeded proof lanes and a 3-round critical-gap verification loop.
- evidence from this round (metrics, runtime, structure):
- Mandatory cross-run memory and local-paper-first requirements were completed.
- Strong search stack and concise engine selector were formalized.
- Practice blockers were mapped to source-backed implementation deltas.
- transfer value for next rounds:
- Rounds2+ can execute without re-deriving proof skeleton or switch logic.
- Engine switches and residual activation are now explicit and falsifiable.

## Next-hypothesis
- hypothesis statement:
- For `S(6,7,17)`, bounded symmetry triage plus pressure-triggered repair handoff will outperform prolonged single-engine continuation while preserving strict feasibility.
- mechanism (why this should help):
- It aligns with observed plateau behavior in rounds2-5 and targets saturated `(r-1)` motifs directly.
- expected metric movement:
- faster uncovered reduction slope,
- lower `(r-1)` pressure tail,
- stable `overcovered=0` and zero `(r-1)` oversubscription.
- falsification / stop condition:
- Reject after 3 matched seeds if uncovered reduction per fixed budget does not beat add-only baseline or if strict feasibility is violated.
