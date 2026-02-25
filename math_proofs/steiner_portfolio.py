from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import dataclass
from math import comb
from pathlib import Path
from typing import Any


_SUMMARY_ROW_RE = re.compile(r"^\|")
_INSTANCE_LABEL_RE = re.compile(r"S\((\d+),\s*(\d+),\s*(\d+)\)")
_EXACT_ONCE_RE = re.compile(r"^\s*(\d+)\s*/\s*(\d+)\s*$")


@dataclass
class ObservedStats:
    attempts: int = 0
    best_score: float = 0.0
    best_coverage: float = 0.0
    is_solved: bool = False


def _parse_summary_rows(summary_path: Path) -> list[dict[str, str]]:
    if not summary_path.exists():
        return []

    rows: list[dict[str, str]] = []
    for raw_line in summary_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not _SUMMARY_ROW_RE.match(line):
            continue
        if line.startswith("|---") or line.startswith("| Round "):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < 9:
            continue
        rows.append(
            {
                "round": parts[0],
                "mode": parts[1],
                "instance": parts[2],
                "score": parts[3],
                "valid": parts[4],
                "exact_once": parts[5],
                "uncovered": parts[6],
                "overcovered": parts[7],
                "notes": parts[8],
            }
        )
    return rows


def _parse_instance_label(label: str) -> tuple[int, int, int] | None:
    m = _INSTANCE_LABEL_RE.search(label.strip())
    if not m:
        return None
    r = int(m.group(1))
    q = int(m.group(2))
    n = int(m.group(3))
    return n, q, r


def _parse_exact_once_ratio(raw: str) -> float:
    m = _EXACT_ONCE_RE.match(raw)
    if not m:
        return 0.0
    num = int(m.group(1))
    den = int(m.group(2))
    if den <= 0:
        return 0.0
    return num / den


def _parse_bool(raw: str) -> bool:
    return raw.strip().lower() == "true"


def _parse_score(raw: str) -> float:
    try:
        return float(raw)
    except ValueError:
        return 0.0


def build_observed_stats(log_root: Path) -> dict[tuple[int, int, int], ObservedStats]:
    observed: dict[tuple[int, int, int], ObservedStats] = {}

    for summary_path in sorted(log_root.glob("run_*/RUN_SUMMARY.md")):
        for row in _parse_summary_rows(summary_path):
            if row["mode"].strip().lower() != "solve":
                continue
            parsed = _parse_instance_label(row["instance"])
            if parsed is None:
                continue

            stats = observed.setdefault(parsed, ObservedStats())
            stats.attempts += 1

            score = _parse_score(row["score"])
            coverage = _parse_exact_once_ratio(row["exact_once"])
            valid = _parse_bool(row["valid"])

            if score > stats.best_score:
                stats.best_score = score
            if coverage > stats.best_coverage:
                stats.best_coverage = coverage
            if valid:
                stats.is_solved = True

    return observed


def _admissible_with_expected(n: int, q: int, r: int) -> tuple[bool, int]:
    if not (n > q > r > 5):
        return False, 0
    if not (r < 10 and n < 200):
        return False, 0

    for s in range(r):
        numerator = comb(n - s, r - s)
        denominator = comb(q - s, r - s)
        if numerator % denominator != 0:
            return False, 0

    expected_blocks = comb(n, r) // comb(q, r)
    return True, expected_blocks


