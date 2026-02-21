from __future__ import annotations

from collections import Counter
from itertools import combinations
from math import comb
from typing import Any, Iterable

_RESIDUAL_REPAIR_MAX_TOTAL_R_SUBSETS = 5000000
_RESIDUAL_REPAIR_MAX_UNCOVERED_R_SUBSETS = 20000
_RESIDUAL_REPAIR_MAX_UNCOVERED_RATIO = 0.10


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _normalize_instance(instance: dict[str, Any]) -> tuple[int, int, int, list[str]]:
    issues: list[str] = []

    if not isinstance(instance, dict):
        return 0, 0, 0, ["instance must be a dict with keys: n, q, r"]

    n = instance.get("n")
    q = instance.get("q")
    r = instance.get("r")

    if not _is_int(n):
        issues.append("instance.n must be an integer")
    if not _is_int(q):
        issues.append("instance.q must be an integer")
    if not _is_int(r):
        issues.append("instance.r must be an integer")

    if issues:
        return 0, 0, 0, issues

    n = int(n)
    q = int(q)
    r = int(r)

    if n <= 0:
        issues.append("instance.n must be > 0")
    if q <= 0:
        issues.append("instance.q must be > 0")
    if r <= 0:
        issues.append("instance.r must be > 0")
    if not (n > q > r):
        issues.append("instance must satisfy n > q > r")

    return n, q, r, issues


def _divisibility_failures(n: int, q: int, r: int) -> list[dict[str, int]]:
    failures: list[dict[str, int]] = []
    for check in _admissibility_checks(n, q, r):
        if check["remainder"] != 0:
            failures.append(
                {
                    "s": check["i"],
                    "i": check["i"],
                    "numerator": check["numerator"],
                    "denominator": check["denominator"],
                    "remainder": check["remainder"],
                }
            )
    return failures


def _admissibility_checks(n: int, q: int, r: int) -> list[dict[str, int | None]]:
    checks: list[dict[str, int | None]] = []
    for i in range(r):
        numerator = comb(n - i, r - i)
        denominator = comb(q - i, r - i)
        remainder = numerator % denominator
        quotient = numerator // denominator if remainder == 0 else None
        checks.append(
            {
                "i": i,
                "numerator": numerator,
                "denominator": denominator,
                "remainder": remainder,
                "quotient": quotient,
            }
        )
    return checks


def steiner_admissibility_report(instance: dict[str, Any]) -> dict[str, Any]:
    """Return mandatory divisibility/admissibility diagnostics for S(r, q, n)."""
    n, q, r, instance_issues = _normalize_instance(instance)
    if instance_issues:
        return {
            "instance": {"n": n, "q": q, "r": r},
            "is_well_formed": False,
            "is_admissible": False,
            "issues": instance_issues,
            "checks": [],
            "divisibility_failures": [],
            "replication_numbers": {},
            "expected_block_count": None,
        }

    checks = _admissibility_checks(n, q, r)
    divisibility_failures = [
        {
            "s": int(check["i"]),
            "i": int(check["i"]),
            "numerator": int(check["numerator"]),
            "denominator": int(check["denominator"]),
            "remainder": int(check["remainder"]),
        }
        for check in checks
        if check["remainder"] != 0
    ]
    replication_numbers = {
        f"lambda_{check['i']}": int(check["quotient"])
        for check in checks
        if check["quotient"] is not None
    }
    is_admissible = not divisibility_failures
    issues = []
    if not is_admissible:
        issues.append("instance fails Steiner divisibility preconditions")

    expected_block_count = replication_numbers.get("lambda_0")
    return {
        "instance": {"n": n, "q": q, "r": r},
        "is_well_formed": True,
        "is_admissible": is_admissible,
        "issues": issues,
        "checks": checks,
        "divisibility_failures": divisibility_failures,
        "replication_numbers": replication_numbers,
        "expected_block_count": expected_block_count,
    }


