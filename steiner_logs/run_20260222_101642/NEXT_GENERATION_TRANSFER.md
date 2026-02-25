# Next Generation Transfer

Generated (UTC): 2026-02-22T10:16:42Z
Run directory: steiner_logs/run_20260222_101642

## Scope
- This run is **round1 research-only** (no certificate construction prioritized).
- Goal: preserve the highest-signal gates + method transfers so rounds2+ do not repeat essay loops.

## Latest Round Snapshot
- Round: 1 (research)
- Instance: `S(6,7,19)`
- Divisibility: **passes** (`b=3876`, `λ_5=7`)
- New critical note: the **local roadmap PDF** asserts `S(4,5,17)` is non-existent; by derivation veto this would eliminate
  `S(6,7,19)` via `S(6,7,19) -> S(5,6,18) -> S(4,5,17)`.
- Status: treat as **provisional until primary-source verification** of the base nonexistence claim, but enforce as a pre-solve gate.

## Core Advances (transfer value)
1. Added a **derivation-veto nonexistence gate** (beyond divisibility) as the first decision point.
2. Promoted roadmap mechanisms into the canonical pipeline:
   - Kramer–Mesner orbit method (`Ax=1` on orbit-incidence) as the symmetry engine,
   - exact-cover size metrics to rank feasibility before committing to solvers.
3. Updated the primary synthesis artifact `steiner_logs/RESEARCH_PAPER.md` with:
   - 4 falsifiable claims grounded in repo verifier metrics,
   - a mandatory “Source-to-Method Transfer” mapping table (all local PDFs),
   - explicit retired/active hypotheses and stop conditions.
4. Filled `notes/round_0001_notes.md` with a proof-first stack (5 seeds), 3-round gap verification loop, and a typeset-ready
   conditional nonexistence outline.

## Knowledge Gaps / Blockers
- The repo currently encodes **divisibility-only** feasibility; it does not encode a verified seed list of known nonexistences
  and derivation propagation.
- Practice evidence shows repeated wasted effort on:
  - add-only plateau at saturated `(r-1)` pressure,
  - symmetry stalls under non-binary orbit coefficients,
  - premature residual exact-cover attempts.

## Concrete Next Actions (rounds2+)
1. **Verify and encode** the roadmap’s base nonexistence facts (at minimum `S(4,5,17)`; optionally `S(5,6,16)` if confirmed),
   then propagate by repeated derivation in portfolio selection.
2. Re-run portfolio selection excluding vetoed triples; likely next frontier starts at:
   `S(6,7,23)`, `S(7,8,24)`, `S(8,9,25)`, `S(9,10,26)`.
3. On any non-vetoed instance, execute the canonical hybrid protocol:
   `bounded symmetry/KM triage -> strict constructive bulk -> pressure-triggered destroy/repack + absorber reserve -> late residual gate`.

## Mandatory Metrics (track every checkpoint)
- Point degree spread: `min/max/gap` vs target `λ_1`.
- `(r-1)` pressure: `max load`, `cap-hit count`, `oversubscribed count` (must stay `0` under strict).
- Coverage: `exact_once`, `uncovered`, `overcovered` (strict requires `overcovered=0`).
- Efficiency: accepted move rate; uncovered reduction per 1000 trials; micro-pack hit rate (for LNS).
- Symmetry diagnostics (if used): compression ratio, KM matrix nnz, non-binary coefficient share.

## Next Hypothesis (canonical)
Adding a verified derivation-veto nonexistence gate before portfolio selection will increase useful solve yield per compute by
eliminating impossible divisibility-admissible instances, while the existing bounded-symmetry + strict-repair hybrid remains
dominant on the remaining unknown set.

## Falsification / Stop Conditions
- Reject the derivation-veto gate immediately if any vetoed instance later gets a valid certificate in this repo.
- Reject the hybrid dominance claim if, on three matched seeds for a non-vetoed instance, it fails to beat add-only baseline
  on uncovered-reduction slope while maintaining strict feasibility invariants.
