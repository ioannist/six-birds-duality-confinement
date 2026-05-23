# Step 25: Predictive Probe-Family Capacity

This step upgrades static probe-family anti-localization to predictive/refinement anti-localization.

## Main object

For each accepted refinement level `j`, define the transported family currency matrix

\[
\widehat K_j
=R_jL_j\Gamma_jC_{\Gamma,j}^{\dagger}\Gamma_j^*L_j^*R_j^*.
\]

Here:

- `Gamma_j` is the exact packaged carrier,
- `C_j` is the audit energy,
- `L_j` is the declared native probe family,
- `R_j` transports level-j responses into a common response space.

## Predictive anti-localization theorem

A predictive family certificate with budget \(\Theta\succeq0\) is

\[
\widehat K_j\preceq\Theta \qquad \text{for all accepted }j.
\]

This is equivalent to

\[
\sup_j y^*\widehat K_jy\le y^*\Theta y
\]

for every recombination vector \(y\). Thus a formed predictive closure has no native predictive recombination needles if and only if its transported family currency matrices admit a common Loewner budget.

## Summable defect theorem

If

\[
K_{j+1}\preceq (1+\varepsilon_j)K_j+D_j,
\]

with \(\prod_j(1+\varepsilon_j)<\infty\) and \(\sum_jD_j\preceq D_\infty\), then

\[
K_n\preceq P_\infty(K_0+D_\infty)
\]

for all \(n\). This gives a forward-stable predictive anti-localization budget.

## Countermodels

1. Current-level equivalence is not predictive equivalence:

\[
K_0=I,\qquad K_n=\operatorname{diag}(1,n).
\]

The two coordinate probes are equal at depth 0, but one becomes a predictive needle.

2. Branchwise predictive bounds do not control recombinations when the family grows:

\[
K_m=\mathbf 1_m\mathbf 1_m^*.
\]

Every coordinate probe has capacity 1, but the normalized all-ones recombination has capacity \(m\).

3. Pointwise finite capacity does not imply predictive anti-localization:

\[
K_j=j.
\]

Every stage is finite, but the predictive supremum is infinite.

## Closure-only scope

The theorem is explicitly scoped to formed predictive closures/layers. A non-closed artifact may fail transport, native-family declaration, null-mode legality, or defect summability. Such failures are outside the no-native-predictive-needle claim.

## Layman meaning

Static anti-localization says: “the doors are locked now.”

Predictive anti-localization says: “as the building is extended, every native key-combination remains priced.”

The key object is the whole forward price table, not individual probe prices at one time.
