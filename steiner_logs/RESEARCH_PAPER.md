# Research Synthesis Paper (Round1 Backbone)

Generated (UTC): `2026-02-22T04:40:00Z`
Updated (UTC): `2026-02-22T13:59:46Z`
Log root: `steiner_logs`
Focus run: `run_20260222_135457`

## Abstract
This project studies constructive existence and/or nonexistence for Steiner systems `S(r,q,n)` in the regime
`n > q > r > 5`, `r ∈ {6,7,8,9}`, `n < 200`, using repository-scale evidence from research rounds (round1)
and solve rounds (rounds2–5). The key synthesis is operational:

1) **Divisibility is necessary but incomplete at small `n`**; adding a **derivation-veto nonexistence gate**
can eliminate divisibility-admissible triples (notably on the `q=r+1` line) before any solver spend.

2) For triples that survive all gates, success is not tied to a single method; it depends on a **staged engine
policy**: bounded symmetry/Kramer–Mesner (KM) triage when orbit compression is strong, otherwise randomized
bulk + strict repair + absorption-inspired closure. Residual exact-cover is reserved for late-stage residues only.

## Problem Statement
Given `[n]={1,…,n}`, find `\mathcal{B} ⊆ \binom{[n]}{q}` such that every `r`-subset appears in **exactly one** block.
Equivalently, find an exact cover of the row set `\binom{[n]}{r}` by columns `\binom{[n]}{q}` where a column covers
the `\binom{q}{r}` rows induced by a block.

### Current focus instance: `S(6,7,19)` (divisible; provisional veto)
Arithmetic snapshot (divisibility passes):
- Total required `r`-subsets: `\binom{19}{6} = 27132`
- Expected blocks: `b = \binom{19}{6}/\binom{7}{6} = 27132/7 = 3876`
- Replications: `λ_1 = 1428`, `λ_5 = 7`

Exact-cover sizing (useful for feasibility ranking):
- Rows `= \binom{19}{6} = 27132`
- Columns `= \binom{19}{7} = 50388`
- Row degree `= \binom{19-6}{7-6} = \binom{13}{1} = 13`
- Total incidences `= \binom{19}{6}\binom{13}{1} = \binom{19}{7}\binom{7}{6} = 352716`

### Immediate nonexistence triage (from local roadmap)
The local roadmap PDF reports (i) a proven base nonexistence `S(4,5,17) ≁ exists` (Östergård–Pottonen),
and (ii) a recorded base nonexistence `S(5,6,16) ≁ exists` (tabulated by van der Pol), and stresses
**derivation** as a closure property: `S(r,q,n) ⇒ S(r-1,q-1,n-1)` by fixing a point and deleting it from
incident blocks. If these base facts are correct, then `S(6,7,19)` is eliminated by repeated derivation:
`S(6,7,19) -> S(5,6,18) -> S(4,5,17)`.

This paper therefore treats `S(6,7,19)` as **divisible-but-provisionally-vetoed** pending primary-source verification
of the base nonexistence claim. The most valuable output in this state is not a partial certificate; it is a gate
stack that prevents repeated solver spend on instances likely eliminated by derivation.

### Portfolio pivot after derivation-veto (roadmap-guided)
If the two base nonexistences above are verified, then along the `q=r+1` line the first admissible `n` for
`r∈{6,7,8,9}` is eliminated at offsets `+11` and `+13`, so the smallest *not-yet-eliminated* starts become:
`S(6,7,23)`, `S(7,8,24)`, `S(8,9,25)`, `S(9,10,26)`. These have `\binom{n}{r}` rows
`= 100947, 346104, 1081575, 3124550` and expected block counts `b = 14421, 43263, 120175, 312455`
respectively.

## Strongest Prior Claims

### Claim 1: Divisibility is mandatory but incomplete at `n<200`; a derivation-veto nonexistence gate is required.
Evidence: The repo’s divisibility sieve finds only `254/72964 ≈ 0.00348` admissible triples in the `r=6..9, n<200`
domain, so divisibility is already a near-total filter. The roadmap adds a second, orthogonal gate: derivation.
If `S(4,5,17)` is non-existent, then every `S(t,t+1,t+13)` is non-existent by repeated derivation, which would
eliminate `(r,q,n) ∈ {(6,7,19),(7,8,20),(8,9,21),(9,10,22)}` despite divisibility passing; formally
`S(6,7,19) ⇒ S(5,6,18) ⇒ S(4,5,17)`. If `S(5,6,16)` is also non-existent, it eliminates
`(6,7,17),(7,8,18),(8,9,19),(9,10,20)` by the same mechanism. The proof obligation is not computational;
it is bibliographic: verify the base nonexistences once, then propagate by derivation as a fast pre-sieve.

