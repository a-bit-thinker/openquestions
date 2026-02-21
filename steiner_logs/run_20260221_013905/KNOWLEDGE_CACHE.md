# Steiner Knowledge Cache

Run ID: 20260221_013905
Created (UTC): 2026-02-21T01:39:05Z

## Hard Admissibility/Divisibility Gate
- Keep this as an absolute pre-search invariant.
- For `S(6,7,17)`: admissible with `expected_block_count=1768`, `lambda_5=6`, no divisibility failures.
- Enforce the same integrality checks for `r=7,8,9` before spending solver budget.

## Strong Search Stack (Research Backbone)
1. Hard admissibility/divisibility gate.
2. Symmetry/Kramer-Mesner exact-cover mode (bounded front gate).
3. Nibble -> boosting/repair -> absorber -> residual exact-cover mode.

## Engine Selector Rubric (Concise)
- Use symmetry/orbit compression first when:
  - orbit reduction is strong (target at least one order-of-magnitude shrink),
  - orbit coefficients are mostly binary,
  - bounded probe shows progress quickly.
- Use generalized randomized construction first when:
  - non-binary orbit coefficients are material,
  - bounded symmetry probe stalls,
  - `(r-1)` pressure motifs dominate and require repeated local repair.

## Source Notes (High-Value, blocker-driven)
1. URL: https://arxiv.org/abs/1401.3665
- Takeaway: Divisibility is the non-negotiable existence gate (asymptotically sufficient), but constructive success still needs a staged computational engine.
- Implementation consequence by `r`:
  - `r=6`: hard-fail immediately on any integrality miss; otherwise lock target block count and run staged search.
  - `r=7`: same gate; treat any early score gain without gate compliance as invalid.
  - `r=8`: keep gate fixed, but avoid monolithic exact-cover attempts as primary strategy.
  - `r=9`: plan decomposition-style pipeline from start; no single-engine global exact solve.

2. URL: https://arxiv.org/abs/1611.06827
- Takeaway: Iterative absorption formalizes the practical stack: random partial structure, regularity boosting/repair, then absorber-driven completion.
- Implementation consequence by `r`:
  - `r=6`: short nibble + immediate repair beats long add-only continuation.
  - `r=7`: add explicit boosting stage when additive growth stalls near cap constraints.
  - `r=8`: keep absorber reserve active throughout LNS to avoid late dead-ends.
  - `r=9`: require multi-pass reserve-aware destroy/repack; residual exact-cover only after large reduction.

3. URL: https://www.sciencedirect.com/science/article/pii/0097316586900944
- Takeaway: Orbit-incidence algebra maps Wilson-style incidence to Kramer-Mesner orbit systems, clarifying why non-binary orbit coefficients are structural, not noise.
- Implementation consequence by `r`:
  - `r=6`: binary KM lane remains viable when non-binary orbit mass is tiny.
  - `r=7`: track coefficient histogram (`max_coeff`, non-binary share) as mandatory switch signal.
  - `r=8`: when non-binary share rises, move from pure DLX exact-cover to weighted orbit ILP micro-solves.
  - `r=9`: skip extended binary-only orbit DFS once non-binary dominance is observed; use weighted orbit models only as candidate generators.

4. URL: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v32i1p17
- Takeaway: Differential-equation analysis of random greedy hypergraph construction supports instrumented stopping rather than maximal-length greedy runs.
- Implementation consequence by `r`:
  - `r=6`: terminate nibble when marginal gain and pressure-tail metrics flatten.
  - `r=7`: run many short seeded nibbles with pressure-aware early stop.
  - `r=8`: avoid long single-seed additive phases; switch earlier to motif-targeted repair.
  - `r=9`: formalize handoff trigger from nibble to repair using gain-per-accept and `(r-1)` tail thresholds.

5. URL: https://digitalcommons.mtu.edu/michigantech-p2/2010/
- Takeaway: Recent symmetry encoding (normalizer-aware) can collapse isomorphic branches into one exact-cover instance and reduce restart overhead.
- Implementation consequence by `r`:
  - `r=6`: add normalizer/canonical dedup in local exact augmentation neighborhoods.
  - `r=7`: apply symmetry-dedup hashing before launching repeated micro exact solves.
  - `r=8`: use normalizer-aware branch pruning only in residual exact microphase.
  - `r=9`: reserve this for tiny residual subinstances; global orbit search remains too expensive.

## Practice-Log Failure -> Research Delta
1. Blocker (Rounds 2-5): symmetry lane repeatedly stalls when non-binary orbit coefficients appear.
- Source likely to address it: incidence-algebra/KM orbit formulation (`0097316586900944`) + normalizer-aware exact-cover encoding (`digitalcommons.mtu.edu/.../2010`).
- Concrete implementation change: add weighted-orbit ILP fallback and canonicalized branch dedup before any long symmetry probe.

2. Blocker (Rounds 2-5): additive-only growth plateaus under saturated `(r-1)` motif clusters.
- Source likely to address it: iterative absorption (`1611.06827`) + random-greedy trajectory instrumentation (`v32i1p17`).
- Concrete implementation change: enforce nibble early-stop + immediate motif-targeted destroy/repack with reserve-first refill.

3. Blocker (Rounds 2-5): augmenting gains are sparse and often duplicated by isomorphic neighborhoods.
- Source likely to address it: normalizer-based symmetry encoding (`digitalcommons.mtu.edu/.../2010`).
- Concrete implementation change: couple two-step motif neighborhoods and deduplicate by canonical orbit signature before micro exact solve.

