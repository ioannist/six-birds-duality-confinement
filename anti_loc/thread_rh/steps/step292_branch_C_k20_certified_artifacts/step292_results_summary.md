# Step 292 Results Summary — Branch C k=10/15/20 delta_Dk certification

## M(G) Provenance
Recovered from Step 196 as used by Steps 269-270: compact three-bump generators with beta bump `exp(-1/(1-u^2))` on `|u|<1`, moment coefficients enforcing the inherited endpoint constraints.
- `G_star`: centers `1.5;2.5;3.5`, epsilon `0.20`, coefficients `1.0;-3.3409952306131084085969211508;2.3409952306131084085969211508`.
- `G_prime`: centers `2.0;2.5;3.0`, epsilon `0.25`, coefficients `1.0;-2.50307172422744214727451181436;1.50307172422744214727451181436`.

## Certified delta_Dk Values
Values are raw `delta_Dk=(zeta*M(G))^(k)(rho)` proxies, not exact projected `L_k`. dps80 and dps100 agreed to the displayed precision.

| triple | k=10 | k=15 | k=20 |
|---|---:|---:|---:|
| `rho1_G_star` | `165.439` | `8515.27` | `554847` |
| `rho2_G_star` | `667.785` | `75532.1` | `8.74461e+06` |
| `rho1_G_prime` | `115.543` | `3851.26` | `169966` |

## Fit Residuals vs Step 269 k=0..7 Polynomial-Corrected Fit
Step 269 fit values used verbatim: `rho1_G_star` a=0.1761, b=0.7497, c=-0.2998; `rho2_G_star` a=0.2070, b=1.0832, c=-1.1248; `rho1_G_prime` a=0.2387, b=0.6441, c=-0.1369.

| triple | max residual / RMSE | decision |
|---|---:|---|
| `rho1_G_star` | `1.97e+07` | `law_breaks_for_delta_proxy` |
| `rho2_G_star` | `4.04e+08` | `law_breaks_for_delta_proxy` |
| `rho1_G_prime` | `7.01e+06` | `law_breaks_for_delta_proxy` |

At k=15 and k=20, residuals are orders of magnitude beyond the Step 269 RMSE, so the inherited law does not continue for the raw delta proxy.

## Projected Spot Check
Legacy projected k=10 spot-check for `rho1_G_star`: `|projected|=14536`, `|delta|=165.439`, ratio `0.0113813`. This does not confirm `L_k≈delta_Dk` at k=10; projected high-k certification remains open and the legacy projected pipeline is not used as the primary result.

Final verdict: `V_branch_C_k20_law_breaks`. Direct delta proxy computation is certified; projected Branch C `L_k` is not certified by this reduction at high k.
