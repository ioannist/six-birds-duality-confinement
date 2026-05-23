# Step 366 Candidate Derivations for the Branch C Height Coefficient

Inherited baseline:

- Step 324: `gamma ~= A*T^alpha + B*d^beta` with `A = 4.118`, `alpha = -0.997`, `B = -0.039`, `beta = 0.409`.
- Step 325: Stirling-Gamma derivations predicted constants on the order of `1/2` or `1/6`, not `4.118`; this route failed.
- Step 316/317: high-order Hadamard log-derivative power sums are dominated by the nearest neighbor zero.

## Candidate (a): Local Zero Density

Riemann-von Mangoldt gives local zero density

`rho_zero(T) = (1/(2*pi))*log(T/(2*pi))`.

The local mean spacing is

`spacing(T) = 1/rho_zero(T) = 2*pi/log(T/(2*pi))`.

The candidate scale is the half-spacing

`A_density(T) = spacing(T)/2 = pi/log(T/(2*pi))`.

At `rho_1`, this gives `3.87488581199`, within `5.9%` of the global Step 324 coefficient `A = 4.118`.

Interpretation: Branch C's height coefficient appears to be tied to the symmetric local zero-density scale, not to the full local mean spacing.

## Candidate (b): Plancherel / Spectral Density

The same density appears as the critical-line spectral density. The unhalved inverse density

`A_Plancherel(T) = 2*pi/log(T/(2*pi))`

gives `7.74977162399` at `rho_1`, about `88%` above `A = 4.118`. This overpredicts by nearly a factor of two. If the critical-line pairing is symmetrized by the pair of directions around a zero, it collapses back to Candidate (a).

## Candidate (c): Zeta-Derivative Ratio Scale

Two direct derivative-ratio scales were tested:

- `A_zeta_prime(T) = 1/|zeta'(rho)|`.
- `A_zeta_ratio(T) = 1/|zeta''(rho)/zeta'(rho)|`.

At `rho_1`, these are `1.26078` and `1.20914`, far below `4.118`. Across `rho_1..rho_5`, both have mean relative error above `0.64` against `gamma*T`.

## Interpretation

The only candidate with the correct global scale is half the local mean zero spacing. It also gives the best cross-zero behavior against the contaminated per-zero values `gamma_j*T_j`, though spacing correction and finite-k fit noise remain visible.
