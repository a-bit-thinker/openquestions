# Steiner Knowledge Cache

Run ID: 20260220_222441
Created (UTC): 2026-02-20T22:24:41Z

## Reused From Prior Runs (not new in this round)
- Hard admissibility/divisibility gate is mandatory before any search or construction.
- Dual-engine policy already validated: symmetry/orbit compression front gate, then fallback to general randomized + repair pipeline.
- Strict feasibility invariants from prior optimization rounds: keep `overcovered_r_subsets = 0` and keep `(r-1)` load cap (`oversubscribed_(r-1)=0`) at every accepted move.

## Genuinely New In This Round
- Added a web/arXiv-backed source stack tying existence theory, nibble/iterative absorption, and symmetry/Kramer-Mesner search into one execution policy.
- Added explicit implementation consequences for each target level `r in {6,7,8,9}`.
- Added a concise engine-selector rubric with concrete switch criteria.

## Strong Search Stack (research-only)
1. Hard admissibility/divisibility gate
- Require integer `lambda_i = C(n-i, r-i)/C(q-i, r-i)` for `i=0..r-1` before any expensive search.
- For the tracked family `S(r, r+1, r+11)`, expected block counts are:
  - `r=6`: `1768`
  - `r=7`: `3978`
  - `r=8`: `8398`
  - `r=9`: `16796`
- In this family, `(r-1)` target replication is always `lambda_(r-1)=6`; use this as a hard pressure cap in all constructive engines.

2. Symmetry/Kramer-Mesner exact-cover mode
- Build orbit incidence under candidate groups (cyclic, dihedral, affine/projective where available).
- Use exact-cover only when orbit coefficients are mostly binary and compressed matrix is tractable.
- If non-binary orbit coefficients dominate, treat symmetry lane as diagnostic and switch quickly.

3. Nibble -> boosting/repair -> absorber -> residual exact-cover mode
- Start from random-greedy/nibble near-packing, then run reserve-aware boosting/repair with hard caps.
- Use absorber-style reserved capacity to make late-stage repairs feasible.
- Attempt residual exact-cover only when residual uncovered mass is small and strict feasibility is intact (`overcovered=0`, `(r-1)` oversubscribed `=0`).

## Engine Selector Rubric (concise)
- Use symmetry/orbit compression first when:
  - orbit compression is strong (rows/cols shrink materially),
  - binary orbit columns dominate,
  - bounded exact-cover probe shows early progress.
- Use general randomized construction first when:
  - non-binary orbit coefficients are common,
  - exact-cover probe stalls quickly,
  - residual remains large after symmetry diagnostics.

## Source Notes

### 1) Keevash: existence of designs
- URL: https://arxiv.org/abs/1401.3665
- Takeaway: Establishes asymptotic existence of Steiner systems/designs from divisibility conditions; this justifies divisibility as the non-negotiable front gate.
- Implementation consequence:
  - `r=6`: keep admissibility as hard precondition; still rely on computational construction because `n=17` is small.
  - `r=7`: same policy at `n=18`; use theorem as feasibility signal, not as a direct constructor.
  - `r=8`: same at `n=19`; do not treat asymptotic existence as an algorithm.
  - `r=9`: same at `n=20`; computational pipeline remains primary.

### 2) Glock-Kuhn-Lo-Osthus: iterative absorption for designs
- URL: https://arxiv.org/abs/1611.06827
- Takeaway: Gives a concrete proof framework: random partial construction plus iterative absorption/cleanup to finish exact decompositions.
- Implementation consequence:
  - `r=6`: include explicit reserve/absorber budget after nibble, not just greedy add-only growth.
  - `r=7`: increase focus on staged cleanup passes and template-preserving repairs.
  - `r=8`: treat absorption-aware LNS as core engine, not optional post-processing.
  - `r=9`: run multi-pass absorber-aware repair by default; expect single-pass to plateau.