The roadmap’s admissibility enumeration also quantifies *where* the search mass lives: for each `r∈{6,7,8,9}`,
most admissible triples satisfy `q−r∈{1,2,3}`, with `q=r+1` dominating:

| r | admissible `q−r=1` | `q−r=2` | `q−r=3` | `q−r≥4` | total |
|---:|---:|---:|---:|---:|---:|
| 6 | 44 | 13 | 8 | 2 | 67 |
| 7 | 43 | 13 | 8 | 1 | 65 |
| 8 | 43 | 13 | 6 | 1 | 63 |
| 9 | 42 | 10 | 6 | 1 | 59 |

### Claim 2: Strict feasibility invariants transfer better than raw score and should remain the repo backbone.
Evidence: Non-strict runs can show high scalar score while carrying collisions; e.g. `S(9,10,20)` reached `score=55.44`
with `overcovered=20643`. In contrast, strict runs that preserve `overcovered=0` and zero `(r-1)` oversubscription
show reliable, monotone improvements that can be reused: `S(9,10,22)` improved strict blocks `23752 -> 24165` while
maintaining `overcovered=0`, `oversubscribed_(r-1)=0`, and moving uncovered `259900 -> 255770`, i.e.
uncovered fraction `255770/497420 ≈ 0.5142`.

### Claim 3: Symmetry/Kramer–Mesner must be bounded and diagnostics-driven; orbit compression can be decisive when it exists.
Evidence: Practice records show symmetry can be highly instance-dependent. On `S(6,8,29)`, Stage-A cyclic symmetry was
empirically tractable (`non-binary share ≈ 0.83%`, `max_coeff=2`, `117` accepted cyclic orbits) and produced a reusable
strict seed; on other instances, non-binary inflation and sparse orbit gains forced early fallback. The roadmap’s KM framing
(`Ax=1` on orbit-incidence for prescribed group `G`) supports a bounded policy: compute orbit counts (`|O_r|,|O_q|`) and
coefficient profile (non-binary mass, max coefficient) first, then commit to orbit-level SAT/ILP/DLX only if diagnostics pass.
The roadmap also suggests a pragmatic *group menu* for bounded attempts (moderate reductions, not maximal symmetry): cyclic
and dihedral actions (difference-method inspired), small transitive groups from GAP’s library, affine groups when `n` supports
them, and subgroup chains `G0 ≥ G1 ≥ …` to relax symmetry if no solution appears.

### Claim 4: Residual exact-cover is a late closure lane with explicit eligibility gates; “early residual” is a retired policy.
Evidence: The best strict `S(9,10,22)` checkpoints still have uncovered fraction `≈0.51`, far above any plausible residual
exact-cover budget; practice explicitly retires “residual exact cover may help at ~50% uncovered.” Empirically, strict repair
and motif-coupled repacks continue to yield monotone gains at such residual mass, while residual exact-cover attempts are
structurally premature.

### Claim 5: Roadmap-style parameter ranking should override “smallest admissible `n`” when derivation-veto applies.
Evidence: The roadmap’s two base nonexistences eliminate the smallest admissible instances on the `q=r+1` line for
`r∈{6,7,8,9}`: `S(6,7,17)`, `S(6,7,19)`, `S(7,8,18)`, `S(7,8,20)`, `S(8,9,19)`, `S(8,9,21)`, `S(9,10,20)`, `S(9,10,22)`.
Thus the smallest *not-yet-eliminated* starting points shift to `n=23,24,25,26`. This is a measurable compute-policy change:
if veto is correct, any solver budget spent on the eliminated set has zero chance of a full certificate.

## Lemma Chain (proof-first obligations)
1. **Lemma A (Divisibility gate)**. Verify all `q−i choose r−i | n−i choose r−i` constraints (`i=0..r-1`) and compute `λ_i`.
2. **Lemma A2 (Classical lower bounds)**. Apply Ray–Chaudhuri–Wilson and Tits/Cameron bounds as additional necessary gates,
   especially when `q−r` grows (these rarely eliminate `q=r+1` cases, but can prune larger gaps).
3. **Lemma B (Derivation-veto gate)**. If a derived instance `S(r-k,q-k,n-k)` is known non-existent for some `k≥1`, then the
   original instance is non-existent. Record the witness chain explicitly (the “derivation certificate”).
4. **Lemma C (Engine selector)**. Use bounded diagnostics (orbit compression, non-binary mass, pressure tails) to select
   between orbit-compressed exact-cover (KM) and randomized/repair engines.
