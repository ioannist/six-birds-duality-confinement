# Step 408: Joint (alpha, T) Failure Classifier

## Inputs Used

- Step 395 used verbatim in substance: close-pair dataset has `243` zeros and `38` foreclosure failures at `k=5`.
- Step 396 used verbatim in substance: `T` was the dominant individual predictor, but no single feature sufficed.
- Step 406 used verbatim in substance: Montgomery PCC was not the right spacing statistic.
- Step 407 used verbatim in substance: Wigner-Dyson NN matches close-pair density, but foreclosure failure is not explained by spacing alone.

## Feature Added

For each row in Step396:

```text
alpha_j = s_min(j) / Delta_bar(T_j),
Delta_bar(T) = 2*pi/log(T/(2*pi)).
```

## Scatter Structure

Failures are concentrated toward higher `T`, but not purely at the smallest
`alpha`.  In fact:

```text
fail alpha range: 0.1803 .. 0.8182
pass alpha range: 0.2363 .. 0.8230
```

so `alpha` alone cannot separate failures from passes inside the close-pair
set.

## Model Fits

### Combined score

```text
fail if T*(1-alpha) > 556.2692223790
```

Balanced accuracy:

```text
0.5935173299
```

AIC/BIC using two empirical leaf probabilities:

```text
AIC = 208.5960
BIC = 219.0752
```

### Linear log-odds

Fit form:

```text
logit(P(fail)) = a + b*T + c*alpha + d*T*alpha
```

Using standardized features and balanced logistic regression:

```text
intercept = -0.34364944
coefficients = [1.10553587, 0.24880003, -0.23418346]
best probability threshold = 0.5300164114
balanced accuracy = 0.7508344031
TPR = 0.7894736842
TNR = 0.7121951220
AIC = 290.9089
BIC = 304.8811
```

### Tree-style threshold

Best hard criterion:

```text
fail if T > 1048.953785194686 and alpha < 0.8230436348983109.
```

Balanced accuracy:

```text
0.7601412067
TPR = 0.7105263158
TNR = 0.8097560976
```

Leaf counts:

```text
predicted-fail region: 27 failures / 66 rows
predicted-pass region: 11 failures / 177 rows
```

AIC/BIC using two empirical leaf probabilities:

```text
AIC = 179.7248
BIC = 193.6970
```

## Verdict

No clean joint criterion at the requested `>=80%` balanced-accuracy level.

The best model is the tree-style high-`T` criterion with a weak alpha gate:
`T > 1048.95` and `alpha < 0.8230`, balanced accuracy `0.7601`.  Since
`alpha_crit` is near the upper edge of the close-pair set, the classifier is
mostly a high-`T` effect with spacing acting as a secondary qualifier.
