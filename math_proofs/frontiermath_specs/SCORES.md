# FrontierMath 14-problem scoring for iterative proof/search loops

Scoring target: likelihood that continuous technique iteration (search + verifier + stronger methods) yields useful theorem progress.

| Rank | Problem | Score (/10) | Score (/100) | Why this score |
|---:|---|---:|---:|---|
| 1 | Large Steiner Systems | 9.0 | 90 | exact combinatorial construction and verification align perfectly with code. |
| 2 | Stretched Littlewood-Richardson Coefficients | 8.8 | 88 | search + exact symbolic coefficient extraction is very automatable. |
| 3 | A Ramsey-style Problem on Hypergraphs | 8.4 | 84 | hypergraph constraints are machine-checkable and searchable. |
| 4 | Ramsey Numbers for Book Graphs | 8.3 | 83 | finite graph encodings + SAT certificates are strong. |
| 5 | Unknotting Number = 1 | 7.8 | 78 | decision procedures and counterexample tests are programmable. |
| 6 | Degree vs Sensitivity for Boolean Functions | 7.4 | 74 | boolean-function exhaustive search works for finite n. |
| 7 | Prime Factorization (GNFS constant) | 7.1 | 71 | algorithmic optimization loop is strong though asymptotic proof is hard. |
| 8 | The Arithmetic Kakeya Conjecture | 6.8 | 68 | construction search and bound computation are programmable, full proof is hard. |
| 9 | Inverse Galois (M23 polynomial) | 6.2 | 62 | candidate polynomial verification is exact once found. |
| 10 | Symplectic Ball Packing | 5.6 | 56 | numerical embeddings can be tested but full proof needs geometry theory. |
| 11 | Explicit Deformations of Algebras | 5.2 | 52 | symbolic checks help but deep structural proof remains. |
| 12 | Surface with a High Number of Singularities | 4.9 | 49 | CAS can verify candidate singularities but existence proof is subtle. |
| 13 | Apéry-style Irrationality Proofs | 4.6 | 46 | experimental sequence discovery is possible; proof certificates are difficult. |
| 14 | The 2-adic Absolute Galois Group | 3.7 | 37 | computational experiments weakly constrain full profinite presentation. |

## Interpreting limits

Programming loops can prove/disprove concrete encoded instances and find certificates/counterexamples.
They cannot by themselves establish true meta-level unprovability claims without separate formal results.
