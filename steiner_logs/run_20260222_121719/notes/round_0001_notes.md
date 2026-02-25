# Round 1 Notes (Research-Only)

Instance: `S(6,7,19)`
Expected blocks: `3876`
Date (UTC): `2026-02-22`

## Cross-run bootstrap (mandatory first read, completed)
- Repo-wide history: steiner_logs/run_20260222_121719/REPO_WIDE_HISTORY.md
- Global research log (all runs round1): steiner_logs/RESEARCH_LOG.md
- Global practice log (all runs round2-5): steiner_logs/PRACTICE_LOG.md
- Global research paper (paper-style synthesis): steiner_logs/RESEARCH_PAPER.md
- Existence frontier report (all admissible triples): steiner_logs/EXISTENCE_FRONTIER.md
- Local paper notes: steiner_logs/PAPER_NOTES.md
- Primary local roadmap PDF: /root/openquestions/papers/Computational and Theoretical Roadmap for Steiner Systems with Strength 6–9 and n _ 200.pdf
- Latest prior run: run_20260222_052536
- Latest prior round1 notes source run: run_20260222_052536
- Latest prior round1 notes: steiner_logs/run_20260222_052536/notes/round_0001_notes.md
- Latest prior round5 notes source run: run_20260222_052536
- Latest prior round5 notes: steiner_logs/run_20260222_052536/notes/round_0005_notes.md
- Latest prior transfer: steiner_logs/run_20260222_052536/NEXT_GENERATION_TRANSFER.md

## Local-paper-first check
- Read the roadmap first (via extracted text): `papers/_extracted_text/Computational and Theoretical Roadmap for Steiner Systems with Strength 6–9 and n _ 200.txt`.
- Read local extracted texts for Keevash/iterative-absorption/workflow: `papers/_extracted_text/arxiv_1401.3665.txt`, `papers/_extracted_text/arxiv_1611.06827.txt`, `papers/_extracted_text/oai_first_proof.txt`.
- External web search: not used (`0` new links).

## Admissibility gate snapshot
```json
{
  "checks": [
    {
      "denominator": 7,
      "i": 0,
      "numerator": 27132,
      "quotient": 3876,
      "remainder": 0
    },
    {
      "denominator": 6,
      "i": 1,
      "numerator": 8568,
      "quotient": 1428,
      "remainder": 0
    },
    {
      "denominator": 5,
      "i": 2,
      "numerator": 2380,
      "quotient": 476,
      "remainder": 0
    },
    {
      "denominator": 4,
      "i": 3,
      "numerator": 560,
      "quotient": 140,
      "remainder": 0
    },
    {
      "denominator": 3,
      "i": 4,
      "numerator": 105,
      "quotient": 35,
      "remainder": 0
    },
    {
      "denominator": 2,
      "i": 5,
      "numerator": 14,
      "quotient": 7,
      "remainder": 0
    }
  ],
  "divisibility_failures": [],
  "expected_block_count": 3876,
  "instance": {
    "n": 19,
    "q": 7,
    "r": 6
  },
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 3876,
    "lambda_1": 1428,
    "lambda_2": 476,
    "lambda_3": 140,
    "lambda_4": 35,
    "lambda_5": 7
  }
}
```

## Roadmap-derived nonexistence triage (provisional until verified)
From the local roadmap:
- Claimed base nonexistences:
  - Östergård–Pottonen: `S(4,5,17)` does not exist, implying nonexistence for all `S(t,t+1,t+13)` with `t ≥ 4`.
  - van der Pol table: `S(5,6,16)` does not exist, which by derivation eliminates the `n=r+11` line in our regime.

Immediate conditional consequence:
- Derivation chain: `S(6,7,19) -> S(5,6,18) -> S(4,5,17)`.
- Therefore: if the `S(4,5,17)` nonexistence is verified from a primary source, then `S(6,7,19)` is non-existent.

Verification obligation (before spending solve rounds on this instance):
- Close the bibliographic gap by locating a primary PDF/source for the `S(4,5,17)` nonexistence (and the `S(5,6,16)` table if used), then treat the derivation-veto as a hard gate.

## Strong search stack (mandatory)
### Gate 0: forced parameters + size diagnostics
- Blocks: `b = 3876`.
- Replications: `λ_5 = 7` (hard `(r-1)` cap for strict partials), `λ_1 = 1428`.
- Exact-cover sizing: rows `C(19,6)=27132`, cols `C(19,7)=50388`, row degree `C(13,1)=13`, incidences `352716`.

### Gate 1: divisibility/admissibility
- Status: pass (all remainders `0` in the snapshot above).

