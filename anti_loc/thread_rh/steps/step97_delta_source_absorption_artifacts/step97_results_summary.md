# Step 97: Hecke/Dirichlet Source Absorption for the Semilocal Cross-Term

## Purpose

Step 97 formulates the source-absorption theorem for the hybrid semilocal RH route.

The active obstruction is

\[
\Delta_S=q_{\mathrm{Weil},S}-q_{\mathrm{pos},S}.
\]

The source route does not require proving \(\Delta_S\preceq0\). It requires absorbing its positive part:

\[
\Delta_S^+\preceq F_n+E_{\mathrm{abs},n}.
\]

Here

\[
F_n=\sum_{\omega\in\mathcal X_n}\lambda_{\omega,n}Q_\omega^*\Theta_\omega^{-1}Q_\omega
\]

is a response-side Hecke/Dirichlet source frame.

## Main theorem

If

\[
q_Z\le q_{\mathrm{Weil},S}+e_{\mathrm{Weil},S},
\]

\[
q_{\mathrm{Weil},S}=q_{\mathrm{pos},S}+\Delta_S,
\]

and

\[
\Delta_S^+\preceq F_n+E_{\mathrm{abs},n},
\]

then

\[
q_Z\le q_{\mathrm{pos},S}+F_n+e_{\mathrm{Weil},S}+E_{\mathrm{abs},n}.
\]

So the positive package plus source frame dominates the zero-side anti-invariant form up to declared defects.

## Budget-collapse theorem

If the source frame satisfies the full anti-invariant lower-frame bound

\[
F_n\succeq \Lambda_n(\Theta_0^-)^{-1},
\]

then

\[
K_n^-\preceq \Lambda_n^{-1}\Theta_0^-+E_{\mathrm{src},n}.
\]

If

\[
\Lambda_n\to\infty
\]

and defects vanish in the fixed/exhaustive ledger sense, then the anti-invariant budget collapses.

## Arithmetic input needed

The theorem isolates the following required input:

1. an upstream-visible character family ordered by conductor or semilocal refinement;
2. carrier-native readout maps \(Q_\omega:Y_S^-\to Z_\omega\);
3. a full lower-frame/Plancherel inequality, not just an upper large-sieve estimate;
4. the absorption inequality \(\Delta_S^+\preceq F_n+E_{\mathrm{abs},n}\);
5. a finite-window tail/exhaustivity bridge;
6. auxiliary explicit-formula records for twists/L-functions if auxiliary sources are used;
7. descent from the enlarged Hecke/source carrier back to the zeta zero ledger;
8. all-six Six Birds records.

## No-go warnings

- Partial character coverage leaves hidden anti-invariant directions.
- Upper-frame estimates do not imply lower-frame coercivity.
- Finite conductor windows are support-only without tail control.
- Source weights or readouts chosen after looking at the target inequality are smuggled.
- Trace-only character averages are public shadows, not carrier witnesses.

## Bottom line

The active analytic target is now:

\[
\boxed{\Delta_S^+\preceq F_n+E_{\mathrm{abs},n}}
\]

with

\[
\boxed{F_n\succeq \Lambda_n(\Theta_0^-)^{-1},\qquad \Lambda_n\to\infty.}
\]

This is the precise form in which Hecke/Dirichlet character-source technology must enter the hybrid semilocal membrane program.
