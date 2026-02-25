# Round 1 Notes (Research-Only)

Instance: `S(6,7,23)`
Expected blocks: `14421`
Date (UTC): 2026-02-22

## Cross-run bootstrap (mandatory first read, completed)
- `steiner_logs/PAPER_NOTES.md`
- `steiner_logs/RESEARCH_LOG.md`
- `steiner_logs/PRACTICE_LOG.md`
- `steiner_logs/EXISTENCE_FRONTIER.md`
- `steiner_logs/run_20260222_012007/REPO_WIDE_HISTORY.md`
- `steiner_logs/run_20260221_013905/notes/round_0001_notes.md`
- `steiner_logs/run_20260221_013905/notes/round_0005_notes.md`
- `steiner_logs/run_20260221_013905/NEXT_GENERATION_TRANSFER.md`

## Local-paper-first check
- Local papers directory checked first: `papers/oai_first_proof.pdf`.
- Local extraction tooling is unavailable in this environment (`pdftotext` and `pdfinfo` not installed).
- This round reuses local paper memory and prior cached references; no external search was required.

## Admissibility gate snapshot
```json
{
  "checks": [
    {
      "denominator": 7,
      "i": 0,
      "numerator": 100947,
      "quotient": 14421,
      "remainder": 0
    },
    {
      "denominator": 6,
      "i": 1,
      "numerator": 26334,
      "quotient": 4389,
      "remainder": 0
    },
    {
      "denominator": 5,
      "i": 2,
      "numerator": 5985,
      "quotient": 1197,
      "remainder": 0
    },
    {
      "denominator": 4,
      "i": 3,
      "numerator": 1140,
      "quotient": 285,
      "remainder": 0
    },
    {
      "denominator": 3,
      "i": 4,
      "numerator": 171,
      "quotient": 57,
      "remainder": 0
    },
    {
      "denominator": 2,
      "i": 5,
      "numerator": 18,
      "quotient": 9,
      "remainder": 0
    }
  ],
  "divisibility_failures": [],
  "expected_block_count": 14421,
  "instance": {
    "n": 23,
    "q": 7,
    "r": 6
  },
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 14421,
    "lambda_1": 4389,
    "lambda_2": 1197,
    "lambda_3": 285,
    "lambda_4": 57,
    "lambda_5": 9
  }
}
```

## Proof-first round1 stack (mandatory)

### Seed 1: asymptotic existence skeleton
- High-level idea: use divisibility as a gateway, then approximate decomposition plus absorption-style closure.
- Solve-attempt: convert this into concrete obligations (approximate coverage, bounded residual, absorber closure).
- Current critical gap: asymptotic threshold constants are not instantiated for `n=23`.

### Seed 2: finite-size bridge via PBD/Wilson-style decomposition
- High-level idea: bridge from asymptotic claims to finite `n` using decomposition scaffolding.
- Solve-attempt: define this as fallback proof lane when Seed 1 has finite-size ambiguity.
- Current critical gap: no explicit bridge decomposition has been instantiated for this exact triple.

### Seed 3: symmetry-compressed exact-cover lane
- High-level idea: orbit compression can reduce exact-cover size enough to become tractable.
- Solve-attempt: make this a strict front gate with cyclic/dihedral probes and coefficient histogram checks.
- Current critical gap: prior runs show non-binary coefficient inflation for larger `r`; weighted fallback is required.

### Seed 4: pressure-monitored random nibble lane
- High-level idea: nibble handles bulk coverage; handoff before `(r-1)` saturation hardens.
- Solve-attempt: define handoff trigger by acceptance-rate decay and pressure-tail growth.
- Current critical gap: thresholds need first pilot calibration on this instance.

### Seed 5: absorber-plus-micro-augment closure lane
- High-level idea: reserve absorber capacity, then use motif-coupled micro-augments for sparse late gains.
- Solve-attempt: transfer prior `1->2` strict-gain behavior into a closure lane with canonical motif dedup.
- Current critical gap: absorber template construction for `S(6,7,23)` remains to be formalized.

## Critical-gap verification loop (up to 3 rounds)
1. Round-loop A: arithmetic and consistency check
- Verify integrality, replication numbers, and target block count.
- Exit rule: fail fast if any divisibility condition breaks.
2. Round-loop B: engine-compatibility check
- Run bounded symmetry diagnostics; measure compression ratio and non-binary share.
- Exit rule: if compression is weak or non-binary mass is material, switch early to randomized lane.
3. Round-loop C: closure feasibility check
- Require strict feasibility and small residual before residual exact-cover.
- Exit rule: if residual remains large, continue repair/absorber passes and defer exact cover.

## Typeset-ready final proof outline
1. Proposition 1 (Admissibility): all necessary divisibility conditions hold for `S(6,7,23)`.
2. Lemma 2 (Bounded engine dichotomy): bounded symmetry probes either produce a tractable compressed exact-cover or justify immediate fallback.
3. Lemma 3 (Monotone repair regime): under strict feasibility gates, accepted repair moves preserve hard constraints and improve coverage potential.
4. Lemma 4 (Residual closure condition): absorber-reserve plus micro exact-cover closes only when uncovered residual is below threshold.
5. Theorem schema (operational): combining 1-4 yields a finite proof/search protocol with explicit failure certificates at each gate.

## Strong search stack (mandatory)
1. Hard admissibility/divisibility gate.
- Recompute all `lambda_i` and expected block count first.
- Reject instance if any integrality check fails.
2. Symmetry/Kramer-Mesner exact-cover mode (bounded front gate).
- Run cyclic/dihedral orbit diagnostics with coefficient histograms.
- Keep lane only when compression is strong and coefficients are mostly binary.
3. General randomized construction mode.
- `nibble -> boosting/repair -> absorber -> residual exact-cover`.
- Treat residual exact-cover as a late microphase only.

