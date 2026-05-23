# Step 68 — Zero-Readout Separation and Exact Fixed-Locus Confinement

## Main result

Let `j` be the anti-linear/real involution on the zero/root space and let `Fix(j)` be its fixed locus. Let `psi` be a zero readout into a real Hilbert response space with involution `J_Y`, and define the anti-invariant readout

\[
q(x)=P_-\psi(x),\qquad P_-=(I-J_Y)/2.
\]

For a visible zero ledger `(Z,w)`, define

\[
\mathsf A_Z=\sum_{z\in Z}w_zq(z)q(z)^*.
\]

If weights are positive, then

\[
\mathsf A_Z=0 \iff q(z)=0\quad(z\in Z).
\]

If the readout separates the fixed locus,

\[
q(z)=0\iff z\in \operatorname{Fix}(j),
\]

then

\[
\mathsf A_Z=0\Rightarrow Z\subseteq \operatorname{Fix}(j).
\]

## Quantitative version

If the readout has a separation modulus `m(eps)`:

\[
d(z,\operatorname{Fix}(j))\ge\varepsilon\Rightarrow \|q(z)\|\ge m(\varepsilon),
\]

then

\[
\mu\{d(z,\operatorname{Fix}(j))\ge\varepsilon\}\le \operatorname{tr}\mathsf A_Z/m(\varepsilon)^2.
\]

## RH specialization

For RH,

\[
j(s)=1-\overline{s},\qquad \operatorname{Fix}(j)=\{s:\Re(s)=1/2\}.
\]

The readout

\[
q(s)=\Re(s)-1/2
\]

is separating. Thus

\[
\mathsf A_Z=\sum_{\rho\in Z} w_\rho(\Re\rho-1/2)^2=0
\]

implies every visible zero in `Z` lies on the critical line.

## Key warning

A nonseparating readout can give `A_Z=0` while off-fixed zeros remain. For example, a readout depending only on `Im(s)` ignores the displacement `Re(s)-1/2`. This is `trace_shadow_only` or `failed_separation`, not confinement.

## Relation to Step 67

Step 67 proved fixed/exhaustive ledger squeeze. Step 68 adds the final readout gate:

\[
\text{fixed/exhaustive squeeze} + \text{separating readout} \Rightarrow \text{exact fixed-locus confinement}.
\]
