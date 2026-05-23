# Step 406: PCC/GUE Cross-Check

## Inputs Used

- Step 195 inherited structural context: Branch/foreclosure diagnostics remain cascade-local empirical tests.
- Step 395 used verbatim from the prompt: `243 close-pair zeros`, `38/243 = 15.6% fail foreclosure at k=5`.
- Step 405 used verbatim in substance: Branch C and BN share zero-density structure but require careful distinction between density-level and observable-level claims.

## Normalization

The prompt approximates the j-range `[400,800]` by mean height `T ~= 1100`.
Then

```text
Delta_bar(T) = 2*pi/log(T/(2*pi)) = 1.216448443708...
```

The close-pair cutoff `s_min < 1.0` corresponds to

```text
alpha_0 = 1/Delta_bar = 0.822065264648.
```

## Montgomery PCC Integral

Using the requested density

```text
R_2(alpha)=1-(sin(pi*alpha)/(pi*alpha))^2,
```

the literal integral gives

```text
Integral_0^0.822 R_2(alpha)dalpha = 0.373008424797.
```

The empirical close-pair fraction from Step395 is

```text
243/401 = 0.605985037406.
```

So the literal PCC integral underpredicts the cascade close-pair criterion by
about `0.233` absolute.

## Foreclosure Failure Sub-Fraction

The exact foreclosure failure fraction among close pairs is

```text
38/243 = 0.156378600823.
```

Solving

```text
P_GUE(alpha < alpha_crit)/P_GUE(alpha < 0.822) = 38/243
```

gives

```text
alpha_crit = 0.391273093837.
```

The prompt also mentions `15.6%/60.6% = 25.7%`; this mixes denominators if
`15.6%` is already the within-close-pair failure rate.  For completeness,
using ratio `0.257` gives

```text
alpha_crit = 0.469661478708.
```

## Caveat

Montgomery pair correlation is not the nearest-neighbor spacing distribution.
The cascade's `s_min` statistic is a nearest-neighbor-style observable.  The
literal integral requested here is therefore a structural sanity check, not a
definitive GUE nearest-spacing test.

## Verdict

Mismatch under the requested PCC integral.  The cascade's `s_min<1.0` frequency
`0.606` is not reproduced by the literal `R_2` integral value `0.373`.
Consequently, the `15.6%` foreclosure-failure subrate should not be promoted to
a Montgomery-PCC structural explanation from this calculation alone.
