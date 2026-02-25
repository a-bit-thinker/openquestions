# Global Research Log (Round1 Knowledge)

Generated (UTC): 2026-02-22T16:50:46.240550+00:00
Log root: steiner_logs
Current run dir: /root/openquestions/steiner_logs/run_20260222_154119

## Intent
- Aggregate all run round1 knowledge to avoid repeated essay loops.
- Keep reasoning/proof structure primary; keep links as supporting evidence only.

## Raw Redundancy
- Per-run round logs remain as source of truth under `run_*/notes/round_0001_notes.md`.

### run_20260219_025532 / round_0001
- Metrics: score=0 valid=? exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Build a reusable knowledge cache for unknown large Steiner systems.
  - Focus on existence conditions and practical construction heuristics.

### run_20260219_030101 / round_0001
- Metrics: score=0 valid=? exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Established a high-signal reference base and converted it into a concrete rounds-2+ strategy for `r=6..9`.
  - For admissible large instances with `r=6..9`, an iterative-absorption workflow with monitored nibble phases and multi-start restarts will outperform naive exact/monolithic construction attempts.
  - The strongest consistent message is asymptotic: admissibility conditions are non-negotiable and should be enforced before any heavy search.
  - Practical construction is not one-shot exact solving; it is a pipeline where random greedy handles the bulk and structured absorption/trades finish.
  - Randomization should be treated as a first-class strategy: multiple short-to-medium runs with diagnostics likely dominate one long run.
  - Searched arXiv/web for large Steiner-system existence and constructions.
  - Collected primary sources: Keevash (existence/short proof/counting), iterative absorption (Glock-Kuehn-Lo-Osthus), classical nibble/packing papers, Wilson baseline.
  - Translated literature into concrete operational choices for subsequent rounds.

### run_20260219_180444 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Converted this run from generic notes into a concrete, source-grounded execution program:
  - strong search stack,
  - engine-selector rubric,
  - next-round plan with measurable gates.
  - Hypothesis A (symmetry-first): if orbit compression is strong, KM+basis reduction can beat randomized construction for `r=6,7` and may remain viable at `r=8`.
  - Hypothesis B (randomized-first): if no strong group action appears, nibble+boosting+absorber with residual exact-cover is the only scalable path for `r>=8`.
  - Current instance `S(6,7,17)` is admissible and internally consistent (`lambda_1=728`, `lambda_5=6`).
  - Admissibility is necessary only; source evidence strongly favors either:
- Reference-to-proof mapping:
  - Built and documented a strong search stack in `../KNOWLEDGE_CACHE.md`:
  - 1) hard admissibility/divisibility gate,
  - 2) symmetry/Kramer-Mesner exact-cover mode,
  - 3) nibble -> boosting/repair -> absorber -> residual exact-cover mode.

### run_20260220_183105 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - advance statement: Established a dual-engine search strategy with a mandatory divisibility gate and phase-structured randomized completion.
  - Structure: hard gate + symmetry mode + randomized mode now explicitly specified.
  - Metrics selected for rounds 2+: point degree, `(r-1)`-pressure, uncovered/overcovered counts.
  - Source support: Keevash + iterative absorption + Kramer-Mesner + DLX references linked.
  - Future rounds can run measurable experiments instead of ad hoc search.
  - Engine switching condition is now explicit and testable.
  - hypothesis statement: A hybrid policy (symmetry pre-scan, then randomized iterative absorption, then residual DLX) will dominate single-engine attempts for `r=6..9`.
  - mechanism (why this should help): orbit compression wins when structure exists; randomized absorption handles unstructured bulk; DLX resolves only tiny residue.

### run_20260220_215736 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - advance statement: Established a concrete dual-engine construction stack with explicit selector rules and measurable diagnostics.
  - evidence from this round (metrics, runtime, structure): Admissibility snapshot confirmed; six high-value references mapped to direct implementation consequences for `r=6..9`.
  - transfer value for next rounds: Future rounds can execute immediately without re-deriving theory-to-implementation links.
  - hypothesis statement: Early symmetry triage plus pressure-aware seed selection will dominate either single-engine baseline.
  - mechanism (why this should help): It avoids expensive wrong-engine runs and filters randomized trajectories before hard local bottlenecks harden.
  - expected metric movement: Lower high-quantile `(r-1)` pressure, reduced overcoverage, smaller residual exact-cover instance.
  - falsification / stop condition: If symmetry compression is weak and pressure tails stay high across many seeds, switch to absorber-heavy randomized path only.
  - Current instance is admissible, so downstream quality is now engine-dependent.
