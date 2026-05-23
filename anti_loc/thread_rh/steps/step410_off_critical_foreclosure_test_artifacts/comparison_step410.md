# Step 410 Comparison

## Inherited Statements Cited

- Step 196: foreclosure threshold `|L_k| >= 0.034`.
- Step 292: raw proxy identity `delta_Dk = (zeta*M(G_star))^(k)(rho)`.
- Step 380: on-critical baseline at `rho_1`, `k=5` is approximately `4.28`.
- Step 409: the Branch C structural discussion is smooth-height/RMT-natural, not a proof of RH.

## Method

The Step 292 evaluator is written for critical-line zeros through a height parameter `gamma`, but its raw identity is a product-rule formula:

```text
delta_Dk(s) = (zeta*M(G_star))^(k)(s)
            = sum_j binom(k,j) zeta^(j)(s) M(G_star)^(k-j)(s).
```

For this step the same identity and the same `G_star` Mellin bump coefficients were used, with the Mellin derivatives generalized from `s = 1/2+iT` to arbitrary `s = sigma+iT`.

No projected `I_k` or `R_k` corrections were applied, because the off-critical and nonzero test points do not have a Burnol/Sonine zero-spectral interpretation.

## Results

All four raw-proxy magnitudes are far above the foreclosure threshold:

```text
rho_actual       |delta_D5| = 4.276557470203644
rho_off_right    |delta_D5| = 2.847142289161922
rho_off_left     |delta_D5| = 6.430420423102830
on_line_not_zero |delta_D5| = 4.253088491394162
```

Ratios to the actual zero value:

```text
rho_off_right    0.6658
rho_off_left     1.5036
on_line_not_zero 0.9945
```

## Interpretation

The right off-critical point is smaller than the actual-zero value by about one third, while the left mirror is larger by about half. The nearby on-critical nonzero point is nearly unchanged.

Thus the raw proxy has some real-part sensitivity, but it does not produce a foreclosure violation and does not distinguish an actual zero from a nearby nonzero critical-line point at this `k=5`, `T≈14.13` test.

The result is heuristic only: `rho_off1` and `rho_off2` are not zeros of `zeta`, so the full spectral Branch C matrix element is not defined there as a genuine zero-carrier object.
