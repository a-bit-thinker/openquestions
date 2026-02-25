# Next Generation Transfer

Generated (UTC): `2026-02-22T05:10:43Z`
Updated (UTC): `2026-02-22`
Run directory: `steiner_logs/run_20260222_051043`

## Scope
- Current run status: round1 research completed (no solve rounds executed yet).
- Goal of this transfer: allow round2+ execution without re-deriving theory.

## Round1 Snapshot
- Mode: research-only
- Instance focus: `S(6,8,29)`
- Admissibility: pass (`expected_blocks=16965`, `lambda_5=8`)
- New external links: `0`
- New PDFs saved under `papers/`: `none`

## Core advances from this round
1. Built a proof-first stack with five seeded proof lanes and explicit gaps.
2. Added a 3-loop critical-gap verification routine (arithmetic, engine, closure).
3. Formalized the strong search stack:
- hard admissibility/divisibility gate,
- bounded symmetry/Kramer-Mesner mode,
- `nibble -> boosting/repair -> absorber -> residual exact-cover` mode.
4. Mapped practice blockers to source-backed implementation deltas.
5. Added a concise engine-selector rubric and round2+ metric contract.

## Reused vs new (explicit)
- Reused:
  - admissibility-first gate,
  - bounded symmetry triage,
  - strict feasibility invariants.
- New:
  - finite-size bridge obligation explicitly added for `S(6,8,29)`,
  - blocker-to-implementation mapping tied to rounds2-5 failures,
  - unified theorem-sized active hypothesis for hybrid dominance.

## Practice blockers -> concrete next changes
1. Blocker: binary-orbit symmetry stalls on non-binary coefficients.
- Next change: add weighted-orbit micro-ILP fallback neighborhoods.

2. Blocker: add-only plateau at saturated `(r-1)` motifs.
- Next change: pressure-triggered early handoff to strict destroy/repack.

3. Blocker: residual exact-cover launched too early.
- Next change: enforce residual eligibility threshold before exact mode.

## Mandatory round2+ execution order
1. Stage A: admissibility and sizing gate (`lambda_i`, expected blocks).
2. Stage B: bounded symmetry diagnostics and optional orbit-seeded build.
3. Stage C: randomized nibble + strict boosting/repair.
4. Stage D: absorber-reserved motif-coupled repacks.
5. Stage E: residual exact-cover only if strict residual eligibility passes.

## Metrics to track every checkpoint
- Point degree: `min/max/gap`.
- `(r-1)` pressure: max load, cap-tail counts, oversubscribed count.
- Coverage: `exact_once`, `uncovered`, `overcovered`.
- Efficiency: accepted-move rate, gain per 1000 trials, micro-augment hit rate.

## Active hypotheses for immediate testing
1. Hybrid selector hypothesis.
- Expectation: better uncovered-reduction slope vs single-engine baselines.
- Stop condition: reject if 3 matched seeds show no slope gain.

2. Weighted-orbit fallback hypothesis.
- Expectation: better seed quality when binary orbit mode stalls.
- Stop condition: reject if gain is `< +0.5%` exact-once over matched budget.

3. Motif-coupled repack hypothesis.
- Expectation: better strict `k -> k+1` hit rate in coupled neighborhoods.
- Stop condition: reject if `>=400` accepted neighborhoods give `< +20` net blocks.

## Immediate round2 target
- Instance: `S(6,8,29)`
- Priority: execute Stage A-E with matched-seed calibration of handoff thresholds.
- Non-negotiable invariants: `overcovered=0`, zero `(r-1)` oversubscription.
