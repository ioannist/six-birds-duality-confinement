# Step 27: Countermodel and Matched-Control Atlas

## Purpose

This step proves that the gates in the accepted predictive anti-localization test-family theorem are necessary.  The result is a finite countermodel atlas: for each gate, a small Hilbert-space package shows that if the gate is removed, a scalar, diagonal, route-local, current-only, or public-shadow anti-localization claim can look valid while the intended family-level predictive no-needle claim is false, outside scope, or support-only.

## Main theorem

Let an accepted anti-localization test family require gates for closure, exact package, null-mode legality, declared native family, recombination closure, protocol honesty, readout agreement, predictive stability, lawful witness, packaging confluence/order, no-smuggling, and conditioning control.

For each gate there exists a finite-dimensional countermodel satisfying the surrounding algebraic identities but failing that gate, such that a false anti-localization overclaim becomes possible.

Thus the accepted-test-family theorem is not overbuilt. Its gates are forced by finite obstructions.

## Minimal countermodels

| Gate | Countermodel | Failure |
|---|---|---|
| closure/exactness | `C_epsilon = diag(epsilon,1)` | passive positive carrier has capacity `1/epsilon` |
| null legality | `C=diag(0,1)`, probe sees kernel | capacity is infinite |
| recombination closure | `K = 1 1^*` | all diagonal capacities are 1, top recombination capacity is `m` |
| protocol honesty | duplicated route stack | route-local capacities are 1, mixed protocol capacity is 2 |
| readout agreement | `Lq=(1,3)`, `Lp=(1,0)` | budget transfer needs defect 9 |
| predictive stability | `K_j=diag(1,j)` | each stage finite, predictive supremum infinite |
| lawful witness | compressed-vs-ambient example | public shadow differs from compressed witness by factor about 25.5 |
| packaging confluence | noncommuting projections | completion order changes carrier |
| no-smuggling | select package by maximizing S6 margin | support-only or smuggled |
| conditioning control | two broad atoms differ by needle | branchwise trace small, span capacity 1 |

## Matched controls

Each countermodel is paired with a matched control: same or comparable finite scope, but with the missing gate restored. Examples include orthogonal probe families for recombination, orthogonal route stacks for protocol honesty, reducing subspaces for compressed/ambient equality, and upstream-declared selectors for no-smuggling.

## Why this matters

The atlas turns the Six Birds audit gates into mathematical necessity statements. It proves that anti-localization cannot be accepted from:

- scalar-only checks,
- diagonal-only probe checks,
- route-local checks,
- current-depth checks,
- public-shadow checks,
- post-hoc selected packages,
- approximate carriers with unbudgeted tails,
- branchwise delocalization without frame control.

## Layman interpretation

A layer membrane is not verified by checking one door, one route, or one moment in time. A real membrane must withstand every declared native combination of probes, every lawful route, and every refinement step. The countermodels show exactly how a false membrane claim slips through when one gate is missing.

## Status

Proof-level necessity atlas. The numerical script only verifies the tiny finite matrix examples and creates support plots for exposition; it is not a Six Birds simulation.
