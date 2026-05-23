# Step 155: Xi^BC residual classification

## Main verdict

The active Burnol/co-Poisson residual is

\[
\Xi^{\rm BC}_{\ell,a}=\mathfrak B_{\ell,a}^*\Pi_{Y_a}\mathfrak B_{\ell,a}\succeq0.
\]

It is not currently closed.

Step 155 classifies the lawful possibilities:

1. **Exact exclusion**: \(\Xi^{\rm BC}=0\).
2. **Compact/tail payment**: \(\Xi^{\rm BC}\) is compact, trace-class, or tail-vanishing on a fixed/exhaustive ledger.
3. **Non-circular source absorption**: a signed/direct source identity pays \(\Xi^{\rm BC}\) without using the blocked positive source-budget squeeze.
4. **Scoped nonclaim**: \(\Xi^{\rm BC}\) remains an active adequacy residual.

The current status is the fourth.

## Active formula

With

\[
C_\ell=(I-P_\infty)M_{m_\ell}P_\infty,
\qquad
m_\ell(s)=e^{-\ell(1/2-s)},
\]

and pulled Burnol zero-evaluators

\[
\eta^a_{\rho,k}=J_a^*Y^a_{\rho,k},
\]

the residual kernel is

\[
\mathcal R_\ell((\rho,k),(z,j))
=\langle C_\ell\eta^a_{\rho,k},C_\ell\eta^a_{z,j}\rangle.
\]

Direct residual exclusion is equivalent to

\[
C_\ell\eta^a_{\rho,k}=0
\quad\forall \rho,k.
\]

This is not forced by the raw log shift.

## Why the positive source route is blocked

If

\[
F_N^\Omega\succeq\Lambda_N^\Omega G_R,
\qquad
\Lambda_N^\Omega\to\infty,
\]

and \(K_R^\omega\succeq0\) is a fixed positive ledger, then

\[
\frac{\operatorname{tr}(F_N^\Omega K_R^\omega)}{\Lambda_N^\Omega}
\ge
\operatorname{tr}(G_RK_R^\omega).
\]

Therefore the desired source budget

\[
\operatorname{tr}(F_N^\Omega K_R^\omega)=o(\Lambda_N^\Omega)
\]

already implies residual collapse. It is not an independent side estimate.

## Current route status

- Exact exclusion: open, not earned.
- Compact/tail payment: open, not earned.
- Positive source-frame absorption: blocked unless replaced by a non-circular signed/direct mechanism.
- Scoped residual: currently active.

## Next step

Step 156 should classify the residual kernel

\[
\mathcal R_\ell((\rho,k),(z,j))
\]

as compact/tail-payable or genuinely noncompact on the pulled zero-evaluator family.
