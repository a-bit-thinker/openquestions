# Next Generation Transfer

Generated (UTC): 2026-02-22T11:06:32Z
Updated (UTC): 2026-02-22T11:14:03Z
Run directory: steiner_logs/run_20260222_110632

## Scope
- This run is **round1 research-only** (no certificate construction prioritized).
- Primary artifact updated: `steiner_logs/RESEARCH_PAPER.md`.
- Run-local artifacts: `steiner_logs/run_20260222_110632/notes/round_0001_notes.md`, `steiner_logs/run_20260222_110632/KNOWLEDGE_CACHE.md`.

## Round 1 Snapshot (research)
- Instance: `S(6,7,19)`
- Divisibility: pass (expected blocks `3876`, `λ_5=7`)
- Status: **provisionally vetoed** pending primary-source verification of roadmap base nonexistences.

## Core Advances (transferable)
1. **Derivation-veto gate expanded (roadmap)**:
   - If verified, `S(4,5,17)` eliminates `(6,7,19),(7,8,20),(8,9,21),(9,10,22)`.
   - If verified, `S(5,6,16)` eliminates `(6,7,17),(7,8,18),(8,9,19),(9,10,20)`.
   - Portfolio pivot on `q=r+1` becomes: `S(6,7,23)`, `S(7,8,24)`, `S(8,9,25)`, `S(9,10,26)`.
2. **Proof-first round1 stack now filled**: 5 seeded lanes + 3-round verification loop + typeset-ready conditional nonexistence outline.
3. **Strong search stack locked**: hard gates → bounded KM triage → randomized/repair/absorber → residual exact-cover only when eligible.
4. **Practice-driven deltas preserved**: add-only plateau triggers repack; early residual is retired; symmetry must be diagnostics-bounded.

## Immediate Next Steps (Rounds 2+)
1. **Verify base nonexistence sources** for `S(4,5,17)` and `S(5,6,16)` (download/store PDFs; record provenance).
2. **Implement derivation-veto propagation** in `math_proofs/steiner_portfolio.py` and surface witness chains in `math_proofs/steiner_system.py`.
3. **Re-rank portfolio** after veto; do not schedule solve rounds on eliminated triples unless veto is downgraded.
4. **Run bounded KM diagnostics first** on the new smallest open starts; switch engines early if compression/coefficients fail.

## Metrics to Track (every checkpoint)
- Point degree: min/max/gap + tail quantiles.
- `(r-1)` pressure: max load, cap-hit count, oversubscribed count (must stay 0 in strict mode).
- Coverage: `exact_once`, `uncovered`, `overcovered`.
- Efficiency: accepted moves per 1000 trials; uncovered reduction slope; micro-augment hit rate.

## Stop / Reject Conditions
- If any derivation-vetoed instance later yields a valid certificate in this repo, immediately reject the veto implementation and require source re-verification.
- If symmetry diagnostics show weak compression or high non-binary mass, stop extending the symmetry budget and switch to randomized+repair.
- Do not attempt residual exact-cover unless a residual eligibility gate is satisfied (uncovered is small and pressure controlled).
