# Round 1 Notes (Research-Only)

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

## Strong search stack (mandatory)
1. Hard admissibility/divisibility gate:
- Recompute all `lambda_i` and expected block count before any search.
- Reject instance immediately if any integrality check fails.
2. Symmetry/Kramer-Mesner exact-cover mode (bounded front gate):
- Run short cyclic/dihedral orbit diagnostics first.
- Keep this lane only if orbit compression is strong and coefficients are mostly binary.
3. General randomized construction mode:
- `nibble -> boosting/repair -> absorber -> residual exact-cover`.
- Residual exact-cover is a late microphase, not the global default engine.

## Research (this round, web/arXiv)
1. URL: https://arxiv.org/abs/1401.3665
- Takeaway: divisibility is the hard admissibility backbone; construction still needs explicit algorithmic phases.
- Applied change from source: keep divisibility gate as absolute precondition for `r=6..9`.

2. URL: https://arxiv.org/abs/1611.06827
- Takeaway: iterative absorption gives the right practical sequence for large design construction.
- Applied change from source: keep `nibble -> boosting/repair -> absorber -> residual exact-cover` as the default general pipeline.

3. URL: https://www.sciencedirect.com/science/article/pii/0097316586900944
- Takeaway: orbit/Kramer-Mesner systems naturally generate non-binary coefficients under automorphisms.
- Applied change from source: add weighted-orbit fallback (ILP-style micro-solves) when binary exact-cover assumptions break.

4. URL: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v32i1p17
- Takeaway: random-greedy progress should be monitored with trajectory diagnostics and switched before saturation hardens.
- Applied change from source: add explicit early-stop/handoff triggers from nibble to repair/LNS.

5. URL: https://digitalcommons.mtu.edu/michigantech-p2/2010/
- Takeaway: normalizer/symmetry-aware encoding prunes isomorphic branches in exact-cover style search.
- Applied change from source: canonicalize local exact neighborhoods to avoid repeated isomorphic augmentation trials.

## Engine-selector rubric (concise)
- Choose symmetry/orbit compression when:
  - orbit count shrinks strongly (target at least 10x),
  - non-binary orbit coefficients are rare,
  - bounded probe returns quick progress.
- Choose generalized randomized pipeline when:
  - non-binary orbit coefficients are material,
  - symmetry probes stall in bounded budget,
  - `(r-1)` pressure motifs dominate failures.

## Reuse vs genuinely new (explicit)
- Reused from prior runs:
  - hard admissibility gate before heavy search,
  - symmetry-front-gate then quick fallback discipline,
  - strict-feasible invariants from solve rounds (`overcovered=0`, no `(r-1)` oversubscription).
- Genuinely new in this round:
  - blocker-driven source additions targeting non-binary orbit failure and nibble saturation,
  - explicit weighted-orbit fallback when KM coefficients are non-binary,
  - explicit nibble early-stop/handoff policy tied to pressure diagnostics,
  - concise engine-selector rubric keyed to observed run-time diagnostics.

## Practice-log failures -> research deltas (mandatory)
1. Blocker from rounds 2-5: symmetry probe frequently stalls once non-binary orbit coefficients appear (especially larger `r`).
- Source likely to address blocker: https://www.sciencedirect.com/science/article/pii/0097316586900944
- Concrete implementation change: after bounded binary probe fails, switch to weighted-orbit micro-ILP candidate generation instead of extending binary-only DFS.

2. Blocker from rounds 2-5: additive-only growth plateaus near saturated `(r-1)` faces.
- Source likely to address blocker: https://arxiv.org/abs/1611.06827 and https://www.combinatorics.org/ojs/index.php/eljc/article/view/v32i1p17
- Concrete implementation change: enforce early handoff from nibble/additive stage to motif-targeted destroy/repack with reserve-first refill.

3. Blocker from rounds 2-5: exact local augmentation gives sparse gains and many duplicate neighborhoods.
- Source likely to address blocker: https://digitalcommons.mtu.edu/michigantech-p2/2010/
- Concrete implementation change: canonicalize/deduplicate motif neighborhoods by symmetry signature before running local exact augmentation.

