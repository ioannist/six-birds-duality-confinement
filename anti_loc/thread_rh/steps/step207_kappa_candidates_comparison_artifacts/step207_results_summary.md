# Step 207 Results Summary

## Verdict

`V_kappa_tau_candidates_disagree`.

The two candidate transport-sampling formulas were evaluated on the same
200-node Gauss-Legendre grid in `tau in [-40,40]` for `rho_1,rho_2,rho_3`.
The nominal ratio `CAND1/CAND2` is not constant for any of the three zeros:

| rho | min |CAND1/CAND2| | max |CAND1/CAND2| | status |
|---|---:|---:|---|
| rho_1 | 2.5008929629627379e-26 | 1.7748924779317304e-10 | nominal varying, CAND1-error dominated |
| rho_2 | 7.4226939561589834e-30 | 2.6079509268902143e-15 | nominal varying, CAND1-error dominated |
| rho_3 | 1.3962291433488764e-33 | 3.0769935351035648e-18 | nominal varying, CAND1-error dominated |

No row exceeds the conservative `20x` threshold against the inherited Step 205
CAND1 absolute-error labels, so this is not recorded as a certified equality
or inequality theorem. It is recorded as a specific disagreement pattern: the
Burnol-boundary candidate and the zeta-dual candidate do not agree up to a
constant at the numerical level available in the inherited implementation.

## Transport-Sampling Resolution

The transport-sampling theorem is not resolved by candidate agreement. Step 207
therefore does not select either CAND1 or CAND2 as `kappa_i(tau)`.

## Commutator and Xi

The hard constraint forbids arbitrary candidate selection when the candidates
disagree. Consequently:

- `c_ij = <kappa_i, (I-P_inf) M_{m_l} P_inf kappa_j>` was not evaluated.
- `Xi_matrix_source = tr(G^{-1} c^dagger G^{-1} c)` was not evaluated.
- The inherited `G` matrix from Step 204 was copied for provenance only.

## Next Gate

The new explicit gate is no longer Burnol's projected kernel formula; it is the
transport-sampling identification:

`T_a^* K_a^Gamma(.,rho)(1/2+i tau) = ?`

The manager-level audit should decide whether the cascade's `T_a^*` corresponds
to the de Branges boundary trace CAND1, the zeta-dual CAND2 after finite
linear-combination correction, or a third normalized expression.
