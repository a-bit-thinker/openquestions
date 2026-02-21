# Steiner Knowledge Cache

Run ID: 20260219_180444
Created (UTC): 2026-02-19T18:04:45Z

## Scope
- Goal: high-signal cache for unknown large Steiner-system construction.
- Round mode: research-only (no certificate-construction priority in this round).

## Strong Search Stack (Research Mode)
### 0) Hard admissibility/divisibility gate (non-negotiable)
- Before any search engine, enforce integrality of
  `lambda_i = C(n-i, r-i) / C(q-i, r-i)` for all `i = 0..r-1`.
- If any divisibility fails, stop; do not run symmetry, nibble, or exact-cover.
- Cache outputs:
  `expected_block_count=lambda_0`, `replication_vector=(lambda_1..lambda_{r-1})`,
  and failing congruences if present.

### 1) Symmetry/Kramer-Mesner exact-cover mode
- Pick candidate automorphism group `G <= S_n`, compress `r`-sets and `q`-sets into `G`-orbits.
- Build Kramer-Mesner incidence matrix `A` (rows: `r`-orbit reps, cols: `q`-orbit reps).
- Solve exact-cover/integer system `A x = 1` with `x in {0,1}` (or equivalent exact-cover SAT/ILP).
- Prefer this mode when orbit compression is strong and matrix dimensions stay tractable.

### 2) Nibble -> boosting/repair -> absorber -> residual exact-cover mode
- Nibble: randomized greedy partial design that covers most `r`-sets while limiting local conflicts.
- Boosting/repair: flatten degree/profile irregularities (point degree and `(r-1)`-pressure).
- Absorber: pre-position local gadgets to absorb hard leftover structures.
- Residual exact-cover: solve only the tiny leftover exactly (SAT/ILP/XC), not the full instance.

## Engine-Selector Rubric (Concise)
| Signal | Choose symmetry/orbit-compressed exact-cover | Choose randomized iterative-absorption pipeline |
|---|---|---|
| Automorphism evidence | Known large group actions, transitivity, small orbit counts | No strong group, orbits near full size |
| Matrix size | KM matrix feasible in memory/time | KM matrix explodes |
| Target regime | Small/medium `n`, highly structured instance | Larger `n`, weak symmetry, asymptotic-friendly |
| Operational objective | Deterministic exact solve via compressed system | Fast near-cover + controlled repair + tiny residual exact solve |

## Source Notes (High-Value)
### 1) Keevash, *The existence of designs*
- URL: https://arxiv.org/abs/1401.3665
- Takeaway: For fixed `q>r`, natural divisibility conditions are asymptotically sufficient; framework uses pseudorandomness/extendability plus robust fractional decomposition.
- Implementation consequence (`r in {6,7,8,9}`):
  - `r=6`: keep strict divisibility gate and drive residual toward pseudorandom/extendable profile before exact cleanup.
  - `r=7`: add stronger monitoring on high-order codegrees to preserve extendability assumptions.
  - `r=8`: default to randomized-combinatorial pipeline unless very strong symmetry is present.
  - `r=9`: treat direct full exact-cover as last resort; target tiny residual before exact solve.

### 2) Glock-Kuehn-Lo-Osthus, *The existence of designs via iterative absorption*
- URL: https://arxiv.org/abs/1611.06827
- Takeaway: Provides a full iterative-absorption route with regularity constraints and explicit regularity boosting; extends beyond purely quasirandom settings.
- Implementation consequence (`r in {6,7,8,9}`):
  - `r=6`: run nibble then explicit boosting passes before absorption.
  - `r=7`: budget more repair iterations; `(r-1)`-set pressure balancing is more brittle.
  - `r=8`: pre-plan absorber families earlier; do not postpone absorber design to endgame.
  - `r=9`: multi-scale absorption becomes primary; residual solver should only see very small support.

### 3) Keevash, *The existence of designs II*
- URL: https://arxiv.org/abs/1802.05900
- Takeaway: Lattice/extra-data generalization covers colored/ordered/resolvable variants and decomposition-with-constraints settings.
- Implementation consequence (`r in {6,7,8,9}`):
  - `r=6`: if side constraints appear (ordering/classes), encode them early as lattice constraints.
  - `r=7`: avoid ad-hoc penalties; formal constrained decomposition model is safer.
  - `r=8`: constraint-rich instances should bypass plain KM and use constrained residual ILP/SAT.
  - `r=9`: prioritize formulations that keep divisibility and side constraints jointly feasible.

