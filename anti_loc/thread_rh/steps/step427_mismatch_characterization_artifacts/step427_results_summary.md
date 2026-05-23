# Step 427 Results Summary

## Decomposition Results

- j=705: T=1067.990000, s_min=0.571140, nearest=below, |zeta'|=3.503196, arg(zeta')=2.0832, arch=-17.561170, rest=29.043280, B=10.692042
- j=871: T=1267.570572, s_min=0.370226, nearest=below, |zeta'|=2.357500, arg(zeta')=2.3067, arch=-14.772625, rest=25.142192, B=9.439615
- j=965: T=1379.683283, s_min=0.465295, nearest=above, |zeta'|=3.042091, arg(zeta')=-2.2825, arch=-11.636095, rest=24.925409, B=9.901510

## Dominant terms

For all three zeros, the positive sign is regular-residual-assisted: the Archimedean contribution is negative, the close-pair contribution is positive, and the exact far-zero residual contribution is positive and large enough that `A > B`.

## Verdict

Common structural feature identified. The Step 422 candidate theorem refines from one mechanism to two:

```text
Mechanism 1: B > 0 and |B| > |A|.
Mechanism 2: B > 0, A > 0, |A| > |B|, and A+B > 0.
```

The mechanism-2 predictor is partial because the truncated `g'_rest` window is diagnostic but does not exactly reproduce the full regular residual.
