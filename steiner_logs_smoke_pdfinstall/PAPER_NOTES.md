# Local Paper Notes

Generated (UTC): 2026-02-22T09:57:49.107430+00:00
Papers directory: /root/openquestions/papers

## Intent
- Keep reusable local-paper reasoning so round1 focuses on proof strategy, not repeated link collection.
- Prioritize method transfer from local PDFs into solver architecture and proof artifacts.

## Computational and Theoretical Roadmap for Steiner Systems with Strength 6–9 and n _ 200.pdf
- Parsed title hint: Computational and Theoretical Roadmap for
- Extraction method: pdftotext-layout
- Extraction size ratio: text_bytes=39163, pdf_bytes=136950, ratio=0.286
- Transfer methods to apply in Steiner loop:
  - No high-confidence strategy hits extracted; inspect paper manually.
- Prompting strategy excerpt:
  - symmetry templates (affine/projective planes, nets, etc.), which can still be useful in your regime through

## arxiv_1401.3665.pdf
- Parsed title hint: The existence of designs
- Extraction method: pdftotext-layout
- Extraction size ratio: text_bytes=242725, pdf_bytes=964364, ratio=0.252
- Transfer methods to apply in Steiner loop:
  - No high-confidence strategy hits extracted; inspect paper manually.
- Prompting strategy excerpt:
  - of possible local modifications. We treat this partial decomposition as a template for the final
  - partial decomposition that covers all edges not in the template, which also spills over slightly into
  - the template, so that every edge is covered once or twice, and very few edges are covered twice (we
  - call the latter the ‘spill’). The crucial point is that the choice of the template was such that the spill
  - its basic form) as applied to the problem of designs, the analogue of our template would be a random
  - Nevertheless, we will see that a suitable algebraically defined template has a dense well-distributed
  - template via a suitable local modification. Our template can be thought of as a general absorber,
  - We further ensure that each positive clique can be absorbed into the template, via a series of
  - x+y template. These may be swapped with the
  - template of a graph G in [42], we randomly embed V (G) in F2a for some a such that 2a is not much

## arxiv_1611.06827.pdf
- Parsed title hint: THE EXISTENCE OF DESIGNS VIA ITERATIVE ABSORPTION:
- Extraction method: pdftotext-layout
- Extraction size ratio: text_bytes=494728, pdf_bytes=1287434, ratio=0.384
- Transfer methods to apply in Steiner loop:
  - No high-confidence strategy hits extracted; inspect paper manually.
- Prompting strategy excerpt:
  - verify the conditions of Lemma 11.9.

## oai_first_proof.pdf
- Parsed title hint: First Proof?
- Extraction method: pdftotext-layout
- Extraction size ratio: text_bytes=299942, pdf_bytes=928401, ratio=0.323
- Transfer methods to apply in Steiner loop:
  - Seed-idea fanout before solving (multiple independent approaches).
  - Bounded verify-revise loops (up to 3 rounds).
  - Final proof artifact pass after verification.
  - Use barrier-potential arguments and matrix-normalization as proof skeleton.
- Prompting strategy excerpt:
  - tasks posted on February 5th, 2026. All presented attempts were generated and typeset by
  - compatibly from the outset, and then verify that the resulting Lagrangian isotopy has vanishing
  - • Generate a small number of seed ideas.
  - • Prompt the model to solve the given problem using each of the seed ideas.
  - • Repeat up to 3 times:
  - – Verify (i) correctness of the proof and (ii) validity of any cited material and biblio-
  - – If gaps are found, prompt the model to revise the drafted solution.
  - • If the verifications pass, typeset the resulting solution.
  - A.2 Prompt templates
  - A.2.1 Generate ideas template

## Round1 Writing Rules
- Write reasoning-first content: proof skeleton, lemma plan, verification checkpoints, failure modes.
- Keep external links minimal and only when they unlock a missing step.
- Carry over reusable method templates from these local notes before doing new web search.

