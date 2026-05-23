# Step 302 Results Summary

Applied the proposed steepest-descent width correction at the dominant far-upper-left arc using the inherited `t^{-z}` convention. Derivatives were computed analytically from `M'(z)=int G(t)(-log t)t^{-z}dt` and `M''(z)=int G(t)(log t)^2t^{-z}dt`, combined with `zeta'` and `zeta''`.

Final verdict: `V_saddle_width_correction_partial`. The correction reduces the Step 301 Cauchy looseness, but the residual factor is not uniformly below 10%.
