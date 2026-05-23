# Step 250 Results Summary

## Target

Branch C higher-order evaluator growth:

`|L_{rho,k}(G)|` for `k = 0,1,2,3,4` on the three specific triples
`(rho_1, G_star)`, `(rho_2, G_star)`, `(rho_1, G_prime)`.

## Higher-k Kernel Rule

Using Burnol 2002 Theorem 8 and the kernel formula from equation (1), the
anti-holomorphic derivatives satisfy

`partial_wbar^k K_a^Gamma(z,w) =
[E(z) conj(E^(k)(w)) + (-1)^(k+1) E(1-z) conj(E^(k)(1-w))] / (z+w-1)`.

For operational numerical evaluation this is equivalent on the critical-line
samples to applying `(-i d/dgamma)^k` to the projected branch-C functional.

## k=3 and k=4 Values

| triple | k=3 | k=4 |
|---|---:|---:|
| `rho1_G_star` | `1.1164964359 +/- 9.31e-6` | `2.2021731761 +/- 1.15e-5` |
| `rho2_G_star` | `1.1457543044 +/- 6.66e-6` | `2.5868233085 +/- 7.55e-6` |
| `rho1_G_prime` | `1.3778472859 +/- 2.71e-6` | `2.5398826197 +/- 3.24e-6` |

All tested k=3 and k=4 values remain bounded well away from zero.

## Growth Fit

Tested models: linear, quadratic, exponential, factorial, affine factorial,
and Pochhammer `(1)_k`.  The best raw RMSE for all three triples was
exponential:

| triple | best model | RMSE |
|---|---|---:|
| `rho1_G_star` | exponential | `2.7407e-3` |
| `rho2_G_star` | exponential | `3.3832e-2` |
| `rho1_G_prime` | exponential | `3.4952e-3` |

The factorial/Pochhammer fits were substantially worse on k=0..4.

## Extrapolation

Exponential extrapolations are diagnostic only, not theorem-grade:

| triple | predicted k=5 | predicted k=10 |
|---|---:|---:|
| `rho1_G_star` | `4.3235` | `126.4457` |
| `rho2_G_star` | `5.5588` | `261.8553` |
| `rho1_G_prime` | `4.6814` | `99.5022` |

## Verdict

`V_branch_C_k_growth_law_exponential`.

On the sampled Branch C triples, the k-growth is cleanly nonzero and is best
fit by an exponential law over k=0..4. This does not prove an asymptotic growth
law and does not alter the retained Branch C nonclaim boundary.
