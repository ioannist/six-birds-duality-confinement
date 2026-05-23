# Step 427 Mechanism 2 Structural Signature

Mechanism 1 from Step 422 was close-pair dominance:

```text
B > 0 and |B| > |A|.
```

The three Step 426 mismatches show a second positive-sign mechanism:

```text
B > 0, A > 0, |A| > |B|, and A+B > 0.
```

Equivalently, `g'_near` still contributes with the positive sign, but the regular Hadamard remainder is phase-aligned with `zeta'(rho)` strongly enough to dominate the near term rather than oppose it.

A practical predictor before computing `Re zeta''` is partial, not theorem-grade:

```text
if nearest-neighbor B is positive and a truncated-window estimate of 2 Re[zeta'(rho) g'_rest_window(rho)] is positive with magnitude comparable to B, flag mechanism 2.
```

This is only diagnostic because the truncated rest differs materially from the exact residual; a theorem-grade predictor still requires a phase-sensitive regular-remainder estimate.
