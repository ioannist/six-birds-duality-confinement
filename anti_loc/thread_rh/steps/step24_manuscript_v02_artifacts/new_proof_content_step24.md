# New proof content in Step 24

Step 24 is not only a manuscript update. It adds the following proof content to the integrated draft.

## 1. Probe-family currency theorem

Scalar capacity is extended to a declared native probe family \(L:H\to Y\). The central object is

\[
\mathsf K=L_\Gamma C_\Gamma^\dagger L_\Gamma^*.
\]

For every recombination \(y\),

\[
\operatorname{Cap}(y^*L)=y^*\mathsf K y.
\]

This proves that the only correct family-level anti-localization condition is a PSD matrix bound.

## 2. Minimum-spend theorem

For a desired probe-family response \(z\),

\[
\inf_{L_\Gamma a=z} a^*C_\Gamma a=z^*\mathsf K^\dagger z.
\]

This makes the currency interpretation exact: \(\mathsf K\) is compliance/shadow value, \(\mathsf K^\dagger\) is resistance/minimum spend.

## 3. Family Schur square

The block matrix

\[
\begin{pmatrix}
\Theta & L_\Gamma\\
L_\Gamma^* & C_\Gamma
\end{pmatrix}
\]

is positive semidefinite iff null-mode legality holds and \(\mathsf K\preceq\Theta\). This is the family version of Schur anti-localization.

## 4. Family semigroup and dual-witness controls

The operator identity

\[
\mathsf K=\int_0^\infty L_\Gamma e^{-tC_\Gamma}L_\Gamma^*\,dt
\]

upgrades scalar probe persistence to family persistence. A factorization \(L_\Gamma=WB_\Gamma\) gives

\[
\mathsf K\preceq WW^*.
\]

## 5. Compression DPI

For a compressed feasible subspace \(V\subset H\),

\[
\mathsf K_V\preceq \mathsf K_H.
\]

Equality requires the ambient minimum-energy representers to lie in the compressed carrier. This is the formal version of the ambient/public-shadow overread warning.

## 6. Closure-only no-native-needle theorem

If a formed closure satisfies

\[
\mathsf K\preceq\Theta,
\]

then no declared native recombination needle exists. The theorem explicitly does not apply to non-closed artifacts or undeclared probes.
