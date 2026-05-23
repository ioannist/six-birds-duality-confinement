# Step 136 — Response-Metric Normalization for the Incidence Operator

## Main verdict

The raw Boolean incidence amplification

\[
\|Z_y\|_{\ell^2}=\varphi^{\pi(y)}
\]

is **not** the correct final metric for the RH source route.

In the critical-line Dirichlet coefficient metric

\[
\|a\|_{H_1}^2=\sum_n |a_n|^2/n,
\]

the incidence norm becomes

\[
\|Z_y\|_{H_1}
=
\prod_{p\le y}\sigma_p(1)
=
\exp\{O(\sqrt y/\log y)\}.
\]

So the Burnol/Müntz/Dirichlet response metric reduces the raw amplification from

\[
\exp(\asymp y/\log y)
\]

to

\[
\exp(O(\sqrt y/\log y)).
\]

This is a major reduction, but not a complete elimination.

---

## One-prime theorem

For one prime, the incidence block is

\[
Z_p=\begin{pmatrix}1&0\\1&1\end{pmatrix}.
\]

In the weighted metric

\[
\|(b_0,b_1)\|_{H_\sigma}^2=|b_0|^2+p^{-\sigma}|b_1|^2,
\]

its orthonormal-coordinate form is

\[
A_{p,\sigma}
=
\begin{pmatrix}1&0\\p^{-\sigma/2}&1\end{pmatrix}.
\]

Therefore

\[
\sigma_p(\sigma)^2
=
1+\frac{p^{-\sigma}}2
+p^{-\sigma/2}\sqrt{1+\frac{p^{-\sigma}}4}.
\]

Tensoring over primes gives

\[
\boxed{
\|Z_y\|_{H_{\sigma,y}}
=
\prod_{p\le y}\sigma_p(\sigma).
}
\]

For \(\sigma=0\), this recovers the raw norm \(\varphi^{\pi(y)}\). For \(\sigma=1\), this is the critical-line Dirichlet/BPRZ coefficient norm.

---

## Incidence-conditioned tail gate

The correct tail is

\[
\tau_{\Omega,N}^{Z}
=
\|Z_y(I-P_{\Omega\le K})B_NG_{B,N}^{-1/2}\|.
\]

If

\[
\|(I-P_{\Omega\le K})B_NG_{B,N}^{-1/2}\|_{H_{\sigma,y}}
\le e_{\Omega,N},
\]

then

\[
\boxed{
\tau_{\Omega,N}^{Z}
\le
\left(\prod_{p\le y}\sigma_p(\sigma)\right)e_{\Omega,N}.
}
\]

For \(\sigma=1\), the seed tail only needs to beat the subexponential incidence factor

\[
\exp(O(\sqrt y/\log y)).
\]

In raw Boolean geometry it would need to beat

\[
\exp(\asymp y/\log y).
\]

---

## Relation to \(\Xi_{\rm GCD}\)

The GCD-log blind residual is

\[
\Xi_{{\rm GCD},N}=R_N^*\Pi_{\mathcal B}R_N.
\]

Step 136 gives

\[
\boxed{
\Xi_{{\rm GCD},N}
\preceq
(\tau_{\Omega,N}^{Z})^2G_{B,N}.
}
\]

So the blind-sector residual is controlled exactly by the response-metric-conditioned high-\(\Omega\) tail.

---

## What remains open

Step 136 does not prove the actual Burnol/Müntz seed estimate. It proves that the right metric is not raw Boolean \(\ell^2\), but the critical-line response metric or a stronger semilocal metric.

The open record is:

\[
\boxed{
\|Z_y(I-P_{\Omega\le K})B_NG_{B,N}^{-1/2}\|_{H_1}
\to0
}
\]

or at least

\[
\boxed{
\|Z_y(I-P_{\Omega\le K})B_NG_{B,N}^{-1/2}\|_{H_1}
\le \tau<1.
}
\]

---

## Bottom line

\[
\boxed{
\text{the response metric reduces incidence amplification but does not remove the tail gate.}
}
\]

The next step is:

\[
\boxed{\textbf{Step 137: critical-line }H_1\textbf{ seed-tail estimate}.}
\]

Target: estimate the actual Burnol/Müntz residual seed tail in the metric

\[
\|b\|_{H_1}^2=\sum_n |b_n|^2/n,
\]

and decide whether it beats

\[
\prod_{p\le y}\sigma_p(1).
\]
