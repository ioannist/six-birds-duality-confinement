# Step 368 Results Summary

Residual:

`R_j = gamma_j*T_j - pi/log(T_j/(2*pi))`.

Baseline mean relative error from Step 367 convention:

`mean |A_pred - A_eff|/|A_pred| = 0.3411`.

## Predictors Tested

- forward spacing `s_fwd`
- backward spacing `s_bwd`
- harmonic mean spacing `s_mean`
- nearest spacing `s_min`
- spacing asymmetry `s_fwd - s_bwd`
- default defect order `d=0`
- `eta = sgn(Re zeta''(rho_j))`
- `|zeta''(rho_j)|`
- sign of gamma

The default defect order, `eta`, and sign of gamma were constant on this 15-zero dataset, so their correlations are undefined.

## Top Correlations

Top Pearson absolute correlations:

1. `s_min`: `r = -0.354`
2. `s_fwd`: `r = -0.250`
3. `s_mean`: `r = -0.243`

Top Spearman absolute correlations:

1. `spacing_asym`: `rho = -0.401`
2. `s_min`: `rho = -0.309`
3. `s_fwd`: `rho = -0.292`

## Corrections

Best single-variable correction:

`A_eff ~= A_pred + 0.5051518999 - 0.1865126682*s_min`.

Mean relative error becomes `0.3130`, only a modest improvement over `0.3411`.

Best two-variable correction:

`A_eff ~= A_pred + 0.0749280798 + 0.2189932715*s_bwd - 0.3163282506*s_min`.

Mean relative error becomes `0.2716`.

## Verdict

No explicit correction reaches the requested thresholds. The spacing variables carry weak-to-moderate signal, especially nearest spacing and spacing asymmetry, but the residual remains structurally complex. The `pi/log(T/(2*pi))` law captures a smooth leading scale, while per-zero scatter needs a richer model than first-neighbor spacing, default defect order, or `zeta''` sign.
