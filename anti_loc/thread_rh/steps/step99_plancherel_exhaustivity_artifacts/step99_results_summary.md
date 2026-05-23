# Step 99: Semilocal Plancherel/Exhaustivity Record

## Purpose
Step 99 formalizes the promotion gate between finite character orthogonality and a completed anti-invariant lower frame for the RH source-coercivity route.

Finite character families are exact tight frames on finite abelian quotients, but RH needs a lower frame on the completed anti-invariant response space. The missing record is Plancherel/exhaustivity plus a vanishing tail.

## Main theorem
Let

\[
\Pi_n:Y^-_{\rm H}\to Y^-_n
\]

be a finite conductor/place/spectral window and let

\[
F_n^{\rm win}\succeq \Lambda_n B_n
\]

be the finite window source lower frame. If the completed response space has an exhaustivity record

\[
(\Theta_0^-)^{-1}\preceq \Pi_n^*B_n\Pi_n+T_n,
\]

then the lifted frame satisfies

\[
F_n+\Lambda_nT_n\succeq \Lambda_n(\Theta_0^-)^{-1}.
\]

Equivalently,

\[
F_n\succeq \Lambda_n(\Theta_0^-)^{-1}-\Lambda_nT_n.
\]

So finite character frames promote only with an explicit tail form.

## Completed Plancherel version
If the completed Hecke/idèle response admits a Plancherel decomposition

\[
Y^-_{\rm H}\cong\int_\Omega^\oplus Y^-_\omega\,d\mu_{\rm Pl}(\omega),
\]

and finite windows \(P_n\) increase to the identity with tail condition

\[
\operatorname{tr}((I-P_n)A_Z(I-P_n))\to0,
\]

then finite-window lower frames are exhaustive for the zero ledger. With \(\Lambda_n\to\infty\), vanishing source defects, and source absorption of \(\Delta_S^+\), the anti-invariant budget collapses.

## Key warning
Strong or finite-window convergence is not enough by itself. The proof needs fixed/exhaustive ledger promotion. Otherwise the status is:

`moving_window_support_only`.

## Relation to literature
The Connes--Consani--Moscovici semilocal Hardy--Titchmarsh transform supplies the response geometry: finite local Euler factors enter the transform and the measure \(dm_S\). Zeta spectral triples and chiral adelic Dirac models provide strong finite-window/truncation evidence, but both still need convergence/tail/descent records to become full zeta proofs.

## Bottom line
The RH source route now requires:

\[
\text{finite character orthogonality}
+
\text{completed Plancherel/exhaustivity}
+
\text{lower-frame growth}
+
\text{vanishing tail}.
\]
