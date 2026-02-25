# Existence Frontier Report

Generated from log root: `steiner_logs_smoke_round1paper`
Search domain: all `n > q > r > 5`, `r < 10`, `n < 200`.

## Status semantics
- `impossible_divisibility`: ruled out by necessary Steiner divisibility constraints.
- `exists_certificate`: at least one valid certificate found in run logs.
- `unknown`: admissible but not yet solved in this repository.

## Global counts
- Total triples scanned: 72964
- Divisibility-impossible: 72710
- Admissible: 254
- Exists (certificate found): 0
- Unknown admissible: 254

## Per-r breakdown
| r | total | admissible | divisibility-impossible | exists_certificate | unknown_admissible |
|---:|---:|---:|---:|---:|---:|
| 6 | 18528 | 67 | 18461 | 0 | 67 |
| 7 | 18336 | 65 | 18271 | 0 | 65 |
| 8 | 18145 | 63 | 18082 | 0 | 63 |
| 9 | 17955 | 59 | 17896 | 0 | 59 |

## Suggested next portfolio picks
- r=6: S(6,7,23) expected_blocks=14421
- r=7: S(7,8,20) expected_blocks=9690
- r=8: S(8,9,19) expected_blocks=8398
- r=9: S(9,10,20) expected_blocks=16796

## Top unresolved admissible (top 20)
| instance | expected_blocks | attempts | best_score | best_coverage |
|---|---:|---:|---:|---:|
| S(6,7,17) | 1768 | 0 | 0.00 | 0.000000 |
| S(6,7,19) | 3876 | 0 | 0.00 | 0.000000 |
| S(7,8,18) | 3978 | 0 | 0.00 | 0.000000 |
| S(8,9,19) | 8398 | 0 | 0.00 | 0.000000 |
| S(7,8,20) | 9690 | 0 | 0.00 | 0.000000 |
| S(6,7,23) | 14421 | 0 | 0.00 | 0.000000 |
| S(9,10,20) | 16796 | 0 | 0.00 | 0.000000 |
| S(6,8,29) | 16965 | 0 | 0.00 | 0.000000 |
| S(8,9,21) | 22610 | 0 | 0.00 | 0.000000 |
| S(6,7,25) | 25300 | 0 | 0.00 | 0.000000 |
| S(7,8,24) | 43263 | 0 | 0.00 | 0.000000 |
| S(9,10,22) | 49742 | 0 | 0.00 | 0.000000 |
| S(7,9,30) | 56550 | 0 | 0.00 | 0.000000 |
| S(6,7,29) | 67860 | 0 | 0.00 | 0.000000 |
| S(7,8,26) | 82225 | 0 | 0.00 | 0.000000 |
| S(6,9,45) | 96965 | 0 | 0.00 | 0.000000 |
| S(6,12,68) | 118456 | 0 | 0.00 | 0.000000 |
| S(8,9,25) | 120175 | 0 | 0.00 | 0.000000 |
| S(8,10,31) | 175305 | 0 | 0.00 | 0.000000 |
| S(6,7,35) | 231880 | 0 | 0.00 | 0.000000 |

## Top solved admissible (top 20)
- none