### 3) Rodl nibble / near-perfect coverings
- URL: https://www.sciencedirect.com/science/article/pii/S0195669885800457
- Takeaway: Randomized nibble methods produce near-perfect packings/coverings in uniform hypergraphs, motivating fast approximate starts.
- Implementation consequence:
  - `r=6`: use multi-seed nibble starts to cut uncovered mass quickly before local search.
  - `r=7`: bias nibble scoring by low point-degree and `(r-1)` slack to delay pressure spikes.
  - `r=8`: assume nibble-only plateaus; schedule immediate boosting/repair phases.
  - `r=9`: use nibble strictly as initializer; hand off early to pressure-targeted repair.

### 4) Wilson theorem baseline for pairwise balanced designs
- URL: https://www.sciencedirect.com/science/article/pii/0097316575900679
- Takeaway: Classical divisibility-plus-large-order existence for `t=2` designs; useful as a shadow-regularity heuristic for higher-`t` search.
- Implementation consequence:
  - `r=6`: track pair-shadow imbalance as an early warning metric.
  - `r=7`: include pair-balance in tie-break scores when adding/removing blocks.
  - `r=8`: use pair-shadow smoothing to choose repair neighborhoods.
  - `r=9`: prioritize destroys that reduce pair-shadow outliers when `(r-1)` pressures tie.

### 5) Kramer-Mesner symmetry construction (modern high-t computational example)
- URL: https://www.sciencedirect.com/science/article/pii/S0012365X07003524
- Takeaway: Demonstrates that strong automorphism groups can make high-`t` simple design construction tractable via orbit incidence systems.
- Implementation consequence:
  - `r=6`: spend nontrivial budget on symmetry lane (cyclic/dihedral + one richer group when available).
  - `r=7`: keep symmetry as first engine; proceed only if binary-column share is high.
  - `r=8`: use symmetry mainly for compression diagnostics and candidate generation.
  - `r=9`: short symmetry probe only; switch quickly on non-binary orbit inflation.

### 6) Symmetry-enhanced branch-and-bound for large design search
- URL: https://digitalcommons.mtu.edu/michigantech-p2/2010/
- Takeaway: Recent computational work shows symmetry, meet-in-the-middle, and branch-and-bound ordering materially improve exact search feasibility.
- Implementation consequence:
  - `r=6`: use orbit-weighted branch ordering in residual exact-cover attempts.
  - `r=7`: add meet-in-the-middle only for small residual orbit subinstances.
  - `r=8`: use as residual micro-solver after repair reduces uncovered to a small core.
  - `r=9`: keep this as late-phase tool only; avoid full-instance exact search.

## Incremental Additions (Round 2 Solve)
- Symmetry front-gate diagnostics for `S(6,7,17)` were re-measured with bounded binary DFS:
  - cyclic `Z_17`: `|O_6|=728`, `|O_7|=1144`, binary/non-binary columns `1136/8`, `max_coeff=2`, DFS `137349` nodes in `20s` (unsolved);
  - dihedral `D_17`: `|O_6|=392`, `|O_7|=600`, binary/non-binary columns `544/56`, `max_coeff=2`, DFS `45` nodes (unsolved).
- Broad reserve-aware LNS can stall at `1115` strict-feasible blocks even with large neighborhoods.
- Exact local augmenting repacks (`1->2`, `2->3`, `3->4`) can break that stall sparsely; this round produced `1115 -> 1116` while preserving strict gates (`overcovered=0`, `oversubscribed_(r-1)=0`).
- Residual additive exact completion at `1116` is currently `infeasible_residual` (`some uncovered subsets have no feasible additive block`), so further progress still requires delete+repack moves.

## Incremental Additions (Round 3 Solve)
- Instance `S(7,8,18)` strict-feasible frontier improved by reserve-aware motif LNS from `2251` to `2252` blocks while keeping `overcovered_r_subsets=0` and `oversubscribed_(r-1)=0`.
- For this frontier, additive feasibility remains exhausted after refill (`feasible_left=0`) and the final plateau shows ~`113` saturated 6-subsets (load exactly `6`).
- Secondary pressure balancing is still useful at fixed block count: point-degree spread tightened from gap `141` to `135` without violating strict gates.
- Residual exact completion remains blocked by residual size (`uncovered fraction = 13808/31824 = 0.4339`), so delete+repack neighborhoods remain mandatory.
