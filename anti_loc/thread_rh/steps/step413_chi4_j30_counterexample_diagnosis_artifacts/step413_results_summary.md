# Step 413 Results Summary

## Key Finding

The apparent `L(s, chi_4)` `j=30` counterexample from Step 412 was a boundary truncation artifact caused by truncating the zero list at `j=30`. After computing `T31`, the true nearest neighbor is above `j=30`, not below it.

```text
T30 = 67.6369208635460683980549911506
T31 = 68.3658845038344229612337381444
s_min = 0.728963640288354563178746993803
```

## Re L'' and Contributions

```text
Re L''(rho30, chi4) = +1.74907673401781231012473702928.
```

Per-term real contributions to `L'' = 2L'g'`:

```text
Archimedean: -6.75302795071881
Close pair:  +5.64212432441989
Far residual:+2.85998036031673
Total:       +1.74907673401781
```

## Verdict

Mixed/cancellation, with a correction to Step 412: the close-pair-only predictor does not actually fail once the forward neighbor `j=31` is included. The sign is positive because the close-pair and regular far-zero residual jointly overcome the negative Archimedean contribution.
