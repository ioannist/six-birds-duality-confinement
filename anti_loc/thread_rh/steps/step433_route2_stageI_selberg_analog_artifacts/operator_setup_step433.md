# Step 433 Operator Setup

Define

```text
H_space = L^2(M_0, dmu_M),
H = Delta_M = -div grad.
```

Since `M_0` is compact without boundary, `Delta_M` on `C^infty(M_0)` is essentially self-adjoint and has a unique nonnegative self-adjoint extension. The spectrum is discrete:

```text
0 = lambda_0 < lambda_1 <= lambda_2 <= ...,
lambda_n -> infinity.
```

For Selberg trace formula notation, write `lambda_n = 1/4 + r_n^2` for the high spectrum, with finitely many small eigenvalues handled separately.

No arithmetic boundary condition or zeta-zero spectral stipulation is used.
