from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        return {}
    if payload is None:
        return {}
    return payload if isinstance(payload, dict) else {}


def _count_local_sources(papers_dir: Path) -> list[dict[str, Any]]:
    pdf_names = sorted([p.name.lower() for p in papers_dir.glob("*.pdf") if p.is_file()])
    specs: list[dict[str, Any]] = []
    if any("1401.3665" in name for name in pdf_names):
        specs.append(
            {
                "id": "keevash",
                "label": "Keevash (arxiv_1401.3665)",
                "aliases": ["1401.3665", "keevash"],
                "mechanisms": ["template", "spill", "robust fractional", "extendability", "absorber"],
            }
        )
    if any("1611.06827" in name for name in pdf_names):
        specs.append(
            {
                "id": "iter_absorption",
                "label": "Iterative absorption (arxiv_1611.06827)",
                "aliases": ["1611.06827", "iterative absorption", "glock"],
                "mechanisms": ["vortex", "cover down", "transformer", "regularity boosting", "absorber"],
            }
        )
    if any("oai_first_proof" in name for name in pdf_names):
        specs.append(
            {
                "id": "oai_first_proof",
                "label": "OpenAI first proof (oai_first_proof.pdf)",
                "aliases": ["oai_first_proof", "first proof", "openai first proof"],
                "mechanisms": ["seed ideas", "repeat up to 3", "verify", "gaps", "refinement", "typeset"],
            }
        )
    if any("roadmap" in name and "steiner" in name for name in pdf_names):
        specs.append(
            {
                "id": "roadmap",
                "label": "Steiner roadmap PDF",
                "aliases": ["roadmap", "steiner systems with strength", "n < 200"],
                "mechanisms": ["derivation", "nonexistence", "kramer", "orbit reduction", "sat", "ilp", "dlx"],
            }
        )
    return specs


def _has_explicit_mechanism(text: str, mechanisms: list[str]) -> bool:
    text_l = text.lower()
    normalized_text = re.sub(r"[^a-z0-9]+", " ", text_l)
    mechanism_hits = 0
    for token in mechanisms:
        token_norm = re.sub(r"[^a-z0-9]+", " ", token.lower()).strip()
        if token_norm and token_norm in normalized_text:
            mechanism_hits += 1
    has_structure_or_flow = any(
        token in text_l
        for token in (
            "phase",
            "stage",
            "pipeline",
            "closure",
            "repair",
            "reduction",
            "propagation",
            "scheduler",
            "route",
            "loop",
            "->",
            "=>",
            "⇒",
        )
    )
    return mechanism_hits >= 1 and (len(text.split()) >= 6 or has_structure_or_flow)


def _has_concrete_code_delta(text: str) -> bool:
    text_l = text.lower()
    has_path = bool(
        re.search(
            r"(run_steiner_loop\.sh|run_steiner_round\.sh|README\.md|STEINER_LOOP_LOGGING\.md|"
            r"math_proofs/[a-zA-Z0-9_./-]+|docs/[a-zA-Z0-9_./-]+|steiner_logs/[a-zA-Z0-9_./-]+)",
            text,
        )
    )
    has_action = any(
        token in text_l
        for token in (
            "add",
            "update",
            "modify",
            "enforce",
            "route",
            "replace",
            "refactor",
            "implement",
            "switch",
            "gate",
        )
    )
    has_change_hint = any(
        token in text_l
        for token in (
            "scheduler",
            "routing",
            "hook",
            "policy",
            "logging",
            "counter",
            "checkpoint",
            "metric",
            "gate",
            "stub",
            "pipeline",
            "stage",
        )
    )
    return has_path and (has_action or has_change_hint) and len(text.split()) >= 4


def _contains_instance(registry_rows: list[dict[str, Any]], instance_label: str) -> dict[str, Any] | None:
    for row in registry_rows:
        if not isinstance(row, dict):
            continue
        if str(row.get("instance", "")).strip() == instance_label:
            return row
    return None


