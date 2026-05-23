# Step 135: Incidence-Conditioned Ω-Tail Theorem

## Result
The GCD-log blind-sector residual is controlled by the incidence-conditioned high-divisibility tail

\[
\tau_{\Omega,N}^{Z}
=\left\|Z_y(I-P_{\Omega\le K})B_NG_{B,N}^{-1/2}\right\|.
\]

This is stronger than an ordinary seed-tail estimate because the zeta/Müntz incidence operator \(Z_y\) may amplify high-\(\Omega\) seed components.

## Main theorem
If the declared blind Walsh family is covered by the block cutoff, then

\[
\Pi_{\mathcal B}Z_yB_NG_{B,N}^{-1/2}
=
\Pi_{\mathcal B}Z_y(I-P_{\Omega\le K})B_NG_{B,N}^{-1/2},
\]

and therefore

\[
\Xi_{{\rm GCD},N}\preceq (\tau_{\Omega,N}^{Z})^2G_{B,N}.
\]

## Incidence warning
In the raw Boolean \(\ell^2\) model, the one-prime incidence matrix has singular values \(\varphi\) and \(\varphi^{-1}\), so \(\|Z_y\|=\varphi^k\). Thus seed-tail smallness alone is not enough unless it beats incidence amplification or the response metric changes the bound.

## Restricted BPRZ salvage
If the GCD-log kernel has lower frame \(K_q\succeq\gamma_qI\) on the nonblind sector and the blind overlap is \(\delta_N<1\), then

\[
R_N^*K_qR_N\succeq \gamma_q(1-\delta_N^2)G_{B,N}.
\]

Since \(\gamma_q\asymp\log q\), a uniform positive floor can still yield source-coercivity growth.

## Status
The deterministic gate is closed. The analytic estimate for the actual Burnol/Müntz seed remains open:

\[
\left\|Z_y(I-P_{\Omega\le K})B_NG_{B,N}^{-1/2}\right\|\to0
\]

or at least a uniform bound below one.