### Gate 2: derivation-veto propagation
- If `S(4,5,17)` nonexistence is verified, veto `S(6,7,19)` immediately and pivot the solve portfolio.
- Until verified, treat the veto as provisional and prioritize closing the bibliographic gap.

### Gate 3: classical lower bounds (roadmap)
- Apply Fisher–Ray–Chaudhuri–Wilson / Tits/Cameron style necessary bounds as additional pruning when `q-r > 1` (usually not decisive on `q=r+1`).

### Engine A: symmetry / Kramer–Mesner (KM) exact-cover mode
- Mechanism: prescribe a group `G ≤ S_n`, compute orbits `O_r` on `r`-subsets and `O_q` on `q`-subsets, form orbit-incidence matrix `A`, solve `Ax=1` in `{0,1}^{|O_q|}`.
- Diagnostics (bounded budget):
  - orbit compression ratio (`|O_q|` vs `C(n,q)`),
  - coefficient profile (non-binary share, max coefficient),
  - early solver feasibility for `Ax=1`.
- Roadmap group menu (first tries): cyclic `C_n`, dihedral `D_{2n}`, small transitive groups (GAP library), affine groups when `n` has suitable arithmetic form, subgroup chains for symmetry relaxation.
- Switch rule: if `|O_q|` is large or non-binary mass is material, stop and fall back to Engine B.

### Engine B: nibble → boosting/repair → absorber → residual exact-cover mode
- B1 Bulk: random greedy / nibble to cover most `r`-subsets quickly.
- B2 Repair: strict add-only while `(r-1)` pressure tails permit; then pressure-triggered destroy/repack neighborhoods when add acceptance plateaus.
- B3 Absorber-inspired discipline: maintain reserve/flex so late-stage “cover-down” style micro-solves are possible.
- B4 Residual exact-cover: only after an explicit eligibility gate (uncovered mass small). Practice logs retire “early residual” at uncovered fractions around `~0.5`.

## External references used (minimal)
- New links introduced in this round: `0`.
- Reused sources: local PDFs only (no link churn).
- New round1 PDFs saved under `/root/openquestions/papers`: `none`.

## Proof-first round1 stack (mandatory)
### Seed 1: derivation-veto nonexistence (conditional proof lane)
- High-level proof idea: use derivation closure: `S(r,q,n) ⇒ S(r-1,q-1,n-1)`; a verified nonexistence at the end of the chain refutes the start.
- Solve-attempt (this round): write a typeset-ready conditional nonexistence proof `S(4,5,17) ≁ exists ⇒ S(6,7,19) ≁ exists`.
- Critical gap: the base nonexistence must be verified from a primary source (roadmap alone is not a final certificate).

### Seed 2: computational nonexistence via derived-design classification (roadmap-inspired)
- High-level proof idea: mimic the `S(4,5,17)` nonexistence workflow described in the roadmap (derived designs + exact cover), but on the derived instance `S(5,6,18)`.
- Solve-attempt (this round): specify a branch-and-reduce plan: fix a point, enumerate non-isomorphic derived partials, and attempt extension via DLX/SAT with symmetry pruning.
- Critical gap: requires strong isomorphism rejection and large compute; not yet instantiated in repo artifacts.

### Seed 3: bounded KM symmetry triage (existence or structured UNSAT evidence)
- High-level proof idea: if orbit compression is strong, KM reduces variables to orbit level and can decide feasibility for a prescribed symmetry.
- Solve-attempt (this round): commit to a bounded “group menu” probe, and record orbit counts + coefficient profile as an engine-choice witness.
- Critical gap: UNSAT under a group does not imply global nonexistence; this is a triage lane, not a proof by itself.

### Seed 4: direct exact-cover decision attempt (DLX / libexact framing)
- High-level proof idea: `S(6,7,19)` has moderate size (rows `27132`, degree `13`); a carefully split DLX search could be feasible if the instance is not vetoed.
- Solve-attempt (this round): define how to split: canonical seed fixing (lex-first block choices), distributed branching, and strict logging of explored subspaces.
- Critical gap: requires heavy compute and careful logging to become a real nonexistence certificate.

### Seed 5: randomized near-design + strict repair (Keevash/absorption-inspired, proof as “mechanism”)
- High-level proof idea: build a near-solution quickly (nibble), then repair collisions and absorb leftover constraints, treating strict invariants as proof obligations.
- Solve-attempt (this round): define stage gates and eligibility thresholds (pressure tails, uncovered slope, residual size) rather than assuming closure.
- Critical gap: asymptotic proofs do not supply finite constants for `n=19`; this lane is operational, not a theorem instance.

