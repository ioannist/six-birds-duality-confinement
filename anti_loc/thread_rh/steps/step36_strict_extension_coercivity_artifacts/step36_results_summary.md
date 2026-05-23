# Step 36 — Strict-Extension Sources of Anti-Invariant Coercivity

## Purpose

Step 35 showed that anti-invariant budget collapse requires a coercive audit inequality

\[
C_\Gamma\succeq \lambda (L^-_\Gamma)^*(\Theta_0^-)^{-1}L^-_\Gamma.
\]

Step 36 identifies what kind of *lawful strict extension* can supply such an inequality without smuggling zero confinement.

## Main theorem

For accepted source records

\[
\mathsf R_s=(D_s,Q_s,\Theta_s,\lambda_s),
\]

with

\[
D_s\succeq \lambda_s(Q_sL^-_\Gamma)^*\Theta_s^{-1}(Q_sL^-_\Gamma),
\]

define the response-side source coverage

\[
F_{\mathcal S}=\sum_s\lambda_s Q_s^*\Theta_s^{-1}Q_s.
\]

If

\[
F_{\mathcal S}\succeq \Lambda(\Theta_0^-)^{-1},
\]

then

\[
C_\Gamma^+\succeq\Lambda(L^-_\Gamma)^*(\Theta_0^-)^{-1}L^-_\Gamma,
\]

and therefore

\[
\mathsf K_-^+\preceq\Lambda^{-1}\Theta_0^-.
\]

## Collapse theorem

If strict extensions produce source coverages with

\[
\Lambda_n\to\infty,
\]

then

\[
\mathsf K^-_n\to0.
\]

Together with the explicit-formula domination bridge

\[
\mathsf A_Z\preceq\mathsf K^-_n,
\]

this gives quantitative zero/root confinement:

\[
\sum_{z:\|P_-\psi(z)\|\ge\delta}w_z
\le
\frac{\operatorname{tr}\Theta_0^-}{\delta^2\Lambda_n}.
\]

## Lawful source types

1. **Completion/gamma-pole source** — lawful only after signed terms are packaged into a positive anti-invariant quadratic source.
2. **Root-composite character forcing** — each anti-invariant character block must be covered.
3. **Threshold/refinement growth** — collapse requires divergent cumulative coverage, not merely infinitely many terms.
4. **Parity-closed restriction** — can make \(L^-_\Gamma=0\), but only as a scoped nonclaim for excluded anti-invariant displacement.
5. **Explicit nonclaim/gating** — narrows the claim; does not prove zero confinement.

## No-go warnings

- Symmetry and self-duality alone do not imply budget collapse.
- Hardening the wrong anti-invariant sector leaves an uncovered direction.
- A finite source gives a finite budget, not collapse.
- A source chosen because it makes zero confinement pass is post-hoc smuggling unless selected by an upstream-visible square.

## Numerical sanity checks

The finite checks confirm the PSD inequalities only. They are not Six Birds simulations.

- 60 random source-frame trials all satisfied \(\mathsf K\preceq\Lambda^{-1}\Theta\).
- In the wrong-sector model, one coordinate collapsed to \(9.999\times10^{-5}\) at \(\lambda=10^4\), while the uncovered coordinate stayed at capacity \(1\).
- A divergent strict-extension source ladder drove the model capacity to about \(0.0510\) by stage 100.
- A convergent finite source ladder stopped at a nonzero certified budget around \(0.6116\).

## Bottom line

Anti-invariant budget collapse requires an accepted strict-extension source that sees the whole anti-invariant native family with sufficient, preferably divergent, coercive strength.

For RH, this means the next real obligation is not generic positivity. It is to identify an upstream-visible completed source — gamma/pole completion, root-composite character forcing, threshold growth, or another lawful strict extension — that produces anti-invariant coercivity without using the zero-confinement conclusion.
