# Step 182: Hilbert-Polya / Berry-Keating Carrier Pivot

Verdict:

`HP_verdict = V_HP_meta_pattern_confirmed`.

Carrier declaration:

Use the standard Berry-Keating half-line carrier

```tex
H_HP = L^2(R_+, dx),
\qquad
H_xp = (xp+px)/2 = -i(x d/dx + 1/2).
```

The natural unitary

```tex
(Uf)(t)=e^{t/2}f(e^t), \qquad U:L^2(R_+,dx)->L^2(R,dt),
```

conjugates `H_xp` to the momentum operator

```tex
U H_xp U^{-1} = -i d/dt.
```

On the full half-line carrier, the closure has domain
`U^{-1}H^1(R)`, is self-adjoint, and has purely absolutely continuous
spectrum `R`. It has no point spectrum equal to the zeta ordinates. On a
finite logarithmic interval, `-i d/dt` has a `U(1)` family of extensions with
arithmetic spectrum `(2 pi n + theta)/L`, again not the zeta ordinates.

Parent residual:

`Xi_HP` is the typed spectral-defect residual: it vanishes only if a declared
self-adjoint HP operator has eigenvalue ledger `{gamma_n}` with multiplicity
matching the nontrivial zeta zeros. For the standard `H_xp`, this residual is
not closable because the spectral type is continuous. For modified HP/BK
operators, exact closure is the Hilbert-Polya conjecture itself and is
target-equivalent.

New no-go:

`Hilbert-Polya/Berry-Keating standard xp bridge failure and modified-operator target-equivalence`.

Meta-pattern status:

`meta_pattern_confirmed`. The three classical RH-equivalent pivots now show
typed no-go foreclosure: Hecke H6 bridge non-comparability, de Branges
target-equivalence, and HP/BK standard-xp bridge failure / modified-operator
target-equivalence.
