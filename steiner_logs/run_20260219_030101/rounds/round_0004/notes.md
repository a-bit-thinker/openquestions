# Round 4 Notes

Instance: S(8,9,19)
Expected blocks: 8398

## Research reuse
- Read steiner_logs/run_20260219_030101/KNOWLEDGE_CACHE.md first.
- Add only incremental references if needed.

## Plan
- Apply cached techniques to improve verifier score for this instance.

## Work log
- Implemented a full-size constructive search for `S(8,9,19)` at fixed block count `8398`.
- Enumerated all `9`-subsets of `[0..18]` and their induced `8`-subset incidences.
- Phase A (greedy add): best-of-random-sample block insertion to build an initial 8398-block certificate while maximizing immediate objective gain.
- Phase B (targeted repair): ran 25,000 remove/add swap iterations at fixed block count, with add candidates biased toward currently uncovered `8`-subsets.
- Added periodic checkpoint saves/evaluation to preserve best-so-far candidate during long runs.
- Wrote improved certificate to `steiner_logs/run_20260219_030101/candidates/candidate_19_9_8.json`.
- Verified with `math_proofs.steiner_system.evaluate_steiner_system`.

## Observations
- Keeping `actual_block_count=expected_block_count=8398` removes block-count penalty and makes uncovered/overflow tradeoffs the dominant optimization target.
- Conflict-directed swaps (remove high-collision blocks, add near uncovered facets) gave consistent incremental gains over pure random swaps.
- Improvements became incremental after ~15k swaps, but continued through 25k.
- No additional web sources were needed beyond cached round-1 references.

## Core advance
- Replaced empty candidate `[]` with a well-formed 8398-block certificate candidate and substantially improved verifier metrics.
- Before: `score=0.00`, `exact_once=0/75582`, `uncovered=75582`, `overcovered=0`, `actual_blocks=0`.
- After: `score=57.35`, `exact_once=54397/75582`, `uncovered=12276`, `overcovered=8909`, `overflow_multiplicity=12276`, `actual_blocks=8398`.

## Next-hypothesis
- Continue local search from this certificate with larger add-sample neighborhoods and occasional multi-block (2-for-2 / ejection-chain) moves to escape local plateaus.
- Prioritize swaps touching highest-multiplicity `8`-subsets and uncovered hotspots to reduce both uncovered and overcovered counts together.
