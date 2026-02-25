from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


ALLOWED_CODE_ACTIONS = {
    "add",
    "update",
    "modify",
    "enforce",
    "route",
    "replace",
    "refactor",
}

ALLOWED_INSTANCE_STATUS = {
    "impossible_divisibility",
    "proved_nonexistence",
    "provisional_nonexistence_veto",
    "unknown_admissible_frontier",
    "unknown_admissible",
    "proved_existence",
}

ALLOWED_CERT_STATUS = {"provisional", "verified", "retracted"}


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _count_local_sources(papers_dir: Path) -> list[dict[str, Any]]:
    pdf_names = sorted([p.name.lower() for p in papers_dir.glob("*.pdf") if p.is_file()])
    specs: list[dict[str, Any]] = []

    if any("1401.3665" in name for name in pdf_names):
        specs.append(
            {
                "id": "arxiv_1401_3665",
                "label": "Keevash (arxiv_1401.3665)",
                "aliases": ["1401.3665", "keevash"],
                "mechanisms": ["template", "spill", "robust fractional", "extendability", "absorber"],
            }
        )
    if any("1611.06827" in name for name in pdf_names):
        specs.append(
            {
                "id": "arxiv_1611_06827",
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
                "aliases": ["oai_first_proof", "openai first proof", "first proof"],
                "mechanisms": ["seed ideas", "repeat up to 3", "verify", "gaps", "refinement", "typeset"],
            }
        )
    if any("roadmap" in name and "steiner" in name for name in pdf_names):
        specs.append(
            {
                "id": "roadmap_n_lt_200",
                "label": "Steiner roadmap PDF",
                "aliases": ["roadmap", "steiner systems with strength", "n < 200"],
                "mechanisms": ["derivation", "nonexistence", "kramer", "orbit reduction", "sat", "ilp", "dlx"],
            }
        )
    return specs


def _row_has_explicit_mechanism(text: str, mechanism_tokens: list[str]) -> bool:
    text_l = text.lower()
    normalized_text = re.sub(r"[^a-z0-9]+", " ", text_l)
    mechanism_hits = 0
    for token in mechanism_tokens:
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


def _row_has_code_delta(text: str) -> bool:
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
            "switch",
            "route",
            "implement",
            "inject",
            "gate",
            "replace",
            "rewrite",
            "refactor",
            "tune",
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


def _ensure_file(path: Path, reasons: list[str]) -> None:
    if not path.exists():
        reasons.append(f"Missing required artifact: {path}")


