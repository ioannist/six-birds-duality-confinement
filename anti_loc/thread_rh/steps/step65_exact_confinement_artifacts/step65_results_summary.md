# Step 65: Exact Confinement Versus Asymptotic Budgets

This step answers the asymptotic-vs-exact concern.

## Key conclusion

Finite termination is **not necessary** for exact confinement. An infinite strict-extension ladder is enough if it gives a **fixed-ledger squeeze**:

\[
A_Z \preceq B_n, \qquad B_n\to 0
\]

for the same zero-side anti-invariant displacement matrix \(A_Z\). Then \(A_Z=0\).

What is insufficient is merely:

\[
K_n=1+1/n \downarrow 1
\]

or any moving finite-stage defect that improves forever but never gives a fixed-object squeeze or finite acceptance.

## Theorem

If

\[
A_Z\preceq
(1+t_n)(\Lambda_n^{-1}\Theta_0^-+E_{{\rm src},n})
+(1+t_n^{-1})E_{{\rm EF},n}
\]

and the trace of the right-hand side tends to zero, then

\[
A_Z=0.
\]

If the anti-invariant zero readout separates the fixed locus, the visible zero/root mass lies on the fixed locus.

For RH, the fixed locus of

\[
J(s)=1-\bar{s}
\]

is

\[
\Re(s)=1/2.
\]

So a fixed/exhaustive root-composite squeeze would give exact critical-line confinement.

## Optimized obstruction budget

Let

\[
a_n=\operatorname{tr}(\Lambda_n^{-1}\Theta_0^-+E_{{\rm src},n}),
\qquad
b_n=\operatorname{tr}E_{{\rm EF},n}.
\]

Then

\[
\inf_{t>0}\operatorname{tr}B_n=(\sqrt{a_n}+\sqrt{b_n})^2.
\]

Thus exact confinement follows if

\[
a_n\to0, \qquad b_n\to0.
\]

## Important distinction

The monotone nonterminating example

\[
K_n=1+1/n,\qquad \Theta=1
\]

shows that decreasing defect is not finite completion.

But it does **not** refute exact confinement from an infinite squeeze. If a fixed positive object satisfies

\[
A\preceq 1/n
\]

for every \(n\), then \(A=0\).

## Moving-ledger warning

If the ladder only proves

\[
A_{Z,n}\preceq B_n, \qquad B_n\to0,
\]

for moving or truncated ledgers \(A_{Z,n}\), exact confinement of the full \(A_Z\) requires tail/exhaustivity:

\[
A_Z\preceq A_{Z,n}+T_n,
\qquad
\operatorname{tr}(B_n+T_n)\to0.
\]

Without that, the proof may squeeze the visible part while missing hidden zeros/tails.

## Bottom line

The real RH question is not simply:

> Does the strict-extension ladder terminate?

It is:

> Does the ladder produce a fixed or exhaustive zero-ledger squeeze with vanishing EF/source defects?

Finite termination is one route. Infinite exact squeezing is another. Mere asymptotic finite-stage improvement is not enough.
