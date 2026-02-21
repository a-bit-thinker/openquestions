# Global Research Log (Round1 Knowledge)

Generated (UTC): 2026-02-21T14:40:44.324040+00:00
Log root: steiner_logs
Current run dir: /root/openquestions/steiner_logs/run_20260221_143916

## Intent
- Aggregate all run round1 knowledge to avoid repeated essay loops.
- Keep reasoning/proof structure primary; keep links as supporting evidence only.

## Raw Redundancy
- Per-run round logs remain as source of truth under `run_*/notes/round_0001_notes.md`.

### run_20260219_025532 / round_0001
- Metrics: score=0 valid=? exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Build a reusable knowledge cache for unknown large Steiner systems.
  - Focus on existence conditions and practical construction heuristics.

### run_20260219_030101 / round_0001
- Metrics: score=0 valid=? exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Established a high-signal reference base and converted it into a concrete rounds-2+ strategy for `r=6..9`.
  - For admissible large instances with `r=6..9`, an iterative-absorption workflow with monitored nibble phases and multi-start restarts will outperform naive exact/monolithic construction attempts.
  - The strongest consistent message is asymptotic: admissibility conditions are non-negotiable and should be enforced before any heavy search.
  - Practical construction is not one-shot exact solving; it is a pipeline where random greedy handles the bulk and structured absorption/trades finish.
  - Randomization should be treated as a first-class strategy: multiple short-to-medium runs with diagnostics likely dominate one long run.
  - Searched arXiv/web for large Steiner-system existence and constructions.
  - Collected primary sources: Keevash (existence/short proof/counting), iterative absorption (Glock-Kuehn-Lo-Osthus), classical nibble/packing papers, Wilson baseline.
  - Translated literature into concrete operational choices for subsequent rounds.

### run_20260219_180444 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Converted this run from generic notes into a concrete, source-grounded execution program:
  - strong search stack,
  - engine-selector rubric,
  - next-round plan with measurable gates.
  - Hypothesis A (symmetry-first): if orbit compression is strong, KM+basis reduction can beat randomized construction for `r=6,7` and may remain viable at `r=8`.
  - Hypothesis B (randomized-first): if no strong group action appears, nibble+boosting+absorber with residual exact-cover is the only scalable path for `r>=8`.
  - Current instance `S(6,7,17)` is admissible and internally consistent (`lambda_1=728`, `lambda_5=6`).
  - Admissibility is necessary only; source evidence strongly favors either:
- Reference-to-proof mapping:
  - Built and documented a strong search stack in `../KNOWLEDGE_CACHE.md`:
  - 1) hard admissibility/divisibility gate,
  - 2) symmetry/Kramer-Mesner exact-cover mode,
  - 3) nibble -> boosting/repair -> absorber -> residual exact-cover mode.

### run_20260220_183105 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - advance statement: Established a dual-engine search strategy with a mandatory divisibility gate and phase-structured randomized completion.
  - Structure: hard gate + symmetry mode + randomized mode now explicitly specified.
  - Metrics selected for rounds 2+: point degree, `(r-1)`-pressure, uncovered/overcovered counts.
  - Source support: Keevash + iterative absorption + Kramer-Mesner + DLX references linked.
  - Future rounds can run measurable experiments instead of ad hoc search.
  - Engine switching condition is now explicit and testable.
  - hypothesis statement: A hybrid policy (symmetry pre-scan, then randomized iterative absorption, then residual DLX) will dominate single-engine attempts for `r=6..9`.
  - mechanism (why this should help): orbit compression wins when structure exists; randomized absorption handles unstructured bulk; DLX resolves only tiny residue.

### run_20260220_215736 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - advance statement: Established a concrete dual-engine construction stack with explicit selector rules and measurable diagnostics.
  - evidence from this round (metrics, runtime, structure): Admissibility snapshot confirmed; six high-value references mapped to direct implementation consequences for `r=6..9`.
  - transfer value for next rounds: Future rounds can execute immediately without re-deriving theory-to-implementation links.
  - hypothesis statement: Early symmetry triage plus pressure-aware seed selection will dominate either single-engine baseline.
  - mechanism (why this should help): It avoids expensive wrong-engine runs and filters randomized trajectories before hard local bottlenecks harden.
  - expected metric movement: Lower high-quantile `(r-1)` pressure, reduced overcoverage, smaller residual exact-cover instance.
  - falsification / stop condition: If symmetry compression is weak and pressure tails stay high across many seeds, switch to absorber-heavy randomized path only.
  - Current instance is admissible, so downstream quality is now engine-dependent.
