# Step 132: Müntz shadow high-divisibility / Boolean blind-sector suppression theorem

## Main result

Step 132 proves an exact finite Boolean theorem. On a squarefree prime cube, the zeta/incidence convolution

\[
(Z_y b)(T)=\sum_{S\subseteq T}b(S)
\]

has Walsh coefficient at sign vector \(\epsilon\) given by

\[
\widehat{Z_yb}(\epsilon)=
2^{-k/2}(-1)^{|A|}
\sum_{V\subseteq A^c}2^{k-|A|-|V|}b(A\cup V),
\]

where \(A=\{p:\epsilon_p=-1\}\). Therefore a blind sign mode only sees seed coefficients divisible by every prime in its negative set.

## Upward-closure theorem

For any family of blind negative-prime sets \(\mathcal B\), define

\[
\uparrow\mathcal B=\{S: \exists A\in\mathcal B, A\subseteq S\}.
\]

Then

\[
\Pi_{\mathcal B}Z_yb=\Pi_{\mathcal B}Z_yP_{\uparrow\mathcal B}b.
\]

So the blind-sector projection is exactly controlled by the high-divisibility tail of the seed.

For the threshold family \(\mathcal B_R=\{A:|A|\ge R\}\), this gives

\[
\Pi_{\mathcal B_R}Z_yb=0
\]

whenever \(b(S)=0\) for \(|S|\ge R\).

## RH-route implication

The unrestricted BPRZ lower-frame import is blocked by squarefree Boolean near-null modes. Step 132 identifies the possible repair:

\[
\Xi_{{\rm GCD},N}=R_N^*\Pi_{\rm sf}R_N
\]

is tail-small if the actual regularized Burnol/Müntz seed coefficients have small high-divisibility tail on the upward closure of the blind sets.

If the GCD-log kernel has lower bound \(\gamma_q\asymp\log q\) on the nonblind complement and blind overlap is \(\delta_N\), then

\[
\langle Z_yb,K_qZ_yb\rangle
\ge
\gamma_q(1-\delta_N^2)\|Z_yb\|^2.
\]

A positive visibility floor is enough. Exact blind suppression is better but not necessary.

## New obligation

The active analytic target is now:

\[
\frac{\|\Pi_{\rm sf}Z_yb_N\|}{\|Z_yb_N\|}\to0
\]

or at least a uniform bound below one, for the actual regularized Burnol/Müntz residual seed coefficients.

This aligns with the Heap--Soundararajan architecture: their short Dirichlet polynomials use explicit \(\Omega\)-cutoffs, which is exactly the kind of high-divisibility control the Boolean blind-sector theorem needs.

## Nonclaim

Step 132 does not prove RH and does not prove the high-divisibility tail estimate for the actual Burnol/Müntz seed. It proves the finite algebraic mechanism and isolates the remaining analytic obligation.
