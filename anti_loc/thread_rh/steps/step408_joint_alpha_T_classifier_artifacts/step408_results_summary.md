# Step 408 Results Summary

## Joint Fit Form

Best hard classifier:

```text
fail if T > 1048.953785194686 and alpha < 0.8230436348983109.
```

where

```text
alpha = s_min / Delta_bar(T).
```

## Accuracy

Balanced accuracy:

```text
0.7601412067
```

Components:

```text
TPR = 0.7105263158
TNR = 0.8097560976
```

Leaf counts:

```text
predicted fail: 27/66 actual failures
predicted pass: 11/177 actual failures
```

## Model Comparison

- `T*(1-alpha)>C`: balanced accuracy `0.5935`.
- Logistic `a+bT+c alpha+dT alpha`: balanced accuracy `0.7508`.
- Tree-style `T>Tcrit AND alpha<acrit`: balanced accuracy `0.7601`, best AIC/BIC among fitted simple models.

## Verdict

No clean `>=80%` joint criterion.  Failures are structurally biased toward
high `T`, but alpha does not sharply separate them inside the close-pair set.
Best diagnosis: soft/high-T-dominated pattern, not a clean `(high T) AND
(extra close pair)` law.

No RH claim is made.
