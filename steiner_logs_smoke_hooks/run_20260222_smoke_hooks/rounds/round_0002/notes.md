# Round 2 Notes

Instance: S(6,7,23)
Expected blocks: 14421

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: steiner_logs_smoke_hooks/run_20260222_smoke_hooks/REPO_WIDE_HISTORY.md
- Global research log (all runs round1): steiner_logs_smoke_hooks/RESEARCH_LOG.md
- Global practice log (all runs round2-5): steiner_logs_smoke_hooks/PRACTICE_LOG.md
- Local paper notes: steiner_logs_smoke_hooks/PAPER_NOTES.md
- Latest prior run: none
- Latest prior round1 notes source run: none
- Latest prior round1 notes: missing
- Latest prior round5 notes source run: none
- Latest prior round5 notes: missing
- Latest prior transfer: missing
- Best known metrics across all runs for this instance: none

## Admissibility gate snapshot
```json
{
  "checks": [
    {
      "denominator": 7,
      "i": 0,
      "numerator": 100947,
      "quotient": 14421,
      "remainder": 0
    },
    {
      "denominator": 6,
      "i": 1,
      "numerator": 26334,
      "quotient": 4389,
      "remainder": 0
    },
    {
      "denominator": 5,
      "i": 2,
      "numerator": 5985,
      "quotient": 1197,
      "remainder": 0
    },
    {
      "denominator": 4,
      "i": 3,
      "numerator": 1140,
      "quotient": 285,
      "remainder": 0
    },
    {
      "denominator": 3,
      "i": 4,
      "numerator": 171,
      "quotient": 57,
      "remainder": 0
    },
    {
      "denominator": 2,
      "i": 5,
      "numerator": 18,
      "quotient": 9,
      "remainder": 0
    }
  ],
  "divisibility_failures": [],
  "expected_block_count": 14421,
  "instance": {
    "n": 23,
    "q": 7,
    "r": 6
  },
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 14421,
    "lambda_1": 4389,
    "lambda_2": 1197,
    "lambda_3": 285,
    "lambda_4": 57,
    "lambda_5": 9
  }
}
```

## Research reuse
- Read steiner_logs_smoke_hooks/PAPER_NOTES.md, steiner_logs_smoke_hooks/RESEARCH_LOG.md, steiner_logs_smoke_hooks/PRACTICE_LOG.md, then steiner_logs_smoke_hooks/run_20260222_smoke_hooks/KNOWLEDGE_CACHE.md.
- At most 1 targeted search(es) if cache is insufficient.

## Plan
- Stage A: decide engine (symmetry/orbit exact-cover vs randomized nibble pipeline).
- Stage B: reserve flex/absorber blocks up front.
- Stage C: improve via large-neighborhood repair and residual exact completion when eligible.
- Stage D: run critical-gap self-verification and revise before close.

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
