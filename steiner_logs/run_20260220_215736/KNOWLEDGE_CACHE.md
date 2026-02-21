# Steiner Knowledge Cache

Run ID: 20260220_215736
Created (UTC): 2026-02-20T21:57:37Z
Updated (UTC): 2026-02-20T22:00:00Z

## Strong Search Stack (Research-Only)

### 1) Hard admissibility/divisibility gate (non-negotiable)
- For candidate `S(r,q,n)`, require
  `lambda_i = C(n-i, r-i) / C(q-i, r-i) in Z` for every `i in {0,...,r-1}`.
- Emit and persist:
  `is_admissible`, `expected_block_count=lambda_0`, and full `lambda_i` vector.
- If any integrality check fails: stop that branch immediately.
- Current snapshot `S(6,7,17)` passes, with `expected_block_count=1768` and `lambda_1..lambda_5 = 728,273,91,26,6`.

### 2) Symmetry / Kramer-Mesner exact-cover mode
- Pick an automorphism group `G` and compute orbits on `r`-subsets and `q`-subsets.
- Build orbit-compressed Kramer-Mesner matrix `A_G` (rows: `r`-orbits, cols: `q`-orbits).
- Solve `A_G x = 1` as 0/1 exact cover (`DLX`, SAT, or ILP backend).
- Apply normalizer/canonical pruning to avoid isomorphic restart overhead.
- Best when orbit compression is strong and classification-level search is needed.

### 3) Nibble -> boosting/repair -> absorber -> residual exact-cover mode
- Run random greedy nibble to cover most `r`-subsets while keeping collisions low.
- Apply boosting/repair sweeps to flatten point loads and `(r-1)`-subset pressure.
- Activate preplanned absorbers around hard local deficits.
- Convert final small residual to exact cover and finish deterministically.
- Best when symmetry is weak but pseudorandom behavior is usable.

## Engine-Selector Rubric (Concise)

Use symmetry/orbit compression first when:
- A plausible `G` gives large compression (rough rule: >=10x on `q`-subsets), and
- pilot exact-cover branching is stable, and
- objective includes canonical/enumerative output.

Use randomized construction first when:
- No group gives meaningful compression (rough rule: <5x), or symmetry constraints stall,
- residual statistics look pseudorandom enough for nibble/repair, and
- objective is witness construction at larger scale.

## Source Notes

### Source 1
- URL: https://arxiv.org/abs/1401.3665
- Takeaway: Keevash proves that (for fixed `r<q` and sufficiently large `n`) divisibility is asymptotically sufficient for design existence, via randomized-algebraic plus absorption ideas.
- Implementation consequence for `r in {6,7,8,9}`:
  - `r=6`: keep divisibility as hard gate, then treat failures as search/engine issues, not arithmetic issues.
  - `r=7`: same gate; bias budget toward constructive pipeline tuning.
  - `r=8`: same gate; expect more value from scalability engineering than extra pre-filters.
  - `r=9`: same gate; plan for hybrid randomized + residual exact-cover rather than pure direct cover.
- Inference: finite-`n` exceptions remain possible, so dual-engine fallback is still required.

### Source 2
- URL: https://arxiv.org/abs/1611.06827
- Takeaway: Glock-Kuehn-Lo-Osthus establish iterative absorption for arbitrary `F`-designs; explicit pipeline components include regularity boosting, absorbing structure, and resilience framing.
- Implementation consequence for `r in {6,7,8,9}`:
  - `r=6`: run full nibble->boost->absorber->residual pipeline as primary randomized engine.
  - `r=7`: increase repair rounds before absorber activation; pressure variance tends to hurt completion.
  - `r=8`: pre-allocate larger absorber budget; skip direct exact-cover except on small residual.
  - `r=9`: default to staged absorption with strict residual-size cutoff before deterministic finish.
- Inference: higher `r` magnifies local bottleneck sensitivity, so repair/absorber instrumentation must get stricter.

### Source 3
- URL: https://arxiv.org/abs/1802.05900
- Takeaway: Keevash’s lattice framework extends design existence machinery to settings with extra structural constraints (label/order/color-type side conditions).
- Implementation consequence for `r in {6,7,8,9}`:
  - `r=6`: encode balancing/side constraints early as linear invariants, not post hoc filters.
  - `r=7`: preserve invariant checks through every repair move.
  - `r=8`: enforce lattice-compatible local moves only; avoid repairs that violate global balances.
  - `r=9`: keep a minimal invariant core and reject any seed whose early trajectory drifts from it.
- Inference: constraint-aware repair is safer than unconstrained greedy correction.

### Source 4
- URL: https://www.mit.edu/~asah/papers/2204.03964.pdf
- Takeaway: For random host settings (STS case), a bootstrapped iterative-absorption approach succeeds near threshold scale; randomization plus structured completion is practical.
- Implementation consequence for `r in {6,7,8,9}`:
  - `r=6`: run multi-seed nibble batches and keep top residual profiles for completion.
  - `r=7`: increase seed count and select by low `(r-1)` pressure tail risk.
  - `r=8`: use seed triage aggressively; discard runs with early pressure spikes.
  - `r=9`: treat randomized phase as candidate generator only; accept only seeds with tiny residual core.
- Inference: although this source is STS-specific, the operational lesson (multi-seed + absorption completion) transfers to larger `r` search workflows.

### Source 5
- URL: https://digitalcommons.mtu.edu/michigantech-p2/2010/
- Takeaway: Recent computational Steiner construction work uses Kramer-Mesner + exact-cover, with normalizer-based symmetry encoding to remove isomorphic branch restarts.
- Implementation consequence for `r in {6,7,8,9}`:
  - `r=6`: symmetry-encoded exact cover is a realistic first engine when group action is evident.
  - `r=7`: use orbit/normalizer pruning before launching any heavy exact-cover run.
  - `r=8`: reserve full exact-cover for reduced residual instances unless compression is exceptional.
  - `r=9`: use KM mainly for residual completion/validation; full-space exact-cover is usually too wide.
- Inference: normalizer-aware de-duplication is mandatory whenever using group-constrained search.

### Source 6
- URL: https://www.sciencedirect.com/science/article/pii/S0012365X16301753
- Takeaway: Kramer-Mesner workflows remain practical by reducing design search to 0/1 linear exact-cover systems under prescribed automorphism groups.
- Implementation consequence for `r in {6,7,8,9}`:
  - `r=6`: benchmark orbit matrix dimensions before committing to solver backend.
  - `r=7`: solver choice should be conditioned on matrix sparsity and orbit count.
  - `r=8`: expect NP-hard branching pressure unless orbit compression is very strong.
  - `r=9`: require aggressive preprocessing (dominance/orbit cuts) before any exact-cover attempt.
- Inference: exact-cover viability is dominated by compression quality, not by raw admissibility.
