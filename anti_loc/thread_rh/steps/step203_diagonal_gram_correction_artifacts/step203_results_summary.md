# Step 203 Results Summary

Verdict: `V_diagonal_corrected_xi_inconclusive`.

Step 203 fixed the algebraic diagonal degeneracy from Step 202.  Reading Burnol 2002 directly shows that equation 1 is the bilinear de Branges kernel

`K(z1,z2)=(E(z1)E(z2)-E(1-z1)E(1-z2))/(z1+z2-1)`,

and Burnol states that as a function of one variable it is the evaluator at the reflected/conjugate point.  Therefore the critical-line diagonal must be evaluated as a limit, not by literal substitution.

## Diagonal Formula

For `w=1/2+iτ`,

`K(conj(w),w) = E(conj(w))E'(w)+E(w)E'(conj(w)) = 2 Re(conj(E(w)) E'(w))`.

The opposite sign was also tested.  The `+` sign is the nonnegative-norm convention in the finite calculation.

## Numerical Values

Using the Step 202 finite cosine-resolvent model with differentiated Burnol Theorem 8:

- `E'_{1/2}(rho_1) ≈ -2.18362493552e-5 + 1.54944169115e-5 i`
- `E'_{1/2}(rho_2) ≈ -1.87039981590e-8 - 1.01285320801e-7 i`
- `E'_{1/2}(rho_3) ≈ -4.34711344794e-9 - 1.20194935955e-9 i`

Corrected diagonal candidates:

- `G_11 ≈ 6.66157962829e-10`
- `G_22 ≈ 1.28713995247e-14`
- `G_33 ≈ 2.39433517220e-17`

The sign and `N_resolvent` stability are good: `N=160,240,320` give stable displayed digits.  However the cutoff-derived error bounds are much larger than the values:

- `G_11` error bound `≤ 1.90e-7`
- `G_22` error bound `≤ 2.74e-9`
- `G_33` error bound `≤ 2.12e-9`

Thus the finite diagonal is symbolically corrected but not numerically certified.

## Dual-System Cross-Check

Burnol 2004 [19] Theorems 3.1/3.2 align structurally with the bilinear Euclid pairing and the minimality of the `Z^a_{rho,k}` system for `a<1`. They do not provide an independent numerical norm formula for `a=1/2` in this step. Status: structural alignment, no independent numerical cross-check.

## Xi Matrix Source

The corrected full Gram matrix was assembled with Step 202 off-diagonal entries and the L'Hopital diagonal.  The commutator matrix was not certified because the diagonal error budget dominates and the transported `kappa`/`K_infty^op` quadrature still needs a certified implementation.

New sub-residual: `certified_E_prime_tail_bound_and_kappa_commutator_quadrature`.

