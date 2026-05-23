# Step 416 Constraint Engineering Audit

## Active Basis

The active constraints are:

```text
C1, C2, C4, C5, C6, C8
```

## C5 Underfit

Gate:

```text
training_log_RMSE < 0.5
```

Best passing setting:

```text
lambda = 3
training_log_RMSE = 0.06638935814747417
```

Status: C5 satisfied.

## C6 Overfit

Gate:

```text
holdout_log_RMSE / training_log_RMSE <= 1.3
```

Best passing setting:

```text
holdout_log_RMSE = 0.03872616304405194
ratio = 0.583318834895609
```

Status: C6 satisfied.

## Why This Is Not Post-Hoc

In `G_U_flat`, fits were accepted or rejected after the search. In `G_U_flat_reg`, `R_crossval` is a rewrite/audit rule. A candidate with good training but failed holdout cannot descend to `d[pass]`.

Example blocked settings:

```text
lambda = 0: train = 0.000473, holdout = 0.007885, ratio = 16.66 -> blocked by C6.
lambda = 300: train = 1.10667 -> blocked by C5.
```

Thus accepted underfit/overfit is structurally impossible inside the carrier gate. The attempt still does not solve H6 because the operator certificate remains outside this log-magnitude residual.

## C8 Framing Variation

This is not a state-count or surface-framing variation. The admissible-expression set changes: without `R_crossval`, overfit settings descend; with `R_crossval`, they block.
