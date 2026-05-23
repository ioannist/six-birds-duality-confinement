# Step 217 Results Summary

## Target

Test `C_l P_infty` on Gaussian wavepacket Weyl sequences localized at far-apart critical-line ordinates. This avoids the near-parallel `kappa` sequence issue from Steps 214-216.

## Construction

Primary packets:

`u_n(tau) = Z_n^{-1/2} exp(-(tau - T_n)^2/(2 sigma^2)) 1_{|tau-T_n|<3 sigma}`

with:

- `T_n = 30 n`, `n=1..10`.
- `sigma = 1.0`.
- `ell = log 2`.
- `||u_n||_{L^2(d tau/2 pi)} = 1`.
- Operator: `C_l u_n = (I - P_infty) M_{m_l} P_infty u_n`.

This tests `C_l P_infty`, not the finite evaluator carrier `C_l P_eta`.

## Results

Primary `||C_l u_n||` values:

`0.264162, 0.264780, 0.264507, 0.266053, 0.264949, 0.264790, 0.265199, 0.264650, 0.265504, 0.264970`

Weak-null / orthogonality check:

- Numerical max pairwise overlap: `0.0` at displayed precision.
- Analytic Gaussian overlap for adjacent centers is bounded by `exp(-30^2/4)`, before truncation; truncation makes the finite-grid overlap exactly zero in this model.

Trend:

- Minimum: `0.26416193343444977`.
- Conservative lower after error `7.5e-2`: `0.18916193343444976`.
- Tail minimum over `n=6..10`: `0.2646502242790166`.
- No decay observed through `T=300`.

Robustness:

- `sigma=0.5`: lower around `0.351`.
- `sigma=2.0`: near-zero/uncertain around `0.047`.
- `ell=log 3` and `ell=1.0`: bounded below around `0.277` and `0.275`.
- spacing `10` and `50`: bounded below around `0.264`.

## Verdict

`V_wavepacket_essential_obstruction`.

This certifies a finite-model essential-norm lower-bound diagnostic for `C_l P_infty` along a genuine weak-null wavepacket sequence. It does not decide the narrower Branch A object `C_l P_eta`.
