# Step 349 Virtual Free-Energy Algebra

## Carrier

Finite carrier:

`K = {rho_1, rho_2, rho_3}` with coordinates `(T_j, d_j, G_star)`, where
`T_j = Im(rho_j)` and `d_j` is the local zero-spacing diagnostic inherited from step 324.

Numerical carrier values:

- `rho_1`: `T = 14.1347`, `d = 6.8873`
- `rho_2`: `T = 21.0220`, `d = 3.9888`
- `rho_3`: `T = 25.0109`, `d = 3.9888`

## Dimensionless Temperature Lens

The literal pair of derivative requirements in the prompt,
`gamma_infty = -partial_T F = T partial_T F`, is inconsistent for positive `T`
unless `gamma_infty = 0`.  The finite algebra therefore records this as an
overconstrained raw lens and uses the dimensionless-temperature lens

`u = -log T`, so `partial_u = -T partial_T`.

The thermodynamic readout is

`gamma_infty = partial_u F = -T partial_T F`

on the stationary branch.

## Virtual Field

The inherited step 324 high-k shape is used only as a finite external field,
not by calling any `L_k` evaluator:

`theta(T,d) = A T^alpha + B d^beta`

with

- `A = 4.118`
- `alpha = -0.997`
- `B = -0.039`
- `beta = 0.409`

## Free-Energy Density

For each carrier point `sigma = (T,d,G_star)`, adjoin a virtual free-energy
density in the asymptotic order parameter `gamma`:

`F_sigma(gamma) = (1/2) gamma^2 + (lambda/4) gamma^4 - theta(T,d) gamma`

with fixed interaction parameter `lambda = 0.75`.

## Self-Consistency / Fixed Point

Stationarity gives

`partial_gamma F_sigma = gamma + lambda gamma^3 - theta(T,d) = 0`.

Equivalently,

`gamma = S_sigma(gamma) := theta(T,d) - lambda gamma^3`.

Because `gamma + lambda gamma^3` is strictly increasing for `lambda > 0`,
the finite carrier has a unique real stationary branch.

## Non-Descending Object

The virtual free-energy symbol does not descend to a finite-k Branch C
evaluator.  It targets `gamma_infty`, an asymptotic coefficient only
approximated in the cascade by finite-k fits.

## SAU Boundary

This construction does not axiomatize the H6 bridge.  It supplies only a
target-local asymptotic free-energy calibration for the Branch C `gamma`
coefficient.  The coefficients in `theta(T,d)` remain inherited from the
step 324 empirical fit, so this is not a theorem-grade derivation of
`gamma_infty`.
