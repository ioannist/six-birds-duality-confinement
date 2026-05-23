# Step 193 Results Summary

## Verdict

`V_BN_CRCFT_TE`.

The Beurling-Nyman carrier is a new CRE carrier, but it does not escape the Dichotomy.  The carrier is

`H_BN = L^2(0,1)`

with Müntz/fractional-part atoms

`rho_a(t) = {a/t} - a {1/t}`, `0 < a <= 1`,

and subspace

`M_BN = closure span {rho_a}`.

The residual is

`Xi_BN = (I - P_{M_BN}) 1`,

with scalar defect

`delta_BN^2 = ||Xi_BN||_2^2 = inf_{f in M_BN} ||1 - f||_2^2`.

By the Beurling-Nyman theorem, `Xi_BN = 0` is equivalent to RH.  Therefore the CRCFT mode is target-equivalence (`CRCFT-TE`).

## Gram Matrix Subinterface

For a finite parameter set `A = {a_1,...,a_N}`, define

`G_A(i,j) = <rho_{a_i}, rho_{a_j}>`,

`b_A(i) = <1, rho_{a_i}> = a_i log(1/a_i)`,

and

`delta_A^2 = 1 - b_A^* G_A^dagger b_A`.

The Gram entries are computable by explicit integrals, finite floor-function partitions, or known Báez-Duarte arithmetic formulas.  This is a useful computational subinterface, but it does not turn the carrier into CTMT-stuck: the matrix elements are not missing.  The hard problem is proving `delta_A -> 0` along an exhausting family, which is the RH-equivalent target.

## Dichotomy Update

BN adds a sixth CRE carrier instance and lands in `CRCFT-TE`.  It is substantively different in attack shape from Burnol/Sonine, but it remains a target-equivalence carrier.

