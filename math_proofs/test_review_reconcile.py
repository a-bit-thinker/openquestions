from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from math_proofs.review_reconcile import reconcile_instance


class ReviewReconcileTests(unittest.TestCase):
    def test_replaces_blocked_solve_instance_with_frontier(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docs_root = Path(tmp) / "docs"
            instances_dir = docs_root / "instances"
            instances_dir.mkdir(parents=True, exist_ok=True)

            (instances_dir / "INSTANCE_REGISTRY.yaml").write_text(
                "\n".join(
                    [
                        "version: 1",
                        "registry:",
                        "  - instance: \"S(6,7,19)\"",
                        "    status: provisional_nonexistence_veto",
                        "  - instance: \"S(6,7,23)\"",
                        "    status: unknown_admissible_frontier",
                        "  - instance: \"S(7,8,24)\"",
                        "    status: unknown_admissible_frontier",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (instances_dir / "FRONTIER_QUEUE.yaml").write_text(
                "\n".join(
                    [
                        "version: 1",
                        "queue:",
                        "  - rank: 1",
                        "    instance: \"S(7,8,24)\"",
                        "  - rank: 2",
                        "    instance: \"S(6,7,23)\"",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            payload = reconcile_instance(
                docs_root=docs_root,
                instance={"n": 19, "q": 7, "r": 6},
                mode="solve",
                run_id="x",
                round_num=2,
                run_log_dir=None,
            )
            self.assertEqual(payload["decision"]["action"], "replace")
            self.assertEqual(payload["decision"]["replacement_label"], "S(6,7,23)")


if __name__ == "__main__":
    unittest.main()
