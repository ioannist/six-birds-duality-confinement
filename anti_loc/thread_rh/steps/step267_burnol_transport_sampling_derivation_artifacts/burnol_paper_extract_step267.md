# Burnol Paper Extracts for Step 267

Sources fetched:

- Burnol 2002: `math/0208121`, "Sur les Espaces de Sonine associes par de Branges a la transformation de Fourier".
- Burnol 2004: `math/0112254`, "On Fourier and Zeta(s)", Forum Mathematicum 16 (2004), 789-840.

Only the formulas needed for the derivation attempt are transcribed.

## Burnol 2002, Equation (1): de Branges Kernel

```tex
K(z_1, z_2) =
\frac{E(z_1)E(z_2) - E(1-z_1)E(1-z_2)}{z_1 + z_2 - 1}
```

Equivalent displayed form:

```tex
K(z_1, z_2)
= 2\frac{(-iB(z_1))A(z_2)+A(z_1)(-iB(z_2))}{z_1 + z_2 - 1}
```

## Burnol 2002, Theorem 4: Sonine Projection

```tex
\pi_\lambda(f) =
f - (1 - D_\lambda)^{-1}\Big(P_\lambda(f) - F_\lambda\mathcal F_+(f)\Big)
- \mathcal F_+(1 - D_\lambda)^{-1}
\Big(P_\lambda\mathcal F_+(f) - F_\lambda(f)\Big)
```

with

```tex
F_\lambda = P_\lambda \mathcal F_+ P_\lambda,
\qquad D_\lambda = F_\lambda^2.
```

Burnol also states that \(D_\lambda\) may be replaced by the restricted
Dirichlet kernel

```tex
\sin(2\pi\lambda(x-y))/\pi(x-y).
```

## Burnol 2002, Theorem 8: \(E_\lambda\)

```tex
\mathcal E_\lambda(w) =
\pi^{-w/2}\Gamma(w/2)
\Big(\lambda^{1/2-w}
+ \frac{\sqrt{\lambda}}{2}
\int_\lambda^\infty
(\psi_+^\lambda(t)-\psi_-^\lambda(t))t^{-w}dt\Big)
```

This makes the de Branges kernel explicit after substitution into equation (1).

## Burnol 2004, Section 6: Mellin Transform and Evaluators

The completed Mellin transform on \(K_\lambda\):

```tex
M(f)(s) := \pi^{-s/2}\Gamma(s/2)
\int_\lambda^\infty f(t)t^{-s}dt.
```

Evaluator vectors:

```tex
\forall f\in K_\lambda\quad [f,Z^\lambda_{w,k}]
= M(f)^{(k)}(w).
```

Fourier action on evaluator vectors:

```tex
\mathcal F_+(Z^\lambda_{w,k}) = (-1)^k Z^\lambda_{1-w,k}.
```

Zero-evaluator span:

```tex
Z_\lambda =
\overline{\operatorname{span}}\{Z^\lambda_{\rho,k}: 0\leq k<m_\rho\}.
```

Main theorem component:

```tex
K_\lambda = Z_\lambda \quad \text{if and only if}\quad \lambda\geq 1.
```

## Extract Assessment

The fetched formulas provide:

- exact projection \(\pi_\lambda\);
- exact de Branges kernel \(K\);
- exact \(E_\lambda\);
- continuous Mellin evaluator vectors \(Z^\lambda_{w,k}\);
- a closed infinite zero-evaluator span theorem for \(\lambda\geq1\).

They do not provide the cascade-needed finite identity

```tex
\pi_\lambda^* M_\zeta^* Z_w
= \sum_{i=1}^N c_i Z^\lambda_{\tau_i,0}.
```

This missing finite transported-evaluator expansion is the gap.
