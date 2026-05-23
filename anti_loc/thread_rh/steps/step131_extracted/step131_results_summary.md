# Step 131: Residual coefficient class versus the GCD-log blind sector

## Main result

Step 130 showed that the BPRZ shifted main-term kernel does not give a lower frame on the unrestricted coefficient space. Step 131 asks the sharper question: does the **actual residual coefficient class** hit the squarefree Boolean near-null sector?

The new residual is

\[
\Xi_{\rm GCD,N}=R_N^*\Pi_{\rm sf}R_N.
\]

Here \(\Pi_{\rm sf}\) projects onto the GCD-log near-null Boolean sign modes.

If \(\Xi_{\rm GCD,N}\) is zero or tail-small, then BPRZ may still be usable on the restricted residual class. If it is not, this blind sector must be separately source-absorbed.

## New structural observation

The zeta/Müntz shadow is not an arbitrary coefficient vector. On a squarefree Boolean cube, zeta convolution is the incidence map

\[
(Z_y b)(d)=\sum_{e\mid d}b(e).
\]

In the Boolean sign basis,

\[
\langle \psi_\epsilon,Z_yb\rangle
=2^{-k/2}(\otimes_p\ell_{\epsilon_p})b,
\]

with

\[
\ell_+(b_0,b_1)=2b_0+b_1,
\qquad
\ell_-(b_0,b_1)=-b_1.
\]

In particular, for the all-minus blind mode,

\[
\langle\psi_-,Z_yb\rangle=2^{-k/2}(-1)^k b(P_y).
\]

So deep Boolean blind modes see only high-divisibility boundary coefficients of the seed. This gives a possible escape from the Step 130 obstruction.

## New analytic gate

The next required theorem is a high-divisibility / sieve-tail estimate for the actual regularized Burnol/Müntz seed coefficients:

\[
\sum_{\epsilon\in\operatorname{Blind}}
|(\otimes_p\ell_{\epsilon_p})b_N|^2
\le
\delta_N\|Z_yb_N\|^2.
\]

If \(\delta_N\to0\), the GCD-log blind sector is avoided. If \(\delta_N\le\delta<1\), a positive visibility floor may remain. If not, \(\Xi_{\rm GCD}\) becomes the next source-absorption target.

## Finite checks

The finite checks verify the Boolean algebra identities and show toy suppression for zeta-convolved seeds with high-divisibility damping. They are not RH evidence.

The maximum Möbius identity error was at roundoff scale.

At the largest tested cube, the synthetic band-limited zeta seed had bottom-10% blind-sector overlap approximately \(7\times10^{-34}\). This only illustrates the mechanism; the real work is to prove the corresponding estimate for the actual regularized Burnol/Müntz shadow.

## Bottom line

The unrestricted BPRZ lower-frame import is blocked, but Step 131 identifies a specific possible repair:

\[
\boxed{\text{zeta convolution may suppress GCD-log blind modes by Möbius/high-divisibility annihilation.}}
\]

The next step is to prove or refute that suppression for the actual Burnol/Müntz residual coefficient class.