def _normalize_certificate(
    certificate: Iterable[Iterable[Any]], n: int, q: int
) -> tuple[list[tuple[int, ...]], list[str], int, int]:
    issues: list[str] = []

    if not isinstance(certificate, list):
        return [], ["certificate must be a list of blocks"], 0, 0

    valid_blocks: list[tuple[int, ...]] = []
    invalid_block_count = 0

    for idx, raw_block in enumerate(certificate):
        if not isinstance(raw_block, (list, tuple)):
            issues.append(f"block[{idx}] must be a list/tuple of vertices")
            invalid_block_count += 1
            continue

        if len(raw_block) != q:
            issues.append(f"block[{idx}] must contain exactly q={q} vertices")
            invalid_block_count += 1
            continue

        if any(not _is_int(v) for v in raw_block):
            issues.append(f"block[{idx}] contains non-integer vertices")
            invalid_block_count += 1
            continue

        block_tuple = tuple(sorted(int(v) for v in raw_block))

        if len(set(block_tuple)) != q:
            issues.append(f"block[{idx}] contains duplicate vertices")
            invalid_block_count += 1
            continue

        if block_tuple[0] < 0 or block_tuple[-1] >= n:
            issues.append(f"block[{idx}] contains out-of-range vertex (valid range: 0..{n - 1})")
            invalid_block_count += 1
            continue

        valid_blocks.append(block_tuple)

    duplicate_blocks = len(valid_blocks) - len(set(valid_blocks))
    if duplicate_blocks:
        issues.append(f"certificate contains {duplicate_blocks} duplicate blocks")

    return valid_blocks, issues, invalid_block_count, duplicate_blocks


