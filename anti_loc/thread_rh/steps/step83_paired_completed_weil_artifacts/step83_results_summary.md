# Step 83: Paired Completed Weil Feature Gate

This step replaces separated diagonal bookkeeping by a paired completed Weil feature gate.

## Main point

The previous route tried to make the prime term positive as

\[
q_{\rm pr,L}=P_{\rm pr,L}+d_{\rm pr,L}\|f\|^2.
\]

This creates a large diagonal bill. Step 82 showed that finite-rank pole/completion features cannot pay a full diagonal on an infinite anti-invariant core.

The new route is to avoid separated diagonal accounting and ask directly for a paired completed positive feature representation:

\[
q_{\rm cmp}[f]
=
c\|f'\|_2^2+
\int\|\tau_a f-f\|_2^2\,d\mu(a)
+q_{\rm pole}[f]+e_{\rm tail}[f].
\]

The Douglas bridge gate becomes

\[
\|V_Z f\|^2\le q_{\rm cmp}[f]+e_{\rm br}[f]
\]

on the completed anti-invariant core, with defects controlled in the fixed/exhaustive ledger sense.

## Main theorem

A translation-invariant paired difference feature is governed by a continuous negative definite symbol:

\[
\Psi(\xi)=c\xi^2+2\int(1-\cos(a\xi))\,d\mu(a),
\qquad c\ge0,\quad \mu\ge0.
\]

If the completed signed Weil form can be matched to such a paired positive form, plus finite-rank pole/completion and tail records, and if the core-to-full closure gate passes, then

\[
V_Z^*V_Z\preceq W_{\rm cmp}^*W_{\rm cmp}+E_{\rm br}.
\]

If the defect vanishes, Douglas factorization gives

\[
V_Z=T W_{\rm cmp},\qquad \|T\|\le1.
\]

## What this changes

The active RH construction target is no longer:

\[
\text{pay the separated prime diagonal by pole/tail terms.}
\]

It is now:

\[
\boxed{\text{construct a paired completed Weil feature representation.}}
\]

This avoids the no-free-diagonal obstruction: singular or growing diagonals must remain paired or be renormalized by an audit record.

## Warnings

- Spectral positivity of a symbol is weaker than being a shift-difference feature; the CND gate is stronger.
- Finite-rank pole data can repair finite-dimensional completion/null directions, but not a full-core scalar diagonal.
- Moving finite-window feature checks are support-only without tail/exhaustivity.
- Trace equality is not Loewner domination.

## Bottom line

Step 83 does not prove RH. It reformulates the central O1 bridge in the mathematically honest form that survives Step 82:

\[
\boxed{\text{paired completed Weil feature domination, not separated diagonal accounting.}}
\]
