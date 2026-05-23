# Step 219 Results Summary

## Target

Investigate the large-`T` essential-norm value

`Phi(sigma, ell) = lim_T ||C_ell u_T||`

seen in Steps 217-218 for Gaussian wavepackets.

## Phi Values: sigma = 1

At `T=10000`:

| ell | Phi |
|---:|---:|
| 0.1 | 0.130865 |
| 0.25 | 0.197482 |
| 0.5 | 0.246751 |
| log 2 | 0.263846 |
| 1.0 | 0.274862 |
| log 3 | 0.276368 |
| pi/2 | 0.278822 |
| log 5 | 0.278868 |
| log 7 | 0.279020 |
| 2.0 | 0.277880 |
| log 10 | 0.179178 |
| 5.0 | 0.001115 |

The curve rises to a plateau near `0.279` for `ell` near `1.5..2`, then drops for larger shifts.

## Phi Values: ell = log 2

| sigma | Phi |
|---:|---:|
| 0.25 | 0.293059 |
| 0.5 | 0.351218 |
| 1.0 | 0.263846 |
| 2.0 | 0.047012 |
| 5.0 | 0.001215 |

The `sigma` dependence is non-monotone: it peaks around `sigma=0.5` and decays sharply for wide packets.

## Fits

Generic fits performed poorly:

- Power law RMSE: `8.18e-2`.
- Logarithmic RMSE: `1.52e-1`.
- Saturating exponential RMSE: `1.19e-1`.
- Sinc-like RMSE: `5.60e-2`.
- Sigmoid-like RMSE: `7.68e-2`.

Best structured model:

`Phi^2 ≈ 0.5 * (erf(sigma*b(ell)) - erf(sigma*a(ell)))`,

where `a(ell)=1` for `ell<=2`, `a(ell)=ell-1` for `ell>2`, and `b(ell)=ell+1`.

This is the natural Gaussian spectral-band shift model from the sinc projection. For `sigma=1`, it gives:

- RMSE: `2.40e-3`.
- Max residual: `6.07e-3`.

With two fitted parameters (`scale=0.97977`, `sigma_eff=0.98932`):

- RMSE: `1.47e-3`.
- Max residual: `4.15e-3`.

For the sigma sweep at `ell=log2`, the same model gives RMSE `1.47e-3`, max residual `2.11e-3`.

## Verdict

`V_essential_norm_ell_dependence_numerical_pattern`.

A clean error-function band-shift pattern was identified, but not at the `<1e-4` residual level required to declare a simple closed form.
