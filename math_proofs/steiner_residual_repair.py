from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from itertools import combinations
from math import comb
from pathlib import Path
from typing import Any

from math_proofs.steiner_system import evaluate_steiner_system


def _normalize_blocks(certificate: list[list[int]], n: int, q: int) -> list[tuple[int, ...]]:
    blocks: list[tuple[int, ...]] = []
    for raw_block in certificate:
        if not isinstance(raw_block, list) or len(raw_block) != q:
            raise ValueError("certificate must contain only q-sized list blocks")
        if any((not isinstance(v, int) or isinstance(v, bool)) for v in raw_block):
            raise ValueError("certificate blocks must contain integer vertices")

        block = tuple(sorted(raw_block))
        if len(set(block)) != q:
            raise ValueError("certificate block has repeated vertices")
        if block[0] < 0 or block[-1] >= n:
            raise ValueError("certificate block has out-of-range vertex")

        blocks.append(block)

    return blocks


def build_additive_residual_exact_cover(
    instance: dict[str, int],
    certificate: list[list[int]],
    *,
    max_total_r_subsets: int = 5_000_000,
    max_uncovered_r_subsets: int = 20_000,
    max_q_subset_scan: int = 2_000_000,
    max_candidate_blocks: int = 400_000,
) -> dict[str, Any]:
    """Build an additive-only residual exact-cover instance.

    This mode assumes we only ADD blocks to a collision-free partial packing.
    It is intentionally strict: if overcoverage already exists, it returns ineligible.
    """
    report = evaluate_steiner_system(instance, certificate)
    n = int(report["instance"]["n"])
    q = int(report["instance"]["q"])
    r = int(report["instance"]["r"])

    summary: dict[str, Any] = {
        "status": "ineligible",
        "instance": {"n": n, "q": q, "r": r},
        "reason": "",
        "metrics": {
            "score": report["score"],
            "is_valid": report["is_valid"],
            "uncovered_r_subsets": report["uncovered_r_subsets"],
            "overcovered_r_subsets": report["overcovered_r_subsets"],
            "invalid_block_count": report["invalid_block_count"],
            "divisibility_failures": report["divisibility_failures"],
        },
    }

    if report["invalid_block_count"] > 0:
        summary["reason"] = "candidate has invalid blocks"
        return summary

    if report["divisibility_failures"]:
        summary["reason"] = "instance fails admissibility/divisibility"
        return summary

    if report["overcovered_r_subsets"] > 0:
        summary["reason"] = "overcovered subsets present; additive residual repair is not applicable"
        return summary

    if report["uncovered_r_subsets"] == 0:
        summary["status"] = "already_complete"
        summary["reason"] = "no uncovered subsets"
        summary["uncovered_subsets"] = []
        summary["candidate_blocks"] = []
        return summary

    total_required = int(report["total_required_r_subsets"])
    if total_required > max_total_r_subsets:
        summary["reason"] = "instance too large for residual exact-cover budget"
        return summary

    uncovered_count = int(report["uncovered_r_subsets"])
    if uncovered_count > max_uncovered_r_subsets:
        summary["reason"] = "residual uncovered set is too large for exact-cover budget"
        return summary

    total_q_subsets = comb(n, q)
    if total_q_subsets > max_q_subset_scan:
        summary["reason"] = "q-subset search space too large for residual builder"
        return summary

    blocks = _normalize_blocks(certificate, n, q)
    used_blocks = set(blocks)

    subset_counts: Counter[tuple[int, ...]] = Counter()
    for block in blocks:
        for subset in combinations(block, r):
            subset_counts[subset] += 1

    uncovered_subsets = [subset for subset in combinations(range(n), r) if subset_counts.get(subset, 0) == 0]
    uncovered_index = {subset: i for i, subset in enumerate(uncovered_subsets)}

    block_candidates: list[dict[str, Any]] = []
    subset_to_block_ids: list[list[int]] = [[] for _ in uncovered_subsets]

    for block in combinations(range(n), q):
        if block in used_blocks:
            continue

        cover_indices: list[int] = []
        feasible = True
        for subset in combinations(block, r):
            if subset_counts.get(subset, 0) != 0:
                feasible = False
                break
            idx = uncovered_index.get(subset)
            if idx is None:
                feasible = False
                break
            cover_indices.append(idx)

        if not feasible:
            continue

        block_id = len(block_candidates)
        block_candidates.append(
            {
                "block": list(block),
                "cover_indices": cover_indices,
            }
        )
        for idx in cover_indices:
            subset_to_block_ids[idx].append(block_id)

        if len(block_candidates) > max_candidate_blocks:
            summary["reason"] = "candidate block pool exceeds budget"
            return summary

    dead_rows = sum(1 for options in subset_to_block_ids if not options)
    if dead_rows > 0:
        summary["status"] = "infeasible_residual"
        summary["reason"] = "some uncovered subsets have no feasible additive block"
    else:
        summary["status"] = "ready"
        summary["reason"] = "residual exact-cover instance built"

    summary.update(
        {
            "uncovered_subsets": [list(subset) for subset in uncovered_subsets],
            "subset_to_block_ids": subset_to_block_ids,
            "candidate_blocks": block_candidates,
            "expected_added_blocks": (
                uncovered_count // comb(q, r)
                if uncovered_count % comb(q, r) == 0
                else None
            ),
            "dead_rows": dead_rows,
        }
    )
    return summary


