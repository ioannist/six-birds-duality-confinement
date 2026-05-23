# Step 67: Zero-Ledger Visibility and Exhaustivity

This step formalizes when an asymptotic anti-invariant budget proves exact zero confinement.

## Main theorem

If a single completed zero-side ledger satisfies

\[
\mathsf A_Z\preceq B_n\quad\forall n,
\qquad
\operatorname{tr}B_n\to0,
\]

then

\[
\mathsf A_Z=0.
\]

If the anti-invariant readout separates the fixed locus of the anti-linear involution, then all visible positive-weight roots lie on the fixed locus.

## Exhaustive-ledger version

If finite zero windows satisfy

\[
\mathsf A_Z\preceq \iota_n\mathsf A_{Z,n}\iota_n^*+T_n,
\qquad
\mathsf A_{Z,n}\preceq B_n,
\]

and

\[
\operatorname{tr}(\iota_nB_n\iota_n^*)+\\operatorname{tr}T_n\to0,
\]

then again

\[
\mathsf A_Z=0.
\]

## Moving-ledger warning

If every stage squeezes only a moving finite ledger with no completed/tail record, the status is only:

`moving_ledger_support_only`.

A hidden zero-side tail can remain even while all finite visible budgets tend to zero.

## RH-facing criterion

For the root-composite RH route, the obstruction budget is

\[
B_n(t)=(1+t)(\Lambda_n^{-1}\Theta_0^-+E_{{\rm src},n})+(1+t^{-1})E_{{\rm EF},n}.
\]

Exact confinement follows if this budget squeezes a fixed/exhaustive zero ledger and

\[
\operatorname{tr}B_n(t_n)\to0.
\]

Optimizing over \(t\), the trace budget is

\[
(\sqrt{a_n}+\sqrt{b_n})^2,
\]

where

\[
a_n=\operatorname{tr}(\Lambda_n^{-1}\Theta_0^-+E_{{\rm src},n}),
\qquad
b_n=\operatorname{tr}E_{{\rm EF},n}.
\]

## Bottom line

Finite termination is sufficient but not necessary. Infinite decay proves exact confinement only if it squeezes a fixed completed zero ledger or an exhaustive partial ledger with vanishing tail.
