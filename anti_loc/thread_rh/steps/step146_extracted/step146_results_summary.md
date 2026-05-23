
# Step 146: Trace-Class Residual Ledger Theorem for `K_R`

## Verdict

The completed residual ledger

\[
K_R=\Pi_RK_Z\Pi_R
\]

is **not trace-class automatically**.

A lawful trace-class ledger is available only after declaring a positive weight schedule

\[
\omega_{\rho,k}>0
\]

and proving the evaluator-norm summability record

\[
\sum_{(\rho,k)}
\omega_{\rho,k}
(\Re\rho-1/2)^2
\|\Pi_RY^a_{\rho,k}\|^2<\infty.
\]

## Main theorem

Define

\[
(D_R^\omega h)_{\rho,k}
=
\sqrt{\omega_{\rho,k}}(\Re\rho-1/2)
\langle h,\Pi_RY^a_{\rho,k}\rangle.
\]

Then

\[
K_R^\omega=(D_R^\omega)^*D_R^\omega
\]

is trace-class iff

\[
D_R^\omega\in\mathcal S_2.
\]

Equivalently,

\[
\operatorname{tr}K_R^\omega
=
\sum_{(\rho,k)}
\omega_{\rho,k}
(\Re\rho-1/2)^2
\|\Pi_RY^a_{\rho,k}\|^2
<\infty.
\]

## Tail promotion

If

\[
K_R^\omega\in\mathcal S_1(H_R)
\]

and

\[
P_N\uparrow I_{H_R},
\]

then

\[
\operatorname{tr}((I-P_N)K_R^\omega(I-P_N))\to0.
\]

Thus the completed residual-tail term in Step 144 is paid.

## Separation

If every weight is strictly positive, the weighted ledger still separates visible off-critical residual zero directions:

\[
\operatorname{tr}K_R^\omega=0
\Rightarrow
\Re\rho=1/2
\]

for every zero direction visible in the residual carrier.

This is not RH yet. It is the residual-carrier statement. The route still needs adequacy: every off-critical zero probe must be visible in `H_R` or paid by a declared residual.

## Active next obligation

Choose a lawful weight schedule and prove an evaluator-norm envelope:

\[
\omega_{\rho,k}>0,
\qquad
\sum_{(\rho,k)}
\omega_{\rho,k}
(\Re\rho-1/2)^2
\|\Pi_RY^a_{\rho,k}\|^2<\infty.
\]

Recommended next step:

**Step 147: zero-evaluator norm envelope and weight schedule.**
