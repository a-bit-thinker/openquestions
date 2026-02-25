# Steiner Knowledge Cache

Run ID: `20260222_051043`
Created (UTC): `2026-02-22T05:10:43Z`
Updated (UTC): `2026-02-22`
Instance focus: `S(6,8,29)` (`expected_blocks=16965`, admissible)

## Round-1 objective
- Build a proof-first research cache for unknown large Steiner construction.
- Prioritize gate design, lemma chain quality, and falsifiable execution rules.
- Defer certificate construction to solve rounds.

## Reused from prior runs
- Hard admissibility/divisibility gate as non-negotiable precondition.
- Bounded symmetry gate (diagnose first, do not over-invest when coefficients inflate).
- Strict feasibility discipline (`overcovered=0`, no `(r-1)` oversubscription).
- Staged randomized pipeline ending in late residual exact-cover.

## Genuinely new in this run
- Proof-first stack specialized to `S(6,8,29)` with five explicit proof seeds.
- Three-loop critical-gap verification protocol tied to stop/switch rules.
- Finite-size bridge obligation elevated to explicit lemma for `n=29`.
- Practice blockers mapped to source-backed implementation deltas for rounds2+.

## Proof-first Round-1 stack
1. Seed A (asymptotic existence spine)
- Idea: divisibility + approximate decomposition + absorption.
- Gap: asymptotic constants not instantiated at `n=29`.

2. Seed B (finite PBD/Wilson bridge)
- Idea: finite decomposition scaffold closes asymptotic-to-finite gap.
- Gap: explicit scaffold for `S(6,8,29)` is missing.

3. Seed C (symmetry-compressed KM)
- Idea: orbit compression may make exact-cover tractable.
- Gap: non-binary coefficient inflation can break binary-only search.

4. Seed D (pressure-aware nibble)
- Idea: random greedy covers bulk quickly.
- Gap: handoff thresholds must be calibrated for this instance.

5. Seed E (absorber + strict local repair)
- Idea: reserve slack early, then execute motif-coupled `k -> k+1` repacks.
- Gap: absorber template library is not yet instantiated.

## Critical-gap verification loop
1. Arithmetic loop: verify divisibility + `lambda_i` integrality.
2. Engine loop: bounded symmetry diagnostics, then route by compression/coefficients.
3. Closure loop: enforce strict feasibility and residual-eligibility threshold before exact cover.

## Strong search stack
1. Hard admissibility/divisibility gate.
2. Symmetry/Kramer-Mesner exact-cover mode (bounded).
3. `nibble -> boosting/repair -> absorber -> residual exact-cover` mode.

## Engine-selector rubric
- Prefer symmetry/orbit mode when compression is high and non-binary orbit mass is low.
- Prefer randomized mode when compression is weak, coefficients inflate, or `(r-1)` tails harden early.

## Practice blockers -> implementation deltas
1. Blocker: binary-only orbit probes stall on non-binary coefficients.
- Source: `https://www.sciencedirect.com/science/article/pii/0097316586900944`
- Change: weighted-orbit micro-ILP neighborhoods after bounded binary failure.

2. Blocker: add-only growth plateaus at saturated `(r-1)` motifs.
- Source: `https://arxiv.org/abs/1611.06827`
- Change: pressure-triggered early handoff to destroy/repack with reserved slack.

3. Blocker: residual exact-cover attempted too early.
- Source: `https://arxiv.org/abs/1401.3665`
- Change: strict residual-eligibility gate (low uncovered fraction + strict feasibility).

## Source Notes
- `https://arxiv.org/abs/1401.3665`
  - Takeaway: admissibility plus absorption gives asymptotic existence architecture.
  - Strategy impact: keep admissibility as hard gate and treat exact closure as late phase.

- `https://arxiv.org/abs/1611.06827`
  - Takeaway: iterative absorption supports staged constructive completion.
  - Strategy impact: pipeline design should separate bulk random coverage from structured repair/closure.

- `https://www.sciencedirect.com/science/article/pii/0097316586900944`
  - Takeaway: Kramer-Mesner orbit methods require coefficient-aware handling.
  - Strategy impact: include weighted-orbit fallback; avoid binary-only assumptions.

## Link policy (this round)
- New external links added: `0`.
- New PDFs downloaded to `papers/`: `none`.
