# Steiner Loop Logging System

This logging system records each Codex round independently and generates a handoff summary for the next round.

## 1) Start a round

```bash
cd /root/openquestions
python3 -m math_proofs.steiner_round_logger start \
  --log-dir steiner_logs \
  --instance-json '{"n":17,"q":7,"r":6}' \
  --objective 'Construct S(6,7,17)' \
  --hypothesis 'Use constructive search with collision penalties'
```

Output: `round_0001` (or next id).

## 2) Prepare candidate certificate JSON

`candidate.json` format:

```json
[
  [0, 1, 2],
  [0, 3, 4]
]
```

Each entry is one block (q-subset).

## 3) Close round and evaluate benchmark score

```bash
python3 -m math_proofs.steiner_round_logger close \
  --log-dir steiner_logs \
  --round-id round_0001 \
  --certificate-file candidate.json \
  --notes-file notes.md \
  --technique greedy \
  --technique local-search
```

Writes:

- `steiner_logs/rounds/round_0001/meta.json`
- `steiner_logs/rounds/round_0001/notes.md`
- `steiner_logs/rounds/round_0001/candidate.json`
- `steiner_logs/rounds/round_0001/evaluation.json`
- `steiner_logs/rounds/round_0001/round_summary.md`
- `steiner_logs/rounds/index.jsonl`
- `steiner_logs/rounds/NEXT_ROUND_BRIEF.md`

## 4) Score/benchmark definition

Per round benchmark includes:

- `is_valid` (exact Steiner validity)
- `score` (0..100; 100 means exact valid certificate)
- `exact_once_r_subsets / total_required_r_subsets`
- `uncovered_r_subsets`
- `overcovered_r_subsets`
- `actual_block_count` vs `expected_block_count`
- `invalid_block_count`
- admissibility/divisibility diagnostics (`divisibility_failures`)
- structural pressure metrics:
  - `point_degree_min/max/gap` vs `target_point_degree`
  - `(r-1)` load metrics (`r_minus_1_max_degree`, `oversubscribed_r_minus_1_subsets`)
- repair hints:
  - `additive_repair_feasible`
  - `residual_repair_hint`

This gives both theorem-level pass/fail and incremental progress signals for partial candidates.

## 5) Regenerate next-round brief

```bash
python3 -m math_proofs.steiner_round_logger report --log-dir steiner_logs
```

The generated `NEXT_ROUND_BRIEF.md` is the handoff document for the next Codex round.

## 6) Optional residual exact-repair stage

For a collision-free partial candidate (no overcovered r-subsets), run:

```bash
python3 -m math_proofs.steiner_residual_repair \
  --instance-json '{"n":8,"q":4,"r":3}' \
  --candidate-file candidate.json \
  --output-file candidate_repaired.json
```

If residual exact cover is solved, `candidate_repaired.json` contains the improved certificate.

## 7) Per-round time limit in loop runs

`run_steiner_loop.sh` enforces a per-round wall-clock budget:

```bash
ROUND_TIME_LIMIT_SEC=3600 ./run_steiner_loop.sh
```

Default is `3600` seconds (1 hour) per round.

Low-time summary guard (default `200s`) to prevent timeout spillover:

```bash
LOW_TIME_SUMMARY_THRESHOLD_SEC=200 ./run_steiner_loop.sh
```

When remaining round time is at or below the threshold, the loop skips heavy stages (exact solver / Codex / residual repair) and appends synthesis notes instead.

## 8) Exact-cover-first backbone

The loop can run an exact-cover stage before Codex in solve rounds (recommended for `S(6,7,17)`):

```bash
EXACT_BACKBONE_ENABLED=1 \
EXACT_BACKBONE_R_VALUES='6 7 8 9' \
EXACT_BACKBONE_TIMEOUT_SEC=900 \
./run_steiner_loop.sh
```

Standalone CLI:

```bash
python3 -m math_proofs.steiner_exact_cover \
  --instance-json '{"n":17,"q":7,"r":6}' \
  --candidate-file steiner_candidate.json \
  --output-file steiner_candidate.json \
  --time-limit-sec 900
```

This uses exact-cover-first (with symmetry breaking for empty seeds) and falls back to conflict-free greedy plus exact completion when full exact is too large.

The loop now selects per-instance \"best\" candidates using an exactness-first rank:
`is_valid`, then `overcovered==0`, then lower `overcovered`, then coverage quality.
This prevents high-collision candidates from blocking clean exact-cover progress.

## 9) Cross-round knowledge transfer artifact

Each round now refreshes:

- `RUN_LOG_DIR/NEXT_GENERATION_TRANSFER.md`

This file summarizes recent rounds (trajectory, core advances, blockers, and next-hypothesis ladder) so round-5 handoff preserves reasoning for the next run/agent.

The loop also generates:

- `RUN_LOG_DIR/REPO_WIDE_HISTORY.md`
- `LOG_ROOT/RESEARCH_LOG.md` (repo-wide round1 knowledge aggregation)
- `LOG_ROOT/PRACTICE_LOG.md` (repo-wide rounds2-5 trajectory aggregation)

This scans all `steiner_logs/run_*`, records best-known metrics by instance across runs, and points to the latest available prior `round_0001_notes.md` and `round_0005_notes.md`.
Each round prompt now requires reading `RESEARCH_LOG.md` and `PRACTICE_LOG.md` before new work.
If either file exceeds `GLOBAL_LOG_MAX_BYTES` (default `50000`), the loop writes a compact summary view while preserving raw redundancy in `run_*/notes/`.

When `STRICT_ROUND5_SYNTHESIS_GATE=1` (default), solve rounds `>=5` will **fail before close** unless the round notes contain this heading exactly:

`## Rounds 1-5 Synthesis`
