# Step 247 Results Summary

## Symbolic k=1 Derivative

Using Burnol 2002 eq. 1 / Theorem 8 notation,

```text
K_a^Gamma(z,w) =
  [E_lambda(z) Ebar_lambda(w) - E_lambda(1-z) Ebar_lambda(1-w)]
  / (z+w-1).
```

The anti-holomorphic first jet is

```text
partial_wbar K_a^Gamma(z,w)
  = [E(z) conj(E'(w)) + E(1-z) conj(E'(1-w))] / (z+w-1),
```

under the inherited `z+w-1` denominator convention, so the denominator contributes no `partial_wbar` term. The sign in the second term comes from
`partial_wbar conj(E(1-w)) = -conj(E'(1-w))`.

The derivative of Burnol's Theorem 8 function is

```text
E'(w)=P'(w)B(w)+P(w)B'(w),
P'/P=-0.5 log(pi)+0.5 digamma(w/2),
B'=-log(lambda)lambda^(1/2-w)
   -(sqrt(lambda)/2) int psi_diff(t)t^(-w)log(t)dt.
```

Operationally, step 196's Branch C convention gives

```text
L_{rho,1}(G) = -i d/dgamma [(P_infty M_zeta G)(1/2+i gamma)]_{gamma=Im rho}.
```

Step 247 differentiates the step 196 sinc+PSWF projected-value formula analytically instead of using central finite differences.

## Proper k=1 Values

| case | rho | G | proper L | |L| | error | lower |
|---|---|---|---:|---:|---:|---:|
| C16 | rho_1 | G_star | `-0.2035000848 + 0.2058173914 i` | `0.2894358013` | `9.65e-6` | `0.2894261536` |
| C17 | rho_2 | G_star | `-0.2885165538 + 0.0065784014 i` | `0.2885915404` | `6.56e-6` | `0.2885849807` |
| C18 | rho_1 | G_prime | `-0.3941798798 + 0.0779675121 i` | `0.4018167625` | `2.80e-6` | `0.4018139639` |

The minimum proper k=1 lower bound is `0.2885849807`.

## Finite-Difference Comparison

The largest difference from step 196's finite-difference diagnostics is `2.30e-5`, far below the old k=1 error bars (`8.5e-3` to `1.97e-2`). The proper derivative therefore confirms the old k=1 diagnostic while sharply reducing its uncertainty.

## Verdict

`V_branch_C_k1_proper_foreclosure`.
