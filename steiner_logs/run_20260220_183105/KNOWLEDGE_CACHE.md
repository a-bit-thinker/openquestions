# Steiner Knowledge Cache

Run ID: 20260220_183105
Created (UTC): 2026-02-20T18:31:07Z

## Strong Search Stack (Research Mode)
1. Hard admissibility/divisibility gate (mandatory precheck)
- For `S(r,q,n)`, require integrality of all replication numbers
  `lambda_i = C(n-i, r-i) / C(q-i, r-i)` for `i=0..r-1`.
- Reject parameter sets immediately on any failed congruence/integrality check.
- For admissible instances, compute target loads (`lambda_1..lambda_{r-1}`) up front and use them as hard runtime invariants.

2. Symmetry/Kramer-Mesner exact-cover mode
- If a nontrivial automorphism group `G` is plausible, orbit-compress `(r)`- and `(q)`-subsets.
- Build orbit-incidence matrix `A_{O_r,O_q}` and solve `A x = 1` (or `=lambda` in generalized settings) with `x in {0,1}` for simple systems.
- Use DLX/Algorithm X or ILP on orbit variables; progressively relax `G` if infeasible or over-constrained.

3. Nibble -> boosting/repair -> absorber -> residual exact-cover mode
- Run randomized nibble to get near-cover with bounded local discrepancy.
- Apply regularity boosting/repair to reduce local pressure spikes and leave structured residual.
- Pre-wire absorber capacity, then execute absorption.
- Solve tiny leftover with exact-cover (`DLX/ILP`) only at residual scale.

## Engine Selector Rubric
- Prefer symmetry/orbit compression when:
  - Candidate groups plausibly yield large orbit reduction (`|O_q| << C(n,q)` and manageable matrix sparsity).
  - You expect algebraic/geometric structure (projective groups, sharply transitive actions, known catalog families).
  - Exact-cover on compressed columns is within memory/time budget.
- Prefer generalized randomized construction when:
  - No strong automorphism is evident or orbit count remains near full size.
  - `r` is high (`7-9`) and global exact-cover is combinatorially explosive.
  - You can maintain stable degree/pressure trajectories and hand only a small residual to exact-cover.

## Source Notes

### 1) Keevash, *The existence of designs* (arXiv:1401.3665)
- URL: https://arxiv.org/abs/1401.3665
- Takeaway: Establishes asymptotic existence of combinatorial designs under the natural divisibility conditions. Treats divisibility as the non-negotiable first gate.
- Implementation consequence for `r in {6,7,8,9}`:
  - `r=6`: keep exact integrality gate and stop all inadmissible runs before search.
  - `r=7`: same gate; prioritize scalable search only after full `lambda_i` audit.
  - `r=8`: same gate plus stricter early-abort on unstable load trajectories.
  - `r=9`: use divisibility gate as the only universal hard filter before randomized engines.

### 2) Glock-Kuehn-Lo-Osthus, *The existence of designs via iterative absorption* (arXiv:1611.06827)
- URL: https://arxiv.org/abs/1611.06827
- Takeaway: Gives an iterative-absorption framework with explicit phases: nibble, regularity boosting/greedy cover, vortices/absorbers, final completion.
- Implementation consequence for `r in {6,7,8,9}`:
  - `r=6`: run full 4-phase pipeline with moderate absorber budget.
  - `r=7`: increase reservoir/absorber budget and trigger boosting earlier.
  - `r=8`: expect heavier repair pressure; allocate larger residual cleanup budget.
  - `r=9`: randomized-first is default; exact-cover only on very small leftover.

### 3) Keevash, *The existence of designs II* (arXiv:1802.05900)
- URL: https://arxiv.org/abs/1802.05900
- Takeaway: Extends to lattice/labelled-face formulations, enabling extra linear constraints (colors/orders/resolvability-type structure) to be encoded in the model.
- Implementation consequence for `r in {6,7,8,9}`:
  - `r=6`: add optional lattice constraints only if they reduce branching.
  - `r=7`: use constraint-augmented feasibility checks before expensive search.
  - `r=8`: prefer weighted/lattice-guided nibble objectives to reduce drift.
  - `r=9`: enforce coarse linear invariants early; avoid unconstrained random walks.

