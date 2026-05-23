# Step 409 Results Summary

## Result

The Wigner-Dyson β=2 nearest-neighbor density

```text
p(s) = (32/pi^2) s^2 exp(-4s^2/pi)
```

has

```text
∫ p(s) ds = 1
∫ s p(s) ds = 1.
```

Therefore the GUE NN expected physical spacing is exactly the Riemann-von-Mangoldt mean spacing:

```text
<spacing> = 2*pi/log(T/(2*pi)).
```

Using the Step 371 half-spacing mechanism:

```text
gamma_zeta_GUE(T) = (<s>/2)*(2*pi/log(T/(2*pi)))/T
                  = pi/(T*log(T/(2*pi))).
```

## T1 Numerical Comparison

For `T1 = 14.1347251417347`,

```text
gamma_zeta_GUE(T1) = 0.274139452528282289424404915499.
```

Compared to the prompt's empirical `0.20`, this is `37.07%` high. Compared to the Step 324 inherited `0.2046`, it is `33.99%` high.

## Verdict

RMT-natural at the smooth-law level. The GUE NN calculation does not change the prefactor because `<s>=1`; it validates the use of the Riemann-von-Mangoldt mean spacing as the RMT-normalized unit-spacing scale. It does not by itself explain finite-height per-zero deviations from the empirical raw values.
