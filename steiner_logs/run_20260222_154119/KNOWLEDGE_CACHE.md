# Steiner Knowledge Cache

Run ID: 20260222_154119
Created (UTC): 2026-02-22T15:41:19Z
Updated (UTC): 2026-02-22T17:24:00Z
Instance focus: `S(6,7,17)`

## Local-paper-first status
- Checked local papers before any web lookup:
- `papers/Computational and Theoretical Roadmap for Steiner Systems with Strength 6–9 and n _ 200.pdf`
- `papers/arxiv_1401.3665.pdf`
- `papers/arxiv_1611.06827.pdf`
- `papers/oai_first_proof.pdf`
- External links added this round: `0`.

## Reused vs New (explicit)
- Reused from prior runs:
- hard divisibility/admissibility gate as non-negotiable front gate,
- bounded symmetry/Kramer-Mesner triage before large randomized spend,
- strict feasibility discipline (`overcovered=0`, zero `(r-1)` oversubscription) as transferable artifact,
- residual exact-cover as late-stage gate only.
- Genuinely new in this run:
- proof-first stack specialized to `S(6,7,17)` with five seeds and per-seed solve-attempt,
- explicit derivation-veto lane added as a co-equal theorem branch,
- blocker-to-source-to-implementation map tied directly to rounds2-5 failures,
- one transfer-ready selector rubric for symmetry vs randomized engines.

## Admissibility anchor
- `S(6,7,17)` passes all divisibility checks (`6/6` remainders `0`).
- Forced block count: `b=1768`.
- Replication anchor: `lambda_5=6`.
- Interpretation: arithmetic gate passes; search burden moves to structural existence/nonexistence and engine fit.

## Proof-first round1 stack (condensed)
1. Arithmetic existence obligations.
- Solve-attempt: fixed `b` and `lambda_i` obligations; no arithmetic obstruction found.
- Gap: arithmetic necessity is not constructive sufficiency.
2. Derivation-veto nonexistence lane.
- Solve-attempt: map `S(6,7,17) -> S(5,6,16)` via derivation closure from local roadmap extraction.
- Gap: base nonexistence citation must be treated as a verified bibliographic obligation before certifying impossibility.
3. Symmetry/Kramer-Mesner compressed lane.
- Solve-attempt: bounded orbit triage with explicit diagnostics (`compression`, `non_binary_share`, `max_coeff`).
- Gap: if non-binary mass is high, binary exact-cover is structurally weak.
4. Nibble plus iterative-absorption lane.
- Solve-attempt: staged lane `nibble -> cover-down repair -> absorber reserve` with strict caps.
- Gap: asymptotic theorems do not give finite `n=17` closure constants.
5. Strict constructive closure lane.
- Solve-attempt: motif-coupled local repacks preserving hard caps to reduce uncovered mass monotonically.
- Gap: known practice plateau at saturated `(r-1)` motifs requires adaptive neighborhood scaling.

## Critical-gap verification loop (up to 3)
1. Loop A: arithmetic + derivation source integrity.
- Pass on arithmetic.
- Pending on base nonexistence source verification.
2. Loop B: engine compatibility.
- Run bounded symmetry diagnostics first.
- Switch immediately if compression weak or non-binary share material.
3. Loop C: closure eligibility.
- Allow residual exact-cover only if strict invariants hold and uncovered fraction is small.

## Strong search stack (execution contract)
1. Hard admissibility/divisibility gate.
2. Symmetry/Kramer-Mesner exact-cover mode (bounded front gate).
3. General randomized mode: `nibble -> boosting/repair -> absorber -> residual exact-cover`.

## Engine-selector rubric (concise)
- Use symmetry/orbit compression when orbit count reduction is large, non-binary coefficients are rare, and a short packed probe gives strict progress.
- Use general randomized construction when orbit compression is weak, non-binary mass is high, or early add-only progress stalls with rising `(r-1)` pressure tails.

## Practice blockers -> research deltas
1. Blocker: add-only strict growth plateaus at saturated `(r-1)` motifs.
- Source: iterative absorption workflow (local file `papers/_extracted_text/arxiv_1611.06827.pdftotext.txt`).
- Concrete change: add pressure-triggered handoff to motif-coupled destroy/repack when add acceptance falls below threshold.
2. Blocker: binary orbit search stalls under non-binary coefficients.
- Source: roadmap KM sections (local file `papers/_extracted_text/Computational and Theoretical Roadmap for Steiner Systems with Strength 6–9 and n _ 200.pdftotext.txt`).
- Concrete change: enable weighted-orbit micro-ILP neighborhoods instead of extending binary-only search budget.
3. Blocker: residual exact-cover invoked too early with large uncovered mass.
- Source: template/spill/absorb staging (local file `papers/_extracted_text/arxiv_1401.3665.pdftotext.txt`).
- Concrete change: hard residual gate requiring strict feasibility plus low uncovered fraction before launch.
4. Blocker: repeated low-yield neighborhood sampling.
- Source: verify/revise discipline from `oai_first_proof` and practice logs.
- Concrete change: canonical motif signatures with short taboo cache and 3-loop revise limit.

