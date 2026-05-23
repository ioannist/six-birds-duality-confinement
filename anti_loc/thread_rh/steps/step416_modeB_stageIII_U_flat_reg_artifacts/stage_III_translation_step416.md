# Step 416 Stage III Translation

## Typed Residual

The H6 bridge target is translated into a `U_flat_reg` residual:

```text
R_reg(theta) = log Z_k - (beta0 + sum_chi a_chi log H_chi,k)
```

on the scoped inherited tables:

```text
Hecke: step320 characters chi_3, chi_4, chi_5a, chi_5b, k=1..10.
Zeta: step320 Branch C recomputed raw zeta values, k=1..10.
```

Training split:

```text
k = 1..8
```

Holdout split:

```text
k = 9,10
```

## Carrier-Internal Gate

The candidate descends to `d[pass]` only if:

```text
C5: training_log_RMSE < 0.5
C6: holdout_log_RMSE / training_log_RMSE <= 1.3
```

## Best Passing Setting

The best passing regularization setting was:

```text
lambda = 3
training_log_RMSE = 0.06638935814747417
holdout_log_RMSE = 0.03872616304405194
ratio = 0.583318834895609
```

This satisfies both C5 and C6 on the scoped log-magnitude residual.

## Boundary

This is not a proof of H6. It does not certify the operator component of the original `(mag, phase, operator)` bridge. It shows that the prior C5/C6 numerical failure shape is avoidable when regularization and cross-validation are part of the carrier grammar.
