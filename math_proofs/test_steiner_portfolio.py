import tempfile
import unittest
from pathlib import Path

from math_proofs.steiner_portfolio import (
    build_observed_stats,
    generate_existence_report,
    select_instance_for_r,
)


def _write_summary(path: Path, rows: list[str]) -> None:
    text = "\n".join(
        [
            "# Run Summary",
            "",
            "| Round | Mode | Instance | Score | Valid | Exact Once | Uncovered | Overcovered | Notes |",
            "|---:|---|---|---:|---|---|---:|---:|---|",
            *rows,
            "",
        ]
    )
    path.write_text(text, encoding="utf-8")


class SteinerPortfolioTests(unittest.TestCase):
    def test_build_observed_stats_parses_solve_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_dir = root / "run_20260101_000000"
            run_dir.mkdir(parents=True)
            _write_summary(
                run_dir / "RUN_SUMMARY.md",
                [
                    "| 1 | research | S(6,7,17) | 0 | false | 0/12376 | 12376 | 0 | cache-build |",
                    "| 2 | solve | S(6,7,17) | 48.37 | false | 7812/12376 | 4564 | 0 | r=6 |",
                    "| 3 | solve | S(6,7,17) | 100 | true | 12376/12376 | 0 | 0 | solved |",
                ],
            )

            observed = build_observed_stats(root)
            stats = observed[(17, 7, 6)]
            self.assertEqual(2, stats.attempts)
            self.assertEqual(100.0, stats.best_score)
            self.assertEqual(1.0, stats.best_coverage)
            self.assertTrue(stats.is_solved)

    def test_select_instance_for_r_skips_solved_instances(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_dir = root / "run_20260101_000000"
            run_dir.mkdir(parents=True)
            _write_summary(
                run_dir / "RUN_SUMMARY.md",
                [
                    "| 2 | solve | S(6,7,17) | 100 | true | 12376/12376 | 0 | 0 | solved |",
                ],
            )

            pick = select_instance_for_r(
                r=6,
                log_root=root,
                mode="portfolio",
                min_expected_blocks=1000,
                max_expected_blocks=10000,
            )
            self.assertEqual(6, pick["r"])
            self.assertNotEqual((17, 7, 6), (pick["n"], pick["q"], pick["r"]))

    def test_generate_existence_report_writes_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_dir = root / "run_20260101_000000"
            run_dir.mkdir(parents=True)
            _write_summary(
                run_dir / "RUN_SUMMARY.md",
                [
                    "| 2 | solve | S(6,7,17) | 48.37 | false | 7812/12376 | 4564 | 0 | r=6 |",
                ],
            )

            out = root / "EXISTENCE_FRONTIER.md"
            generate_existence_report(
                log_root=root,
                output_file=out,
                r_min=6,
                r_max=6,
                n_max=25,
                top_k=5,
                min_expected_blocks=1000,
                max_expected_blocks=10000,
            )

            text = out.read_text(encoding="utf-8")
            self.assertIn("# Existence Frontier Report", text)
            self.assertIn("impossible_divisibility", text)
            self.assertIn("unknown", text)


if __name__ == "__main__":
    unittest.main()
