# Step 289 Results Summary

## G Provenance

The exact Branch B matrix used here is the preserved `G_matrix_step208.csv`, copied from Step 207.  Its entries are documented in the CSV as:

- diagonal entries: `diagonal_from_step203_LHopital`, source `Step203 LHopital K(conj(rho_i),rho_i)`;
- off-diagonal entries: `off_diagonal_step204_conjugate_convention`, source `Burnol 2002 equation 1 with z1=rho_j,z2=conj(rho_i)`.

The next-layer quantity is the Step 208 inherited unnormalized residual

`Xi_matrix_source = tr(G^{-1} c^dagger G^{-1} c)`.

## Condition Number vs Precision

Using the preserved decimal `G`, the singular-value condition number is stable:

| dps | sigma_min | sigma_max | condition |
|---:|---:|---:|---:|
| 80 | `2.43907347702444e-17` | `6.66158017880950e-10` | `2.73119290647050e7` |
| 200 | `2.43907347702444e-17` | `6.66158017880950e-10` | `2.73119290647050e7` |
| 500 | `2.43907347702444e-17` | `6.66158017880950e-10` | `2.73119290647050e7` |
| 1000 | `2.43907347702444e-17` | `6.66158017880950e-10` | `2.73119290647050e7` |

So the stored matrix is not structurally singular.  However `||G^{-1}||_F = 4.09992478506014e16`, which strongly amplifies c-matrix uncertainty.

## Inversion Techniques

At dps=500:

- direct inverse, LU column solves, SVD pseudo-inverse, and Newton refinement agree on `Xi` to extreme precision;
- Tikhonov `lambda=1e-80` and `lambda=1e-30` are numerically close but marked separately as regularized diagnostics;
- QR column pivoting is unavailable in mpmath here;
- Cholesky is not applicable because the preserved `G` is not Hermitian positive definite.

Next-layer values:

| candidate | stable Xi abs | propagated error |
|---|---:|---:|
| CAND1 | `2.8770749388153867e-2` | `1.4685454221295172e14` |
| CAND2 | `8.1516179028375357e65` | `2.6239388728881304e66` |

## Verdict

`V_branch_B_G_inv_partial`.

The arbitrary-precision inversion itself is stable, so the preserved decimal `G` inverse is technique-solvable.  But the Step 208 next-layer residual remains non-decisive because finite-grid c-matrix / unresolved transport-sampling uncertainty is amplified by `G^{-1}`.  The Branch B wall moves from raw inverse arithmetic toward the upstream c-matrix/transport normalization, but it does not crack into a certified next-layer closure or hard foreclosure.
