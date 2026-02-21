import unittest

from math_proofs.steiner_exact_cover import solve_steiner_exact_cover

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


class SteinerExactCoverTests(unittest.TestCase):
    def test_solves_small_exact_cover_from_empty(self):
        instance = {"n": 8, "q": 4, "r": 3}
        result = solve_steiner_exact_cover(
            instance,
            [],
            time_limit_sec=10.0,
            max_nodes=200_000,
            full_exact_max_rows=1_000,
            full_exact_max_options=1_000,
            random_seed=0,
        )

        self.assertEqual("solved", result["status"])
        self.assertTrue(result["evaluation"]["is_valid"])
        self.assertEqual(100.0, result["evaluation"]["score"])

    def test_handles_overcovered_seed_by_conflict_free_projection(self):
        instance = {"n": 8, "q": 4, "r": 3}
        overcovered_seed = STEINER_S348_BLOCKS + [STEINER_S348_BLOCKS[0]]
        result = solve_steiner_exact_cover(
            instance,
            overcovered_seed,
            time_limit_sec=10.0,
            max_nodes=200_000,
            full_exact_max_rows=1_000,
            full_exact_max_options=1_000,
            random_seed=1,
        )

        self.assertEqual("solved", result["status"])
        self.assertTrue(result["evaluation"]["is_valid"])

    def test_inadmissible_instance_short_circuits(self):
        instance = {"n": 6, "q": 3, "r": 2}
        result = solve_steiner_exact_cover(instance, [], time_limit_sec=1.0)
        self.assertEqual("inadmissible", result["status"])


if __name__ == "__main__":
    unittest.main()