def evaluate_steiner_system(instance: dict[str, Any], certificate: list[list[int]]) -> dict[str, Any]:
    """Evaluate a candidate block system against S(r, q, n) constraints.

    Returns a structured report with exact verifier metrics and a round score (0..100).
    """
    admissibility = steiner_admissibility_report(instance)
    n = admissibility["instance"]["n"]
    q = admissibility["instance"]["q"]
    r = admissibility["instance"]["r"]
    instance_issues = [] if admissibility["is_well_formed"] else list(admissibility["issues"])

    base_report: dict[str, Any] = {
        "instance": {"n": n, "q": q, "r": r},
        "is_valid": False,
        "score": 0.0,
        "issues": list(instance_issues),
        "admissibility": admissibility,
    }

    if instance_issues:
        base_report.update(
            {
                "total_required_r_subsets": 0,
                "expected_block_count": None,
                "actual_block_count": 0,
                "unique_covered_r_subsets": 0,
                "exact_once_r_subsets": 0,
                "overcovered_r_subsets": 0,
                "uncovered_r_subsets": 0,
                "overflow_multiplicity": 0,
                "invalid_block_count": 0,
                "duplicate_block_count": 0,
                "divisibility_failures": [],
                "point_degree_min": 0,
                "point_degree_max": 0,
                "point_degree_gap": 0,
                "target_point_degree": None,
                "r_minus_1_target_degree": None,
                "r_minus_1_max_degree": 0,
                "oversubscribed_r_minus_1_subsets": 0,
                "min_additional_blocks_needed_for_uncovered": None,
                "remaining_block_slots": None,
                "additive_repair_feasible": None,
                "residual_repair_hint": {
                    "eligible": False,
                    "reason": "instance is not well-formed",
                },
            }
        )
        return base_report

    div_failures = admissibility["divisibility_failures"]
    if div_failures:
        base_report["issues"].append("instance fails Steiner divisibility preconditions")

    valid_blocks, cert_issues, invalid_block_count, duplicate_block_count = _normalize_certificate(
        certificate, n, q
    )
    base_report["issues"].extend(cert_issues)

    subset_counts: Counter[tuple[int, ...]] = Counter()
    for block in valid_blocks:
        for r_subset in combinations(block, r):
            subset_counts[r_subset] += 1

    total_required = comb(n, r)
    unique_covered = len(subset_counts)
    exact_once = sum(1 for count in subset_counts.values() if count == 1)
    overcovered = sum(1 for count in subset_counts.values() if count > 1)
    overflow_multiplicity = sum(count - 1 for count in subset_counts.values() if count > 1)
    uncovered = max(total_required - unique_covered, 0)

    expected_block_num = comb(n, r)
    expected_block_den = comb(q, r)
    expected_block_count = (
        expected_block_num // expected_block_den
        if expected_block_num % expected_block_den == 0
        else None
    )

    actual_block_count = len(valid_blocks)

    point_degrees = [0] * n
    for block in valid_blocks:
        for vertex in block:
            point_degrees[vertex] += 1
    point_degree_min = min(point_degrees) if point_degrees else 0
    point_degree_max = max(point_degrees) if point_degrees else 0
    point_degree_gap = point_degree_max - point_degree_min
    target_point_degree = admissibility["replication_numbers"].get("lambda_1")

    r_minus_1_target_degree = admissibility["replication_numbers"].get(f"lambda_{r - 1}")
    r_minus_1_counts: Counter[tuple[int, ...]] = Counter()
    for block in valid_blocks:
        for subset in combinations(block, r - 1):
            r_minus_1_counts[subset] += 1
    r_minus_1_max_degree = max(r_minus_1_counts.values(), default=0)
    oversubscribed_r_minus_1_subsets = 0
    if r_minus_1_target_degree is not None:
        oversubscribed_r_minus_1_subsets = sum(
            1 for value in r_minus_1_counts.values() if value > r_minus_1_target_degree
        )
        if oversubscribed_r_minus_1_subsets > 0:
            base_report["issues"].append(
                "certificate oversubscribes some (r-1)-subsets; completion is impossible without deletions"
            )

    has_coverage_validity = uncovered == 0 and overcovered == 0 and unique_covered == total_required
    has_structure_validity = not base_report["issues"]
    is_valid = has_structure_validity and has_coverage_validity

    coverage_ratio = exact_once / total_required if total_required else 0.0
    uncovered_ratio = uncovered / total_required if total_required else 1.0
    overflow_ratio = overflow_multiplicity / total_required if total_required else 1.0
    invalid_ratio = invalid_block_count / max(len(certificate), 1)

    if expected_block_count is None:
        block_count_penalty = 1.0
        remaining_block_slots = None
    else:
        block_count_penalty = abs(actual_block_count - expected_block_count) / max(expected_block_count, 1)
        remaining_block_slots = expected_block_count - actual_block_count

    per_block_r_coverage = comb(q, r)
    min_additional_blocks_needed_for_uncovered = (
        (uncovered + per_block_r_coverage - 1) // per_block_r_coverage if uncovered > 0 else 0
    )
    additive_repair_feasible: bool | None
    if remaining_block_slots is None:
        additive_repair_feasible = None
    else:
        additive_repair_feasible = (
            overcovered == 0 and remaining_block_slots >= min_additional_blocks_needed_for_uncovered
        )

    residual_repair_eligible = (
        overcovered == 0
        and uncovered > 0
        and actual_block_count > 0
        and total_required <= _RESIDUAL_REPAIR_MAX_TOTAL_R_SUBSETS
        and uncovered <= _RESIDUAL_REPAIR_MAX_UNCOVERED_R_SUBSETS
        and (uncovered / total_required if total_required else 1.0) <= _RESIDUAL_REPAIR_MAX_UNCOVERED_RATIO
    )
    if residual_repair_eligible:
        residual_reason = "eligible for exact residual completion"
    elif overcovered > 0:
        residual_reason = "not eligible: overcovered subsets must be repaired first"
    elif actual_block_count == 0:
        residual_reason = "not eligible: residual exact repair is for late-stage candidates, not empty starts"
    elif uncovered == 0:
        residual_reason = "not needed: no uncovered subsets remain"
    elif total_required > _RESIDUAL_REPAIR_MAX_TOTAL_R_SUBSETS:
        residual_reason = "not eligible: instance too large for built-in residual exact repair budget"
    elif (uncovered / total_required if total_required else 1.0) > _RESIDUAL_REPAIR_MAX_UNCOVERED_RATIO:
        residual_reason = "not eligible: uncovered fraction is too large; use constructive search first"
    else:
        residual_reason = "not eligible: uncovered residual too large for exact repair budget"

    raw_score = (
        coverage_ratio
        - 0.60 * overflow_ratio
        - 0.30 * uncovered_ratio
        - 0.15 * invalid_ratio
        - 0.10 * min(block_count_penalty, 1.0)
    )
    score = round(max(0.0, min(1.0, raw_score)) * 100.0, 2)
    if is_valid:
        score = 100.0

    base_report.update(
        {
            "is_valid": is_valid,
            "score": score,
            "total_required_r_subsets": total_required,
            "expected_block_count": expected_block_count,
            "actual_block_count": actual_block_count,
            "unique_covered_r_subsets": unique_covered,
            "exact_once_r_subsets": exact_once,
            "overcovered_r_subsets": overcovered,
            "uncovered_r_subsets": uncovered,
            "overflow_multiplicity": overflow_multiplicity,
            "invalid_block_count": invalid_block_count,
            "duplicate_block_count": duplicate_block_count,
            "divisibility_failures": div_failures,
            "coverage_ratio": round(coverage_ratio, 6),
            "point_degree_min": point_degree_min,
            "point_degree_max": point_degree_max,
            "point_degree_gap": point_degree_gap,
            "target_point_degree": target_point_degree,
            "r_minus_1_target_degree": r_minus_1_target_degree,
            "r_minus_1_max_degree": r_minus_1_max_degree,
            "oversubscribed_r_minus_1_subsets": oversubscribed_r_minus_1_subsets,
            "min_additional_blocks_needed_for_uncovered": min_additional_blocks_needed_for_uncovered,
            "remaining_block_slots": remaining_block_slots,
            "additive_repair_feasible": additive_repair_feasible,
            "residual_repair_hint": {
                "eligible": residual_repair_eligible,
                "reason": residual_reason,
            },
        }
    )

    return base_report


