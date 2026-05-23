
# Step 157: Calkin-Level Pulled-Evaluator Avoidance Audit

## Orientation

Adequacy-oriented.  The residual

\[
\Xi^{\rm BC}_{\ell,a}=\mathfrak B_{\ell,a}^*\Pi_{Y_a}\mathfrak B_{\ell,a}
\]

is bad news unless it is exact, compact/tail-paid, Schatten-paid, or explicitly budgeted.

## Main object

The shifted Sonine/prolate commutator block is

\[
C_\ell=(I-P_\infty)M_{m_\ell}P_\infty,
\qquad m_\ell(s)=e^{-\ell(1/2-s)}.
\]

The pulled evaluator span is

\[
H_\eta=\overline{\operatorname{span}\{\eta^a_{\rho,k}\}},
\qquad \eta^a_{\rho,k}=J_a^*Y^a_{\rho,k},
\]

and the Calkin-level object is

\[
\boxed{\mathfrak c_{\ell,\eta}=q(C_\ell P_\eta)\in\mathcal B(H)/\mathcal K(H).}
\]

The active question is

\[
\boxed{[C_\ell]P_\eta\stackrel{?}{=}0.}
\]

## Calkin avoidance theorem

The following are equivalent:

\[
[C_\ell]P_\eta=0,
\]

\[
C_\ell P_\eta\in\mathcal K(H),
\]

\[
\forall u_n\in H_\eta,
\quad \|u_n\|\le1,
\quad u_n\rightharpoonup0
\Rightarrow
\|C_\ell u_n\|\to0,
\]

and for a finite-rank exhaustion \(Q_N\uparrow P_\eta\),

\[
\|C_\ell(P_\eta-Q_N)\|\to0.
\]

So compact/tail-payment of \(\Xi^{\rm BC}\) is exactly a Calkin-vanishing theorem.

## Weyl-sequence obstruction

A noncompactness certificate is a pulled-evaluator Weyl sequence:

\[
\|u_n\|=1,
\qquad u_n\in H_\eta,
\qquad u_n\rightharpoonup0,
\qquad \liminf_n\|C_\ell u_n\|>0.
\]

Such a sequence proves

\[
\|C_\ell P_\eta\|_{\rm e}>0.
\]

## Main verdict

Step 157 does **not** prove compactness and does **not** prove noncompactness.

It converts the question into a precise Calkin alternative:

\[
\boxed{C_\ell P_\eta\in\mathcal K(H)}
\]

or

\[
\boxed{\|C_\ell P_\eta\|_{\rm e}>0.}
\]

Finite-window singular-value plots are diagnostic only.  They are not completed-carrier proof.

## Route status

| status | condition | current state |
|---|---|---|
| exact | \(C_\ell P_\eta=0\) | not proved |
| compact/tail-payable | \(C_\ell P_\eta\in\mathcal K\) | not proved |
| Schatten-payable | \(C_\ell\widetilde E\in\mathcal S_{2p}\) | not proved |
| Calkin obstruction | \(\|C_\ell P_\eta\|_e>0\) | not proved |
| active residual | no accepted exact/compact/obstruction record | active |

## Next step

**Step 158: pulled-evaluator Weyl sequence / essential-symbol test.**

Target: either prove compactness via a Sonine/prolate Calkin theorem or construct a Weyl sequence in the pulled evaluator span showing nonzero essential residual.
