# Step 440 Deficiency Index Computation

## Bare Berry-Keating dilation operator

Let

```text
H_sym = (x p + p x)/2 = -i (x d/dx + 1/2)
```

on `L^2(R_+, dx)` with natural dense domain `C_c^infty(R_+)`.

Use the unitary logarithmic transform

```text
u = log x,
(U psi)(u) = exp(u/2) psi(exp u),
U : L^2(R_+, dx) -> L^2(R, du).
```

Then

```text
U H_sym U^{-1} = -i d/du
```

on `C_c^infty(R)`. The momentum operator `-i d/du` on the full line is essentially self-adjoint. Hence the natural bare dilation operator has

```text
(n_+, n_-) = (0, 0).
```

The same conclusion follows from the deficiency equations. For `(H_sym^* - i) psi = 0`,

```text
x psi' + 3/2 psi = 0  ->  psi = C x^{-3/2},
```

which is not in `L^2(R_+)` near `0`. For `(H_sym^* + i) psi = 0`,

```text
x psi' - 1/2 psi = 0  ->  psi = C x^{1/2},
```

which is not in `L^2(R_+)` near infinity. Thus both deficiency spaces are zero-dimensional.

## Consequence

The inherited shorthand claim that the bare `H_sym` has deficiency indices `(1,1)` on `L^2(R_+)` is not correct for the natural full half-line dilation operator. This correction strengthens the no-go:

- Bare `H_sym`: no `U(1)` tuning parameter exists, so it cannot be tuned to zeta zeros.
- Modified/cutoff Berry-Keating/Sierra/Bender-Brody-Müller models: if a nontrivial boundary or extension phase is introduced, that phase is part of the operator definition. Choosing it from zeta/L-function data is arithmetic input.

## von Neumann extension theorem

For any symmetric operator `T` with deficiency indices `(n,n)`, self-adjoint extensions are parameterized by `U(n)`. In the common `(1,1)` case, the family is `U(1)`, i.e. a phase `theta`. The no-go theorem targets exactly the Route 2 use of such `theta` as a selector for zeta or Dirichlet L-function spectra.
