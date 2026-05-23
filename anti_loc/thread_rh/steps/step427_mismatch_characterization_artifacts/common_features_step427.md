# Step 427 Common Features

## Per-zero features

- j=705: T=1067.990000, s_min=0.571140, nearest=below, |zeta'|=3.503196, arg(zeta')=2.0832, arch=-17.561170, rest=29.043280, B=10.692042
- j=871: T=1267.570572, s_min=0.370226, nearest=below, |zeta'|=2.357500, arg(zeta')=2.3067, arch=-14.772625, rest=25.142192, B=9.439615
- j=965: T=1379.683283, s_min=0.465295, nearest=above, |zeta'|=3.042091, arg(zeta')=-2.2825, arch=-11.636095, rest=24.925409, B=9.901510

## Shared pattern

All three mismatches are high-index zeta zeros in the n=1000 extension (`j=705,871,965`). Each has a compressed nearest-neighbor spacing, so the close-pair contribution `B` is positive and large, but not larger than the exact regular contribution `A`. Unlike the Step 422 close-pair-dominance cells, these have a positive regular residual contribution that assists the sign flip.

The Archimedean term is negative in all three cases. The positive sign is not Archimedean-driven; it comes from the far-zero regular residual plus the close-pair term.

The common structural feature is therefore:

```text
B > 0, A > 0, |A| > |B|, and A+B > 0.
```

This is a second mechanism: regular-residual-assisted sign flip.
