# Step 419 Results Summary

## Rule

`R_char_embed`: `log_mag_hat = alpha*log(qT/(2*pi)) + beta*log(k) + gamma`, with no character-specific columns.

## Calibration

- `alpha = 0.654846816717966`
- `beta = 0.000000000000000` (fixed; common OOS table has `k=2`)
- `gamma = 0.044533487621859`

## Verification

- In-sample train log-RMSE: `0.299435674236`
- In-sample hold-out log-RMSE: `0.300035396793`
- Hold-out/train ratio: `1.002002842709`
- OOS chi_13 log-RMSE: `0.354367058828`
- OOS chi_15 log-RMSE: `0.333474388257`
- OOS combined log-RMSE: `0.344079336786`

## Verdict

C5 and C6 pass under the active thresholds, and C11 passes in the narrow sense that the predictor extends to chi_13 and chi_15 without per-character columns. However, the error is about `5.18x` the Step 416 lambda=3 in-sample magnitude RMSE, so the rule does not provide magnitude generalization comparable to the prior in-sample closure. Verdict: partial R_char_embed repair; richer intrinsic embedding is still needed for full magnitude Stage III extension.
