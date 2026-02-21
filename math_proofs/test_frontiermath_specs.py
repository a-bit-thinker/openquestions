import csv
import pathlib
import unittest


class FrontierMathSpecsTests(unittest.TestCase):
    def setUp(self):
        self.spec_dir = pathlib.Path(__file__).resolve().parent / "frontiermath_specs"
        self.scores_csv = self.spec_dir / "scores.csv"

    def test_has_exactly_14_problem_specs(self):
        spec_files = sorted(
            p.name
            for p in self.spec_dir.glob("*.md")
            if p.name not in {"README.md", "SCORES.md"}
        )
        self.assertEqual(14, len(spec_files))

    def test_scores_csv_consistency(self):
        self.assertTrue(self.scores_csv.exists())

        with self.scores_csv.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

        self.assertEqual(14, len(rows))

        seen_ranks = set()
        seen_files = set()
        previous_score = None

        for i, row in enumerate(rows, start=1):
            rank = int(row["rank"])
            score = float(row["score"])
            filename = row["file"]

            self.assertEqual(i, rank)
            self.assertNotIn(rank, seen_ranks)
            self.assertNotIn(filename, seen_files)

            seen_ranks.add(rank)
            seen_files.add(filename)

            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 10.0)

            spec_path = self.spec_dir / filename
            self.assertTrue(spec_path.exists(), msg=f"Missing spec file listed in CSV: {filename}")

            text = spec_path.read_text(encoding="utf-8")
            self.assertIn("Iterative proof likelihood score:", text)
            self.assertIn("Reason:", text)

            if previous_score is not None:
                self.assertLessEqual(score, previous_score)
            previous_score = score


if __name__ == "__main__":
    unittest.main()
