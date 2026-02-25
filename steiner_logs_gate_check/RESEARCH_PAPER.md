# Research Synthesis Paper (Round1 Backbone)

Generated (UTC): `2026-02-22T04:40:00Z`
Updated (UTC): `2026-02-22`
Log root: `steiner_logs`

## Abstract
This project studies constructive existence search for Steiner systems `S(r,q,n)` with `n > q > r > 5`, `r < 10`, `n < 200`. Across the repository, admissibility (Steiner divisibility) is the dominant global filter, but admissibility alone has not yet yielded full certificates for any unresolved instance.

The strongest cross-run conclusion is operational: successful progress requires a staged protocol, not a single solver mode. The protocol is: hard arithmetic gate, bounded symmetry triage, strict-feasible constructive repair, and late residual exact-cover only when residual size is small enough. Round1 in the current run extends this with an explicit proof-first lemma stack for `S(6,8,29)`.

## Problem Statement
Given `[n] = {1, ..., n}`, find a block family `B subseteq C([n], q)` such that every `r`-subset of `[n]` appears in exactly one block.

For the current round focus instance `S(6,8,29)`:
- `|C(29,6)| = 475020`
- expected block count `b = 16965`
- admissibility checks pass (`lambda_1=4680`, `lambda_5=8`)

## Strongest Prior Claims
### Claim 1 (Arithmetic gate is decisive)
Divisibility constraints are a hard partition of the search space; most triples are impossible before any constructive search.

Evidence: The frontier report has `72964` triples scanned and only `254` admissible (`72710` ruled out by divisibility). For `S(6,8,29)`, all six integrality checks pass with remainder `0`, so this instance is in the admissible-but-unknown set.

### Claim 2 (Engine choice must be instance-adaptive)
A bounded symmetry pass is useful, but prolonged symmetry-only search is not uniformly effective.

Evidence: In `S(9,10,22)`, cyclic diagnostics were strong (`48/29414` non-binary columns) and produced a high-quality strict seed (`23716` blocks, `overcovered=0`). In other higher-`r` runs, non-binary inflation and sparse binary improvements forced early handoff to repair lanes. This supports a bounded selector, not a fixed symmetry-first dogma.

### Claim 3 (Strict-feasible repair yields transferable monotone gains)
Maintaining `overcovered=0` and zero `(r-1)` oversubscription preserves valid progress structure even when gains are sparse.

Evidence: Cross-run strict lanes repeatedly improved exact-once counts while preserving hard constraints, e.g. `S(9,10,22)` moved `23716 -> 23752` blocks with `overcovered=0` throughout; `S(6,7,23)` improved to score `50.09` with `overcovered=0` and large uncovered reduction.

### Claim 4 (Residual exact-cover is a late-phase theorem, not an early tool)
Residual exact completion is structurally premature when uncovered mass is still large.

Evidence: In the best `S(9,10,22)` strict run, uncovered remained `259900/497420 = 0.5225`; exact residual completion was correctly rejected at that stage. Similar early-exact attempts in other runs did not produce frontier gains.

## Lemma Chain
1. Lemma A (Admissibility).
- Verify all divisibility conditions and replication numbers `lambda_i`.
- If any condition fails, emit arithmetic impossibility certificate.

2. Lemma B (Finite bridge obligation).
- Translate asymptotic design machinery into finite obligations (local balance, decomposition compatibility, recomposition consistency) for target `n`.

3. Lemma C (Bounded engine dichotomy).
- Run bounded orbit diagnostics (compression, non-binary share, coefficient ceiling).
- Either keep symmetry-compressed exact-cover mode or certify fallback to randomized mode.

4. Lemma D (Strict monotone repair).
- Under hard caps (`c_r<=1`, `c_{r-1}<=lambda_{r-1}`), accepted moves preserve feasibility and reduce residual pressure metrics in expectation.

5. Lemma E (Residual closure threshold).
- Residual exact-cover is attempted only after strict feasibility plus uncovered-mass threshold.

6. Operational Theorem.
- The staged protocol outputs one of: arithmetic impossibility, strict-feasible improved partial certificate, or full certificate.

## Proof Strategy
1. Start with arithmetic certification (`lambda_i`, expected block count, divisibility remainders).
2. Execute bounded symmetry diagnostics; avoid long unbounded orbit search before quality evidence.
3. If symmetry quality is strong, seed from orbit-compressed structure; otherwise use randomized nibble seed.
4. Enforce strict feasibility during all repair operations.
5. Shift from add-only to motif-coupled repacks when `(r-1)` pressure tails rise.
6. Attempt exact residual closure only after explicit eligibility gates are satisfied.

## Failure Certificates
- Certificate F1 (Arithmetic failure): record the first `(i, numerator, denominator, remainder!=0)` witness.
- Certificate F2 (Engine mismatch): report bounded symmetry diagnostics proving weak compression or heavy non-binary mass; justify randomized fallback.
- Certificate F3 (Strict infeasibility): provide first violated constraint (`overcovered>0` or oversubscribed `(r-1)` subset) and rollback witness.
- Certificate F4 (Residual ineligible): provide uncovered fraction and strict-gate status showing exact residual mode is premature.

## Next Theorem-Sized Hypothesis
Hypothesis T (`S(6,8,29)` hybrid dominance):
Given admissibility for `S(6,8,29)`, a bounded symmetry triage followed by pressure-triggered strict repair (with absorber reserve) achieves better uncovered-reduction slope than either prolonged symmetry-only search or add-only strict growth under matched budgets, while preserving `overcovered=0` and zero `(r-1)` oversubscription.

Why theorem-sized: it is a single canonical statement that unifies earlier overlapping hypotheses about engine choice, pressure-triggered handoff, and strict repair discipline.

## Retired Hypotheses
- Long binary-only symmetry exploration as default at high `r`.
- Add-only continuation after strict frontier saturation.
- Early residual exact-cover invocation without residual-size gating.

## Active Hypotheses
1. Hybrid selector hypothesis.
- Bounded symmetry triage plus pressure-triggered handoff dominates single-engine policies on admissible unsolved instances.

2. Weighted-orbit fallback hypothesis.
- Weighted KM neighborhoods recover useful symmetry information when binary-orbit mode stalls.

3. Motif-coupled repack hypothesis.
- Coupled `k -> k+1` local repacks around shared motifs outperform uncoupled windows at strict frontiers.

4. Residual-threshold hypothesis.
- Explicit residual eligibility thresholds reduce wasted exact-cover compute and improve net gain per wall-time.

## Falsification Criteria
- Reject Hypothesis 1 if three matched seeds show no improvement in uncovered-reduction slope over add-only baseline.
- Reject Hypothesis 2 if weighted-orbit fallback yields `< +0.5%` exact-once gain over binary-only fallback across matched budget.
- Reject Hypothesis 3 if after `>=400` accepted LNS neighborhoods, net block gain is `< +20`.
- Reject Hypothesis 4 if residual exact-cover launched below threshold does not improve coverage per unit time relative to continued strict repair.

## Strongest Prior Claims to Carry Forward
- Arithmetic admissibility is necessary and must remain a hard gate.
- Engine choice is empirical and should be decided by bounded diagnostics.
- Strict feasibility invariants preserve reliable transfer across runs.
- Residual exact-cover belongs only at late stage after threshold gating.

## References (minimal working set)
- Keevash, existence framework: `https://arxiv.org/abs/1401.3665`
- Glock, Kuhn, Lo, Osthus, iterative absorption framing: `https://arxiv.org/abs/1611.06827`
- Kramer-Mesner computational design framework: `https://www.sciencedirect.com/science/article/pii/0097316586900944`
