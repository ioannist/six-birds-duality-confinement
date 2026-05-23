# Step 129 — Shifted Main-Term Positivity Audit

## Target
Audit whether the shifted Bui–Pratt–Robles–Zaharescu twisted second-moment main term can be imported as the source-weighted matrix lower-frame theorem needed by the membrane route.

The source-weighted Gram is

\[
G_{q,w}(m,n)=\sum_{\chi\in\mathcal X_q}w_\chi\chi(n)\overline{\chi(m)},
\]

with first source-weight candidate

\[
w_\chi=|L(1/2,\chi)|^2.
\]

The framework needs

\[
G_{q,w}\succeq \gamma_q H_q,
\qquad \gamma_q\to\infty.
\]

## Imported theorem platform
Bui–Pratt–Robles–Zaharescu prove a shifted asymptotic for

\[
I_{\alpha,\beta}
=
\frac1{\varphi^+(q)}
\sum_{\chi\bmod q}^{+}
L(1/2+\alpha,\chi)
L(1/2+\beta,\overline\chi)
|A(\chi)|^2,
\]

where

\[
A(\chi)=\sum_{a\le q^\kappa}\frac{\alpha_a\chi(a)}{\sqrt a},
\]

for arbitrary coefficients and length

\[
\kappa<\frac12+\frac1{202}=\frac{51}{101}.
\]

This is the right theorem platform because it is already arbitrary-coefficient and source-weighted.

## Shifted-limit kernel
Passing to the symmetric unshifted limit \(\alpha=\beta=z\to0\), the two zeta-pole terms cancel and produce the limiting main kernel

\[
M_q(\alpha)=
\sum_{da,db\le q^\kappa\atop (a,b)=1}
\frac{\alpha_{da}\overline{\alpha_{db}}}{dab}
\left(C_q-\log(ab)\right),
\]

where

\[
C_q=\log\frac q\pi+2\gamma+\psi(1/4).
\]

Equivalently, with \(d=(m,n)\),

\[
M_q(\alpha)=
\sum_{m,n\le q^\kappa}
\alpha_m\overline{\alpha_n}
\frac{(m,n)}{mn}
\left(C_q-\log\frac{mn}{(m,n)^2}\right).
\]

The exact constant must be verified against the published normalization before any formal claim.

## Main gate
The source import requires

\[
M_q\succeq c_0\log q\,H_q,
\]

where

\[
H_q(\alpha)=\sum_{n\le L}\frac{|\alpha_n|^2}{n}.
\]

Equivalently,

\[
\lambda_{\min}\left(H_q^{-1/2}M_qH_q^{-1/2}\right)
\gg \log q.
\]

## Verdict
The shifted main term is the correct operator kernel. The next proof obligation is not a scalar lower moment. It is a lower-eigenvalue theorem for this GCD-log kernel, with uniform subordinate error.

For \(\kappa<1/2\), a conservative diagonal-dominance route may be possible. For the BPRZ range \(\kappa<51/101\), off-diagonal main terms are load-bearing, so the full matrix positivity audit is essential.

## Next step
Step 130 should audit the GCD-log kernel itself:

\[
K_q(m,n)=\frac{(m,n)}{mn}\left(C_q-\log\frac{mn}{(m,n)^2}\right),
\]

and determine whether existing Hilberdink/GCD-sum or resonance-matrix results imply a lower-frame floor on the residual coefficient class, or whether the operator-lift remains new.
