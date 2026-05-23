# Step 205 Results Summary

Verdict: `V_kappa_tau_sampling_formula_corrected`.

Step 205 audited the proposed critical-line sampling formula

`kappa_i(tau) ?= K_{1/2}^Gamma(1/2+i tau, rho_i)`.

The formula is **not justified** by inherited records.  Step 153 gives

`U_infty(J_a^*Y^a_{w,k}) = T_a^* partial_{bar w}^k K_a^Gamma(.,w)`,

and Step 152/153 gives

`T_a = M_Gamma J_a U_infty^{-1}`, so `T_a^* = U_infty J_a^* M_Gamma^*`.

Nothing in Steps 152/153 or Burnol 2002/2004 says that this adjoint transport
reduces to raw boundary evaluation of the de Branges kernel.  Therefore the
candidate formula would be an ambient/boundary shadow unless an additional
transport theorem is supplied.

## Candidate Sampling

The candidate boundary kernel was still sampled on the requested 200-point
Gauss-Legendre grid over `tau in [-40,40]`, for `rho_1,rho_2,rho_3`.  These
600 values are written to `kappa_tau_samples_step205.csv` with status
`candidate_boundary_kernel_not_certified_as_kappa`.

Representative candidate values for `rho_1`:

- `tau ~ -25`: `7.49470020947e-15`
- `tau ~ -14`: `8.42407963493e-10`
- `tau ~ 0`: `4.67028549034e-7`
- `tau ~ 14`: `-3.66923017176e-12`
- `tau ~ 25`: `-1.95825829371e-15`

These are **not** certified `kappa_i(tau)` values.

## c-Matrix and Xi

Because the `kappa_i(tau)` sampling formula is not verified, the commutator integral

`c_ij = int conj(kappa_i(tau)) [(I-P_infty) M_m P_infty kappa_j](tau) d tau/(2pi)`

was not lawfully evaluated.  Running the Step 173 `K_infty^op` PSWF machinery on
the candidate samples would be an unjustified substitution.

Therefore `c_matrix`, `M_matrix`, and `Xi_matrix_source` remain undecided.

Required next record:

`T_a^*K_a^Gamma(.,rho)(1/2+i tau)=K_a^Gamma(1/2+i tau,rho)`,

or the corrected explicit formula for `U_infty J_a^* M_Gamma^*` on
`K_a^Gamma(.,rho)`.

