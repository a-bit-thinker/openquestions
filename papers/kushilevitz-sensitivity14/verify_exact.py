"""Verify the stated finite Boolean-function identities, not the open existence question."""

import json
import sys


SCHEMA = "degree-sensitivity-shape-claims-verifier/v1"
DESIGN = (
    (0, 1, 3),
    (0, 1, 4),
    (0, 2, 4),
    (0, 2, 5),
    (0, 3, 5),
    (3, 4, 5),
    (1, 4, 5),
    (1, 2, 5),
    (1, 2, 3),
    (2, 3, 4),
)
BLOCKS = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (9, 10, 11),
)


def _bits(mask, count):
    return tuple((mask >> index) & 1 for index in range(count))


def _popcount(mask):
    return bin(mask).count("1")


def _nae3(a, b, c):
    return a + b + c - a * b - a * c - b * c


def _k_value(values):
    linear = sum(values)
    quadratic = sum(
        values[left] * values[right]
        for left in range(6)
        for right in range(left + 1, 6)
    )
    cubic = sum(values[a] * values[b] * values[c] for a, b, c in DESIGN)
    return linear - quadratic + cubic


def _block_values(values):
    return tuple(_nae3(*(values[index] for index in block)) for block in BLOCKS)


def _mobius(truth, variable_count):
    coefficients = truth.copy()
    for bit in range(variable_count):
        bit_mask = 1 << bit
        for mask in range(1 << variable_count):
            if mask & bit_mask:
                coefficients[mask] -= coefficients[mask ^ bit_mask]
    return coefficients


def _degree(coefficients):
    return max(
        (_popcount(mask) for mask, coefficient in enumerate(coefficients) if coefficient),
        default=-1,
    )


def _profile(coefficients):
    profile = {}
    for mask, coefficient in enumerate(coefficients):
        if coefficient:
            degree = _popcount(mask)
            profile.setdefault(degree, {})[coefficient] = (
                profile.setdefault(degree, {}).get(coefficient, 0) + 1
            )
    return profile


def _json_profile(profile):
    return {
        str(degree): {
            str(coefficient): count
            for coefficient, count in sorted(profile[degree].items())
        }
        for degree in sorted(profile)
    }


def _origin_sensitivity(truth, variable_count):
    origin = truth[0]
    return sum(truth[1 << bit] != origin for bit in range(variable_count))


def _support_at_degree(coefficients, degree):
    return {
        mask: coefficient
        for mask, coefficient in enumerate(coefficients)
        if _popcount(mask) == degree and coefficient
    }


def _pair_masks(block):
    return tuple(
        (1 << block[left]) | (1 << block[right])
        for left in range(3)
        for right in range(left + 1, 3)
    )


def _summary(truth, coefficients, variable_count):
    degree = _degree(coefficients)
    top_support = _support_at_degree(coefficients, degree)
    top_coefficients = sorted(set(top_support.values()))
    assert len(top_coefficients) == 1, "top-degree coefficients are not uniform"
    return {
        "variable_count": variable_count,
        "boolean": all(value in (0, 1) for value in truth),
        "origin_value": truth[0],
        "origin_sensitivity": _origin_sensitivity(truth, variable_count),
        "degree": degree,
        "nonzero_coefficient_count": sum(coefficient != 0 for coefficient in coefficients),
        "coefficient_profile": _json_profile(_profile(coefficients)),
        "top_support_count": len(top_support),
        "top_support_coefficient": top_coefficients[0],
    }


def _enumerate_truth_tables():
    k_truth = [_k_value(_bits(mask, 6)) for mask in range(1 << 6)]

    p_truth = []
    j0_truth = []
    q_truth = []
    for mask in range(1 << 14):
        values = _bits(mask, 14)
        g0, g1, g2, g3 = _block_values(values)
        p_value = _k_value((g0, g1, g2, g3, values[12], values[13]))
        j0_value = g1 * g3 * (g0 ^ g2)
        p_truth.append(p_value)
        j0_truth.append(j0_value)
        q_truth.append(p_value ^ j0_value)

    a_truth = []
    for mask in range(1 << 12):
        values = _bits(mask, 12)
        g0, g1, g2, unused_g3 = _block_values(values)
        assert unused_g3 in (0, 1), "NAE3 left the Boolean range"
        a_truth.append(_k_value((g0, g1, g2, values[9], values[10], values[11])))

    return k_truth, p_truth, a_truth, j0_truth, q_truth


