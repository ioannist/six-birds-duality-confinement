# Step 51: Proof Tightening Pass

This step tightens three weak proof points in the integrated membrane manuscript and updates the title/scope.

## 1. Singular minimum-spend duality

The minimum-spend theorem now works on the legal energy quotient. If `C >= 0`, write `E0 = ker(C)^perp` and `C0 = C|E0 > 0`. Under null-mode legality `L ker(C)=0`,

\[
\operatorname{Cost}_C(z;L)=
\begin{cases}
 z^*(L_0C_0^{-1}L_0^*)^\dagger z, & z\in\operatorname{Ran} L_0,\\
 +\infty, & z\notin\operatorname{Ran} L_0.
\end{cases}
\]

The warning is explicit: if a probe sees a legal zero-energy direction, pseudoinverse currency can hide a fake zero while the variational capacity is infinite.

## 2. Adequacy residual \(\Xi_C(D\mid L)\)

The residual now has its own standalone theorem. On the legal quotient,

\[
\Xi_C(D\mid L)=K_{DD}-K_{DL}K_{LL}^\dagger K_{LD}.
\]

For every map `A`,

\[
(D-AL)C^\dagger(D-AL)^*
=\Xi_C(D\mid L)+(A-A_*)K_{LL}(A-A_*)^*,
\qquad A_*=K_{DL}K_{LL}^\dagger.
\]

Thus \(\Xi\) is the unique Loewner-minimal blind-spot currency. Exact adequacy is now precise:

\[
\Xi_C(D\mid L)=0
\Longleftrightarrow
D=AL\text{ on the legal quotient}
\Longleftrightarrow
\ker L\subseteq\ker D.
\]

Adding native probes monotone decreases \(\Xi\). Repeating the same native family does not.

## 3. All-six acceptance wording

The manuscript now separates mathematical membrane equivalence from Six Birds acceptance.

Mathematical equivalence:

\[
K\preceq\Theta
\Longleftrightarrow
\text{no unresolved native recombination witness}.
\]

Six Birds acceptance:

\[
\text{accepted all-six record}
\Longrightarrow
K\preceq\Theta.
\]

The reverse is not valid unless all gate records are supplied. Without gates, the honest status is support-only, local-only, native-only, public-shadow-only, or failed-audit.

## 4. Title update

The draft is retitled:

**Formed-Layer Membrane Theory: Anti-Localization, Adequacy, and the Root-Composite Obligation**

This matches the evolved framework: anti-localization is one consequence of a broader formed-layer membrane theory.
