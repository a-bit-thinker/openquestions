# Loop Contract

## Round Responsibilities
- Round 1: proof-first synthesis, source transfer mapping, executable hypotheses.
- Rounds 2-4: solver attempts with strict metrics and checkpoint evidence.
- Round 5: synthesis of rounds1-4 and next hypothesis ladder.

## Required Round Outputs (target format)
- `RUN_FACTS.json`: instance, budgets, route, metrics, outcome class.
- `CLAIM_DELTAS.yaml`: added/updated/retired claims with evidence references.
- `HYPOTHESIS_DELTAS.yaml`: activation, retirement, falsification outcomes.
- `SOURCE_TRANSFER_DELTAS.yaml`: source -> mechanism -> code delta entries.

## Change Boundary Contract (target behavior)
Before running a round, define:
- allowed file globs,
- forbidden file globs,
- required checks,
- required docs updates.

Round close should fail if edits violate the boundary contract.