### 4) Wilson, *An existence theory for pairwise balanced designs, III*
- URL: https://www.sciencedirect.com/science/article/pii/0097316575900679
- Takeaway: For `r=2` (BIBD/PBD), congruence/divisibility conditions are asymptotically sufficient; foundational baseline for design existence logic.
- Implementation consequence (`r in {6,7,8,9}`):
  - `r=6`: project intermediate states to pair-level marginals to detect impossible drift early.
  - `r=7`: enforce pair-level congruence sanity checks during repair, not only at start.
  - `r=8`: use pairwise imbalance as a cheap early-warning proxy for later high-order bottlenecks.
  - `r=9`: integrate pairwise sanity metrics into termination criteria for randomized phases.

### 5) Kramer-Mesner, *t-designs on hypergraphs* (foundational KM method)
- URL: https://dblp.org/rec/journals/dm/KramerM76.html
- Takeaway: Canonical orbit-incidence reduction for t-design search with prescribed automorphism groups; exact-cover style algebraic core.
- Implementation consequence (`r in {6,7,8,9}`):
  - `r=6`: first symmetry pass should attempt KM compression before full search.
  - `r=7`: proceed with KM only if orbit compression ratio is strong (otherwise skip quickly).
  - `r=8`: KM is viable mainly when a large group drastically shrinks column count.
  - `r=9`: symmetry must be exceptional; otherwise choose randomized pipeline directly.

### 6) Kreher-Radziszowski, *Finding Simple T-designs by Using Basis Reduction*
- URL: https://repository.rit.edu/article/635/
- Takeaway: Basis-reduction acceleration of KM-style systems; reports computational success including a new simple 6-design.
- Implementation consequence (`r in {6,7,8,9}`):
  - `r=6`: include basis-reduction preprocessing in symmetry-mode prototype.
  - `r=7`: test basis reduction as a pruning stage before branch-and-bound.
  - `r=8`: only worth running when symmetry already produced a compact matrix.
  - `r=9`: use as fallback post-compression, not as primary strategy.

### 7) Laue-Wassermann, *Simple 8-(31,12,3080), 8-(40,12,16200), 8-(40,12,16520) designs...*
- URL: https://www.sciencedirect.com/science/article/pii/S0012365X07003524
- Takeaway: Demonstrates high-`t` computational feasibility via prescribed automorphism groups + Kramer-Mesner; supplies concrete 8-design constructions.
- Implementation consequence (`r in {6,7,8,9}`):
  - `r=6`: validates symmetry-first search as a practical baseline for moderate-high `r`.
  - `r=7`: encourages targeted group search before expensive randomized runs.
  - `r=8`: strong evidence that group-prescribed KM can still succeed at high `r`.
  - `r=9`: if no strong group emerges, do not expect direct KM to scale.

### 8) Pippenger-Spencer, *Asymptotic Behavior of the Chromatic Index for Hypergraphs*
- URL: https://scholarship.claremont.edu/hmc_fac_pub/1041/
- Takeaway: Near-regular degree plus low codegree conditions imply near-perfect packing/covering behavior; conceptual backbone for nibble-style progress guarantees.
- Implementation consequence (`r in {6,7,8,9}`):
  - `r=6`: tune nibble acceptance to keep degree spread tight and pair codegrees small.
  - `r=7`: increase conflict penalties on repeated `(r-1)` neighborhoods.
  - `r=8`: prefer shorter nibble epochs with frequent rebalancing.
  - `r=9`: stop nibble earlier and hand off to absorber/repair before instability spikes.

## Current Instance Anchor
- Instance: `S(6,7,17)`
- Admissibility snapshot: divisible with `expected_block_count=1768`, `lambda_1=728`, `lambda_5=6`.

