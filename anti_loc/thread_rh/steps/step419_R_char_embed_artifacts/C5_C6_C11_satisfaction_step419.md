# Step 419 C5/C6/C11 Satisfaction

## Results

- Embedding train log-RMSE: `0.299435674236`.
- Embedding hold-out log-RMSE: `0.300035396793`.
- Hold-out/train ratio: `1.002002842709`.
- OOS chi_13+chi_15 log-RMSE: `0.344079336786`.

## Constraint Status

- C5: PASS under the active threshold because `0.299436 < 0.5`.
- C6: PASS because hold-out/train ratio `1.002003 <= 1.3`.
- C11: PASS in the narrow embedding sense because OOS/train ratio `1.149093 <= 2` and no character-specific columns are used.
- Step-416 comparability: FAIL because OOS RMSE `0.344079` is `5.18x` the Step 416 train RMSE `0.066389`.
- C10: unchanged; operator-certificate residual remains open.

## Interpretation

`R_char_embed` fixes the mechanical OOS blockage from Step 418, but the simple conductor-height rule loses too much magnitude fidelity compared with the Step 416 lambda=3 character-column ridge model. The result is a partial C11 repair, not a full Stage III magnitude extension with comparable accuracy.
