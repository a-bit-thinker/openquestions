from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import yaml

from math_proofs.agent_review import review_round


class AgentReviewTests(unittest.TestCase):
    def _write_yaml(self, path: Path, payload: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    def _bootstrap_docs(self, root: Path) -> tuple[Path, Path, Path, Path]:
        docs = root / "docs"
        papers = root / "papers"
        papers.mkdir(parents=True, exist_ok=True)

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
            "instance_label": "S(6,7,23)",
            "metrics": {
                "score": 12.3,
                "is_valid": False,
                "exact_once_r_subsets": 100,
                "total_required_r_subsets": 100947,
                "uncovered_r_subsets": 100847,
                "overcovered_r_subsets": 0,
            },
        }
        (round_dir / "RUN_FACTS.json").write_text(json.dumps(run_facts), encoding="utf-8")

        self._write_yaml(
            round_dir / "CLAIM_DELTAS.yaml",
            {
                "version": 1,
                "claims": [{"statement": "Derivation veto reduced frontier noise", "origin": "core_advance", "status": "observed"}],
            },
        )
        self._write_yaml(
            round_dir / "HYPOTHESIS_DELTAS.yaml",
            {
                "version": 1,
                "hypotheses": [{"statement": "Verify base nonexistence first", "origin": "next_hypothesis", "action": "observe"}],
            },
        )
        self._write_yaml(
            round_dir / "SOURCE_TRANSFER_DELTAS.yaml",
            {
                "version": 1,
                "entries": [
                    {
                        "source": "arxiv_1401.3665",
                        "theorem_or_mechanism": "Theorem mechanism template spill robust fractional extendability with absorber closure.",
                        "code_delta": "update math_proofs/steiner_exact_cover.py with template spill repair stages",
                        "validation_metric": "uncovered_slope",
                    },
                    {
                        "source": "arxiv_1611.06827",
                        "theorem_or_mechanism": "Workflow mechanism vortex cover down transformer absorber and regularity boosting.",
                        "code_delta": "modify run_steiner_loop.sh to add vortex schedule gate",
                        "validation_metric": "cover_down_hit_rate",
                    },
                    {
                        "source": "oai_first_proof",
                        "theorem_or_mechanism": "Protocol mechanism seed ideas repeat up to 3 verify loops with gap checks and typeset closure.",
                        "code_delta": "enforce run_steiner_loop.sh 5 seed round1 and <=3 verify loops",
                        "validation_metric": "verification_pass_rate",
                    },
                    {
                        "source": "roadmap",
                        "theorem_or_mechanism": "Workflow mechanism derivation nonexistence propagation plus kramer orbit reduction and sat ilp dlx routing.",
                        "code_delta": "update math_proofs/steiner_portfolio.py with derivation veto routing",
                        "validation_metric": "vetoed_candidates",
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
                        "theorem_or_mechanism": "Theorem mechanism template spill robust fractional extendability with absorber closure.",
                        "code_delta": [{"file": "math_proofs/steiner_exact_cover.py", "action": "update", "detail": "update template spill repair stages"}],
                        "validation_metrics": ["uncovered_slope"],
                        "status": "active",
                    },
                    {
                        "source_id": "arxiv_1611_06827",
                        "theorem_or_mechanism": "Workflow mechanism vortex cover down transformer absorber transitions.",
                        "code_delta": [{"file": "run_steiner_loop.sh", "action": "modify", "detail": "modify vortex level scheduler"}],
                        "validation_metrics": ["cover_down_hit_rate"],
                        "status": "active",
                    },
                    {
                        "source_id": "oai_first_proof",
                        "theorem_or_mechanism": "Protocol mechanism seed ideas repeat up to 3 verify loops with gaps and typeset closure.",
                        "code_delta": [{"file": "run_steiner_loop.sh", "action": "enforce", "detail": "enforce 5 seeds and verify loop cap"}],
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
            {"version": 1, "hypotheses": [{"hypothesis_id": "H1", "statement": "Hypothesis", "falsification_condition": "Reject if no improvement"}]},
        )
        self._write_yaml(
            docs / "knowledge" / "HYPOTHESES_RETIRED.yaml",
            {"version": 1, "hypotheses": [{"retired_id": "R1", "statement": "Old", "retire_reason": "invalid", "evidence_ref": "x"}]},
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
                        "source_refs": ["x"],
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
                "queue": [{"rank": 1, "instance": "S(6,7,23)", "reason": "frontier"}],
            },
        )

        generated = docs / "generated"
        generated.mkdir(parents=True, exist_ok=True)
        (generated / "RUN_METRICS.jsonl").write_text(
            json.dumps({"run_id": "testrun", "round": 1, "mode": "research", "instance": "S(6,7,23)"}) + "\n",
            encoding="utf-8",
        )
        (generated / "SNAPSHOT.md").write_text("# snapshot\n", encoding="utf-8")

        notes_file = root / "round_0001_notes.md"
        notes_file.write_text("# notes\n", encoding="utf-8")
        paper_file = root / "RESEARCH_PAPER.md"
        paper_file.write_text("# paper\n", encoding="utf-8")

        return docs, papers, notes_file, paper_file

    def test_review_round_passes_with_consistent_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            docs, papers, notes_file, paper_file = self._bootstrap_docs(root)
            payload = review_round(
                docs_root=docs,
                run_id="testrun",
                round_num=1,
                round_id="round_0001",
                mode="research",
                notes_file=notes_file,
                research_paper_file=paper_file,
                papers_dir=papers,
            )
            self.assertTrue(payload["passed"], payload)
            self.assertTrue(payload["reviewers"]["skeptic"]["passed"])
            self.assertTrue(payload["reviewers"]["verifier"]["passed"])

    def test_review_round_fails_when_source_transfer_deltas_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            docs, papers, notes_file, paper_file = self._bootstrap_docs(root)
            (docs / "generated" / "runs" / "run_testrun" / "round_0001" / "SOURCE_TRANSFER_DELTAS.yaml").write_text(
                "version: 1\nentries: []\n",
                encoding="utf-8",
            )
            payload = review_round(
                docs_root=docs,
                run_id="testrun",
                round_num=1,
                round_id="round_0001",
                mode="research",
                notes_file=notes_file,
                research_paper_file=paper_file,
                papers_dir=papers,
            )
            self.assertFalse(payload["passed"])
            self.assertFalse(payload["reviewers"]["skeptic"]["passed"])


if __name__ == "__main__":
    unittest.main()
