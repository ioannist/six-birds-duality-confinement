# Step 369 Results Summary

Evaluator used:
- `anti_loc/thread/steps/step292_branch_C_k20_certified_artifacts/compute_delta_Dk_step292.py`.
- Routine signature used: `zeta_derivatives(gamma, max_k, dps)`, `mellin_derivatives(GENERATORS['G_star'], gamma, max_k, dps)`, `delta_from_derivatives(zds, mds, k)`.
- This is the inherited raw Branch C proxy `(zeta*M(G_star))^(k)(rho)`, using the `t^{-s}` Mellin convention.

Defect-order support:
- Requested defect orders: `d=0..5`.
- Actual evaluator support: `unsupported_by_step292_no_d_argument`.
- Therefore only `d=0` raw evaluator rows were produced. The requested local model `gamma_j(d)=A_j/T_j+B_j*d^beta_j` is not identifiable per zero.

Raw coverage: `75` rows = 15 zeros x 1 supported d x 5 k-values.
Closest supported diagnostic `A_eff = gamma_fit(d=0)*T` vs `pi/log(T/(2*pi))`: mean rel err `0.36097`, median `0.338929`, max `0.951351`, std `0.256492`.
Inherited manager-log `gamma*T` vs `pi/log(T/(2*pi))`: mean rel err `0.341101`, median `0.253665`, max `0.952665`, std `0.264643`.

Cited inherited results:
- Step 324: `gamma ~= A*T^alpha + B*d^beta` with `A=4.118`, `alpha ~= -1`, `B=-0.039`, `beta=0.409`, `RMSE=0.014`, `G_star`.
- Step 366: `A_predicted(T)=pi/log(T/(2*pi))` matched the smooth Step 324 coefficient at rho_1 within 5.9%.
- Step 367: per-zero `gamma_j*T_j` comparison had 34% mean relative error for `G_star`.
- Step 368: first-neighbor spacing correction reduced 34% to 27%, still structurally insufficient.

Verdict: the per-zero `A_j` refit cannot be performed with the current cascade evaluator because the defect-order axis is absent. The available data support only the smoothed-coefficient interpretation, not a rigorous per-zero local `A_j` confirmation.