def _solve_exact_cover(
    subset_to_block_ids: list[list[int]],
    block_to_cover_ids: list[list[int]],
    *,
    timeout_sec: float,
    max_nodes: int,
    expected_solution_size: int | None,
) -> dict[str, Any]:
    start = time.perf_counter()
    uncovered = set(range(len(subset_to_block_ids)))
    selected: list[int] = []
    explored_nodes = 0
    timed_out = False

    def active_options(row_id: int) -> list[int]:
        options: list[int] = []
        for block_id in subset_to_block_ids[row_id]:
            if all(col in uncovered for col in block_to_cover_ids[block_id]):
                options.append(block_id)
        return options

    def dfs() -> list[int] | None:
        nonlocal explored_nodes, timed_out

        if explored_nodes >= max_nodes:
            timed_out = True
            return None
        if (time.perf_counter() - start) >= timeout_sec:
            timed_out = True
            return None

        if not uncovered:
            if expected_solution_size is None or len(selected) == expected_solution_size:
                return list(selected)
            return None

        if expected_solution_size is not None:
            per_block = len(block_to_cover_ids[0]) if block_to_cover_ids else 1
            min_additional = (len(uncovered) + per_block - 1) // per_block
            if len(selected) + min_additional > expected_solution_size:
                return None

        best_row: int | None = None
        best_options: list[int] | None = None
        for row_id in uncovered:
            options = active_options(row_id)
            if not options:
                return None
            if best_options is None or len(options) < len(best_options):
                best_row = row_id
                best_options = options
                if len(best_options) == 1:
                    break

        assert best_row is not None
        assert best_options is not None

        for block_id in best_options:
            explored_nodes += 1
            removed_rows: list[int] = []
            for row in block_to_cover_ids[block_id]:
                if row in uncovered:
                    uncovered.remove(row)
                    removed_rows.append(row)
            selected.append(block_id)

            solved = dfs()
            if solved is not None:
                return solved

            selected.pop()
            for row in removed_rows:
                uncovered.add(row)

        return None

    solution = dfs()
    return {
        "solution": solution,
        "explored_nodes": explored_nodes,
        "timeout": timed_out,
        "runtime_sec": round(time.perf_counter() - start, 6),
    }


