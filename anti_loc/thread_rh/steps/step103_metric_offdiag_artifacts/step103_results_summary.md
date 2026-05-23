
# Step 103: Semilocal Metric Off-Diagonal Block Audit

## Main result

The finite-place semilocal metric is multiplication by

\[
a_S(\xi)=\prod_{p\in S_f}|1-p^{-1/2+i\xi}|^{-2}.
\]

For finite \(S_f\), it has an absolutely convergent Bohr expansion

\[
a_S(\xi)=\sum_{\mathbf k\in\mathbb Z^{S_f}}c_{\mathbf k}e^{i\xi\ell_{\mathbf k}},
\]

with

\[
c_{\mathbf k}=\prod_{p\in S_f}\frac{p^{-|k_p|/2}}{1-p^{-1}},
\qquad
\ell_{\mathbf k}=\sum_{p\in S_f}k_p\log p.
\]

Thus the off-diagonal block becomes

\[
P_\infty A_S(I-P_\infty)
=
\sum_{\mathbf k\ne0}
c_{\mathbf k}P_\infty\tau_{\ell_{\mathbf k}}(I-P_\infty).
\]

So compactness of \(\Delta_S\) now reduces to compactness of shifted Sonin/prolate off-diagonal blocks.

## Verdict

The block is not compact-certified.

Raw finite-place multipliers are bounded and invertible, but they do not create compactness.
A hard-cutoff model shows that shifted off-diagonal blocks can be noncompact partial isometries.

Therefore the compactness shortcut requires a genuine semilocal Sonin/prolate theorem:

\[
P_\infty\tau_\ell(I-P_\infty)
\text{ compact/Hilbert--Schmidt after quotient}.
\]

If this theorem fails, the noncompact sector must be charged by the Hecke/Dirichlet source lower-frame ladder.

## Layman interpretation

Finite Euler factors change the measuring ruler. That change decomposes into many tiny shifts.

The question is whether the Sonin/prolate safety projection turns those shifts into a compact leftover. If yes, the problem becomes mostly finite-dimensional. If no, there is an infinite-dimensional prime/gamma cross-term that must be paid by source coercivity.

## Bottom line

\[
\boxed{
\text{semilocal compactness reduces to shifted off-diagonal Sonin/prolate compactness.}
}
\]

The next step is to test/prove the compactness of

\[
P_\infty\tau_{\log p}(I-P_\infty)
\]

or identify its noncompact sector.
