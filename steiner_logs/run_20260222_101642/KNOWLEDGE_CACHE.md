# Steiner Knowledge Cache

Run ID: 20260222_101642
Created (UTC): 2026-02-22T10:16:42Z

Instance focus (round1): `S(6,7,19)` (admissible by divisibility; expected blocks `b=3876`).

## High-Signal Gates (apply before any solver spend)
1. **Divisibility/admissibility** (mandatory): verify `\binom{q-i}{r-i} | \binom{n-i}{r-i}` for `i=0..r-1`; record the witness table.
2. **Derivation-veto nonexistence propagation** (roadmap): if `S(r,q,n)` exists then `S(r-1,q-1,n-1)` exists.
   - Roadmap asserts `S(4,5,17)` is non-existent; if verified, this eliminates `S(6,7,19)` via:
     `S(6,7,19) -> S(5,6,18) -> S(4,5,17)`.
3. **Residual exact-cover eligibility**: only attempt residual exact-cover when the uncovered set is *small* (count/ratio gates).

## Strong Search Stack (two-engine policy)
### Engine A: Symmetry / Kramer–Mesner orbit exact-cover
Use when orbit compression is strong under a group `G <= S_n`.
- Build orbit-incidence `A` and solve `Ax=1` over `x in {0,1}` (SAT/ILP/DLX on orbit variables).
- Diagnostics to record: `|O_r|, |O_q|, nnz(A), max coefficient, non-binary share`.

### Engine B: Randomized constructive (iterative absorption-inspired)
Use when symmetry compression is weak or KM coefficients inflate.
- `nibble/greedy bulk -> strict repair/boost -> absorber reserve -> residual exact-cover`.
- Keep strict invariants (when constructing partial packings): `overcovered=0`, `oversubscribed_(r-1)=0`.

## Engine Selector Rubric (concise)
- Symmetry/orbit compression is plausible when `|O_q|, |O_r|` are orders-of-magnitude smaller than `\binom{n}{q}, \binom{n}{r}`
  and KM coefficients are mostly binary/low-weight.
- Randomized is better when compression is weak, non-binary mass is high, or strict add-only quickly saturates `(r-1)` pressure.

## Exact-Cover Size Metrics (roadmap; useful for feasibility ranking)
For `S(r,q,n)`:
- rows `= \binom{n}{r}`, cols `= \binom{n}{q}`
- row degree `= \binom{n-r}{q-r}`
- incidences `= \binom{n}{r}\binom{n-r}{q-r} = \binom{n}{q}\binom{q}{r}`

For `S(6,7,19)` specifically:
- rows `27132`, cols `50388`, row degree `13`, incidences `352716` (direct DLX/SAT is memory-feasible if needed).

## Practice-Driven Blockers -> Deltas (carry into rounds2+)
- Missing gate: divisibility-only portfolio selection can choose derivation-veto eliminated triples.
  - Delta: encode a verified nonexistence seed list + derivation propagation into portfolio selection.
- Add-only plateau at high `(r-1)` pressure tails.
  - Delta: pressure-triggered destroy/repack + absorber reserve (iterative absorption framing).
- Binary symmetry stall under non-binary orbit coefficients.
  - Delta: weighted-orbit fallback after bounded binary KM.
- Early residual exact-cover attempts at large residual mass.
  - Delta: enforce uncovered eligibility thresholds before residual builders/solvers.

## Source Notes (local-first; minimal links)
- `papers/Computational and Theoretical Roadmap for Steiner Systems with Strength 6–9 and n _ 200.pdf`
  - Takeaway: derivation veto is a powerful nonexistence propagator; KM orbit method `Ax=1` is the symmetry-compressed lane; exact-cover size metrics guide feasibility.
  - Strategy change: add derivation-veto nonexistence gate + bounded KM triage before randomized repair.
- `papers/arxiv_1401.3665.pdf` (Keevash)
  - Takeaway: template + spill + local modification / absorption makes asymptotic existence operational as a *staged algorithm sketch*.
  - Strategy change: treat “spill size” and “local fix success” as explicit metrics; do not expect one-shot exact cover to scale.
- `papers/arxiv_1611.06827.pdf` (Glock–Kühn–Lo–Osthus)
  - Takeaway: vortex + cover-down + transformers/absorbers + regularity boosting is the canonical staged decomposition blueprint.
  - Strategy change: schedule search in vortex-like phases; reserve absorbers early; use cover-down micro-solves in repair.
- `papers/oai_first_proof.pdf`
  - Takeaway: seed-idea fanout + up-to-3 verify/revise loops produces higher-quality proof artifacts and reduces repeated round1 essays.
  - Strategy change: keep round1 “proof-first stack” as a repeatable template for each new instance.

## Reuse vs New (explicit)
- Reused: hybrid engine policy + strict invariants + residual gating from prior runs.
- New: roadmap-driven derivation-veto nonexistence triage and KM `Ax=1` framing are now first-class gates.
