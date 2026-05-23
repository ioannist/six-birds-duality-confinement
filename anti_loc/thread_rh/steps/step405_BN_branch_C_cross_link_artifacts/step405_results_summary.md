# Step 405 Results Summary

## Partial Sum

First 100 positive zeta zeros:

```text
sum_{j=1}^{100} 1/|rho_j|^2
 = 0.019984852403923805300300450226026915
```

Closed-form Báez-Duarte constant:

```text
2 + gamma_E - log(4*pi)
 = 0.046191417932242067628620495812990583
```

Fraction captured by first 100 positive zeros:

```text
43.2652932049834%
```

Cascade Step199 empirical:

```text
d_N^2 log N ~= 0.0457
```

Relative difference from closed form:

```text
about 1.06%
```

## Cross-Link Assessment

Branch C structural law:

```text
gamma_zeta(T) ~= pi/(T*log(T/(2*pi))).
```

This shares the Riemann-von-Mangoldt local-density logarithm with the BN zero
sum, but it is a Burnol/Sonine matrix-element decay rate, not the
Báez-Duarte residue weight.

## Verdict

No new BN constraint.  There is a weak structural cross-link through the common
zero-density factor `log(T/(2*pi))`, but Branch C does not change the known
Báez-Duarte constant or improve the `d_N^2 ~ A/log N` law without an additional
residue-to-matrix-element bridge theorem.

No RH claim is made.
