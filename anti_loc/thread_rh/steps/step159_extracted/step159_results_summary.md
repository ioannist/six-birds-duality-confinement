# Step 159: Boundary-Weyl Inclusion / Avoidance Theorem for H_eta

## Orientation

Adequacy-oriented track:

\[
\Xi^{BC}\to0
\]

is good. Robust positive residual is missed adequacy.

Typed context:

\[
H_\eta=\overline{\operatorname{span}\{\eta^a_{\rho,k}\}},
\qquad
\eta^a_{\rho,k}=J_a^*Y^a_{\rho,k},
\]

inside the Burnol/Sonine pulled-evaluator carrier, with Calkin comparison.

## Main object

The active residual remains

\[
\Xi^{BC}_{\ell,a}=\mathfrak B_{\ell,a}^*\Pi_{Y_a}\mathfrak B_{\ell,a}.
\]

The projected commutator block is

\[
C_\ell=(I-P_\infty)M_{m_\ell}P_\infty,
\qquad
m_\ell(s)=e^{-\ell(1/2-s)}.
\]

The compact/tail question is exactly

\[
C_\ell P_\eta\stackrel{?}{\in}\mathcal K.
\]

## Main theorem

If there is a Calkin-faithful boundary-symbol factorization

\[
C_\ell=U_\ell W_\ell+K_\ell,
\qquad K_\ell\in\mathcal K,
\]

with \(U_\ell\) bounded below on the boundary-symbol range, then:

1. If

\[
W_\ell P_\eta\in\mathcal K,
\]

then

\[
C_\ell P_\eta\in\mathcal K.
\]

So \(\Xi^{BC}\) is compact/tail-payable.

2. If there is a normalized weak-null sequence

\[
u_n\in H_\eta,
\qquad
u_n\rightharpoonup0,
\qquad
\liminf\|W_\ell u_n\|>0,
\]

then

\[
\|C_\ell P_\eta\|_{ess}>0.
\]

So \(\Xi^{BC}\) is genuinely noncompact.

## Verdict

Step 159 does **not** prove compactness or noncompactness on the Burnol/Sonine carrier.

It reduces the question to a precise boundary-Weyl sub-residual:

\[
\Xi^{BW}_{\ell,a}=P_\eta W_\ell^*W_\ell P_\eta.
\]

If this is compact/tail-small, \(\Xi^{BC}\) may be compact/tail-payable.

If this has essential mass, \(\Xi^{BC}\) is a genuine noncompact adequacy residual.

## Hard-support shadow

The hard-support model gives a clear noncompact Weyl sequence, but its status is only:

`public_shadow`

until a Calkin-faithful bridge to the actual Burnol/Sonine commutator is proved.

## Bottom line

\[
\boxed{\text{Step 159 turns }\Xi^{BC}\text{ into a boundary-Weyl bridge problem.}}
\]

The next step is:

\[
\boxed{\textbf{Step 160: Calkin-faithful boundary-symbol bridge for }C_\ell.}
\]
