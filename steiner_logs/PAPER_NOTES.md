# Local Paper Notes

Generated (UTC): 2026-02-21T14:40:48.832104+00:00
Papers directory: /root/openquestions/papers

## Intent
- Keep reusable local-paper reasoning so round1 focuses on proof strategy, not repeated link collection.
- Prioritize method transfer from local PDFs into solver architecture and proof artifacts.

## oai_first_proof.pdf
- Parsed title hint: First Proof?
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
  - 3 Verify (i) correctness of the proof and (ii) validity of any cited material and biblio-
  - 3 If gaps are found, prompt the model to revise the drafted solution.
  - • If the veri昀椀cations pass, typeset the resulting solution.
  - A.2 Prompt templates
  - A.2.1 Generate ideas template

## Round1 Writing Rules
- Write reasoning-first content: proof skeleton, lemma plan, verification checkpoints, failure modes.
- Keep external links minimal and only when they unlock a missing step.
- Carry over reusable method templates from these local notes before doing new web search.

