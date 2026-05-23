# Step 66: Fixed-Ledger versus Moving-Ledger Criteria

## Purpose

This step answers the exact-confinement concern raised after Step 65. A decreasing obstruction budget proves exact zero confinement only if it squeezes a fixed completed zero ledger, or an exhaustive sequence of partial ledgers with vanishing tail. A moving finite-stage ledger without tail/exhaustivity is support-only.

## Main theorem: fixed-ledger squeeze

Let \(\mathsf A_Z\succeq0\) be a positive trace-class zero-side anti-invariant displacement ledger. If

\[
\mathsf A_Z\preceq B_n\quad\text{for all }n,
\qquad
\operatorname{tr}B_n\to0,
\]

then

\[
\mathsf A_Z=0.
\]

Thus an infinite strict-extension ladder can prove exact confinement, but only when it dominates the same completed zero ledger at every stage.

## Exhaustive-ledger theorem

If partial ledgers \(\mathsf A_{Z,n}\) satisfy

\[
\mathsf A_Z\preceq \iota_n\mathsf A_{Z,n}\iota_n^*+T_n,
\]

and

\[
\mathsf A_{Z,n}\preceq B_n,
\qquad
\operatorname{tr}(\iota_nB_n\iota_n^*)+\operatorname{tr}T_n\to0,
\]

then again

\[
\mathsf A_Z=0.
\]

So a moving/truncated ledger is acceptable only if it comes with a vanishing tail/exhaustivity bridge to the completed ledger.

## Moving-ledger failure

A moving finite-stage ledger can shrink to zero while a completed hidden ledger remains nonzero. Example:

\[
\mathsf A_Z=\operatorname{diag}(2^{-1},2^{-2},2^{-3},\ldots),
\qquad
\operatorname{tr}\mathsf A_Z=1.
\]

At stage \(n\), if the ledger sees only coordinate \(e_n\), then the visible budget is \(2^{-n}\to0\), but the completed ledger is still nonzero. Without a tail record, this is only support evidence.

## RH/root-composite criterion

The root-composite obstruction budget is

\[
B_n(t)=
(1+t)(\Lambda_n^{-1}\Theta_0^-+E_{\rm src,n})
+(1+t^{-1})E_{{\rm EF},n}.
\]

If either fixed-ledger or exhaustive-ledger domination gives

\[
\mathsf A_Z\preceq B_n(t_n)
\]

with

\[
\operatorname{tr}B_n(t_n)\to0,
\]

then

\[
\mathsf A_Z=0.
\]

In scalar trace form, if

\[
a_n=\operatorname{tr}(\Lambda_n^{-1}\Theta_0^-+E_{\rm src,n}),
\qquad
b_n=\operatorname{tr}E_{{\rm EF},n},
\]

then

\[
\inf_{t>0}\operatorname{tr}B_n(t)=(\sqrt{a_n}+\sqrt{b_n})^2.
\]

So exact confinement follows from \(a_n\to0\) and \(b_n\to0\), but only with a fixed or exhaustive zero ledger.

## Status taxonomy

- `finite_completion`: a finite stage proves the completed ledger is zero.
- `fixed_ledger`: the same completed ledger is dominated by vanishing budgets.
- `exhaustive_ledger`: partial ledgers plus vanishing tails dominate the completed ledger.
- `moving_ledger_support_only`: moving finite ledgers improve, but no tail/exhaustivity record exists.
- `failed_tail`: tail does not vanish.
- `failed_visibility`: zero readout does not separate the fixed locus.
- `failed_budget_collapse`: EF/source/coercivity defects do not tend to zero.

## Layman interpretation

A shrinking bound proves exact zero only if it keeps bounding the same thing. If every stage measures a different visible slice, the visible slice can shrink while hidden mass remains outside the measurement.

For RH, the ladder must either finish in finite steps or squeeze the same completed zero ledger, or an exhaustive approximation with a vanishing tail. Better and better finite windows alone are not enough.
