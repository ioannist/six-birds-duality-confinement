# Step 311 Results Summary

Computed `arg(term_j)` for the Leibniz contributions
`term_j = binom(k,j) zeta^(j)(rho_1) M(G_star)^(k-j)(rho_1)`
at `k=10,20,30,50` using the same dps=80 construction as Step 309.

Inherited Step 309 interference ratios were `0.812, 0.625, 0.469, 0.268`.
After unwrapping, the central saddle windows are very nearly linear,
with central linear R^2 values from about 0.993 to 0.99998.
This is not chaotic phase behavior.  However, the central phase variation
grows from about 2.17 at k=10 to about 6.40 at k=50, so the direct
bounded-variation/cosine lower bound is not usable.

Phase-route feasibility: smoothness makes the gap more structured,
but no theorem-grade `(C_0,C_1)` interference bound follows from the
direct bounded-variation estimate.  The named Step 310 gap remains open
and appears to require a discrete stationary-phase estimate for the
central j-sum, or a positivity/quadratic-form reformulation.

Final verdict: `V_leibniz_phase_smooth_but_no_direct_BV_bound`.
