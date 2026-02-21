# PR Review: #3, #4, #5, #6

## Findings (ordered by severity)

### Medium: path and naming instability across PRs breaks automation
- PR #3 points readers to `math_proofs/frontiermath_specs/` (`math_proofs/README.md:82`).
- PR #4 points to `math_proofs/frontiermath_program_specs/` (`math_proofs/README.md:79`).
- PR #5 points to `math_proofs/frontiermath_14_specs/` (`math_proofs/README.md:81`).
- PR #6 returns to `math_proofs/frontiermath_specs/` (`math_proofs/README.md:81`).
- Impact: scripts/prompts that iterate one canonical folder will fail or require branch-specific conditionals.

### Medium: scoring scale is inconsistent and not normalized
- PR #3 uses decimal `/10` (`math_proofs/frontiermath_specs/01_ramsey_book_graphs.md:3`).
- PR #4 uses integer `/100` (`math_proofs/frontiermath_program_specs/01_ramsey_book_graphs.md:14`).
- PR #5 uses integer `/10` (`math_proofs/frontiermath_14_specs/01_ramsey_numbers_for_book_graphs.md:4`).
- PR #6 uses decimal `/10` (`math_proofs/frontiermath_specs/01_ramsey_numbers_for_book_graphs.md:24`).
- Impact: cross-PR ranking comparisons are noisy and hard to consume programmatically.

### Medium: no automated tests for the new spec corpus
- Existing tests only cover FLT utilities (`math_proofs/test_fermat_little_theorem.py:1` to `math_proofs/test_fermat_little_theorem.py:39`).
- None of the four PRs add validation for: file count, naming convention, or score-table consistency.
- Impact: documentation drift can happen without CI signal.

### Low: PR #6 metadata is placeholder-quality
- Title/body are generic and do not explain intent beyond a generated placeholder.
- Impact: lower traceability during later maintenance and review.

## What each PR did best

- PR #3: strongest spec depth and explicit verifier/certificate framing; includes `scores.csv`.
- PR #4: best assessment-level ranked summary insertion.
- PR #5: clear plain-language score interpretation.
- PR #6: concise scoring rationale style and descriptive file naming direction.

## Merge strategy used in `/root/openquestions`

- Kept PR #3 as structural base for depth and machine-readable outputs.
- Adopted descriptive filename direction used by PR #6.
- Integrated ranking narrative style inspired by PR #4 and PR #6.
- Kept score-interpretation guidance style from PR #5.
- Normalized scoring outputs into both `/10` and `/100` in one canonical source set.