def _verify():
    k_truth, p_truth, a_truth, j0_truth, q_truth = _enumerate_truth_tables()
    for name, truth in (
        ("K", k_truth),
        ("P", p_truth),
        ("A", a_truth),
        ("J0", j0_truth),
        ("P_xor_J0", q_truth),
    ):
        assert all(type(value) is int for value in truth), name + " did not use exact integers"

    k_coefficients = _mobius(k_truth, 6)
    p_coefficients = _mobius(p_truth, 14)
    a_coefficients = _mobius(a_truth, 12)
    j0_coefficients = _mobius(j0_truth, 14)
    q_coefficients = _mobius(q_truth, 14)

    design_masks = {
        (1 << a) | (1 << b) | (1 << c): 1 for a, b, c in DESIGN
    }
    assert all(value in (0, 1) for value in k_truth), "K is not Boolean"
    assert k_truth[0] == 0, "K is nonzero at the origin"
    assert _origin_sensitivity(k_truth, 6) == 6, "K origin sensitivity is not 6"
    assert _degree(k_coefficients) == 3, "K does not have degree 3"
    assert _support_at_degree(k_coefficients, 3) == design_masks, "K cubic design differs"

    block_pairs = tuple(_pair_masks(block) for block in BLOCKS)
    expected_p_top = {
        pair1 | pair3 | pair02: -1
        for pair1 in block_pairs[1]
        for pair3 in block_pairs[3]
        for pair02 in block_pairs[0] + block_pairs[2]
    }
    assert len(expected_p_top) == 54, "P expected top support does not have 54 masks"
    assert all(value in (0, 1) for value in p_truth), "P is not Boolean"
    assert p_truth[0] == 0, "P is nonzero at the origin"
    assert _origin_sensitivity(p_truth, 14) == 14, "P origin sensitivity is not 14"
    assert _degree(p_coefficients) == 6, "P does not have degree 6"
    assert _support_at_degree(p_coefficients, 6) == expected_p_top, (
        "P degree-6 support is not -E1*E3*(E0+E2)"
    )
    assert all(
        coefficient == 0
        for mask, coefficient in enumerate(p_coefficients)
        if _popcount(mask) > 6
    ), "P has coefficients above degree 6"

    expected_a_top = {}
    for left_block, right_block, singletons in (
        (0, 1, (9, 10)),
        (0, 2, (10, 11)),
        (1, 2, (11, 9)),
    ):
        for left_pair in block_pairs[left_block]:
            for right_pair in block_pairs[right_block]:
                for singleton in singletons:
                    expected_a_top[left_pair | right_pair | (1 << singleton)] = 1
    assert len(expected_a_top) == 54, "A expected top support does not have 54 masks"
    assert all(value in (0, 1) for value in a_truth), "A is not Boolean"
    assert a_truth[0] == 0, "A is nonzero at the origin"
    assert _origin_sensitivity(a_truth, 12) == 12, "A origin sensitivity is not 12"
    assert _degree(a_coefficients) == 5, "A does not have degree 5"
    assert _support_at_degree(a_coefficients, 5) == expected_a_top, (
        "A degree-5 support does not match the three stated E-products"
    )
    assert all(
        coefficient == 0
        for mask, coefficient in enumerate(a_coefficients)
        if _popcount(mask) > 5
    ), "A has coefficients above degree 5"

    expected_j0_top = {
        pair0 | pair1 | pair2 | pair3: -2
        for pair0 in block_pairs[0]
        for pair1 in block_pairs[1]
        for pair2 in block_pairs[2]
        for pair3 in block_pairs[3]
    }
    assert len(expected_j0_top) == 81, "J0 expected top support does not have 81 masks"
    assert all(value in (0, 1) for value in j0_truth), "J0 is not Boolean"
    assert j0_truth[0] == 0, "J0 is nonzero at the origin"
    assert _origin_sensitivity(j0_truth, 14) == 0, "J0 origin sensitivity is not 0"
    assert _degree(j0_coefficients) == 8, "J0 does not have degree 8"
    assert _support_at_degree(j0_coefficients, 8) == expected_j0_top, (
        "J0 degree-8 support is not -2*E0*E1*E2*E3"
    )

    expected_q_profile = {
        1: {1: 14},
        2: {-1: 91},
        3: {1: 192},
        4: {-1: 168, 2: 189},
        5: {-4: 162, -2: 702, 1: 54},
        6: {2: 972, 4: 729},
        7: {-2: 594, -4: 1296},
        8: {2: 135, 4: 1134},
        9: {-4: 486},
        10: {4: 81},
    }
    expected_q_top = {
        pair0 | pair1 | pair2 | pair3 | (1 << 12) | (1 << 13): 4
        for pair0 in block_pairs[0]
        for pair1 in block_pairs[1]
        for pair2 in block_pairs[2]
        for pair3 in block_pairs[3]
    }
    assert len(expected_q_top) == 81, "Q expected top support does not have 81 masks"
    assert all(value in (0, 1) for value in q_truth), "P XOR J0 is not Boolean"
    assert q_truth[0] == 0, "P XOR J0 is nonzero at the origin"
    assert _origin_sensitivity(q_truth, 14) == 14, (
        "P XOR J0 origin sensitivity is not 14"
    )
    assert _degree(q_coefficients) == 10, "P XOR J0 does not have degree 10"
    assert sum(coefficient != 0 for coefficient in q_coefficients) == 6999, (
        "P XOR J0 does not have 6999 nonzero coefficients"
    )
    assert _profile(q_coefficients) == expected_q_profile, (
        "P XOR J0 coefficient profile differs"
    )
    assert _support_at_degree(q_coefficients, 10) == expected_q_top, (
        "P XOR J0 degree-10 support differs"
    )
    assert all(
        coefficient == 0
        for mask, coefficient in enumerate(q_coefficients)
        if _popcount(mask) > 10
    ), "P XOR J0 has coefficients above degree 10"

    return {
        "schema": SCHEMA,
        "status": "PASS",
        "design": [list(block) for block in DESIGN],
        "construction": {
            "K": "sum(z_i)-sum(z_i*z_j)+sum(product(z_i for i in T) for T in D)",
            "NAE3": "a+b+c-a*b-a*c-b*c",
            "g_blocks": [list(block) for block in BLOCKS],
            "P": "K(g0,g1,g2,g3,x12,x13)",
            "A": "K(g0,g1,g2,x9,x10,x11)",
            "J0": "g1*g3*(g0 XOR g2)",
            "P_xor_J0": "P XOR J0",
        },
        "diagnostics": {"J0_degree": _degree(j0_coefficients)},
        "summaries": {
            "K": _summary(k_truth, k_coefficients, 6),
            "P": _summary(p_truth, p_coefficients, 14),
            "A": _summary(a_truth, a_coefficients, 12),
            "J0": _summary(j0_truth, j0_coefficients, 14),
            "P_xor_J0": _summary(q_truth, q_coefficients, 14),
        },
    }


def _emit(payload):
    sys.stdout.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")


def main():
    try:
        report = _verify()
    except AssertionError as error:
        _emit({"schema": SCHEMA, "status": "FAIL", "error": str(error)})
        return 1
    except Exception as error:
        _emit(
            {
                "schema": SCHEMA,
                "status": "FAIL",
                "error": type(error).__name__ + ": " + str(error),
            }
        )
        return 1
    _emit(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
