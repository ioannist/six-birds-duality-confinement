# Step 384 Results Summary

Riemann-Siegel asymptotic used:

`theta(t) = (t/2)log(t/(2pi)) - t/2 - pi/8 + O(1/t)`,

with `zeta(1/2+it)=exp(-i theta(t))Z(t)`.

Direct Cauchy/Riemann-Siegel saddle:

`r_* ~ k/log(T/(2pi))`.

Derived formula:

`gamma_RS(T) = 1 - log(log(T/(2pi)))`.

Comparison to Branch C:

- Branch C law: `pi/(T log(T/(2pi)))`
- Step 324 empirical RMSE for direct RS formula: `0.434114`
- Step 324 empirical RMSE for Branch C structural law: `0.023707`

Verdict: `different_formula_projection_missing`. Riemann-Siegel alone gives a different unprojected derivative scale; the missing piece is the Burnol/Sonine `P_infty` projection or projected kernel asymptotic.
