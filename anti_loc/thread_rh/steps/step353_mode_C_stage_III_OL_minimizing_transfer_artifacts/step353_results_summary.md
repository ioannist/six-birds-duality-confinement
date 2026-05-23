# Step 353 Results Summary

Translated the H6 bridge target into an OL residual minimization problem:

`lambda_obs(T_theta) = |log(T_theta(H_chi,k) / Z_rho_j,k)|`.

Three transfer families were tested.

## Candidate (a): Scalar Per Target

`T(H_chi,k) = c_j H_chi,k`.

Best target fit was `rho_3`, with `rmse_lambda = 0.49994`,
`max_lambda = 1.40462`.  This does not reach a bridge-grade residual.

## Candidate (b): Affine Log Normalizer

`log T(H_chi,k) = alpha_j + beta_j log H_chi,k`.

Best target fit was `rho_1`, with `rmse_lambda = 0.28072`,
`max_lambda = 0.69356`.  This improves on scalar normalization but remains
too large.

## Candidate (d): Weighted Geometric Mean

`log T_j(k) = sum_chi w_{j,chi} log H_chi,k`.

In-sample per-target fits can nearly close the OL ledger:

- `rho_1`: `rmse_lambda = 3.96e-5`, `max_lambda = 7.76e-5`
- `rho_2`: `rmse_lambda = 1.43e-4`, `max_lambda = 2.71e-4`
- `rho_3`: `rmse_lambda = 3.18e-5`, `max_lambda = 6.09e-5`

However, target hold-out fails.  Training the weighted geometric transfer on
`rho_1` and applying it to other targets gives:

- hold-out `rho_2`: `rmse_lambda = 0.74209`, `max_lambda = 1.39538`
- hold-out `rho_3`: `rmse_lambda = 1.62546`, `max_lambda = 2.45803`

## Verdict

`V_mode_C_stage_III_transfer_overfits_no_structural_H6_candidate`.

The OL formulation successfully translates H6 into a residual minimization
problem.  The tested finite transfer families do not produce a structural H6
bridge candidate: simple families fail in training, and the flexible
geometric family overfits target-by-target.
