# Step 422 Dominance Condition

Define the Hadamard logarithmic derivative split at a simple zero `rho`:

```text
g'(rho) = arch(rho) + g'_near(rho) + g'_rest(rho),
g'_near(rho) = -1/(rho_nearest-rho).
```

Then

```text
L''(rho) = 2 L'(rho) g'(rho),
Re L''(rho) = A(rho) + B(rho),
A(rho) = 2 Re[L'(rho) * (arch(rho)+g'_rest(rho))],
B(rho) = 2 Re[L'(rho) * g'_near(rho)].
```

Candidate dominance condition:

```text
Re L''(rho) >= 0 iff B(rho) > 0 and |B(rho)| > |A(rho)|.
```

For this audit, `B` is read from the cascade's close-pair Hadamard contribution columns. `A` is computed as the exact residual `Re L'' - B`, so it includes Archimedean plus far-zero regular remainder.

## Verbatim Step Anchors

- Step 381: `L''(rho) = 2L'(rho)*g'(rho)` with close-pair contribution.
- Step 411: `L(s, chi_3)` close-pair term identified `2/2` exceptional zeros.
- Step 412: `L(s, chi_4)` and `L(s, chi_5)` were added.
- Step 414: `Hadamard close-pair 22/22 = 100% across 7 L-functions.`
- Step 418: `phase generalizes universally OOS`.
