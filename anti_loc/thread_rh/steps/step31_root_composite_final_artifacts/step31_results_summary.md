# Step 31 — Root-Composite / Algebraic-Extension Anti-Localization Profile

## Main point

This step adds the missing SAU/root-composite profile to the anti-localization theory.  The key idea is that an algebraic extension may contain branch/root probes that are not native to the base closure.  The base closure sees only declared descended probes: trace, invariant, norm, or coefficient data.

Thus algebraic anti-localization is not:

\[
\text{all extension roots/branches have no needles}.
\]

It is:

\[
\text{all native descended algebraic observables of the formed closure have finite audited prices}.
\]

## Core theorem

Given an extension-level probe family

\[
\widetilde L:E\to \widetilde Y,
\]

a descent map

\[
D:\widetilde Y\to Y,
\]

and base-visible probe family

\[
L=D\widetilde L,
\]

the extension currency is

\[
\widetilde K=\widetilde L C_E^\dagger \widetilde L^*,
\]

and the descended base currency is exactly

\[
\boxed{K_D=D\widetilde K D^*.}
\]

So if

\[
\widetilde K\preceq\widetilde\Theta,
\]

then

\[
K_D\preceq D\widetilde\Theta D^*.
\]

This is the trace/invariant descent theorem.

## Nonlinear algebraic maps

For norm and coefficient maps, the anti-localization object is tangent-linearized.

If

\[
F:\widetilde Y\to Y
\]

is differentiable at a background response \(\bar r\), then

\[
K_F=dF_{\bar r}\,\widetilde K\,dF_{\bar r}^*.
\]

This covers:

- norm/log-norm descent,
- coefficient descent from roots to polynomial coefficients,
- characteristic-polynomial descent,
- trace-type invariant descent.

## Discriminant gate

For roots \(r_i\), coefficient descent is safe, but lifting coefficient anti-localization back to labeled root anti-localization is not safe near root collisions.

For a quadratic,

\[
(a,b)=(-r_1-r_2,r_1r_2),
\]

with Jacobian

\[
J=\begin{pmatrix}-1&-1\\ r_2&r_1\end{pmatrix},
\qquad
\det J=r_2-r_1.
\]

Thus the lift from coefficients to roots blows up like

\[
|r_1-r_2|^{-1}.
\]

A coefficient-level anti-localization bound does not imply branch/root anti-localization without a discriminant/separation record.

## Closure-only scope

The theorem is base-closure relative.

If the formed closure sees only invariant/trace/coefficient probes, then non-invariant branch needles are outside the claim unless a bridge declares them visible.

So the lawful statement is:

\[
D\widetilde K D^*\preceq\Theta
\Rightarrow
\text{no native descended recombination needles}.
\]

The unlawful overread is:

\[
D\widetilde K D^*\preceq\Theta
\Rightarrow
\widetilde K\preceq\widetilde\Theta.
\]

## Numerical sanity checks

1. Random trace-descent checks verified

\[
K(D\widetilde L)=D\widetilde K D^*
\]

up to numerical precision.

2. Invariant-vs-branch checks showed that base trace capacity can stay fixed while a non-native anti-invariant branch sector becomes arbitrarily large.

3. Quadratic coefficient-to-root lifting showed capacity blowup as the discriminant tends to zero.

## RH relevance

This does not prove RH.  It suggests that the RH anti-localization mechanism may not be purely harmonic.  If the completed zeta carrier is naturally a root/composite object, the lawful anti-localization statement may live on trace/norm/coefficient/invariant descents of the zero/root extension, not on individually labeled branch probes.

The RH obligation becomes:

\[
\text{identify the algebraic extension carrier, its descent map, and prove the descended currency bound.}
\]

