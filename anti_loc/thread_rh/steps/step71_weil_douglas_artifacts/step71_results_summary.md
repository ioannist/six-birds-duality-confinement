# Step 71 — Weil–Douglas Bridge Gate

This step begins the RH-specific construction program by isolating the first load-bearing obligation:

\[
\mathsf A_Z \preceq \mathsf K_{\rm cmp}.
\]

The result is not an RH proof. It states exactly what the explicit formula must become: a Douglas-contractive factorization

\[
V_Z = T W_{\rm cmp},\qquad \|T\|\le 1.
\]

Here \(V_Z\) is the zero-side anti-invariant displacement readout and \(W_{\rm cmp}\) is the completed carrier feature map, decomposed into prime-power, gamma/archimedean, pole/completion, and tail components.

## Main theorem

For Hilbert-space maps \(V:Y\to \mathcal Z\) and \(W:Y\to\mathcal E\), the following are equivalent:

\[
V^*V\preceq W^*W,
\]

\[
\|Vy\|\le \|Wy\|\quad\forall y,
\]

and there exists a contraction \(T\) such that

\[
V=TW.
\]

Thus the RH explicit-formula bridge must be a contractive domination, not merely a scalar explicit-formula identity.

## Why this matters

The classical explicit formula has signed pieces. The framework requires a positive feature representation:

\[
W_{\rm cmp}=W_{\rm pr}\oplus W_\infty\oplus W_{\rm pole}\oplus W_{\rm tail}.
\]

If any of these terms are missing or remain signed, the honest record is a defect:

\[
\mathsf A_Z\preceq \mathsf K_{\rm vis}+E_{\rm EF}.
\]

## Key warning

Trace equality is not enough. It is possible that

\[
\operatorname{tr}\mathsf A_Z=\operatorname{tr}\mathsf K_{\rm cmp}
\]

while

\[
\mathsf A_Z\npreceq\mathsf K_{\rm cmp}.
\]

The needed relation is Loewner domination / Douglas factorization.

## Next construction target

Construct the actual zeta/Weil objects:

\[
Y^-,\quad V_Z,\quad W_{\rm pr},\quad W_\infty,\quad W_{\rm pole},\quad W_{\rm tail}
\]

and prove

\[
V_Z=T(W_{\rm pr}\oplus W_\infty\oplus W_{\rm pole}\oplus W_{\rm tail}),\qquad \|T\|\le1.
\]