## Critical-gap verification loop (up to 3 rounds)
1. Verification round A (arithmetic consistency)
- Check: divisibility table, replication numbers, expected `b`.
- Status: pass (`6/6` remainders are `0`).
- Stop rule: any nonzero remainder is an arithmetic impossibility certificate.

2. Verification round B (bibliographic closure of derivation veto)
- Check: obtain primary reference(s) for `S(4,5,17)` nonexistence (and `S(5,6,16)` if used).
- Status: open (roadmap provides the claim; we still need primary-source verification).
- Stop/switch rule: if primary sources cannot be located quickly, treat veto as “provisional” and pivot solve rounds to not-eliminated instances anyway.

3. Verification round C (engine compatibility + eligibility gates)
- Check: bounded KM diagnostics first; otherwise randomized bulk + strict repair. Residual exact-cover only when residual is small.
- Status: set as contract for rounds 2+ (no solver spend in this research-only round).

## Typeset-ready final proof outline (conditional nonexistence)
1. Proposition (admissibility): `S(6,7,19)` satisfies all divisibility constraints; `b=3876`, `λ_5=7`.
2. Lemma (derivation): if `S(6,7,19)` exists then `S(5,6,18)` exists.
3. Lemma (derivation again): if `S(5,6,18)` exists then `S(4,5,17)` exists.
4. Theorem (conditional veto): if `S(4,5,17)` does not exist, then `S(6,7,19)` does not exist.
5. Corollary (portfolio pivot): once the base nonexistence is verified, remove `S(6,7,19)` and the entire `n=r+13` line from the solve queue.

## Engine selector rubric (concise, mandatory)
- Use symmetry/orbit compression when `|O_q|` and `|O_r|` are tiny (strong orbit compression) and KM coefficients stay mostly binary/low-weight.
- Use general randomized construction when compression is weak, non-binary mass is high, or early strict add-only behavior shows `(r-1)` pressure saturation.

## Paper-to-loop method extraction (mandatory, all local PDFs)
| Source PDF | Theorem/Mechanism (explicit) | Code Delta Mapping (file:path + action) | Validation Metric |
|---|---|---|---|
| `Computational and Theoretical Roadmap for Steiner Systems with Strength 6–9 and n _ 200.pdf` | Derivation-veto propagation from verified base nonexistences on `q=r+1`. | `math_proofs/steiner_portfolio.py`: add `derivation_veto()` + witness chain; `math_proofs/steiner_system.py`: surface `nonexistence_witness` in admissibility output | `vetoed_admissible_count`; wasted solve rounds avoided |
| `Computational and Theoretical Roadmap for Steiner Systems with Strength 6–9 and n _ 200.pdf` | Kramer–Mesner orbit reduction `Ax=1` + group-menu triage before raw exact cover. | add `math_proofs/steiner_kramer_mesner.py`; `run_steiner_loop.sh`: bounded KM diagnostics; `math_proofs/steiner_exact_cover.py`: orbit-variable routing | Orbit compression ratio; non-binary coefficient share; runtime/nodes |
| `arxiv_1401.3665.pdf` | Randomized-algebraic template → spill repair → absorber/cascade closure. | `math_proofs/steiner_exact_cover.py`: add `template_seed()` + `spill_fix()` hooks; `math_proofs/steiner_round_logger.py`: log spill metrics | `spill_size`; spill-fixed rate; uncovered slope post-fix |
| `arxiv_1611.06827.pdf` | Iterative absorption: vortex levels, boosted nibble, cover-down lemma, transformers/absorbers for bounded leftovers. | `run_steiner_loop.sh`: vortex scheduler; `math_proofs/steiner_residual_repair.py`: cover-down micro-solver stub + reserve policy | Leftover mass per level; cover-down hit rate; strict violations (must be 0) |
| `oai_first_proof.pdf` | Workflow: 5 seed ideas → independent solves → ≤3 verify/revise loops → typeset-ready artifact. | `run_steiner_loop.sh`: enforce 5-seed round1 + ≤3 verify loops; `math_proofs/steiner_round_logger.py`: verification checklist fields | #seeds; % verification passes; reduced repeated round1 essays |

## Practice-log failures -> research deltas (mandatory)
1. Blocker: add-only strict growth plateaus once `(r-1)` faces saturate.
- Source likely to address it: `arxiv_1611.06827.pdf` (iterative absorption: cover-down / absorber framing).
- Concrete implementation change: trigger destroy/repack once add-acceptance drops below a calibrated threshold in a fixed trial window; preserve a reserve budget for closure.