- Reference-to-proof mapping:
  - Added high-signal references for:
  - asymptotic existence + divisibility gate,
  - iterative absorption pipeline,
  - lattice-constrained decomposition,

### run_20260220_222225 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Build a reusable knowledge cache for unknown large Steiner systems.
  - Keep strict admissibility as a hard gate.
  - Define when to use symmetry/exact-cover vs nibble/absorption engines.

### run_20260220_222329 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Build a reusable knowledge cache for unknown large Steiner systems.
  - Keep strict admissibility as a hard gate.
  - Define when to use symmetry/exact-cover vs nibble/absorption engines.

### run_20260220_222441 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Converted prior heuristic policy into a source-backed, transfer-ready dual-engine protocol with explicit switch rules and per-`r` consequences.
  - Mandatory cross-run reads completed first, then targeted paper search.
  - Added six primary sources to the cache and linked each to concrete implementation actions for `r=6,7,8,9`.
  - Captured round-2+ stage execution order and mandatory metric set.
  - Next rounds can execute directly from the stage protocol without re-deriving theory.
  - Engine selection now has explicit criteria instead of ad-hoc switching.
  - A fixed symmetry budget plus early fallback into absorber-aware repair will outperform symmetry-heavy attempts on `r=8,9` while preserving strict feasibility.
  - Prior diagnostics show non-binary orbit inflation at larger `r`; longer symmetry search has low marginal value compared with repair passes that directly reduce uncovered mass.

### run_20260221_011431 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Build a reusable knowledge cache for unknown large Steiner systems.
  - Keep strict admissibility as a hard gate.
  - Define when to use symmetry/exact-cover vs nibble/absorption engines.
  - Add new references only if practice logs expose a gap not already covered in global research log.

### run_20260221_013905 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Converted round-1 research into a blocker-driven execution contract: bounded symmetry gate, monitored randomized pipeline, weighted-orbit fallback, and explicit handoff triggers.
  - Mandatory cross-run files were read first.
  - Added five web/arXiv references tied to explicit `r=6..9` consequences.
  - Captured round-2+ stage order and metric requirements with concrete switch signals.
  - Future rounds can execute without re-deriving engine choice rules.
  - Practice blockers now map directly to source-backed implementation changes.
  - A short symmetry front gate plus pressure-triggered early handoff to motif-targeted reserve-aware repair will outperform longer symmetry-heavy or additive-only runs for `r=8,9`, while preserving strict feasibility for all `r=6..9`.
  - Practice logs show plateaus at saturated `(r-1)` motifs and sparse augmenting moves; early switch avoids wasting budget on structurally mismatched binary-orbit search.

### run_20260221_143515 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Build a reusable knowledge cache for unknown large Steiner systems.
  - Keep strict admissibility as a hard gate.
  - Define when to use symmetry/exact-cover vs nibble/absorption engines.
  - Add new references only if practice logs expose a gap not already covered in global research log.

### run_20260221_143650 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Build a reusable knowledge cache for unknown large Steiner systems.
  - Keep strict admissibility as a hard gate.
  - Define when to use symmetry/exact-cover vs nibble/absorption engines.
  - Add new references only if practice logs expose a gap not already covered in global research log.

### run_20260221_143722 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Build a reusable knowledge cache for unknown large Steiner systems.
  - Keep strict admissibility as a hard gate.
  - Define when to use symmetry/exact-cover vs nibble/absorption engines.
  - Add new references only if practice logs expose a gap not already covered in global research log.

### run_20260221_143916 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Build a reusable knowledge cache for unknown large Steiner systems.
  - Keep strict admissibility as a hard gate.
  - Define when to use symmetry/exact-cover vs nibble/absorption engines.
  - Add new references only if practice logs expose a gap not already covered in global research log.

