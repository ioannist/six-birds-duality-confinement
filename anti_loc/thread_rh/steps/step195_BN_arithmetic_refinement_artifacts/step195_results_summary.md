# Step 195 Results Summary

## Verdict

`V_BN_arithmetic_refined_RH_consistent`.

The harmonic Beurling-Nyman chain was extended to `N=1000` using an arithmetic Gram formula for reciprocal-integer parameters:

`G_{p,q} = sum_{n>=1} ((n mod p)/p) ((n mod q)/q) / (n(n+1))`.

An equivalent finite periodized form is

`G_{p,q} = (1/L) sum_{r=1}^L {r/p}{r/q} [psi((r+1)/L)-psi(r/L)]`,

where `L=lcm(p,q)` and `psi` is the digamma function.  This was verified by high-precision spot checks.

Large dense matrices used the arithmetic series in vectorized form with `X_MAX=200000`, giving tail bound per Gram entry `<=5e-6`.  Scalar source values used `mpmath` at 80 dps; dense pseudoinverses used NumPy float64 SVD with `rcond=1e-12`.

## Computed Data

| N | delta_A^2 | delta_A^2 log N |
|---:|---:|---:|
| 200 | 0.00892242600837 | 0.0472738446719 |
| 500 | 0.00741541353971 | 0.0460838890371 |
| 1000 | 0.00654423096394 | 0.0452059459881 |

Full table includes `N = 5, 10, 20, 40, 80, 200, 500, 1000`.

## Decay Fit

- Mean of `delta_A^2 log N` over `N = 80, 200, 500, 1000`: `C ≈ 0.0466828337786`.
- Fit `delta_A^2 ~ C/(log N)^alpha` over `N >= 20`: `C ≈ 0.0541389792663`, `alpha ≈ 1.0886679`.
- Power-law comparison gives `beta ≈ 0.2295`, but the log model is the BN-relevant model.

The refined data are consistent with the Báez-Duarte slow-logarithmic behavior.  They do not prove RH or close the infinite BN residual.