5. **Lemma D (Strict monotone repair)**. Under hard caps (`c_r≤1`, `c_{r-1}≤λ_{r-1}`), accepted local operations preserve feasibility.
6. **Lemma E (Absorption-inspired closure discipline)**. Reserve flexibility early; use destroy/repack neighborhoods to reopen slack.
7. **Lemma F (Residual eligibility)**. Attempt residual exact-cover only when uncovered mass is below explicit thresholds.
8. **Operational theorem**. The staged protocol returns one of: arithmetic impossibility witness, derivation-veto nonexistence witness,
   strict-feasible improved partial, or full certificate.

## Proof Strategy (operational, research-only)
1. Run Lemma A (divisibility), Lemma A2 (bounds), and Lemma B (derivation-veto) before any solver runs; abort immediately on a verified nonexistence chain.
2. If not vetoed, run Lemma C symmetry diagnostics; use KM orbit reduction only when compression is strong and coefficients remain low.
3. Construct a strict-feasible partial via symmetry seed or randomized nibble/greedy.
4. Apply strict repair with pressure-triggered destroy/repack; preserve invariants throughout.
5. Attempt residual exact-cover only when Lemma F gate is satisfied.

## Failure Certificates
- F0 **Derivation-veto witness**: an explicit chain `S(r,q,n) -> … -> S(r',q',n')` where `S(r',q',n')` is verified non-existent.
- F1 **Arithmetic failure**: the first tuple `(i, numerator, denominator, remainder)` with `remainder ≠ 0`.
- F2 **Engine mismatch**: bounded symmetry diagnostics show weak compression or heavy non-binary mass.
- F3 **Strict infeasibility**: first violated hard invariant (`overcovered>0` or `(r-1)` oversubscription).
- F4 **Plateau witness**: uncovered-reduction slope and accepted-move rate fall below windowed thresholds.
- F5 **Residual ineligibility**: uncovered mass exceeds residual builder/solver thresholds.
- F6 **Exact-cover UNSAT**: SAT/ILP/DLX transcript (when feasible) establishing infeasibility under explored symmetry/constraints.
- F7 **Bibliographic gap**: a derivation-veto claim is used without an accessible primary reference; treat veto as provisional until closed.

## Source-to-Method Transfer (mandatory, all local PDFs)
The table maps each local PDF to one concrete mechanism and a code-level delta with a validation metric.

| Source PDF | Theorem/Mechanism (explicit) | Code Delta Mapping (file:path + action) | Validation Metric |
|---|---|---|---|
| `Computational and Theoretical Roadmap for Steiner Systems with Strength 6–9 and n _ 200.pdf` | Workflow mechanism: derivation-based nonexistence propagation along `q=r+1` using verified base certificates (`S(4,5,17)` and `S(5,6,16)`). | `math_proofs/steiner_portfolio.py`: add `derivation_veto()` with witness chain; `math_proofs/steiner_system.py`: expose `nonexistence_witness` in admissibility output | `vetoed_admissible_count`; `wasted_rounds_avoided`; any vetoed instance later solved ⇒ reject |
| `Computational and Theoretical Roadmap for Steiner Systems with Strength 6–9 and n _ 200.pdf` | Workflow mechanism: Kramer–Mesner orbit reduction (`Ax=1`) + group-menu search + engine routing after orbit diagnostics. | add `math_proofs/steiner_kramer_mesner.py` (new) for orbit enumeration + KM matrix; update `math_proofs/steiner_exact_cover.py` to accept orbit variables; update `run_steiner_loop.sh` to run bounded KM diagnostics first | Orbit compression ratio `|O_q|/C(n,q)`; non-binary coefficient share; solver runtime/nodes |
| `arxiv_1401.3665.pdf` | Theorem mechanism: randomized-algebraic template → nibble/greedy cover → “spill” repair → absorber/cascade closure. | `math_proofs/steiner_exact_cover.py`: add hooks `template_seed()` + `spill_fix()`; `math_proofs/steiner_round_logger.py`: log `spill_size` and `spill_fixed_rate` | `spill_size`; uncovered slope after spill-fix; local-fix success rate |
| `arxiv_1611.06827.pdf` | Workflow mechanism: iterative absorption with vortex levels, boosted nibble, Cover-down lemma, transformers/absorbers for bounded leftovers. | `run_steiner_loop.sh`: add vortex scheduler + per-level checkpoints; `math_proofs/steiner_residual_repair.py`: add “cover-down” micro-solver stub + absorber reserve policy | Leftover mass per level; cover-down hit rate; strict violations (must be 0) |
| `oai_first_proof.pdf` | Protocol mechanism: 5 seed ideas → independent solve attempts → ≤3 verify/revise loops → typeset-ready closure. | `run_steiner_loop.sh`: enforce 5-seed round1 + ≤3 verify loops; `math_proofs/steiner_round_logger.py`: add verification checklist fields | #seeds explored; % verification passes; reduced repeated round1 essays |

