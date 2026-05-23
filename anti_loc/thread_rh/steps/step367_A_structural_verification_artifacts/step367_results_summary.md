# Step 367 Results Summary

Prediction tested:

`A_pred(T) = pi/log(T/(2*pi))`.

Effective observed value:

`A_eff(rho_j,G) = gamma_j(G)*T_j`.

## Aggregate Results

All 30 cells:

- mean relative error: `0.4936`
- median relative error: `0.4046`
- max relative error: `2.0386`
- standard deviation: `0.4366`

By test function:

- `G_star`: mean `0.3411`, median `0.2537`, max `0.9527`
- `G_prime`: mean `0.6460`, median `0.4374`, max `2.0386`

## Position Stratification

`G_star`:

- low `rho_1..rho_5`: mean `0.1633`
- mid `rho_6..rho_10`: mean `0.4730`
- high `rho_11..rho_15`: mean `0.3871`

`G_prime`:

- low `rho_1..rho_5`: mean `0.3735`
- mid `rho_6..rho_10`: mean `0.5165`
- high `rho_11..rho_15`: mean `1.0480`

## Verdict

The step 366 half-spacing law is **not** verified as a universal 15-zero / two-test-function law.

It remains a plausible leading low-height scale for `G_star`, especially over `rho_1..rho_5`, but it breaks down under high-zero finite-fit noise and the `G_prime` control. The structural origin is therefore only partially identified: local zero density gives the correct scale, but test-function dependence and spacing corrections dominate outside the low-`T`, `G_star` band.
