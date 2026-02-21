# Global Research Log (Round1 Knowledge)

Generated (UTC): 2026-02-21T01:14:34.507924+00:00
Log root: steiner_logs
Current run dir: /root/openquestions/steiner_logs/run_20260221_011431

## Intent
- Aggregate all run round1 knowledge to avoid repeated essay loops.
- Add new references only when practice logs expose new blockers.

## Raw Redundancy
- Per-run round logs remain as source of truth under `run_*/notes/round_0001_notes.md`.

### run_20260219_030101 / round_0001
- Metrics: score=0 valid=? exact_once=0/12376 uncovered=12376 overcovered=0
- Key takeaways:
  - URL: https://arxiv.org/abs/1401.3665
  - Takeaway: Asymptotic existence is governed by divisibility/admissibility; constructive viewpoint is probabilistic + absorption.
  - Applied change from source: Future rounds should enforce divisibility as a strict pre-filter and use a staged construction mindset.
  - URL: https://doi.org/10.48550/arXiv.1611.06827
  - Takeaway: Iterative absorption provides a practical architecture (nibble -> boosting/greedy cover -> absorber-based completion).
  - Applied change from source: Round planning should include reserved absorber resources from the start, not as a post-hoc patch.
  - URL: https://doi.org/10.1016/S0195-6698(85)80023-8
  - Takeaway: Nibble-style random packing efficiently gets near-complete coverage.
  - Applied change from source: Use random greedy for bulk progress and reserve deterministic search for sparse leftovers only.
  - URL: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v4i2r19
  - Takeaway: Random greedy processes can be monitored via regularity trajectories; stopping too late hurts structure.
  - Applied change from source: Add online drift metrics and early-stop thresholds in future randomized runs.
  - Established a high-signal reference base and converted it into a concrete rounds-2+ strategy for `r=6..9`.
  - For admissible large instances with `r=6..9`, an iterative-absorption workflow with monitored nibble phases and multi-start restarts will outperform naive exact/monolithic construction attempts.
  - The strongest consistent message is asymptotic: admissibility conditions are non-negotiable and should be enforced before any heavy search.
  - Practical construction is not one-shot exact solving; it is a pipeline where random greedy handles the bulk and structured absorption/trades finish.
  - Randomization should be treated as a first-class strategy: multiple short-to-medium runs with diagnostics likely dominate one long run.

### run_20260219_180444 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Key takeaways:
  - Built and documented a strong search stack in `../KNOWLEDGE_CACHE.md`:
  - 1) hard admissibility/divisibility gate,
  - 2) symmetry/Kramer-Mesner exact-cover mode,
  - 3) nibble -> boosting/repair -> absorber -> residual exact-cover mode.
  - Added high-value primary references (Keevash I/II, iterative absorption, Wilson, Kramer-Mesner, computational 6/8-design construction papers).
  - Added an engine-selector rubric for when orbit compression is likely to win vs when randomized iterative absorption should be primary.
  - Converted this run from generic notes into a concrete, source-grounded execution program:
  - strong search stack,
  - engine-selector rubric,
  - next-round plan with measurable gates.
  - Hypothesis A (symmetry-first): if orbit compression is strong, KM+basis reduction can beat randomized construction for `r=6,7` and may remain viable at `r=8`.
  - Hypothesis B (randomized-first): if no strong group action appears, nibble+boosting+absorber with residual exact-cover is the only scalable path for `r>=8`.
  - Current instance `S(6,7,17)` is admissible and internally consistent (`lambda_1=728`, `lambda_5=6`).
  - Admissibility is necessary only; source evidence strongly favors either:
  - heavy symmetry compression (KM route), or
  - iterative-absorption pipeline with residual exact cleanup.
  - High-order search should not start without metric instrumentation; blind search will hide bottlenecks.

