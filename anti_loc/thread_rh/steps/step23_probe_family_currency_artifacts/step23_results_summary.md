# Step 23 — Probe-Family Currency Theorem

## What changed

This step upgrades anti-localization from scalar probe capacity to finite probe-family currency.

A formed closure/layer is now tested by a declared native probe family

\[
L:H\to Y,
\]

not just a single probe.  On the exact packaged carrier \(\mathcal F=\operatorname{Ran}\Gamma\), define

\[
C_\Gamma=\Gamma^*C\Gamma,
\qquad
L_\Gamma=L\Gamma.
\]

The central object is the family capacity / compliance / shadow-value matrix

\[
\boxed{
\mathsf K_{C,\Gamma}(L)=L_\Gamma C_\Gamma^\dagger L_\Gamma^*.
}
\]

## Main theorem

For every recombination vector \(y\in Y\), the scalar probe \(\ell_y(u)=\langle y,Lu\rangle\) has capacity

\[
\boxed{
\operatorname{Cap}_C(\ell_y;\operatorname{Ran}\Gamma)
=
y^*\mathsf K_{C,\Gamma}(L)y.
}
\]

Thus family anti-localization is the matrix inequality

\[
\boxed{
\mathsf K_{C,\Gamma}(L)\preceq\Theta.
}
\]

This controls all declared recombinations, not only the original listed probes.

## Currency / minimum-spend theorem

For a desired response \(z\in Y\), define the minimum audit spend

\[
\operatorname{Cost}_C(z;L,\Gamma)
=
\inf\{a^*C_\Gamma a: L_\Gamma a=z\}.
\]

Then, when \(z\in\operatorname{Ran}L_\Gamma\),

\[
\boxed{
\operatorname{Cost}_C(z;L,\Gamma)=z^*\mathsf K^\dagger z.
}
\]

So \(\mathsf K\) is the compliance/shadow-value matrix, and \(\mathsf K^\dagger\) is the resistance/minimum-price matrix.

## Family Schur square

The family version of the Schur wall is

\[
\begin{pmatrix}
\Theta & L_\Gamma\\
L_\Gamma^* & C_\Gamma
\end{pmatrix}
\succeq 0
\]

if and only if

\[
\mathsf K_{C,\Gamma}(L)\preceq\Theta
\]

with null-mode legality.

## Recombination countermodel

Take

\[
H=\mathbb C,
\qquad C=1,
\qquad Lu=u(1,\ldots,1).
\]

Then

\[
\mathsf K=\mathbf 1\mathbf 1^*.
\]

Every coordinate probe has scalar capacity \(1\), but the normalized all-ones recombination has capacity \(m\).

Therefore diagonal scalar bounds are not family anti-localization.

## Closure-only scope

This theorem is intentionally scoped to formed closures/layers only.

A non-closed artifact may contain needles.  It is outside the accepted anti-localization claim because it has not yet earned exact package, declared native probe family, null-mode legality, and audit budget.

The closure-layer theorem says:

\[
\boxed{
\text{formed closure} + \mathsf K\preceq\Theta
\Rightarrow
\text{no native recombination needles.}
}
\]

## Layman interpretation

A layer has many ways it can be addressed.  Checking one address at a time is not enough, because safe-looking addresses can be combined into an unsafe address.

The matrix \(\mathsf K\) is the price table for the whole address system.  Its diagonal prices the listed probes.  Its off-diagonal entries price recombinations.

A layer is anti-localized when every native address has a finite declared price.

A needle is an address that is too cheap.
