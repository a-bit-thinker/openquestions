# Round 1 Notes (Research-Only)

Instance: S(6,7,17)
Expected blocks: 1768

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: steiner_logs/run_20260220_222441/REPO_WIDE_HISTORY.md
- Latest prior run: run_20260220_222329
- Latest prior round1 notes source run: run_20260220_222329
- Latest prior round1 notes: steiner_logs/run_20260220_222329/notes/round_0001_notes.md
- Latest prior round5 notes source run: run_20260220_183105
- Latest prior round5 notes: steiner_logs/run_20260220_183105/notes/round_0005_notes.md
- Latest prior transfer: steiner_logs/run_20260220_222329/NEXT_GENERATION_TRANSFER.md

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

## Research (this round)
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

## Reuse vs genuinely new (explicit)
- Reused from prior runs:
  - hard admissibility gate before any heavy search,
  - symmetry-front-gate then fallback policy,
  - strict feasibility invariants (`overcovered=0`, `(r-1)` oversubscription `=0`) from strict-feasible LNS rounds.
- Genuinely new in this round:
  - web/arXiv-backed source grounding for each engine stage,
  - explicit per-`r` (`6,7,8,9`) implementation consequences captured in `KNOWLEDGE_CACHE.md`,
  - concise engine-selector rubric with practical switch conditions.

## Rounds 2+ execution and metrics (mandatory)
1. Stage A: hard gate and instance sizing
- Recompute divisibility/replication numbers and expected block count.
- Reject/skip if any `lambda_i` integrality fails.

2. Stage B: symmetry/Kramer-Mesner front gate (bounded)
- Try cyclic/dihedral first; add richer group only if orbit compression is strong.
- Track: orbit row/column counts, binary vs non-binary orbit coefficients, bounded exact-cover probe outcome.
- If non-binary coefficients dominate or probe stalls, switch immediately.

3. Stage C: general randomized pipeline
- Run multi-seed nibble/additive boosting for strict-feasible initializer.
- Run reserve-aware repair/LNS passes with hard move gates.
- Keep absorber reserve logic active throughout repair.

4. Stage D: residual exact-cover microphase
- Attempt only when `uncovered` is small and strict feasibility remains intact.
- Use symmetry-aware branch ordering / meet-in-the-middle only on residual subinstance.

5. Metrics to track every checkpoint
- Coverage: `exact_once`, `uncovered`, `overcovered`.
- Point degree: `min`, `max`, and `gap`.
- `(r-1)` pressure: `max load`, `target lambda_(r-1)`, count at cap, oversubscribed count.
- Search health: accepted neighborhoods, gain per 100 accepts, residual exact probe success/fail.

## Plan
- Build a reusable knowledge cache for unknown large Steiner systems.
- Keep strict admissibility as a hard gate.
- Define when to use symmetry/exact-cover vs nibble/absorption engines.

## Work log
- Read mandatory cross-run memory files before any web search.
- Added a source-backed strong search stack and engine selector.
- Mapped source consequences to each target level `r in {6,7,8,9}`.
- Converted round notes and transfer artifacts into round-2+ executable protocol.

## Observations
- Prior strict-feasible optimization rounds show that feasibility invariants can stay intact while coverage improves steadily.
- Symmetry remains valuable as a front diagnostic, but non-binary orbit coefficients are a recurring reason to switch engines quickly.
- Nibble-only growth is not sufficient near plateaus; planned absorber-aware repair is the higher-confidence route.

## Core advance
- advance statement:
  - Converted prior heuristic policy into a source-backed, transfer-ready dual-engine protocol with explicit switch rules and per-`r` consequences.
- evidence from this round (metrics, runtime, structure):
  - Mandatory cross-run reads completed first, then targeted paper search.
  - Added six primary sources to the cache and linked each to concrete implementation actions for `r=6,7,8,9`.
  - Captured round-2+ stage execution order and mandatory metric set.
- transfer value for next rounds:
  - Next rounds can execute directly from the stage protocol without re-deriving theory.
  - Engine selection now has explicit criteria instead of ad-hoc switching.

## Next-hypothesis
- hypothesis statement:
  - A fixed symmetry budget plus early fallback into absorber-aware repair will outperform symmetry-heavy attempts on `r=8,9` while preserving strict feasibility.
- mechanism (why this should help):
  - Prior diagnostics show non-binary orbit inflation at larger `r`; longer symmetry search has low marginal value compared with repair passes that directly reduce uncovered mass.
- expected metric movement:
  - `r=6,7`: better early exact-once growth from selective symmetry wins.
  - `r=8,9`: lower uncovered at fixed compute budget; maintain `overcovered=0` and `oversubscribed_(r-1)=0`.
- falsification / stop condition:
  - Reject the hypothesis if bounded symmetry probes consistently produce high-quality binary reductions (or exact progress) for `r=8,9` within the same budget.
