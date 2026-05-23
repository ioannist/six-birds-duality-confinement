# Step 417 U_flat_reg Phase Extension Design

## Inherited Statements Cited

- Step 381: `g'_near(rho_j) = -1/(rho_nearest - rho_j)`.
- Step 411: `L(s, chi_3)` phase exception detection matched `2/2`.
- Step 414: new characters `chi_7`, `chi_8`, `chi_11` matched `9/9`, giving corrected aggregate `22/22`.
- Step 416: `U_flat_reg` magnitude residual passed with `lambda=3`, train `0.06638935814747417`, holdout `0.03872616304405194`.

## Extension

`G_U_flat_reg` is extended with one phase rule:

```text
R_phase_hadamard
```

The state set remains:

```text
Sigma = {a,b,c,d,e}
```

`R_phase_hadamard` attaches a phase-sign ledger to the comparison state `c`:

```text
c[mag_residual] -> c[mag_residual, phase_sign_prediction]
```

The rule does not introduce a transfer primitive, a kernel-preservation axiom, or an operator certificate.

## Joint Residual

The joint residual is:

```text
R_joint = (R_mag_log, R_phase_sign)
```

with norm:

```text
sqrt(R_mag_log^2 + R_phase_sign^2).
```

Since the inherited phase exception detector has zero mismatch on the tested exceptional set, the joint errors equal the Step 416 magnitude errors.

## Operator Boundary

The operator component is not addressed. It remains `C10_operator_certificate_open`.
