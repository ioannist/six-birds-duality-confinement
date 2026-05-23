# Step 259 Results Summary

## Moment Carrier

For fixed `k >= 1`,

`M_{2k}(T) = int_0^T |zeta(1/2+it)|^{2k} dt`.

The Keating-Snaith residual is

`Xi_{2k}(T) = |M_{2k}(T)/(a_k g_k T (log T)^{k^2}) - 1|`.

Closure is `Xi_{2k}(T) -> 0` for each fixed `k`.

## Keating-Snaith Prediction

`M_{2k}(T) ~ a_k g_k T (log T)^{k^2}`,

where `a_k` is the arithmetic Euler product and

`g_k = prod_{j=0}^{k-1} j!/(j+k)!`

is the CUE/RMT factor.

## Proved vs Conjectural

- `k=1`: second moment proved, `M_2(T) ~ T log T`.
- `k=2`: fourth moment proved by Ingham,
  `M_4(T) ~ (1/(2*pi^2)) T (log T)^4`.
- `k=3`: sixth moment conjectural, Conrey-Ghosh.
- General `k`: Keating-Snaith / CFKRS conjectural.

## Classification Call

Moments are not cross-correlations and not RH-equivalent.  They are averaged
critical-line growth residuals.  Since Lindelof is equivalent to
`M_{2k}(T)=O_k(T^{1+epsilon})` for all fixed `k`, moments refine the
Subconvexity Extension rather than forming a separate ninth framework finding.

Subtype refinement:

- Type alpha: pointwise/sup-bound growth residuals.
- Type beta: moment-growth and precise moment-asymptotic residuals.

## Status

`Selberg-Class Subconvexity Extension` updated to:

`candidate (verified-on-4-growth-rate-instances, subtype-refined alpha/beta) corpus-pending`.

## Verdict

`V_moments_inside_subconvexity_extension`.
