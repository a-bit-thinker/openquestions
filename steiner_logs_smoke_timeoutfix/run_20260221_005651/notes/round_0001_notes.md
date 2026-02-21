# Round 1 Notes (Research-Only)

Instance: S(6,7,17)
Expected blocks: 1768

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: steiner_logs_smoke_timeoutfix/run_20260221_005651/REPO_WIDE_HISTORY.md
- Global research log (all runs round1): steiner_logs_smoke_timeoutfix/RESEARCH_LOG.md
- Global practice log (all runs round2-5): steiner_logs_smoke_timeoutfix/PRACTICE_LOG.md
- Latest prior run: run_20260221_005638
- Latest prior round1 notes source run: none
- Latest prior round1 notes: missing
- Latest prior round5 notes source run: none
- Latest prior round5 notes: missing
- Latest prior transfer: steiner_logs_smoke_timeoutfix/run_20260221_005638/NEXT_GENERATION_TRANSFER.md

## Admissibility gate snapshot
```json
{
  "checks": [
    {
      "denominator": 7,
      "i": 0,
      "numerator": 12376,
      "quotient": 1768,
      "remainder": 0
    },
    {
      "denominator": 6,
      "i": 1,
      "numerator": 4368,
      "quotient": 728,
      "remainder": 0
    },
    {
      "denominator": 5,
      "i": 2,
      "numerator": 1365,
      "quotient": 273,
      "remainder": 0
    },
    {
      "denominator": 4,
      "i": 3,
      "numerator": 364,
      "quotient": 91,
      "remainder": 0
    },
    {
      "denominator": 3,
      "i": 4,
      "numerator": 78,
      "quotient": 26,
      "remainder": 0
    },
    {
      "denominator": 2,
      "i": 5,
      "numerator": 12,
      "quotient": 6,
      "remainder": 0
    }
  ],
  "divisibility_failures": [],
  "expected_block_count": 1768,
  "instance": {
    "n": 17,
    "q": 7,
    "r": 6
  },
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 1768,
    "lambda_1": 728,
    "lambda_2": 273,
    "lambda_3": 91,
    "lambda_4": 26,
    "lambda_5": 6
  }
}
```

## Research (this round)
- URL:
- Takeaway:
- Applied change from source:

## Plan
- Build a reusable knowledge cache for unknown large Steiner systems.
- Keep strict admissibility as a hard gate.
- Define when to use symmetry/exact-cover vs nibble/absorption engines.
- Add new references only if practice logs expose a gap not already covered in global research log.

## Work log
-

## Observations
-

## Core advance
- advance statement:
- evidence from this round (metrics, runtime, structure):
- transfer value for next rounds:

## Next-hypothesis
- hypothesis statement:
- mechanism (why this should help):
- expected metric movement:
- falsification / stop condition:
