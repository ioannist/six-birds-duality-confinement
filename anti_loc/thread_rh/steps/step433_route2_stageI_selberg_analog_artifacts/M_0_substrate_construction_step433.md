# Step 433 M_0 Substrate Construction

## Choice of substrate

Let `M_0` be a genus-2 compact hyperbolic surface specified by Fenchel-Nielsen coordinates in a Bers/Maskit pants decomposition:

```text
ell_1 = 2,        tau_1 = sqrt(2)/7
ell_2 = 2sqrt(2), tau_2 = sqrt(3)/7
ell_3 = 2sqrt(3), tau_3 = sqrt(5)/7
```

By Fenchel-Nielsen/Bers theory these coordinates determine a compact hyperbolic surface of genus 2. The construction uses only Riemannian/hyperbolic geometry primitives: geodesic lengths, twists, pants gluing, and the hyperbolic metric.

## Non-Arithmetic Reason

The holonomy trace of the cuff with `ell_1=2` is

```text
tr = 2 cosh(ell_1/2) = 2 cosh(1) = e + e^(-1).
```

If `e + e^(-1)` were algebraic, then `e` would satisfy a quadratic polynomial with algebraic coefficients, contradicting Lindemann-Weierstrass. Thus the trace is transcendental. Arithmetic Fuchsian groups have algebraic invariant trace fields; this substrate cannot be arithmetic.

This uses no rational lattices, congruence subgroups, `SL(2,Z)`, modular forms, adeles, ideles, primes, or zeta zeros.

## Numerical Length Sample

The CSV length sample is produced from a local holonomy proxy in the same Bers chart using two hyperbolic generators with translation lengths `2` and `2sqrt(2)` and a generic rotation angle `0.73`. It is a short-word length sample, not a certified complete length spectrum.
