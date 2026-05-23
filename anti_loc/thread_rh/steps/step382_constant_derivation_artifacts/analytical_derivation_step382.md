# Step 382 Analytical Constant Derivation Attempt

Step 381 gave the empirical close-pair correction

`R_j ~= -4.472883537971084 + 10.17670932369573/s_min`.

The Hadamard local identity is

`zeta''(rho_j)=2 zeta'(rho_j) g'_j(rho_j)`,

with

`g'_j(rho_j)=arch(rho_j)+sum_(rho != rho_j)[-1/(rho-rho_j)+1/rho]`.

For a nearest neighbor `rho_n=rho_j +/- i s_min`,

`g'_near = -1/(rho_n-rho_j)= +/- i/s_min`.

The Branch C saddle action has the smooth height law

`gamma(T) ~= pi/(T log(T/(2pi)))`.

The close-pair perturbation enters through `Re g_j(z*)` at the large-k saddle `z*=rho_j+delta z`. Since `g'_near` is purely imaginary, the first-order perturbation is

`Delta S_near ~= Re(g'_near delta z) ~= C_sad/s_min`.

The fitted slope therefore measures the effective saddle displacement constant `C_sad`. The natural closed-form candidate is `pi^2`: one `pi` from the cusp angular displacement and one `pi` from the zero-density normalization in the Branch C height law.

Numerically:

- empirical slope: `10.176709323695727`
- `pi^2`: `9.8696044010893586188`
- relative error: `0.0301772324273129153794689619087`

The fitted offset is the regular Hadamard remainder plus the smooth Archimedean subtraction. The simplest structural candidate is `-3pi/2`.

- empirical offset: `-4.472883537971084`
- `-3pi/2`: `-4.7123889803846898577`
- relative error: `0.0535460940085746977810798124296`

Important limitation: this identifies plausible constants and their Hadamard/saddle origin, but the exact saddle displacement `delta z` for the projected Burnol/Sonine matrix element is not derived here. Therefore this is not theorem-grade.
