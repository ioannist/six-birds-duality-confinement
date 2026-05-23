# Step 72: Candidate Completed Weil Feature Maps

## Purpose

Step 72 begins the RH-specific construction track for obligation O1:

\[
\mathsf A_Z \preceq \mathsf K_{\rm cmp}.
\]

Equivalently, it asks for a Douglas contractive factorization

\[
V_Z = T W_{\rm cmp}, \qquad \|T\|\le 1.
\]

This step does not prove RH and does not prove the bridge. It sets up a concrete positive-feature target for the completed Weil carrier.

## Test-function side

We work in the logarithmic variable \(t=\log x\), with a real even smooth test-function space \(\mathcal T\subset \mathcal S(\mathbb R)\). Shifts act by

\[
(\tau_a f)(t)=f(t+a).
\]

The RH anti-linear symmetry is

\[
J(s)=1-\overline{s},
\]

and the anti-invariant readout is

\[
\psi_-(s)=\operatorname{Re}(s)-\frac12.
\]

A formal zero-side feature is

\[
(V_Z f)_\rho=\sqrt{w_\rho}(\operatorname{Re}\rho-1/2)\mathcal E_\rho(f).
\]

## Positive shift-feature template

For a positive shift measure \(\mu\), define

\[
(W_\mu f)(a,t)=\sqrt{\mu(a)}(f(t+a)-f(t)).
\]

Then

\[
\|W_\mu f\|^2=\int \Psi_\mu(\xi)|\widehat f(\xi)|^2d\xi,
\]

with

\[
\Psi_\mu(\xi)=\int \mu(a)|e^{ia\xi}-1|^2da\ge0.
\]

So shift features are positive by construction.

## Candidate four-feature decomposition

The candidate completed feature map is

\[
W_{\rm cmp}=
\begin{bmatrix}
W_{\rm pr}\\
W_\infty\\
W_{\rm pole}\\
W_{\rm tail}
\end{bmatrix}.
\]

The four slots are:

1. **Prime-power feature**

\[
(W_{{\rm pr},L}f)_n(t)=
\sqrt{\Lambda(n)/\sqrt n}\,\alpha_L(\log n)(f(t+\log n)-f(t)).
\]

This is positive as a shift-Dirichlet feature.

2. **Archimedean/gamma feature**

\[
(W_\infty f)(a,t)=\sqrt{\kappa_\infty(a)}(f(t+a)-f(t)),
\qquad
\kappa_\infty(a)\sim \frac1{2\sinh(a/2)}.
\]

This is positive after a declared renormalization or quotient handling of the singularity at \(a=0\).

3. **Pole/completion feature**

\[
W_{\rm pole}f=(\langle f,p_1\rangle,\ldots,\langle f,p_m\rangle).
\]

This is a finite-dimensional positive feature once pole and null modes are declared.

4. **Tail/support feature**

\[
W_{\rm tail,L}
\]

records omitted shifts, support leakage, and finite-to-completed promotion tails. At finite level it may appear as a defect budget \(E_{\rm tail,L}\).

## Main gate

The bridge gate passes only if

\[
V_Z=T W_{\rm cmp}, \qquad \|T\|\le1.
\]

Equivalently,

\[
\mathsf A_Z\preceq
\mathsf K_{\rm pr}+\mathsf K_\infty+\mathsf K_{\rm pole}+\mathsf K_{\rm tail}.
\]

If the bridge is incomplete, the honest statement is

\[
\mathsf A_Z\preceq
\mathsf K_{\rm vis}+E_{\rm EF}+E_{\rm tail}.
\]

## Key warning

The classical explicit formula has signed pieces. A signed distributional identity is not a positive feature-map certificate.

Trace equality is also not enough:

\[
\operatorname{tr}\mathsf A_Z=\operatorname{tr}\mathsf K_{\rm cmp}
\not\Rightarrow
\mathsf A_Z\preceq\mathsf K_{\rm cmp}.
\]

The Douglas gate needs Loewner domination.

## Bottom line

Step 72 identifies the concrete construction target for O1:

\[
\boxed{
V_Z=T
\begin{bmatrix}
W_{\rm pr}\\ W_\infty\\ W_{\rm pole}\\ W_{\rm tail}
\end{bmatrix},
\qquad \|T\|\le1.
}
\]

It also separates which pieces are already positive-feature candidates and which need completion/repair records.

## Next target

Compare this candidate feature-map gate with an actual Weil positivity formulation. The next question is whether Weil positivity implies, or can be strengthened to, the Douglas domination

\[
V_Z^*V_Z\preceq W_{\rm cmp}^*W_{\rm cmp}.
\]