def _verifier_review(
    *,
    docs_root: Path,
    run_round_dir: Path,
    run_id: str,
    round_num: int,
    round_id: str,
    mode: str,
) -> dict[str, Any]:
    findings: list[str] = []

    run_facts_path = run_round_dir / "RUN_FACTS.json"
    claim_deltas_path = run_round_dir / "CLAIM_DELTAS.yaml"
    hypothesis_deltas_path = run_round_dir / "HYPOTHESIS_DELTAS.yaml"
    source_transfer_deltas_path = run_round_dir / "SOURCE_TRANSFER_DELTAS.yaml"
    metrics_jsonl_path = docs_root / "generated" / "RUN_METRICS.jsonl"
    snapshot_path = docs_root / "generated" / "SNAPSHOT.md"

    required_paths = [
        run_facts_path,
        claim_deltas_path,
        hypothesis_deltas_path,
        source_transfer_deltas_path,
        metrics_jsonl_path,
        snapshot_path,
    ]
    for path in required_paths:
        if not path.exists():
            findings.append(f"Missing required artifact: {path}")

    run_facts = _read_json(run_facts_path)
    if run_facts:
        if run_facts.get("run_id") != run_id:
            findings.append("RUN_FACTS run_id mismatch.")
        if int(run_facts.get("round", -1)) != int(round_num):
            findings.append("RUN_FACTS round mismatch.")
        if run_facts.get("round_id") != round_id:
            findings.append("RUN_FACTS round_id mismatch.")
        if run_facts.get("mode") != mode:
            findings.append("RUN_FACTS mode mismatch.")

        metrics = run_facts.get("metrics")
        if not isinstance(metrics, dict):
            findings.append("RUN_FACTS metrics must be an object.")
            metrics = {}
        for field in (
            "score",
            "is_valid",
            "exact_once_r_subsets",
            "total_required_r_subsets",
            "uncovered_r_subsets",
            "overcovered_r_subsets",
        ):
            if field not in metrics:
                findings.append(f"RUN_FACTS metrics missing field: {field}")

    claim_rows = _read_yaml(claim_deltas_path).get("claims", [])
    if not isinstance(claim_rows, list) or len(claim_rows) < 1:
        findings.append("CLAIM_DELTAS.yaml must contain at least one claim entry.")

    hypothesis_rows = _read_yaml(hypothesis_deltas_path).get("hypotheses", [])
    if not isinstance(hypothesis_rows, list):
        findings.append("HYPOTHESIS_DELTAS.yaml hypotheses must be a list.")
        hypothesis_rows = []
    if mode == "research" and round_num == 1 and len(hypothesis_rows) < 1:
        findings.append("Round1 research requires at least one hypothesis delta entry.")

    source_rows = _read_yaml(source_transfer_deltas_path).get("entries", [])
    if not isinstance(source_rows, list):
        findings.append("SOURCE_TRANSFER_DELTAS.yaml entries must be a list.")
        source_rows = []
    if mode == "research" and round_num == 1 and len(source_rows) < 1:
        findings.append("Round1 research requires non-empty SOURCE_TRANSFER_DELTAS entries.")
    for idx, row in enumerate(source_rows, start=1):
        if not isinstance(row, dict):
            findings.append(f"SOURCE_TRANSFER_DELTAS entry {idx} must be an object.")
            continue
        if not str(row.get("source", "")).strip():
            findings.append(f"SOURCE_TRANSFER_DELTAS entry {idx} missing source.")
        if not str(row.get("theorem_or_mechanism", "")).strip():
            findings.append(f"SOURCE_TRANSFER_DELTAS entry {idx} missing theorem_or_mechanism.")
        if not str(row.get("code_delta", "")).strip():
            findings.append(f"SOURCE_TRANSFER_DELTAS entry {idx} missing code_delta.")

    metric_rows = []
    if metrics_jsonl_path.exists():
        for raw in metrics_jsonl_path.read_text(encoding="utf-8").splitlines():
            raw = raw.strip()
            if not raw:
                continue
            try:
                item = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if isinstance(item, dict):
                metric_rows.append(item)

    matched_metric = any(
        row.get("run_id") == run_id and int(row.get("round", -1)) == int(round_num) and row.get("mode") == mode
        for row in metric_rows
    )
    if not matched_metric:
        findings.append("RUN_METRICS.jsonl missing row for current run/round/mode.")

    return {
        "passed": len(findings) == 0,
        "findings": findings[:30],
        "metrics": {
            "claim_delta_entries": len(claim_rows) if isinstance(claim_rows, list) else 0,
            "hypothesis_delta_entries": len(hypothesis_rows) if isinstance(hypothesis_rows, list) else 0,
            "source_delta_entries": len(source_rows) if isinstance(source_rows, list) else 0,
            "metrics_rows_total": len(metric_rows),
        },
    }


