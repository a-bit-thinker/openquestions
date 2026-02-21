from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from math_proofs.steiner_system import evaluate_steiner_system


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _ensure_log_dirs(log_root: Path) -> Path:
    rounds_dir = log_root / "rounds"
    rounds_dir.mkdir(parents=True, exist_ok=True)
    return rounds_dir


def _next_round_id(rounds_dir: Path) -> str:
    existing = sorted(p.name for p in rounds_dir.iterdir() if p.is_dir() and p.name.startswith("round_"))
    if not existing:
        return "round_0001"

    last_num = max(int(name.split("_")[1]) for name in existing)
    return f"round_{last_num + 1:04d}"


def _load_index(index_path: Path) -> list[dict[str, Any]]:
    if not index_path.exists():
        return []

    rows: list[dict[str, Any]] = []
    for line in index_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def _append_index(index_path: Path, row: dict[str, Any]) -> None:
    with index_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")


def _build_next_brief(index_rows: list[dict[str, Any]]) -> str:
    if not index_rows:
        return "# Next Round Brief\n\nNo rounds recorded yet.\n"

    latest = index_rows[-1]
    top = sorted(index_rows, key=lambda row: row.get("score", 0.0), reverse=True)[:3]

    lines = [
        "# Next Round Brief",
        "",
        f"Generated at: {_utc_now_iso()}",
        "",
        "## Latest round",
        f"- Round: {latest['round_id']}",
        f"- Score: {latest['score']:.2f}",
        f"- Valid: {latest['is_valid']}",
        f"- Exact-once subsets: {latest['exact_once_r_subsets']} / {latest['total_required_r_subsets']}",
        f"- Uncovered subsets: {latest['uncovered_r_subsets']}",
        f"- Overcovered subsets: {latest['overcovered_r_subsets']}",
        f"- Advance label: {latest['advance_label']}",
        "",
        "## Best rounds so far",
    ]

    for row in top:
        lines.append(
            f"- {row['round_id']}: score={row['score']:.2f}, valid={row['is_valid']}, "
            f"exact_once={row['exact_once_r_subsets']}/{row['total_required_r_subsets']}"
        )

    lines.extend(["", "## Actionable next priorities"])

    if latest["is_valid"]:
        lines.append("- Valid certificate found. Focus on proof artifact quality and independent reproduction.")
    else:
        if latest["divisibility_failures"]:
            lines.append("- Instance appears impossible by divisibility checks. Change instance before further search.")
        if latest.get("oversubscribed_r_minus_1_subsets", 0) > 0:
            lines.append("- Reduce (r-1)-subset oversubscription; completion is impossible without deletions.")
        if latest["invalid_block_count"] > 0:
            lines.append("- Fix certificate formatting/vertex-range issues before search optimization.")
        if latest["uncovered_r_subsets"] > 0:
            lines.append("- Prioritize moves that increase uncovered-subset coverage.")
        if latest["overcovered_r_subsets"] > 0:
            lines.append("- Reduce collisions: avoid reusing already covered r-subsets.")
        residual_hint = latest.get("residual_repair_hint", {})
        if residual_hint.get("eligible"):
            lines.append("- Residual exact-repair stage is eligible; run exact cover on uncovered subsets.")
        elif residual_hint.get("reason"):
            lines.append(f"- Residual exact-repair status: {residual_hint['reason']}.")
        if latest["actual_block_count"] and latest.get("expected_block_count"):
            lines.append(
                f"- Align block count toward expected {latest['expected_block_count']} "
                f"(current {latest['actual_block_count']})."
            )

    lines.append("")
    return "\n".join(lines)


def start_round(
    log_root: Path,
    instance: dict[str, int],
    objective: str,
    hypothesis: str = "",
    parent_round_id: str | None = None,
) -> str:
    rounds_dir = _ensure_log_dirs(log_root)
    round_id = _next_round_id(rounds_dir)
    round_dir = rounds_dir / round_id
    round_dir.mkdir(parents=False, exist_ok=False)

    meta = {
        "round_id": round_id,
        "created_at": _utc_now_iso(),
        "instance": instance,
        "objective": objective,
        "hypothesis": hypothesis,
        "parent_round_id": parent_round_id,
        "status": "open",
    }
    _write_json(round_dir / "meta.json", meta)

    notes_template = "\n".join(
        [
            f"# {round_id} notes",
            "",
            "## Plan",
            "- ",
            "",
            "## Work log",
            "- ",
            "",
            "## Observations",
            "- ",
            "",
            "## Core advance",
            "- ",
            "",
            "## Next-hypothesis",
            "- ",
            "",
        ]
    )
    (round_dir / "notes.md").write_text(notes_template, encoding="utf-8")
    return round_id


