# Step 316 Results Summary

Computed `xi^(j)(rho_1)` for j=1..11 and compared `arg(xi^(j+1)/xi^(j))` to the corresponding zeta derivative-ratio phases.
The xi and zeta ratio phases differ by the smooth prefactor in xi, so they track but are not identical.

A truncated local Hadamard product normalized by `xi'(rho_1)` did not approximate `xi^(j)(rho_1)` to 10% for j=1..10 using up to the tested local zeros.  This indicates that the Taylor coefficients are not captured by a small local zero packet alone; the global canonical product/exponential tail matters.

The log-derivative power-sum diagnostic is different: for powers j=k/2, the nearest nontrivial zero after rho_1 dominates the weight rapidly.  That creates a plausible Montgomery-pair-correlation connection for logarithmic derivative asymptotics, but not yet for the raw xi derivative ratios required for alpha.

Final verdict: `V_alpha_hadamard_partial_local_power_sums_not_xi_derivatives`.
