# Step 366 Results Summary

Step 366 tested three structural-origin candidates for the empirical height coefficient from Step 324.

## Candidate Results

Candidate (a), local zero density:

`A_density(T) = pi/log(T/(2*pi))`.

At `rho_1`, this gives `3.8749`, only `5.9%` below the global `A_G_star = 4.118`. Against the per-zero contaminated values `gamma_j*T_j` for `rho_1..rho_5`, its mean relative error is `0.168`; it is within `20%` for three of five zeros and just misses for `rho_4`.

Candidate (b), unhalved Plancherel inverse density:

`A_Plancherel(T) = 2*pi/log(T/(2*pi))`.

At `rho_1`, this gives `7.7498`, overpredicting `A_G_star` by `88%`. It is effectively a factor-of-two miss.

Candidate (c), zeta-derivative ratio scales:

`1/|zeta'(rho)|` and `1/|zeta''(rho)/zeta'(rho)|`.

At `rho_1`, these give `1.2608` and `1.2091`, far below `A_G_star`; cross-zero mean relative errors exceed `0.64`.

## Verdict

Partial structural origin identified: `A` is plausibly governed by **half the local Riemann-von Mangoldt mean zero spacing**, not by Gamma/Stirling terms or direct zeta-derivative ratio amplitudes.

This is not a proof. The remaining gap is to derive why Branch C's `(mag, phase, operator)` geometry selects the half-spacing normalization and how the `B*d^beta` spacing correction couples to it.
