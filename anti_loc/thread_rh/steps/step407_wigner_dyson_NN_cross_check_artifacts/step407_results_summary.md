# Step 407 Results Summary

## Single-Gap Wigner-Dyson CDF

For `alpha=0.822065264648`,

```text
P_NN(single gap < alpha) = 0.367700147594.
```

## s_min Correction

The cascade uses `s_min`, the minimum of the two adjacent gaps.  With the
standard two-sided approximation,

```text
P(s_min < alpha) = 1 - (1 - F(alpha))^2
                 = 0.600196896648.
```

Empirical Step395:

```text
243/401 = 0.605985037406.
```

Relative difference:

```text
0.955%.
```

## Foreclosure Sub-Rate

For the prompt's `25.7%` sub-rate:

```text
alpha_fail(single gap) = 0.468992018520
alpha_fail(s_min two-sided) = 0.441586862892
```

For the exact `38/243` within-close-pair rate:

```text
alpha_fail(s_min two-sided) = 0.366556261126.
```

## Verdict

Close-pair density matches GUE/Wigner-Dyson nearest-neighbor statistics once
the cascade's `s_min` statistic is compared to a two-sided nearest-neighbor
probability.  The foreclosure failure subrate is not explained by this alone.

No RH claim is made.
