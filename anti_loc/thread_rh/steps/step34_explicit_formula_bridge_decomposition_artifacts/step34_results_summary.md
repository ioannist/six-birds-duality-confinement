# Step 34: Completed explicit-formula bridge decomposition

Step 33 isolated the RH-facing bridge as

\[
\mathsf A_Z\preceq \mathsf K^-.
\]

Step 34 decomposes this bridge into visible explicit-formula pieces:

\[
W_{\rm cmp}=\begin{bmatrix}
W_{\rm pr}\\ W_\infty\\ W_{\rm pole}\\ W_{\rm tail}
\end{bmatrix},
\qquad
\mathsf K_{\rm cmp}=W_{\rm cmp}^*W_{\rm cmp}.
\]

The bridge is accepted only if the zero-side anti-invariant readout factors through the completed carrier by a contraction:

\[
V_Z=T W_{\rm cmp},\qquad \|T\|\le1.
\]

Equivalently,

\[
\mathsf A_Z=V_Z^*V_Z\preceq \mathsf K_{\rm cmp}.
\]

The four component obligations are:

1. prime-power feature \(W_{\rm pr}\),
2. archimedean/gamma feature \(W_\infty\),
3. pole/completion/null-mode feature \(W_{\rm pole}\),
4. support/tail/promotion feature \(W_{\rm tail}\).

Raw signed explicit-formula terms are not enough; the bridge requires positive carrier-side feature maps or an equivalent positive quadratic representation.

If the bridge is defective,

\[
V_Z=T W_{\rm cmp}+R,
\qquad R^*R\preceq E_{\rm EF},
\]

then for every \(t>0\),

\[
\mathsf A_Z\preceq(1+t)\mathsf K_{\rm cmp}+(1+t^{-1})E_{\rm EF}.
\]

So missing gamma, pole, support, endpoint, or tail terms become explicit off-critical allowance.

Trace equality and invariant-sector control are explicitly insufficient. The bridge must be Loewner domination on the anti-invariant sector, not a scalar accounting identity.
