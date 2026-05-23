# Step 270 Results Summary

Verdict: `V_branch_C_stationary_phase_partial`.

The Burnol evaluator identity was separated into the raw source term and the
actual projected Branch C value.

In the inherited Step 196/269 pipeline,

```text
delta_Dk(rho,G) = (zeta * M(G))^(k)(rho)
```

holds for the unprojected Mellin derivative term by the Burnol 2004 Section 6
evaluator relation and the Leibniz rule.  However the Branch C quantity tested
in Steps 247-269 is not just `delta_Dk`; it is

```text
L_k = delta_Dk - I_k - R_k
```

where `I_k` is the sinc/projection integral and `R_k` is the finite PSWF
projection correction.

Raw/product derivative versus projected Step 269 values:

| triple | raw/projected abs ratio k=1 | k=2 | k=3 | k=4 | k=5 | k=6 | k=7 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `rho1_G_star` | 0.548 | 0.782 | 0.900 | 0.952 | 0.978 | 0.989 | 0.995 |
| `rho2_G_star` | 0.544 | 0.806 | 0.934 | 0.979 | 0.996 | 0.999 | 1.000 |
| `rho1_G_prime` | 0.567 | 0.801 | 0.914 | 0.960 | 0.984 | 0.993 | 0.998 |

This supports a qualitative explanation: the raw derivative source term
appears to dominate at higher tested k.  It does not establish the closed
identity requested for the actual Branch C projected matrix element.

The stationary-phase template gives

```text
h^(k)(rho) = k!/(2*pi*i) int h(z)/(z-rho)^(k+1) dz
(log h)'(z_*) = (k+1)/(z_*-rho)
```

For a nondegenerate saddle after cancellation of the naive factorial scale,
the generic prefactor is `k^(-1/2)`, suggesting a baseline `c=-1/2`.  The
Step 269 exp-polynomial fits give:

| triple | numerical b | numerical c | baseline c |
|---|---:|---:|---:|
| `rho1_G_star` | 0.7497 | -0.2998 | -0.5 |
| `rho2_G_star` | 1.0832 | -1.1248 | -0.5 |
| `rho1_G_prime` | 0.6441 | -0.1369 | -0.5 |

The `c` values are qualitatively in a negative-polynomial prefactor regime
but are not universal.  The exponent `b` remains undetermined from the
available saddle template because it depends on the saddle geometry of the
projected kernel, not only on `zeta*M(G)`.

No Branch C closure and no RH consequence are claimed.