### 4) Knuth, *Dancing links* (arXiv:cs/0011047)
- URL: https://arxiv.org/abs/cs/0011047
- Takeaway: Algorithm X with reversible linked-structure updates is a fast exact-cover backend for sparse 0-1 matrices.
- Implementation consequence for `r in {6,7,8,9}`:
  - `r=6`: viable as residual solver and for modest orbit-compressed instances.
  - `r=7`: use strong column-order heuristics; still residual-first unless symmetry is strong.
  - `r=8`: avoid global DLX; reserve for compressed or post-absorption leftovers.
  - `r=9`: DLX is patch-only, not primary construction engine.

### 5) Acketa-Mudrinski, *A family of 4-designs on 26 points* (EuDML)
- URL: https://eudml.org/doc/247869
- Takeaway: Concrete computational Kramer-Mesner workflow with automorphism groups and orbit-incidence partitioning; demonstrates practical orbit-based design search.
- Implementation consequence for `r in {6,7,8,9}`:
  - `r=6`: start symmetry mode by testing group actions and orbit-incidence compressibility.
  - `r=7`: keep only group choices that materially reduce orbit matrix dimension.
  - `r=8`: symmetry mode is only justified if orbit reduction is dramatic.
  - `r=9`: attempt symmetry mode only with very strong, explicit algebraic candidates.

### 6) Bennett-Colbourn-Mullin, *Quintessential pairwise balanced designs* (JSPI, 1998)
- URL: https://www.sciencedirect.com/science/article/abs/pii/S0378375898000214
- Takeaway: Detailed spectrum results for PBD block-size sets `{5,..,9}` with explicit exception handling; useful as low-order scaffolding knowledge.
- Implementation consequence for `r in {6,7,8,9}`:
  - `r=6`: use PBD-style scaffolds as load-balancing templates before enforcing full `r`-wise exactness.
  - `r=7`: same as warm-start/template generation, not final certification.
  - `r=8`: treat as initialization prior only; do not infer `t=r` existence from `t=2`.
  - `r=9`: use only for heuristic seeding of randomized schedules.

## Incremental empirical additions (Round 2)

### A) Symmetry/orbit compression diagnostics on S(6,7,17)
- Tested cyclic (`Z_17`) orbit compression before randomized search.
- Orbit sizes observed:
  - `|O_6| = 728`, `|O_7| = 1144`.
- Orbit-incidence structure:
  - 1136 columns behaved as binary incidence,
  - 8 columns had multiplicity-2 incidence entries (incompatible with strict `A x = 1` exact-cover rows without generalized handling).
- Bounded orbit DFS (`20s`, node cap `200000`) reached `17271` nodes and timed out without usable completion.
- Practical implication: keep symmetry pass as a cheap front gate, but switch quickly to general LNS pipeline unless stronger group structure appears.

### B) Feasible LNS recipe that improved this run
- Start from a strict-feasible seed (`overcovered=0`, `(r-1)` max load at target).
- Use destroy/repair neighborhoods with `k` in `[18,84]` (multi-block, not 1-for-1).
- Local repack pool: blocks touching rows freed by destroy step.
- Move admissibility (hard):
  - all 6-subset rows stay unique (`row_owner` gate),
  - all 5-subset loads stay `<= 6` (`lambda_5` gate).
- Heuristic gain: weighted preference for low point degree and low 5-subset load blocks.
- Observed gain in this round: `1088 -> 1115` blocks while preserving `overcovered=0` and `(r-1)` oversubscription `=0`.

## Incremental empirical additions (Round 4)

