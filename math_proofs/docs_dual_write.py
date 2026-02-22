from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_json_text(raw: str, field: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {field}: {exc}") from exc


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _section_lines(text: str, heading_keywords: tuple[str, ...]) -> list[str]:
    lines = text.splitlines()
    start = None
    for idx, raw in enumerate(lines):
        match = re.match(r"^\s*##\s+(.+?)\s*$", raw)
        if not match:
            continue
        heading = match.group(1).strip().lower()
        if any(keyword in heading for keyword in heading_keywords):
            start = idx + 1
            break
    if start is None:
        return []

    block: list[str] = []
    for raw in lines[start:]:
        if re.match(r"^\s*##\s+", raw):
            break
        block.append(raw)
    return block


def _extract_bullets(block: list[str]) -> list[str]:
    out: list[str] = []
    for raw in block:
        match = re.match(r"^\s*(?:-|\*|\d+\.)\s+(.+?)\s*$", raw)
        if not match:
            continue
        item = match.group(1).strip()
        item = re.sub(
            r"^(advance|evidence|hypothesis|next-hypothesis|observation|result)\s*:\s*",
            "",
            item,
            flags=re.IGNORECASE,
        )
        if item:
            out.append(item)
    return out


def _parse_markdown_table(section_block: list[str]) -> tuple[list[str], list[list[str]]]:
    cleaned = [line.strip() for line in section_block if line.strip()]
    groups: list[list[str]] = []
    current: list[str] = []

    for line in cleaned:
        if line.startswith("|"):
            current.append(line)
            continue
        if current:
            groups.append(current)
            current = []
    if current:
        groups.append(current)

    if not groups:
        return [], []

    table_lines = max(groups, key=len)
    if len(table_lines) < 2:
        return [], []

    def split_cells(raw_line: str) -> list[str]:
        return [cell.strip() for cell in raw_line.strip().strip("|").split("|")]

    header = split_cells(table_lines[0])
    start = 1
    if len(table_lines) >= 2 and re.match(r"^\|?[\s:\-|]+\|?$", table_lines[1]) and "-" in table_lines[1]:
        start = 2

    rows: list[list[str]] = []
    width = len(header)
    for raw in table_lines[start:]:
        cells = split_cells(raw)
        if not any(cells):
            continue
        if len(cells) < width:
            cells.extend([""] * (width - len(cells)))
        rows.append(cells[:width])
    return header, rows


def _find_column(header: list[str], keywords: tuple[str, ...]) -> int:
    for idx, cell in enumerate(header):
        cell_l = cell.lower()
        if any(keyword in cell_l for keyword in keywords):
            return idx
    return -1


def _extract_source_transfer_entries(notes_text: str) -> list[dict[str, str]]:
    block = _section_lines(notes_text, ("paper-to-loop method extraction", "source-to-method transfer"))
    header, rows = _parse_markdown_table(block)
    if not header or not rows:
        return []

    source_col = _find_column(header, ("source", "pdf", "paper"))
    mechanism_col = _find_column(header, ("theorem", "mechanism", "method", "workflow", "protocol"))
    delta_col = _find_column(header, ("code", "delta", "file", "path", "implementation"))
    metric_col = _find_column(header, ("validation", "metric"))

    if source_col < 0 or mechanism_col < 0 or delta_col < 0:
        return []

    entries: list[dict[str, str]] = []
    for row in rows:
        source = row[source_col].strip() if source_col < len(row) else ""
        mechanism = row[mechanism_col].strip() if mechanism_col < len(row) else ""
        code_delta = row[delta_col].strip() if delta_col < len(row) else ""
        metric = row[metric_col].strip() if metric_col >= 0 and metric_col < len(row) else ""
        if not source and not mechanism and not code_delta:
            continue
        entries.append(
            {
                "source": source,
                "theorem_or_mechanism": mechanism,
                "code_delta": code_delta,
                "validation_metric": metric,
            }
        )
    return entries


def _yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _write_claim_deltas(path: Path, *, run_id: str, round_id: str, mode: str, notes_file: str, notes_text: str) -> None:
    core = _extract_bullets(_section_lines(notes_text, ("core advance",)))
    obs = _extract_bullets(_section_lines(notes_text, ("observations",)))

    claim_rows: list[tuple[str, str]] = []
    for item in core[:8]:
        claim_rows.append((item, "core_advance"))
    for item in obs[:6]:
        claim_rows.append((item, "observation"))

    lines = [
        "version: 1",
        f"generated_utc: {_yaml_quote(_utc_now_iso())}",
        f"run_id: {_yaml_quote(run_id)}",
        f"round_id: {_yaml_quote(round_id)}",
        f"mode: {_yaml_quote(mode)}",
        f"source_notes_file: {_yaml_quote(notes_file)}",
    ]
    if not claim_rows:
        lines.append("claims: []")
    else:
        lines.append("claims:")
        for statement, origin in claim_rows:
            lines.append(f"  - statement: {_yaml_quote(statement)}")
            lines.append(f"    origin: {_yaml_quote(origin)}")
            lines.append("    status: \"observed\"")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_hypothesis_deltas(path: Path, *, run_id: str, round_id: str, mode: str, notes_file: str, notes_text: str) -> None:
    next_h = _extract_bullets(_section_lines(notes_text, ("next-hypothesis", "next hypothesis")))
    active_h = _extract_bullets(_section_lines(notes_text, ("active hypotheses",)))

    rows: list[tuple[str, str]] = []
    for item in next_h[:8]:
        rows.append((item, "next_hypothesis"))
    for item in active_h[:8]:
        rows.append((item, "active_hypothesis"))

    lines = [
        "version: 1",
        f"generated_utc: {_yaml_quote(_utc_now_iso())}",
        f"run_id: {_yaml_quote(run_id)}",
        f"round_id: {_yaml_quote(round_id)}",
        f"mode: {_yaml_quote(mode)}",
        f"source_notes_file: {_yaml_quote(notes_file)}",
    ]
    if not rows:
        lines.append("hypotheses: []")
    else:
        lines.append("hypotheses:")
        for statement, origin in rows:
            lines.append(f"  - statement: {_yaml_quote(statement)}")
            lines.append(f"    origin: {_yaml_quote(origin)}")
            lines.append("    action: \"observe\"")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_source_transfer_deltas(path: Path, *, run_id: str, round_id: str, mode: str, notes_file: str, notes_text: str) -> None:
    entries = _extract_source_transfer_entries(notes_text)

    lines = [
        "version: 1",
        f"generated_utc: {_yaml_quote(_utc_now_iso())}",
        f"run_id: {_yaml_quote(run_id)}",
        f"round_id: {_yaml_quote(round_id)}",
        f"mode: {_yaml_quote(mode)}",
        f"source_notes_file: {_yaml_quote(notes_file)}",
    ]
    if not entries:
        lines.append("entries: []")
    else:
        lines.append("entries:")
        for row in entries:
            lines.append(f"  - source: {_yaml_quote(row['source'])}")
            lines.append(
                f"    theorem_or_mechanism: {_yaml_quote(row['theorem_or_mechanism'])}"
            )
            lines.append(f"    code_delta: {_yaml_quote(row['code_delta'])}")
            lines.append(f"    validation_metric: {_yaml_quote(row['validation_metric'])}")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _update_metrics_jsonl(path: Path, entry: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if path.exists():
        for raw in path.read_text(encoding="utf-8").splitlines():
            raw = raw.strip()
            if not raw:
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if not isinstance(row, dict):
                continue
            rows.append(row)

    rows = [
        row
        for row in rows
        if not (
            row.get("run_id") == entry.get("run_id")
            and int(row.get("round", -1)) == int(entry.get("round", -1))
            and row.get("mode") == entry.get("mode")
        )
    ]
    rows.append(entry)

    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")

    return rows


def _update_snapshot(path: Path, rows: list[dict[str, Any]]) -> None:
    latest = rows[-1] if rows else {}
    lines = [
        "# Docs Bridge Snapshot",
        "",
        f"Generated (UTC): {_utc_now_iso()}",
        "",
        f"Latest run: `{latest.get('run_id', '?')}`",
        f"Latest round: `{latest.get('round', '?')}` mode=`{latest.get('mode', '?')}`",
        f"Latest instance: `{latest.get('instance', '?')}`",
        f"Latest score: `{latest.get('score', '?')}` valid=`{latest.get('is_valid', '?')}`",
        "",
        "## Recent entries (last 10)",
        "| run_id | round | mode | instance | score | valid | uncovered | overcovered |",
        "|---|---:|---|---|---:|---|---:|---:|",
    ]

    for row in rows[-10:]:
        lines.append(
            "| {run_id} | {round} | {mode} | {instance} | {score} | {is_valid} | {uncovered} | {overcovered} |".format(
                run_id=row.get("run_id", "?"),
                round=row.get("round", "?"),
                mode=row.get("mode", "?"),
                instance=row.get("instance", "?"),
                score=row.get("score", "?"),
                is_valid=row.get("is_valid", "?"),
                uncovered=row.get("uncovered_r_subsets", "?"),
                overcovered=row.get("overcovered_r_subsets", "?"),
            )
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_round_artifacts(
    *,
    docs_root: Path,
    run_id: str,
    run_log_dir: str,
    round_num: int,
    round_id: str,
    mode: str,
    instance_label: str,
    instance_json: dict[str, Any],
    round_metrics: dict[str, Any],
    notes_file: Path,
    paper_gate: dict[str, Any] | None,
    techniques: list[str],
) -> dict[str, str]:
    generated_dir = docs_root / "generated"
    runs_root = generated_dir / "runs" / f"run_{run_id}" / f"round_{round_num:04d}"
    runs_root.mkdir(parents=True, exist_ok=True)
    generated_dir.mkdir(parents=True, exist_ok=True)

    notes_text = _read_text(notes_file)

    run_facts = {
        "version": 1,
        "generated_utc": _utc_now_iso(),
        "run_id": run_id,
        "run_log_dir": run_log_dir,
        "round": int(round_num),
        "round_id": round_id,
        "mode": mode,
        "instance_label": instance_label,
        "instance": instance_json,
        "notes_file": str(notes_file),
        "techniques": techniques,
        "metrics": round_metrics,
    }
    if paper_gate:
        run_facts["paper_gate"] = paper_gate

    run_facts_path = runs_root / "RUN_FACTS.json"
    run_facts_path.write_text(json.dumps(run_facts, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    claim_deltas_path = runs_root / "CLAIM_DELTAS.yaml"
    _write_claim_deltas(
        claim_deltas_path,
        run_id=run_id,
        round_id=round_id,
        mode=mode,
        notes_file=str(notes_file),
        notes_text=notes_text,
    )

    hypothesis_deltas_path = runs_root / "HYPOTHESIS_DELTAS.yaml"
    _write_hypothesis_deltas(
        hypothesis_deltas_path,
        run_id=run_id,
        round_id=round_id,
        mode=mode,
        notes_file=str(notes_file),
        notes_text=notes_text,
    )

    source_transfer_deltas_path = runs_root / "SOURCE_TRANSFER_DELTAS.yaml"
    _write_source_transfer_deltas(
        source_transfer_deltas_path,
        run_id=run_id,
        round_id=round_id,
        mode=mode,
        notes_file=str(notes_file),
        notes_text=notes_text,
    )

    metrics_entry = {
        "run_id": run_id,
        "run_log_dir": run_log_dir,
        "round": int(round_num),
        "round_id": round_id,
        "mode": mode,
        "instance": instance_label,
        "score": round_metrics.get("score"),
        "is_valid": round_metrics.get("is_valid"),
        "exact_once_r_subsets": round_metrics.get("exact_once_r_subsets"),
        "total_required_r_subsets": round_metrics.get("total_required_r_subsets"),
        "uncovered_r_subsets": round_metrics.get("uncovered_r_subsets"),
        "overcovered_r_subsets": round_metrics.get("overcovered_r_subsets"),
        "techniques": techniques,
        "artifact_dir": str(runs_root),
    }
    if paper_gate:
        metrics_entry["paper_gate_pass"] = paper_gate.get("passed")
        metrics_entry["paper_quality_score"] = paper_gate.get("quality_score")
        metrics_entry["source_mapping"] = (
            f"{paper_gate.get('validated_source_count', '?')}/{paper_gate.get('required_source_count', '?')}"
        )

    metrics_jsonl_path = generated_dir / "RUN_METRICS.jsonl"
    rows = _update_metrics_jsonl(metrics_jsonl_path, metrics_entry)

    snapshot_path = generated_dir / "SNAPSHOT.md"
    _update_snapshot(snapshot_path, rows)

    return {
        "run_facts": str(run_facts_path),
        "claim_deltas": str(claim_deltas_path),
        "hypothesis_deltas": str(hypothesis_deltas_path),
        "source_transfer_deltas": str(source_transfer_deltas_path),
        "metrics_jsonl": str(metrics_jsonl_path),
        "snapshot": str(snapshot_path),
    }


def _cmd_round(args: argparse.Namespace) -> None:
    instance_json = _load_json_text(args.instance_json, "--instance-json")
    round_metrics = _load_json_text(args.round_metrics_json, "--round-metrics-json")
    paper_gate = None
    if args.paper_gate_json:
        paper_gate = _load_json_text(args.paper_gate_json, "--paper-gate-json")
        if not isinstance(paper_gate, dict):
            raise ValueError("--paper-gate-json must decode to a JSON object")

    if not isinstance(instance_json, dict):
        raise ValueError("--instance-json must decode to a JSON object")
    if not isinstance(round_metrics, dict):
        raise ValueError("--round-metrics-json must decode to a JSON object")

    paths = write_round_artifacts(
        docs_root=Path(args.docs_root),
        run_id=args.run_id,
        run_log_dir=args.run_log_dir,
        round_num=args.round,
        round_id=args.round_id,
        mode=args.mode,
        instance_label=args.instance_label,
        instance_json=instance_json,
        round_metrics=round_metrics,
        notes_file=Path(args.notes_file),
        paper_gate=paper_gate,
        techniques=args.technique,
    )
    print(json.dumps(paths, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Dual-write bridge for docs/ structured artifacts")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    round_parser = subparsers.add_parser("round", help="write docs artifacts for one round")
    round_parser.add_argument("--docs-root", default="docs")
    round_parser.add_argument("--run-id", required=True)
    round_parser.add_argument("--run-log-dir", required=True)
    round_parser.add_argument("--round", type=int, required=True)
    round_parser.add_argument("--round-id", required=True)
    round_parser.add_argument("--mode", choices=("research", "solve", "synthesis"), required=True)
    round_parser.add_argument("--instance-label", required=True)
    round_parser.add_argument("--instance-json", required=True)
    round_parser.add_argument("--round-metrics-json", required=True)
    round_parser.add_argument("--notes-file", required=True)
    round_parser.add_argument("--paper-gate-json", default="")
    round_parser.add_argument("--technique", action="append", default=[])
    round_parser.set_defaults(func=_cmd_round)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
