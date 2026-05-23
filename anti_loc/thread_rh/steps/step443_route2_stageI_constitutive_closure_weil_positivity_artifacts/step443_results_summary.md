# Step 443 Results Summary

## Choice

Weil explicit-formula positivity, anchored in Weil 1952.

## A_W split

Concrete `W[f]` requires either the zero side `sum_rho fhat(gamma_rho)` or the prime side `sum_n Lambda(n) f(log n)/sqrt(n)`. Both smuggle arithmetic. Formal `W` avoids smuggling but does not provide numerical values or derived positivity.

## Numerics

Restricted formal branch Schur identity error: `1.3177747429e-82`. Residual eigenvalues: `['0.0012', '0.0025', '0.0064']`. Adequacy budget: `Xi_Z=0.0064 I`.

## Gates

6 gates: 2 pass, 1 partial, 3 fail. Grammar-local: 1 pass, 1 fail. Prior constraints checked: both fail on the concrete/formal split. New constraint added: `C_weil_positivity_explicit_formula_smuggling`.

## Verdict

Stage I retracts. Weil positivity confirms the audit-currency derivability tension across three structurally distinct attempts. This is a saturation observation only; `G_constitutive_closure` is not globally exhausted here.