## Round 2 Execution Addendum (Instance S(6,7,17))
- Symmetry reconnaissance (cyclic `C17`) was stronger than expected but still hard in bounded solve time:
  - `r`-orbits: 728 (`12376/17`), `q`-orbits: 1144 (`19448/17`).
  - Orbit incidence profile: 1136 usable 0/1-style columns; 8 columns had duplicate row-orbit hits.
  - KM-size estimate: `728 x 1144 = 832,832` entries.
  - Bounded orbit-level exact-cover DFS (~49s, 109,515 nodes) did not find a completion (best depth 35/104), so round execution switched to general pipeline.
- Empirical search takeaway:
  - Flex-reserve + refill can improve `(r-1)` load tails (e.g., max load 10 -> 8 in intermediate states),
    but this often trades off against uncovered/overcovered and can lower verifier score.
  - For this instance, uncovered/overcovered reductions remained the dominant driver of score gains.

## Round 3 Execution Addendum (Instance S(7,8,18))
- Symmetry/orbit gate results:
  - Cyclic `C18`: `r`-orbits `1768`, `q`-orbits `2438`, KM estimate `4,310,384` entries; clean orbit-columns `2409`, dirty `29`.
  - Dihedral `D18`: `r`-orbits `912`, `q`-orbits `1282`, KM estimate `1,169,184` entries; clean orbit-columns `1147`, dirty `135`, with `1` dead clean-row orbit.
  - Round decision: symmetry exact mode not tractable in bounded budget; switch to general nibble/repair/LNS pipeline.
- Empirical search takeaway:
  - Early reserve/remove + refill is useful for opening neighborhood diversity, but by itself can worsen uncovered/overcovered even if `(r-1)` pressure tails improve.
  - For this instance, best gains came from fixed-cardinality LNS using the exact verifier proxy objective (`1.9*uncovered + overcovered`) with `(r-1)`-oversubscription as tie-break.
  - Resulting candidate improvement over imported seed: `score 60.01 -> 60.35`, `uncovered 4823 -> 4793`, `overcovered 3563 -> 3510`, `oversubscribed_(r-1) 5420 -> 5262`.

## Round 4 Execution Addendum (Instance S(8,9,19))
- Symmetry/orbit gate results:
  - Cyclic `C19`: `r`-orbits `3978`, `q`-orbits `4862`, KM estimate `19,341,036` entries.
  - Dihedral `D19`: `r`-orbits `2052`, `q`-orbits `2494`, KM estimate `5,117,688` entries.
  - Round decision: symmetry exact mode not tractable in bounded budget; switch to general nibble/repair/LNS pipeline.
- Empirical search takeaway:
  - Early reserve/remove substantially lowers `(r-1)` oversubscription tails, but temporarily worsens uncovered/overcovered until refill completes.
  - Best gains again came from fixed-cardinality remove-`k`/refill-`k` LNS using verifier proxy objective (`1.9*uncovered + overcovered`) with `(r-1)` oversubscription as tie-break.
  - Resulting candidate improvement over imported seed: `score 57.35 -> 57.49`, `uncovered 12276 -> 12247`, `overcovered 8909 -> 8860`, `oversubscribed_(r-1) 15245 -> 15046`.

## Round 5 Execution Addendum (Instance S(9,10,20))
- Symmetry/orbit gate results:
  - Cyclic `C20`: `r`-orbits `8398`, `q`-orbits `9252`, KM estimate `77,698,296` entries.
  - Dihedral `D20`: `r`-orbits `4262`, `q`-orbits `4752`, KM estimate `20,253,024` entries.
  - Round decision: symmetry exact mode not tractable in bounded budget; switched to general nibble/repair/LNS pipeline.
- Empirical search takeaway:
  - Early reserve/remove improves `(r-1)` oversubscription tails but worsens uncovered/overcovered until refill completes.
  - Fixed-cardinality remove-`k`/refill-`k` LNS (`k` in `{3,4,5,6,7,8,9,10,12}`) with primary objective `19*uncovered + 10*overcovered` and `(r-1)` oversubscription tie-break produced steady gains.
  - Resulting candidate improvement over imported seed: `score 54.95 -> 55.44`, `uncovered 28774 -> 28530`, `overcovered 20999 -> 20643`, `oversubscribed_(r-1) 38926 -> 38551`.
