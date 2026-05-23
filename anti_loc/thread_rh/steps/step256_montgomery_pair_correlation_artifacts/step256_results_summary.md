# Step 256 Results Summary

## Montgomery Pair-Correlation Carrier

For zeta zeros `rho_n = 1/2 + i gamma_n`, normalized by

`tilde_gamma_n = gamma_n log(gamma_n)/(2*pi)`,

define the zero-pair count

`R_2(alpha,beta;T) = (1/N(T)) #{(n,m): alpha < tilde_gamma_n - tilde_gamma_m < beta, n != m}`.

The GUE prediction is

`R_2(alpha,beta;T) -> int_alpha^beta (1 - (sin(pi*u)/(pi*u))^2) du`.

Residual:

`Xi_MPC(alpha,beta;T) = |R_2(alpha,beta;T) - GUE_integral(alpha,beta)|`.

Closure: `lim_{T->infty} Xi_MPC(alpha,beta;T)=0` for all `alpha < beta`.

## Known Status

Montgomery proved the restricted Fourier-support/range result under RH
(`|u| < 1`, equivalently the restricted pair-correlation theorem).  The full
GUE pair-correlation conjecture remains open.  Odlyzko's computations gave
strong numerical evidence at high zeta-zero heights.

## Classification

Montgomery pair correlation is not known equivalent to RH.  It is also not a
per-L zero-location residual, so it remains outside the Riemann Dichotomy and
outside the single-L Selberg-Class Dichotomy Generalization.

However, it is a correlation residual.  It fits the Selberg-Class
Cross-Correlation Extension after a subtype refinement:

- Type Ia: coefficient correlations across L-functions, e.g. SOC and full
  Selberg orthonormality.
- Type Ib: zero correlations for one L-function, e.g. Montgomery pair
  correlation and Hejhal triple correlation.
- Type II: multi-L or family zero correlations, e.g. Rudnick-Sarnak /
  Katz-Sarnak style n-level statistics.

## Framework Update

The cross-correlation extension is now `candidate (verified-on-3-Selberg-
instances, subtype-refined) corpus-pending`.

`anti_loc/findings_framework.md` was updated accordingly.

## Verdict

`V_montgomery_subtype_refinement`.

No proof of Montgomery pair correlation, RH, or GRH is claimed.
