
# Step 134: Actual Burnol/Müntz seed Ω-tail estimate

## Main verdict

The unrestricted BPRZ lower-frame import remains blocked by the squarefree Boolean GCD-log blind sector.

Step 134 proves the finite deterministic suppression mechanism and identifies the exact missing analytic record:

\[
\boxed{
\tau_{\Omega,N}
=
\frac{\|Z_y(I-P_{\Omega\le K})b_N\|}{\|Z_yb_N\|}
\to0
}
\]

or at least

\[
\boxed{\tau_{\Omega,N}\le \tau<1.}
\]

Here \(b_N\) is the actual regularized Burnol/Müntz residual seed and \(Z_y\) is the finite zeta/incidence convolution.

## Main theorem

For a Boolean blind family \(\mathcal B\),

\[
\Pi_{\mathcal B}Z_yb
=
\Pi_{\mathcal B}Z_yP_{\uparrow\mathcal B}b.
\]

So blind-sector mass is controlled exactly by the upward-closure / high-divisibility tail of the seed.

If the seed satisfies declared block cutoffs

\[
\Omega_j(S)\le K_j
\]

and every blind mode violates some block cutoff, then

\[
\boxed{\Pi_{\mathcal B}Z_yb=0.}
\]

## What Heap--Soundararajan contributes

Heap--Soundararajan provide the right imported architecture: prime blocks, \(\Omega(n_j)\le K_j\) truncations, and exponentially small scalar tail terms in their mean-value proof. Their construction defines short Dirichlet polynomials designed to mimic powers of \(\zeta\), and their block thresholds are declared before the mean-value estimates.

What remains new here is the uniform residual operator tail:

\[
\boxed{
\left\|Z_y(I-P_{\Omega\le K})B_NG_{B,N}^{-1/2}\right\|
\le \tau_{\Omega,N}.
}
\]

Scalar average tail control is not the same as this worst-direction residual tail bound.

## Incidence conditioning warning

The incidence convolution \(Z_y\) can amplify seed tails. In the raw Boolean \(\ell^2\) model, the one-prime incidence matrix has singular values \(\varphi\) and \(\varphi^{-1}\), so the condition number over \(k\) primes grows like \(\varphi^{2k}\).

Therefore the route needs either:

\[
\boxed{\text{lawful weighted response norm where incidence is controlled}}
\]

or

\[
\boxed{\text{an explicit incidence amplification budget}.}
}
\]

## Restricted BPRZ salvage

If the BPRZ GCD-log kernel has lower frame

\[
K_q\succeq \gamma_q I,
\qquad \gamma_q\asymp \log q,
\]

on the nonblind residual class, and

\[
\|\Pi_{\mathcal B}Z_yb_N\|\le\delta_N\|Z_yb_N\|,
\]

then

\[
\boxed{
\langle Z_yb_N,K_qZ_yb_N\rangle
\ge
\gamma_q(1-
\delta_N^2)\|Z_yb_N\|^2.
}
\]

So exact suppression is sufficient, but a uniform positive floor \(\delta_N<1\) can also be enough when \(\gamma_q\to\infty\).

## Route status

The HS-style declared seed route is viable if the residual seed can be made \(\Omega\)-compatible without smuggling.

The generic Burnol/Müntz seed route is not certified: no automatic high-\(\Omega\) tail bound has been proved.

The active residual is still

\[
\boxed{
\Xi_{\rm GCD,N}=R_N^*\Pi_{\rm sf}R_N.
}
\]

Step 134 shows how this residual is dominated by the high-divisibility seed tail, but does not prove that the actual seed tail vanishes.

## Bottom line

\[
\boxed{
\text{The next analytic obligation is a uniform }\Omega\text{-tail theorem for the actual residual seed.}
}
\]

If that theorem fails, \(\Xi_{\rm GCD}\) remains as a genuine residual requiring a separate source-frame record.
