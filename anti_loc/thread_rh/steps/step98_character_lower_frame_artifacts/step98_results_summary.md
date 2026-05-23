# Step 98 — Finite Character Orthogonality versus Completed Lower-Frame Audit

## Core result
For a finite abelian group \(G\), the complete character family \(\widehat G\) is an orthonormal basis of \(\ell^2(G)\). Thus finite character analysis is a tight frame:

\[
\sum_{\chi\in\widehat G} P_\chi=I_{\ell^2(G)}.
\]

For Dirichlet characters modulo \(q\), this gives a tight frame on the unit group

\[
G_q=(\mathbb Z/q\mathbb Z)^\times.
\]

## Main warning
This finite tight-frame theorem is not yet a completed RH source frame. A conductor window, finite quotient, or finite character set controls only the visible finite response sector. To promote to the completed anti-invariant response space \(Y^-\), we need a tail/exhaustivity record:

\[
I_{Y^-}\preceq R_n^*R_n+T_n,
\qquad
\operatorname{tr}T_n\to0.
\]

Without that bridge, the status is:

\[
\texttt{finite\_window\_support\_only}.
\]

## Completed lower-frame target
The RH source route needs

\[
F_n=
\sum_{\omega\in\mathcal X_n}
\lambda_{\omega,n}Q_\omega^*\Theta_\omega^{-1}Q_\omega
\succeq
\Lambda_n(\Theta_0^-)^{-1},
\qquad
\Lambda_n\to\infty.
\]

Then

\[
K_n^-\preceq \Lambda_n^{-1}\Theta_0^-+E_{\rm src,n}.
\]

So budget collapse follows only from full lower-frame coverage plus vanishing defects.

## What the checks showed
The finite algebra checks confirm:

- full cyclic character families give identity frame operators up to numerical roundoff;
- partial character subsets leave null directions;
- finite windows need a vanishing tail to promote;
- lower-frame budget collapse fails if there is a fixed hidden hole or nonvanishing defect.

These are algebra sanity checks, not RH evidence.

## Bottom line
Finite character orthogonality is real but finite. The RH route needs:

\[
\boxed{
\text{finite character frames}
+
\text{Plancherel/exhaustivity}
+
\text{lower-frame growth}
\Rightarrow
\text{completed anti-invariant budget collapse}.
}
\]
