# Step 384 Riemann-Siegel Derivation Attempt

Standard Riemann-Siegel setup (Titchmarsh, *Theory of the Riemann Zeta-function*, Ch. IV; Edwards, *Riemann's Zeta Function*, Ch. 7):

`zeta(1/2+it) = exp(-i theta(t)) Z(t)`,

where

`theta(t) = arg Gamma(1/4+it/2) - (t/2)log pi`

and

`theta(t) = (t/2)log(t/(2pi)) - t/2 - pi/8 + O(1/t)`.

The Riemann-Siegel main sum is

`Z(t) = 2 sum_(n<=sqrt(t/(2pi))) n^(-1/2) cos(theta(t)-t log n) + error`.

For a direct Cauchy estimate of zeta derivatives at `rho=1/2+iT`,

`zeta^(k)(rho) = k!/(2pi i) int zeta(s)/(s-rho)^(k+1) ds`.

Using the Riemann-Siegel phase scale `log(T/(2pi))`, the natural direct saddle has

`r_* ~ k/log(T/(2pi))`.

Then

`log|zeta^(k)(rho)| ~ log(k!) - k log r_* + O(k)`

which gives the linear coefficient

`gamma_RS(T) = 1 - log(log(T/(2pi)))`

under the sign convention used here.

This is not the Branch C empirical law

`gamma_BC(T) = pi/(T log(T/(2pi)))`.

The mismatch means Riemann-Siegel alone sees the unprojected zeta derivative scale. The missing ingredient is the Burnol/Sonine projector `P_infty` (or equivalently the projected kernel asymptotic from Steps 153/172/372), which suppresses the direct Riemann-Siegel saddle and introduces the cusp/zero-density scale `1/(T log T)`.

Numerical comparison over Step 324's 15-zero dataset:

- RMSE direct Riemann-Siegel formula: `0.434114`
- RMSE `pi/(T log(T/(2pi)))`: `0.023707`

Verdict: `different_formula_projection_missing`.
