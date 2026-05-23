# Step 418 Results Summary

## OOS Characters

Computed:

```text
chi_13: real primitive quadratic character mod 13.
chi_15: real primitive product character chi_3 * chi_5 mod 15.
```

Blocked:

```text
chi_16: no real primitive Dirichlet character of conductor 16 exists; real characters modulo 16 are imprimitive/lower-conductor lifts.
```

## Phase OOS

```text
chi_13: 3 exceptional zeros, 3/3 matched.
chi_15: 1 exceptional zero, 1/1 matched.
chi_16: blocked, no real primitive character.
```

OOS phase match on computable characters:

```text
4/4 = 100%.
```

## Magnitude OOS

The Step 416 `lambda=3` magnitude model is not OOS-character-ready. Its feature columns are explicitly tied to training characters:

```text
chi_3, chi_4, chi_5a, chi_5b.
```

No grammar-declared embedding maps an unseen character such as `chi_13` or `chi_15` into that feature vector. Therefore OOS magnitude log-RMSE is blocked, not numerically meaningful.

## Verdict

Mixed. The phase component generalizes on the computable OOS characters, but joint `(mag, phase)` OOS closure does not pass because the magnitude component lacks an unseen-character embedding and `chi_16` is unavailable under the required real-primitive constraint.
