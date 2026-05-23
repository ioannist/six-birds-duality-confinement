# Step 417 Results Summary

## Rule Added

```text
R_phase_hadamard:
phase_sign = sign(Re(2 * L'(rho_j) * (-1/(rho_nearest-rho_j)))).
```

## Joint Residual

Magnitude from Step 416:

```text
train = 0.06638935814747417
holdout = 0.03872616304405194
```

Phase mismatch:

```text
train = 0
holdout = 0
```

Joint:

```text
train = 0.06638935814747417
holdout = 0.03872616304405194
ratio = 0.583318834895609
```

## SAU

`6/6` gates pass.

## Verdict

Joint `(mag, phase)` Stage III passes for `U_flat_reg + R_phase_hadamard`.

Remaining residual:

```text
C10 operator-certificate-open
```

No full H6 closure is claimed.
