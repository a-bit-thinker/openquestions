# Round 1 Notes (Research-Only)

## Research (this round)
- URL: https://arxiv.org/abs/1401.3665
  Takeaway: Asymptotic existence is governed by divisibility/admissibility; constructive viewpoint is probabilistic + absorption.
  Applied change from source: Future rounds should enforce divisibility as a strict pre-filter and use a staged construction mindset.
- URL: https://doi.org/10.48550/arXiv.1611.06827
  Takeaway: Iterative absorption provides a practical architecture (nibble -> boosting/greedy cover -> absorber-based completion).
  Applied change from source: Round planning should include reserved absorber resources from the start, not as a post-hoc patch.
- URL: https://doi.org/10.1016/S0195-6698(85)80023-8
  Takeaway: Nibble-style random packing efficiently gets near-complete coverage.
  Applied change from source: Use random greedy for bulk progress and reserve deterministic search for sparse leftovers only.
- URL: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v4i2r19
  Takeaway: Random greedy processes can be monitored via regularity trajectories; stopping too late hurts structure.
  Applied change from source: Add online drift metrics and early-stop thresholds in future randomized runs.

## Plan
- Build a reusable knowledge cache for unknown large Steiner systems.
- Keep round 2+ execution research-driven: prioritize method experiments over certificate output.
- Target `r in {6,7,8,9}` with a fixed experiment ladder (admissibility -> nibble -> absorption/repair -> restart policy).

## Work log
- Searched arXiv/web for large Steiner-system existence and constructions.
- Collected primary sources: Keevash (existence/short proof/counting), iterative absorption (Glock-Kuehn-Lo-Osthus), classical nibble/packing papers, Wilson baseline.
- Translated literature into concrete operational choices for subsequent rounds.

## Observations
- The strongest consistent message is asymptotic: admissibility conditions are non-negotiable and should be enforced before any heavy search.
- Practical construction is not one-shot exact solving; it is a pipeline where random greedy handles the bulk and structured absorption/trades finish.
- Randomization should be treated as a first-class strategy: multiple short-to-medium runs with diagnostics likely dominate one long run.

## Core advance
- Established a high-signal reference base and converted it into a concrete rounds-2+ strategy for `r=6..9`.

## Next-hypothesis
- For admissible large instances with `r=6..9`, an iterative-absorption workflow with monitored nibble phases and multi-start restarts will outperform naive exact/monolithic construction attempts.

## Techniques to try in rounds 2+
1. Admissibility gate first.
   Check all divisibility constraints for the intended Steiner parameters before any search; reject impossible instances immediately.
2. Random greedy nibble as phase A.
   Generate a large partial packing quickly; track uncovered `r`-sets and degree/codegree imbalance online.
3. Early-stop + residual targeting.
   Stop nibble when drift metrics worsen, then isolate sparse leftovers for structured repair.
4. Iterative absorption as phase B.
   Pre-reserve absorber structure and execute completion in stages rather than a single final repair.
5. Local repair operators.
   Use trades/switchings on small substructures to eliminate remaining conflicts/divisibility defects.
6. Multi-start restart schedule.
   Run many randomized trajectories with diversity scoring; keep top candidates by residual size + regularity, then repair.
7. Pairwise sanity layer.
   Use Wilson-style pairwise congruence/projection checks as low-cost invariants while debugging higher-order (`r=6..9`) code.
