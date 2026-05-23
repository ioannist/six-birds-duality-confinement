# Step 436: Spectral Zeta Function

For the candidate spectral triple `(C^infty(S^1), L^2(S^1, spinors), D_R)`, the eigenfunctions are Fourier modes `e^{in theta}`. The Dirac operator has eigenvalues

```text
lambda_n = n/R,    n in Z.
```

Removing the zero mode, the spectral zeta function is

```text
zeta_D(s) = Tr |D_R|^{-s}
          = sum_{n != 0} |n/R|^{-s}
          = 2 R^s sum_{n=1}^infty n^{-s}
          = 2 R^s zeta(s).
```

The factor `2 R^s` is entire and nonzero, so the zeros of `zeta_D(s)` match the zeros of the Riemann zeta function as a function of the complex variable `s`.

## Critical distinction

Route 2 target is not `zeta_D(s) has zeta's zeros`. The target is:

```text
Spec(H) = { gamma : zeta(1/2 + i gamma) = 0 }.
```

For the circle Dirac triple,

```text
Spec(D_R) = (1/R) Z,
```

which is not the sequence of Riemann-zero ordinates. The equality `zeta_D(s) = 2 R^s zeta(s)` is a spectral zeta identity, not a Hilbert-Polya spectral realization.

## Explicit formula check

The trace formula behind the circle Dirac operator is Poisson summation on the integer lattice. Its primitive spectral data are integer Fourier modes and their dual lattice, not rational primes or log-prime weights. Therefore the Weil explicit formula for zeta does not arise naturally from this substrate.

## Numerical sanity sample

For `R = 1`, the first nonzero eigenvalue magnitudes are `1, 1, 2, 2, 3, 3, ...`. The first zeta-zero ordinates are approximately `14.1347, 21.0220, 25.0109, ...`. No rescaling `R` can transform the full integer lattice into the zeta-zero sequence.
