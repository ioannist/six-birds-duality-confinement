# Step 429 L-prime Phase Constraint

The functional equation yields, for self-dual real characters,

```text
Arg L'(rho,chi) = -Arg(i F_chi(rho)) (mod pi).
```

Consequently, if the nearest zero is above `rho`, then

```text
g_near = -1/(rho_near-rho) = i/s_min,
B = 2 Re[L'(rho) g_near] = -2 Im L'(rho)/s_min.
```

If the nearest zero is below `rho`, then

```text
g_near = -i/s_min,
B = 2 Im L'(rho)/s_min.
```

Thus `B>0` is equivalent to the empirical phase statement:

```text
sign Im L'(rho) opposes the nearest-neighbor direction.
```

The functional equation explains why `L'(rho)` lies on a computable phase line, but it does not by itself force the sign of `Im L'(rho)` relative to the nearest-neighbor direction. That sign also depends on the zero-crossing orientation of the Hardy-normalized function.

For zeta, the numerical check in `numerical_verification_step429.csv` verifies the phase-line identity at `rho_1`, `rho_2`, `rho_5`, and exceptional `rho_34` to high precision.
