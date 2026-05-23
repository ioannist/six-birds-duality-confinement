# Step 185: Selberg / Maass Carrier Pivot

Verdict:

`selberg_verdict = V_selberg_closes_with_proved_RH`.

Carrier declaration:

For `Gamma = SL_2(Z)` (equivalently `PSL_2(Z)` up to the center), use

```tex
H_Gamma = L^2(Gamma \ H, dmu),  dmu = dx dy / y^2.
```

The native operator is the positive self-adjoint hyperbolic Laplacian

```tex
Delta = -y^2(partial_x^2 + partial_y^2).
```

Its spectral decomposition contains Maass cusp-form eigenvalues
`lambda_j = 1/4 + r_j^2`, residual/discrete terms, and continuous Eisenstein
spectrum.

Selberg zeta:

```tex
Z_Gamma(s)= product_{primitive geodesics P} product_{k>=0}
(1 - N(P)^(-s-k)).
```

Native residual:

`Xi_Gamma` is the Selberg trace-formula defect between the spectral side of
the Laplacian and the geometric side of primitive closed geodesics plus
identity, parabolic/scattering, and residual correction terms.

Closure status:

`Xi_Gamma = 0` on the native Selberg carrier by the Selberg trace formula,
with the Selberg-zeta RH analog supplied by the self-adjoint spectral
realization of the relevant zeros. This is a native proved analog, not a proof
of Riemann RH.

CRE audit:

`CRE_status = not_CRE`. Closing `Xi_Gamma` for `Z_Gamma` is not logically
equivalent to closing the Riemann zeta residual. Therefore CRCFT does not
apply as a foreclosure taxonomy here.

Implication:

The framework closes a non-CRE RH-analogous carrier when the carrier supplies
its complete native spectral/geometric ledger. This supports the distinction:
CRCFT is triggered by classical-RH-equivalent carriers, not by every proved
RH-style trace carrier.
