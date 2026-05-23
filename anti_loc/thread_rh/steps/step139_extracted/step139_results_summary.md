
# Step 139: Actual Burnol/Müntz Seed-Tail Import

## Verdict

The actual Burnol/Müntz seed \(\Omega\)-tail estimate is **not imported for free** from Heap--Soundararajan.

Heap--Soundararajan supplies an \(\Omega\)-block architecture for constructing short Euler-product mimics, but it does not prove that an arbitrary Burnol/Müntz residual seed has small high-\(\Omega\) tail.

So the route must now choose one of two lawful forms:

1. build an upstream-declared \(\Omega\)-compatible Burnol/Müntz residual dictionary;
2. carry the high-\(\Omega\) miss as a real \(\Xi_{\rm GCD}\) residual.

## Main gate

The active seed-tail quantity is

\[
\sigma_{K,N}
=
\left\|
(I-P_{\Omega\le K})B_NG_{B,N}^{-1/2}
\right\|.
\]

The Step 138 blind-projected incidence bound becomes

\[
\Xi_{\mathrm{GCD},N}
\preceq
\bigl(L_{R,K}+T_{R,K}\sigma_{K,N}\bigr)^2G_{B,N}.
\]

Thus the restricted BPRZ route remains viable if

\[
L_{R,K}+T_{R,K}\sigma_{K,N}<1.
\]

## Main theorem

If the residual seed family is exactly \(\Omega\)-compatible,

\[
B_N=P_{\Omega\le K}B_N,
\]

then

\[
\sigma_{K,N}=0
\]

and

\[
\Xi_{\mathrm{GCD},N}\preceq L_{R,K}^2G_{B,N}.
\]

If instead

\[
\sigma_{K,N}\le\sigma_0,
\]

then

\[
\Xi_{\mathrm{GCD},N}
\preceq
(L_{R,K}+T_{R,K}\sigma_0)^2G_{B,N}.
\]

So exact suppression is not required. A positive floor is enough if the source strength diverges.

## New defect

Requiring \(\Omega\)-compatibility introduces a new Burnol-side density defect:

\[
\epsilon_{B\to\Omega,N}
=
\left\|
(I-P_{\mathcal D_{\Omega,N}})
M_{R,N}G_{R,N}^{-1/2}
\right\|.
\]

This is the geometric price of using source-readable, \(\Omega\)-compatible atoms.

The next constructive theorem must prove

\[
\epsilon_{B\to\Omega,N}\to0
\]

or at least

\[
\epsilon_{B\to\Omega,N}\le\epsilon<1.
\]

## Bottom line

Step 139 replaces the vague request

> prove the actual seed tail is small

with the precise lawful choice:

> build an \(\Omega\)-compatible Burnol/Müntz residual dictionary, or carry the high-\(\Omega\) miss as \(\Xi_{\rm GCD}\).

## Next step

**Step 140: \(\Omega\)-compatible Burnol/Müntz residual dictionary theorem.**

Target: define a non-smuggled atom family whose regularized Dirichlet shadows obey the Heap--Soundararajan block cutoffs and test whether it remains dense enough in the Burnol/Sonine residual sector.
