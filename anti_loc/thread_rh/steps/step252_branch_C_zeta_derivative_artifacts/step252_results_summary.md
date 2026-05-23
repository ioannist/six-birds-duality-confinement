# Step 252 Results Summary

## Target

Investigate whether the Branch C foreclosure values
`|L_{rho,k}(G)|` for k=0..4 have a simple analytical relation to
`zeta^{(k)}(rho)` or `xi^{(k)}(rho)`.

The Branch C data were read from step 250, which consolidated steps
196/247/249/250.

## Derivatives at rho1

For `rho1 = 1/2 + 14.134725141734693... i`:

| k | `|zeta^{(k)}(rho1)|` | `|xi^{(k)}(rho1)|` |
|---:|---:|---:|
| 0 | `5.28444e-81` | `9.21239e-84` |
| 1 | `0.793160433357` | `0.00138271908922` |
| 2 | `0.655972498139` | `0.00160293252834` |
| 3 | `0.569370575252` | `0.00111290451070` |
| 4 | `0.520289648618` | `0.000474784799997` |

`k=0` is numerically zero, as expected at a zeta zero.

## Comparison to Branch C L-values

For `rho1_G_star`, the ratios over k=1..4 are:

- `|L_k| / |zeta^{(k)}(rho1)|`: `0.365, 0.874, 1.961, 4.233`
- `|L_k| / |xi^{(k)}(rho1)|`: `209, 358, 1003, 4638`
- `|L_k| / (k! |zeta^{(k)}(rho1)|)`: `0.365, 0.437, 0.327, 0.176`
- `|L_k| / (k! |xi^{(k)}(rho1)|)`: `209, 179, 167, 193`

For `rho1_G_prime` and `rho2_G_star`, the same candidate ratios also vary
substantially and do not stabilize to a constant.

## Growth-Rate Check

Step 250 exponential growth parameters:

- `rho1_G_star`: `b = 0.675150127456`
- `rho1_G_prime`: `b = 0.611315044773`
- `rho2_G_star`: `b = 0.770481777167`

Derivative successive log ratios do not match these values uniformly:

- rho1 zeta derivative mean log ratio k=1..4: `-0.1405`
- rho1 xi derivative mean log ratio k=1..4: `-0.3563`
- rho2 zeta derivative mean log ratio k=1..4: `0.2064`
- rho2 xi derivative mean log ratio k=1..4: `-0.1793`

## Verdict

`V_branch_C_zeta_derivative_no_simple_connection`.

No simple scalar relationship of the form
`|L_k| = const * |zeta^{(k)}(rho)|`, `const * |xi^{(k)}(rho)|`, or the
factorial-normalized variants was identified.  The Branch C values remain
projection- and test-function-dependent.
