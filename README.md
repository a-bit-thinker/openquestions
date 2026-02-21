# Open Questions

`openquestions` is a working research repo for two tracks:

1. Frontier math problem assessment artifacts (ranked specs and scoring).
2. Steiner system search tooling, verification, and multi-round knowledge-transfer logs.

## Repository Structure

- `math_proofs/`
  - `frontiermath_specs/`: normalized specs for 14 open problems plus `scores.csv` and `SCORES.md`.
  - `frontiermath_open_problems_assessment.md`: merged narrative assessment.
  - `steiner_system.py`: verifier, evaluator, and admissibility diagnostics.
  - `steiner_exact_cover.py`: exact-cover-first solver stage.
  - `steiner_residual_repair.py`: residual exact completion helper.
  - `steiner_round_logger.py`: round lifecycle logger (`start`, `close`, `report`).
- `run_steiner_round.sh`: thin wrapper for single round start/close flow.
- `run_steiner_loop.sh`: automated multi-round loop with cross-run memory.
- `papers/`: local PDF library for reusable proof-method context.
- `STEINER_LOOP_LOGGING.md`: detailed workflow and logging rules.
- `PR_REVIEW.md`: review notes from merged PR variants.

## Quick Start

Run tests:

```bash
python3 -m unittest
```

Run a single round manually:

```bash
python3 -m math_proofs.steiner_round_logger start \
  --log-dir steiner_logs \
  --instance-json '{"n":17,"q":7,"r":6}' \
  --objective 'Construct S(6,7,17)' \
  --hypothesis 'Try exact-cover-first with strict admissibility'
```

Run the loop:

```bash
./run_steiner_loop.sh
```

## Steiner Loop Design

The loop is built to preserve progress across rounds and across runs.

- Hard admissibility gate before search.
- Optional exact-cover backbone before heuristic/model steps.
- Residual exact repair when eligible.
- Strict round-5 synthesis gate (configurable).
- Repo-wide memory refresh each round:
  - `steiner_logs/RESEARCH_LOG.md` (round1 knowledge)
  - `steiner_logs/PRACTICE_LOG.md` (round2-5 trajectory)
  - `steiner_logs/PAPER_NOTES.md` (auto-extracted local-paper method notes)
- Auto-compaction of global logs via `GLOBAL_LOG_MAX_BYTES` (default `50000`).

## Important Runtime Knobs

- `ROUNDS`
- `ROUND_TIME_LIMIT_SEC`
- `LOW_TIME_SUMMARY_THRESHOLD_SEC`
- `GLOBAL_LOG_MAX_BYTES`
- `PAPERS_DIR`
- `LOCAL_PAPER_NOTES_FILE`
- `EXACT_BACKBONE_ENABLED`
- `AUTO_RESIDUAL_REPAIR`
- `USE_CODEX`

Example:

```bash
ROUNDS=5 \
ROUND_TIME_LIMIT_SEC=3600 \
LOW_TIME_SUMMARY_THRESHOLD_SEC=200 \
GLOBAL_LOG_MAX_BYTES=50000 \
./run_steiner_loop.sh
```

## Notes

- Per-run raw notes are kept as redundancy under `steiner_logs/run_*/notes/`.
- Global research/practice logs are synthesized views and may be compacted.
- Put PDFs in `papers/`; the loop auto-refreshes `PAPER_NOTES.md` each round and uses it in round prompts.
