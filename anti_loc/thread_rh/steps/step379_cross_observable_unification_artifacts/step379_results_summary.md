# Step 379 Results Summary

Step 378 finding cited verbatim: `7 exceptional zeros have mean s_min = 0.97 (vs non-exceptional 1.75); Pearson r = 0.732 between Re zeta''(rho_j) and (Delta_bar - s_min)`.

Computed Branch C `G_star` gamma for the seven exceptional zeros with the Step 292 raw delta proxy:
`delta_Dk=(zeta*M(G_star))^(k)(rho)`, fitted on `k=[5, 10, 15, 20, 30]` using the Step 323/324 saddle form
`log|delta_Dk| = log A + alpha log k + b k + gamma k log k`.

Mean `|R|` exceptional: `6.24245689789771241e+00`.
Mean `|R|` Step 368 baseline `j=1..15`: `5.88115221898721674e-01`.
Ratio: `10.614343`.

Exceptional signed residual signs: `{'positive': 6, 'negative': 1, 'zero': 0}`.
Baseline signed residual signs: `{'positive': 8, 'negative': 7, 'zero': 0}`.

Verdict: `unification_confirmed_exceptional_residuals_large`. By the requested `>2x` threshold, the exceptional zeros show anomalous Branch C gamma residuals as well as anomalous `Re zeta''` behavior. The Welch test is underpowered at `n=7` and is not below a conventional `0.05` threshold, so this is a strong effect-size unification signal rather than a theorem-grade statistical closure.
