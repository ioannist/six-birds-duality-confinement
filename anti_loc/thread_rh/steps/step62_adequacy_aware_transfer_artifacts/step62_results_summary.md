# Step 62: Adequacy-Aware Membrane Transfer

## Purpose

This step proves the bridge theorem that combines the main formed-layer membrane transfer law with the standalone \(\Xi\)-companion transfer law.

The central statement is:

\[
\text{native membrane} + \Xi\text{-adequacy} + \text{faithful bridge}
\Rightarrow
\text{transferred layer-dissolving membrane with explicit defects}.
\]

## Exact transfer theorem

Let the source record be \((E,C,L,D)\), where:

- \(L:E\to Y\) is the native probe family,
- \(D:E\to Z\) is the layer-dissolving probe family,
- \(C\succeq0\) is the audit energy, read on the legal quotient.

Let the target record be \((E',C',L',D')\). An exact adequacy-aware bridge consists of:

\[
P:E'\to E,
\qquad
J:Y\to Y',
\qquad
R:Y'\to Y,
\qquad
B:Z\to Z',
\]

with

\[
C'\succeq \beta P^*CP,
\qquad
L'=JLP,
\qquad
D'=BDP,
\qquad
RJ=I_Y.
\]

The condition \(RJ=I_Y\) is the faithful native-readout condition.

If the source has native membrane budget

\[
K_{LL}\preceq \Theta_Y,
\]

and adequacy budget

\[
\Xi_C(D\mid L)\preceq \Omega_Z,
\]

then the target has

\[
K_{L'L'}\preceq \beta^{-1}J\Theta_YJ^*,
\]

and

\[
\Xi_{C'}(D'\mid L')\preceq \beta^{-1}B\Omega_ZB^*.
\]

Consequently, the target layer-dissolving currency is bounded by

\[
K_{D'D'}
\preceq
\beta^{-1}B(A_*\Theta_YA_*^*+\Omega_Z)B^*,
\]

where

\[
A_*=K_{DL}K_{LL}^{\dagger}
\]

is the source optimal native explanation.

## Defective transfer theorem

If the bridge has residuals

\[
L'=JLP+S,
\qquad
D'=BDP+T,
\]

then with

\[
Q=T-BA_*RS,
\qquad
E_\Xi=Q(C')^\dagger Q^*,
\]

we get, for every \(s>0\),

\[
\Xi_{C'}(D'\mid L')
\preceq
(1+s)\beta^{-1}B\Xi_C(D\mid L)B^*
+(1+s^{-1})E_\Xi.
\]

Thus bridge defects are allowed only when explicitly paid as blind-spot currency.

## Main warning

Native membrane transfer alone is insufficient. A bridge must also transfer adequacy.

If the native response map coarsens the native family and has no reconstruction, \(\Xi\) may grow. If the public dissolving readout forgets hidden directions, the public \(\Xi\) can be zero while the intrinsic \(\Xi\) is arbitrarily large.

## Finite checks

The finite algebra checks verified:

- exact transfer equality up to roundoff in the scaled exact case;
- defective transfer Loewner bounds;
- native coarsening increases \(\Xi\);
- public-shadow \(\Xi\) can hide arbitrarily large intrinsic blind spots.

These checks are only algebra sanity tests, not Six Birds simulations.

## Bottom line

\[
\boxed{
\text{membrane transfer must be adequacy-aware.}
}
\]

A lawful bridge of formed-layer membranes must carry:

\[
\text{energy},
\quad
\text{native probes},
\quad
\text{layer-dissolving probes},
\quad
\text{adequacy residual defects}.
\]

Otherwise the transferred claim is only native, public-shadow, or support-only, not a full layer-dissolving membrane.
