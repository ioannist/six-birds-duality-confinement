# Step 24: Manuscript v0.2 with probe-family currency integrated

## Purpose

This step updates the manuscript only because Step 23 created real proof content that needed to become central. The main additions are not cosmetic:

1. The scalar capacity theory is upgraded to a finite probe-family currency theorem.
2. Anti-localization is now stated as a matrix inequality, not a list of scalar probe bounds.
3. The minimum-spend duality theorem identifies the pseudoinverse of the currency matrix as the resistance/price matrix.
4. A family Schur square is added.
5. A compression data-processing inequality is added: compressed capacity is bounded by ambient/public-shadow capacity, with an equality condition.
6. The closure-only no-native-needle theorem is made explicit.

## Main new theorem stack

For a formed closure with exact package \(\Gamma:E\to H\), audit energy \(C\succeq0\), and declared native probe family \(L:H\to Y\), set

\[
C_\Gamma=\Gamma^*C\Gamma,\qquad L_\Gamma=L\Gamma.
\]

The probe-family currency matrix is

\[
\mathsf K_{C,\Gamma}(L)=L_\Gamma C_\Gamma^\dagger L_\Gamma^*.
\]

For every recombination \(y\in Y\),

\[
\operatorname{Cap}_C(y^*L;\operatorname{Ran}\Gamma)
= y^*\mathsf K_{C,\Gamma}(L)y.
\]

A formed closure is family anti-localized when

\[
\mathsf K_{C,\Gamma}(L)\preceq \Theta.
\]

The reciprocal minimum-spend theorem says that for a desired response \(z\in Y\),

\[
\operatorname{Cost}_C(z;L,\Gamma)=z^*\mathsf K_{C,\Gamma}(L)^\dagger z.
\]

The family Schur square is

\[
\begin{pmatrix}
\Theta & L_\Gamma\\
L_\Gamma^* & C_\Gamma
\end{pmatrix}\succeq0
\quad\Longleftrightarrow\quad
\mathsf K_{C,\Gamma}(L)\preceq\Theta
\]

under null-mode legality.

## New DPI result

For a compressed feasible subspace \(V\subset H\),

\[
\mathsf K_V\preceq \mathsf K_H.
\]

This is the formal version of the lawful-witness/public-shadow warning: ambient capacity can support or upper-bound, but the compressed carrier is the lawful object unless a reducing/equality bridge is audited.

## Closure-only scope

The theorem now explicitly claims no needles only for formed closures/layers. Non-closed artifacts, raw substrates, undeclared probes, and public shadows are outside scope.

## Files

- `anti_localization_manuscript_step24.tex`: integrated v0.2 manuscript.
- `new_proof_content_step24.md`: standalone explanation of the new proof content.
- `theorem_stack_step24.csv`: theorem stack and statuses.
- `audit_gate_table_step24.csv`: accepted test-family gates.
- `step24_manuscript_v02_artifacts.zip`: complete artifact bundle.
