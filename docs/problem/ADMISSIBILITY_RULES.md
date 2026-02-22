# Admissibility Rules

For `S(r,q,n)`, required divisibility constraints:

`C(q-i, r-i)` divides `C(n-i, r-i)` for all `i = 0..r-1`.

Derived required quantities:
- block count: `b = C(n,r) / C(q,r)`
- multiplicities: `lambda_i = C(n-i, r-i) / C(q-i, r-i)`

Any failure marks the instance as `impossible_divisibility`.
