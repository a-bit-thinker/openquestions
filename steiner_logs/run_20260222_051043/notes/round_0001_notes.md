# Round 1 Notes (Research-Only)

Instance: `S(6,8,29)`
Expected blocks: `16965`
Date (UTC): `2026-02-22`

## Cross-run bootstrap (mandatory first read, completed before any new search)
- `steiner_logs/PAPER_NOTES.md`
- `steiner_logs/RESEARCH_LOG.md`
- `steiner_logs/PRACTICE_LOG.md`
- `steiner_logs/RESEARCH_PAPER.md`
- `steiner_logs/EXISTENCE_FRONTIER.md`
- `steiner_logs/run_20260222_051043/REPO_WIDE_HISTORY.md`
- `steiner_logs/run_20260222_012007/notes/round_0001_notes.md`
- `steiner_logs/run_20260222_012007/notes/round_0005_notes.md`
- `steiner_logs/run_20260222_012007/NEXT_GENERATION_TRANSFER.md`

## Local-paper-first check (completed)
- Local papers were checked before any web search: `papers/oai_first_proof.pdf`.
- Local PDF text extraction tools are unavailable in this environment (`pdftotext`, `pdfinfo`, `mutool`, `gs` not installed).
- This round therefore reuses the local-paper memory plus prior cached references; external links were not expanded.

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

## Proof-first Round-1 stack (mandatory)

### Seed 1: asymptotic existence spine
- High-level idea: divisibility + pseudorandom approximate decomposition + absorption implies existence in large regimes.
- Solve-attempt in this run: make this a theorem template with explicit finite-size obligations for `n=29` rather than a direct certificate attempt.
- Critical gap: asymptotic constants are not instantiated for this exact finite triple.

### Seed 2: finite bridge via PBD/Wilson decomposition
- High-level idea: move from asymptotic statements to finite `n=29` by decomposition into manageable local pieces.
- Solve-attempt in this run: define bridge obligations as explicit lemmas (local balance, compatibility, recomposition).
- Critical gap: no explicit bridge construction for `S(6,8,29)` is currently instantiated in repo artifacts.

### Seed 3: symmetry-compressed Kramer-Mesner lane
- High-level idea: if orbit compression is strong, exact-cover on orbit incidence can become tractable.
- Solve-attempt in this run: keep symmetry lane as a bounded front gate with coefficient histogram diagnostics and weighted fallback.
- Critical gap: practice history shows non-binary orbit inflation can stall binary-only KM.

### Seed 4: pressure-aware nibble lane
- High-level idea: random greedy covers bulk `6`-subsets quickly, but must hand off before `(r-1)` tails harden.
- Solve-attempt in this run: define measurable handoff triggers (accept-rate decay, cap-tail growth, stagnant uncovered slope).
- Critical gap: trigger thresholds require first matched-budget calibration on `S(6,8,29)`.

### Seed 5: absorber + motif-coupled repair lane
- High-level idea: reserve sparse flexibility early, then perform strict local repacks (`k -> k+1`) in hotspot neighborhoods.
- Solve-attempt in this run: convert prior successful strict LNS behavior into a closure lemma with motif canonicalization.
- Critical gap: absorber template library for this instance family is missing.

## Critical-gap verification loop (up to 3 rounds)
1. Loop A (arithmetic consistency)
- Verify all divisibility checks, `lambda_i`, and expected block count.
- Status now: pass (`is_admissible=true`).
- Exit rule: fail immediately if any remainder is non-zero.

2. Loop B (engine compatibility)
- Run bounded symmetry diagnostics (`compression ratio`, `non-binary column share`, `max coefficient`).
- Status now: pending execution in solve rounds.
- Exit rule: if compression is weak or non-binary mass is material, route to randomized lane.

3. Loop C (closure eligibility)
- Require strict feasibility (`overcovered=0`, no `(r-1)` oversubscription) plus small residual before exact-cover closure.
- Status now: defined as gate, not executed in round1.
- Exit rule: if residual is large, continue repair/absorber passes and defer residual exact cover.

## Typeset-ready final proof outline
1. Proposition 1 (Admissibility): all divisibility constraints for `S(6,8,29)` hold and produce integer replication numbers `lambda_0..lambda_5`.
2. Lemma 2 (Finite bridge obligation): if a finite decomposition scaffold satisfies local balance constraints, then it can host a valid Steiner completion skeleton.
3. Lemma 3 (Engine dichotomy): bounded orbit diagnostics either produce a tractable symmetry-compressed exact-cover instance or certify fallback to randomized construction.
4. Lemma 4 (Monotone strict repair): under hard constraints (`c_6<=1`, `c_5<=8`), accepted local moves preserve feasibility and weakly reduce residual pressure.
5. Lemma 5 (Residual closure threshold): exact residual closure is valid only below an explicit uncovered-mass threshold.
6. Theorem schema (operational): combining 1-5 yields a finite proof/search protocol with gate-specific failure certificates.

## Strong search stack (mandatory)
1. Hard admissibility/divisibility gate.
- Recompute all `lambda_i` and expected block count before any heavy search.
- Reject instance immediately on any integrality failure.

2. Symmetry/Kramer-Mesner exact-cover mode (bounded front gate).
- Run cyclic/dihedral orbit diagnostics and coefficient histograms.
- Keep this mode only if compression is strong and weighted coefficients remain controllable.

3. `nibble -> boosting/repair -> absorber -> residual exact-cover` mode.
- Nibble for bulk coverage.
- Boosting/repair for strict improvement under cap constraints.
- Absorber-reserved local repacks for late sparse gains.
- Residual exact-cover only as late microphase when residual gate is passed.

