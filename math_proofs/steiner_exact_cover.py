from __future__ import annotations

import argparse
import json
import random
import time
from itertools import combinations
from math import comb
from pathlib import Path
from typing import Any

from math_proofs.steiner_system import evaluate_steiner_system, steiner_admissibility_report


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


def _build_exact_cover_matrix(n: int, q: int, r: int) -> dict[str, Any]:
    row_subsets = list(combinations(range(n), r))
    row_index = {subset: i for i, subset in enumerate(row_subsets)}

    option_blocks: list[tuple[int, ...]] = []
    option_rows: list[tuple[int, ...]] = []
    row_to_options: list[list[int]] = [[] for _ in row_subsets]

    for block in combinations(range(n), q):
        rows = tuple(row_index[subset] for subset in combinations(block, r))
        option_id = len(option_blocks)
        option_blocks.append(block)
        option_rows.append(rows)
        for row_id in rows:
            row_to_options[row_id].append(option_id)

    return {
        "row_subsets": row_subsets,
        "row_to_options": row_to_options,
        "option_blocks": option_blocks,
        "option_rows": option_rows,
        "block_to_option": {block: i for i, block in enumerate(option_blocks)},
    }


def _select_conflict_free_option_ids(
    option_ids: list[int],
    option_rows: list[tuple[int, ...]],
) -> list[int]:
    seen_rows: set[int] = set()
    selected: list[int] = []
    for option_id in option_ids:
        rows = option_rows[option_id]
        if any(row in seen_rows for row in rows):
            continue
        selected.append(option_id)
        seen_rows.update(rows)
    return selected


def _algorithm_x(
    row_to_options: list[list[int]],
    option_rows: list[tuple[int, ...]],
    *,
    fixed_option_ids: list[int] | None = None,
    time_limit_sec: float = 60.0,
    max_nodes: int = 1_000_000,
    random_seed: int | None = None,
) -> dict[str, Any]:
    rng = random.Random(random_seed)
    start = time.perf_counter()

    num_rows = len(row_to_options)
    num_options = len(option_rows)

    uncovered: set[int] = set(range(num_rows))
    active = [True] * num_options
    selected: list[int] = []
    nodes = 0
    timed_out = False

    static_option_weight = [sum(len(row_to_options[row]) for row in option_rows[i]) for i in range(num_options)]

    def choose_option(option_id: int) -> tuple[list[int], list[int]] | None:
        if not active[option_id]:
            return None
        rows = option_rows[option_id]
        if any(row not in uncovered for row in rows):
            return None

        removed_rows: list[int] = []
        removed_options: list[int] = []

        for row in rows:
            uncovered.remove(row)
            removed_rows.append(row)
            for other in row_to_options[row]:
                if active[other]:
                    active[other] = False
                    removed_options.append(other)

        selected.append(option_id)
        return removed_rows, removed_options

    def undo(removed_rows: list[int], removed_options: list[int]) -> None:
        selected.pop()
        for option_id in reversed(removed_options):
            active[option_id] = True
        for row in reversed(removed_rows):
            uncovered.add(row)

    if fixed_option_ids:
        for option_id in fixed_option_ids:
            state = choose_option(option_id)
            if state is None:
                return {
                    "status": "infeasible",
                    "reason": "fixed options conflict",
                    "solution_option_ids": None,
                    "runtime_sec": round(time.perf_counter() - start, 6),
                    "nodes": 0,
                    "timeout": False,
                }

    def dfs() -> list[int] | None:
        nonlocal nodes, timed_out

        if nodes >= max_nodes:
            timed_out = True
            return None
        if (time.perf_counter() - start) >= time_limit_sec:
            timed_out = True
            return None
        if not uncovered:
            return list(selected)

        best_row = -1
        best_options: list[int] | None = None

        for row in uncovered:
            options = [option_id for option_id in row_to_options[row] if active[option_id]]
            if not options:
                return None
            if best_options is None or len(options) < len(best_options):
                best_row = row
                best_options = options
                if len(best_options) == 1:
                    break

        assert best_row >= 0
        assert best_options is not None

        best_options.sort(key=lambda option_id: static_option_weight[option_id])
        if len(best_options) > 2:
            # Light randomized tie-shake for restart diversity.
            head = best_options[:2]
            tail = best_options[2:]
            rng.shuffle(tail)
            best_options = head + tail

        for option_id in best_options:
            state = choose_option(option_id)
            if state is None:
                continue
            nodes += 1

            found = dfs()
            if found is not None:
                return found

            undo(state[0], state[1])

        return None

    solution = dfs()

    if solution is not None:
        status = "solved"
        reason = "exact cover found"
    elif timed_out:
        status = "search_exhausted"
        reason = "time/node budget reached"
    else:
        status = "search_exhausted"
        reason = "no exact cover under explored tree"

    return {
        "status": status,
        "reason": reason,
        "solution_option_ids": solution,
        "runtime_sec": round(time.perf_counter() - start, 6),
        "nodes": nodes,
        "timeout": timed_out,
    }