## Minimal references
- Reused external links:
- `https://arxiv.org/abs/1401.3665`
- `https://arxiv.org/abs/1611.06827`
- New external links this round: `0`.

## Incremental additions (round_0002, S(6,7,23))
- Symmetry front-gate evidence on this instance:
  - cyclic sampled non-binary share `=1.0`, sampled max coeff `=23`, estimated orbit counts `rows=4389`, `cols=10659`;
  - dihedral sampled non-binary share `=1.0`, sampled max coeff `=92`;
  - bounded cyclic packed probe (`1500` orbit trials) reached only `5267` strict blocks.
- Practical consequence: treat symmetry as a short diagnostic gate for this frontier; switch early to generalized strict repair.
- New strict improvement pattern discovered:
  - direct positive LNS from `9280` stalled,
  - neutral strict rebalancing (`1->1`) reduced pressure (`point gap 413 -> 366`, cap-9 5-faces `83 -> 82`),
  - follow-up positive LNS then produced `+7` strict blocks (`9280 -> 9287`) with `overcovered=0` and zero `(r-1)` oversubscription preserved.
- Updated frontier metrics (`S(6,7,23)`):
  - `score=50.16`, `exact_once=65009/100947`, `uncovered=35938`, `overcovered=0`, `blocks=9287`.

## Incremental additions (round_0003, S(7,8,24))
- Symmetry front-gate evidence at this frontier:
  - bounded cyclic full-orbit packed probe (`320` trials) accepted `0` full orbits at `21080` strict blocks;
  - practical consequence: keep symmetry as a short diagnostic gate here, then switch early to general strict construction.
- New strict frontier movement under required architecture:
  - reserve-first strict general pipeline (`12%` reserve cap) plus uncovered-driven add-only gave `+9` strict blocks (`21080 -> 21089`),
  - LNS `k>1` remove/refill added `+1` (`21089 -> 21090`),
  - hard invariants preserved (`overcovered=0`, `oversubscribed_(r-1)=0`).
- Plateau verification signal:
  - immediate second pass from `21090` produced `0` accepted add-only moves over `1.2M` attempts and `0` net LNS gain over `1400` neighborhoods;
  - practical consequence: this neighborhood family is near local exhaustion once `(r-1)` reaches cap (`9/9`), so next rounds need coupled motif reuse + neutral rebalance or larger exact local windows.
- Updated frontier metrics (`S(7,8,24)`):
  - `score=28.25`, `exact_once=168720/346104`, `uncovered=177384`, `overcovered=0`, `blocks=21090`, `r_minus_1_max=9/9`, `oversubscribed_(r-1)=0`.

## Incremental additions (round_0004, S(8,9,25))
- Symmetry front-gate evidence at this frontier:
  - cyclic sampled non-binary share `=0.0`, sampled max coeff `=1`;
  - bounded cyclic full-orbit strict probe (`320` trials) accepted `255` orbits and reached `6375` strict blocks.
- Practical consequence:
  - unlike the recent `r=8,9` frontiers where symmetry was only a short diagnostic, this instance keeps symmetry as a productive primary engine.
- New strict frontier movement under required architecture:
  - reserve-first (`12%` reserve cap) orbit continuation accepted `1924/199680` full orbits and moved `6375 -> 54475`,
  - uncovered-driven nibble then added `+575` (`54475 -> 55050`),
  - LNS `k>1` remove/refill added `+74` (`55050 -> 55124`),
  - second nibble (`+15`) plus second LNS (`+95`) reached `55234` strict blocks.
- Hard invariants preserved throughout:
  - `overcovered=0`, `oversubscribed_(r-1)=0`, `r_minus_1_max=8/9`.
- Updated frontier metrics (`S(8,9,25)`):
  - `score=24.35`, `exact_once=497106/1081575`, `uncovered=584469`, `overcovered=0`, `blocks=55234`.

## Incremental additions (round_0005, S(9,10,26))
- Symmetry front-gate evidence at this frontier:
  - cyclic sampled non-binary share `=0.0`, sampled max coeff `=1`, sampled orbit size `26`;
  - dihedral sampled non-binary share `=0.00293`, sampled max coeff `=2`, sampled orbit size `52`;
  - bounded cyclic full-orbit strict probe/continuation (`2200` trials) accepted `1246` full orbits and reached `32383` strict blocks.
- Practical consequence:
  - keep cyclic symmetry as a productive Stage A engine on `S(9,10,26)` rather than only a short diagnostic.
- New strict frontier movement under required architecture:
  - reserve-first (`12%` reserve) nibble/boosting moved `32383 -> 119973` (`+87590`),
  - `k>1` LNS remove/refill added `+692` (`119973 -> 120665`),
  - post-LNS revision add-only added `+3060` to reach `123725` strict blocks.
- Hard invariants preserved throughout:
  - `overcovered=0`, `oversubscribed_(r-1)=0`, `r_minus_1_max<=9`.
- Updated frontier metrics (`S(9,10,26)`):
  - `score=15.44`, `exact_once=1237250/3124550`, `uncovered=1887300`, `overcovered=0`, `blocks=123725`.