## Per-r implementation consequences (explicit)
- `r=6`: symmetry lane remains viable if orbit matrix stays mostly binary; otherwise run short nibble then targeted repair.
- `r=7`: same architecture, but add coefficient-histogram trigger and stronger motif-aware augmentation.
- `r=8`: default to randomized pipeline after short symmetry gate; weighted-orbit tools only for small residuals.
- `r=9`: symmetry is diagnostic-only unless exceptional compression appears; rely on repeated reserve-aware repair passes.

## Rounds 2+ execution and metrics (mandatory)
1. Stage A: hard gate and sizing
- Recompute divisibility and `lambda_i`.
- Fix target block count and cap constraints.
2. Stage B: symmetry/Kramer-Mesner front gate (bounded)
- Run cyclic/dihedral diagnostics and short probe.
- Record orbit compression ratio, non-binary share, `max_coeff`, and probe outcome.
3. Stage C: general randomized pipeline
- Multi-seed nibble with early-stop triggers.
- Boosting/repair with reserve-first refill and hard feasibility gates.
- Maintain absorber reserve while reducing uncovered mass.
4. Stage D: residual exact-cover microphase
- Run only when uncovered is sufficiently small and strict feasibility holds.
- Use canonicalized neighborhoods and weighted-orbit options if non-binary coefficients persist.
5. Metrics to track at every checkpoint
- Coverage: `exact_once`, `uncovered`, `overcovered`.
- Point degree: `min`, `max`, `gap`.
- `(r-1)` pressure: `max load`, target `lambda_(r-1)`, count at cap, oversubscribed count.
- Search efficiency: accepted neighborhoods, gain per 100 accepts, micro exact success rate.
- Symmetry diagnostics: orbit counts, binary/non-binary column counts, `max_coeff`.

## Plan
- Build a reusable knowledge cache for unknown large Steiner systems.
- Keep strict admissibility as a hard gate.
- Define when to use symmetry/exact-cover vs nibble/absorption engines.
- Add new references only if practice logs expose a gap not already covered in global research log.

## Work log
- Completed mandatory cross-run memory read before any web/arXiv search.
- Queried targeted sources for the two recurring blockers: non-binary orbit coefficients and `(r-1)`-cap plateaus.
- Added five high-value sources and mapped each to explicit implementation consequences for `r=6,7,8,9`.
- Wrote transfer-ready stage protocol and metric contract for rounds 2+.

## Observations
- Cross-run solve logs show consistent strict-feasible progress but repeated plateau behavior.
- The most repeatable failure mode is not admissibility; it is wrong-engine persistence after symmetry diagnostics fail.
- Early handoff plus motif-targeted repair is the highest-signal change supported by both practice logs and sources.

## Core advance
- advance statement:
  - Converted round-1 research into a blocker-driven execution contract: bounded symmetry gate, monitored randomized pipeline, weighted-orbit fallback, and explicit handoff triggers.
- evidence from this round (metrics, runtime, structure):
  - Mandatory cross-run files were read first.
  - Added five web/arXiv references tied to explicit `r=6..9` consequences.
  - Captured round-2+ stage order and metric requirements with concrete switch signals.
- transfer value for next rounds:
  - Future rounds can execute without re-deriving engine choice rules.
  - Practice blockers now map directly to source-backed implementation changes.

## Next-hypothesis
- hypothesis statement:
  - A short symmetry front gate plus pressure-triggered early handoff to motif-targeted reserve-aware repair will outperform longer symmetry-heavy or additive-only runs for `r=8,9`, while preserving strict feasibility for all `r=6..9`.
- mechanism (why this should help):
  - Practice logs show plateaus at saturated `(r-1)` motifs and sparse augmenting moves; early switch avoids wasting budget on structurally mismatched binary-orbit search.
- expected metric movement:
  - `r=6,7`: modest but consistent block-count gains from symmetry-aided local exact neighborhoods.
  - `r=8,9`: larger uncovered reduction at fixed budget via earlier repair entry and better motif targeting.
  - Maintain `overcovered=0` and zero `(r-1)` oversubscription.
- falsification / stop condition:
  - Reject if bounded symmetry probes produce better gain-per-time than early repair across at least three matched seeds, or if early handoff does not improve uncovered reduction rate over baseline.
