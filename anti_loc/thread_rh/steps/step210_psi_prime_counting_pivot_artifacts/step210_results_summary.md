# Step 210 Results Summary

## Carrier Declaration

The carrier is Chebyshev's function
\[
  \psi(x)=\sum_{p^k\le x}\log p
  =\sum_{n\le x}\Lambda(n),
\]
viewed on \(L^2_{\rm loc}(\mathbb R_+,dx/x)\) or a weighted asymptotic-envelope
space. Native probes are pointwise values \(\psi(x)\), the error
\(\psi(x)-x\), and weighted averages.

Two residual forms were recorded:
\[
  \Xi_\psi(\epsilon)=\limsup_{x\to\infty}
  {|\psi(x)-x|\over x^{1/2+\epsilon}}
  \quad(\epsilon>0),
\]
and the sharper von Koch form
\[
  \Xi_\psi=\limsup_{x\to\infty}
  {|\psi(x)-x|\over \sqrt{x}\log^2 x}.
\]

## CRE Audit

By von Koch (1901),
\[
  \psi(x)-x=O(\sqrt{x}\log^2 x)
  \quad\Longleftrightarrow\quad \mathrm{RH}.
\]
Thus this is a CRE carrier.

## Explicit Formula Audit

The explicit formula
\[
  \psi(x)-x=-\sum_\rho {x^\rho\over \rho}
  +\log(2\pi)-{1\over2}\log(1-x^{-2})
\]
is an exact zero-sum decomposition. It does not create a CTMT terminus: the
individual terms \(x^\rho/\rho\) are computable once zeros are specified. The
closure problem is global summability/cancellation strong enough to imply the
von Koch bound, which is RH-equivalent.

## Relationship With Mertens

This matches Step 197's Mertens classification. Both are scalar asymptotic
CRE carriers, related by Perron/Mellin transforms of \(1/\zeta\) and
\(-\zeta'/\zeta\), and both fall in CRCFT-TE.

## Verdict

`V_psi_CRCFT_TE`.

The psi carrier adds another CRE target-equivalence instance and does not
refute the Dichotomy coverage pattern.
