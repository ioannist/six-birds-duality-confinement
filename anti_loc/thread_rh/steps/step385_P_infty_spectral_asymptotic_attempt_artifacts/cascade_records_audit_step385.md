# Step 385 Cascade Records Audit

Audited records:

- Step 102: `/anti_loc/thread/steps/step102_projection_residual_artifacts/step102_results_summary.md`
- Step 104: `/anti_loc/thread/steps/step104_shifted_sonin_artifacts/step104_results_summary.md`
- Step 105: `/anti_loc/thread/steps/step105_semilocal_prolate_repair_artifacts/step105_results_summary.md`
- Step 145: `/anti_loc/thread/steps/step145_extracted/step145_results_summary.md`
- Step 153: `/anti_loc/thread/steps/step153_extracted/step153_results_summary.md`
- Step 172: `/anti_loc/thread/steps/step172_cascade_reduction_theorem_artifacts/step172_results_summary.md`
- Step 173: `/anti_loc/thread/steps/step173_p_infty_kernel_attempt_artifacts/step173_results_summary.md`
- Step 196: `/anti_loc/thread/steps/step196_branch_C_extended_dataset_artifacts/step196_results_summary.md`

## Extracts

Step 102: `R_S compact iff P_infty A_S(I-P_infty) compact.`

Step 104: `The raw archimedean Sonin off-diagonal block B_a=S_lambda tau_a(I-S_lambda) is not compact for any nonzero shift a.`

Step 105: `If the actual semilocal prolate projection repairs the finite-place shifted sector, it must change the projection at the essential level, not merely by finite-dimensional or compact correction.`

Step 145: `H_R=overline(span{Ran Pi_Ya B_{ell,a}: ell != 0})`.

Step 153: `U_infty(J_a^*Y^a_{w,k}) = T_a^* partial_{\bar w}^k K_a^Gamma(.,w).`

Step 153 also records: `K_a^Gamma(.,w)=P_{L_a^Gamma} K_a^{Gamma,amb}(.,w)` and warns that the projection is load-bearing.

Step 172: the terminal gap is `L_{rho,k}(G)=<M_zeta G, P_infty y_{rho,k}>`.

Step 173: exact operational identity:

`S_lambda=I-P-(I-P)Q(I_{QH}-QPQ)^{-1}Q(I-P)`

and, with PSWFs `QPQ phi_n = mu_n phi_n`,

`S_lambda = I-P - sum_n |(I-P)phi_n><(I-P)phi_n|/(1-mu_n)`.

Mellin transport:

`K_infty^op(s,s')=delta(tau-tau') - sin(lambda(tau-tau'))/(pi(tau-tau')) - sum_n Psi_n^lambda(s) conjugate(Psi_n^lambda(s'))`.

Step 196: `min(|L|-error)=3.4126458948014055e-02`.

## Available

The records do provide an exact operational PSWF-series identity for `P_infty` after Step 173.

## Missing

They do not provide a large-`k` asymptotic for the coefficients

`<T_a^* partial_{\bar rho}^k K_a^Gamma(.,rho), Psi_n^lambda>`

or for the projected kernel derivative

`partial_{\bar rho}^k P_{L_a^Gamma}K_a^{Gamma,amb}(.,rho)`.
