# Step 196 Results Summary

## Verdict

`V_branch_C_dataset_generic_foreclosure`.

The Branch C terminal matrix element

```text
L_{rho,k}(G) = <M_zeta G, P_infty y_{rho,k}>
```

was evaluated on an extended dataset of 18 triples.  The dataset covers the first six critical-line zeta zero ordinates, two evaluator orders (`k=0` and finite-difference diagnostics for `k=1`), and five legal three-bump Burnol generators on `[1,4]`.

All 18 computed values are separated from zero by the stated error budget.  The smallest certified lower bound is

```text
min(|L| - error) = 3.4126458948014055e-02
```

at `(rho_1, k=0, G_high)`.

## Numerical Method

The computation reused the Step 175/176 convention:

- `lambda = 1`
- `U = 200`, grid spacing `h = 0.05`
- `mpmath` precision `50` decimal digits for zeta values
- Gauss-Legendre quadrature for Mellin transforms of bump generators
- PSWF approximation by sinc-kernel diagonalization on `[-1,1]`
- `N_PSWF_PRIMARY = 320`, with a secondary `N_PSWF_ALT = 240` comparison folded into the error estimate
- `k=1` values are central finite-difference diagnostics of the already projected value, with the error inflated by the finite-difference scale

## Dataset Highlights

Representative values:

| case | triple | L | abs(L) | error |
|---|---|---:|---:|---:|
| C01 | `(rho_1, 0, G_star)` | `0.1214665 - 0.0898573 i` | `0.151091` | `1.965e-4` |
| C06 | `(rho_6, 0, G_star)` | `-0.0833893 - 0.0131859 i` | `0.084425` | `1.922e-4` |
| C07 | `(rho_1, 0, G_prime)` | `0.204214 - 0.0735031 i` | `0.217039` | `8.432e-5` |
| C15 | `(rho_1, 0, G_high)` | `-0.00765558 - 0.0338240 i` | `0.0346795` | `5.531e-4` |
| C16 | `(rho_1, 1, G_star)` | `-0.203489 + 0.205803 i` | `0.289417` | `1.970e-2` |
| C18 | `(rho_1, 1, G_prime)` | `-0.394157 + 0.0779687 i` | `0.401794` | `8.500e-3` |

## Structural Pattern

The extended dataset reinforces the Step 176 generic-foreclosure finding.  No tested triple produced a near-zero value.  The `k=0` absolute values range from `3.467955e-02` to `2.170389e-01`; the `k=1` finite-difference diagnostics range from `2.885740e-01` to `4.017945e-01`, with larger but still well-separated error bars.

No clean monotone law in the zero ordinate `gamma` is visible at this sample size.  The observed Pearson correlation between `gamma` and `|L|` for `k=0` is approximately `-0.198`, so the present data support robustness of nonvanishing rather than a scaling law.

## Branch C Status

The full-carrier shifted co-Poisson ZI-COV(i) route remains foreclosed on the inherited `U_infty` and `lambda=1` normalization.  The zero-free output subclass from Step 170 remains retained, but the extended data provide no evidence for a broader annihilating subclass.