def _conflict_free_greedy_pack(
    row_to_options: list[list[int]],
    option_rows: list[tuple[int, ...]],
    option_blocks: list[tuple[int, ...]],
    *,
    initial_option_ids: list[int],
    n: int,
    target_point_degree: int | None,
    target_block_count: int | None,
    time_limit_sec: float = 20.0,
    sample_size: int = 256,
    random_seed: int | None = None,
) -> dict[str, Any]:
    rng = random.Random(random_seed)
    start = time.perf_counter()

    active: set[int] = set(range(len(option_rows)))
    covered_rows: set[int] = set()
    selected: list[int] = []
    point_deg = [0] * n

    def remove_option_if_active(option_id: int) -> None:
        if option_id in active:
            active.remove(option_id)

    def pick_option(option_id: int) -> bool:
        rows = option_rows[option_id]
        if any(row in covered_rows for row in rows):
            return False

        selected.append(option_id)
        for v in option_blocks[option_id]:
            point_deg[v] += 1

        for row in rows:
            covered_rows.add(row)
            for other in row_to_options[row]:
                remove_option_if_active(other)

        return True

    for option_id in initial_option_ids:
        ok = pick_option(option_id)
        if not ok:
            continue

    while active and (time.perf_counter() - start) < time_limit_sec:
        if target_block_count is not None and len(selected) >= target_block_count:
            break

        pool = list(active)
        if not pool:
            break

        if len(pool) > sample_size:
            sample = rng.sample(pool, sample_size)
        else:
            sample = pool

        best_option = None
        best_score = None

        for option_id in sample:
            rows = option_rows[option_id]
            if any(row in covered_rows for row in rows):
                continue

            # Lower score is better. This keeps point degrees balanced.
            if target_point_degree is None:
                score = sum(point_deg[v] for v in option_blocks[option_id])
            else:
                score = 0
                for v in option_blocks[option_id]:
                    next_deg = point_deg[v] + 1
                    score += abs(next_deg - target_point_degree)

            tie = rng.random() * 1e-6
            ranked = score + tie
            if best_score is None or ranked < best_score:
                best_score = ranked
                best_option = option_id

        if best_option is None:
            break

        if not pick_option(best_option):
            active.discard(best_option)

    return {
        "selected_option_ids": selected,
        "covered_rows": len(covered_rows),
        "total_rows": len(row_to_options),
        "runtime_sec": round(time.perf_counter() - start, 6),
    }


