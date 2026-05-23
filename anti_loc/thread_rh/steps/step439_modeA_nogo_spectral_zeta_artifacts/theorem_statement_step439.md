# Step 439 Theorem Statement

## Spectral triple setup

Let `(A,H,D)` be a Connes spectral triple with `D` self-adjoint, compact resolvent, and nonzero eigenvalue magnitudes `{mu_n}`. Its spectral zeta function is

```text
zeta_D(s) = Tr |D|^{-s} = sum_n mu_n^{-s}
```

for `Re(s)` sufficiently large, then by meromorphic continuation where available.

## No-go theorem: spectral-zeta correspondence is not Hilbert-Polya

**Theorem (Mode A no-go, Dispatch 3).** A construction that only proves a spectral-zeta correspondence

```text
zeta_D(s) = F(s) zeta(s)
```

for a nonzero analytic factor `F`, or even exact proportionality in a concrete model, does not prove the Hilbert-Polya target

```text
Spec(H) = { gamma_n : zeta(1/2 + i gamma_n)=0 }.
```

The spectral-zeta identity concerns the Dirichlet/Mellin transform of eigenvalue magnitudes. The Hilbert-Polya target concerns the eigenvalues themselves. These are different spectral objects.

## Concrete counterexample

For the non-adelic circle spectral triple

```text
A = C^infty(S^1),
H = L^2(S^1, spinors),
D_R = -i R^{-1} d/dtheta,
```

with zero mode removed,

```text
Spec(D_R) = { n/R : n in Z, n != 0 },
zeta_D(s) = sum_{n != 0} |n/R|^{-s} = 2 R^s zeta(s).
```

Thus `zeta_D` is exactly proportional to the Riemann zeta function, but the operator spectrum is the integer lattice, not the zeta-zero ordinate set.

## Constraint form

`C_spectral_zeta_not_spectrum`: matching zeta as `Tr |D|^{-s}` is insufficient for Route 2 unless an additional independent argument identifies `Spec(D)` or another self-adjoint operator's spectrum pointwise with the zeta-zero ordinates.
