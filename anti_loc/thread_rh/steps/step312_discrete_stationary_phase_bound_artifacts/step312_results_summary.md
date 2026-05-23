# Step 312 Results Summary

Extracted the central phase slope `alpha` and j-space width `sigma(k)` from Step 311/309 data.
The correct frequency is the central linear phase slope, about `0.386..0.427` radians per j, not the total phase variation divided by the saddle width.

The Gaussian-Fourier stationary-phase model
`interference ≈ exp(-alpha^2 sigma^2 / 2)` matches the empirical interference ratios at k=10,20,30,50 to a few percent.

A conservative sample-calibrated bound is `interference(k) >= exp(-0.028 k)` on the certified sample.
This does not yet close the Step 310 theorem: the Gaussian saddle, phase expansion, and stationary-phase remainders remain numerical/heuristic rather than rigorous, i.e. not theorem-grade.

Final verdict: `V_discrete_stationary_phase_matches_empirical_interference_but_not_rigorous`.
