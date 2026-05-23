# Step 409 Derivation Chain

## Inherited Statements Cited

- Step 366-372: "γ_ζ ≈ π/(T·log(T/(2π)))" is the Branch C structural law.
- Step 371: the heuristic mechanism is Riemann-von-Mangoldt density / half-spacing.
- Step 407: the cascade close-pair density matches the Wigner-Dyson nearest-neighbor prediction within 0.96% after using the two-sided `s_min` correction.

## Wigner-Dyson β=2 NN Density

Use

```text
p(s) = (32/pi^2) s^2 exp(-4 s^2/pi),  s >= 0.
```

The normalization and first moment are:

```text
∫_0^∞ p(s) ds = 1,
<s> = ∫_0^∞ s p(s) ds
    = (32/pi^2) ∫_0^∞ s^3 exp(-(4/pi)s^2) ds
    = (32/pi^2) * 1/(2*(4/pi)^2)
    = 1.
```

Thus the Wigner-Dyson β=2 nearest-neighbor law is normalized to unit mean local spacing.

## Riemann-von-Mangoldt Scaling

The local zero density at height `T` is

```text
n(T) = log(T/(2*pi))/(2*pi).
```

The mean physical nearest-neighbor spacing is therefore

```text
Delta_bar(T) = 1/n(T) = 2*pi/log(T/(2*pi)).
```

Because `<s> = 1`, the expected GUE physical spacing is exactly `Delta_bar(T)`. The half-spacing saddle scale used in the Step 371 mechanism is

```text
Delta_bar(T)/2 = pi/log(T/(2*pi)).
```

Dividing by the height scale `T` gives

```text
gamma_zeta_GUE(T) = <s> * pi/(T*log(T/(2*pi)))
                  = pi/(T*log(T/(2*pi))).
```

## Numerical T1 Comparison

At `T1 = 14.1347251417347`,

```text
gamma_zeta_GUE(T1) = 0.274139452528282289424404915499.
```

This is `37.07%` above the prompt comparison value `0.20` and `33.99%` above the inherited Step 324 first-zero value `0.2046`. This mismatch is not a failure of the RMT derivation of the smooth law; it indicates that the per-zero raw value still carries finite-height, test-function, and residual corrections not represented by the unit-mean NN spacing argument.

## Outcome

The GUE NN derivation reproduces the same constant as the Riemann-von-Mangoldt half-spacing derivation because the Wigner-Dyson β=2 distribution has expected normalized spacing exactly `1`. It does not provide a new prefactor beyond the mean-spacing law.
