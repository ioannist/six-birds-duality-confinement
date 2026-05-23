# Step 204 Results Summary

Verdict: `V_unnormalized_partial`.

This step tested whether the Branch B finite residual can be decided from the unnormalized matrix entries

`c_ij = <kappa_i, (I-P_infty) M_{m_ell} P_infty kappa_j>`

without forming `e_i = kappa_i / sqrt(G_ii)`.

## Formula Derivation

Let `H_eta_fin = span{kappa_1,kappa_2,kappa_3}` and `G_ij=<kappa_i,kappa_j>`.
The orthogonal projection is

`P_eta x = sum_{i,j} kappa_i (G^{-1})_{ij}<kappa_j,x>`.

For the full finite Hilbert-Schmidt residual,

`||C_l P_eta||_HS^2 = tr(G^{-1} H)`, where `H_ij=<C_l kappa_i, C_l kappa_j>`.

Therefore the requested `c`-only identity

`tr(G^{-1} c^* G^{-1} c)`

computes the compressed diagnostic `||P_eta C_l P_eta||_HS^2`, not the full `||C_l P_eta||_HS^2`, unless `C_l(H_eta_fin) subset H_eta_fin` or a range projection is intended.

This is the main Step 204 symbolic finding.

## Gram Matrix

The Step 204 off-diagonal convention

`G_ij = K_{1/2}^Gamma(rho_j, conj(rho_i))`

was assembled using Step 202 `E_{1/2}` values and Step 203 L'Hopital diagonals. Representative entries:

- `G_11 = 6.661579628286e-10`, error bound `1.900688988e-7`
- `G_12 = -1.913153364500e-13`, error bound `5.597494281e-15`
- `G_13 = -8.526722281111e-15`, error bound `3.164870713e-15`
- `G_22 = 1.287139952474e-14`, error bound `2.742348785e-9`
- `G_23 = 6.623069784056e-17`, error bound `4.234974366e-17`
- `G_33 = 2.394335172196e-17`, error bound `2.118059237e-9`

Nominal diagnostics: `det(G) ≈ 2.10033807151e-40`, `||G^{-1}||_F ≈ 4.09992478506e16`.

The diagonal error bounds still dominate the diagonal values.

## c-Matrix Attempt

The unnormalized route removes explicit division by `sqrt(G_ii)` but does not remove the need for concrete boundary-line samples

`kappa_i(tau)=T_{1/2}^*K_{1/2}^Gamma(.,rho_i)(1/2+i tau)`

and the full `K_infty^op` PSWF quadrature. Burnol's `E`-kernel gives pairings and the projected reproducing kernel, but this step still lacks a certified numerical sampling formula for `T_a^*K(.,rho)`.

Thus `c_ij` was not certified, `M=G^{-1/2}cG^{-1/2}` was not formed, and `Xi_matrix_source` remains undecided.

New sub-residual: derive either certified `kappa` boundary sampling or the full matrix `H_ij=<C_l kappa_i,C_l kappa_j>`.

