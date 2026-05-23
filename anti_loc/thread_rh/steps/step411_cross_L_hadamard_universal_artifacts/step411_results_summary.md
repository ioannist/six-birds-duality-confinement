# Step 411 Results Summary

## Result

The `chi_3` Hadamard close-pair-only predictor was computed for the 50 zeros from Step 389 using

```text
L(s, chi_3) = 3^(-s) * (zeta(s, 1/3) - zeta(s, 2/3)).
```

At each zero,

```text
L''_near(rho_j) = 2 L'(rho_j) g'_near,
g'_near = -1/(rho_nearest - rho_j).
```

## Match Counts

```text
exceptional zeros j=39,48 matched: 2/2
non-exceptional negatives matched: 10/48
overall sign match: 12/50
predicted positive signs: 40/50
```

## Verdict

Partial universality. The Hadamard close-pair term analytically identifies both `L(s, chi_3)` exceptional zeros, matching the ζ-side mechanism at the exception-detection level. It is not a complete sign model for the full `chi_3` baseline because it over-predicts positive signs; the regular Hadamard remainder and conductor-specific factors remain necessary.
