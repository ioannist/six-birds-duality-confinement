# Step 410 Results Summary

## Four-Point Raw-Proxy Test

Using the Step 292 raw proxy generalized to arbitrary `s`,

```text
delta_Dk(s) = (zeta*M(G_star))^(k)(s),
```

with `k=5` and `T = Im(rho_1) = 14.1347251417346937904572519836`, the computed magnitudes were:

| point | `|delta_D5|` | threshold status |
|---|---:|---|
| `0.5+iT` actual `rho_1` | `4.276557470203644` | pass |
| `0.7+iT` off-critical right | `2.847142289161922` | pass |
| `0.3+iT` off-critical left | `6.430420423102830` | pass |
| `0.5+14.0i` on-line nonzero | `4.253088491394162` | pass |

All values are well above the Step 196 threshold `0.034`.

## Verdict

No foreclosure-discriminating signal appears in this raw-proxy test. The evaluator is not position-blind, since right and left off-critical shifts change the magnitude asymmetrically, but the changes remain same-scale and do not violate the bound. The nearby critical-line nonzero point is almost indistinguishable from the actual-zero value at this test resolution.

The off-critical test is interpretively limited because the Burnol/Sonine zero-spectral carrier is not directly defined at nonzero off-critical points.