## Incremental Additions (Round 2, 2026-02-21)
- Symmetry-gate diagnostics for `S(6,7,17)`:
  - `C17`: `|O_6|=728`, `|O_7|=1144`, binary/non-binary columns `1136/8`, `max_coeff=2`, bounded binary DFS unsolved.
  - `D17`: `|O_6|=392`, `|O_7|=600`, binary/non-binary columns `352/248`, `max_coeff=2`, bounded binary DFS unsolved.
  - Practical consequence: keep symmetry as bounded front gate, but switch quickly when DFS stalls even under moderate non-binary share.
- Strict-feasible plateau evidence at current frontier:
  - Add-only probe from `1116` found `0` feasible strict additions.
  - High-trial motif exact augment scans (`>59k` trials) found `0` strict `k->k+1` augmentations.
- New operational tactic that worked:
  - Neutral strict repacks can improve structure even without block gain:
    - point-degree gap `24 -> 19`,
    - cap-6 `(r-1)` tail count (`5`-subset load `=6`) `72 -> 69`,
    - while preserving `overcovered=0` and `(r-1)` oversubscription `=0`.
  - Consequence for next rounds: run a short balance-first neutral phase before expensive exact augment scans.

## Incremental Additions (Round 3, 2026-02-21)
- Symmetry-gate diagnostics for `S(7,8,18)` (bounded, reproducible):
  - `C18`: `|O_7|=1768`, `|O_8|=2438`, binary/non-binary columns `2409/29`, `max_coeff=2`; bounded binary DFS unsolved (`20s`, `nodes=330`).
  - `D18`: `|O_7|=912`, `|O_8|=1282`, binary/non-binary columns `1147/135`, `max_coeff=4`; bounded binary DFS unsolved in budget (`20s`).
  - Consequence: keep symmetry as a strict front gate but switch rapidly on this instance.
- New strict-feasible augment evidence on current round candidate:
  - Add-only probe from `2252` found `0` feasible strict additions over all `C(18,8)=43758` blocks.
  - Motif-coupled `1->2` strict augment loop produced `+36` blocks (`2252 -> 2288`).
  - Reserve-aware motif-coupled `2->3` pass added `+1` (`2288 -> 2289`).
- Net verifier impact from the new lane:
  - `score 39.26 -> 40.56`, `exact_once 18016 -> 18312`, `uncovered 13808 -> 13512`, with `overcovered=0` and `(r-1)` oversubscription `=0` preserved.

## Incremental Additions (Round 4, 2026-02-21)
- Symmetry-gate diagnostics for `S(8,9,19)` (revalidated this round):
  - `C19`: `|O_8|=3978`, `|O_9|=4862`, binary/non-binary columns `4853/9`, `max_coeff=2`; bounded binary DFS unsolved (`20s`, `nodes=274`).
  - `D19`: reused deterministic diagnostics from prior same-instance round: `|O_8|=2052`, `|O_9|=2494`, binary/non-binary `2368/126`, `max_coeff=2`; bounded DFS unsolved.
  - Consequence: on this instance, keep symmetry as a strict front gate only; switch quickly to general repair.
- Strict-feasible augment evidence:
  - Add-only strict scan from `4392` found `0` feasible additions.
  - Motif-coupled exact `1->2` loop found sparse strict gains: `+2` blocks (`4392 -> 4394`) over `1812` trials.
  - Follow-up lanes (`2->3` exact local repacks, reserve-aware `k=16..32` LNS destroy/repack) produced `0` net gains in tested budget.
- Net verifier impact:
  - `score 33.22 -> 33.25`, `exact_once 39528 -> 39546`, `uncovered 36054 -> 36036`, while keeping `overcovered=0`, `(r-1)` oversubscription `=0`, and `r_minus_1_max_degree=6`.
- Operational consequence:
  - For `r=8` strict-feasible states near this frontier, prioritize long-run motif-coupled `1->2` search with chained neighborhoods; treat larger-window local exact and reserve-aware wide LNS as diversification, not primary gain lane.

## Incremental Additions (Round 5, 2026-02-21)
- Symmetry gate decision for `S(9,10,20)` reused deterministic diagnostics:
  - `C20`: `|O_9|=8398`, `|O_10|=9252`, binary/non-binary `9215/37`, `max_coeff=10`, bounded binary DFS unsolved.
  - `D20`: `|O_9|=4262`, `|O_10|=4752`, binary/non-binary `4488/264`, `max_coeff=10`, bounded binary DFS unsolved.
  - Consequence: keep symmetry as bounded front gate only on this instance; switch quickly.
- Strict-feasible additive plateau reconfirmed:
  - Add-only strict scan from `8120` found `0` feasible additions.
- New strict augment evidence at `r=9` frontier:
  - Exact micro `1->2` motif/freed-face lane achieved `18` successful augmentations over `1325` trials.
  - Net strict movement: `8120 -> 8138` blocks.
  - Verifier impact: `score 27.68 -> 27.83`, `exact_once 81200 -> 81380`, `uncovered 86760 -> 86580`.
  - Hard invariants preserved: `overcovered=0`, `oversubscribed_(r-1)=0`, `r_minus_1_max_degree=6`.
- Operational consequence:
  - For this environment and this frontier, prioritize high-throughput exact micro-augment neighborhoods over expensive broad-window LNS neighborhoods.
