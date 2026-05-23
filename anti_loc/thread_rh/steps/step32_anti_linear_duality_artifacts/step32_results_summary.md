
# Step 32: Anti-Linear Duality and Zero-Confinement Witnesses

## Main theorem

Let `J` be an involution on a spectral/root-composite index set and let `Fix(J)` be its fixed locus. In the RH-facing case:

```math
J(s)=1-\bar{s},
\qquad
\operatorname{Fix}(J)=\{\Re(s)=1/2\}.
```

An off-fixed orbit `{x,Jx}` produces an anti-invariant witness

```math
y_x=\frac{\delta_x-\delta_{Jx}}{\sqrt2}.
```

If the accepted root-composite currency matrix satisfies

```math
\mathsf K\preceq\Theta
```

and the anti-invariant budget vanishes,

```math
P_-\Theta P_-=0,
```

then every anti-invariant witness has zero capacity:

```math
y^*\mathsf K y=0\quad(y\in Y_-).
```

If the native witness family separates visible off-fixed orbits, this forces all visible spectral support onto the fixed locus.

## Quantitative version

For orthonormal anti-invariant witnesses `y_i`, if each off-fixed orbit carries witness weight `w_i <= y_i^* K y_i`, then:

```math
\sum_i w_i \le \operatorname{tr}(P_-\Theta).
```

Thus a vanishing anti-invariant budget gives asymptotic confinement.

## RH-facing reading

A zero off the critical line yields the anti-invariant signed witness

```math
y_\rho=\frac{\delta_\rho-\delta_{1-\bar\rho}}{\sqrt2}.
```

So the RH-facing anti-localization obligation becomes:

```math
\text{the completed RH carrier has no effective anti-invariant root-composite witnesses.}
```

A sufficient abstract form is:

```math
\mathsf K_-\preceq\Theta_-,
\qquad
\Theta_-\to0
```

on the accepted refinement/closure ledger.

## Key warning

Finite anti-invariant pricing is not exact zero confinement. It controls leakage but does not forbid off-fixed orbits. Exact fixed-locus confinement requires zero/vanishing anti-invariant budget or an additional strict exclusion theorem.

## Layman interpretation

The completed symmetry pairs every off-line zero with its mirror. If the zero is not on the critical line, the pair has a difference signal: “left minus right.” That signal is an anti-invariant witness.

So RH-style confinement can be phrased as:

> the completed carrier must make every left-minus-right off-line witness impossible or vanishingly expensive.

This is not yet RH, but it says exactly what root-composite anti-localization must eliminate.
