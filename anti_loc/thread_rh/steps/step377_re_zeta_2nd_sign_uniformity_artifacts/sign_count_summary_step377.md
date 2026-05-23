# Step 377 Sign Count Summary

Computed `zeta''(rho_j)` for `j=1..100` using `mpmath.zetazero(j)` and `mpmath.zeta(rho_j, derivative=2)` at `dps=80`.

- negative Re count: `93/100`
- nonnegative Re count: `7/100` (`positive=7`, `zero=0`)
- mean Re zeta'': `-4.73364834535139334e+00`
- variance Re zeta'': `1.79713862319439492e+01`
- std Re zeta'': `4.23926718100474886e+00`
- min Re zeta'': `-1.74703662061180154e+01`
- max Re zeta'': `5.18220663161495132e+00`
- mean Im zeta'': `9.44248201266540688e-02`
- mean |zeta''|: `8.19187531913244094e+00`
- Step 368 cross-check rows: `15`; all signs match: `True`; max relative |zeta''| difference: `3.545e-15`

Verdict: `majority_negative_not_uniform`.
