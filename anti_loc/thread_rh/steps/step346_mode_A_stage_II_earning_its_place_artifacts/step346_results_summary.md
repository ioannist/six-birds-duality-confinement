# Step 346 Results Summary

Mode A Stage II extended the Step 345 preview from 4 values to 100 scoped realization values.

Reproduction count: `100/100` within 1%.
- Hecke rows: 7 characters x 10 k-values = 70.
- Zeta rows: rho_1..rho_3 x 10 k-values = 30, routed via `F(H_chi3,k)=Z_j,k+Omega_chi3,j,k` with `Omega` retained.

Spot checks:
- `R_H(H_chi3_10)` matches Step 320 value `2612.37946598909174`.
- `R_H(H_chi7b_10)` matches Step 338 value `11338.9438476577826`.
- `R_zeta(F(H_chi3_10))` at rho_1 matches `165.438682953307426` with `Omega` retained.
- `R_zeta(F(H_chi3_10))` at rho_3 matches `1932.60752705489886` with `Omega` retained.

Ablation result: `100/100` rows break when `emit_basis_to_realization_lens` is removed.
Diagnostic note: quotienting `Omega=0` does not change numeric host values, but it fails SAU no-smuggling because it kills the H6 obstruction.

SAU gate: primitive exclusion pass; dependency trace pass; defect retained pass.

Final verdict: `V_mode_A_stage_II_reproduction_passes_ablation_breaks`.
Runtime: `34.452` seconds.
