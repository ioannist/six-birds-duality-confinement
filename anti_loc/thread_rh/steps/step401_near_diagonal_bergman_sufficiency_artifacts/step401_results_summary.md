# Step 401 Results Summary

## Scale Comparison

For the Step220 maximizer `(sigma, ell)=(0.35,2.0)`,

```text
wavepacket width ~= 1/(sigma*T).
```

The standard near-diagonal condition is

```text
1/(sigma*T) <= 1/sqrt(p)
```

or `p <= (sigma*T)^2`.

Key values:

- `T=14.1347`: width `0.2021`, standard near-diagonal through `p<=20`, marginal at `p=30`, log-window still true.
- `T=100`: width `0.02857`, standard near-diagonal through `p<=1000`.
- `T=10000`: width `0.0002857`, standard near-diagonal through `p<=12,250,000`.

## Regime Identification

The Step220 essential-norm computation is a large-`T` wavepacket calculation.
For any `p` comparable to the cascade's finite `k` scales, the wavepacket is
comfortably near-diagonal at large `T`.

## Verdict

Marginal / conditional sufficiency.

Near-diagonal Bergman asymptotics are sufficient for Branch A's large-`T`
wavepacket regime if the missing dictionary identifies `p` as bounded or
subquadratic in `sigma*T`.  The low-`T` regime is marginal, and Branch C still
requires the off-diagonal/transition asymptotic.

No RH claim is made.