def _candidate_rows_for_r(
    *,
    r: int,
    n_max: int,
    observed: dict[tuple[int, int, int], ObservedStats],
    include_solved: bool,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for n in range(r + 2, n_max + 1):
        for q in range(r + 1, n):
            admissible, expected_blocks = _admissible_with_expected(n, q, r)
            if not admissible:
                continue

            key = (n, q, r)
            stats = observed.get(key, ObservedStats())
            if stats.is_solved and not include_solved:
                continue

            rows.append(
                {
                    "n": n,
                    "q": q,
                    "r": r,
                    "expected_blocks": expected_blocks,
                    "attempts": stats.attempts,
                    "best_score": round(stats.best_score, 4),
                    "best_coverage": round(stats.best_coverage, 8),
                    "is_solved": stats.is_solved,
                }
            )
    return rows


def select_instance_for_r(
    *,
    r: int,
    log_root: Path,
    mode: str = "portfolio",
    n_max: int = 199,
    min_expected_blocks: int = 1500,
    max_expected_blocks: int = 50000,
    include_solved: bool = False,
) -> dict[str, Any]:
    observed = build_observed_stats(log_root)
    rows = _candidate_rows_for_r(
        r=r,
        n_max=n_max,
        observed=observed,
        include_solved=include_solved,
    )

    if not rows:
        raise ValueError(f"no admissible candidates found for r={r}")

    mode = mode.strip().lower()
    if mode == "min_expected":
        rows.sort(key=lambda row: (row["expected_blocks"], row["n"], row["q"]))
        chosen = rows[0]
        return {
            "n": chosen["n"],
            "q": chosen["q"],
            "r": chosen["r"],
            "expected_blocks": chosen["expected_blocks"],
        }

    # Portfolio mode: prioritize in-band candidates, low-attempt coverage, and
    # a target size near the middle of the requested complexity band.
    lo = max(1, min_expected_blocks)
    hi = max(lo, max_expected_blocks)
    target = math.sqrt(lo * hi)
    target_log = math.log(target)

    def rank(row: dict[str, Any]) -> tuple[float, ...]:
        expected = max(1, int(row["expected_blocks"]))
        in_band = lo <= expected <= hi
        band_penalty = 0.0 if in_band else 1.0
        size_penalty = abs(math.log(expected) - target_log)
        attempts = float(row["attempts"])
        # Higher coverage/score means we already have a useful seed.
        # Keep this as a weak preference after coverage balance and attempts.
        coverage_bonus = -float(row["best_coverage"])
        score_bonus = -float(row["best_score"]) / 100.0
        return (
            band_penalty,
            attempts,
            size_penalty,
            coverage_bonus,
            score_bonus,
            float(expected),
            float(row["n"]),
            float(row["q"]),
        )

    rows.sort(key=rank)
    chosen = rows[0]
    return {
        "n": chosen["n"],
        "q": chosen["q"],
        "r": chosen["r"],
        "expected_blocks": chosen["expected_blocks"],
    }


def generate_existence_report(
    *,
    log_root: Path,
    output_file: Path,
    r_min: int = 6,
    r_max: int = 9,
    n_max: int = 199,
    top_k: int = 20,
    min_expected_blocks: int = 1500,
    max_expected_blocks: int = 50000,
) -> Path:
    observed = build_observed_stats(log_root)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    total = 0
    admissible_total = 0
    impossible_total = 0
    solved_total = 0
    unknown_total = 0

    by_r: dict[int, dict[str, int]] = {}
    unresolved_rows: list[dict[str, Any]] = []
    solved_rows: list[dict[str, Any]] = []

    for r in range(r_min, r_max + 1):
        by_r[r] = {
            "total": 0,
            "admissible": 0,
            "impossible_divisibility": 0,
            "solved": 0,
            "unknown": 0,
        }
        for n in range(r + 2, n_max + 1):
            for q in range(r + 1, n):
                if not (n > q > r > 5):
                    continue
                if not (r < 10 and n < 200):
                    continue

                total += 1
                by_r[r]["total"] += 1
                admissible, expected_blocks = _admissible_with_expected(n, q, r)
                key = (n, q, r)
                stats = observed.get(key, ObservedStats())

                if not admissible:
                    impossible_total += 1
                    by_r[r]["impossible_divisibility"] += 1
                    continue

                admissible_total += 1
                by_r[r]["admissible"] += 1
                row = {
                    "n": n,
                    "q": q,
                    "r": r,
                    "expected_blocks": expected_blocks,
                    "attempts": stats.attempts,
                    "best_score": stats.best_score,
                    "best_coverage": stats.best_coverage,
                    "label": f"S({r},{q},{n})",
                }

                if stats.is_solved:
                    solved_total += 1
                    by_r[r]["solved"] += 1
                    solved_rows.append(row)
                else:
                    unknown_total += 1
                    by_r[r]["unknown"] += 1
                    unresolved_rows.append(row)

    unresolved_rows.sort(
        key=lambda row: (
            row["best_coverage"],
            row["best_score"],
            -row["attempts"],
            -row["expected_blocks"],
        ),
        reverse=True,
    )
    solved_rows.sort(
        key=lambda row: (row["best_score"], row["best_coverage"], -row["expected_blocks"]),
        reverse=True,
    )

    lines = [
        "# Existence Frontier Report",
        "",
        f"Generated from log root: `{log_root}`",
        "Search domain: all `n > q > r > 5`, `r < 10`, `n < 200`.",
        "",
        "## Status semantics",
        "- `impossible_divisibility`: ruled out by necessary Steiner divisibility constraints.",
        "- `exists_certificate`: at least one valid certificate found in run logs.",
        "- `unknown`: admissible but not yet solved in this repository.",
        "",
        "## Global counts",
        f"- Total triples scanned: {total}",
        f"- Divisibility-impossible: {impossible_total}",
        f"- Admissible: {admissible_total}",
        f"- Exists (certificate found): {solved_total}",
        f"- Unknown admissible: {unknown_total}",
        "",
        "## Per-r breakdown",
        "| r | total | admissible | divisibility-impossible | exists_certificate | unknown_admissible |",
        "|---:|---:|---:|---:|---:|---:|",
    ]

    for r in range(r_min, r_max + 1):
        row = by_r[r]
        lines.append(
            f"| {r} | {row['total']} | {row['admissible']} | {row['impossible_divisibility']} | "
            f"{row['solved']} | {row['unknown']} |"
        )

    lines.extend(["", "## Suggested next portfolio picks"])
    for r in range(r_min, r_max + 1):
        try:
            pick = select_instance_for_r(
                r=r,
                log_root=log_root,
                mode="portfolio",
                n_max=n_max,
                min_expected_blocks=min_expected_blocks,
                max_expected_blocks=max_expected_blocks,
                include_solved=False,
            )
            lines.append(
                f"- r={r}: S({pick['r']},{pick['q']},{pick['n']}) expected_blocks={pick['expected_blocks']}"
            )
        except ValueError:
            lines.append(f"- r={r}: no unresolved admissible candidates available.")

    lines.extend(["", f"## Top unresolved admissible (top {top_k})"])
    if unresolved_rows:
        lines.append("| instance | expected_blocks | attempts | best_score | best_coverage |")
        lines.append("|---|---:|---:|---:|---:|")
        for row in unresolved_rows[:top_k]:
            lines.append(
                f"| {row['label']} | {row['expected_blocks']} | {row['attempts']} | "
                f"{row['best_score']:.2f} | {row['best_coverage']:.6f} |"
            )
    else:
        lines.append("- none")

    lines.extend(["", f"## Top solved admissible (top {top_k})"])
    if solved_rows:
        lines.append("| instance | expected_blocks | attempts | best_score | best_coverage |")
        lines.append("|---|---:|---:|---:|---:|")
        for row in solved_rows[:top_k]:
            lines.append(
                f"| {row['label']} | {row['expected_blocks']} | {row['attempts']} | "
                f"{row['best_score']:.2f} | {row['best_coverage']:.6f} |"
            )
    else:
        lines.append("- none")

    output_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_file


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Steiner instance portfolio selector and existence reporter")
    subparsers = parser.add_subparsers(dest="command", required=True)

    pick_parser = subparsers.add_parser("pick", help="pick an admissible instance for a given r")
    pick_parser.add_argument("--log-root", default="steiner_logs")
    pick_parser.add_argument("--r", type=int, required=True)
    pick_parser.add_argument("--mode", choices=["portfolio", "min_expected"], default="portfolio")
    pick_parser.add_argument("--n-max", type=int, default=199)
    pick_parser.add_argument("--min-expected-blocks", type=int, default=1500)
    pick_parser.add_argument("--max-expected-blocks", type=int, default=50000)
    pick_parser.add_argument("--include-solved", action="store_true")

    report_parser = subparsers.add_parser("report", help="generate existence frontier markdown report")
    report_parser.add_argument("--log-root", default="steiner_logs")
    report_parser.add_argument("--output-file", required=True)
    report_parser.add_argument("--r-min", type=int, default=6)
    report_parser.add_argument("--r-max", type=int, default=9)
    report_parser.add_argument("--n-max", type=int, default=199)
    report_parser.add_argument("--top-k", type=int, default=20)
    report_parser.add_argument("--min-expected-blocks", type=int, default=1500)
    report_parser.add_argument("--max-expected-blocks", type=int, default=50000)

    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "pick":
        payload = select_instance_for_r(
            r=int(args.r),
            log_root=Path(args.log_root),
            mode=args.mode,
            n_max=int(args.n_max),
            min_expected_blocks=int(args.min_expected_blocks),
            max_expected_blocks=int(args.max_expected_blocks),
            include_solved=bool(args.include_solved),
        )
        print(json.dumps(payload, sort_keys=True))
        return

    if args.command == "report":
        path = generate_existence_report(
            log_root=Path(args.log_root),
            output_file=Path(args.output_file),
            r_min=int(args.r_min),
            r_max=int(args.r_max),
            n_max=int(args.n_max),
            top_k=int(args.top_k),
            min_expected_blocks=int(args.min_expected_blocks),
            max_expected_blocks=int(args.max_expected_blocks),
        )
        print(str(path))
        return

    raise ValueError(f"unknown command: {args.command}")


if __name__ == "__main__":
    main()