## Engine-selector rubric (concise)
- Use symmetry/orbit compression when bounded probes show high compression (`>=10x` candidate shrink) and low non-binary mass (`<=2%` columns with coefficient `>1`).
- Use general randomized construction when compression is weak, non-binary mass is high, or `(r-1)` pressure tails rise early.

## Practice-log failures -> research deltas (mandatory)
1. Blocker seen in rounds2-5: binary-only orbit search stalls when non-binary coefficients appear.
- Source that may address it: Kramer-Mesner weighted orbit formulation (`https://www.sciencedirect.com/science/article/pii/0097316586900944`).
- Concrete implementation change: add weighted-orbit micro-ILP neighborhoods after bounded binary probe failure.

2. Blocker seen in rounds2-5: add-only growth plateaus at saturated `(r-1)` motifs.
- Source that may address it: iterative absorption framework (`https://arxiv.org/abs/1611.06827`).
- Concrete implementation change: pressure-triggered early handoff from add-only to destroy/repack with reserved slack.

3. Blocker seen in rounds2-5: residual exact-cover invoked too early with huge uncovered mass.
- Source that may address it: asymptotic decomposition + absorption discipline (`https://arxiv.org/abs/1401.3665`).
- Concrete implementation change: enforce residual exact-cover eligibility gate (e.g., uncovered fraction threshold + strict feasibility).

## Reuse vs genuinely new (explicit)
- Reused from prior runs:
  - hard admissibility-first gate,
  - bounded symmetry front gate with fast fallback,
  - strict feasibility invariants (`overcovered=0`, no `(r-1)` oversubscription),
  - staged constructive pipeline ending in residual exact-cover gate.

- Genuinely new in this round:
  - proof-first stack rewritten for `S(6,8,29)` with five explicit proof seeds,
  - critical-gap verification loop specialized for this instance,
  - typeset-ready lemma chain includes finite-size bridge obligation for `n=29`,
  - blocker-to-source-to-implementation mapping tied directly to observed rounds2-5 failure modes.

## Rounds 2+ execution summary and metrics contract (mandatory)

### Execution order
1. Round 2 (`S(6,8,29)`): run full Stage A/B/C/D/E with matched-seed calibration of handoff thresholds.
2. Round 3 (`S(7,8,24)`): re-use calibrated trigger logic; symmetry gate remains bounded.
3. Round 4 (`S(8,9,21)`): expect randomized lane dominance unless symmetry compression is unusually strong.
4. Round 5 (`S(9,10,22)`): keep symmetry seed if cyclic diagnostics remain tractable, then strict LNS.

### Stage protocol for every solve round
1. Stage A: divisibility and sizing gate (`lambda_i`, expected block count).
2. Stage B: bounded symmetry diagnostics and optional orbit-seeded build.
3. Stage C: randomized nibble + strict boosting/repair.
4. Stage D: absorber-reserved motif-coupled local repacks.
5. Stage E: residual exact-cover only after strict residual eligibility.

### Metrics to track at every checkpoint
- Point degree: `min`, `max`, and `gap`.
- `(r-1)` pressure: max load, cap-tail counts, oversubscribed count.
- Coverage: `exact_once`, `uncovered`, `overcovered`.
- Throughput: accepted-move rate, gain per 1000 trials, micro-augment hit rate.

## External references used (minimal)
- New links introduced in this round: `0`.
- Reused cached links:
  - `https://arxiv.org/abs/1401.3665`
  - `https://arxiv.org/abs/1611.06827`
  - `https://www.sciencedirect.com/science/article/pii/0097316586900944`

## Round-1 links with downloadable PDFs
- New Round-1 links with downloadable PDFs: `none`.
- Saved filenames under `/root/openquestions/papers`: `none`.

## Plan
- Build a reusable knowledge cache for unknown large Steiner systems.
- Keep strict admissibility as a hard gate.
- Define when to use symmetry/exact-cover vs nibble/absorption engines.
- Add new references only when a blocker is not already covered by cached sources.

## Work log
- Completed mandatory cross-run reads before any external search.
- Checked local papers first and confirmed extraction-tool gap.
- Built proof-first and strong-search stacks for `S(6,8,29)`.
- Added blocker-driven implementation deltas from practice logs.

## Observations
- Arithmetic admissibility is not the bottleneck for this instance; finite-size closure and late-stage pressure control are.
- Cross-run practice strongly supports short symmetry triage and early handoff into strict repair when caps tighten.
- Residual exact-cover should remain late and conditional; premature invocation is repeatedly unproductive.

## Core advance
- advance statement:
  - Converted round1 for `S(6,8,29)` into a proof-first, gate-explicit execution contract with five seeded proof lanes and a 3-loop gap verification process.
- evidence from this round (metrics, runtime, structure):
  - Mandatory cross-run memory and local-paper-first constraints were completed.
  - Strong search stack and concise engine-selector rubric were formalized.
  - Practice blockers now map to explicit source-backed implementation changes.
- transfer value for next rounds:
  - Rounds2+ can execute directly from stage gates and metric thresholds.
  - Future runs can avoid repeated round1 essay loops by reusing this contract.

## Next-hypothesis
- hypothesis statement:
  - For `S(6,8,29)`, bounded symmetry triage plus pressure-triggered early repair handoff will outperform prolonged symmetry-only or add-only strategies while keeping strict feasibility.
- mechanism (why this should help):
  - Practice history across `r=6..9` shows add-only plateau and sparse local gains after `(r-1)` saturation; early repair targets this bottleneck.
- expected metric movement:
  - improved uncovered-reduction slope per fixed trial budget,
  - reduced `(r-1)` cap-tail concentration,
  - stable `overcovered=0` and zero `(r-1)` oversubscription.
- falsification / stop condition:
  - Reject if three matched seeds fail to improve uncovered reduction rate vs add-only baseline.
