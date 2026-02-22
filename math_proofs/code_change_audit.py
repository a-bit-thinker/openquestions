from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_INCLUDE_PATHS = (
    "run_steiner_loop.sh",
    "run_steiner_round.sh",
    "README.md",
    "STEINER_LOOP_LOGGING.md",
    "math_proofs",
    "docs",
)

DEFAULT_EXCLUDE_PREFIXES = (
    ".git/",
    "steiner_logs/",
    "docs/generated/",
    "papers/_extracted_text/",
)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _as_repo_rel(path: Path, repo_root: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def _is_excluded(rel_path: str) -> bool:
    return any(rel_path.startswith(prefix) for prefix in DEFAULT_EXCLUDE_PREFIXES)


def _iter_included_files(repo_root: Path) -> list[Path]:
    files: set[Path] = set()
    for rel in DEFAULT_INCLUDE_PATHS:
        target = repo_root / rel
        if not target.exists():
            continue
        if target.is_file():
            rel_path = _as_repo_rel(target, repo_root)
            if not _is_excluded(rel_path):
                files.add(target)
            continue
        for candidate in target.rglob("*"):
            if not candidate.is_file():
                continue
            rel_path = _as_repo_rel(candidate, repo_root)
            if _is_excluded(rel_path):
                continue
            files.add(candidate)
    return sorted(files)


def _file_record(path: Path, repo_root: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    sha256 = hashlib.sha256(raw).hexdigest()
    line_count = None
    try:
        line_count = len(raw.decode("utf-8").splitlines())
    except UnicodeDecodeError:
        line_count = None
    return {
        "path": _as_repo_rel(path, repo_root),
        "sha256": sha256,
        "size_bytes": len(raw),
        "line_count": line_count,
    }


def build_snapshot(repo_root: Path) -> dict[str, Any]:
    records = [_file_record(path, repo_root) for path in _iter_included_files(repo_root)]
    return {
        "version": 1,
        "generated_utc": _utc_now_iso(),
        "repo_root": str(repo_root.resolve()),
        "files": records,
    }


def write_snapshot(repo_root: Path, output: Path) -> dict[str, Any]:
    snapshot = build_snapshot(repo_root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return snapshot


def _load_snapshot(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"snapshot is not an object: {path}")
    files = payload.get("files", [])
    if not isinstance(files, list):
        raise ValueError(f"snapshot files field must be a list: {path}")
    return payload


def _index_files(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = snapshot.get("files", [])
    out: dict[str, dict[str, Any]] = {}
    if not isinstance(rows, list):
        return out
    for row in rows:
        if not isinstance(row, dict):
            continue
        rel_path = str(row.get("path", "")).strip()
        if not rel_path:
            continue
        out[rel_path] = row
    return out


def _line_count(row: dict[str, Any]) -> int | None:
    value = row.get("line_count")
    if isinstance(value, int):
        return value
    return None


def build_diff_event(
    *,
    before_snapshot: dict[str, Any],
    after_snapshot: dict[str, Any],
    run_id: str,
    round_num: int,
    round_id: str,
    mode: str,
) -> dict[str, Any]:
    before_map = _index_files(before_snapshot)
    after_map = _index_files(after_snapshot)

    changes: list[dict[str, Any]] = []
    for rel_path in sorted(set(before_map) | set(after_map)):
        before_row = before_map.get(rel_path)
        after_row = after_map.get(rel_path)
        if before_row is None and after_row is not None:
            after_lines = _line_count(after_row)
            changes.append(
                {
                    "path": rel_path,
                    "kind": "added",
                    "before_sha256": "",
                    "after_sha256": str(after_row.get("sha256", "")),
                    "before_lines": None,
                    "after_lines": after_lines,
                    "line_delta": after_lines,
                }
            )
            continue
        if before_row is not None and after_row is None:
            before_lines = _line_count(before_row)
            changes.append(
                {
                    "path": rel_path,
                    "kind": "deleted",
                    "before_sha256": str(before_row.get("sha256", "")),
                    "after_sha256": "",
                    "before_lines": before_lines,
                    "after_lines": None,
                    "line_delta": -before_lines if before_lines is not None else None,
                }
            )
            continue
        if before_row is None or after_row is None:
            continue

        if str(before_row.get("sha256", "")) == str(after_row.get("sha256", "")):
            continue
        before_lines = _line_count(before_row)
        after_lines = _line_count(after_row)
        line_delta = None
        if before_lines is not None and after_lines is not None:
            line_delta = after_lines - before_lines
        changes.append(
            {
                "path": rel_path,
                "kind": "modified",
                "before_sha256": str(before_row.get("sha256", "")),
                "after_sha256": str(after_row.get("sha256", "")),
                "before_lines": before_lines,
                "after_lines": after_lines,
                "line_delta": line_delta,
            }
        )

    return {
        "version": 1,
        "generated_utc": _utc_now_iso(),
        "run_id": run_id,
        "round": int(round_num),
        "round_id": round_id,
        "mode": mode,
        "change_count": len(changes),
        "changes": changes,
    }


def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, sort_keys=True) + "\n")


def _append_markdown(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"## {payload.get('round_id', '?')} ({payload.get('mode', '?')})",
        f"- Generated (UTC): {payload.get('generated_utc', '')}",
        f"- Changed files: {payload.get('change_count', 0)}",
        "",
        "| Path | Kind | Before SHA | After SHA | Line Delta |",
        "|---|---|---|---|---:|",
    ]
    for row in payload.get("changes", []):
        if not isinstance(row, dict):
            continue
        before_sha = str(row.get("before_sha256", ""))[:8]
        after_sha = str(row.get("after_sha256", ""))[:8]
        line_delta = row.get("line_delta")
        line_delta_cell = "n/a" if line_delta is None else str(line_delta)
        lines.append(
            f"| {row.get('path', '')} | {row.get('kind', '')} | {before_sha} | {after_sha} | {line_delta_cell} |"
        )
    lines.append("")
    with path.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def _cmd_snapshot(args: argparse.Namespace) -> None:
    repo_root = Path(args.repo_root).resolve()
    output = Path(args.output)
    write_snapshot(repo_root, output)
    print(
        json.dumps(
            {
                "snapshot": str(output),
                "repo_root": str(repo_root),
            },
            sort_keys=True,
        )
    )


def _cmd_diff(args: argparse.Namespace) -> None:
    before_path = Path(args.before)
    repo_root = Path(args.repo_root).resolve()
    after_output = Path(args.after_output)
    event_json_out = Path(args.event_json_out) if args.event_json_out else None
    jsonl_out = Path(args.jsonl_out)
    md_out = Path(args.md_out)

    before_snapshot = _load_snapshot(before_path)
    after_snapshot = write_snapshot(repo_root, after_output)

    payload = build_diff_event(
        before_snapshot=before_snapshot,
        after_snapshot=after_snapshot,
        run_id=args.run_id,
        round_num=args.round,
        round_id=args.round_id,
        mode=args.mode,
    )

    _append_jsonl(jsonl_out, payload)
    _append_markdown(md_out, payload)
    if event_json_out is not None:
        event_json_out.parent.mkdir(parents=True, exist_ok=True)
        event_json_out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "change_count": payload["change_count"],
                "event_json_out": str(event_json_out) if event_json_out else "",
                "jsonl_out": str(jsonl_out),
                "md_out": str(md_out),
                "round_id": args.round_id,
            },
            sort_keys=True,
        )
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Code change audit utilities for loop runs")
    sub = parser.add_subparsers(dest="cmd", required=True)

    snap = sub.add_parser("snapshot", help="write a code snapshot")
    snap.add_argument("--repo-root", default=".")
    snap.add_argument("--output", required=True)
    snap.set_defaults(func=_cmd_snapshot)

    diff = sub.add_parser("diff", help="append per-round code diff audit")
    diff.add_argument("--before", required=True)
    diff.add_argument("--after-output", required=True)
    diff.add_argument("--repo-root", default=".")
    diff.add_argument("--run-id", required=True)
    diff.add_argument("--round", type=int, required=True)
    diff.add_argument("--round-id", required=True)
    diff.add_argument("--mode", required=True)
    diff.add_argument("--jsonl-out", required=True)
    diff.add_argument("--md-out", required=True)
    diff.add_argument("--event-json-out", default="")
    diff.set_defaults(func=_cmd_diff)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