def validate_round_docs(
    *,
    docs_root: Path,
    run_id: str,
    round_num: int,
    round_id: str,
    mode: str,
    papers_dir: Path,
) -> dict[str, Any]:
    reasons: list[str] = []

    run_round_dir = docs_root / "generated" / "runs" / f"run_{run_id}" / f"round_{round_num:04d}"
    run_facts_path = run_round_dir / "RUN_FACTS.json"
    claim_deltas_path = run_round_dir / "CLAIM_DELTAS.yaml"
    hypothesis_deltas_path = run_round_dir / "HYPOTHESIS_DELTAS.yaml"
    source_transfer_deltas_path = run_round_dir / "SOURCE_TRANSFER_DELTAS.yaml"

    required_paths = [
        run_facts_path,
        claim_deltas_path,
        hypothesis_deltas_path,
        source_transfer_deltas_path,
        docs_root / "knowledge" / "SOURCE_TRANSFER.yaml",
        docs_root / "knowledge" / "CLAIMS.yaml",
        docs_root / "knowledge" / "HYPOTHESES_ACTIVE.yaml",
        docs_root / "knowledge" / "HYPOTHESES_RETIRED.yaml",
        docs_root / "knowledge" / "NONEXISTENCE_CERTIFICATES.yaml",
        docs_root / "instances" / "INSTANCE_REGISTRY.yaml",
        docs_root / "instances" / "FRONTIER_QUEUE.yaml",
        docs_root / "generated" / "RUN_METRICS.jsonl",
        docs_root / "generated" / "SNAPSHOT.md",
    ]
    for path in required_paths:
        _ensure_file(path, reasons)

    run_facts: dict[str, Any] = {}
    claim_deltas: dict[str, Any] = {}
    hypothesis_deltas: dict[str, Any] = {}
    source_transfer_deltas: dict[str, Any] = {}
    source_transfer: dict[str, Any] = {}
    claims: dict[str, Any] = {}
    active_hyp: dict[str, Any] = {}
    retired_hyp: dict[str, Any] = {}
    certs: dict[str, Any] = {}
    registry: dict[str, Any] = {}
    frontier: dict[str, Any] = {}

    try:
        if run_facts_path.exists():
            run_facts = _read_json(run_facts_path)
    except Exception as exc:  # pragma: no cover - defensive
        reasons.append(f"Failed parsing RUN_FACTS.json: {exc}")

    for path, target_name in (
        (claim_deltas_path, "claim_deltas"),
        (hypothesis_deltas_path, "hypothesis_deltas"),
        (source_transfer_deltas_path, "source_transfer_deltas"),
        (docs_root / "knowledge" / "SOURCE_TRANSFER.yaml", "source_transfer"),
        (docs_root / "knowledge" / "CLAIMS.yaml", "claims"),
        (docs_root / "knowledge" / "HYPOTHESES_ACTIVE.yaml", "active_hyp"),
        (docs_root / "knowledge" / "HYPOTHESES_RETIRED.yaml", "retired_hyp"),
        (docs_root / "knowledge" / "NONEXISTENCE_CERTIFICATES.yaml", "certs"),
        (docs_root / "instances" / "INSTANCE_REGISTRY.yaml", "registry"),
        (docs_root / "instances" / "FRONTIER_QUEUE.yaml", "frontier"),
    ):
        try:
            if path.exists():
                parsed = _read_yaml(path)
                if parsed is None:
                    parsed = {}
                if not isinstance(parsed, dict):
                    reasons.append(f"{path} must decode to a YAML mapping.")
                    parsed = {}
                if target_name == "claim_deltas":
                    claim_deltas = parsed
                elif target_name == "hypothesis_deltas":
                    hypothesis_deltas = parsed
                elif target_name == "source_transfer_deltas":
                    source_transfer_deltas = parsed
                elif target_name == "source_transfer":
                    source_transfer = parsed
                elif target_name == "claims":
                    claims = parsed
                elif target_name == "active_hyp":
                    active_hyp = parsed
                elif target_name == "retired_hyp":
                    retired_hyp = parsed
                elif target_name == "certs":
                    certs = parsed
                elif target_name == "registry":
                    registry = parsed
                elif target_name == "frontier":
                    frontier = parsed
        except Exception as exc:
            reasons.append(f"Failed parsing {path}: {exc}")

    if run_facts:
        if run_facts.get("run_id") != run_id:
            reasons.append("RUN_FACTS run_id mismatch.")
        if int(run_facts.get("round", -1)) != int(round_num):
            reasons.append("RUN_FACTS round mismatch.")
        if run_facts.get("round_id") != round_id:
            reasons.append("RUN_FACTS round_id mismatch.")
        if run_facts.get("mode") != mode:
            reasons.append("RUN_FACTS mode mismatch.")

        metrics = run_facts.get("metrics")
        if not isinstance(metrics, dict):
            reasons.append("RUN_FACTS metrics must be an object.")
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
                reasons.append(f"RUN_FACTS metrics missing field: {field}")

    claim_rows = claims.get("claims", []) if isinstance(claims, dict) else []
    if not isinstance(claim_rows, list):
        reasons.append("CLAIMS.yaml 'claims' must be a list.")
        claim_rows = []
    if len(claim_rows) < 1:
        reasons.append("CLAIMS.yaml must contain at least one claim.")

    active_rows = active_hyp.get("hypotheses", []) if isinstance(active_hyp, dict) else []
    if not isinstance(active_rows, list):
        reasons.append("HYPOTHESES_ACTIVE.yaml 'hypotheses' must be a list.")
        active_rows = []
    if not (1 <= len(active_rows) <= 4):
        reasons.append(f"Active hypotheses must have 1..4 items (found {len(active_rows)}).")
    for idx, row in enumerate(active_rows, start=1):
        if not isinstance(row, dict):
            reasons.append(f"Active hypothesis {idx} must be an object.")
            continue
        if not str(row.get("statement", "")).strip():
            reasons.append(f"Active hypothesis {idx} missing statement.")
        if not str(row.get("falsification_condition", "")).strip():
            reasons.append(f"Active hypothesis {idx} missing falsification_condition.")

    retired_rows = retired_hyp.get("hypotheses", []) if isinstance(retired_hyp, dict) else []
    if not isinstance(retired_rows, list):
        reasons.append("HYPOTHESES_RETIRED.yaml 'hypotheses' must be a list.")
        retired_rows = []
    if len(retired_rows) < 1:
        reasons.append("HYPOTHESES_RETIRED.yaml must include at least one retired item.")
    for idx, row in enumerate(retired_rows, start=1):
        if not isinstance(row, dict):
            reasons.append(f"Retired hypothesis {idx} must be an object.")
            continue
        if not str(row.get("retire_reason", "")).strip():
            reasons.append(f"Retired hypothesis {idx} missing retire_reason.")
        if not str(row.get("evidence_ref", "")).strip():
            reasons.append(f"Retired hypothesis {idx} missing evidence_ref.")

    transfer_entries = source_transfer.get("entries", []) if isinstance(source_transfer, dict) else []
    if not isinstance(transfer_entries, list):
        reasons.append("SOURCE_TRANSFER.yaml 'entries' must be a list.")
        transfer_entries = []
    if len(transfer_entries) < 1:
        reasons.append("SOURCE_TRANSFER.yaml must contain at least one entry.")

    transfer_map: dict[str, list[dict[str, Any]]] = {}
    for idx, row in enumerate(transfer_entries, start=1):
        if not isinstance(row, dict):
            reasons.append(f"SOURCE_TRANSFER entry {idx} must be an object.")
            continue
        sid = str(row.get("source_id", "")).strip()
        if not sid:
            reasons.append(f"SOURCE_TRANSFER entry {idx} missing source_id.")
            continue
        transfer_map.setdefault(sid, []).append(row)

        mechanism = str(row.get("theorem_or_mechanism", "")).strip()
        if len(mechanism.split()) < 6:
            reasons.append(f"SOURCE_TRANSFER entry {sid} mechanism statement too short.")

        deltas = row.get("code_delta", [])
        if not isinstance(deltas, list) or not deltas:
            reasons.append(f"SOURCE_TRANSFER entry {sid} missing code_delta list.")
            deltas = []
        for didx, delta in enumerate(deltas, start=1):
            if not isinstance(delta, dict):
                reasons.append(f"SOURCE_TRANSFER entry {sid} code_delta {didx} must be object.")
                continue
            file_path = str(delta.get("file", "")).strip()
            action = str(delta.get("action", "")).strip().lower()
            detail = str(delta.get("detail", "")).strip()
            if not file_path:
                reasons.append(f"SOURCE_TRANSFER entry {sid} code_delta {didx} missing file.")
            if action not in ALLOWED_CODE_ACTIONS:
                reasons.append(
                    f"SOURCE_TRANSFER entry {sid} code_delta {didx} action must be one of {sorted(ALLOWED_CODE_ACTIONS)}."
                )
            if len(detail.split()) < 3:
                reasons.append(f"SOURCE_TRANSFER entry {sid} code_delta {didx} detail too short.")

        metrics = row.get("validation_metrics", [])
        if not isinstance(metrics, list) or not metrics:
            reasons.append(f"SOURCE_TRANSFER entry {sid} missing validation_metrics.")

    cert_rows = certs.get("certificates", []) if isinstance(certs, dict) else []
    if not isinstance(cert_rows, list):
        reasons.append("NONEXISTENCE_CERTIFICATES.yaml 'certificates' must be a list.")
        cert_rows = []
    for idx, row in enumerate(cert_rows, start=1):
        if not isinstance(row, dict):
            reasons.append(f"Certificate {idx} must be an object.")
            continue
        status = str(row.get("status", "")).strip()
        if status not in ALLOWED_CERT_STATUS:
            reasons.append(f"Certificate {idx} has invalid status '{status}'.")

    registry_rows = registry.get("registry", []) if isinstance(registry, dict) else []
    if not isinstance(registry_rows, list):
        reasons.append("INSTANCE_REGISTRY.yaml 'registry' must be a list.")
        registry_rows = []

    instance_set: set[str] = set()
    for idx, row in enumerate(registry_rows, start=1):
        if not isinstance(row, dict):
            reasons.append(f"Registry row {idx} must be an object.")
            continue
        instance = str(row.get("instance", "")).strip()
        status = str(row.get("status", "")).strip()
        if not instance:
            reasons.append(f"Registry row {idx} missing instance.")
        else:
            instance_set.add(instance)
        if status not in ALLOWED_INSTANCE_STATUS:
            reasons.append(f"Registry row {idx} has invalid status '{status}'.")

    frontier_rows = frontier.get("queue", []) if isinstance(frontier, dict) else []
    if not isinstance(frontier_rows, list):
        reasons.append("FRONTIER_QUEUE.yaml 'queue' must be a list.")
        frontier_rows = []

    seen_ranks: set[int] = set()
    for idx, row in enumerate(frontier_rows, start=1):
        if not isinstance(row, dict):
            reasons.append(f"Frontier row {idx} must be an object.")
            continue
        instance = str(row.get("instance", "")).strip()
        rank = row.get("rank")
        if not isinstance(rank, int) or rank < 1:
            reasons.append(f"Frontier row {idx} has invalid rank '{rank}'.")
        elif rank in seen_ranks:
            reasons.append(f"Frontier rank collision at rank {rank}.")
        else:
            seen_ranks.add(rank)
        if instance and instance not in instance_set:
            reasons.append(f"Frontier instance '{instance}' missing from instance registry.")

    # Validate source coverage from local PDFs.
    required_specs = _count_local_sources(papers_dir)

    source_delta_rows = source_transfer_deltas.get("entries", []) if isinstance(source_transfer_deltas, dict) else []
    if not isinstance(source_delta_rows, list):
        reasons.append("SOURCE_TRANSFER_DELTAS.yaml 'entries' must be a list.")
        source_delta_rows = []

    validated_sources: list[str] = []
    for spec in required_specs:
        sid = spec["id"]
        aliases = [a.lower() for a in spec["aliases"]]
        mechanisms = [m.lower() for m in spec["mechanisms"]]

        canonical_matches = transfer_map.get(sid, [])
        if not canonical_matches:
            reasons.append(f"Canonical SOURCE_TRANSFER missing entry for {spec['label']}.")
            continue

        if not any(
            _row_has_explicit_mechanism(str(row.get("theorem_or_mechanism", "")), mechanisms)
            and any(_row_has_code_delta(str(delta.get("file", "")) + " " + str(delta.get("action", "")) + " " + str(delta.get("detail", ""))) for delta in row.get("code_delta", []) if isinstance(delta, dict))
            for row in canonical_matches
        ):
            reasons.append(
                f"Canonical SOURCE_TRANSFER row for {spec['label']} must include explicit mechanism language and concrete code delta."
            )
            continue

        delta_matches = []
        for row in source_delta_rows:
            if not isinstance(row, dict):
                continue
            source_cell = str(row.get("source", "")).lower()
            if any(alias in source_cell for alias in aliases):
                delta_matches.append(row)
        if not delta_matches:
            reasons.append(f"SOURCE_TRANSFER_DELTAS missing row for {spec['label']}.")
            continue

        if not any(
            _row_has_explicit_mechanism(str(row.get("theorem_or_mechanism", "")), mechanisms)
            and _row_has_code_delta(str(row.get("code_delta", "")))
            for row in delta_matches
        ):
            reasons.append(
                f"SOURCE_TRANSFER_DELTAS row for {spec['label']} must include explicit mechanism language and concrete code delta."
            )
            continue

        validated_sources.append(sid)

    # Gate metrics
    payload = {
        "passed": len(reasons) == 0,
        "run_id": run_id,
        "round": int(round_num),
        "round_id": round_id,
        "mode": mode,
        "required_source_count": len(required_specs),
        "validated_source_count": len(validated_sources),
        "validated_sources": validated_sources,
        "active_hypotheses": len(active_rows),
        "retired_hypotheses": len(retired_rows),
        "canonical_source_entries": len(transfer_entries),
        "source_delta_entries": len(source_delta_rows),
        "frontier_entries": len(frontier_rows),
        "instance_registry_entries": len(registry_rows),
        "reasons": reasons[:40],
    }
    return payload


def _cmd_validate_round(args: argparse.Namespace) -> None:
    payload = validate_round_docs(
        docs_root=Path(args.docs_root),
        run_id=args.run_id,
        round_num=args.round,
        round_id=args.round_id,
        mode=args.mode,
        papers_dir=Path(args.papers_dir),
    )
    print(json.dumps(payload, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate docs-first structured round artifacts")
    sub = parser.add_subparsers(dest="cmd", required=True)

    round_parser = sub.add_parser("validate-round", help="validate docs artifacts for a specific round")
    round_parser.add_argument("--docs-root", default="docs")
    round_parser.add_argument("--run-id", required=True)
    round_parser.add_argument("--round", type=int, required=True)
    round_parser.add_argument("--round-id", required=True)
    round_parser.add_argument("--mode", choices=("research", "solve", "synthesis"), required=True)
    round_parser.add_argument("--papers-dir", default="papers")
    round_parser.set_defaults(func=_cmd_validate_round)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
