# Steiner Knowledge Cache

Run ID: 20260219_030101
Created (UTC): 2026-02-19T03:01:01Z

## Source Notes
- Add references as: URL + takeaway + how it changes construction strategy.

## References (Round 1 Research)

### [R1] Keevash, *The existence of designs* (arXiv:1401.3665)
- URL: https://arxiv.org/abs/1401.3665
- Takeaway: For fixed design parameters, natural divisibility conditions are asymptotically sufficient for existence. The proof framework is randomized-algebraic with absorption-style correction.
- Implication for `r=6..9`: Make divisibility checks the first hard gate, then design rounds around a two-stage solver (probabilistic near-cover + structured leftover repair) instead of direct exact construction from scratch.

### [R2] Keevash, *A short proof of the existence of designs* (arXiv:2411.18291)
- URL: https://arxiv.org/abs/2411.18291
- Takeaway: Reproves existence with a shorter argument and better bounds. This suggests the asymptotic regime may become practically reachable earlier than older proof constants implied.
- Implication for `r=6..9`: In rounds 2+, widen candidate `n` ranges near the admissibility boundary and test smaller "likely feasible" instances before jumping to extremely large sizes.

### [R3] Glock-Kuehn-Lo-Osthus, *The existence of designs via iterative absorption* (arXiv:1611.06827 / Memoirs AMS 2023)
- URL: https://doi.org/10.48550/arXiv.1611.06827
- Takeaway: Gives an iterative-absorption framework (nibble, boosting, greedy covers, vortices, absorbers) that proves existence for very general hypergraph design settings.
- Implication for `r=6..9`: Prioritize an explicit iterative-absorption pipeline in later rounds: reserve absorber resources early, run randomized packing in phases, and finish by targeted divisibility/leftover elimination.

### [R4] R\"odl, *On a Packing and Covering Problem* (Eur. J. Comb. 1985)
- URL: https://doi.org/10.1016/S0195-6698(85)80023-8
- Takeaway: Establishes asymptotically tight packing/covering via probabilistic nibble ideas (Erdos-Hanani context), justifying near-perfect partial solutions as a first stage.
- Implication for `r=6..9`: Build rounds around a nibble core that rapidly covers most `r`-sets, then switch to deterministic/local-repair mode only for the sparse residual.

### [R5] Spencer, *Real Time Asymptotic Packing* (EJC 1997)
- URL: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v4i2r19
- Takeaway: Analyzes random greedy packing by differential-equation tracking; predicts controlled residual size under regularity assumptions.
- Implication for `r=6..9`: Add online regularity diagnostics (degree/codegree drift) during random greedy phases and stop early when drift spikes, handing off to repair before the process degrades.

### [R6] Wilson, *An existence theory for pairwise balanced designs, III* (JCTA 1975)
- URL: https://doi.org/10.1016/0097-3165(75)90067-9
- Takeaway: For `r=2` (pairwise/BIBD context), congruence/divisibility conditions are sufficient for all sufficiently large admissible orders; this is the classical asymptotic template.
- Implication for `r=6..9`: Use pairwise projections/congruence checks as low-cost sanity filters and debugging invariants before expensive higher-order search.

### [R7] Keevash, *Counting designs* (JEMS 2018)
- URL: https://ems.press/journals/jems/articles/15331
- Takeaway: Gives asymptotic counts for designs and explains randomized algebraic construction in a more concrete special-case setting.
- Implication for `r=6..9`: Expect many feasible objects in admissible large regimes; use multi-start randomized searches with diversity scoring/restarts rather than a single long trajectory.