def verify_steiner_system(instance: dict[str, Any], certificate: list[list[int]]) -> bool:
    """Return True iff the certificate is a valid Steiner system S(r, q, n)."""
    return bool(evaluate_steiner_system(instance, certificate)["is_valid"])


def full_question_constraint_issues(instance: dict[str, Any]) -> list[str]:
    """Validate the frontier-task constraints from the prompt."""
    n, q, r, issues = _normalize_instance(instance)
    if issues:
        return issues

    prompt_issues: list[str] = []
    if not (n < 200):
        prompt_issues.append("full-task constraint failed: n must be < 200")
    if not (r < 10):
        prompt_issues.append("full-task constraint failed: r must be < 10")
    if not (r > 5):
        prompt_issues.append("full-task constraint failed: r must be > 5")
    return prompt_issues


def parse_steiner_submission_text(
    submission: str,
) -> tuple[dict[str, int], list[list[int]], list[str]]:
    """Parse prompt-format submission text into instance + 0-based certificate.

    Expected format:
    - First non-empty line: #n,q,r
    - Remaining non-empty lines: q integers in [1, n], space-separated
    """
    issues: list[str] = []

    if not isinstance(submission, str):
        return {"n": 0, "q": 0, "r": 0}, [], ["submission must be a string"]

    lines = [line.strip() for line in submission.splitlines() if line.strip()]
    if not lines:
        return {"n": 0, "q": 0, "r": 0}, [], ["submission is empty"]

    header = lines[0]
    if not header.startswith("#"):
        return {"n": 0, "q": 0, "r": 0}, [], ["first line must start with '#' as '#n,q,r'"]

    header_parts = [part.strip() for part in header[1:].split(",")]
    if len(header_parts) != 3:
        return {"n": 0, "q": 0, "r": 0}, [], ["header must be exactly '#n,q,r'"]

    try:
        n, q, r = (int(header_parts[0]), int(header_parts[1]), int(header_parts[2]))
    except ValueError:
        return {"n": 0, "q": 0, "r": 0}, [], ["header values n,q,r must be integers"]

    instance = {"n": n, "q": q, "r": r}
    _, _, _, instance_issues = _normalize_instance(instance)
    if instance_issues:
        return instance, [], instance_issues

    certificate_zero_based: list[list[int]] = []
    for i, line in enumerate(lines[1:], start=2):
        parts = line.split()
        if len(parts) != q:
            issues.append(f"line {i}: expected exactly q={q} integers")
            continue

        try:
            values = [int(token) for token in parts]
        except ValueError:
            issues.append(f"line {i}: all block elements must be integers")
            continue

        if any(v < 1 or v > n for v in values):
            issues.append(f"line {i}: all block elements must be in [1, {n}]")
            continue

        certificate_zero_based.append([v - 1 for v in values])

    return instance, certificate_zero_based, issues


def evaluate_steiner_submission_text(
    submission: str,
    enforce_full_question_constraints: bool = False,
) -> dict[str, Any]:
    """Evaluate a text submission in prompt format.

    - Returns evaluator metrics over the parsed (0-based) internal certificate.
    - `task_valid` means it satisfies both Steiner validity and requested prompt constraints.
    """
    instance, certificate, format_issues = parse_steiner_submission_text(submission)

    report = evaluate_steiner_system(instance, certificate)
    constraint_issues = (
        full_question_constraint_issues(instance) if enforce_full_question_constraints else []
    )

    steiner_valid = bool(report["is_valid"])
    task_valid = steiner_valid and not format_issues and not constraint_issues

    merged_issues = list(dict.fromkeys(format_issues + constraint_issues + report["issues"]))
    report["format_issues"] = format_issues
    report["constraint_issues"] = constraint_issues
    report["steiner_valid"] = steiner_valid
    report["task_valid"] = task_valid
    report["task_score"] = 100.0 if task_valid else 0.0
    report["is_valid"] = task_valid
    report["issues"] = merged_issues
    return report


def verify_steiner_submission_text(
    submission: str,
    enforce_full_question_constraints: bool = False,
) -> bool:
    """Return True iff a prompt-format submission is task-valid."""
    return bool(
        evaluate_steiner_submission_text(
            submission, enforce_full_question_constraints=enforce_full_question_constraints
        )["task_valid"]
    )
