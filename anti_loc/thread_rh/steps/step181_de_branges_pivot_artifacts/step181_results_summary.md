# Step 181: de Branges Carrier Pivot

Verdict:

`dB_verdict = V_dB_target_equivalent`.

Carrier declaration:

Let

```tex
xi(s)=1/2 s(s-1) pi^{-s/2} Gamma(s/2) zeta(s),
Xi(t)=xi(1/2+it).
```

A de Branges RH carrier would require a Hermite-Biehler function

```tex
E_zeta(z)=A_zeta(z)-iB_zeta(z),   A_zeta(z)=Xi(z),
```

or a unitarily equivalent normalization.  The de Branges space `H(E_zeta)` has
kernel

```tex
K_E(z,w)
= [E(z) overline{E(w)} - E#(z) overline{E#(w)}]
  / [2 pi i (overline{w}-z)].
```

The problem is that the required `E_zeta` is not free data: the existence of a
Hermite-Biehler companion and/or the de Branges chain positivity condition is
the classical de Branges RH route.  Using it as a closure mechanism would be
target-equivalent to RH.

Inherited records:

- Step 145 gives Burnol/Sonine `L_a`, not a concrete de Branges `E`.
- Step 153 gives `L_a^Gamma` as an RKHS with projected kernel, but not an
  explicit `E`.
- `anti_loc/adequacy.tex` and `anti_loc/needles.tex` contain no de Branges
  carrier package.
- Step 90 and Step 93 carry the de Branges/RKHS warning: de Branges kernels
  are carrier candidates, and Conrey-Li refutes natural de Branges-type zeta
  positivity shortcuts.

New no-go:

`de Branges RH-carrier closure target-equivalence / Conrey-Li survival`.

Implication: the de Branges pivot does not offer a non-CTMT free route. It is
a typed target-equivalence no-go unless an explicitly scoped, non-naive,
non-target-equivalent de Branges carrier is supplied in a later step.