def solve_steiner_exact_cover(
    instance: dict[str, int],
    certificate: list[list[int]],
    *,
    time_limit_sec: float = 120.0,
    max_nodes: int = 1_000_000,
    full_exact_max_rows: int = 20_000,
    full_exact_max_options: int = 50_000,
    use_symmetry_break: bool = True,
    random_seed: int | None = None,
) -> dict[str, Any]:
    admiss = steiner_admissibility_report(instance)
    n = int(admiss["instance"]["n"])
    q = int(admiss["instance"]["q"])
    r = int(admiss["instance"]["r"])

    if not admiss["is_well_formed"]:
        return {
            "status": "invalid_instance",
            "reason": "; ".join(admiss["issues"]),
            "instance": {"n": n, "q": q, "r": r},
        }

    if not admiss["is_admissible"]:
        return {
            "status": "inadmissible",
            "reason": "instance fails divisibility constraints",
            "instance": {"n": n, "q": q, "r": r},
            "divisibility_failures": admiss["divisibility_failures"],
        }

    report = evaluate_steiner_system(instance, certificate)
    if report["is_valid"]:
        return {
            "status": "already_valid",
            "reason": "candidate already satisfies Steiner constraints",
            "instance": {"n": n, "q": q, "r": r},
            "candidate": certificate,
            "evaluation": report,
        }

    if report["invalid_block_count"] > 0:
        return {
            "status": "invalid_candidate",
            "reason": "candidate has invalid blocks",
            "instance": {"n": n, "q": q, "r": r},
            "evaluation": report,
        }

    matrix = _build_exact_cover_matrix(n, q, r)
    row_count = len(matrix["row_subsets"])
    option_count = len(matrix["option_blocks"])

    if row_count > 250_000 or option_count > 500_000:
        return {
            "status": "too_large",
            "reason": "exact-cover matrix exceeds hard budget",
            "instance": {"n": n, "q": q, "r": r},
            "matrix_shape": {"rows": row_count, "options": option_count},
            "evaluation": report,
        }

    cert_blocks = _normalize_blocks(certificate, n, q)
    option_ids = [
        matrix["block_to_option"][block]
        for block in cert_blocks
        if block in matrix["block_to_option"]
    ]
    # Keep only a conflict-free seed so exact completion remains feasible.
    seed_option_ids = _select_conflict_free_option_ids(option_ids, matrix["option_rows"])

    canonical_option_ids: list[int] = []
    if use_symmetry_break and not seed_option_ids:
        canonical = tuple(range(q))
        canonical_option = matrix["block_to_option"].get(canonical)
        if canonical_option is not None:
            canonical_option_ids = [canonical_option]

    start = time.perf_counter()

    prefer_full_exact = row_count <= full_exact_max_rows and option_count <= full_exact_max_options
    full_exact_attempt: dict[str, Any] | None = None
    if prefer_full_exact:
        fixed = canonical_option_ids + seed_option_ids
        full_exact_budget = max(1.0, time_limit_sec * 0.65)
        solve = _algorithm_x(
            matrix["row_to_options"],
            matrix["option_rows"],
            fixed_option_ids=fixed,
            time_limit_sec=full_exact_budget,
            max_nodes=max_nodes,
            random_seed=random_seed,
        )

        if solve["solution_option_ids"] is not None:
            solved_blocks = [
                list(matrix["option_blocks"][option_id]) for option_id in solve["solution_option_ids"]
            ]
            solved_report = evaluate_steiner_system(instance, solved_blocks)
            return {
                "status": "solved",
                "reason": solve["reason"],
                "instance": {"n": n, "q": q, "r": r},
                "matrix_shape": {"rows": row_count, "options": option_count},
                "engine": "full_exact_cover",
                "solver": {
                    "runtime_sec": solve["runtime_sec"],
                    "nodes": solve["nodes"],
                    "timeout": solve["timeout"],
                    "fixed_seed_blocks": len(fixed),
                },
                "candidate": solved_blocks,
                "evaluation": solved_report,
            }

        full_exact_attempt = {
            "status": solve["status"],
            "reason": solve["reason"],
            "solver": {
                "runtime_sec": solve["runtime_sec"],
                "nodes": solve["nodes"],
                "timeout": solve["timeout"],
                "fixed_seed_blocks": len(fixed),
            },
        }

    # Hybrid fallback: conflict-free greedy packing, then exact completion on remaining rows.
    elapsed = time.perf_counter() - start
    remaining_total = max(0.0, time_limit_sec - elapsed)
    if remaining_total < 1.0:
        return {
            "status": "search_exhausted",
            "reason": "time budget exhausted before hybrid fallback",
            "instance": {"n": n, "q": q, "r": r},
            "matrix_shape": {"rows": row_count, "options": option_count},
            "engine": "full_exact_cover" if prefer_full_exact else "hybrid_conflict_free_then_exact",
            "full_exact_attempt": full_exact_attempt,
            "evaluation": report,
        }

    greedy_budget = max(0.5, min(remaining_total * 0.35, remaining_total * 0.8))
    greedy = _conflict_free_greedy_pack(
        matrix["row_to_options"],
        matrix["option_rows"],
        matrix["option_blocks"],
        initial_option_ids=seed_option_ids,
        n=n,
        target_point_degree=admiss["replication_numbers"].get("lambda_1"),
        target_block_count=admiss.get("expected_block_count"),
        time_limit_sec=greedy_budget,
        sample_size=512,
        random_seed=random_seed,
    )

    greedy_blocks = [
        list(matrix["option_blocks"][option_id]) for option_id in greedy["selected_option_ids"]
    ]
    greedy_report = evaluate_steiner_system(instance, greedy_blocks)

    remaining = max(0.0, time_limit_sec - (time.perf_counter() - start))
    if remaining < 1.0:
        result = {
            "status": "search_exhausted",
            "reason": "time budget exhausted after conflict-free greedy stage",
            "instance": {"n": n, "q": q, "r": r},
            "matrix_shape": {"rows": row_count, "options": option_count},
            "engine": "hybrid_conflict_free_then_exact",
            "greedy": greedy,
            "candidate": greedy_blocks,
            "evaluation": greedy_report,
        }
        if full_exact_attempt is not None:
            result["full_exact_attempt"] = full_exact_attempt
        return result

    exact = _algorithm_x(
        matrix["row_to_options"],
        matrix["option_rows"],
        fixed_option_ids=greedy["selected_option_ids"],
        time_limit_sec=remaining,
        max_nodes=max_nodes,
        random_seed=random_seed,
    )

    if exact["solution_option_ids"] is not None:
        solved_blocks = [
            list(matrix["option_blocks"][option_id]) for option_id in exact["solution_option_ids"]
        ]
        solved_report = evaluate_steiner_system(instance, solved_blocks)
        result = {
            "status": "solved",
            "reason": exact["reason"],
            "instance": {"n": n, "q": q, "r": r},
            "matrix_shape": {"rows": row_count, "options": option_count},
            "engine": "hybrid_conflict_free_then_exact",
            "greedy": greedy,
            "solver": {
                "runtime_sec": exact["runtime_sec"],
                "nodes": exact["nodes"],
                "timeout": exact["timeout"],
            },
            "candidate": solved_blocks,
            "evaluation": solved_report,
        }
        if full_exact_attempt is not None:
            result["full_exact_attempt"] = full_exact_attempt
        return result

    result = {
        "status": exact["status"],
        "reason": exact["reason"],
        "instance": {"n": n, "q": q, "r": r},
        "matrix_shape": {"rows": row_count, "options": option_count},
        "engine": "hybrid_conflict_free_then_exact",
        "greedy": greedy,
        "solver": {
            "runtime_sec": exact["runtime_sec"],
            "nodes": exact["nodes"],
            "timeout": exact["timeout"],
        },
        "candidate": greedy_blocks,
        "evaluation": greedy_report,
    }
    if full_exact_attempt is not None:
        result["full_exact_attempt"] = full_exact_attempt
    return result


