# Step 364 Results Summary

U^flat_G was constructed as a graph-based finite operational signature.

Nodes: v_H, v_Z, v_compare, v_audit, v_blocked.

Edges: e_load_H, e_load_Z, e_compare, e_audit, e_block.

Path predicates: P_mag, P_phase, P_operator, P_admit.

SAU gates: 6/6 pass.

Stage II preview: 50/50 graph descent cells passed with relative error 0.

Stage III graph transfer used shared edge-label weights:

- log |T_G(H)| = a0 + a1 x + a2 k + a3 xk + a4 k^2.
- arg T_G(H) = arg H + b0 + b1 x + b2 k + b3 xk + b4 k^2.

Residual RMSE(lambda_total):

- rho_1 training: 1.764253290788628
- rho_2 holdout: 2.122900424929048
- rho_3 holdout: 2.347972116925062

Verdict: graph framing also retracts at Stage III.  The obstruction is not specific to the three state-based framings tested so far.
