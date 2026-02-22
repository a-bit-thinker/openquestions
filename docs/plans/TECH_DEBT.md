# Technical Debt

## High Priority
- Replace custom docs gate validators with full JSON-schema-backed validation for YAML artifacts.
- Add automatic generation of `docs/generated/RUN_METRICS.jsonl` from run close events.
- Add boundary-contract enforcement before solver/code changes.
- Remove legacy round1 markdown word-detection gate after observing stable agent-review performance.

## Medium Priority
- Add multi-agent review harness (author/skeptic/verifier roles).
- Add canonical status transitions for instance registry.

## Low Priority
- Auto-render dashboard from `docs/generated/` artifacts.
