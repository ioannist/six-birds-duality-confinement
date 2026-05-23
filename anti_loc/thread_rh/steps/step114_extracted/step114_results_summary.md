# Step 114: Boundary-to-Co-Poisson Inclusion Test

## Verdict

The desired inclusion

\[
\mathcal B_a \subseteq P_a
\]

is **not proved** in this step. It is reduced to a precise Burnol-native annihilation condition.

For a shifted boundary block

\[
\mathfrak B_\ell = J_aP_\infty\tau_\ell(I-P_\infty),
\]

where \(J_a\) transports the semilocal/archimedean Sonin model into Burnol's \(L_a\) carrier, the inclusion

\[
\operatorname{Ran}\mathfrak B_\ell\subseteq P_a
\]

holds if and only if

\[
\Pi_{Y_a}\mathfrak B_\ell=0.
\]

Equivalently,

\[
M(\mathfrak B_\ell u)^{(k)}(\rho)=0
\]

for every legal input \(u\), every nontrivial zero \(\rho\), and every \(0\le k<m_\rho\).

## Main reduction

Burnol gives

\[
P_a=Y_a^\perp
\]

for \(a<1\), where \(Y_a\) is the closed span of the zeta zero-evaluator vectors \(Y^a_{\rho,k}\). Therefore boundary-to-co-Poisson inclusion is exactly zero-evaluator annihilation.

## Zeta-factorization sufficient route

A strong sufficient certificate is:

\[
M(\mathfrak B_\ell u)(s)=\zeta(s)\alpha_{\ell,u}(s)
\]

with all Burnol support, pole, endpoint, and trivial-zero records. This would force every zero-evaluator to vanish on \(\mathfrak B_\ell u\).

Raw shifted Sonin/prolate blocks do not currently exhibit this factorization. So the inclusion is not automatic.

## Residual if inclusion fails

The exact residual is

\[
\Xi^{\rm BC}_{\ell,a}
=
\mathfrak B_\ell^*\Pi_{Y_a}\mathfrak B_\ell\succeq0.
\]

This is the boundary-to-co-Poisson adequacy residual. If it is nonzero, the Burnol/co-Poisson atom family does not see the whole boundary-packet sector.

## Consequence

The next load-bearing theorem must be one of:

1. prove zeta-factorization of the transported shifted boundary packets;
2. prove direct zero-evaluator annihilation;
3. accept the residual and source-absorb it via Hecke/Dirichlet lower frames.

## Strategic status

The current likely status is:

\[
\boxed{\text{inclusion unearned; residual must be measured or source-absorbed}.}
\]

This keeps the source-coercivity route active.
