# Step 440 Theorem Statement

## Corrected theorem form

**Theorem (Mode A no-go, Dispatch 4).** Let `T` be a Route 2 Hilbert-Polya candidate obtained from Berry-Keating, Sierra-Rodriguez-Laguna, Bender-Brody-Müller, or an analogous phase-space Hamiltonian. Suppose its self-adjoint realization is not native but requires selecting a self-adjoint extension parameter

```text
theta in U(1)   (or more generally U(n)).
```

If the value `theta=theta_zeta` is chosen so that `Spec(T_theta)` matches or is compatible with the Riemann zeta zero ordinates, and if different L-functions require different `theta_chi`, then the map

```text
L_chi -> theta_chi
```

is arithmetic data in the domain of the operator. Therefore the construction violates `C_arithmetic_independence` and `C_self_adjoint_native`.

## Bare Berry-Keating correction

For the natural dilation operator

```text
H_sym = -i(x d/dx + 1/2)
```

on `L^2(R_+)`, the deficiency indices are `(0,0)`, not `(1,1)`. Hence the bare operator supplies no boundary phase to tune. It therefore also fails as a route to zeta zeros, but for a different reason: no adjustable extension parameter is available.

## Final no-go

The Berry-Keating/Sierra/Bender-Brody-Müller class cannot satisfy both conditions simultaneously:

1. arithmetic-independent self-adjoint operator construction;
2. pointwise spectrum equal to zeta-zero ordinates.

Either the operator is native/essentially self-adjoint and has no arithmetic tuning mechanism, or a boundary/extension phase is introduced and selecting it for zeta imports arithmetic target data.
