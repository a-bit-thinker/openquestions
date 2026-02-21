import tempfile
import unittest
from pathlib import Path

from math_proofs.steiner_round_logger import close_round, start_round


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


class SteinerRoundLoggerTests(unittest.TestCase):
    def test_round_logging_and_handoff(self):
        with tempfile.TemporaryDirectory() as td:
            log_root = Path(td) / "steiner_logs"
            instance = {"n": 8, "q": 4, "r": 3}

            r1 = start_round(
                log_root=log_root,
                instance=instance,
                objective="Find S(3,4,8)",
                hypothesis="Start from partial coverage",
            )
            self.assertEqual("round_0001", r1)

            summary1 = close_round(
                log_root=log_root,
                round_id=r1,
                certificate=STEINER_S348_BLOCKS[:6],
                techniques=["greedy-init"],
                notes_text="# round 1 notes\n",
            )

            self.assertFalse(summary1["is_valid"])
            self.assertLess(summary1["score"], 100.0)
            self.assertIn("point_degree_gap", summary1)
            self.assertIn("residual_repair_hint", summary1)

            r2 = start_round(
                log_root=log_root,
                instance=instance,
                objective="Fix uncovered/collisions",
                parent_round_id=r1,
            )
            self.assertEqual("round_0002", r2)

            summary2 = close_round(
                log_root=log_root,
                round_id=r2,
                certificate=STEINER_S348_BLOCKS,
                techniques=["exact-certificate"],
                notes_text="# round 2 notes\n",
            )

            self.assertTrue(summary2["is_valid"])
            self.assertEqual(100.0, summary2["score"])
            self.assertEqual("new_best", summary2["advance_label"])

            brief_path = log_root / "rounds" / "NEXT_ROUND_BRIEF.md"
            index_path = log_root / "rounds" / "index.jsonl"
            round2_summary = log_root / "rounds" / "round_0002" / "round_summary.md"

            self.assertTrue(brief_path.exists())
            self.assertTrue(index_path.exists())
            self.assertTrue(round2_summary.exists())

            brief_text = brief_path.read_text(encoding="utf-8")
            self.assertIn("round_0002", brief_text)
            self.assertIn("Valid: True", brief_text)


if __name__ == "__main__":
    unittest.main()