def attempt_additive_residual_repair(
    instance: dict[str, int],
    certificate: list[list[int]],
    *,
    timeout_sec: float = 20.0,
    max_nodes: int = 200_000,
    max_total_r_subsets: int = 5_000_000,
    max_uncovered_r_subsets: int = 20_000,
    max_q_subset_scan: int = 2_000_000,
    max_candidate_blocks: int = 400_000,
) -> dict[str, Any]:
    residual = build_additive_residual_exact_cover(
        instance,
        certificate,
        max_total_r_subsets=max_total_r_subsets,
        max_uncovered_r_subsets=max_uncovered_r_subsets,
        max_q_subset_scan=max_q_subset_scan,
        max_candidate_blocks=max_candidate_blocks,
    )

    outcome: dict[str, Any] = {
        "status": residual["status"],
        "reason": residual["reason"],
        "instance": residual["instance"],
        "metrics": residual["metrics"],
    }

    if residual["status"] != "ready":
        return outcome

    block_to_cover_ids = [
        [int(v) for v in candidate["cover_indices"]]
        for candidate in residual["candidate_blocks"]
    ]
    solve = _solve_exact_cover(
        residual["subset_to_block_ids"],
        block_to_cover_ids,
        timeout_sec=timeout_sec,
        max_nodes=max_nodes,
        expected_solution_size=residual["expected_added_blocks"],
    )

    outcome.update(
        {
            "solver": {
                "explored_nodes": solve["explored_nodes"],
                "timeout": solve["timeout"],
                "runtime_sec": solve["runtime_sec"],
                "expected_added_blocks": residual["expected_added_blocks"],
            }
        }
    )

    solution = solve["solution"]
    if solution is None:
        outcome["status"] = "search_exhausted"
        if solve["timeout"]:
            outcome["reason"] = "residual exact-cover search hit limits"
        else:
            outcome["reason"] = "no additive residual completion found"
        return outcome

    added_blocks = [
        residual["candidate_blocks"][block_id]["block"]
        for block_id in solution
    ]
    repaired_candidate = list(certificate) + added_blocks
    repaired_report = evaluate_steiner_system(instance, repaired_candidate)

    outcome.update(
        {
            "status": "solved",
            "reason": "residual exact-cover completion found",
            "added_block_count": len(added_blocks),
            "added_blocks": added_blocks,
            "repaired_candidate": repaired_candidate,
            "repaired_evaluation": repaired_report,
        }
    )
    return outcome


def _parse_instance_json(raw: str) -> dict[str, int]:
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("instance must decode to a JSON object")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Residual exact-cover repair helper for Steiner search")
    parser.add_argument("--instance-json", required=True)
    parser.add_argument("--candidate-file", required=True)
    parser.add_argument("--output-file", default=None)
    parser.add_argument("--timeout-sec", type=float, default=20.0)
    parser.add_argument("--max-nodes", type=int, default=200_000)
    parser.add_argument("--max-total-r-subsets", type=int, default=5_000_000)
    parser.add_argument("--max-uncovered-r-subsets", type=int, default=20_000)
    parser.add_argument("--max-q-subset-scan", type=int, default=2_000_000)
    parser.add_argument("--max-candidate-blocks", type=int, default=400_000)
    args = parser.parse_args()

    instance = _parse_instance_json(args.instance_json)
    certificate = json.loads(Path(args.candidate_file).read_text(encoding="utf-8"))
    if not isinstance(certificate, list):
        raise ValueError("candidate file must contain a JSON list")

    result = attempt_additive_residual_repair(
        instance,
        certificate,
        timeout_sec=args.timeout_sec,
        max_nodes=args.max_nodes,
        max_total_r_subsets=args.max_total_r_subsets,
        max_uncovered_r_subsets=args.max_uncovered_r_subsets,
        max_q_subset_scan=args.max_q_subset_scan,
        max_candidate_blocks=args.max_candidate_blocks,
    )

    if args.output_file and result.get("status") == "solved":
        Path(args.output_file).write_text(
            json.dumps(result["repaired_candidate"], indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
