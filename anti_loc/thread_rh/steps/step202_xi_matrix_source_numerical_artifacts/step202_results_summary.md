# Step 202 Results Summary

Verdict: `V_xi_matrix_source_partial`.

This step implemented a first numerical pipeline for Branch B's finite matrix-source residual on
`Rho_fin={rho_1,rho_2,rho_3}`, `A_fin={1/2}`, `K_fin={0}` using the Step 201 Burnol 2002/2004 unblock.

## Pipeline

- `lambda=1/2`.
- `E_{1/2}` was evaluated from Burnol 2002 Theorem 8 using a finite cosine-resolvent discretization of `(1 \pm F_{1/2})^{-1}`.
- Numerical settings: `mpmath` scalar precision `70` dps, cosine-resolvent dimension `160`, Gauss-Legendre integral nodes `520`, main cutoff `80`, check cutoff `55`.
- The de Branges kernel formula from Burnol 2002 equation 1 was then used to assemble the literal finite Gram matrix
  `G_ij = K_{1/2}^Gamma(rho_j,rho_i)`.

## E-values

Representative computed values:

- `E_{1/2}(rho_1) = -4.081212091972708e-6 + 1.574506597413041e-5 i`, error bound `1.66e-8`.
- `E_{1/2}(rho_2) = -5.56494927208788e-8 - 5.326370801110695e-8 i`, error bound `1.11e-9`.
- `E_{1/2}(rho_3) = -2.852540269008198e-9 + 3.566209339918986e-10 i`, error bound `1.06e-9`.

The values at `1-rho_i` were the corresponding conjugates in this discretization.

## Gram Matrix Finding

The literal convention inherited from Step 201,

`G_ij = K_{1/2}^Gamma(rho_j,rho_i)`,

assembled numerically, but it gives zero diagonal entries for `i=j` on the critical line. Therefore the normalized vectors

`e_i = kappa_i / sqrt(G_ii)`

cannot be formed from this literal convention. This exposes a new downstream sub-residual: the Branch B computation needs the correct de Branges diagonal/reproducing-kernel limit or inner-product convention before `c_ij(ell)` is numerically meaningful.

## Commutator Matrix

The commutator entries

`c_ij(ell)=<e_i,(I-P_infty)M_{m_ell}P_infty e_j>`

were not certified. In addition to the zero-diagonal normalization blocker, a certified implementation must still sample the transported boundary vectors
`kappa_i=T_{1/2}^*K_{1/2}^Gamma(.,rho_i)` and include the full `K_infty^op` PSWF correction.

## Residual Decision

`Xi_matrix_source` is not decided in this step:

- not closed;
- not certified nonzero;
- partial pipeline established through `E_{1/2}` and the literal Gram layer;
- new blocker: `fix_Branches_B_kernel_inner_product_convention_and_certified_commutator_quadrature`.

