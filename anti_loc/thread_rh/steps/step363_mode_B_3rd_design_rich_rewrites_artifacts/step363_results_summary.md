# Step 363 Results Summary

U^flat-double-prime was constructed with four states and richer rewrites:

- alpha: composite Hecke-zeta atom.
- beta: residual-decomposition atom.
- gamma: transfer-conditioning atom.
- delta: defect witness.

SAU gates: 6/6 pass.

Stage II preview: 50/50 cells passed with relative error 0.

Stage III used per-character polynomial rewrites:

- log |T(H)| = A + B log|H| + C(log|H|)^2.
- arg T(H) = arg H + D + E k + F k^2.

Residual RMSE(lambda_total):

- rho_1 training: 0.1558010988527524
- rho_2 holdout: 1.973439189878534
- rho_3 holdout: 2.525160108522078

Verdict: third Mode B design retracts at Stage III.  Failure mode is over-expressive in-sample improvement without cross-rho robustness, plus no external operator certificate.

Reach-boundary evidence: three structurally distinct Mode B designs now fail Stage III.