def review_round(
    *,
    docs_root: Path,
    run_id: str,
    round_num: int,
    round_id: str,
    mode: str,
    notes_file: Path,
    research_paper_file: Path,
    papers_dir: Path,
) -> dict[str, Any]:
    run_round_dir = docs_root / "generated" / "runs" / f"run_{run_id}" / f"round_{round_num:04d}"

    run_facts = _read_json(run_round_dir / "RUN_FACTS.json")
    claim_deltas = _read_yaml(run_round_dir / "CLAIM_DELTAS.yaml")
    hypothesis_deltas = _read_yaml(run_round_dir / "HYPOTHESIS_DELTAS.yaml")
    source_transfer_deltas = _read_yaml(run_round_dir / "SOURCE_TRANSFER_DELTAS.yaml")

    registry = _read_yaml(docs_root / "instances" / "INSTANCE_REGISTRY.yaml")
    active_hyp = _read_yaml(docs_root / "knowledge" / "HYPOTHESES_ACTIVE.yaml")

    skeptic_findings: list[str] = []

    metrics = run_facts.get("metrics") if isinstance(run_facts, dict) else None
    if not isinstance(metrics, dict):
        skeptic_findings.append("RUN_FACTS metrics object is missing or invalid.")
        metrics = {}

    for field in (
        "score",
        "is_valid",
        "exact_once_r_subsets",
        "total_required_r_subsets",
        "uncovered_r_subsets",
        "overcovered_r_subsets",
    ):
        if field not in metrics:
            skeptic_findings.append(f"RUN_FACTS metrics missing required field '{field}'.")

    claims_rows = claim_deltas.get("claims", []) if isinstance(claim_deltas, dict) else []
    if not isinstance(claims_rows, list) or len(claims_rows) < 1:
        skeptic_findings.append("CLAIM_DELTAS.yaml must include at least one claim delta.")

    hyp_rows = hypothesis_deltas.get("hypotheses", []) if isinstance(hypothesis_deltas, dict) else []
    if not isinstance(hyp_rows, list):
        skeptic_findings.append("HYPOTHESIS_DELTAS.yaml must decode to a list.")
        hyp_rows = []

    if mode == "research" and round_num == 1 and len(hyp_rows) < 1:
        skeptic_findings.append("Round1 research review requires at least one hypothesis delta entry.")

    required_sources = _count_local_sources(papers_dir)
    source_rows = source_transfer_deltas.get("entries", []) if isinstance(source_transfer_deltas, dict) else []
    if not isinstance(source_rows, list):
        skeptic_findings.append("SOURCE_TRANSFER_DELTAS.yaml must decode to a list.")
        source_rows = []

    if mode == "research" and round_num == 1:
        if len(source_rows) < len(required_sources):
            skeptic_findings.append(
                f"Round1 research requires at least {len(required_sources)} source transfer delta rows (found {len(source_rows)})."
            )

        for spec in required_sources:
            aliases = [item.lower() for item in spec["aliases"]]
            mechanisms = [item.lower() for item in spec["mechanisms"]]
            matches = []
            for row in source_rows:
                if not isinstance(row, dict):
                    continue
                source_cell = str(row.get("source", "")).lower()
                if any(alias in source_cell for alias in aliases):
                    matches.append(row)

            if not matches:
                skeptic_findings.append(f"Missing source transfer delta row for {spec['label']}.")
                continue

            if not any(
                _has_explicit_mechanism(str(row.get("theorem_or_mechanism", "")), mechanisms)
                and _has_concrete_code_delta(str(row.get("code_delta", "")) )
                for row in matches
            ):
                skeptic_findings.append(
                    f"Source transfer delta row for {spec['label']} must include explicit mechanism and concrete code delta."
                )

    if not notes_file.exists():
        skeptic_findings.append(f"Round notes file missing: {notes_file}")

    if mode == "research" and round_num == 1 and not research_paper_file.exists():
        skeptic_findings.append(f"Research paper missing: {research_paper_file}")

    if mode == "research" and round_num == 1:
        active_rows = active_hyp.get("hypotheses", []) if isinstance(active_hyp, dict) else []
        if not isinstance(active_rows, list) or not (1 <= len(active_rows) <= 4):
            skeptic_findings.append("Canonical active hypotheses must have 1..4 items.")

    # Guard against solving instances that are already marked as provisional/proved nonexistence.
    instance_label = str(run_facts.get("instance_label", "")).strip()
    registry_rows = registry.get("registry", []) if isinstance(registry, dict) else []
    if isinstance(registry_rows, list) and instance_label and mode == "solve":
        reg_row = _contains_instance([row for row in registry_rows if isinstance(row, dict)], instance_label)
        if reg_row is not None:
            status = str(reg_row.get("status", ""))
            if status in {"provisional_nonexistence_veto", "proved_nonexistence"}:
                skeptic_findings.append(
                    f"Solve round targets {instance_label} but registry status is '{status}'; route should pivot before solver spend."
                )

    skeptic_pass = len(skeptic_findings) == 0

    verifier_payload = _verifier_review(
        docs_root=docs_root,
        run_round_dir=run_round_dir,
        run_id=run_id,
        round_num=round_num,
        round_id=round_id,
        mode=mode,
    )
    verifier_pass = bool(verifier_payload.get("passed", False))

    payload = {
        "passed": skeptic_pass and verifier_pass,
        "generated_utc": _utc_now_iso(),
        "run_id": run_id,
        "round": int(round_num),
        "round_id": round_id,
        "mode": mode,
        "reviewers": {
            "skeptic": {
                "passed": skeptic_pass,
                "finding_count": len(skeptic_findings),
                "findings": skeptic_findings[:30],
            },
            "verifier": {
                "passed": verifier_pass,
                "finding_count": len(verifier_payload.get("findings", [])),
                "findings": verifier_payload.get("findings", [])[:30],
                "metrics": verifier_payload.get("metrics", {}),
            },
        },
    }

    run_round_dir.mkdir(parents=True, exist_ok=True)
    review_json_path = run_round_dir / "AGENT_REVIEW.json"
    review_md_path = run_round_dir / "AGENT_REVIEW.md"
    review_json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Agent Review",
        "",
        f"Generated (UTC): {payload['generated_utc']}",
        f"Round: `{round_id}` mode=`{mode}`",
        f"Result: `{'PASS' if payload['passed'] else 'FAIL'}`",
        "",
        "## Skeptic",
        f"- Passed: `{skeptic_pass}`",
        f"- Findings: `{len(skeptic_findings)}`",
    ]
    for item in skeptic_findings[:10]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Verifier",
            f"- Passed: `{verifier_pass}`",
            f"- Findings: `{len(verifier_payload.get('findings', []))}`",
            f"- Source delta entries: `{verifier_payload.get('metrics', {}).get('source_delta_entries', '?')}`",
        ]
    )
    for item in verifier_payload.get("findings", [])[:10]:
        lines.append(f"- {item}")

    review_md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    payload["artifact_paths"] = {
        "json": str(review_json_path),
        "markdown": str(review_md_path),
    }
    return payload


def _cmd_review_round(args: argparse.Namespace) -> None:
    payload = review_round(
        docs_root=Path(args.docs_root),
        run_id=args.run_id,
        round_num=args.round,
        round_id=args.round_id,
        mode=args.mode,
        notes_file=Path(args.notes_file),
        research_paper_file=Path(args.research_paper_file),
        papers_dir=Path(args.papers_dir),
    )
    print(json.dumps(payload, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Multi-agent review for docs-first Steiner loop")
    sub = parser.add_subparsers(dest="cmd", required=True)

    round_parser = sub.add_parser("review-round", help="review one round using skeptic+verifier agents")
    round_parser.add_argument("--docs-root", default="docs")
    round_parser.add_argument("--run-id", required=True)
    round_parser.add_argument("--round", type=int, required=True)
    round_parser.add_argument("--round-id", required=True)
    round_parser.add_argument("--mode", choices=("research", "solve", "synthesis"), required=True)
    round_parser.add_argument("--notes-file", required=True)
    round_parser.add_argument("--research-paper-file", required=True)
    round_parser.add_argument("--papers-dir", default="papers")
    round_parser.set_defaults(func=_cmd_review_round)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
