# Step 257 Results Summary

## Rudnick-Sarnak Type II Carrier

Carrier: n-level zero correlations for principal/cuspidal automorphic
L-functions, especially GL(N), in families or multi-L settings.

For zeros `rho_j(pi)=1/2+i gamma_j(pi)`, define a normalized n-level statistic
`R_n^family(f;T)` against a Schwartz test function `f`.  The residual is

`Xi_RS(f;T) = |R_n^family(f;T) - GUE_n_level(f)|`.

Closure: `lim_{T->infty} Xi_RS(f;T)=0` for admissible `f`, and conjecturally
beyond the restricted Fourier-support ranges known in theorems.

## Proved vs Open

Rudnick-Sarnak 1996 proves n-level GUE correlations for principal L-functions
in restricted Fourier support.  This is not the full unrestricted conjecture.
Katz-Sarnak and Iwaniec-Luo-Sarnak provide the broader family-zero-statistics
framework.

## Type Classification

- Single-`pi` n-level statistics: Type Ib, single-L zero correlations.
- Multi-`pi` / family n-level statistics: Type II, multi-L/family zero
  correlations.

This completes the subtype matrix:

| subtype | meaning | instances |
|---|---|---|
| Type Ia | multi-L coefficient correlations | SOC; full Selberg orthonormality |
| Type Ib | single-L zero correlations | Montgomery pair correlation |
| Type II | multi-L/family zero correlations | Rudnick-Sarnak n-level/family correlations |

## Framework Update

The Selberg-Class Cross-Correlation Extension is now:

`candidate (verified-on-4-Selberg-instances, all-three-subtypes-covered) corpus-pending`.

`anti_loc/findings_framework.md` was updated.

## Verdict

`V_rudnick_sarnak_type_II_instance`.

No proof of the full Rudnick-Sarnak conjectural range, GRH, or RH is claimed.
