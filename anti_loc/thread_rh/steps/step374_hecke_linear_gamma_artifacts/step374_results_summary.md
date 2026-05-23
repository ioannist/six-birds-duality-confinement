# Step 374 Results Summary

Normalized Hecke evaluator values were used: `|h_chi^(k)(rho_chi)/k!|`.  Step 322 raw magnitudes for `chi_7a`, `chi_8a`, and `chi_11a` were divided by `k!`.

Linear-in-k fit form: `log|H_{chi,k}| = a_chi + alpha_chi log(k) - gamma_Hecke_linear k`.

- `chi_11a` q=11 T=2.47724: gamma_linear=2.2366, RMSE=0.24.
- `chi_3` q=3 T=8.03974: gamma_linear=2.49315, RMSE=0.233.
- `chi_4` q=4 T=6.02095: gamma_linear=2.43032, RMSE=0.234.
- `chi_5a` q=5 T=6.64845: gamma_linear=2.38091, RMSE=0.241.
- `chi_5b` q=5 T=6.18358: gamma_linear=2.3925, RMSE=0.235.
- `chi_7a` q=7 T=4.47574: gamma_linear=2.32873, RMSE=0.237.
- `chi_8a` q=8 T=4.89997: gamma_linear=2.29369, RMSE=0.241.

Candidate aggregate relative errors:
- `C1_zeta_height_only`: mean=1.45976, median=1.19857, max=2.64146.
- `C2_conductor_aware`: mean=5.45807, median=5.54966, max=7.58234.
- `C3_pure_conductor`: mean=0.330538, median=0.225677, max=0.707137.

Best candidate by mean error: `C3_pure_conductor`. Verdict: `none_matches_structurally_different_linear_gamma`.
Implication: the current normalized Hecke linear decay coefficients are much larger than the conductor-aware Riemann-von-Mangoldt half-spacing prediction. H6 does not reduce to this simple gamma-identification on the available first-zero data.
