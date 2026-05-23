# Step 143: Ω-Filtration Density Theorem / Obstruction Audit

## Main verdict

The Ω-compatible Burnol/Müntz dictionary is **dense only relative to the declared regularized Dirichlet-readable shadow closure**.

That is, if \(P_{\Omega,K}\to P_D\) strongly, then finite Ω cutoffs exhaust the Dirichlet-readable part of the residual class. But this does not by itself prove that the whole Burnol/Sonine residual class is Dirichlet-readable, nor that the needed cutoff sequence stays inside the source shortness budget.

## Active defect

\[
\epsilon_{B\to\Omega,N}(K)
=
\|(I-P_{\Omega,K,N})M_{R,N}G_{R,N}^{-1/2}\|.
\]

The corresponding adequacy residual is

\[
\Xi_{B\to\Omega,N}(K)
=
M_{R,N}^*(I-P_{\Omega,K,N})M_{R,N}.
\]

## Main theorem

If

\[
P_{\Omega,K,N}\uparrow P_{D,N},
\]

then for fixed finite windows,

\[
\limsup_{K\to\infty}
\epsilon_{B\to\Omega,N}(K)
\le
\epsilon_{B\to D,N}.
\]

For growing windows, the route needs a diagonal ladder

\[
K_N\to\infty
\]

such that

\[
\|(P_{D,N}-P_{\Omega,K_N,N})M_{R,N}G_{R,N}^{-1/2}\|\to0.
\]

## Bicriteria source condition

The restricted source route remains viable if

\[
\epsilon_{B\to\Omega,N}(K_N)<1,
\quad
\delta_{R_N,K_N,N}<1,
\quad
\gamma_q\to\infty,
\]

with completed fixed/exhaustive tail promotion.

Then

\[
\Lambda_N^\Omega
\gtrsim
\gamma_q
(1-\epsilon_{B\to\Omega,N}^2)
(1-\delta_{R,K,N}^2).
\]

## Obstruction

If

\[
(I-P_{\Omega,\infty})M_R\ne0,
\]

then

\[
\Xi_{B\to\Omega}
=
M_R^*(I-P_{\Omega,\infty})M_R
\]

is a real residual. Increasing the cutoff cannot remove it.

## Bottom line

Step 143 does not close the density gate. It turns it into the exact diagonal problem:

\[
\text{regularized shadow adequacy}
+
\text{Ω cutoff density}
+
\text{source shortness}
+
\text{GCD blind-sector floor}.
\]

Next step: **Step 144: completed residual-tail promotion for the Ω-compatible ladder.**
