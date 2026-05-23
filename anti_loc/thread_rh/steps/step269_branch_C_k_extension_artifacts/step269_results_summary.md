# Step 269 Results Summary

Verdict: `V_branch_C_polynomial_correction`.

The Branch C dataset was extended to k=5, 6, 7 for the same three triples as
step 250, using the inherited step 196/250 quadrature and PSWF pipeline at
`mpmath` 90 dps.

New values:

| triple | k=5 | k=6 | k=7 |
|---|---:|---:|---:|
| `rho1_G_star` | `4.373822966988 +/- 8.88e-6` | `8.804781976434 +/- 1.12e-5` | `17.958730549970 +/- 3.37e-5` |
| `rho2_G_star` | `6.187878923392 +/- 6.64e-6` | `15.417394277714 +/- 7.30e-6` | `39.189293968779 +/- 5.02e-6` |
| `rho1_G_prime` | `4.676864962801 +/- 2.54e-6` | `8.700017345945 +/- 3.20e-6` | `16.316879205385 +/- 4.86e-5` |

Pure exponential fit on k=0..7:

| triple | a | b | RMSE k=0..7 | RMSE k=0..4 |
|---|---:|---:|---:|---:|
| `rho1_G_star` | `0.1293040638` | `0.7046255999` | `3.69e-2` | `2.74e-3` |
| `rho2_G_star` | `0.0612709944` | `0.9228326092` | `1.25e-1` | `3.38e-2` |
| `rho1_G_prime` | `0.2082597819` | `0.6228614952` | `2.47e-2` | `3.50e-3` |

The exponential law remains directionally correct and all fitted `b` values
stay in an exponential-growth regime, but the k=0..7 fit is not as clean as
k=0..4.

The model `a*(k+1)^c*exp(b*k)` improves RMSE:

- `rho1_G_star`: RMSE `1.65e-2`, `c=-0.300`.
- `rho2_G_star`: RMSE `2.11e-2`, `c=-1.125`.
- `rho1_G_prime`: RMSE `1.54e-2`, `c=-0.137`.

Assessment: exponential growth persists, but the extended data favor an
exponential law with a negative polynomial correction over a pure exponential.
No Branch C closure or RH consequence is claimed.
