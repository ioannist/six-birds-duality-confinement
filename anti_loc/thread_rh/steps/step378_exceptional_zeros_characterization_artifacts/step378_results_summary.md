# Step 378 Results Summary

Step 368 observation cited verbatim: `eta_j = sgn(Re zeta''(rho_j)) = -1` for all `j=1..15`.
Step 377 finding cited verbatim: `93/100` zeros have `Re zeta''(rho_j) < 0`; exceptions are `[34, 41, 64, 71, 79, 80, 92]`.

The exact exception heights are in `exceptional_zeros_features_step378.csv`. Neighbor-spacing analysis supports a relative close-pair/local-compression signal:

- mean exceptional `s_min`: `0.968621`
- mean non-exceptional `s_min`: `1.748771`
- mean exceptional close-pair distance `Delta_bar(T)-s_min`: `0.953342`
- mean non-exceptional close-pair distance: `0.543540`

Cluster analysis: not a single T-cluster. Exceptions are late-skewed and include one adjacent pair, but are otherwise scattered.

Top Pearson correlation over all 100 zeros: `mean_spacing_minus_s_min` with `r=7.32214178608617594e-01`. The close-pair deficit is the strongest tested signal; raw `s_min` alone is weaker, so the structural quantity appears to be spacing relative to local Riemann-von Mangoldt mean spacing rather than absolute spacing.

Verdict: `close_pair_deficit_signal; not_single_T_cluster`. The 7 exceptions are not explained by a special arithmetic property of the heights in this audit, but they show a clear local-spacing/close-pair signal.
