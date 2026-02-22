# Docs System Of Record

This directory is the canonical knowledge base for the Steiner loop.
Raw run logs under `steiner_logs/` are telemetry, not canonical state.

## Scope
- Domain: Steiner systems `S(r,q,n)` with `n > q > r > 5`, `r < 10`, `n < 200`.
- Loop modes: round1 research/proof planning; rounds2-5 solver execution and synthesis.

## Document Layers
1. `core/`: loop contracts and architecture.
2. `problem/`: mathematical definitions and fixed rules.
3. `knowledge/`: claims, hypotheses, sources, certificates.
4. `instances/`: instance states and frontier queue.
5. `methods/`: engine routing and playbooks.
6. `quality/`: gate specs, review checklist, scorecard.
7. `generated/`: machine outputs generated from runs.
8. `schemas/`: machine-readable schemas for YAML/JSON artifacts.

## Update Rules
- Any claim/hypothesis update must modify `knowledge/*.yaml`.
- Any instance status change must modify `instances/*.yaml`.
- Any gate change must update `quality/GATE_SPEC.md` and relevant schema files.
- `steiner_logs/*.md` may provide evidence but must not be treated as canonical truth.

## Bootstrapped From
- `steiner_logs/RESEARCH_PAPER.md`
- `steiner_logs/EXISTENCE_FRONTIER.md`
- `steiner_logs/PRACTICE_LOG.md`
- `steiner_logs/RESEARCH_LOG.md`
- `steiner_logs/run_20260222_110632/notes/round_0001_notes.md`
- `steiner_logs/run_20260222_101642/notes/round_0001_notes.md`
