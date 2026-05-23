# Step 137: Blind-projected incidence norm audit

## Purpose

Step 137 audits the sharper object exposed by Step 136:

\[
\left\|
\Pi_{\mathcal B}
Z_y(I-P_{\Omega\le K})B_NG_{B,N}^{-1/2}
\right\|,
\]

not the full incidence norm \(\|Z_y(I-P_{\Omega\le K})\|\).

The goal is to decide whether the GCD-log blind sector from Step 130 can be controlled on the actual Burnol/Muentz residual coefficient class.

## Main correction

The raw unweighted Boolean model had exact upward-closure annihilation:

\[
\Pi_{\mathcal B} Z_y b
\quad\text{only sees high-divisibility seed coefficients.}
\]

After passing to the source-compatible central-line Dirichlet metric, this becomes weighted leakage.

For a prime \(p\), set \(r_p=p^{-1/2}\). The normalized local incidence block is

\[
A_p=\begin{pmatrix}1&0\\ r_p&1\end{pmatrix}.
\]

For Walsh rows

\[
v_+=\frac{(1,1)}{\sqrt2},
\qquad
v_- =\frac{(1,-1)}{\sqrt2},
\]

we get

\[
 v_+^*A_p=\frac{1}{\sqrt2}(1+r_p,1),
\]

\[
 v_-^*A_p=\frac{1}{\sqrt2}(1-r_p,-1).
\]

So a negative Walsh coordinate no longer sees only the seed coefficient containing \(p\). It also sees the absent coefficient with leakage factor

\[
1-p^{-1/2}.
\]

Thus:

\[
\boxed{
\text{exact raw annihilation becomes source-compatible weighted leakage.}
}
\]

## Blind-projected decomposition

For a declared blind Walsh family \(\mathcal B\), define

\[
L_{\mathcal B,K}
=
\|\Pi_{\mathcal B}Z_yP_{\Omega\le K}\|,
\]

\[
T_{\mathcal B,K}
=
\|\Pi_{\mathcal B}Z_y(I-P_{\Omega\le K})\|.
\]

Then for any seed \(b\),

\[
\|\Pi_{\mathcal B}Z_yb\|
\le
L_{\mathcal B,K}\|P_{\Omega\le K}b\|
+
T_{\mathcal B,K}\|(I-P_{\Omega\le K})b\|.
\]

For the actual Burnol/Muentz window,

\[
\Xi_{{\rm GCD},N}
=
R_N^*\Pi_{\mathcal B}R_N,
\qquad
R_N=Z_yB_N.
\]

A sufficient bound is

\[
\Xi_{{\rm GCD},N}
\preceq
\delta_N^2G_{B,N},
\]

where

\[
\delta_N
\le
L_{\mathcal B,K}
+
T_{\mathcal B,K}
\|(I-P_{\Omega\le K})B_NG_{B,N}^{-1/2}\|.
\]

## All-minus row

For the deepest all-minus Walsh mode,

\[
\|v_-^{\otimes k}{}^*Z_y\|^2
=
\prod_{p\le y}
\left(1-p^{-1/2}+\frac{1}{2p}\right).
\]

Hence

\[
\log \|v_-^{\otimes k}{}^*Z_y\|
=
-(1+o(1))\frac{\sqrt y}{\log y}.
\]

So the deepest blind row is suppressed in the source-compatible metric, even though the full incidence norm is amplified.

## Restricted BPRZ salvage

If the GCD-log kernel satisfies

\[
K_q\succeq \gamma_q I,
\qquad
\gamma_q\asymp\log q,
\]

on the nonblind sector, and if

\[
\|\Pi_{\mathcal B}R_NG_{B,N}^{-1/2}\|\le \delta_N<1,
\]

then

\[
R_N^*K_qR_N
\succeq
\gamma_q(1-\delta_N^2)G_{B,N}.
\]

Exact suppression \(\delta_N\to0\) is sufficient, but a uniform floor \(\delta_N<1\) is enough because \(\gamma_q\to\infty\), provided fixed/exhaustive tail promotion also passes.

## Toy audit

The finite sanity checks are not RH evidence.

They show:

- blind projection is much sharper than the full incidence norm;
- all-minus deep blind rows are suppressed in the central-line metric;
- low-\(\Omega\) leakage is real and must be accounted for;
- high-\(\Omega\) tail control alone is not enough unless the low-\(\Omega\) leakage term is also small.

## Route status

The active source route now requires a combined estimate:

\[
\boxed{
L_{\mathcal B,K}(y,1)
+
T_{\mathcal B,K}(y,1)
\|(I-P_{\Omega\le K})B_NG_{B,N}^{-1/2}\|
<1
}
\]

uniformly, or ideally tending to zero.

## Bottom line

\[
\boxed{
\text{Step 137 makes the GCD-log blind-sector gate source-metric correct.}
}
\]

The next step is:

\[
\boxed{\textbf{Step 138: \(\Omega\)-threshold optimization for blind-projected incidence.}}
\]

Target: choose \(K_N\), blind threshold \(R_N\), and prime window \(y_N\) so that low-\(\Omega\) leakage and high-\(\Omega\) tail are jointly below a usable floor.
