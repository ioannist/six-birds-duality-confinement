# Step 445 Scope and Capacity Specification

## Declared zeta scope

- Native strip: `0 <= Re(s) <= 1`, `|Im(s)| <= 51`.
- Nontrivial zeros in declared scope: first 10 zeta zeros.
- Trivial zeros in scope: `-2, -4, -6, -8`.

| j | scoped nontrivial zero |
|---:|---|
| 1 | 1/2 + 14.1347251417346938 i |
| 2 | 1/2 + 21.022039638771555 i |
| 3 | 1/2 + 25.0108575801456888 i |
| 4 | 1/2 + 30.4248761258595132 i |
| 5 | 1/2 + 32.9350615877391897 i |
| 6 | 1/2 + 37.5861781588256713 i |
| 7 | 1/2 + 40.9187190121474952 i |
| 8 | 1/2 + 43.3270732809149995 i |
| 9 | 1/2 + 48.0051508811671597 i |
| 10 | 1/2 + 49.7738324776723022 i |

## Three-component grammar

`G_closure_only_no_audit` uses

```text
P' = (K^L, Xi, [K^D + S])
```

There is no separate audit-currency component.

## Theta^D specification

`Theta^D` is a finite Loewner bound on the transported dissolving currency:

```text
S K^D S^* <= Theta^D.
```

This specification is **not** by itself stated as `all zeros lie on the critical line`; it is a matrix capacity bound. If one strengthens it to mean exactly zero-localization on the critical line, it becomes an implicit audit/RH-equivalent semantic predicate. That tension is the falsification point of this attempt.

## Native and dissolving probes

Native probes: functional-equation center, gamma-factor parity, finite symmetric-layer Schur probes, conductor-1 metadata.

Dissolving probes: finite formal zero-localization probes. Their matrix currencies are constructed without zeta-values, primes, modular forms, adeles, or L-special values.


Marker: The finite matrix specification is not RH-equivalent on its own; only an added semantic interpretation would make it RH-equivalent.