def _parse_instance_json(raw: str) -> dict[str, int]:
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("instance must decode to a JSON object")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Exact-cover-first Steiner solver")
    parser.add_argument("--instance-json", required=True)
    parser.add_argument("--candidate-file", required=True)
    parser.add_argument("--output-file", default=None)
    parser.add_argument("--time-limit-sec", type=float, default=120.0)
    parser.add_argument("--max-nodes", type=int, default=1_000_000)
    parser.add_argument("--full-exact-max-rows", type=int, default=20_000)
    parser.add_argument("--full-exact-max-options", type=int, default=50_000)
    parser.add_argument("--random-seed", type=int, default=0)
    parser.add_argument("--no-symmetry-break", action="store_true")
    args = parser.parse_args()

    instance = _parse_instance_json(args.instance_json)
    candidate = json.loads(Path(args.candidate_file).read_text(encoding="utf-8"))
    if not isinstance(candidate, list):
        raise ValueError("candidate file must contain a JSON list")

    result = solve_steiner_exact_cover(
        instance,
        candidate,
        time_limit_sec=args.time_limit_sec,
        max_nodes=args.max_nodes,
        full_exact_max_rows=args.full_exact_max_rows,
        full_exact_max_options=args.full_exact_max_options,
        use_symmetry_break=not args.no_symmetry_break,
        random_seed=args.random_seed,
    )

    if args.output_file and result.get("candidate") is not None:
        Path(args.output_file).write_text(
            json.dumps(result["candidate"], indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
