# Round 3 Notes

Instance: S(7,8,18)
Expected blocks: 3978

## Research reuse
- Read steiner_logs/run_20260219_030101/KNOWLEDGE_CACHE.md first.
- No new web source added this round.
- Applied cached strategy: randomized near-cover construction, then targeted local repair to reduce residual collisions.

## Plan
- Build a full-size 3978-block candidate while maximizing exact-once 7-subsets.
- Use add-greedy selection biased toward uncovered 7-subsets.
- Run swap-based local improvements at fixed block count to lower uncovered and overflow multiplicity.

## Work log
- Enumerated all 8-subsets of [0..17] and their induced 7-subsets.
- Built an initial 3978-block candidate via best-of-sample greedy add.
- Improved candidate with two swap hill-climb passes, accepting only positive objective delta moves.
- Validated against `math_proofs.steiner_system.evaluate_steiner_system`.

## Observations
- Zero-collision packing saturates around ~1.8k blocks; allowing controlled overlaps is required to approach expected block count 3978.
- At fixed 3978 blocks, reducing overflow multiplicity directly tracks uncovered reduction and drives score gains.
- Higher-quality add sampling in swap moves (larger candidate sample) produced the largest late-stage gains.

## Core advance
- Replaced empty candidate with a full 3978-block certificate candidate.
- Metrics improved from:
- score=0.00, exact_once=0/31824, uncovered=31824, overcovered=0, actual_blocks=0
- to:
- score=60.01, exact_once=23438/31824, uncovered=4823, overcovered=3563, overflow_multiplicity=4823, actual_blocks=3978

## Next-hypothesis
- Keep block count fixed at 3978 and run conflict-directed swaps focused on 7-subsets with multiplicity >= 2.
- Try occasional neutral/annealed swaps to escape local plateaus while preserving format-validity and block-count constraints.
