# Round 5 Notes

Instance: S(9,10,20)
Expected blocks: 16796

## Research reuse
- Read steiner_logs/run_20260219_030101/KNOWLEDGE_CACHE.md first.
- Add only incremental references if needed.

## Plan
- Apply cached techniques to improve verifier score for this instance.

## Work log
- Reused cached round-1 strategy (randomized near-cover + local repair) without new web lookup.
- Loaded `candidate_19_9_8.json` as a seed structure on vertices `[0..18]`.
- Built a two-part certificate for `S(9,10,20)`:
- Part F: for each 9-block `B` in the seed, added `B ∪ {19}` (8398 blocks containing vertex 19).
- Part G: optimized 8398 blocks on `[0..18]` (10-subsets) to complement Part F.
- Part G construction:
- Greedy phase: 8398 add steps, best-of-500 random block samples per step, objective biased to create exact-once 9-subset multiplicities.
- Swap phase: 20,000 fixed-cardinality remove/add swaps (positive-delta acceptance) to reduce uncovered and overcovered counts.
- Wrote final certificate to `steiner_logs/run_20260219_030101/candidates/candidate_20_10_9.json`.
- Verified with `math_proofs.steiner_system.evaluate_steiner_system`.

## Observations
- The decomposition around vertex `19` gave a strong scaffold quickly and kept block count exactly at the target `16796`.
- A naive transformed seed scored `44.07`; rebuilding the `[0..18]` half with objective-driven greedy raised this to `54.34`.
- Swap repair added incremental but consistent gains, ending at `54.95`.
- The final candidate is structurally clean (`invalid_block_count=0`, `duplicate_block_count=0`) with all hard format constraints satisfied.

## Core advance
- Replaced empty candidate `[]` with a full-size, format-valid 16796-block certificate candidate that substantially improves verifier metrics.
- Before: `score=0.00`, `exact_once=0/167960`, `uncovered=167960`, `overcovered=0`, `actual_blocks=0`.
- After: `score=54.95`, `exact_once=118187/167960`, `uncovered=28774`, `overcovered=20999`, `overflow_multiplicity=28774`, `actual_blocks=16796`.

## Next-hypothesis
- Continue fixed-size local search with larger add-neighborhood samples and occasional multi-block exchanges to escape local plateaus.
- Target hotspots: 9-subsets currently uncovered and high-multiplicity collisions in the `[0..18]` projection while preserving exact block count.