## Engine Selector Rubric (concise)
- Prefer symmetry/orbit compression when `|O_q|` and `|O_r|` are tiny relative to `\binom{n}{q}`, `\binom{n}{r}`, and KM coefficients
  remain mostly binary/low-weight under the chosen group.
- Prefer randomized bulk + strict repair when compression is weak, KM non-binary mass is high, or strict add-only quickly saturates
  `(r-1)` pressure tails.

## Blocker-Driven Research Deltas (practice-driven)
- Blocker: **divisibility-only portfolio selection** chases derivation-veto eliminated triples.
  - Source likely to address it: roadmap (derivation veto + small nonexistence results).
  - Concrete implementation change: add `derivation_veto()` + witness chain in `math_proofs/steiner_portfolio.py`, and refuse to schedule solve rounds for vetoed instances.

- Blocker: **add-only saturation** at high `(r-1)` pressure tails.
  - Source likely to address it: iterative absorption (vortex / cover-down / absorbers).
  - Concrete implementation change: pressure-triggered switch from add-only to destroy/repack neighborhoods; maintain an explicit “reserve” budget for absorber-style closure.

- Blocker: **binary-orbit symmetry stalls** under non-binary coefficients.
  - Source likely to address it: roadmap KM workflow + group-menu iteration.
  - Concrete implementation change: after bounded binary KM fails, fall back to weighted-orbit ILP neighborhoods (rather than extending binary-only search).

- Blocker: **early residual exact-cover** wastes runtime at large uncovered mass.
  - Source likely to address it: Keevash staging discipline + repo practice.
  - Concrete implementation change: enforce a residual eligibility gate (uncovered fraction + absolute uncovered) before building any residual exact-cover instance.

- Blocker: **duplicate motif neighborhoods** waste local-search budget.
  - Source: repo strict-LNS practice evidence.
  - Implementation delta: motif signature cache + taboo window for recent failures.

## Next Theorem-Sized Hypothesis
**Hypothesis T (nonexistence-aware hybrid dominance)**.
In the repo’s `r=6..9, n<200` regime, augmenting the front gate from “divisibility-only” to
“divisibility + verified derivation-veto nonexistence propagation” increases useful solve yield per compute by
eliminating impossible triples (especially on `q=r+1`), and on the remaining unknown set the canonical hybrid
selector (bounded symmetry triage + pressure-triggered strict repair + late residual gating) dominates any single-engine policy
under matched budgets while preserving strict feasibility invariants.

## Retired Hypotheses
- “Divisibility-only frontier ranking is sufficient” (retire: roadmap-derived nonexistence propagation can veto divisibility-admissible picks).
- Long binary-only symmetry exploration as a default policy at larger `r`.
- Add-only continuation after strict frontier saturation.
- Residual exact-cover invocation without residual-size eligibility gating.

## Active Hypotheses (max 4)
1. A verified derivation-veto nonexistence gate eliminates a meaningful fraction of divisibility-admissible small instances and should be applied before any solve rounds.
2. The canonical hybrid engine selector (bounded symmetry triage plus pressure-triggered strict repair handoff) is dominant on the remaining unknown admissible set.
3. Kramer–Mesner orbit reduction is worth a bounded upfront budget only when orbit compression and coefficient structure meet explicit diagnostics.
4. Motif-coupled repacks (`k -> k+1`) outperform uncoupled local windows once `(r-1)` pressure tails harden.

## Falsification Criteria
- Reject Active 1 if any vetoed instance later obtains a valid certificate in this repo, or if implementing the veto fails to reduce wasted solve rounds in a matched-budget ablation.
- Reject Active 2 if three matched seeds on a non-vetoed instance fail to beat add-only baseline on uncovered-reduction slope while keeping strict feasibility.
- Reject Active 3 if bounded KM (with diagnostics satisfied) fails to improve solve feasibility/coverage-per-time over non-symmetry baselines across three matched instances.
- Reject Active 4 if after `≥400` accepted repack neighborhoods net gain is `< +20` blocks under strict gates.

## Reuse vs New (this update)
- Reused: strict feasibility backbone; bounded engine selection; residual eligibility discipline; practice-derived falsification windows.
- New: imported the roadmap’s admissibility breakdown by `q−r` (quantifying the `q=r+1` dominance) and added the roadmap’s group-menu guidance as an explicit symmetry-policy input; updated focus run to `S(6,7,19)` and aligned all claims with cross-run practice metrics.

## References (minimal, local-first)
- Local PDFs under `/root/openquestions/papers`: roadmap; `arxiv_1401.3665.pdf` (Keevash); `arxiv_1611.06827.pdf` (iterative absorption); `oai_first_proof.pdf` (workflow).
