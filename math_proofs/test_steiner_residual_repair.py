import unittest

from math_proofs.steiner_residual_repair import attempt_additive_residual_repair

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


class SteinerResidualRepairTests(unittest.TestCase):
    def test_solves_one_block_missing_case(self):
        instance = {"n": 8, "q": 4, "r": 3}
        partial = STEINER_S348_BLOCKS[:-1]

        result = attempt_additive_residual_repair(
            instance,
            partial,
            timeout_sec=5.0,
            max_nodes=50_000,
            max_total_r_subsets=10_000,
            max_uncovered_r_subsets=100,
            max_q_subset_scan=1_000,
            max_candidate_blocks=10_000,
        )

        self.assertEqual("solved", result["status"])
        self.assertEqual(1, result["added_block_count"])
        self.assertTrue(result["repaired_evaluation"]["is_valid"])
        self.assertEqual(100.0, result["repaired_evaluation"]["score"])

    def test_rejects_overcovered_residual(self):
        instance = {"n": 8, "q": 4, "r": 3}
        duplicated = STEINER_S348_BLOCKS + [STEINER_S348_BLOCKS[0]]

        result = attempt_additive_residual_repair(
            instance,
            duplicated,
            timeout_sec=2.0,
            max_nodes=5_000,
        )

        self.assertEqual("ineligible", result["status"])
        self.assertIn("overcovered", result["reason"])


if __name__ == "__main__":
    unittest.main()
