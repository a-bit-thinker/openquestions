# Steiner Knowledge Cache

Run ID: 20260222_110632
Created (UTC): 2026-02-22T11:06:32Z
Updated (UTC): 2026-02-22T11:14:03Z

## Purpose
High-signal cache for *finite* (n<200) `S(r,q,n)` work in `r∈{6,7,8,9}`: what to gate, what to try, what to stop.

## Hard Gates (do before any solver spend)
1. **Divisibility/admissibility**: check `\binom{q-i}{r-i} | \binom{n-i}{r-i}` for all `i=0..r-1`; compute forced block count
   `b = \binom{n}{r}/\binom{q}{r}` and replications `λ_i`.
2. **Classical lower bounds** (roadmap): Ray–Chaudhuri–Wilson + Tits + Cameron bounds; mainly useful when `q−r>1`.
3. **Derivation-veto propagation** (roadmap): derivation closure `S(r,q,n) ⇒ S(r-1,q-1,n-1)` lets any verified base nonexistence
   eliminate whole families.

## Roadmap-derived nonexistence propagation (q=r+1 line)
Provisional until base sources are verified:
- If `S(4,5,17)` is non-existent, it eliminates all `S(t,t+1,t+13)` for `t≥4`, so knocks out `(6,7,19),(7,8,20),(8,9,21),(9,10,22)`.
- If `S(5,6,16)` is non-existent, it eliminates all `S(t,t+1,t+11)` for `t≥5`, so knocks out `(6,7,17),(7,8,18),(8,9,19),(9,10,20)`.
- Therefore the smallest not-yet-eliminated `q=r+1` starts become: `S(6,7,23)`, `S(7,8,24)`, `S(8,9,25)`, `S(9,10,26)`.

## Strong Search Stack (engines)
### Symmetry/Kramer–Mesner exact-cover mode (orbit compressed)
- Prescribe `G ≤ S_n`, enumerate orbits on `r`- and `q`-subsets, form orbit-incidence matrix `A`, solve `Ax=1` with `x∈{0,1}^{|O_q|}`.
- Start groups: cyclic/dihedral; affine groups for prime-ish `n`; small transitive groups; relax via subgroup chains if no solution.
- Diagnostics to log before committing: `|O_r|,|O_q|`, non-binary share, max coefficient, KM nnz.

### Randomized mode: nibble → boosting/repair → absorber → residual exact-cover
- Bulk: random greedy/nibble to cover most `r`-subsets quickly.
- Repair: strict add-only until acceptance collapses or `(r-1)` pressure tails hit cap; then destroy/repack neighborhoods (motif-coupled).
- Absorber discipline: reserve flexibility early; spend to unblock saturated motifs.
- Residual exact-cover: only after explicit eligibility gate (residual is small; pressure controlled).

## Engine selector rubric (1-screen)
- Prefer symmetry/orbit compression when orbit counts are small *and* coefficients are mostly binary/low-weight (KM is then a real reduction).
- Prefer randomized+repair when compression is weak, non-binary mass inflates, or strict add-only quickly saturates `(r-1)` tails.

## Practice-derived blockers → research deltas (what to change)
- **Dead instances**: implement derivation-veto propagation so divisibility-admissible but vetoed triples are never scheduled.
- **Add-only plateau**: add pressure-triggered destroy/repack (absorption-inspired), not more add-only.
- **Binary-KM stalls**: add coefficient diagnostics + weighted-orbit fallback (ILP neighborhoods) instead of extending binary budget.
- **Early residual exact-cover**: enforce uncovered-fraction/size eligibility before building residual instances.
- **Duplicate neighborhoods**: motif signature cache + short taboo window.

## Metrics contract (always log)
- Point degree distribution: min/max/gap + tail quantiles.
- `(r-1)` pressure: max load, cap-hit count, oversubscribed count.
- Coverage: `exact_once`, `uncovered`, `overcovered`.
- Efficiency: accepted-move rate; uncovered reduction per 1000 trials; micro-augment hit rate.

## Source Notes (minimal, local-first)
- `papers/Computational and Theoretical Roadmap for Steiner Systems with Strength 6–9 and n _ 200.pdf`:
  derivation-veto propagation + KM orbit workflow + frontier ranking ⇒ *shift portfolio* from smallest admissible `n` to smallest not-vetoed `n`.
- `https://arxiv.org/abs/1401.3665`:
  template→spill→local modification (cascade) framing ⇒ treat construction as staged “near-solution then repair”, not monolithic exact cover.
- `https://arxiv.org/abs/1611.06827`:
  vortex/cover-down/absorber language ⇒ implement level-by-level residual accounting and cover-down micro-solvers before final closure.
- `papers/oai_first_proof.pdf`:
  5-seed idea fanout + ≤3 verify/revise loops ⇒ round1 output must be falsifiable and typeset-ready, not a single-track essay.
