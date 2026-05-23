# Step 33 Summary — Explicit-Formula Domination Schema

Step 33 formalizes the RH-facing bridge

\[
\mathsf A_Z \preceq \mathsf K^-.
\]

Here \(\mathsf A_Z\) is the zero-side anti-invariant displacement matrix and \(\mathsf K^-\) is the completed carrier-side anti-invariant probe-family currency matrix.

## Main theorem

Let

\[
V_Z:Y^-\to \ell^2(Z,w),
\qquad
\mathsf A_Z=V_Z^*V_Z,
\]

and let

\[
W_E=C_E^{\dagger/2}(L^-_E)^*,
\qquad
\mathsf K^- = W_E^*W_E.
\]

Then the following are equivalent:

1. \(\mathsf A_Z\preceq\mathsf K^-\).
2. Every anti-invariant recombination is carrier-priced:
   \[
   y^*\mathsf A_Zy\le y^*\mathsf K^-y.
   \]
3. There exists a contraction \(T\) such that
   \[
   V_Z=TW_E,
   \qquad
   \|T\|\le1.
   \]

This is the Douglas-factorization form of the explicit-formula domination square.

## RH reading

For RH, the anti-linear symmetry is

\[
J(s)=1-\bar s,
\]

and the fixed locus is

\[
\Re(s)=1/2.
\]

An off-critical zero has anti-invariant displacement. The missing RH bridge is:

\[
\mathsf A_Z\preceq\mathsf K^-.
\]

Together with the anti-invariant anti-localization budget

\[
\mathsf K^-\preceq\Theta^-,
\]

we get

\[
\mathsf A_Z\preceq\Theta^-.
\]

If \(\Theta^-=0\), visible zero mass is confined to the critical line.

## Defective bridge

If the explicit formula is missing gamma, pole, support, endpoint, or tail terms, the honest record is

\[
\mathsf A_Z\preceq\mathsf K^-_{\rm vis}+E_{\rm EF}.
\]

Then zero confinement weakens to

\[
\mathsf A_Z\preceq\Theta^-+E_{\rm EF}.
\]

Missing completion terms are therefore not bookkeeping errors. They become explicit confinement defects.

## No-overread

Trace or invariant-sector agreement is insufficient. The note includes finite countermodels where:

- trace equality holds but Loewner domination fails;
- the invariant sector passes while the anti-invariant sector fails;
- a non-contractive bridge only gives an inflated budget;
- a visible-only bridge fails unless an omitted completion budget is recorded.

## Status

This is not an RH proof. It is the exact bridge theorem an RH proof must instantiate.

The next task is to formulate the completed explicit-formula bridge itself in this contractive-factorization language:

\[
\text{completed explicit formula}
\Longrightarrow
V_Z=TW_E,
\qquad
\|T\|\le1,
\]

or a weakened version with a recorded residual:

\[
V_Z=TW_E+R,
\qquad
R^*R\preceq E_{\rm EF}.
\]