### run_20260222_012007 / round_0001
- Metrics: score=0 valid=false exact_once=0/100947 uncovered=100947 overcovered=0
- Reasoning advances:
  - Converted round1 into a proof-first, gate-explicit execution contract for `S(6,7,23)` with five seeded proof lanes and a 3-loop gap verification routine.
  - Mandatory cross-run memory and local-paper-first requirements were completed.
  - Strong search stack and concise engine selector were formalized for immediate round2 use.
  - Practice blockers now map to source-backed implementation deltas.
  - Rounds2+ can execute without re-deriving proof/search structure.
  - Each stage has explicit stop/switch criteria and required metrics.
  - For `S(6,7,23)`, bounded symmetry triage plus pressure-triggered early repair handoff will beat prolonged symmetry-only or add-only runs while preserving strict feasibility.
  - Practice history shows plateau formation at saturated `(r-1)` motifs and diminishing additive returns; early handoff targets the actual bottleneck.
- Reference-to-proof mapping:
  - New links introduced in this round: `0`.
  - Reused cached links:
  - `https://arxiv.org/abs/1401.3665`
  - `https://arxiv.org/abs/1611.06827`

### run_20260222_043844 / round_0001
- Metrics: score=0 valid=false exact_once=0/475020 uncovered=475020 overcovered=0
- Reasoning advances:
  - Build a reusable knowledge cache for unknown large Steiner systems.
  - Keep strict admissibility as a hard gate.
  - Define when to use symmetry/exact-cover vs nibble/absorption engines.
  - Add new references only if practice logs expose a gap not already covered in global research log.

### run_20260222_043914 / round_0001
- Metrics: score=0 valid=false exact_once=0/475020 uncovered=475020 overcovered=0
- Reasoning advances:
  - Build a reusable knowledge cache for unknown large Steiner systems.
  - Keep strict admissibility as a hard gate.
  - Define when to use symmetry/exact-cover vs nibble/absorption engines.
  - Add new references only if practice logs expose a gap not already covered in global research log.

### run_20260222_045900 / round_0001
- Metrics: score=0 valid=false exact_once=0/475020 uncovered=475020 overcovered=0
- Reasoning advances:
  - Build a reusable knowledge cache for unknown large Steiner systems.
  - Keep strict admissibility as a hard gate.
  - Define when to use symmetry/exact-cover vs nibble/absorption engines.
  - Add new references only if practice logs expose a gap not already covered in global research log.

### run_20260222_051043 / round_0001
- Metrics: score=? valid=? exact_once=? uncovered=? overcovered=?
- Reasoning advances:
  - Converted round1 for `S(6,8,29)` into a proof-first, gate-explicit execution contract with five seeded proof lanes and a 3-loop gap verification process.
  - Mandatory cross-run memory and local-paper-first constraints were completed.
  - Strong search stack and concise engine-selector rubric were formalized.
  - Practice blockers now map to explicit source-backed implementation changes.
  - Rounds2+ can execute directly from stage gates and metric thresholds.
  - Future runs can avoid repeated round1 essay loops by reusing this contract.
  - For `S(6,8,29)`, bounded symmetry triage plus pressure-triggered early repair handoff will outperform prolonged symmetry-only or add-only strategies while keeping strict feasibility.
  - Practice history across `r=6..9` shows add-only plateau and sparse local gains after `(r-1)` saturation; early repair targets this bottleneck.
- Reference-to-proof mapping:
  - New links introduced in this round: `0`.
  - Reused cached links:
  - `https://arxiv.org/abs/1401.3665`
  - `https://arxiv.org/abs/1611.06827`

### run_20260222_052536 / round_0001
- Metrics: score=0 valid=false exact_once=0/475020 uncovered=475020 overcovered=0
- Reasoning advances:
  - Converted round1 for `S(6,8,29)` into a proof-first, gate-explicit execution contract with five seeded proof lanes and a 3-round critical-gap verification loop.
  - Mandatory cross-run memory and local-paper-first conditions were completed.
  - Strong search stack and concise engine selector were formalized.
  - Practice blockers are mapped to explicit implementation changes for rounds2+.
  - Future rounds can execute without re-deriving proof structure.
  - Engine switches and residual exact-cover activation are now gate-based and falsifiable.
  - For `S(6,8,29)`, bounded symmetry triage followed by pressure-triggered strict repair handoff will outperform prolonged symmetry-only or add-only policies under matched budgets while keeping strict feasibility.
  - It matches prior evidence that add-only phases plateau near saturated `(r-1)` motifs and that symmetry quality is highly instance-dependent.