def close_round(
    log_root: Path,
    round_id: str,
    certificate: list[list[int]],
    techniques: list[str] | None = None,
    notes_text: str = "",
) -> dict[str, Any]:
    techniques = techniques or []

    rounds_dir = _ensure_log_dirs(log_root)
    round_dir = rounds_dir / round_id
    if not round_dir.exists():
        raise FileNotFoundError(f"round does not exist: {round_id}")

    meta_path = round_dir / "meta.json"
    meta = _load_json(meta_path)
    instance = meta["instance"]

    start = time.perf_counter()
    evaluation = evaluate_steiner_system(instance, certificate)
    elapsed = time.perf_counter() - start
    evaluation["evaluation_runtime_sec"] = round(elapsed, 6)

    _write_json(round_dir / "candidate.json", certificate)
    _write_json(round_dir / "evaluation.json", evaluation)

    if notes_text:
        (round_dir / "notes.md").write_text(notes_text, encoding="utf-8")

    index_path = log_root / "rounds" / "index.jsonl"
    index_rows = _load_index(index_path)

    best_prior_score = max((row["score"] for row in index_rows), default=0.0)
    previous_row = index_rows[-1] if index_rows else None

    score = float(evaluation["score"])
    if score > best_prior_score:
        advance_label = "new_best"
    elif previous_row and score > previous_row["score"]:
        advance_label = "improved_vs_previous"
    elif previous_row and score == previous_row["score"]:
        advance_label = "flat"
    else:
        advance_label = "regressed"

    summary_row = {
        "round_id": round_id,
        "closed_at": _utc_now_iso(),
        "objective": meta["objective"],
        "score": score,
        "is_valid": bool(evaluation["is_valid"]),
        "advance_label": advance_label,
        "techniques": techniques,
        "total_required_r_subsets": int(evaluation["total_required_r_subsets"]),
        "exact_once_r_subsets": int(evaluation["exact_once_r_subsets"]),
        "uncovered_r_subsets": int(evaluation["uncovered_r_subsets"]),
        "overcovered_r_subsets": int(evaluation["overcovered_r_subsets"]),
        "actual_block_count": int(evaluation["actual_block_count"]),
        "expected_block_count": evaluation["expected_block_count"],
        "invalid_block_count": int(evaluation["invalid_block_count"]),
        "divisibility_failures": evaluation["divisibility_failures"],
        "point_degree_min": int(evaluation.get("point_degree_min", 0)),
        "point_degree_max": int(evaluation.get("point_degree_max", 0)),
        "point_degree_gap": int(evaluation.get("point_degree_gap", 0)),
        "target_point_degree": evaluation.get("target_point_degree"),
        "r_minus_1_target_degree": evaluation.get("r_minus_1_target_degree"),
        "r_minus_1_max_degree": int(evaluation.get("r_minus_1_max_degree", 0)),
        "oversubscribed_r_minus_1_subsets": int(evaluation.get("oversubscribed_r_minus_1_subsets", 0)),
        "additive_repair_feasible": evaluation.get("additive_repair_feasible"),
        "residual_repair_hint": evaluation.get("residual_repair_hint", {}),
        "issues": evaluation["issues"],
    }

    _append_index(index_path, summary_row)

    summary_lines = [
        f"# {round_id} summary",
        "",
        f"- Closed at: {summary_row['closed_at']}",
        f"- Score: {summary_row['score']:.2f}",
        f"- Valid Steiner system: {summary_row['is_valid']}",
        f"- Advance label: {summary_row['advance_label']}",
        "",
        "## Core benchmark",
        f"- Exact-once r-subsets: {summary_row['exact_once_r_subsets']} / {summary_row['total_required_r_subsets']}",
        f"- Uncovered r-subsets: {summary_row['uncovered_r_subsets']}",
        f"- Overcovered r-subsets: {summary_row['overcovered_r_subsets']}",
        f"- Block count: {summary_row['actual_block_count']} (expected: {summary_row['expected_block_count']})",
        f"- Invalid blocks: {summary_row['invalid_block_count']}",
        f"- Point-degree range: {summary_row['point_degree_min']}..{summary_row['point_degree_max']} "
        f"(target: {summary_row['target_point_degree']})",
        f"- (r-1)-subset max load: {summary_row['r_minus_1_max_degree']} "
        f"(target: {summary_row['r_minus_1_target_degree']})",
        f"- Oversubscribed (r-1)-subsets: {summary_row['oversubscribed_r_minus_1_subsets']}",
        f"- Additive repair feasible: {summary_row['additive_repair_feasible']}",
        f"- Residual exact-repair: {summary_row['residual_repair_hint'].get('reason', 'n/a')}",
        "",
        "## Issues",
    ]

    if summary_row["issues"]:
        summary_lines.extend(f"- {item}" for item in summary_row["issues"])
    else:
        summary_lines.append("- none")

    if techniques:
        summary_lines.extend(["", "## Techniques used"])
        summary_lines.extend(f"- {tech}" for tech in techniques)

    summary_lines.extend(["", "## Guidance for next round"])
    if summary_row["is_valid"]:
        summary_lines.append("- Preserve this certificate and focus on proof write-up + independent verification.")
    else:
        if summary_row["divisibility_failures"]:
            summary_lines.append("- Switch to a feasible instance first (divisibility conditions failed).")
        if summary_row["oversubscribed_r_minus_1_subsets"] > 0:
            summary_lines.append("- First remove blocks causing (r-1)-subset oversubscription before adding new ones.")
        if summary_row["invalid_block_count"] > 0:
            summary_lines.append("- Repair certificate formatting/range errors before search.")
        if summary_row["uncovered_r_subsets"] > 0:
            summary_lines.append("- Target uncovered subsets with constructive block additions.")
        if summary_row["overcovered_r_subsets"] > 0:
            summary_lines.append("- Penalize collisions in local search objective.")
        if summary_row["residual_repair_hint"].get("eligible"):
            summary_lines.append("- Run residual exact-cover completion as the next stage.")

    (round_dir / "round_summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    meta["status"] = "closed"
    meta["closed_at"] = summary_row["closed_at"]
    _write_json(meta_path, meta)

    updated_rows = _load_index(index_path)
    brief = _build_next_brief(updated_rows)
    (log_root / "rounds" / "NEXT_ROUND_BRIEF.md").write_text(brief, encoding="utf-8")

    return summary_row


def _parse_instance_json(raw: str) -> dict[str, int]:
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("instance must decode to a JSON object")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Round logger for Steiner-system Codex loops")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    start_parser = subparsers.add_parser("start", help="create a new round")
    start_parser.add_argument("--log-dir", default="steiner_logs")
    start_parser.add_argument("--instance-json", required=True)
    start_parser.add_argument("--objective", required=True)
    start_parser.add_argument("--hypothesis", default="")
    start_parser.add_argument("--parent-round-id", default=None)

    close_parser = subparsers.add_parser("close", help="close a round with evaluation")
    close_parser.add_argument("--log-dir", default="steiner_logs")
    close_parser.add_argument("--round-id", required=True)
    close_parser.add_argument("--certificate-file", required=True)
    close_parser.add_argument("--notes-file", default=None)
    close_parser.add_argument("--technique", action="append", default=[])

    report_parser = subparsers.add_parser("report", help="regenerate NEXT_ROUND_BRIEF.md")
    report_parser.add_argument("--log-dir", default="steiner_logs")

    args = parser.parse_args()
    log_root = Path(args.log_dir)

    if args.cmd == "start":
        instance = _parse_instance_json(args.instance_json)
        round_id = start_round(
            log_root=log_root,
            instance=instance,
            objective=args.objective,
            hypothesis=args.hypothesis,
            parent_round_id=args.parent_round_id,
        )
        print(round_id)
        return

    if args.cmd == "close":
        cert = _load_json(Path(args.certificate_file))
        if not isinstance(cert, list):
            raise ValueError("certificate file must contain a JSON list of blocks")

        notes_text = ""
        if args.notes_file:
            notes_text = Path(args.notes_file).read_text(encoding="utf-8")

        summary = close_round(
            log_root=log_root,
            round_id=args.round_id,
            certificate=cert,
            techniques=args.technique,
            notes_text=notes_text,
        )
        print(json.dumps(summary, indent=2, sort_keys=True))
        return

    if args.cmd == "report":
        rounds_dir = _ensure_log_dirs(log_root)
        index_rows = _load_index(rounds_dir / "index.jsonl")
        brief = _build_next_brief(index_rows)
        (rounds_dir / "NEXT_ROUND_BRIEF.md").write_text(brief, encoding="utf-8")
        print(str(rounds_dir / "NEXT_ROUND_BRIEF.md"))


if __name__ == "__main__":
    main()
