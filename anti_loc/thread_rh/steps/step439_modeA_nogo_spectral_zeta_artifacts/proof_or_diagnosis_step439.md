# Step 439 Proof

## 1. Circle spectral triple computation

Let `A=C^infty(S^1)` act on `H=L^2(S^1)` by multiplication and let

```text
D_R = -i R^{-1} d/dtheta
```

on the standard Sobolev domain `H^1(S^1)`. The Fourier modes `e^{in theta}` are eigenvectors and

```text
D_R e^{in theta} = (n/R) e^{in theta}.
```

Removing the zero mode,

```text
zeta_D(s) = sum_{n != 0} |n/R|^{-s}
          = 2 R^s sum_{n>=1} n^{-s}
          = 2 R^s zeta(s).
```

The construction is non-adelic: it uses only the smooth circle, its `L^2` spinor space, and the Dirac operator.

## 2. Spectrum mismatch

The positive spectrum of `|D_R|` is `{n/R : n>=1}` with multiplicity 2. Equivalently, `Spec(D_R)=R^{-1}Z` before taking absolute values. The first zeta-zero ordinates are approximately

```text
14.134725..., 21.022039..., 25.010858..., 30.424876..., ...
```

No fixed lattice scale `R` can make `{n/R}` equal this sequence: matching the first two would require `gamma_2/gamma_1 = 2`, but numerically `gamma_2/gamma_1 ~= 1.4873`.

Therefore exact spectral-zeta proportionality does not imply pointwise Hilbert-Polya spectral identity.

## 3. Structural point

Exact spectral zeta data can encode substantial information about `|D|` under standard discreteness hypotheses, but it encodes the eigenvalue magnitudes whose Dirichlet series is being summed. In the counterexample, that encoded spectrum is the integer lattice. It is not the zero-ordinate spectrum. Heat-kernel pole data and Seeley-DeWitt coefficients are even weaker: they record asymptotic geometric invariants, not the full pointwise spectrum.

## 4. Connes comparison

Connes 1999 uses an adelic/idèle class construction precisely because non-adelic spectral-zeta coincidences such as the circle triple do not produce the zero ordinates as a self-adjoint spectrum. The adelic substrate supplies arithmetic trace-formula content, but it violates `C_no_adelic_substrate` for the active Route 2 grammar.

## Verdict

`C_spectral_zeta_not_spectrum` is theorem-grade: spectral-zeta equality, even exact and non-adelic, is structurally insufficient for Hilbert-Polya pointwise spectral realization.
