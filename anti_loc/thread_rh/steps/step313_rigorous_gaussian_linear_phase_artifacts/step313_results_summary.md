# Step 313 Results Summary

Computed the discrete second derivative of `log|term_j|` near the dominant `j*(k)` and decomposed it into binomial, zeta-derivative, and Mellin-derivative pieces.
The binomial piece gives the expected `-4/k` curvature and `sigma_binomial ≈ sqrt(k)/2`, close to the empirical widths.

The zeta and Mellin corrections are not negligible enough to yield a clean proof from Stirling alone, but the total curvature remains negative in the certified range and produces a Gaussian saddle.
The alpha/phase law remains numerical: no analytic formula or uniform phase-derivative bound was derived.

The Step 310 theorem therefore remains conditional.  Step 313 strengthens the magnitude-saddle side but does not close the interference theorem.

Final verdict: `V_gaussian_linear_phase_partial_binomial_dominates_sigma_alpha_still_empirical`.