- Reference-to-proof mapping:
  - New links introduced in this round: `0`.
  - Reused cached links:
  - `https://arxiv.org/abs/1401.3665`
  - `https://arxiv.org/abs/1611.06827`

### run_20260222_093016 / round_0001
- Metrics: score=0 valid=false exact_once=0/27132 uncovered=27132 overcovered=0
- Reasoning advances:
  - Build a reusable knowledge cache for unknown large Steiner systems.
  - Keep strict admissibility as a hard gate.
  - Define when to use symmetry/exact-cover vs nibble/absorption engines.
  - Add new references only if practice logs expose a gap not already covered in global research log.

### run_20260222_095901 / round_0001
- Metrics: score=0 valid=false exact_once=0/27132 uncovered=27132 overcovered=0
- Reasoning advances:
  - Build a reusable knowledge cache for unknown large Steiner systems.
  - Keep strict admissibility as a hard gate.
  - Define when to use symmetry/exact-cover vs nibble/absorption engines.
  - Add new references only if practice logs expose a gap not already covered in global research log.

### run_20260222_100809 / round_0001
- Metrics: score=0 valid=false exact_once=0/27132 uncovered=27132 overcovered=0
- Reasoning advances:
  - Build a reusable knowledge cache for unknown large Steiner systems.
  - Keep strict admissibility as a hard gate.
  - Define when to use symmetry/exact-cover vs nibble/absorption engines.
  - Add new references only if practice logs expose a gap not already covered in global research log.

### run_20260222_101642 / round_0001
- Metrics: score=? valid=? exact_once=? uncovered=? overcovered=?
- Reasoning advances:
  - - Added a nonexistence-aware front gate (derivation veto) and rewrote round1 as a proof-first stack for `S(6,7,19)`.
  - - Incorporated roadmap mechanisms (derivation veto; KM; size metrics) into an explicit pipeline and code-delta table.
  - - Mapped practice blockers to concrete implementation changes (portfolio veto, pressure-triggered handoff, weighted-orbit fallback).
  - - Future rounds can avoid wasted solve cycles on derivation-veto eliminated triples and pivot to the smallest *not eliminated* frontier.
  - Adding a verified derivation-veto nonexistence gate before portfolio selection will measurably increase “useful solve yield per compute”
  - by avoiding impossible triples, while preserving the existing hybrid engine benefits on the remaining unknown set.
  - It prevents compute from being spent on instances eliminated by known small nonexistences and focuses effort on the true frontier.
  - fewer solve rounds that terminate with “plateau with no closure” on inherently impossible instances,
- Reference-to-proof mapping:
  - New links introduced in this round: `0`.
  - Reused cached external links: `0` (local PDFs used instead).
  - New PDFs saved under `/root/openquestions/papers`: `none`.

### run_20260222_110632 / round_0001
- Metrics: score=? valid=? exact_once=? uncovered=? overcovered=?
- Reasoning advances:
  - Converted this run’s round1 into a proof-first, veto-aware execution contract for `S(6,7,19)` and rewired the portfolio logic around roadmap derivation-veto results.
  - Admissibility verified (all divisibility remainders `0`); expected blocks `3876`, `λ_5=7`.
  - Roadmap-derived nonexistence propagation identified a high-leverage pre-sieve that may eliminate `S(6,7,19)` and other smallest `q=r+1` admissible instances.
  - Practice-derived metrics reused: strict invariants (`overcovered=0`, `(r-1)` oversubscription `0`) and residual ineligibility at uncovered fraction `≈0.51` for `S(9,10,22)`.
  - Rounds 2+ can avoid solve spend on provably eliminated triples once base nonexistences are verified.
  - The run now has an explicit 5-seed proof stack + 3-stage verification loop + strong search stack to execute without re-deriving theory.
  - Verifying and implementing roadmap derivation-veto propagation (`S(4,5,17)`, `S(5,6,16)`) will measurably increase useful solve yield by eliminating impossible `q=r+1` triples before any solver work.
  - Derivation is a closure property, so each verified base nonexistence wipes out an infinite family; in our finite window it removes the smallest admissible targets that otherwise look most tempting by size.
