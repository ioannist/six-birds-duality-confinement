# Step 451 Construction Synthesis

## Route outcomes

| route | what constructs | what is missing | status |
|---|---|---|---|
| Schur-complement | positive residuals `Xi_n >= 0`, candidate domination-budget shape | contraction/factorization plus `tr Xi_n + tr tail -> 0` | partial |
| Exhaustive moving ledger | finite-window ledgers and formal tail squeeze | `tr T_n^tail -> 0` and window domination decay | partial |
| Obstruction budget | defected budget `B_n(t)` and optimized trace identity | `a_n -> 0`, `b_n -> 0` | partial |

## Named substrate input gap

`Xi_SDTC_trace_decay_input`: a substrate-specific trace-decay input for `Sel^!_{zeta,tr}` that proves vanishing of the source, bridge, Schur residual, and/or tail defects sufficiently to construct `B_n >= 0` with

```text
A_Z(zeta) <= B_n,
tr B_n -> 0.
```

This gap is narrower than the original residual but does not resolve it. It is the framework-only Option 1 analog of a substrate input gap: the formal machinery supplies the domination grammar, but not the analytic decay theorem.

## Synthesis verdict

No route closes from framework primitives alone. The correct Step 451 verdict is:

```text
option1_partial_with_named_substrate_input_gap
```

No RH proof, recognition closure, or BirdInt judgment is made.
