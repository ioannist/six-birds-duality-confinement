# Step 380 Results Summary

Step 379 finding cited verbatim: exceptional zeros have `R_j` up to `+23.60` and `10.6x` amplification of the Branch C gamma residual.

Step 196 foreclosure target: `|L_{rho,k}(G)| >= 0.034`.

Available evaluator used here:

- routine: Step 292 `delta_from_derivatives(zeta_derivatives, mellin_derivatives, k)`
- formula: `delta_Dk=(zeta*M(G_star))^(k)(rho)`
- normalization: unnormalized `abs(delta_Dk)`, no `k!` division
- corrections: no `I_k/R_k` projected corrections applied; unavailable for these cells

Exceptional grid: `7` zeros x `5` k-values = `35` cells.

- pass count: `35/35`
- failure cells: `0`
- borderline cells within 10% of threshold: `0`
- minimum exceptional value: `2.3215072580122387712` at `j=92`, `k=5`
- baseline min value: `4.2765574702036441682` at `j=1`, `k=5`

Verdict: `robust_raw_proxy_foreclosure_all_35_pass`. Under the available raw proxy, close-pair exceptional zeros do not threaten the Step 196 foreclosure threshold.
