# Step 383 Results Summary

Computed Branch C `G_star` gamma for `n=100` zeros with the Step 292 raw proxy:

`delta_Dk=(zeta*M(G_star))^(k)(rho_j)`,

fitted on `k=[5, 10, 15, 20, 30]` using the Step 324 saddle form

`log|delta_Dk| = logA + alpha log(k) + b k + gamma k log(k)`.

Main fit:

- model: `R=a+b/s_min`
- `a=-5.99201268231755435e+00`
- `b=8.33404477418090828e+00`
- Pearson `r=1.48554714576799279e-01`
- RMSE `1.52626208925378020e+01`
- rel err `b` vs `pi^2`: `1.55584718951750717e-01`
- rel err `a` vs `-3pi/2`: `2.71544583280220686e-01`

Higher-order fits:

- `R=a+b/s+c/s^2`: RMSE `1.50465630989753887e+01`, `c=2.58380309653250180e+01`, `p=9.71509127568982722e-02`
- `R=a+b/s+d/T`: RMSE `1.52623151887617379e+01`, `d=1.16036921670884272e+01`, `p=9.50423038213837001e-01`

Verdict: `slope_or_offset_drift_reformulate`.
