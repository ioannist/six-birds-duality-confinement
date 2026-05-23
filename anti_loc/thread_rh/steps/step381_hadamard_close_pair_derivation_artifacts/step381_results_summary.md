# Step 381 Results Summary

Hadamard key formula:

`zeta''(rho_j) = 2 zeta'(rho_j) g'_j(rho_j)`,

with

`g'_j(rho_j)=arch(rho_j)+sum_(rho != rho_j)[-1/(rho-rho_j)+1/rho]`.

The close-pair term is `g'_near=+/- i/s_min`, giving `Re zeta''_near = Re(2 zeta'(rho_j) g'_near)`.

Sign prediction:

- exact Hadamard identity reconstruction: `22/22`
- close-pair-only predictor: `8/22`
- close-pair-only on exceptional zeros: `7/7`
- close-pair-only on baseline zeros: `1/15`

Residual prediction:

- model: `R = -4.47288 + 10.1767/s_min`
- Pearson `corr(R, 1/s_min) = 0.723724`
- RMSE: `3.561247`

Verdict: `partial_close_pair_mechanism_R_correlation_passes_sign_needs_regular_remainder`. The close-pair Hadamard term gives the local amplification mechanism and predicts the Branch C residual above the `r>0.7` threshold, but a complete `Re zeta''` sign theorem requires controlling the regular Hadamard remainder.
