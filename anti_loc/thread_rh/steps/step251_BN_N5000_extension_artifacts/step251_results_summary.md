# Step 251 Results Summary

## Target

Extend the Beurling-Nyman harmonic chain computation for
`A_N = {1/k : 1 <= k <= N}` to `N = 3000, 4000, 5000`.

The computation reuses the arithmetic Gram formula from steps 195/199:

`G_{p,q} = sum_{n>=1} ((n mod p)/p)((n mod q)/q)/(n(n+1))`.

Scalar setup used `mpmath` at 80 dps.  The large Gram matrix was built in
`float64` by vectorized arithmetic-series accumulation through
`X_MAX = 300000`, giving per-entry tail bound `<= 3.33333e-6`.  The active
submatrices were evaluated by symmetric eigen-pseudoinverse with
`rcond = 1e-12`.

## Computed Values

| N | delta_sq | delta_sq * log(N) | rank | condition proxy |
|---:|---:|---:|---:|---:|
| 2000 calibration | `0.00609996484863` | `0.0463652378211` | 1999 | `1.79e7` |
| 3000 | `0.00558973365837` | `0.0447534622742` | 2999 | `4.48e7` |
| 4000 | `0.00538148417111` | `0.0446342968526` | 3999 | `8.69e7` |
| 5000 | `0.00525837798558` | `0.0447866211767` | 4999 | `1.42e8` |

The N=2000 calibration differs from step 199 by `+1.7095e-4` in delta_sq,
using the larger `X_MAX=300000` truncation.

## Updated Decay Fit

Tail mean over `N >= 200` through 5000:

`C = mean(delta_sq * log N) = 0.045311325284006`, spread `0.000862754`.

Recent tail mean over `N >= 1000`:

`C = 0.0448554780938519`, spread `0.000208024`.

Power-log fit:

`delta_sq ~ C / (log N)^alpha`

- `N >= 20`: `C = 0.0545618913647252`, `alpha = 1.094554992`
- `N >= 200`: `C = 0.0572138071988156`, `alpha = 1.118314712`
- `N >= 1000`: `C = 0.0488745892509167`, `alpha = 1.041904016`

## Verdict

`V_BN_N5000_consistent`.

The slow-log pattern persists through `N=5000`.  This remains a finite-chain
diagnostic and does not prove the Beurling-Nyman criterion or RH.
