# Step 381 Hadamard Close-Pair Derivation

For a simple zero `rho_j`, write

`zeta(s) = (s-rho_j) exp(g_j(s))`.

Then

`zeta'(rho_j) = exp(g_j(rho_j))`

and

`zeta''(rho_j) = 2 zeta'(rho_j) g'_j(rho_j)`.

From the completed Hadamard product

`xi(s)=e^(A+Bs) prod_rho (1-s/rho)e^(s/rho)`,

the regular logarithmic derivative at `rho_j` is

`g'_j(rho_j) = arch(rho_j) + sum_(rho != rho_j) [-1/(rho-rho_j) + 1/rho]`,

where `arch` contains the elementary, Gamma, and exponential factors. For a nearest neighbor `rho_n = rho_j +/- i s_min`, the singular local term is

`g'_near = -1/(rho_n-rho_j) = +/- i/s_min`.

Therefore the close-pair contribution to the real part is

`Re zeta''_near(rho_j) = Re(2 zeta'(rho_j) g'_near)`,

so a compressed pair can flip the sign through the phase of `zeta'(rho_j)`. This term is not a full sign theorem by itself because the regular Hadamard remainder can dominate, but it is the local amplification term.

Numerical results over the 22 tested zeros:

- direct Hadamard identity sign match: `22/22`
- close-pair-only sign match: `8/22`
- close-pair-only sign match on exceptions: `7/7`
- close-pair-only sign match on baseline: `1/15`
- `corr(R_j, 1/s_min) = 0.723724`
- `corr(R_j, Re close-pair contribution) = 0.503439`

Interpretation: the identity is exact; the non-tautological close-pair term identifies all seven sign-flip exceptions but overpredicts positives in the low-index baseline. The Branch C residual has a strong `1/s_min` correlation above the requested `0.7` threshold.
