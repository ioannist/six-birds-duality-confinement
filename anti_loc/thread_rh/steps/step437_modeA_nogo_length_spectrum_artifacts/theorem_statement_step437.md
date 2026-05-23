# Step 437 Proposed No-Go Theorem

## Definitions

An **arithmetic-independent compact dynamical system** is a compact geometric/dynamical substrate whose primitive construction vocabulary consists of Riemannian geometry, dynamics, and topology only: manifolds, metrics, curvature, geodesic flow, periodic orbits, entropy, mixing rates, and fundamental groups of geometric origin.

The following are excluded as primitives: rational primes, the integer lattice as a distinguished arithmetic object, arithmetic groups, congruence subgroups, modular forms, adeles, ideles, class field structures, arithmetic schemes, zeta functions, L-functions, and any boundary/domain condition parameter chosen from those objects.

Let

```text
L(X) = { ell(gamma) : gamma primitive closed orbit of X }
```

with multiplicity.

## Candidate theorem: strong form

For every arithmetic-independent compact dynamical system `X`, `L(X)` cannot equal `{log p : p prime}` as a multiset; even after rescaling entropy to `h=1`, the orbit-counting error term is controlled by Pollicott-Ruelle/geodesic-flow data, not by Riemann-zero data.

## Theorem-grade form actually supported

The strong form resists proof because `arithmetic-independent` is a negative design constraint, not a formal mathematical category closed under all possible synthetic constructions. However, the following theorem-grade generic obstruction is supported:

> **Generic Length-Spectrum No-Go.** In any finite-dimensional real-analytic family of compact negatively curved geometric/dynamical systems whose primitive data are non-arithmetic geometric parameters, exact equality `L(X) = {log p}` is a countable infinite system of analytic equations in those parameters. Unless the family contains an arithmetic mechanism forcing the equations, the equality locus is meagre and measure zero when the length functions are nonconstant and independent on finite truncations. Moreover, after entropy normalization `h=1`, orbit-counting errors are governed by Pollicott-Ruelle resonances of the flow, not by the Riemann-zero explicit-formula spectrum.

## Constraint-level theorem statement

`C_length_spectrum_arithmetic_mismatch` should be sharpened to:

> A Selberg/periodic-orbit Route 2 substrate may not rely on formal prime-geodesic analogy alone. It must either derive a canonical, arithmetic-independent map from primitive orbit lengths to `{log p}` with multiplicities and explicit-formula error terms, or it fails `C_trace_formula_compatibility` by length-spectrum arithmetic mismatch.
