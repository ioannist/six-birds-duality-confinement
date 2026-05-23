# Step 35 — Anti-Invariant Budget Collapse

## Purpose

Steps 32--34 isolated the RH-facing route:

\[
\mathsf A_Z\preceq \mathsf K^- ,
\qquad
\mathsf K^-\preceq \Theta^- .
\]

Here \(\mathsf A_Z\) is zero-side anti-invariant displacement and \(\mathsf K^-\) is carrier-side anti-invariant currency. Step 35 studies when \(\mathsf K^-\) can vanish or become small without smuggling the desired zero-confinement conclusion.

## Main results

### 1. Zero budget is exact fixed-layer readout

Under null-mode legality,

\[
\mathsf K^- =0
\]

if and only if

\[
L^-_\Gamma=0
\]

on the legal energy quotient. So exact zero anti-invariant budget requires the formed closure to have no native anti-invariant readout.

### 2. Coercive anti-invariant audit collapses budget

If

\[
C_\Gamma\succeq
\lambda (L^-_\Gamma)^*(\Theta^-_0)^{-1}L^-_\Gamma,
\]

then

\[
\mathsf K^-\preceq \lambda^{-1}\Theta^-_0.
\]

Thus a strict-extension ladder with \(\lambda_n\to\infty\) forces

\[
\mathsf K^-_n\to0.
\]

### 3. Budget collapse gives zero confinement

If

\[
\mathsf A_Z\preceq \mathsf K^-\preceq \varepsilon\Theta^-_0,
\]

then

\[
\sum_{z:\ \|P_-\psi(z)\|\ge\delta}w_z
\le
\frac{\varepsilon\operatorname{tr}(\Theta^-_0)}{\delta^2}.
\]

If \(\varepsilon=0\), all visible root/zero mass lies on the fixed locus.

## No-go results

Anti-linear symmetry alone does not collapse budget. A block decomposition \(Y=Y^+\oplus Y^-\) with \(C=I\) and \(L^-=I_{Y^-}\) has

\[
\mathsf K^-=I_{Y^-}.
\]

Invariant-sector or trace control also does not imply anti-invariant control.

## RH reading

For RH,

\[
J(s)=1-\overline{s},
\qquad
\operatorname{Fix}(J)=\{\Re(s)=1/2\}.
\]

Step 35 says exact zero confinement would follow from:

\[
\mathsf A_Z\preceq\mathsf K^-
\]

plus either

\[
L^-_\Gamma=0
\]

or a coercive anti-invariant audit with \(\lambda\to\infty\). This is not an RH proof; it is the honest budget-collapse mechanism an RH proof would need.

## Small checks

The scalar model \(C_\lambda=1+\lambda\), \(L^-=1\), \(\Theta_0^-=1\) gives

\[
\mathsf K^-_\lambda=\frac{1}{1+\lambda}\le\frac1\lambda.
\]

Random finite-dimensional checks confirmed the Loewner bound \(\mathsf K^-\preceq\lambda^{-1}\Theta^-_0\).

## Bottom line

Anti-invariant budget collapse is not a consequence of symmetry. It requires either exact fixed-layer readout or a strict-extension/coercive audit that makes anti-invariant response increasingly expensive.

## Additional no-go checks

Partial hardening is insufficient. In the model

\[
C_\lambda=I+\lambda e_1e_1^*,\qquad L^-=I_{\mathbb R^2},
\]

the first anti-invariant coordinate has budget \((1+\lambda)^{-1}\), but the second remains at budget \(1\). Thus the audit must be coercive for the whole declared anti-invariant family, not just one visible direction.

Null-mode legality is also essential. For

\[
C=\operatorname{diag}(0,1),\qquad L(a_0,a_1)=a_0,
\]

the pseudoinverse expression gives \(LC^\dagger L^*=0\), but the true variational capacity is infinite. A fake zero budget can appear if a probe sees a legal null mode.