2. Blocker: binary-only symmetry probes stall under non-binary orbit coefficients.
- Source likely to address it: roadmap KM workflow + group menu.
- Concrete implementation change: add weighted-orbit ILP neighborhoods after bounded binary KM failure, rather than extending binary search budget.

3. Blocker: residual exact-cover invoked too early wastes runtime with no frontier movement.
- Source likely to address it: `arxiv_1401.3665.pdf` staging discipline + PRACTICE_LOG retirement evidence.
- Concrete implementation change: enforce uncovered-fraction/absolute uncovered eligibility gates before launching residual exact solver.

4. Blocker: repeated motif neighborhoods produce duplicate low-yield local attempts.
- Source likely to address it: cross-run evidence in `steiner_logs/PRACTICE_LOG.md`.
- Concrete implementation change: canonical motif signatures with a short taboo cache for recent failed neighborhoods.

## Reuse vs genuinely new (explicit; avoid duplicate round1 essays)
- Reused from prior runs:
  - hard divisibility gate before all expensive work,
  - strict feasibility invariants as the transferable backbone,
  - bounded symmetry triage + early fallback discipline,
  - residual exact-cover as a late gated lane only.
- Genuinely new in this round:
  - instance-specialized proof-first stack for `S(6,7,19)` with an explicit conditional derivation-veto nonexistence proof outline,
  - roadmap “group menu” + KM diagnostics integrated into the strong search stack,
  - a concrete bibliographic closure checkpoint (treat veto as provisional until primary sources are in hand).

## Rounds 2+ execution summary and metric contract (mandatory)
### Execution order
1. Round 2: close the bibliographic derivation-veto gate; if verified, remove `S(6,7,19)` from the solve queue and pivot to `S(6,7,23)`.
2. Round 3: run bounded KM diagnostics + short KM feasibility probe on `S(6,7,23)`; choose KM vs randomized engine by diagnostics.
3. Round 4: run the same staged protocol on `S(7,8,24)` as a transfer check.
4. Round 5: escalate to `S(8,9,25)` / `S(9,10,26)` only after KM diagnostics justify, otherwise keep randomized+repair.

### Metrics to track every checkpoint
- Point degree: `min`, `max`, `gap`, and high-quantile tail.
- `(r-1)`-pressure: max load, cap-hit count, oversubscribed count.
- Coverage quality: `exact_once`, `uncovered`, `overcovered`.
- Efficiency: accepted move rate, uncovered reduction per 1000 trials, micro-augment hit rate.

## Work log
- Completed all mandatory cross-run reads before any external lookup.
- Extracted and transferred roadmap mechanisms (derivation-veto; KM orbit reduction; group menu) into the research paper + this round’s method tables.
- Wrote the proof-first stack, strong search stack, engine selector rubric, and practice-driven research deltas for `S(6,7,19)`.

## Observations
- The highest-ROI next step is closing the derivation-veto bibliography; it can zero out entire families of “admissible” instances.
- If veto is verified, solver effort should pivot immediately to `S(6,7,23)` and the larger frontier set, not to deeper search on `S(6,7,19)`.

## Core advance
- advance statement:
  - Converted round1 for `S(6,7,19)` into a proof-first, gate-explicit research contract centered on derivation-veto triage plus a bounded KM-orbit / randomized repair dichotomy.
- evidence from this round (metrics, runtime, structure):
  - Mandatory cross-run reads and local-paper-first discipline completed.
  - Admissibility verified (`6/6` remainder checks `0`); roadmap-derived veto chain written and isolated as a bibliographic obligation.
  - Practice log failures were mapped to explicit code deltas with validation metrics.
- transfer value for next rounds:
  - Future rounds can execute without re-deriving the gate stack; the next move is clearly “verify veto or pivot portfolio,” not “try random solver spend.”

## Next-hypothesis
- hypothesis statement:
  - Implementing (and verifying) the roadmap derivation-veto gate will materially increase useful solve yield per compute by removing divisible-but-impossible `q=r+1` instances before any solve rounds.
- mechanism (why this should help):
  - The gate removes entire families by a short derivation chain, converting “unknown” work into a cheap nonexistence certificate lane.
- expected metric movement:
  - fewer solve rounds scheduled on vetoed instances,
  - higher coverage-per-hour on the remaining unknown set due to portfolio pivot.
- falsification / stop condition:
  - Reject if any vetoed instance later receives a valid certificate in this repo, or if the veto gate fails to reduce wasted solve rounds under matched-budget ablations.
