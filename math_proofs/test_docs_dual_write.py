from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from math_proofs.docs_dual_write import write_round_artifacts


def _sample_notes() -> str:
    return """# round_0001 notes

## Core advance
- Converted derivation-veto into a scheduling pre-gate.

## Observations
- Strict feasibility metrics are stable under bounded runtime.

## Next-hypothesis
- Verify base nonexistence sources and promote certificate status.

## Paper-to-loop method extraction
| Source PDF | Theorem/Mechanism (explicit) | Code Delta Mapping (file:path + action) | Validation Metric |
|---|---|---|---|
| arxiv_1401.3665 | Theorem mechanism: template + spill + absorber closure. | update `math_proofs/steiner_exact_cover.py` with template->spill->repair stages. | uncovered slope |
| oai_first_proof | Protocol mechanism: seed ideas fanout and <=3 verify loops. | enforce `run_steiner_loop.sh` 5-seed round1 loop. | verification pass rate |
"""


class DocsDualWriteTests(unittest.TestCase):
    def test_write_round_artifacts_creates_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            docs_root = tmp_path / "docs"
            notes_file = tmp_path / "round_0001_notes.md"
            notes_file.write_text(_sample_notes(), encoding="utf-8")

            paths = write_round_artifacts(
                docs_root=docs_root,
                run_id="20260222_130000",
                run_log_dir="steiner_logs/run_20260222_130000",
                round_num=1,
                round_id="round_0001",
                mode="research",
                instance_label="S(6,7,23)",
                instance_json={"n": 23, "q": 7, "r": 6},
                round_metrics={
                    "score": 50.12,
                    "is_valid": False,
                    "exact_once_r_subsets": 64931,
                    "total_required_r_subsets": 100947,
                    "uncovered_r_subsets": 36016,
                    "overcovered_r_subsets": 0,
                },
                notes_file=notes_file,
                paper_gate={
                    "passed": True,
                    "quality_score": 100,
                    "validated_source_count": 4,
                    "required_source_count": 4,
                },
                techniques=["research-cache"],
            )

            run_facts_path = Path(paths["run_facts"])
            claim_path = Path(paths["claim_deltas"])
            hypothesis_path = Path(paths["hypothesis_deltas"])
            transfer_path = Path(paths["source_transfer_deltas"])
            metrics_path = Path(paths["metrics_jsonl"])
            snapshot_path = Path(paths["snapshot"])

            self.assertTrue(run_facts_path.exists())
            self.assertTrue(claim_path.exists())
            self.assertTrue(hypothesis_path.exists())
            self.assertTrue(transfer_path.exists())
            self.assertTrue(metrics_path.exists())
            self.assertTrue(snapshot_path.exists())

            run_facts = json.loads(run_facts_path.read_text(encoding="utf-8"))
            self.assertEqual(run_facts["run_id"], "20260222_130000")
            self.assertEqual(run_facts["mode"], "research")
            self.assertEqual(run_facts["instance_label"], "S(6,7,23)")
            self.assertTrue(run_facts["paper_gate"]["passed"])

            claim_text = claim_path.read_text(encoding="utf-8")
            self.assertIn("core_advance", claim_text)
            self.assertIn("derivation-veto", claim_text)

            transfer_text = transfer_path.read_text(encoding="utf-8")
            self.assertIn("arxiv_1401.3665", transfer_text)
            self.assertIn("math_proofs/steiner_exact_cover.py", transfer_text)

    def test_write_round_artifacts_dedupes_metrics_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            docs_root = tmp_path / "docs"
            notes_file = tmp_path / "round_0002_notes.md"
            notes_file.write_text("## Core advance\n- A\n", encoding="utf-8")

            kwargs = dict(
                docs_root=docs_root,
                run_id="20260222_130001",
                run_log_dir="steiner_logs/run_20260222_130001",
                round_num=2,
                round_id="round_0002",
                mode="solve",
                instance_label="S(7,8,24)",
                instance_json={"n": 24, "q": 8, "r": 7},
                notes_file=notes_file,
                paper_gate=None,
                techniques=["solve-r7-round-2"],
            )

            write_round_artifacts(
                round_metrics={
                    "score": 10.0,
                    "is_valid": False,
                    "exact_once_r_subsets": 100,
                    "total_required_r_subsets": 346104,
                    "uncovered_r_subsets": 346004,
                    "overcovered_r_subsets": 0,
                },
                **kwargs,
            )
            write_round_artifacts(
                round_metrics={
                    "score": 11.0,
                    "is_valid": False,
                    "exact_once_r_subsets": 150,
                    "total_required_r_subsets": 346104,
                    "uncovered_r_subsets": 345954,
                    "overcovered_r_subsets": 0,
                },
                **kwargs,
            )

            metrics_path = docs_root / "generated" / "RUN_METRICS.jsonl"
            rows = [
                json.loads(line)
                for line in metrics_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]

            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["score"], 11.0)
            self.assertEqual(rows[0]["round"], 2)


if __name__ == "__main__":
    unittest.main()
