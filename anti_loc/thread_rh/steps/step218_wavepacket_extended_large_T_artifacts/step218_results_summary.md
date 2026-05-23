# Step 218 Results Summary

## Target

Extend the Step 217 wavepacket Weyl test from `T <= 300` to large centers `T in {300, 1000, 3000, 10000}`.

## Method

The computation uses a moving local Gauss-Legendre window centered at each `T`, with half-width `80`, so the width-1 packet is resolved even at `T=10000`. The translation-invariant sinc part of `P_infty` is evaluated on the local coordinate differences; the finite PSWF correction is evaluated at the actual large ordinates.

Primary parameters:

- `sigma = 1.0`.
- `ell = log 2`.
- `N_grid = 1400`.
- `N_PSWF_terms = 24`.
- Conservative error budget: `7.5e-2`.

## Large-T Values

`||C_l u_T||`:

- `T=300`: `0.26384160439935056`
- `T=1000`: `0.26384558925113083`
- `T=3000`: `0.26384586398729620`
- `T=10000`: `0.26384586882096250`

Trend:

- Minimum: `0.26384160439935056`.
- Conservative lower after error: `0.18884160439935055`.
- Drift from min to max: `4.264421611943625e-6`.
- Ratio `T=10000 / T=300`: `1.00001616280958294`.

No decay is visible through `T=10000`; the large-T data is flat at displayed precision.

## Robustness

- `sigma=0.5`, `ell=log2`: `0.351218` at `T=1000`, `0.351218` at `T=10000`.
- `sigma=0.5`, `ell=log3`: `0.413214` at `T=1000`, `0.413214` at `T=10000`.
- `sigma=1.0`, `ell=log3`: `0.276368` at `T=1000`, `0.276368` at `T=10000`.
- Window check at `T=10000`, `sigma=1`, `ell=log2`: `0.262169` for width 40, `0.263846` for width 80, `0.264677` for width 120.

## Verdict

`V_wavepacket_large_T_constant`.

The Step 217 `C_l P_infty` lower bound persists through `T=10000` with essentially constant norm. This strengthens the essential-norm diagnostic for `C_l P_infty`; it still does not decide the narrower `C_l P_eta` Branch A question.
