# Step 162: Calkin Algebra Declaration and Source-Theorem Extraction Audit

## Orientation

\[
\boxed{\text{adequacy-oriented}}
\]

The active residual remains

\[
\Xi^{\rm BC}_{\ell,a}
=
\mathfrak B_{\ell,a}^{*}\Pi_{Y_a}\mathfrak B_{\ell,a},
\]

and the active operator remains

\[
C_\ell P_\eta,
\qquad
C_\ell=(I-P_\infty)M_{m_\ell}P_\infty.
\]

## New declaration

Step 162 declares the typed Calkin context:

\[
\mathcal A_\eta=C^*(P_\infty,M_{m_\ell},P_\eta,I),
\qquad
\mathcal K_\eta=\mathcal A_\eta\cap\mathcal K(H),
\]

with active quotient object

\[
q_\eta(C_\ell P_\eta)\in\mathcal A_\eta/\mathcal K_\eta.
\]

This prevents promotion from Hardy, hard-support, or finite-section shadows
unless a bridge lands in this exact quotient context.

## Source extraction verdict

No audited source passes every extraction gate.  The missing theorem is now
split into precise sub-obligations:

1. source theorem in \(\mathcal A_\eta/\mathcal K_\eta\), or accepted bridge into it;
2. faithful boundary symbol \(\sigma_B\);
3. normal form \(C_\ell=U_\ell W_\ell+K_\ell\);
4. lower-faithfulness of \(U_\ell\) on the relevant boundary range;
5. compact remainder \(K_\ell\in\mathcal K(H)\).

Therefore the current status is

\[
\boxed{\texttt{split\_external\_theorem}.}
\]

## Framework outputs

Predictive structural content:

- public-shadow non-promotion verdict;
- finite-window Calkin blindness verdict.

Analytical structural content:

- typed Calkin algebra declaration;
- split external bridge theorem;
- public-shadow no-go;
- finite-window Calkin blindness no-go;
- conditional bridge normal-form theorem.

Organizational content:

- operator generator ledger;
- source theorem extraction table;
- bridge normal-form candidates;
- updated route and theorem maps.

## Current frontier

The branch is diagnostic-complete at the algebra/source-audit layer.  The next
proof-producing move is to prove one split theorem branch, construct a true
pulled-evaluator Weyl sequence, prove shifted co-Poisson factorization, or
carry \(\Xi^{\rm BC}\) as a scoped adequacy residual.
