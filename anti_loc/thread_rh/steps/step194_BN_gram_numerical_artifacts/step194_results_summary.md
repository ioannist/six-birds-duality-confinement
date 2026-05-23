# Step 194 Results Summary

## Verdict

`V_BN_numerical_structural_pattern`.

The finite Beurling-Nyman Gram experiment shows a clear structural split:

- `A_N={1/k:1<=k<=N}` decays slowly and is consistent with the Báez-Duarte logarithmic picture.
- Sparse reciprocal chains `{2^{-k}}`, `{1/k^2}`, and a fixed random reciprocal subset plateau at the tested scale.

This does not establish RH and does not refute RH.  It makes the CTMT-like finite Gram subinterface concrete: the finite matrix entries are computable, but the infinite closure limit remains target-equivalent.

## Numerical Method

Parameters are reciprocal integers `a=1/q`.  With `x=1/t`,

`rho_a(1/x)=a floor(x)-floor(a x)`.

For reciprocal integers this is constant on each unit interval `(n,n+1)`, so the script computes Gram entries by deterministic unit-interval summation:

`int_n^{n+1} rho_a(1/x) rho_b(1/x) dx/x^2`.

Settings:

- `mpmath_dps = 50` for scalar source vector values.
- `numpy float64` SVD pseudoinverse.
- `X_MAX = 200000`; tail bound per Gram entry `<= 5e-6`.
- `pinv_rcond = 1e-12`.

## Representative Values

| family | N=5 | N=20 | N=80 | pattern |
|---|---:|---:|---:|---|
| harmonic `{1/k}` | 0.036313936859 | 0.016532331786 | 0.010992095538 | slow log decay |
| geometric `{2^{-k}}` | 0.127343192044 | 0.127038005030 | 0.127035826960 | plateau |
| power `{1/k^2}` | 0.207973000023 | 0.207294900712 | 0.207292597760 | plateau |
| random reciprocal | 0.619587408711 | 0.617952020015 | 0.617707146255 | plateau |

For harmonic, `delta_A^2 log N` stays near `0.05` for `N>=20`.  That is consistent with the expected slow logarithmic behavior in the Báez-Duarte/Nyman-Beurling literature.

