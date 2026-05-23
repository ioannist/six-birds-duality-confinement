# Step 220 Results Summary

## Target

Jointly scan the wavepacket essential-norm diagnostic

`Phi(sigma, ell) = lim_T ||C_ell u_T||`

to estimate `Phi_max` over the requested `(sigma, ell)` grid.

## Coarse Scan

Grid:

- `sigma in {0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,1.0,1.5}`.
- `ell in {0.3,0.5,0.7,log2,1.0,log3,1.5,pi/2,2.0,2.5}`.
- `T=10000`, PSWF terms `24`, mpmath dps `80`.

Coarse maximum:

- `sigma = 0.4`
- `ell = 2.0`
- `Phi = 0.4898488467749268`

Top coarse cells were all near `ell=2.0` and `sigma=0.3..0.5`.

## Refined Scan

Refinement: 5x5 grid with step `0.05` around the coarse maximum.

Refined maximum:

- `sigma_max = 0.35`
- `ell_max = 2.0`
- `Phi_max = 0.49047661902424095`
- conservative lower after `7.5e-2` error: `0.41547661902424093`

The maximum is well below the operator-theoretic upper bound `1`.

## Robustness

At `(sigma, ell) = (0.35, 2.0)`:

- `T=1000`, PSWF 24: `0.49047662995845176`
- `T=5000`, PSWF 24: `0.49047662002982523`
- `T=10000`, PSWF 24: `0.4904766190242409`
- PSWF 48 matched PSWF 24 at displayed precision.
- dps 100 matched dps 80 at displayed precision.

## Verdict

`V_phi_max_bounded_below_one`.

The joint scan pins the wavepacket-family essential norm near `0.49`, not near the maximal value `1`.
