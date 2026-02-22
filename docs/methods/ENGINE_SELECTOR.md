# Engine Selector

## Inputs
- divisibility pass/fail
- derivation-veto status
- estimated incidence size
- orbit compression diagnostics (`|O_r|`, `|O_q|`, non-binary share, max coefficient)
- strict pressure metrics ((r-1) cap-hit profile)

## Routing Rules
1. If divisibility fails: reject instance.
2. If derivation-veto verified hit: mark nonexistence and skip solve.
3. If orbit compression is strong: run bounded Kramer/orbit route.
4. If compression is weak: run randomized nibble/repair/absorber route.
5. Run residual exact-cover only when residual eligibility thresholds are satisfied.
