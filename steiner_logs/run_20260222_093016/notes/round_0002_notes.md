# Round 2 Notes

Instance: S(6,7,19)
Expected blocks: 3876

## Cross-run bootstrap (mandatory first read)
- Repo-wide history: steiner_logs/run_20260222_093016/REPO_WIDE_HISTORY.md
- Global research log (all runs round1): steiner_logs/RESEARCH_LOG.md
- Global practice log (all runs round2-5): steiner_logs/PRACTICE_LOG.md
- Global research paper (paper-style synthesis): steiner_logs/RESEARCH_PAPER.md
- Existence frontier report (all admissible triples): steiner_logs/EXISTENCE_FRONTIER.md
- Local paper notes: steiner_logs/PAPER_NOTES.md
- Latest prior run: run_20260222_052536
- Latest prior round1 notes source run: run_20260222_052536
- Latest prior round1 notes: steiner_logs/run_20260222_052536/notes/round_0001_notes.md
- Latest prior round5 notes source run: run_20260222_052536
- Latest prior round5 notes: steiner_logs/run_20260222_052536/notes/round_0005_notes.md
- Latest prior transfer: steiner_logs/run_20260222_052536/NEXT_GENERATION_TRANSFER.md
- Best known metrics across all runs for this instance: score=0 run=run_20260222_093016 round=1 valid=false exact_once=0/27132 uncovered=27132 overcovered=0

## Admissibility gate snapshot
```json
{
  "checks": [
    {
      "denominator": 7,
      "i": 0,
      "numerator": 27132,
      "quotient": 3876,
      "remainder": 0
    },
    {
      "denominator": 6,
      "i": 1,
      "numerator": 8568,
      "quotient": 1428,
      "remainder": 0
    },
    {
      "denominator": 5,
      "i": 2,
      "numerator": 2380,
      "quotient": 476,
      "remainder": 0
    },
    {
      "denominator": 4,
      "i": 3,
      "numerator": 560,
      "quotient": 140,
      "remainder": 0
    },
    {
      "denominator": 3,
      "i": 4,
      "numerator": 105,
      "quotient": 35,
      "remainder": 0
    },
    {
      "denominator": 2,
      "i": 5,
      "numerator": 14,
      "quotient": 7,
      "remainder": 0
    }
  ],
  "divisibility_failures": [],
  "expected_block_count": 3876,
  "instance": {
    "n": 19,
    "q": 7,
    "r": 6
  },
  "is_admissible": true,
  "is_well_formed": true,
  "issues": [],
  "replication_numbers": {
    "lambda_0": 3876,
    "lambda_1": 1428,
    "lambda_2": 476,
    "lambda_3": 140,
    "lambda_4": 35,
    "lambda_5": 7
  }
}
```

## Research reuse
- Read steiner_logs/PAPER_NOTES.md, steiner_logs/RESEARCH_LOG.md, steiner_logs/PRACTICE_LOG.md, steiner_logs/RESEARCH_PAPER.md, steiner_logs/EXISTENCE_FRONTIER.md, then steiner_logs/run_20260222_093016/KNOWLEDGE_CACHE.md.
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
