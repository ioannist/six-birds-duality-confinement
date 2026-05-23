# Step 434 Self-Adjoint Extension Audit

## Native issue

The original Berry-Keating operator `xp` is not self-adjoint on the half-line without specifying a domain/boundary condition. Sierra's modified Hamiltonian improves the classical dynamics but still requires a self-adjoint extension because:

- the space is a half-line with endpoint `x=l_x`,
- `p_hat^{-1}` is nonlocal and domain-sensitive,
- the extension family is parameterized by a phase `theta in U(1)`.

## Does the U(1) family smuggle arithmetic?

The existence of a U(1) family is operator-theoretic and not arithmetic by itself. However, using a particular extension parameter to select the zeta or a Dirichlet L-function spectrum is not derived from phase-space primitives. Sierra's Dirichlet-L generalization via different extension phases means the boundary phase can carry arithmetic labels.

Thus:

```text
self-adjointness as such: partial pass;
self-adjointness as a target-selecting exact-zeta mechanism: fail.
```

For Route 2, the extension parameter must be fixed by non-arithmetic operator-theoretic data. If it is fixed by matching a character, conductor, zeta zeros, or L-special data, it violates `C_self_adjoint_native` and `C_arithmetic_independence` at the target-selection layer.

## New failure-shape refinement

```text
C_boundary_phase_arithmetic_smuggling:
A self-adjoint-extension parameter may not be chosen by matching zeta zeros, Dirichlet characters, conductors, or L-function labels. It must be fixed by arithmetic-independent operator-domain data.
```
