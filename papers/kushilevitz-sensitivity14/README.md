# Paper artifact

This directory contains the self-contained manuscript, one-page theorem
summary, bibliography, and exact verifier for the Kushilevitz-based
degree/sensitivity construction.

## Source files

- main.tex — complete manuscript source.
- theorem_summary.tex — one-page statement and review summary.
- references.bib — bibliography with primary-source metadata.
- verify_exact.py — standalone, standard-library-only verifier using exact
  integer truth-table evaluation and subset Möbius inversion.
- kushilevitz_sensitivity14_preprint.pdf — checked 14-page manuscript.
- kushilevitz_theorem_summary.pdf — checked one-page theorem summary.

## Generated PDFs

The checked PDFs are `kushilevitz_sensitivity14_preprint.pdf` and
`kushilevitz_theorem_summary.pdf` in this directory.

Both PDFs were built on August 15, 2026 with the official Apple Silicon
Tectonic 0.17.0 release. The downloaded release archive was verified against
the SHA-256 digest published with the GitHub release assets:

~~~text
a3f1cac7c5678f01661a92212f58480ae3b0634115d880dbc59e2953ded45667
~~~

The final compilation logs contain no LaTeX, reference, citation, or BibTeX
warnings. All 14 manuscript pages and the one-page summary were rendered with
Poppler and visually inspected.

## Verification

Run the exact verifier from this directory:

~~~sh
python3 -I verify_exact.py
~~~

It emits one deterministic JSON line and exits with status zero only when all
encoded identities and coefficient profiles pass. The checked output has
status PASS and confirms, among other claims, deg(P)=6, deg(A)=5, deg(J0)=8,
and deg(P XOR J0)=10.

## Rebuilding

With Tectonic 0.17.0 on PATH, run from this directory:

~~~sh
mkdir -p build
tectonic -X compile --untrusted --keep-logs --outdir build main.tex
tectonic -X compile --untrusted --keep-logs --outdir build theorem_summary.tex
~~~

The source filenames produce `build/main.pdf` and
`build/theorem_summary.pdf`; rename those outputs to the checked filenames
above for distribution. The first Tectonic run may download its standard TeX
resource bundle. A subsequent offline/cache-only build can add
`--only-cached`.

## Review recommendation

The manuscript makes no novelty or priority claim and states its mathematical
limitations explicitly. Before a first public upload, one thorough Boolean-
complexity assessment is a practical minimum; two independent assessments
would be stronger, ideally separating proof correctness from novelty and
literature coverage.
