# Step 278 Results Summary — Pure-mpmath \(\Phi_{\max}\) Attempt

## Pipeline Status

The NumPy bottleneck from Step 277 was identified as the inherited local-window quadrature / matrix path, especially the PSWF/Sonine projection machinery.  Step 278 replaced the critical numerical path with:

- `mpmath.gauss_quadrature` composite panels;
- `mpmath.matrix` operators;
- pure-mpmath sinc hard-band projection proxy;
- no NumPy in `compute_phi_max_pure_mpmath_step278.py`.

The full pure-mpmath PSWF eigensystem / SVD replacement for the exact inherited Sonine projection was **not completed**.  This is the decisive limitation.

## Convergence Check

Reference inherited value:

```text
0.4904766200298252
```

Pure-mpmath proxy values:

| N | dps | T | Phi |
|---:|---:|---:|---:|
| 40 | 80 | 5000 | 1.8263657332897929 |
| 80 | 80 | 5000 | 0.7483530224406918 |
| 120 | 80 | 5000 | 0.7703229429918259 |
| 160 | 80 | 5000 | 0.5939102228020887 |
| 80 | 120 | 5000 | 0.7483530224406918 |
| 80 | 80 | 10000 | 0.7483530224406918 |

The dps increase is internally stable for the same discretization, but the values do not converge to the inherited reference.  Trusted digits versus the reference: `0`.

## PSLQ Retry

Because no trusted high-precision \(\Phi_{\max}\) value was produced, the PSLQ retry was recorded as `not_run_unstable_input`.  This avoids turning discretization artifacts into false closed forms.

## Verdict

`V_branch_A_high_precision_partial`.

The NumPy precision caveat was addressed directly, but the pure-mpmath replacement did not converge and did not enable a valid high-precision PSLQ search.
