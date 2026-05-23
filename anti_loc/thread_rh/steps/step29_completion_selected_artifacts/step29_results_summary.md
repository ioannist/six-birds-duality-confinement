# Step 29 — Closure-Completion for Anti-Localization

## Purpose

Step 28 showed that every family anti-localization failure has a recombination/critical-pair witness:

\[
\mathsf K\npreceq\Theta
\iff
\exists y\quad y^*(\mathsf K-\Theta)y>0.
\]

Step 29 turns that witness theorem into a completion calculus. A witness is no longer just a counterexample; it is a closure obligation.

## Main theorem

A formed closure/layer earns accepted family anti-localization exactly when its native critical-pair completion reaches an accepted terminal record.

Equivalently, accepted completion means:

\[
\mathsf K\preceq\Theta,
\]

so every declared native recombination is priced:

\[
\operatorname{Cap}_{C}(y^*L;\operatorname{Ran}\Gamma)
=
y^*\mathsf K y
\le
y^*\Theta y.
\]

If completion terminates by exclusion, budget weakening, or downgrade, then only the weakened/scoped claim is accepted.

## Lawful witness-resolution moves

A witness may be handled only by an audited move:

1. exclude / nonclaim,
2. carrier rewrite / package repair,
3. budget weakening,
4. probe-family completion,
5. status downgrade,
6. strict extension.

Ignoring the witness is failed audit. Selecting a package because it hides the witness is smuggling/overread.

## Termination theorem

If every non-terminal completion move strictly decreases a well-founded measure

\[
\mu(\mathcal R_{n+1})<\mu(\mathcal R_n),
\]

then completion terminates in finite time.

This is the honest form of the Reflexive SBT anti-localization conjecture: not “the loop always contracts capacity,” but “every witness-producing move is backed by a well-founded strict-extension or decreasing-measure certificate.”

## No general termination theorem

Two failures are recorded:

1. **Partial repair forever:** in dimension one, \(\mathsf K=1\), \(\Theta_n=1-2^{-n}\). The defect decreases but never reaches zero in finite time.
2. **Infinite strict-extension chain:** each accepted stage is extended by one new native response with a fresh witness. Without a novelty budget, this can continue forever.

So anti-loc completion needs a finite witness universe, a no-resurrection rule, a well-founded measure, or a bounded strict-extension budget.

## Budget completion

For fixed carrier/probe family, the least accepted budget is

\[
\Theta_{\min}=\mathsf K.
\]

From a starting budget \(\Theta_0\), the least Loewner budget extension is

\[
\Theta_{\mathrm{acc}}
=
\Theta_0+(\mathsf K-\Theta_0)_+.
\]

This is useful as a matched control, but it is a weakened claim, not a proof of the original budget.

## Confluence theorem

If the completion relation is terminating and locally confluent modulo status, then the terminal accepted/non-accepted status and budget are unique up to declared equivalence.

This is the Knuth–Bendix form of anti-localization completion: critical-pair witnesses are local divergences, and confluence means the final membrane status does not depend on the order in which witnesses are resolved.

## Bottom line

Anti-localization is now a closure-completion property:

\[
\boxed{
\text{all native critical pairs have been resolved, priced, or lawfully excluded.}
}
\]

A formed layer has a membrane exactly when no reachable native recombination can buy too much addressability for too little audit spend.
