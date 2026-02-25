from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import yaml

from math_proofs.docs_gate import validate_round_docs


class DocsGateTests(unittest.TestCase):
    def _write_yaml(self, path: Path, payload: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    def _write_minimal_docs(self, root: Path, *, frontier_instance: str = "S(6,7,23)") -> tuple[Path, Path]:
        docs = root / "docs"
        papers = root / "papers"
        papers.mkdir(parents=True, exist_ok=True)

        # Trigger 4-source requirement.
        for name in (
            "arxiv_1401.3665.pdf",
            "arxiv_1611.06827.pdf",
            "oai_first_proof.pdf",
            "Computational and Theoretical Roadmap for Steiner Systems with Strength 6-9 and n _ 200.pdf",
        ):
            (papers / name).write_bytes(b"%PDF-1.4\n")

        round_dir = docs / "generated" / "runs" / "run_testrun" / "round_0001"
        round_dir.mkdir(parents=True, exist_ok=True)

        run_facts = {
            "run_id": "testrun",
            "round": 1,
            "round_id": "round_0001",
            "mode": "research",
            "metrics": {
                "score": 50.0,
                "is_valid": False,
                "exact_once_r_subsets": 10,
                "total_required_r_subsets": 100,
                "uncovered_r_subsets": 90,
                "overcovered_r_subsets": 0,
            },
        }
        (round_dir / "RUN_FACTS.json").write_text(json.dumps(run_facts), encoding="utf-8")

        self._write_yaml(
            round_dir / "CLAIM_DELTAS.yaml",
            {"version": 1, "claims": [{"statement": "A", "origin": "core_advance", "status": "observed"}]},
        )
        self._write_yaml(
            round_dir / "HYPOTHESIS_DELTAS.yaml",
            {"version": 1, "hypotheses": [{"statement": "B", "action": "observe"}]},
        )

        self._write_yaml(
            round_dir / "SOURCE_TRANSFER_DELTAS.yaml",
            {
                "version": 1,
                "entries": [
                    {
                        "source": "arxiv_1401.3665",
                        "theorem_or_mechanism": "Theorem mechanism template spill robust fractional extendability with absorber stage.",
                        "code_delta": "update math_proofs/steiner_exact_cover.py with template->spill->repair",
                        "validation_metric": "uncovered slope",
                    },
                    {
                        "source": "arxiv_1611.06827",
                        "theorem_or_mechanism": "Workflow mechanism vortex cover down transformer absorber and regularity boosting.",
                        "code_delta": "modify run_steiner_loop.sh to add vortex stage routing",
                        "validation_metric": "cover down hit rate",
                    },
                    {
                        "source": "oai_first_proof",
                        "theorem_or_mechanism": "Protocol mechanism seed ideas repeat up to 3 verify loops with gap checks and typeset closure.",
                        "code_delta": "enforce run_steiner_loop.sh round1 5 seeds and <=3 verify loops",
                        "validation_metric": "verification pass rate",
                    },
                    {
                        "source": "roadmap",
                        "theorem_or_mechanism": "Workflow mechanism derivation nonexistence plus kramer orbit reduction and sat ilp dlx routing.",
                        "code_delta": "update math_proofs/steiner_portfolio.py with derivation veto routing",
                        "validation_metric": "vetoed candidates",
                    },
                ],
            },
        )

        self._write_yaml(
            docs / "knowledge" / "SOURCE_TRANSFER.yaml",
            {
                "version": 1,
                "entries": [
                    {
                        "source_id": "arxiv_1401_3665",
                        "theorem_or_mechanism": "Theorem mechanism template spill robust fractional extendability with absorber phase.",
                        "code_delta": [{"file": "math_proofs/steiner_exact_cover.py", "action": "update", "detail": "update template spill repair stages"}],
                        "validation_metrics": ["uncovered_slope"],
                        "status": "active",
                    },
                    {
                        "source_id": "arxiv_1611_06827",
                        "theorem_or_mechanism": "Workflow mechanism vortex cover down transformer absorber transitions.",
                        "code_delta": [{"file": "run_steiner_loop.sh", "action": "modify", "detail": "modify vortex stage routing"}],
                        "validation_metrics": ["cover_down_hit_rate"],
                        "status": "active",
                    },
                    {
                        "source_id": "oai_first_proof",
                        "theorem_or_mechanism": "Protocol mechanism seed ideas repeat up to 3 verify loops with gaps and typeset closure.",
                        "code_delta": [{"file": "run_steiner_loop.sh", "action": "enforce", "detail": "enforce 5-seed and verify loop cap"}],
                        "validation_metrics": ["verification_pass_rate"],
                        "status": "active",
                    },
                    {
                        "source_id": "roadmap_n_lt_200",
                        "theorem_or_mechanism": "Workflow mechanism derivation nonexistence propagation and kramer orbit reduction plus sat ilp dlx routing.",
                        "code_delta": [{"file": "math_proofs/steiner_portfolio.py", "action": "update", "detail": "update derivation veto scheduling"}],
                        "validation_metrics": ["vetoed_candidates"],
                        "status": "active",
                    },
                ],
            },
        )

        self._write_yaml(docs / "knowledge" / "CLAIMS.yaml", {"version": 1, "claims": [{"claim_id": "C1", "status": "active", "statement": "Claim", "evidence_refs": ["a"]}]})
        self._write_yaml(
            docs / "knowledge" / "HYPOTHESES_ACTIVE.yaml",
            {
                "version": 1,
                "hypotheses": [
                    {
                        "hypothesis_id": "H1",
                        "statement": "Hypothesis",
                        "falsification_condition": "Reject on failed ablation",
                    }
                ],
            },
        )
        self._write_yaml(
            docs / "knowledge" / "HYPOTHESES_RETIRED.yaml",
            {
                "version": 1,
                "hypotheses": [
                    {
                        "retired_id": "R1",
                        "statement": "Old",
                        "retire_reason": "Invalidated",
                        "evidence_ref": "x",
                    }
                ],
            },
        )
        self._write_yaml(
            docs / "knowledge" / "NONEXISTENCE_CERTIFICATES.yaml",
            {
                "version": 1,
                "certificates": [
                    {
                        "certificate_id": "N1",
                        "base_instance": "S(4,5,17)",
                        "status": "provisional",
                        "source_refs": ["y"],
                        "propagation_rule": "derivation",
                    }
                ],
            },
        )

        self._write_yaml(
            docs / "instances" / "INSTANCE_REGISTRY.yaml",
            {
                "version": 1,
                "registry": [
                    {
                        "instance": "S(6,7,23)",
                        "status": "unknown_admissible_frontier",
                        "admissible": True,
                    }
                ],
            },
        )
        self._write_yaml(
            docs / "instances" / "FRONTIER_QUEUE.yaml",
            {
                "version": 1,
                "queue": [
                    {
                        "rank": 1,
                        "instance": frontier_instance,
                        "reason": "frontier",
                    }
                ],
            },
        )

        generated = docs / "generated"
        generated.mkdir(parents=True, exist_ok=True)
        (generated / "RUN_METRICS.jsonl").write_text(
            json.dumps({"run_id": "testrun", "round": 1, "mode": "research", "instance": "S(6,7,23)"}) + "\n",
            encoding="utf-8",
        )
        (generated / "SNAPSHOT.md").write_text("# snap\n", encoding="utf-8")

        return docs, papers

    def test_validate_round_docs_passes_for_consistent_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            docs, papers = self._write_minimal_docs(root)
            payload = validate_round_docs(
                docs_root=docs,
                run_id="testrun",
                round_num=1,
                round_id="round_0001",
                mode="research",
                papers_dir=papers,
            )
            self.assertTrue(payload["passed"], payload["reasons"])
            self.assertEqual(payload["validated_source_count"], payload["required_source_count"])

    def test_validate_round_docs_fails_on_frontier_registry_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            docs, papers = self._write_minimal_docs(root, frontier_instance="S(7,8,24)")
            payload = validate_round_docs(
                docs_root=docs,
                run_id="testrun",
                round_num=1,
                round_id="round_0001",
                mode="research",
                papers_dir=papers,
            )
            self.assertFalse(payload["passed"])
            joined = "\n".join(payload["reasons"])
            self.assertIn("missing from instance registry", joined)


if __name__ == "__main__":
    unittest.main()