- Reference-to-proof mapping:
  - Added high-signal references for:
  - asymptotic existence + divisibility gate,
  - iterative absorption pipeline,
  - lattice-constrained decomposition,

### run_20260220_222225 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Build a reusable knowledge cache for unknown large Steiner systems.
  - Keep strict admissibility as a hard gate.
  - Define when to use symmetry/exact-cover vs nibble/absorption engines.

### run_20260220_222329 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Build a reusable knowledge cache for unknown large Steiner systems.
  - Keep strict admissibility as a hard gate.
  - Define when to use symmetry/exact-cover vs nibble/absorption engines.

### run_20260220_222441 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Converted prior heuristic policy into a source-backed, transfer-ready dual-engine protocol with explicit switch rules and per-`r` consequences.
  - Mandatory cross-run reads completed first, then targeted paper search.
  - Added six primary sources to the cache and linked each to concrete implementation actions for `r=6,7,8,9`.
  - Captured round-2+ stage execution order and mandatory metric set.
  - Next rounds can execute directly from the stage protocol without re-deriving theory.
  - Engine selection now has explicit criteria instead of ad-hoc switching.
  - A fixed symmetry budget plus early fallback into absorber-aware repair will outperform symmetry-heavy attempts on `r=8,9` while preserving strict feasibility.
  - Prior diagnostics show non-binary orbit inflation at larger `r`; longer symmetry search has low marginal value compared with repair passes that directly reduce uncovered mass.

### run_20260221_011431 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Build a reusable knowledge cache for unknown large Steiner systems.
  - Keep strict admissibility as a hard gate.
  - Define when to use symmetry/exact-cover vs nibble/absorption engines.
  - Add new references only if practice logs expose a gap not already covered in global research log.

### run_20260221_013905 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Converted round-1 research into a blocker-driven execution contract: bounded symmetry gate, monitored randomized pipeline, weighted-orbit fallback, and explicit handoff triggers.
  - Mandatory cross-run files were read first.
  - Added five web/arXiv references tied to explicit `r=6..9` consequences.
  - Captured round-2+ stage order and metric requirements with concrete switch signals.
  - Future rounds can execute without re-deriving engine choice rules.
  - Practice blockers now map directly to source-backed implementation changes.
  - A short symmetry front gate plus pressure-triggered early handoff to motif-targeted reserve-aware repair will outperform longer symmetry-heavy or additive-only runs for `r=8,9`, while preserving strict feasibility for all `r=6..9`.
  - Practice logs show plateaus at saturated `(r-1)` motifs and sparse augmenting moves; early switch avoids wasting budget on structurally mismatched binary-orbit search.

### run_20260221_143515 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Build a reusable knowledge cache for unknown large Steiner systems.
  - Keep strict admissibility as a hard gate.
  - Define when to use symmetry/exact-cover vs nibble/absorption engines.
  - Add new references only if practice logs expose a gap not already covered in global research log.

### run_20260221_143650 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Build a reusable knowledge cache for unknown large Steiner systems.
  - Keep strict admissibility as a hard gate.
  - Define when to use symmetry/exact-cover vs nibble/absorption engines.
  - Add new references only if practice logs expose a gap not already covered in global research log.

### run_20260221_143722 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Build a reusable knowledge cache for unknown large Steiner systems.
  - Keep strict admissibility as a hard gate.
  - Define when to use symmetry/exact-cover vs nibble/absorption engines.
  - Add new references only if practice logs expose a gap not already covered in global research log.

### run_20260221_143916 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Build a reusable knowledge cache for unknown large Steiner systems.
  - Keep strict admissibility as a hard gate.
  - Define when to use symmetry/exact-cover vs nibble/absorption engines.
  - Add new references only if practice logs expose a gap not already covered in global research log.

## URL Index (secondary)
- intentionally minimized
