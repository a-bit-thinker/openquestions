# Steiner Knowledge Cache

Run ID: 20260222_135457
Created (UTC): 2026-02-22T13:54:57Z

## Instance Snapshot (current focus)
- Instance: `S(6,7,19)` (divisibility-admissible)
- Required blocks: `b = C(19,6)/C(7,6) = 27132/7 = 3876`
- Replications: `λ_5 = 7` (each 5-subset must appear in exactly 7 blocks)
- Exact-cover sizing: rows `C(19,6)=27132`, cols `C(19,7)=50388`, row-degree `C(13,1)=13`
- Status: **provisionally vetoed** by roadmap-derived derivation chain; requires bibliographic closure.

## Hard Gates (never skip)
1. **Admissibility / divisibility**: check `C(q-i,r-i) | C(n-i,r-i)` for all `i=0..r-1`; compute `b` and `λ_i`.
2. **Derivation-veto propagation**: if any derived `S(r-k,q-k,n-k)` hits a verified nonexistence, reject immediately and store the witness chain.
3. **Classical bounds (failsafe)**: Ray–Chaudhuri–Wilson; Tits and Cameron bounds (rarely decisive for `q=r+1`, but useful beyond).
4. **Strict feasibility invariants (solver)**: preserve `overcovered=0` and zero `(r-1)` oversubscription as the default transferable regime.

## Roadmap-Derived Nonexistence (high-signal)
- Roadmap asserts: `S(4,5,17)` is proved non-existent (Östergård–Pottonen) ⇒ eliminates all `S(t,t+1,t+13)` for `t≥4`.
  - Consequence in our window: eliminates `(6,7,19),(7,8,20),(8,9,21),(9,10,22)` via derivation.
- Roadmap asserts: `S(5,6,16)` is recorded non-existent (van der Pol table) ⇒ eliminates all `S(t,t+1,t+11)` for `t≥5`.
  - Consequence: eliminates `(6,7,17),(7,8,18),(8,9,19),(9,10,20)`.
- Action: treat these as **provisional** until the base certificates are locally available; once verified, they become a front-gate certificate lane.

## Strong Search Stack (canonical)
### Mode A: Symmetry / Kramer–Mesner (bounded triage)
- Mechanism: prescribe `G ≤ S_n`, compute orbits on `r`- and `q`-subsets, build orbit-incidence matrix `A`, solve `Ax=1`.
- Group menu (roadmap): cyclic/dihedral; small transitive groups (GAP); affine groups; subgroup chains `G0 ≥ G1 ≥ …` to relax.
- Keep only if diagnostics pass: strong orbit compression + low non-binary coefficient mass + small `max_coeff`.

### Mode B: Randomized construction + strict repair (default when symmetry weak)
- Keevash transfer: **template → nibble/greedy → spill → spill-fix → absorber/cascade closure**.
- Iterative absorption transfer: **vortex levels → cover-down cleaning → exclusive absorbers via transformers**.
- Repo practice transfer: strict add-only eventually saturates `(r-1)` pressure tails; switch to destroy/repack neighborhoods that free saturated motifs.

### Mode C: Residual exact-cover (late-only)
- Trigger only when uncovered mass is below explicit thresholds (absolute + fraction); otherwise it is structurally premature.

## Engine Selector Rubric (one-liner)
- Symmetry-first when `(|O_q|,|O_r|)` are tiny and coefficient profile is mostly binary/low-weight.
- Randomized+repair-first when orbit compression is weak, coefficients inflate (non-binary mass), or strict add-only quickly saturates `(r-1)` pressure tails.

## Practice Evidence (what actually moved metrics)
- Strict invariants transfer better than non-strict score: strict runs maintained `overcovered=0` and `(r-1)` oversubscription `0` while still improving coverage.
- Mixed-window strict LNS beats `1->2`-only in gain-per-time (stop if not ≥10% better per 1000 neighborhoods).
- Early residual exact-cover at ~50% uncovered is retired (no meaningful movement; violates eligibility intuition).

## Metrics to Log Every Checkpoint (minimum set)
- Coverage: `exact_once`, `uncovered`, `overcovered`
- `(r-1)` pressure: max load / cap (`λ_{r-1}`), cap-hit count, oversubscribed count
- Point degree: min/max/gap, and high-quantile tail
- Efficiency: accepted move rate; uncovered reduction per 1000 trials; micro-augment hit rate

## Source Notes (local-first)
- `papers/Computational and Theoretical Roadmap for Steiner Systems with Strength 6–9 and n _ 200.pdf`
  - Takeaway: derivation-veto is a first-class nonexistence propagation gate; KM orbit method + group menu is the right symmetry workflow for `n<200`.
  - Strategy change: stop spending solve rounds on divisibility-admissible but derivation-veto-eliminated `q=r+1` low-`n` instances once bases are verified.
- `papers/arxiv_1401.3665.pdf` (Keevash)
  - Takeaway: template/spill framing + local exchange/cascade ideas suggest logging “spill size” and running targeted spill-fix rather than global exact cover early.
  - Strategy change: add template-seeded starts + spill instrumentation; treat spill-fix as a distinct repair lane.
- `papers/arxiv_1611.06827.pdf` (Glock–Kühn–Lo–Osthus)
  - Takeaway: vortex + cover-down + exclusive absorbers is the clean staged completion discipline; “boosting” is an explicit phase.
  - Strategy change: implement levelled checkpoints (vortex-like) and a cover-down micro-solver primitive for strict repair.
- `papers/oai_first_proof.pdf`
  - Takeaway: round1 should be 5 seeds + ≤3 verify loops + typeset-ready outline; prevents single-track lock-in.
  - Strategy change: enforce verification gates and “reuse vs new” discipline to stop repeated round1 essays.

## Round 2 Incremental Additions (2026-02-22)
- Symmetry diagnostics measured on `S(6,7,19)`:
  - Cyclic `C19`: `|O_6|=1428`, `|O_7|=2652`, `nonbinary_share=0.000485`, `max_coeff=2`.
  - Dihedral `D19`: `|O_6|=756`, `|O_7|=1368`, `nonbinary_share=0.054054`, `max_coeff=2`.
- Practical selector outcome:
  - Symmetry lane is tractable and useful for proposal structure, but strict add-only movement from the current seed was `+0`.
  - Strict LNS `k=2..4 -> k+1` repacks are the active mover from this frontier.
- New strict frontier (this run round2):
  - Candidate improved `2438 -> 2508` blocks with `overcovered=0` and `oversubscribed_(r-1)=0` preserved.
  - Verifier movement: `score 48.06 -> 50.59`, `exact_once 17066 -> 17556`, `uncovered 10066 -> 9576`.
- Pressure behavior note:
  - `(r-1)` max remained `7/7` throughout, but cap-hit count dropped from `137` to `67`, and this correlated with additional LNS gains.
- Residual gate reminder:
  - Despite `overcovered=0`, residual exact completion remains ineligible at this frontier (`uncovered fraction 0.353 > 0.10`).
