# Step 451 Obstruction-Budget Route

## Candidate construction

Needles.tex `def:main:obstruction-budget` supplies the defected budget form

```text
B_n(t) = (1+t)(Lambda_n^{-1} Theta_0^- + E_src,n) + (1+t^{-1}) E_br,n,
```

with optimized trace

```text
inf_(t>0) tr B_n(t) = (sqrt(a_n) + sqrt(b_n))^2.
```

Here:

- `E_src,n` is a source defect: the part of the anti-invariant zeta ledger not supplied by accepted trace-source records at stage `n`.
- `E_br,n` is a bridge defect: failure of the stage-`n` transport/Douglas bridge to carry the source record into the anti-invariant ledger coordinates.
- `Lambda_n^{-1} Theta_0^-` is the shrinking base anti-invariant source budget, if such shrinking source budgets are available.

## What framework primitives provide

The framework provides:

1. The budget algebra.
2. Positivity of the terms when the defects are positive operators.
3. The optimized trace identity.
4. The sufficient condition:

```text
a_n -> 0 and b_n -> 0  implies  tr B_n(t_n) -> 0.
```

## Where the route stalls

The framework does **not** prove the decay facts `a_n -> 0` and `b_n -> 0` for the completed zeta zero ledger. Those are substrate-specific analytic claims about the completed Selberg trace closure. They would require evidence such as a trace-source decay theorem, a bridge-defect decay theorem, or an accepted recognition source supplying completed domination records.

Using Weil positivity, explicit zero estimates, Burnol/Sonine projection decay, Beurling-Nyman Gram convergence, or Branch-C asymptotics would import carrier-specific or readout-level content. That is outside Option 1.

## Named missing input

`Xi_SDTC_trace_decay_input`: decay of the source and bridge defects in the defected obstruction budget for `Sel^!_{zeta,tr}`.

## Route verdict

Partial only. The obstruction-budget route gives the cleanest shape of the missing theorem: prove `a_n,b_n -> 0` without importing RH-equivalent or carrier-specific content.
