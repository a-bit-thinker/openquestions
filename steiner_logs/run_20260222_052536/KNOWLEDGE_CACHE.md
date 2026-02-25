# Steiner Knowledge Cache

Run ID: `20260222_052536`
Created (UTC): `2026-02-22T05:25:36Z`
Updated (UTC): `2026-02-22`
Focus instance: `S(6,8,29)`
Round mode: `research-only`

## Bootstrap status
Mandatory memory read completed before new search:
- `steiner_logs/PAPER_NOTES.md`
- `steiner_logs/RESEARCH_LOG.md`
- `steiner_logs/PRACTICE_LOG.md`
- `steiner_logs/RESEARCH_PAPER.md`
- `steiner_logs/EXISTENCE_FRONTIER.md`
- `steiner_logs/run_20260222_052536/REPO_WIDE_HISTORY.md`
- `steiner_logs/run_20260222_012007/notes/round_0001_notes.md`
- `steiner_logs/run_20260222_012007/notes/round_0005_notes.md`
- `steiner_logs/run_20260222_012007/NEXT_GENERATION_TRANSFER.md`

## Local-paper-first result
- Checked `papers/oai_first_proof.pdf` first.
- Local PDF extraction tooling is unavailable in this environment.
- Reused existing local/cached paper notes; no external links added this round.

## Hard gate snapshot (`S(6,8,29)`)
- `|C(29,6)| = 475020`
- expected block count: `b = 16965`
- replication numbers: `lambda_1=4680`, `lambda_2=1170`, `lambda_3=260`, `lambda_4=50`, `lambda_5=8`
- integrality checks: pass (`6/6`, zero remainder)

## Proof-first stack (round1)
1. Asymptotic-to-finite lane: admissibility + absorption obligations.
- Solve-attempt: finite obligations explicitly listed (balance, bounded residual, closure gate).
- Gap: no finite constant instantiation for this exact `n`.

2. Finite bridge lane: Wilson/PBD/lattice compatibility.
- Solve-attempt: bridge obligations defined as decomposition + recomposition checks.
- Gap: no instantiated bridge object in repo.

3. Symmetry/KM lane: orbit-compressed exact-cover.
- Solve-attempt: bounded diagnostics and explicit fallback criteria formalized.
- Gap: non-binary orbit inflation risk requires weighted fallback.

4. Randomized nibble lane: pressure-aware handoff.
- Solve-attempt: handoff signals defined by acceptance decay + `(r-1)` pressure tails.
- Gap: thresholds need round2 calibration.

5. Absorber closure lane: reserve + motif-coupled local repair.
- Solve-attempt: closure staged as `nibble -> repair -> absorber -> residual exact-cover`.
- Gap: absorber templates not yet materialized for this instance.

## Critical-gap loop (3 passes)
1. Arithmetic pass: fail-fast on divisibility witness.
2. Engine pass: bounded symmetry viability test; fallback if weak compression/non-binary mass.
3. Closure pass: residual exact-cover only if strict feasibility and small uncovered residual.

## Typeset-ready theorem skeleton
1. Proposition: admissibility for `S(6,8,29)`.
2. Lemma: finite bridge obligations.
3. Lemma: bounded engine dichotomy.
4. Lemma: strict monotone repair under `c_6<=1`, `c_5<=8`.
5. Lemma: residual closure threshold.
6. Operational theorem: protocol outputs impossibility witness, strict-feasible partial, or full certificate.

## Strong search stack
1. Hard admissibility/divisibility gate.
2. Symmetry/Kramer-Mesner exact-cover mode (bounded).
3. `nibble -> boosting/repair -> absorber -> residual exact-cover` mode.

## Engine-selector rubric
- Prefer symmetry/orbit mode when compression is strong, non-binary coefficients are rare, and bounded probes show immediate strict gains.
- Prefer randomized mode when compression is weak, non-binary mass is material, or `(r-1)` pressure saturates early.

## Practice blockers -> implementation deltas
- Blocker: add-only plateau at saturated `(r-1)` motifs.
- Source: `https://arxiv.org/abs/1611.06827`
- Change: pressure-triggered early destroy/repack handoff.

- Blocker: binary-only orbit search stalls under non-binary coefficients.
- Source: `https://www.sciencedirect.com/science/article/pii/0097316586900944`
- Change: weighted-orbit micro-ILP fallback after bounded binary failure.

- Blocker: premature residual exact-cover spends budget without movement.
- Source: `https://arxiv.org/abs/1401.3665`
- Change: enforce residual eligibility threshold before exact-cover launch.

## Reuse vs new
- Reused: hard gate, bounded symmetry triage, strict feasibility invariants, late exact-cover discipline.
- New: proof-first stack specialized to `S(6,8,29)`, explicit 3-pass gap loop, canonical hypothesis with falsifiable switch rules.

## Source notes
- `https://arxiv.org/abs/1401.3665`: admissibility is necessary baseline; supports theorem-level staging, not early exact closure.
- `https://arxiv.org/abs/1611.06827`: iterative absorption motivates reserve-and-repair pipeline after randomized bulk.
- `https://www.sciencedirect.com/science/article/pii/0097316586900944`: KM/orbit compression motivates bounded symmetry gate and weighted fallback.

## Round1 link/PDF policy
- New links this round: `0`
- New downloadable PDFs saved to `/root/openquestions/papers`: `none`
