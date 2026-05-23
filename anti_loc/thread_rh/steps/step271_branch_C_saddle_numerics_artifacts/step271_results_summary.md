# Step 271 Results Summary

Verdict: `V_branch_C_closed_form_mismatched`.

The saddle equation

```text
(log h)'(z*) = (k+1)/(z* - rho),  h(z)=zeta(z) M(G)(z)
```

was solved numerically using the Step 196 right-Mellin convention
`M(G)(z)=int G(t)t^{-z}dt`, reconstructed from the inherited quadrature and
generator definitions.  `mpmath` precision was set to 55 dps; zeta
log-derivatives were computed by high-precision central finite differences.

Tracked saddle radii:

| triple | k=1 | k=2 | k=5 | k=10 | k=20 |
|---|---:|---:|---:|---:|---:|
| `rho1_G_star` | 0.6715 | 1.2821 | 2.8671 | 5.0620 | 8.8422 |
| `rho2_G_star` | 0.6267 | 1.1387 | 2.3815 | 4.2792 | 8.0244 |
| `rho1_G_prime` | 0.7120 | 1.3814 | 3.1139 | 5.5126 | 9.4933 |

The naive radius prediction `b=-log|z*-rho|` is not stable: by k=20 it is
negative, between `-2.08` and `-2.25`, while Step 269 fitted positive
exponents.

Using the saddle magnitude template and fitting `a*(k+1)^c*exp(b*k)` over the
tracked saddle predictions gives:

| triple | saddle b | saddle c | Step 269 poly b | Step 269 poly c |
|---|---:|---:|---:|---:|
| `rho1_G_star` | 0.7994 | -0.1380 | 0.7497 | -0.2998 |
| `rho2_G_star` | 0.9504 | -0.1087 | 1.0832 | -1.1248 |
| `rho1_G_prime` | 0.7129 | -0.0987 | 0.6441 | -0.1369 |

The `b` values are directionally close for two triples and borderline for one,
but the `c` values do not match within the requested 10% criterion.  The
failure is severe for `rho2_G_star` and still outside tolerance for the other
two.

Assessment: the saddle numerics partly explain why an exponential envelope is
visible, but they do not establish the requested closed-form Branch C law.  The
projected Branch C corrections from Step 270 and the saddle branch selection
remain active gaps.

No Branch C closure and no RH consequence are claimed.
