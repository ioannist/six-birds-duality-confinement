# Step 406 Results Summary

## Alpha Threshold

Using `T ~= 1100`,

```text
Delta_bar = 2*pi/log(1100/(2*pi)) = 1.216448443708
alpha_0 = 1/Delta_bar = 0.822065264648.
```

## GUE/PCC Integral

```text
P_GUE(alpha < 0.822)
 = integral_0^0.822 [1-(sin(pi alpha)/(pi alpha))^2] d alpha
 = 0.373008424797.
```

Empirical Step395 close-pair fraction:

```text
243/401 = 0.605985037406.
```

## Failure Sub-Fraction

Empirical foreclosure failure among close pairs:

```text
38/243 = 0.156378600823.
```

Equivalent PCC alpha threshold for that sub-fraction:

```text
alpha_crit = 0.391273093837.
```

For the prompt's `0.257` ratio, the corresponding threshold is

```text
alpha_crit = 0.469661478708.
```

## Verdict

Mismatch.  The literal Montgomery PCC integral underpredicts the cascade's
close-pair frequency.  The foreclosure-failure subrate is therefore not
structurally explained by this PCC calculation alone.  Also, PCC is not the
nearest-neighbor spacing distribution, so this is a sanity check rather than a
decisive GUE spacing test.

No RH claim is made.
