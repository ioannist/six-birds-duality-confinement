# Step 419 R_char_embed Rule

## Formal Rule

`R_char_embed` replaces the Step 416 character-column magnitude search with an intrinsic conductor-aware rule:

```text
log_mag_hat(rho_j, k, q) = alpha * log(q*T_j/(2*pi)) + beta * log(k) + gamma
```

The rule is evaluated without any character-specific indicator column. This directly targets C11: magnitude must have an intrinsic character-embedding rule.

## Observable Used

The common magnitude observable available across the 7-character in-sample set and Step 418 OOS rows is `|L''(rho)|`, so this test uses `k=2`. Because `k` is fixed in the common table, `beta` is structurally declared but not identifiable here; it is fixed to `0.0` and must be re-estimated when a multi-k OOS table exists.

## Calibrated Parameters

```text
alpha = 0.654846816717966
beta  = 0.000000000000000
gamma = 0.044533487621859
```

## Verbatim Step Anchors

- Step 414: "Hadamard close-pair 22/22 = 100% across 7 L-functions."
- Step 416: "lambda=3 regularized transfer search, log-RMSE training 0.066, hold-out 0.039."
- Step 417: "joint (mag, phase) Stage III passes ... phase mismatch 0."
- Step 418: "magnitude blocked by character-specific feature columns."
