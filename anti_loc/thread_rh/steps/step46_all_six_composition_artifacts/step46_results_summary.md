# Step 46: All-Six Record Composition and Propagation

## Result

This step proves that accepted anti-localization membranes compose only through all-six bridges whose currency maps, budgets, channel records, and defects compose explicitly.

For a membrane record

\[
\mathsf{AL}=(E,C,L,Y,\Theta,P_1,\ldots,P_6),
\]

the currency matrix is

\[
K=LC^\dagger L^*.
\]

An exact bridge from \(\mathsf{AL}\) to \(\mathsf{AL}'\) consists of a carrier map \(P:E'\to E\) and response map \(A:Y\to Y'\) such that

\[
C'\succeq P^*CP,
\qquad
L'=ALP.
\]

Then

\[
K'\preceq AKA^*.
\]

Thus if

\[
K\preceq\Theta,
\qquad
A\Theta A^*\preceq\Theta',
\]

then

\[
K'\preceq\Theta'.
\]

## Defective transfer

If

\[
L'=ALP+R,
\qquad
R(C')^\dagger R^*\preceq E_B,
\]

then for every \(t>0\),

\[
K'\preceq (1+t)AKA^*+(1+t^{-1})E_B.
\]

So defects are allowed only when explicitly paid in the response-side budget.

## Composition law

For two bridges

\[
\mathsf{AL}_1\to\mathsf{AL}_2\to\mathsf{AL}_3,
\]

with maps \(A_{12},A_{23}\) and defects \(E_{12},E_{23}\), the composed bridge has

\[
A_{13}=A_{23}A_{12},
\]

and

\[
E_{13}=A_{23}E_{12}A_{23}^*+E_{23}.
\]

Then

\[
K_3\preceq A_{13}K_1A_{13}^*+E_{13}.
\]

The same formula iterates along an arbitrary chain.

## All-six rule

A composed membrane is accepted only if every channel composes:

\[
P_1:\text{ rewrite/gauge},
\quad
P_2:\text{ feasibility},
\quad
P_3:\text{ route/holonomy},
\]

\[
P_4:\text{ staging/refinement},
\quad
P_5:\text{ packaging/canonicalization},
\quad
P_6:\text{ audit/currency}.
\]

Failure of one channel downgrades the composed membrane, even if the scalar matrix inequality appears to pass.

## Predictive propagation

If

\[
K_{j+1}\preceq (1+\varepsilon_j)K_j+D_j,
\]

with

\[
\prod_j(1+\varepsilon_j)\le P<\infty,
\qquad
\sum_jD_j\preceq D_\infty,
\]

and

\[
P(K_0+D_\infty)\preceq\Theta,
\]

then

\[
K_j\preceq\Theta
\]

for all accepted stages.

## Nonclaim

A public shadow membrane does not imply an intrinsic membrane. If \(F:Y\to Z\) forgets hidden response directions, then \(FKF^*\preceq F\Theta F^*\) may hold while \(K\npreceq\Theta\). Promotion requires a reconstruction bridge or an explicit hidden-direction defect.

## Interpretation

A membrane is not a static number. It is a transportable all-six record. It can move across bridges and strict extensions only when energy, readout, route, stage, package, and audit defects are all accounted for.
