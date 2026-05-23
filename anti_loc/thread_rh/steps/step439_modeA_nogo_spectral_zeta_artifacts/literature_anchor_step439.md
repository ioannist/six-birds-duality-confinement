# Step 439 Literature Anchor

## Connes 1999

Connes, "Trace formula in noncommutative geometry and the zeros of the Riemann zeta function" (Selecta Mathematica, 1999), constructs a spectral realization of zeta zeros on an adèle/idèle class space. This is an arithmetic substrate, not a non-adelic spectral triple of the Step 436 type.

## Connes-Marcolli

Connes-Marcolli, *Noncommutative Geometry, Quantum Fields and Motives*, develops the spectral triple and spectral action framework used here: an algebra `A`, Hilbert-space representation `H`, and self-adjoint unbounded operator `D` with compact resolvent.

## Standard spectral-triple theory

For a compact spectral triple, the spectral zeta function

```text
zeta_D(s) = Tr |D|^{-s}
```

is tied to the heat trace by Mellin transform. Its pole structure is governed by heat-kernel / Seeley-DeWitt / Connes-Moscovici residue data. Those data describe geometric asymptotics and do not by themselves identify zeta-zero ordinates as operator eigenvalues.

## Step 436 circle counterexample

Step 436 provided the non-adelic circle spectral triple with

```text
zeta_D(s)=2R^s zeta(s),
Spec(D_R)=R^{-1}Z.
```

This is the decisive counterexample for the implication `spectral-zeta match => Hilbert-Polya spectrum`.
