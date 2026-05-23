# Step 199 Results Summary

## Verdict

`V_BN_N2000_consistent`.

The Beurling-Nyman harmonic chain was extended to `N=1500` and `N=2000` using the Step 195 arithmetic Gram formula

```text
G_{p,q} = sum_{n>=1} ((n mod p)/p)((n mod q)/q)/(n(n+1)).
```

The run used `mpmath` at 80 decimal digits for scalar setup and a Step-195-comparable symmetric eigen-pseudoinverse on the active Gram matrix.  A full `mpmath` 2000-by-2000 SVD is not feasible in this runtime; the output records this caveat explicitly.

## Computed Values

| N | delta_A^2 | delta_A^2 log(N) | condition proxy |
|---:|---:|---:|---:|
| 1000 calibration | `0.00646330050366617` | `0.0446468981738479` | `5.0051e6` |
| 1500 | `0.00611039863611640` | `0.0446866918788952` | `1.2654e7` |
| 2000 | `0.00592901311818050` | `0.0450658503926355` | `2.4906e7` |

The N=1000 calibration differs from Step 195 by `-8.09304602769102e-05` in `delta_A^2`, consistent with the larger truncation bound used here.

## Updated Fit

Using inherited Step 195 values through `N=1000` plus the new `N=1500,2000` values:

| model | range | C | alpha / spread |
|---|---|---:|---:|
| tail mean of `delta^2 log N` | `N=200,500,1000,1500,2000` | `0.0456632443937048` | spread `0.000926351` |
| `delta^2 ~ C/(log N)^alpha` | `N>=20` | `0.0547051524798759` | `alpha=1.096343229` |
| recent tail-only fit | `N>=200` | `0.0606633898663218` | `alpha=1.15047847` |

## Interpretation

The slow-log decay pattern survives to `N=2000`.  The product `delta_A^2 log(N)` remains near `0.045`, slightly below the Step 195 tail mean `0.0467` but within the expected truncation/conditioning sensitivity.  The data remain consistent with the Baez-Duarte RH-conditional Beurling-Nyman slow-log behavior; they do not prove the infinite closure.