### C) Symmetry/orbit diagnostics on S(8,9,19)
- Enforced symmetry-first check before randomized search.
- Cyclic `Z_19` orbit compression:
  - `|O_8|=3978`, `|O_9|=4862`.
  - Binary columns: `4853`; non-binary columns: `9`; max orbit coefficient `2`.
  - Bounded binary-only DFS (`20s`, `200k` nodes): `nodes=266`, timeout, no completion.
- Dihedral `D_19` orbit compression:
  - `|O_8|=2052`, `|O_9|=2494`.
  - Binary columns: `2368`; non-binary columns: `126`; max coefficient `2`.
  - Binary-only DFS: `nodes=192`, no completion in explored tree.
- Practical implication:
  - Non-binary orbit incidence remains a hard blocker for strict `A x = 1` binary exact-cover in this budget.
  - Keep symmetry pass as a front gate; switch quickly to generalized LNS pipeline for `r=8` here.

### D) Plateau-crossing LNS behavior on S(8,9,19)
- Start from strict-feasible seed (`4371` blocks, `overcovered=0`, `(r-1)` max load at target `6`).
- Pure additive nibble from seed gave `0` one-step feasible additions.
- Effective move pattern:
  - destroy/repack with `k in [24,96]`,
  - reserve-then-flex refill order,
  - local pool from freed rows + global boost,
  - hard gates always on: unique 8-subset ownership and 7-subset load `<= 6`.
- Key empirical finding:
  - Most neighborhoods are `delta=0` plateaus; accepting neutral and occasional small negative moves (annealed) is required to reach better basins.
- Observed gain this round:
  - `4371 -> 4392` blocks,
  - uncovered `36243 -> 36054`,
  - point-degree gap `298 -> 194`,
  - while preserving `overcovered=0` and `(r-1)` oversubscription `=0`.

## Incremental empirical additions (Round 5)

### E) Symmetry/orbit diagnostics on S(9,10,20)
- Enforced symmetry-first check before randomized search.
- Cyclic `Z_20` orbit compression:
  - `|O_9|=8398`, `|O_10|=9252`.
  - Binary columns: `9215`; non-binary columns: `37`; max coefficient `10`.
  - Bounded binary-only DFS (`20s`, `200k` nodes): `nodes=8`, `solved=false`.
- Dihedral `D_20` orbit compression:
  - `|O_9|=4262`, `|O_10|=4752`.
  - Binary columns: `4488`; non-binary columns: `264`; max coefficient `10`.
  - Bounded binary-only DFS (`20s`, `200k` nodes): `nodes=113`, `solved=false`.
- Practical implication:
  - Orbit compression gives size reduction, but non-binary incidence multiplicities are too strong for strict binary exact-cover in this budget.
  - Keep symmetry as a front gate, then switch quickly to generalized strict-feasible LNS.

### F) Multi-pass reserve-aware LNS behavior on S(9,10,20)
- Start seed (`strict-feasible`): `5897` blocks, `uncovered=108990`, `overcovered=0`, `(r-1)` oversubscription `=0`.
- Additive boost best checkpoint: `7693` blocks (`uncovered=91030`) under hard gates.
- Effective move pattern:
  - destroy/repack with `k in [24,72]`,
  - reserve-first refill with `reserve=max(4,k//7)`, then flex completion,
  - local pool from freed 9-subsets + global sample,
  - hard gates always on: unique 9-subset ownership and 8-subset load `<= 6`.
- Multi-pass gains (all strict-feasible):
  - `7693 -> 7866 -> 7934 -> 8019 -> 8070 -> 8120` blocks,
  - uncovered `91030 -> 89300 -> 88620 -> 87770 -> 87260 -> 86760`,
  - point-degree gap `579 -> 415 -> 345 -> 302 -> 281 -> 251`.
- Final round artifact:
  - `8120` blocks,
  - `overcovered=0`, `(r-1)` oversubscription `=0`, `r_minus_1_max_degree=6` (target `6`).
