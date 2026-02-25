# Next Generation Transfer

Generated (UTC): 2026-02-22T12:23:03Z
Run directory: steiner_logs/run_20260222_121719

## Scope
- This run is currently **round1 research-only** (no solve rounds executed yet).
- Goal: preserve the gate stack + method transfers so rounds 2+ can execute without re-deriving theory.

## Round1 Snapshot
- Instance: `S(6,7,19)`
- Expected blocks: `3876`
- Divisibility/admissibility: pass (all remainders `0`; `λ_5=7`)
- Status: **provisional derivation-veto** (roadmap claims `S(4,5,17)` nonexistence ⇒ `S(6,7,19)` veto via derivation; requires primary-source verification).

## Core Advances (research-only)
- Integrated the roadmap’s two highest-leverage mechanisms into the canonical pipeline:
  - **Derivation-veto nonexistence propagation** as a front gate (cheap family elimination).
  - **Kramer–Mesner orbit reduction** + “group menu” as a bounded symmetry triage lane.
- Wrote a full **proof-first round1 stack** (5 seed proof lanes + ≤3 verification loops + typeset-ready conditional nonexistence outline).
- Mapped **practice blockers (rounds2–5)** to concrete implementation deltas with validation metrics (pressure-triggered repacks, residual eligibility gating, weighted-orbit fallback, motif taboo cache).

## Immediate Next Actions (Rounds 2+)
1. Close the **bibliographic gap**: obtain primary references/PDFs for `S(4,5,17)` nonexistence (and `S(5,6,16)` if used) so derivation-veto becomes a hard gate.
2. If veto is verified: remove `S(6,7,19)` and the entire `n=r+13` line from the solve queue; pivot to the first not-eliminated frontier (`S(6,7,23)`, then `S(7,8,24)`, `S(8,9,25)`, `S(9,10,26)`).
3. On the new portfolio: run **bounded KM diagnostics first**, then choose KM vs randomized construction by orbit compression + coefficient profile.
4. Enforce the residual exact-cover eligibility gate (do not repeat “early residual” at high uncovered mass).

## Metrics Contract (track every checkpoint)
- Coverage: `exact_once`, `uncovered`, `overcovered`.
- Point degrees: `min/max/gap` and tail.
- `(r-1)` pressure: max load, cap-hit count, oversubscribed count.
- Efficiency: accepted move rate, uncovered reduction per 1000 trials, micro-solver hit rate.

## Transfer Notes (reuse vs new)
- Reused: strict feasibility backbone, bounded engine selection, residual gating discipline, practice-derived falsification windows.
- New: instance-specialized derivation-veto proof outline for `S(6,7,19)` + roadmap KM group-menu integration + explicit “bibliographic gap” stop condition.
