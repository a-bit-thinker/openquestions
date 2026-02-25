# Steiner Knowledge Cache

Run ID: 20260222_121719
Created (UTC): 2026-02-22T12:17:19Z
Updated (UTC): 2026-02-22T12:23:03Z

## Focus (this run)
- Instance: `S(6,7,19)` (divisible; expected blocks `b=3876`).
- Round mode: research-only (optimize gates + method transfer; no certificate construction priority).

## Nonnegotiable gates (run before any solver spend)
1. **Divisibility/admissibility**: verify `C(q-i,r-i) | C(n-i,r-i)` for `i=0..r-1` and compute `λ_i`.
2. **Derivation-veto propagation (roadmap)**: if a derived instance hits a *verified* nonexistence, veto the original.
3. **Classical bounds** (roadmap): use Fisher–Ray–Chaudhuri–Wilson / Tits–Cameron style necessary bounds when `q-r>1`.
4. **Residual eligibility** (practice-driven): do not build residual exact-cover instances at high uncovered mass; gate by uncovered fraction + absolute uncovered.

## Strong search stack (canonical)
### A) Symmetry / Kramer–Mesner (KM) orbit lane (bounded)
- Build orbits on `r`- and `q`-subsets under a prescribed group `G ≤ S_n`, form orbit-incidence `A`, solve `Ax=1` over `{0,1}`.
- Diagnostics to decide “stay vs switch”:
  - orbit compression (`|O_q|` vs `C(n,q)`),
  - coefficient profile (non-binary share, max coefficient),
  - early feasibility/runtime of `Ax=1` in SAT/ILP.
- Group menu (roadmap): cyclic `C_n`, dihedral `D_{2n}`, small transitive groups, affine groups when applicable, subgroup-chain relaxations.

### B) Randomized bulk → strict repair → absorber-inspired closure
- Bulk: nibble / greedy build an almost-design quickly.
- Repair: strict add-only until `(r-1)` pressure tails harden, then pressure-triggered destroy/repack neighborhoods.
- Closure discipline: maintain reserve (absorber-like flexibility); only attempt residual exact-cover once residue is small.

## Engine selector rubric (concise)
- Symmetry/orbit compression is plausible when `|O_q|,|O_r|` are tiny and KM coefficients stay mostly binary/low-weight.
- Randomized construction is better when orbit compression is weak, non-binary mass is high, or strict add-only quickly saturates `(r-1)` pressure tails.

## Metrics to track (cross-run comparable)
- Coverage: `exact_once`, `uncovered`, `overcovered`.
- Point degrees: `min/max/gap` and high-quantile tail.
- `(r-1)` pressure: max load, cap-hit count, oversubscribed count.
- Efficiency: accepted move rate, uncovered reduction per 1000 trials, micro-solver hit rate.

## Source Notes (local-first; minimal link churn)
- `papers/Computational and Theoretical Roadmap for Steiner Systems with Strength 6–9 and n _ 200.pdf`
  - Takeaway: derivation-veto propagation from base nonexistences can eliminate divisible small instances on `q=r+1` (e.g., if `S(4,5,17)` is non-existent, then `S(6,7,19)` is vetoed via derivation).
  - Strategy change: prioritize bibliographic closure of base nonexistences; pivot solve portfolio to first not-eliminated frontier (`S(6,7,23)`, `S(7,8,24)`, …) before any heavy exact-cover builds.
- `papers/Computational and Theoretical Roadmap for Steiner Systems with Strength 6–9 and n _ 200.pdf`
  - Takeaway: Kramer–Mesner orbit reduction (`Ax=1`) + a “group menu” provides a bounded symmetry triage lane before raw exact cover.
  - Strategy change: run KM diagnostics first; only commit to orbit-level SAT/ILP when compression + coefficient profile is favorable.
- `papers/arxiv_1401.3665.pdf` (Keevash)
  - Takeaway: randomized-algebraic template + “spill” repair + absorber/cascade closure is the proof-level pattern behind designs.
  - Strategy change: treat construction as staged (template/bulk → spill-fix → closure) and log intermediate residues (“spill size”, repair success).
- `papers/arxiv_1611.06827.pdf` (Glock–Kühn–Lo–Osthus)
  - Takeaway: iterative absorption reframes the algorithm: vortex levels, cover-down, transformers/absorbers for bounded leftovers; plus “boosting” regularity between levels.
  - Strategy change: build a multi-level scheduler (vortex) with per-level residue metrics; reserve absorber capacity early and use cover-down style micro-solves late.
- `papers/oai_first_proof.pdf`
  - Takeaway: workflow discipline—5 seed ideas, independent solve attempts, ≤3 verify/revise loops, then typeset-ready artifact.
  - Strategy change: round1 must output (i) seed fanout, (ii) explicit gap checks, (iii) a final proof outline; avoid single-track essay loops.

## Highest-value open obligation
- Close the **bibliographic gap** for the roadmap’s base nonexistence claims (at least `S(4,5,17)` and `S(5,6,16)`) so derivation-veto can be enforced as a hard portfolio gate.
