# Loop Architecture

## Control Flow
1. Load canonical docs from `docs/`.
2. Load latest telemetry from `steiner_logs/`.
3. Run round according to role contract.
4. Emit structured deltas.
5. Update canonical docs.
6. Optionally emit narrative log summaries.

## Data Flow
- Inputs: instance registry, frontier queue, active hypotheses, source transfer map.
- Process: gate checks -> engine selector -> solver/proof steps -> verifier.
- Outputs: metric snapshots, claim/hypothesis deltas, updated statuses.

## Non-goal
`steiner_logs/*.md` growth is not the system of record.
