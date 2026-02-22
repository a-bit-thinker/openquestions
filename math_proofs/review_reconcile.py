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


def _instance_label(instance: dict[str, int]) -> str:
    return f"S({instance['r']},{instance['q']},{instance['n']})"


def _parse_instance_label(label: str) -> dict[str, int] | None:
    m = re.match(r"^\s*S\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)\s*$", label)
    if not m:
        return None
    r, q, n = map(int, m.groups())
    return {"n": n, "q": q, "r": r}


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


def _append_event_log(run_log_dir: Path, payload: dict[str, Any]) -> None:
    run_log_dir.mkdir(parents=True, exist_ok=True)

    events_path = run_log_dir / "REVIEW_EVENTS.jsonl"
    with events_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, sort_keys=True) + "\n")

    dialogue_path = run_log_dir / "REVIEW_DIALOGUE.md"
    lines = [
        f"## {payload.get('generated_utc', _utc_now_iso())} round={payload.get('round', '?')} mode={payload.get('mode', '?')}",
        f"- Skeptic: {payload.get('skeptic', {}).get('statement', 'n/a')}",
        f"- Author: {payload.get('author', {}).get('statement', 'n/a')}",
        f"- Decision: {payload.get('decision', {}).get('summary', 'n/a')}",
        "",
    ]
    with dialogue_path.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def reconcile_instance(
    *,
    docs_root: Path,
    instance: dict[str, int],
    mode: str,
    run_id: str = "",
    round_num: int = 0,
    run_log_dir: Path | None = None,
) -> dict[str, Any]:
    label = _instance_label(instance)

    registry_yaml = _read_yaml(docs_root / "instances" / "INSTANCE_REGISTRY.yaml")
    frontier_yaml = _read_yaml(docs_root / "instances" / "FRONTIER_QUEUE.yaml")
    registry_rows = registry_yaml.get("registry", []) if isinstance(registry_yaml, dict) else []
    frontier_rows = frontier_yaml.get("queue", []) if isinstance(frontier_yaml, dict) else []

    if not isinstance(registry_rows, list):
        registry_rows = []
    if not isinstance(frontier_rows, list):
        frontier_rows = []

    registry_map: dict[str, dict[str, Any]] = {}
    for row in registry_rows:
        if not isinstance(row, dict):
            continue
        row_label = str(row.get("instance", "")).strip()
        if row_label:
            registry_map[row_label] = row

    current_status = str(registry_map.get(label, {}).get("status", "unknown")).strip()

    skeptic_statement = "No blocking contradiction found."
    author_statement = "Continue with selected instance."
    decision_action = "keep"
    decision_summary = "No replacement required."
    replacement_instance: dict[str, int] | None = None
    replacement_label = ""

    blocked_statuses = {"provisional_nonexistence_veto", "proved_nonexistence"}
    if mode == "solve" and current_status in blocked_statuses:
        skeptic_statement = (
            f"Instance {label} is marked '{current_status}' in registry; solver spend is likely wasted."
        )
        author_statement = "Search for nearest frontier instance with unknown status and same r."

        current_r = int(instance.get("r", 0))

        def frontier_rank(row: dict[str, Any]) -> tuple[int, str]:
            rank = row.get("rank", 10**9)
            try:
                rank_i = int(rank)
            except (TypeError, ValueError):
                rank_i = 10**9
            return (rank_i, str(row.get("instance", "")))

        candidates: list[tuple[int, str, dict[str, int]]] = []
        for row in sorted((r for r in frontier_rows if isinstance(r, dict)), key=frontier_rank):
            candidate_label = str(row.get("instance", "")).strip()
            if not candidate_label:
                continue
            reg = registry_map.get(candidate_label, {})
            status = str(reg.get("status", "")).strip()
            if status not in {"unknown_admissible_frontier", "unknown_admissible"}:
                continue
            parsed = _parse_instance_label(candidate_label)
            if not parsed:
                continue
            same_r = 0 if parsed["r"] == current_r else 1
            candidates.append((same_r, candidate_label, parsed))

        if candidates:
            candidates.sort(key=lambda item: (item[0], item[1]))
            replacement_label = candidates[0][1]
            replacement_instance = candidates[0][2]
            decision_action = "replace"
            decision_summary = (
                f"Replace {label} (status={current_status}) with {replacement_label} from frontier queue."
            )
        else:
            decision_action = "keep_with_warning"
            decision_summary = (
                f"No suitable replacement found for blocked instance {label}; keep with warning."
            )

    payload = {
        "generated_utc": _utc_now_iso(),
        "run_id": run_id,
        "round": int(round_num),
        "mode": mode,
        "instance_label": label,
        "instance": instance,
        "registry_status": current_status,
        "skeptic": {
            "statement": skeptic_statement,
        },
        "author": {
            "statement": author_statement,
        },
        "decision": {
            "action": decision_action,
            "summary": decision_summary,
            "replacement_label": replacement_label,
            "replacement_instance": replacement_instance,
        },
    }

    if run_log_dir is not None:
        _append_event_log(run_log_dir, payload)

    return payload


def _cmd_reconcile(args: argparse.Namespace) -> None:
    instance = json.loads(args.instance_json)
    if not isinstance(instance, dict):
        raise SystemExit("--instance-json must decode to an object")

    payload = reconcile_instance(
        docs_root=Path(args.docs_root),
        instance={"n": int(instance["n"]), "q": int(instance["q"]), "r": int(instance["r"])},
        mode=args.mode,
        run_id=args.run_id,
        round_num=args.round,
        run_log_dir=Path(args.run_log_dir) if args.run_log_dir else None,
    )
    print(json.dumps(payload, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="In-loop review reconcile and replacement helper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    rec = sub.add_parser("reconcile", help="reconcile instance with registry and propose replacement")
    rec.add_argument("--docs-root", default="docs")
    rec.add_argument("--instance-json", required=True)
    rec.add_argument("--mode", choices=("research", "solve", "synthesis"), required=True)
    rec.add_argument("--run-id", default="")
    rec.add_argument("--round", type=int, default=0)
    rec.add_argument("--run-log-dir", default="")
    rec.set_defaults(func=_cmd_reconcile)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
