# Step 436: Non-Adelic NCG Substrate Choice

This is STEP 436 -- Route 2 Stage I under grammar `G_spectral_geometric_non_adelic`, the last of the four dispatch-named Route 2 grammars after steps 433, 434, and 435.

## External anchors cited

- Connes 1999 spectral realization: adèle/idèle class space realization of the Riemann zeros. This is explicitly excluded here by `C_no_adelic_substrate`.
- Connes-Marcolli, *Noncommutative Geometry, Quantum Fields and Motives*: spectral triples and spectral action framework.
- Connes-Moscovici residue calculus: zeta functions of spectral triples, dimension spectrum, and noncommutative residue machinery.

## Candidate substrate

I choose the simplest concrete non-adelic spectral triple:

- Algebra: `A = C^infty(S^1)`.
- Hilbert space: `H_space = L^2(S^1, spinors)`.
- Dirac operator: `D_R = -i R^{-1} d/dtheta` on the standard periodic Sobolev domain `H^1(S^1)`.
- Zero mode handling: remove the kernel of `D_R` when forming `Tr |D_R|^{-s}`.

This is a commutative Connes spectral triple rather than an adelic one. It is intentionally chosen because it is the strongest non-adelic positive test for the grammar: its spectral zeta is exactly proportional to the Riemann zeta function.

## Operator facts

`D_R` is self-adjoint by standard elliptic operator theory on a compact spin manifold, has compact resolvent, and has spectrum

```text
Spec(D_R) = { n/R : n in Z }.
```

After removing the zero mode, `|D_R|` has positive eigenvalues `n/R` with multiplicity 2 for `n >= 1`.

## Why this is the right stress test

The prompt asks whether a non-arithmetic NCG substrate can make `zeta_D(s) = Tr |D|^{-s}` equal or close to `zeta(s)`. The circle Dirac triple gives the exact relation

```text
zeta_D(s) = 2 R^s zeta(s).
```

Thus, if spectral-zeta equality were sufficient for the Route 2 Hilbert-Polya target, this would be the cleanest Stage I success. The audit below shows it is not sufficient, because the operator spectrum is the integer lattice, not the zero ordinates `{gamma_n}`.
