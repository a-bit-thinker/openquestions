# Round 5 Notes

Instance: S(9,10,20)
Expected blocks: 16796

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: steiner_logs/run_20260220_222441/REPO_WIDE_HISTORY.md
- Latest prior run: run_20260220_222329
- Latest prior round1 notes source run: run_20260220_222329
- Latest prior round1 notes: steiner_logs/run_20260220_222329/notes/round_0001_notes.md
- Latest prior round5 notes source run: run_20260220_183105
- Latest prior round5 notes: steiner_logs/run_20260220_183105/notes/round_0005_notes.md
- Latest prior transfer: steiner_logs/run_20260220_222329/NEXT_GENERATION_TRANSFER.md
- Best known metrics across all runs for this instance: score=55.44 run=run_20260219_180444 round=5 valid=false exact_once=118787/167960 uncovered=28530 overcovered=20643

## Admissibility gate snapshot
```json
{
  "checks": [
    {
      "denominator": 10,
      "i": 0,
      "numerator": 167960,
      "quotient": 16796,
      "remainder": 0
    },
    {
      "denominator": 9,
      "i": 1,
      "numerator": 75582,
      "quotient": 8398,
      "remainder": 0
    },
    {
      "denominator": 8,
      "i": 2,
      "numerator": 31824,
      "quotient": 3978,
      "remainder": 0
    },
    {
      "denominator": 7,
      "i": 3,
      "numerator": 12376,
      "quotient": 1768,
      "remainder": 0
    },
    {
      "denominator": 6,
      "i": 4,
      "numerator": 4368,
      "quotient": 728,
      "remainder": 0
    },
    {
      "denominator": 5,
      "i": 5,
      "numerator": 1365,
      "quotient": 273,
      "remainder": 0
    },
    {
      "denominator": 4,
      "i": 6,
      "numerator": 364,
      "quotient": 91,
      "remainder": 0
    },
    {
      "denominator": 3,
      "i": 7,
      "numerator": 78,
      "quotient": 26,
      "remainder": 0
    },
    {
      "denominator": 2,
      "i": 8,
      "numerator": 12,
      "quotient": 6,
      "remainder": 0
    }
  ],
  "divisibility_failures": [],
  "expected_block_count": 16796,
  "instance": {
    "n": 20,
    "q": 10,
    "r": 9
  },
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 16796,
    "lambda_1": 8398,
    "lambda_2": 3978,
    "lambda_3": 1768,
    "lambda_4": 728,
    "lambda_5": 273,
    "lambda_6": 91,
    "lambda_7": 26,
    "lambda_8": 6
  }
}
```

## Research reuse
- Read steiner_logs/run_20260220_222441/KNOWLEDGE_CACHE.md first.
- At most 1 targeted search(es) if cache is insufficient.

## Plan
- Stage A: decide engine (symmetry/orbit exact-cover vs randomized nibble pipeline).
- Stage B: reserve flex/absorber blocks up front.
- Stage C: improve via large-neighborhood repair and residual exact completion when eligible.

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
