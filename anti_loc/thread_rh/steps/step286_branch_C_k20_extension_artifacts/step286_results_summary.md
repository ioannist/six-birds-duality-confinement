# Step 286 Results Summary

## Target

Extend Branch C from k=0..7 to k=10, 15, 20 for the three step-269 triples:

- `(rho_1, G_star)`
- `(rho_2, G_star)`
- `(rho_1, G_prime)`

## Computation Attempt

The full Step 269 projected-value pipeline was attempted at mpmath dps=120. It did not complete in a practical time for k=10/15/20. The step is therefore classified as partial.

To preserve a useful diagnostic artifact, the script records:

- inherited certified k=0..7 values from step 269,
- a k=0..7 polynomial-corrected exponential refit,
- extrapolative k=10/15/20 model-probe values clearly marked as not certified.

These high-k rows are not claimed as computed Branch C matrix elements.

## Model-Probe High-k Values

| Triple | k=10 | k=15 | k=20 |
|---|---:|---:|---:|
| `rho1_G_star` | `1.546626491800e+02` | `5.868364203819e+03` | `2.296294436309e+05` |
| `rho2_G_star` | `7.061235559599e+02` | `1.042279167097e+05` | `1.726965455230e+07` |
| `rho1_G_prime` | `1.078157068858e+02` | `2.564809878163e+03` | `6.187798421033e+04` |

## k=0..7 Fit Parameters Used

| Triple | a | b | c | RMSE k=0..7 |
|---|---:|---:|---:|---:|
| `rho1_G_star` | `1.760967365413e-01` | `7.496826447846e-01` | `-2.997872227402e-01` | `1.653179838490e-02` |
| `rho2_G_star` | `2.069855044354e-01` | `1.083197828957e+00` | `-1.124770366118e+00` | `2.112656584263e-02` |
| `rho1_G_prime` | `2.387370630283e-01` | `6.440994502963e-01` | `-1.368611329762e-01` | `1.541070565893e-02` |

## Verdict

`V_branch_C_k20_partial`

The requested certified high-k computation remains precision/time-limited. The extrapolation is useful for scale expectations, but it does not establish persistence or transition of the actual Branch C sequence.
