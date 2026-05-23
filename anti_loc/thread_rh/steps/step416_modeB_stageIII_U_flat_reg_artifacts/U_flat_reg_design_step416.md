# Step 416 U_flat_reg Operational Signature

## Grammar

`G_U_flat_reg`, declared at Step 416, extends `G_U_flat` by adding carrier-internal regularized transfer search.

## State Set

```text
Sigma = {a, b, c, d, e}
```

Same state roles as Step 356:

```text
a: Hecke evaluator atom
b: zeta residual atom
c: comparison atom
d: audit atom
e: blocked defect witness
```

## Lens

The base lens `q` is inherited from `G_U_flat`.

The regularized lens `q_reg` emits:

```text
(training_error, holdout_error, holdout_to_training_ratio, parameter_norm, crossval_status)
```

## Rewrite Rules

Inherited:

```text
R_H_load
R_Z_load
R_compare
R_operator_audit
R_block
R_admit
```

New:

```text
R_regularize(theta, lambda): adds lambda*||theta||^2 to the search audit.
R_crossval(theta): accepts only when train_log_RMSE < 0.5 and holdout/train <= 1.3.
```

`R_crossval` is carrier-internal: a candidate cannot reach `d[pass]` unless the split validation gate passes.

## No-Smuggling Boundary

The carrier does not contain Langlands functoriality, trace formula, kernel preservation, or a primitive transfer theorem. The attempt is a finite log-magnitude residual search over inherited Hecke and zeta evaluator tables.
