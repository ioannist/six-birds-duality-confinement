# Step 290 Results Summary

## c-Matrix Provenance

The c-matrix is the Step 208 finite-grid commutator diagnostic:

`c_ij = sum_tau w(tau) conj(kappa_i(tau))*((I-P) exp(i ell tau) P kappa_j)(tau)/(2*pi)`.

Step 208 used 200 Gauss-Legendre nodes on `[-40,40]`, `ell=log(2)`, and 24 PSWF terms.  CAND1 samples came from Step 205/207:

`K_{1/2}^Gamma(1/2+i tau,rho_i)`.

CAND2 samples came from Step 207:

`zeta(s)/((s-rho_i) zeta'(rho_i) pi^{-rho_i/2} Gamma(rho_i/2))`.

Burnol 2002 supplies the de Branges kernel formula

`K(z1,z2)=(E(z1)E(z2)-E(1-z1)E(1-z2))/(z1+z2-1)`,

and the Sonine `E_lambda` formula

`E_lambda(w)=pi^{-w/2} Gamma(w/2)(lambda^{1/2-w}+sqrt(lambda)/2 int_lambda^infty (psi_+^lambda-psi_-^lambda)t^{-w}dt)`.

## Avenue A: Grid Refinement

I regenerated CAND1 and CAND2 on a 2000-node Gauss-Legendre grid, recomputed the c-matrices with the inherited 24-PSWF Step 208 operator, and compared against the 200-node inherited c-matrices.

Runtime: `465.206s`.

Entry-level uncertainty proxy reduction:

| candidate | min reduction | max reduction | 10-order target |
|---|---:|---:|---|
| CAND1 | `5.85x` | `6.35x` | no |
| CAND2 | `24.92x` | `29.10x` | no |

So the requested 10-order reduction was not achieved.

## Avenue B: Analytical Burnol-Kernel Evaluation

I ran a dps=200 `mpmath.quad` probe for the Burnol `E_lambda` integral using the inherited finite-resolvent convention.  The probe completed, but the inherited artifacts do not contain a closed formula for the full projected commutator c-entry after `P`, sinc convolution, PSWF truncation, and transport sampling.  Therefore the analytical c-matrix avenue is blocked at formula level, not arithmetic precision.

## CAND1 vs CAND2

Using the refined 2000-node c-matrices and proxy errors from the 200-vs-2000 difference:

| candidate | refined `|Xi|` | proxy error | decision |
|---|---:|---:|---|
| CAND1 | `1.0110381170e-2` | `8.9106130286e12` | not individually decisive |
| CAND2 | `7.8384611222e65` | `5.9008860463e64` | nonzero under proxy |

The intervals are disjoint: CAND1 upper proxy scale is `~8.9e12`, while CAND2 lower proxy scale is `~7.25e65`.  Thus the two sampled candidate transport formulas disagree decisively after grid refinement.

## Verdict

`V_branch_B_c_matrix_refined_disagrees_hard_block`.

This is a hard block for the inherited CAND1/CAND2 candidate-transport comparison, not a proof of RH or a resolution of the missing exact Burnol transport theorem.