- Reference-to-proof mapping:
  - New links introduced in this round: `0`.
  - Reused cached links: `0` (local PDFs only; see paths in “Local-paper-first check”).
  - New round1 PDFs saved under `/root/openquestions/papers`: `none`.

### run_20260222_121719 / round_0001
- Metrics: score=? valid=? exact_once=? uncovered=? overcovered=?
- Reasoning advances:
  - Converted round1 for `S(6,7,19)` into a proof-first, gate-explicit research contract centered on derivation-veto triage plus a bounded KM-orbit / randomized repair dichotomy.
  - Mandatory cross-run reads and local-paper-first discipline completed.
  - Admissibility verified (`6/6` remainder checks `0`); roadmap-derived veto chain written and isolated as a bibliographic obligation.
  - Practice log failures were mapped to explicit code deltas with validation metrics.
  - Future rounds can execute without re-deriving the gate stack; the next move is clearly “verify veto or pivot portfolio,” not “try random solver spend.”
  - Implementing (and verifying) the roadmap derivation-veto gate will materially increase useful solve yield per compute by removing divisible-but-impossible `q=r+1` instances before any solve rounds.
  - The gate removes entire families by a short derivation chain, converting “unknown” work into a cheap nonexistence certificate lane.
  - fewer solve rounds scheduled on vetoed instances,
- Reference-to-proof mapping:
  - New links introduced in this round: `0`.
  - Reused sources: local PDFs only (no link churn).
  - New round1 PDFs saved under `/root/openquestions/papers`: `none`.

### run_20260222_135457 / round_0001
- Metrics: score=0 valid=false exact_once=0/27132 uncovered=27132 overcovered=0
- Reasoning advances:
  - - Converted the `S(6,7,19)` round1 into a proof-first, veto-aware execution contract: derivation-veto lane + bounded symmetry triage + staged randomized fallback.
  - - Divisibility gate is explicitly recorded (`b=3876`, `λ_5=7`, all remainders `0`).
  - - Roadmap mechanisms (derivation-veto + KM orbit method) are transferred into an implementation-mapped table for all local PDFs.
  - - Practice-derived blockers are mapped to concrete code deltas and explicit switch/stop rules.
  - - Future rounds can immediately (i) close the bibliographic veto gap and (ii) pivot portfolio to frontier instances without rewriting round1 theory notes.
  - - A verified derivation-veto gate (plus bounded KM diagnostics) will reduce wasted solve spend on `q=r+1` small-`n` instances and improve “useful progress per round” on the remaining unknown set.
  - - It cheaply eliminates impossible instances and routes compute to the smallest not-yet-vetoed frontier (`n=23,24,25,26`) where exact-cover + bounded symmetry has the best chance to matter.
  - - Near-term: fewer solve rounds scheduled on vetoed instances (target: `0`), more rounds allocated to frontier instances; improved log yield (new strict candidates or certified veto witnesses).
- Reference-to-proof mapping:
  - New links introduced in this round: `0`.
  - New round1 PDFs saved under `/root/openquestions/papers`: `none`.

### run_20260222_154119 / round_0001
- Metrics: score=0 valid=false exact_once=0/12376 uncovered=12376 overcovered=0
- Reasoning advances:
  - Converted round1 for `S(6,7,17)` into a proof-first, gate-explicit research contract with five seeded proof lanes and a 3-round critical-gap verification loop.
  - Mandatory cross-run memory and local-paper-first requirements were completed.
  - Strong search stack and concise engine selector were formalized.
  - Practice blockers were mapped to source-backed implementation deltas.
  - Rounds2+ can execute without re-deriving proof skeleton or switch logic.
  - Engine switches and residual activation are now explicit and falsifiable.
  - For `S(6,7,17)`, bounded symmetry triage plus pressure-triggered repair handoff will outperform prolonged single-engine continuation while preserving strict feasibility.
  - It aligns with observed plateau behavior in rounds2-5 and targets saturated `(r-1)` motifs directly.
- Reference-to-proof mapping:
  - New links introduced in this round: `0`.
  - Reused cached links:
  - `https://arxiv.org/abs/1401.3665`
  - `https://arxiv.org/abs/1611.06827`

## URL Index (secondary)
- intentionally minimized
