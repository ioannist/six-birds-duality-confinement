# Step 433 Trace Formula Comparison

For compact hyperbolic `M_0`, Selberg's trace formula has spectral side `sum_n h(r_n)` and a geometric side over primitive closed geodesics:

```text
vol(M_0)/(4pi) integral r h(r) tanh(pi r) dr
+ sum over primitive gamma and k>=1 of ell(gamma)/(2sinh(k ell(gamma)/2)) hhat(k ell(gamma)).
```

The Weil explicit formula for zeta has a prime side involving `log p` and prime powers. Therefore the critical structural test is whether the primitive length spectrum `ell(gamma)` of the non-arithmetic surface naturally equals `{log p}`.

## Numerical short-length comparison

| rank | l_gamma sample | log prime | difference |
|---:|---:|---:|---:|
| 1 | 2.000000 | 0.693147 | +1.306853 |
| 2 | 2.828427 | 1.098612 | +1.729815 |
| 3 | 3.601491 | 1.609438 | +1.992053 |
| 4 | 3.915664 | 1.945910 | +1.969754 |
| 5 | 5.385168 | 2.397895 | +2.987273 |
| 6 | 5.767992 | 2.564949 | +3.203042 |
| 7 | 5.822383 | 2.833213 | +2.989169 |
| 8 | 6.353257 | 2.944439 | +3.408818 |
| 9 | 6.658806 | 3.135494 | +3.523312 |
| 10 | 6.689525 | 3.367296 | +3.322229 |
| 11 | 7.242500 | 3.433987 | +3.808513 |
| 12 | 7.354944 | 3.610918 | +3.744026 |
| 13 | 7.747583 | 3.713572 | +4.034011 |
| 14 | 8.089457 | 3.761200 | +4.328257 |
| 15 | 8.187255 | 3.850148 | +4.337107 |
| 16 | 8.187255 | 3.970292 | +4.216963 |
| 17 | 8.514662 | 4.077537 | +4.437125 |
| 18 | 8.842089 | 4.110874 | +4.731215 |
| 19 | 8.842089 | 4.204693 | +4.637396 |
| 20 | 8.876953 | 4.262680 | +4.614273 |

## Result

The sampled non-arithmetic length values are not structurally or numerically `{log p}`. This is expected: a generic non-arithmetic compact surface has a length spectrum determined by geodesic holonomy, not rational prime data.

Thus Selberg zeta `Z_M0(s)` is not the Riemann zeta function. The trace formula is formally analogous to Weil's explicit formula, but the geometric side is the wrong object for RH unless arithmetic is reintroduced, which the grammar forbids.