## Engine-selector rubric (concise)
- Symmetry/orbit compression is plausible when compression is strong (`>=10x`), non-binary coefficients are rare, and bounded probes show early constructive movement.
- General randomized construction is better when orbit compression is weak, non-binary coefficients are material, or `(r-1)` pressure plateaus appear quickly.

## Practice-log failures -> research deltas (mandatory)
1. Blocker seen in rounds 2-5: binary-only symmetry probes stall under non-binary orbit coefficients.
- Source likely to address it: Kramer-Mesner weighted orbit systems (`https://www.sciencedirect.com/science/article/pii/0097316586900944`).
- Concrete implementation change: after bounded binary probe failure, invoke weighted-orbit micro-ILP neighborhood generation.
2. Blocker seen in rounds 2-5: add-only growth plateaus at saturated `(r-1)` faces.
- Source likely to address it: iterative absorption pipeline (`https://arxiv.org/abs/1611.06827`).
- Concrete implementation change: pressure-triggered early handoff from nibble/add-only to motif-targeted destroy/repack.
3. Blocker seen in rounds 2-5: sparse augment success with heavy duplicate neighborhood replay.
- Source likely to address it: symmetry-aware canonicalization practice from prior cache (`https://digitalcommons.mtu.edu/michigantech-p2/2010/`).
- Concrete implementation change: canonical motif signatures plus short motif-taboo to reduce duplicate local exact attempts.

## Reuse vs genuinely new (explicit)
- Reused from prior runs:
  - hard admissibility gate before expensive search,
  - symmetry front gate with quick fallback discipline,
  - strict invariants (`overcovered=0`, no `(r-1)` oversubscription).
- Genuinely new in this round:
  - five-seed proof-first stack for `S(6,7,23)` with per-seed solve-attempt and gap,
  - explicit 3-loop critical-gap verification protocol,
  - typeset-ready theorem/lemma skeleton tied to switch gates,
  - finite-size warning integrated directly into the proof plan.

## Rounds 2+ execution summary and metric contract (mandatory)

### Execution order
1. Round 2 (`S(6,7,23)`): run full Stage A/B/C stack and calibrate thresholds.
2. Round 3 (`S(7,8,20)`): reuse calibrated switch logic; test weighted-orbit fallback only in bounded windows.
3. Round 4 (`S(8,9,21)`): bias toward randomized lane after short symmetry gate.
4. Round 5 (`S(9,10,22)`): treat symmetry mostly diagnostic; focus on repair and absorber lane.

### Stage protocol for each round
1. Stage A: hard gate and sizing (`lambda_i`, target block count).
2. Stage B: bounded symmetry gate (cyclic/dihedral probes + coefficient diagnostics).
3. Stage C: randomized lane (`nibble -> boosting/repair`) with pressure-triggered handoff.
4. Stage D: absorber-reserved repair and motif-coupled micro-augments.
5. Stage E: residual exact-cover only when residual is small and strict feasibility holds.

### Metrics to track at every checkpoint
- Point degree: `min`, `max`, `gap`.
- `(r-1)` pressure: max load, cap-count, oversubscribed count.
- Coverage quality: `exact_once`, `uncovered`, `overcovered`.
- Efficiency: accepted-move rate, gain per 1000 trials, micro-augment hit rate.

## External references used (minimal)
- New links introduced in this round: `0`.
- Reused cached links:
  - `https://arxiv.org/abs/1401.3665`
  - `https://arxiv.org/abs/1611.06827`
  - `https://www.sciencedirect.com/science/article/pii/0097316586900944`

## Plan
- Build a reusable knowledge cache for unknown large Steiner systems.
- Keep strict admissibility as a hard gate.
- Define when to use symmetry/exact-cover vs nibble/absorption engines.
- Add new references only if practice blockers expose uncovered gaps.

## Work log
- Completed mandatory cross-run reads before any new search.
- Performed local-paper-first check; extraction tooling unavailable, so reused local notes.
- Wrote proof-first stack, strong search stack, and transfer-ready rounds2+ protocol.

## Observations
- The primary risk is not admissibility; it is finite-size closure under sparse late-stage gains.
- Prior solve rounds support quick symmetry triage and early pressure-aware handoff.
- For this instance size, proof obligations should stay operational and falsifiable rather than asymptotic-only.

## Core advance
- advance statement:
  - Converted round1 into a proof-first, gate-explicit execution contract for `S(6,7,23)` with five seeded proof lanes and a 3-loop gap verification routine.
- evidence from this round (metrics, runtime, structure):
  - Mandatory cross-run memory and local-paper-first requirements were completed.
  - Strong search stack and concise engine selector were formalized for immediate round2 use.
  - Practice blockers now map to source-backed implementation deltas.
- transfer value for next rounds:
  - Rounds2+ can execute without re-deriving proof/search structure.
  - Each stage has explicit stop/switch criteria and required metrics.

## Next-hypothesis
- hypothesis statement:
  - For `S(6,7,23)`, bounded symmetry triage plus pressure-triggered early repair handoff will beat prolonged symmetry-only or add-only runs while preserving strict feasibility.
- mechanism (why this should help):
  - Practice history shows plateau formation at saturated `(r-1)` motifs and diminishing additive returns; early handoff targets the actual bottleneck.
- expected metric movement:
  - Improved uncovered reduction slope per fixed trial budget,
  - reduced point-degree gap and `(r-1)` cap-tail concentration,
  - keep `overcovered=0` and zero `(r-1)` oversubscription.
- falsification / stop condition:
  - Reject this hypothesis if three matched seeds show no improvement in uncovered reduction rate versus add-only baseline.
