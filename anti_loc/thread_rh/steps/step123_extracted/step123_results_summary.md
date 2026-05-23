# Step 123 — Balanced-Length Theorem

## Status
Completed.

## Core question
Can the regularized Müntz/co-Poisson shadow be accurate while the Dirichlet polynomial remains short enough for Heap–Soundararajan-style source estimates?

## Main answer
Conditionally yes, exactly when the required shadow length fits inside the short-polynomial range of the source method.

The route has an effective Dirichlet length

\[
L_N \asymp X_N R_N,
\]

where \(X_N\) is the Müntz smoothing length and \(R_N\) is the intrinsic Burnol/coefficient length of the atom window.

The source estimates are lawful only when

\[
L_N \le Q_N^{\theta_{\rm src}-o(1)}.
\]

The visibility errors are modeled by

\[
\tau_{M,N}\le C A_N(1+T_N)^\alpha X_N^{-\eta},
\]

and

\[
\epsilon_{{\rm Mell},N}+\kappa_{{\rm tail},N}\le C A_N R_N^{-\beta}.
\]

If

\[
T_N=Q_N^t,
\qquad
A_N\le Q_N^a,
\qquad
X_N=Q_N^x,
\qquad
R_N=Q_N^r,
\]

then the exact exponent compatibility condition is

\[
\boxed{
\frac{a+\alpha t}{\eta}+\frac{a}{\beta}<\theta_{\rm src}.
}
\]

Equivalently, we need room to choose

\[
x>\frac{a+\alpha t}{\eta},
\qquad
r>\frac{a}{\beta},
\qquad
x+r<\theta_{\rm src}.
\]

## Strategic meaning
The same-aspect route is likely underpowered if the available source method only supports very short Dirichlet polynomials. The viable direction is to decouple the source conductor scale \(Q_N\) from the vertical Müntz window \(T_N\), so that the conductor/aspect family gives more short-polynomial room than pure \(t\)-aspect averaging.

## Positive-floor refinement
Exact shadow completion is stronger than necessary. If

\[
\epsilon_{B,N}+\epsilon_{{\rm Mell},N}+\tau_{M,N}+\kappa_{{\rm tail},N}\le e<1,
\]

then

\[
c_{{\rm hyb},N}\ge1-e^2>0.
\]

Any source strength \(\gamma_N\to\infty\) then gives

\[
\gamma_Nc_{{\rm hyb},N}\to\infty.
\]

## New obstruction
The route now has a quantitative length-balancing gate:

> the Müntz shadow must be long enough to approximate \(\zeta(s)\), while the coefficient object must stay short enough for the source moment estimates.

This is where Burnol/co-Poisson readability and Heap–Soundararajan source strength become coupled.

## Next step
Step 124 should formulate the conductor-decoupled source theorem:

\[
Q_N\gg T_N,
\qquad
X_NR_N\le Q_N^{\theta_{\rm src}},
\qquad
G_{\mathcal X,N}\succeq\gamma_NH_N.
\]

Target: determine which Dirichlet/Hecke conductor family can supply the needed matrix lower frame without violating shortness.
