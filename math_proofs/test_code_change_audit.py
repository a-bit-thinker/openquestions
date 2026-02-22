from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from math_proofs.code_change_audit import build_diff_event, write_snapshot


class CodeChangeAuditTests(unittest.TestCase):
    def test_modified_file_is_reported_with_line_delta(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            target = repo / "run_steiner_loop.sh"
            target.write_text("#!/bin/bash\necho one\n", encoding="utf-8")

            before_path = repo / "before.json"
            write_snapshot(repo, before_path)

            target.write_text("#!/bin/bash\necho one\necho two\n", encoding="utf-8")
            after_path = repo / "after.json"
            write_snapshot(repo, after_path)

            before = json.loads(before_path.read_text(encoding="utf-8"))
            after = json.loads(after_path.read_text(encoding="utf-8"))
            payload = build_diff_event(
                before_snapshot=before,
                after_snapshot=after,
                run_id="r1",
                round_num=2,
                round_id="round_0002",
                mode="solve",
            )

            self.assertEqual(payload["change_count"], 1)
            self.assertEqual(payload["changes"][0]["path"], "run_steiner_loop.sh")
            self.assertEqual(payload["changes"][0]["kind"], "modified")
            self.assertEqual(payload["changes"][0]["line_delta"], 1)

    def test_added_and_deleted_files_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            file_a = repo / "run_steiner_round.sh"
            file_a.write_text("echo start\n", encoding="utf-8")
            docs_dir = repo / "docs"
            docs_dir.mkdir(parents=True, exist_ok=True)

            before_path = repo / "before.json"
            write_snapshot(repo, before_path)

            file_a.unlink()
            (docs_dir / "new.md").write_text("# hello\n", encoding="utf-8")
            after_path = repo / "after.json"
            write_snapshot(repo, after_path)

            before = json.loads(before_path.read_text(encoding="utf-8"))
            after = json.loads(after_path.read_text(encoding="utf-8"))
            payload = build_diff_event(
                before_snapshot=before,
                after_snapshot=after,
                run_id="r2",
                round_num=3,
                round_id="round_0003",
                mode="research",
            )

            kinds = {row["path"]: row["kind"] for row in payload["changes"]}
            self.assertEqual(kinds["run_steiner_round.sh"], "deleted")
            self.assertEqual(kinds["docs/new.md"], "added")


if __name__ == "__main__":
    unittest.main()