### run_20260220_183105 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Key takeaways:
  - URL: https://arxiv.org/abs/1401.3665
  - Takeaway: divisibility/integrality is the first hard filter for admissibility.
  - Applied change from source: formalized hard gate as mandatory pre-search invariant.
  - URL: https://arxiv.org/abs/1611.06827
  - Takeaway: iterative absorption stack (nibble -> boosting/repair -> absorber -> completion).
  - Applied change from source: defined randomized engine phases and residual exact-cover handoff.
  - URL: https://eudml.org/doc/247869
  - Takeaway: practical Kramer-Mesner orbit compression with automorphism groups.
  - Applied change from source: added symmetry/orbit-compressed exact-cover mode and viability checks.
  - URL: https://arxiv.org/abs/cs/0011047
  - Takeaway: DLX is an efficient sparse exact-cover backend.
  - Applied change from source: position DLX as residual solver, not global engine for large `r`.
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
- Key takeaways:
  - Added high-signal references for:
  - asymptotic existence + divisibility gate,
  - iterative absorption pipeline,
  - lattice-constrained decomposition,
  - random-threshold completion behavior,
  - symmetry/Kramer-Mesner exact-cover practice.
  - Consolidated a two-engine strategy:
  - symmetry/KM exact-cover,
  - randomized nibble->repair->absorber->residual exact-cover.
  - advance statement: Established a concrete dual-engine construction stack with explicit selector rules and measurable diagnostics.
  - evidence from this round (metrics, runtime, structure): Admissibility snapshot confirmed; six high-value references mapped to direct implementation consequences for `r=6..9`.
  - transfer value for next rounds: Future rounds can execute immediately without re-deriving theory-to-implementation links.
  - hypothesis statement: Early symmetry triage plus pressure-aware seed selection will dominate either single-engine baseline.
  - mechanism (why this should help): It avoids expensive wrong-engine runs and filters randomized trajectories before hard local bottlenecks harden.
  - expected metric movement: Lower high-quantile `(r-1)` pressure, reduced overcoverage, smaller residual exact-cover instance.
  - falsification / stop condition: If symmetry compression is weak and pressure tails stay high across many seeds, switch to absorber-heavy randomized path only.
  - Current instance is admissible, so downstream quality is now engine-dependent.
  - Source consensus supports hybridization: random construction plus deterministic residual closure.
  - Symmetry methods remain high-leverage when orbit compression is strong.

### run_20260220_222441 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Key takeaways:
  - URL: https://arxiv.org/abs/1401.3665
  - Takeaway: divisibility-driven existence backbone for designs (asymptotic).
  - Applied change from source: kept divisibility gate as absolute precondition and documented that small-`n` search still needs explicit computational engines.
  - URL: https://arxiv.org/abs/1611.06827
  - Takeaway: iterative absorption gives the right staged architecture (partial random structure, then controlled completion).
  - Applied change from source: formalized `nibble -> boosting/repair -> absorber -> residual exact-cover` as the default general pipeline.
  - URL: https://www.sciencedirect.com/science/article/pii/S0195669885800457
  - Takeaway: nibble-style random greedy gives high-quality near-packings quickly.
  - Applied change from source: treat nibble as initializer and require planned repair phases rather than add-only continuation.
  - URL: https://www.sciencedirect.com/science/article/pii/S0012365X07003524
  - Takeaway: high-`t` constructions can become tractable under strong automorphism groups via Kramer-Mesner orbit incidence.
  - Applied change from source: retained symmetry/orbit compression as first engine with explicit quick-switch criteria.
  - URL: https://digitalcommons.mtu.edu/michigantech-p2/2010/
  - Takeaway: symmetry-aware meet-in-the-middle and branch-and-bound heuristics materially improve exact search.
  - Applied change from source: reserved as residual micro-solver only after large residual reduction.
  - Converted prior heuristic policy into a source-backed, transfer-ready dual-engine protocol with explicit switch rules and per-`r` consequences.
  - Mandatory cross-run reads completed first, then targeted paper search.
  - Added six primary sources to the cache and linked each to concrete implementation actions for `r=6,7,8,9`.
  - Captured round-2+ stage execution order and mandatory metric set.
  - Next rounds can execute directly from the stage protocol without re-deriving theory.

## Deduplicated URL Index
- none
