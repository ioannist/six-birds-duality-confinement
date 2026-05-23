# Step 416 Results Summary

## G_U_flat_reg Features

`G_U_flat_reg` adds:

```text
R_regularize
R_crossval
```

to the Step 356 `U_flat` state grammar. Cross-validation is carrier-internal, not post-hoc.

## SAU

Six SAU gates: `6/6 pass`.

## Transfer Search

Best passing setting:

```text
lambda = 3
training_log_RMSE = 0.06638935814747417
holdout_log_RMSE = 0.03872616304405194
holdout/train = 0.583318834895609
```

C5 and C6 both pass.

## Verdict

Constraint-driven Stage III succeeds on the scoped regularized log-magnitude residual. `U_flat_reg` becomes the active Mode B carrier for this residual class.

No RH or full H6 bridge closure is claimed: the operator certificate component remains unresolved.
