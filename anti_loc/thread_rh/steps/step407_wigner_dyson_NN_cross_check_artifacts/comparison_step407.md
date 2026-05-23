# Step 407: Wigner-Dyson Nearest-Neighbor Cross-Check

## Inputs Used

- Step 195 inherited context: foreclosure diagnostics remain cascade-local empirical tests.
- Step 395 used verbatim from the prompt: `243/401 = 60.6%` close-pair rate and `38/243 = 15.6%` foreclosure failure among close pairs.
- Step 405 used verbatim in substance: zero-density factors require observable-specific interpretation.
- Step 406 used verbatim in substance: Montgomery PCC was not the nearest-neighbor spacing distribution.

## Wigner-Dyson GUE Density

The requested beta=2 Wigner-Dyson nearest-neighbor density is

```text
p(s) = (32/pi^2) * s^2 * exp(-4s^2/pi).
```

For the cascade threshold

```text
alpha_0 = 0.822065264648,
```

the single-gap CDF is

```text
F(alpha_0) = 0.367700147594.
```

## Correcting for the Cascade Statistic s_min

Step395 uses

```text
s_min(j) = min(T_j - T_{j-1}, T_{j+1} - T_j).
```

So the correct per-zero comparison is not the single adjacent-gap CDF, but the
two-sided nearest-neighbor probability.  Under the local approximation that the
left and right neighboring normalized gaps have the same Wigner CDF and are
weakly independent,

```text
P(s_min < alpha) ~= 1 - (1 - F(alpha))^2.
```

At `alpha=0.822065264648`,

```text
P_GUE,smin = 0.600196896648.
```

Empirical Step395:

```text
243/401 = 0.605985037406.
```

Relative difference:

```text
0.955%.
```

## Foreclosure Failure Sub-Rate

For the prompt-requested `25.7%` sub-rate:

```text
alpha_fail single-gap = 0.468992018520.
alpha_fail s_min two-sided = 0.441586862892.
```

Using the exact Step395 within-close-pair failure rate `38/243` instead gives

```text
alpha_fail s_min two-sided = 0.366556261126.
```

## Verdict

After matching the statistic correctly (`s_min`, not one adjacent spacing), the
cascade close-pair density is consistent with Wigner-Dyson/GUE nearest-neighbor
statistics to about `1%` in this j-range.  This supports a Montgomery-Odlyzko
style RMT explanation for close-pair density.  It does not by itself explain
which close pairs fail foreclosure; that remains an extra observable layered on
top of the spacing statistic.
