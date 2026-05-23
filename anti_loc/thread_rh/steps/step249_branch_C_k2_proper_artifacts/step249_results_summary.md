# Step 249 Results Summary

## Symbolic k=2 Derivation

From the inherited Burnol kernel convention

```text
K_a^Gamma(z,w)=
  [E(z) Ebar(w)-E(1-z) Ebar(1-w)]/(z+w-1),
```

step 247 gave

```text
partial_wbar K =
  [E(z)conj(E'(w)) + E(1-z)conj(E'(1-w))]/(z+w-1).
```

The second derivative is

```text
partial_wbar^2 K =
  [E(z)conj(E''(w)) - E(1-z)conj(E''(1-w))]/(z+w-1).
```

The sign in the second term is negative: differentiating `conj(E'(1-w))` with respect to `wbar` contributes `-conj(E''(1-w))`. The denominator has no `partial_wbar` contribution under the inherited `z+w-1` convention.

For Burnol 2002 Theorem 8, writing `E=P B`,

```text
E'' = P''B + 2P'B' + P B'',
P''/P = 0.25 polygamma(1,w/2)
       + (-0.5 log(pi)+0.5 digamma(w/2))^2,
B'' = (log lambda)^2 lambda^(1/2-w)
      + (sqrt(lambda)/2) int psi_diff(t)t^(-w)(log t)^2 dt.
```

Operationally, this is evaluated in the step 196/247 convention as

```text
L_{rho,2}(G)=(-i d/dgamma)^2 [(P_infty M_zeta G)(1/2+i gamma)].
```

## k=2 Values

| case | rho | G | proper L | |L| | error | lower |
|---|---|---|---:|---:|---:|---:|
| C19 | rho_1 | G_star | `0.3724577601 - 0.4359254491 i` | `0.5733722876` | `1.15e-5` | `0.5733607751` |
| C20 | rho_2 | G_star | `0.5470714228 + 0.0947686206 i` | `0.5552190856` | `7.64e-6` | `0.5552114438` |
| C21 | rho_1 | G_prime | `0.7521438686 - 0.0499058441 i` | `0.7537977132` | `3.14e-6` | `0.7537945745` |

Minimum proper k=2 lower bound: `0.5552114438`.

## Comparison With k=0 and k=1

- Step 196 k=0 minimum lower bound: about `0.0341`.
- Step 247 k=1 minimum lower bound: `0.2885849807`.
- Step 249 k=2 minimum lower bound: `0.5552114438`.

The tested Branch C evaluator orders `k=0,1,2` all remain bounded away from zero on their sampled legal triples.

## Verdict

`V_branch_C_k2_proper_foreclosure`.
