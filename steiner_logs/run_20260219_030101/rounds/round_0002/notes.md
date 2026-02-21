# Round 2 Notes

Instance: S(6,7,17)
Expected blocks: 1768

## Research reuse
- Read steiner_logs/run_20260219_030101/KNOWLEDGE_CACHE.md first.
- Add only incremental references if needed.

## Plan
- Apply cached techniques to improve verifier score for this instance.

## Work log
- Built a direct constructive search for `S(6,7,17)` candidates in two phases.
- Phase A (greedy coverage): selected 1768 blocks while maximizing newly covered 6-subsets per step.
- Phase B (targeted repair): performed 50,000 swap moves (remove one selected block, add one unselected block) to reduce uncovered/overcovered.
- Wrote best certificate to `steiner_logs/run_20260219_030101/candidates/candidate_17_7_6.json`.
- Verified with local evaluator `math_proofs.steiner_system.evaluate_steiner_system`.

## Observations
- For fixed block count 1768, greedy alone quickly reaches low uncovered but leaves many multiplicity conflicts.
- Swap-based local repair reliably reduced both uncovered and overcovered from the greedy baseline.
- No external source lookup was needed beyond cached round-1 guidance.

## Core advance
- Replaced empty candidate `[]` with a fully well-formed 1768-block certificate that substantially improves verifier metrics:
- Before: `score=0.00`, `exact_once=0/12376`, `uncovered=12376`, `overcovered=0`, `actual_blocks=0`.
- After: `score=66.04`, `exact_once=9591/12376`, `uncovered=1575`, `overcovered=1210`, `actual_blocks=1768`.

## Next-hypothesis
- Continue local search from this 1768-block certificate with stronger neighborhood moves (multi-block trades / tabu memory) to push uncovered and overcovered down further.
