# Step 365 Results Summary

U^flat_R was constructed as a term-rewriting system over the signature {H, Z, M, P, O, Bottom, Tau_R} with no explicit state set.

SAU gates: 6/6 pass.

Stage II preview: 50/50 term reductions passed with relative error 0.

Stage III rewrite-normalizer:

- log|Tau_R(H)| = theta dot [1, x, dx, k, 1/k, x dx].
- arg Tau_R(H) = arg H + eta dot [1, x, dx, k, 1/k, sin(arg H), cos(arg H)].

Residual RMSE(lambda_total):

- rho_1 training: 1.727684439025268
- rho_2 holdout: 2.212545328283977
- rho_3 holdout: 2.374234560617829

Verdict: rewrite-only design retracts at Stage III.  Five structurally distinct Mode B designs now fail.
