# Step 411 Cross-L Hadamard Universality

## Inherited Statements Cited

- Step 381: `L''(rho) = 2L'(rho)*g'(rho)` with close-pair contribution `g'_near = +/- i/s_min`.
- Step 389: for `L(s, chi_3)`, `48/50 have Re L''(rho, chi_3) < 0` and the empirical exceptions are `j = 39, 48`.

## Explicit L-function Used

For the primitive real character modulo `3`,

```text
L(s, chi_3) = 3^(-s) * (zeta(s, 1/3) - zeta(s, 2/3)).
```

The Step 389 zero list was reused. `L'(rho_j)` was recomputed by `mpmath.diff` at dps `60`.

## Predictor

For nearest neighbor `rho_n = rho_j +/- i s_min`,

```text
g'_near = -1/(rho_n - rho_j).
```

Thus:

```text
rho_n above rho_j: g'_near = +i/s_min
rho_n below rho_j: g'_near = -i/s_min
```

Close-pair-only predicted contribution:

```text
L''_near(rho_j) = 2 * L'(rho_j) * g'_near.
```

The predicted sign is `sgn(Re L''_near)`.

## Exceptional Zeros

| j | T | nearest direction | s_min | Re L''_near | actual Re L'' | match |
|---:|---:|---|---:|---:|---:|---|
| 39 | 88.6526172085394 | above | 0.993785548302 | 5.115884816690 | 0.169721396257 | yes |
| 48 | 102.116361845065 | below | 0.741398377165 | 6.866519573249 | 5.624324264578 | yes |

## Match Counts

```text
exceptions matched: 2/2
non-exceptional negatives matched: 10/48
overall sign match: 12/50
predicted positive count: 40/50
```

## Interpretation

The close-pair Hadamard term correctly flags both empirical `chi_3` exceptions. However, it heavily over-predicts positive `Re L''` across the baseline: 40 of 50 zeros are predicted positive while only 2 are actually positive.

This supports partial cross-L universality of the exception mechanism, but not a complete sign classifier. For `L(s, chi_3)`, the regular Hadamard remainder and conductor/archimedean terms are essential for baseline sign suppression.
