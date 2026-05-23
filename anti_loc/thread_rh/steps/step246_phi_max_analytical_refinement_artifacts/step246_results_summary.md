# Step 246 Results Summary

## Phi Grid

Recomputed the inherited wavepacket pipeline at `T=10000`, `mpmath_dps=100`, `GL1400` local-window quadrature, and 24 PSWF terms for 90 grid points:

- `sigma in {0.1,...,1.0}`.
- `ell in {0.5, log 2, 1.0, log 3, 1.5, log 5, 2.0, log(10)/4, 2.5}`.

Grid range:

- min Phi = `0.12848233592000288`.
- max Phi = `0.4898488467749268` at `(sigma, ell) = (0.4, 2.0)` on this grid.
- mean Phi = `0.3354896768976285`.

This is consistent with step 220's refined maximum `Phi_max = 0.4904766190` near `(sigma, ell) = (0.35, 2.0)`.

## Fits Tested

The theorem-shaped candidate remains the high-pass/low-pass two-erf band-shift model:

```text
Phi^2 = 0.5 * (erf(sigma*(1+ell)) - erf(sigma*a(ell)))
a(ell) = 1 for ell <= 2, and ell - 1 for ell > 2.
```

Residuals on the inherited truncated-Gaussian numerical pipeline:

| Fit | RMSE | Max residual |
|---|---:|---:|
| two-erf band shift, no fit | `3.5846804717e-3` | `1.3588215221e-2` |
| two-erf band shift, scaled sigma | `3.4233392285e-3` | `1.2414368725e-2` |
| pure erf affine | `6.4869070712e-2` | `2.2926712678e-1` |
| Voigt profile | `6.3327746713e-2` | `1.6695271420e-1` |
| sinc model | `7.3356484138e-2` | `1.7719860196e-1` |
| flexible two-erf affine edges | `2.5877137384e-2` | `6.6337402309e-2` |

No fit reaches the `1e-4` closed-form-precise threshold.

## Constant Lookup

No low-complexity standalone constant was identified for `0.4904766190`. The closest theorem-shaped expression is parametric: the untruncated band model peaks at `ell=2`, `sigma=sqrt(log(3)/8)`, giving `0.492101613760664`, which is `1.62e-3` away from the inherited numerical maximum.

Web lookup notes: OEIS decimal-string search returned no direct hit for `0.490476619`; the CARMA ISC Plus page describes inverse-symbolic lookup tables but reports the service is down for maintenance indefinitely.

## Verdict

`V_phi_no_simple_closed_form`.
