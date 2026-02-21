import unittest

from math_proofs.steiner_system import (
    evaluate_steiner_submission_text,
    evaluate_steiner_system,
    steiner_admissibility_report,
    verify_steiner_submission_text,
    verify_steiner_system,
)


STEINER_S348_BLOCKS = [
    [0, 1, 2, 3],
    [0, 1, 4, 5],
    [0, 1, 6, 7],
    [0, 2, 4, 6],
    [0, 2, 5, 7],
    [0, 3, 4, 7],
    [0, 3, 5, 6],
    [1, 2, 4, 7],
    [1, 2, 5, 6],
    [1, 3, 4, 6],
    [1, 3, 5, 7],
    [2, 3, 4, 5],
    [2, 3, 6, 7],
    [4, 5, 6, 7],
]

STEINER_S348_TEXT_1_BASED = """#8,4,3
1 2 3 4
1 2 5 6
1 2 7 8
1 3 5 7
1 3 6 8
1 4 5 8
1 4 6 7
2 3 5 8
2 3 6 7
2 4 5 7
2 4 6 8
3 4 5 6
3 4 7 8
5 6 7 8
"""


class SteinerSystemVerifierTests(unittest.TestCase):
    def test_verify_steiner_s348(self):
        instance = {"n": 8, "q": 4, "r": 3}
        self.assertTrue(verify_steiner_system(instance, STEINER_S348_BLOCKS))

    def test_evaluate_valid_report(self):
        instance = {"n": 8, "q": 4, "r": 3}
        report = evaluate_steiner_system(instance, STEINER_S348_BLOCKS)

        self.assertTrue(report["is_valid"])
        self.assertEqual(100.0, report["score"])
        self.assertEqual(56, report["total_required_r_subsets"])
        self.assertEqual(14, report["expected_block_count"])
        self.assertEqual(14, report["actual_block_count"])
        self.assertEqual(0, report["uncovered_r_subsets"])
        self.assertEqual(0, report["overcovered_r_subsets"])

    def test_detects_missing_coverage(self):
        instance = {"n": 8, "q": 4, "r": 3}
        incomplete = STEINER_S348_BLOCKS[:-1]

        report = evaluate_steiner_system(instance, incomplete)
        self.assertFalse(report["is_valid"])
        self.assertGreater(report["uncovered_r_subsets"], 0)
        self.assertLess(report["score"], 100.0)

    def test_detects_divisibility_impossibility(self):
        instance = {"n": 6, "q": 3, "r": 2}
        report = evaluate_steiner_system(instance, [])

        self.assertFalse(report["is_valid"])
        self.assertTrue(report["divisibility_failures"])
        self.assertIn("instance fails Steiner divisibility preconditions", report["issues"])

    def test_admissibility_report_for_valid_instance(self):
        instance = {"n": 8, "q": 4, "r": 3}
        report = steiner_admissibility_report(instance)
        self.assertTrue(report["is_admissible"])
        self.assertEqual(14, report["expected_block_count"])
        self.assertEqual(14, report["replication_numbers"]["lambda_0"])
        self.assertEqual(7, report["replication_numbers"]["lambda_1"])
        self.assertEqual(3, report["replication_numbers"]["lambda_2"])

    def test_admissibility_report_for_invalid_instance(self):
        instance = {"n": 6, "q": 3, "r": 2}
        report = steiner_admissibility_report(instance)
        self.assertFalse(report["is_admissible"])
        self.assertGreater(len(report["divisibility_failures"]), 0)
        self.assertIn("i", report["divisibility_failures"][0])

    def test_detects_invalid_blocks(self):
        instance = {"n": 8, "q": 4, "r": 3}
        bad_certificate = [
            [0, 1, 2],
            [0, 1, 2, 2],
            [0, 1, 2, 8],
            [0, 1, 2, 3],
            [0, 1, 2, 3],
        ]
        report = evaluate_steiner_system(instance, bad_certificate)

        self.assertFalse(report["is_valid"])
        self.assertGreater(report["invalid_block_count"], 0)
        self.assertGreater(report["duplicate_block_count"], 0)

    def test_r_minus_1_oversubscription_is_reported(self):
        instance = {"n": 8, "q": 4, "r": 3}
        duplicated = STEINER_S348_BLOCKS + [STEINER_S348_BLOCKS[0]]
        report = evaluate_steiner_system(instance, duplicated)
        self.assertGreater(report["oversubscribed_r_minus_1_subsets"], 0)
        self.assertIn(
            "certificate oversubscribes some (r-1)-subsets; completion is impossible without deletions",
            report["issues"],
        )

    def test_additive_repair_and_residual_hint_for_one_missing_block(self):
        instance = {"n": 8, "q": 4, "r": 3}
        partial = STEINER_S348_BLOCKS[:-1]
        report = evaluate_steiner_system(instance, partial)
        self.assertTrue(report["additive_repair_feasible"])
        self.assertTrue(report["residual_repair_hint"]["eligible"])
        self.assertEqual(1, report["min_additional_blocks_needed_for_uncovered"])

    def test_text_submission_parsing_and_verification(self):
        report = evaluate_steiner_submission_text(STEINER_S348_TEXT_1_BASED)
        self.assertTrue(report["steiner_valid"])
        self.assertTrue(report["task_valid"])
        self.assertEqual(100.0, report["score"])
        self.assertEqual([], report["format_issues"])

        self.assertTrue(verify_steiner_submission_text(STEINER_S348_TEXT_1_BASED))

    def test_text_submission_full_constraint_gate(self):
        report = evaluate_steiner_submission_text(
            STEINER_S348_TEXT_1_BASED, enforce_full_question_constraints=True
        )
        self.assertTrue(report["steiner_valid"])
        self.assertFalse(report["task_valid"])
        self.assertIn("full-task constraint failed: r must be > 5", report["constraint_issues"])
        self.assertEqual(0.0, report["task_score"])
        self.assertFalse(
            verify_steiner_submission_text(
                STEINER_S348_TEXT_1_BASED, enforce_full_question_constraints=True
            )
        )

    def test_text_submission_format_errors(self):
        bad = """8,4,3
1 2 3 4
"""
        report = evaluate_steiner_submission_text(bad)
        self.assertFalse(report["task_valid"])
        self.assertTrue(report["format_issues"])


if __name__ == "__main__":
    unittest.main()
