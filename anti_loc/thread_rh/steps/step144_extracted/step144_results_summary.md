# Step 144: Completed residual-tail promotion for the Omega-compatible ladder

## Main purpose

Step 144 promotes the finite \(\Omega\)-compatible source-frame certificates to the completed residual ledger, or else marks them as moving-window support evidence.

The active finite source strength is

\[
\Lambda_N^\Omega
=
\gamma_{q_N}
(1-\epsilon_{B\to\Omega,N}^{2})
(1-\delta_{R,K,N}^{2}).
\]

The finite lower frame is

\[
F_N^{\Omega,\mathrm{win}}\succeq \Lambda_N^\Omega G_{R,N}.
\]

The completed promotion requires a residual carrier \(H_R\), a fixed residual ledger \(K_R\) or \(A_R\), window projections \(P_N\), and a tail form \(T_N\) such that

\[
G_R\preceq P_N^*G_{R,N}P_N+T_N.
\]

Then the lifted source frame satisfies

\[
F_N^\Omega+\Lambda_N^\Omega T_N\succeq \Lambda_N^\Omega G_R.
\]

## Completed budget squeeze

If

\[
\sup_N \operatorname{tr}(F_N^\Omega K_R)\le C_{\rm src},
\]

and

\[
\operatorname{tr}(T_NK_R)\to0,
\]

then

\[
\operatorname{tr}(G_RK_R)
\le
\frac{C_{\rm src}}{\Lambda_N^\Omega}
+
\operatorname{tr}(T_NK_R).
\]

Thus the completed residual budget collapses if \(\Lambda_N^\Omega\to\infty\) and the tail is exhaustive.

## Moving-window warning

If the finite windows pass but

\[
\liminf_N\operatorname{tr}(T_NK_R)>0,
\]

then the result remains support-only:

\[
\boxed{\texttt{moving\_window\_support\_only}.}
\]

This is the same fixed/exhaustive discipline established earlier in the membrane framework.

## Status

Step 144 does not close the RH route. It states the exact promotion gate needed after the finite \(\Omega\)-compatible restricted BPRZ source frame.

The next step is to instantiate \(H_R\), \(P_N\), \(T_N\), and \(K_R\) on the actual Burnol/Sonine residual carrier.
