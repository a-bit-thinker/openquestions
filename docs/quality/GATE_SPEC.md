# Gate Specification

## Goal
Round close should validate structured artifacts, not only markdown wording.

Current runtime status:
- Legacy markdown paper gate is deprecated and disabled by default.
- Docs-first artifact hard gate is deprecated and disabled by default.
- Multi-agent review gate (skeptic + verifier) is active when `STRICT_AGENT_REVIEW_GATE=1`.

## Required Structured Artifacts (target)
- `knowledge/SOURCE_TRANSFER.yaml`
- `knowledge/CLAIMS.yaml`
- `knowledge/HYPOTHESES_ACTIVE.yaml`
- `knowledge/HYPOTHESES_RETIRED.yaml`
- `knowledge/NONEXISTENCE_CERTIFICATES.yaml`
- `instances/INSTANCE_REGISTRY.yaml`
- `instances/FRONTIER_QUEUE.yaml`

## Source Transfer Gate
A row is valid only if:
- `source_id` is known,
- `theorem_or_mechanism` is non-empty and specific,
- `code_delta[]` has `file`, `action`, `detail`,
- `validation_metrics[]` is non-empty,
- `evidence_refs[]` points to existing local files.

## Hypothesis Gate
- Active hypotheses count must be 1..4.
- Each active hypothesis must include explicit falsification condition.
- Retired hypotheses must include retirement reason and evidence reference.

## Instance Gate
- Every frontier item must exist in instance registry.
- Registry status must be one of:
  - `impossible_divisibility`
  - `proved_nonexistence`
  - `provisional_nonexistence_veto`
  - `unknown_admissible_frontier`
  - `unknown_admissible`
  - `proved_existence`

## Review Gate
Author output requires skeptic and verifier pass before close.

Runtime implementation:
- Verifier agent: `math_proofs.agent_review` verifier checks (artifact integrity and round consistency).
- Skeptic agent: `math_proofs.agent_review` skeptic checks (consistency/risk checks).
