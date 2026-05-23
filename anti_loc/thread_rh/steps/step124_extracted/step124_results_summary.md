# Step 124 results summary

## Main output

Step 124 proves the conductor-decoupled theorem shape:

\[
\frac{a+\alpha\tau}{\eta}+\frac{a}{\beta}<\theta_{\rm src}
\]

is exactly the power-law feasibility condition for choosing

\[
X_N=Q_N^x,\qquad R_N=Q_N^r
\]

so that the regularized Müntz/co-Poisson shadow is accurate and the effective Dirichlet length

\[
L_N\asymp X_NR_N
\]

remains short enough for the source family.

Equivalently, with \(Q_N=T_N^\omega\), the condition is

\[
\frac{a+\alpha/\omega}{\eta}+\frac{a}{\beta}<\theta_{\rm src}.
\]

So the route now explicitly prefers conductor decoupling:

\[
Q_N\gg T_N.
\]

## Finite source prototype

For a prime modulus \(q_N>L_N\), the complete Dirichlet character family gives an exact finite coefficient frame:

\[
\sum_{\chi\bmod q_N}\left|\sum_{n\in\mathcal N_N}a_n\chi(n)\right|^2
=
\varphi(q_N)\sum_{n\in\mathcal N_N}|a_n|^2.
\]

This supplies a clean finite-model lower frame, but it is not yet a completed RH source theorem.

## Source route after Step 124

The residual source route now has the form

\[
G_{\mathcal X,N}\succeq\gamma_NH_N,
\]

\[
c_{{\rm hyb},N}
\ge
1-(\epsilon_{B,N}+\epsilon_{{\rm Mell},N}+\tau_{M,N}+\kappa_{{\rm tail},N})^2,
\]

and hence

\[
R_N^*G_{\mathcal X,N}R_N
\succeq
\gamma_Nc_{{\rm hyb},N}G_{R,N}.
\]

The route requires

\[
\gamma_Nc_{{\rm hyb},N}\to\infty
\]

plus fixed/exhaustive tail promotion.

## Strategic conclusion

The same-aspect route is likely too tight. The clean next strategy is to use conductor aspect as slack:

\[
T_N \text{ controls the vertical Burnol/Müntz window},
\]

\[
Q_N \text{ controls the arithmetic source family},
\]

with \(Q_N\) allowed to grow faster.

The finite Dirichlet character frame is exact when the conductor exceeds the coefficient support. The hard arithmetic input is the weighted/mollified **matrix lower moment**, not scalar moment lower bounds.
