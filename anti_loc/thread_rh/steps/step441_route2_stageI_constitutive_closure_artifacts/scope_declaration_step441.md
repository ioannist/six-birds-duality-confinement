# Step 441 Scope Declaration

This is STEP 441 -- Route 2 Stage I under `G_constitutive_closure`, first carrier attempt.

## Declared finite zeta-scope

- Strip: `0 <= Re(s) <= 1`, `|Im(s)| <= 51.0`.
- Nontrivial zero scope: first 10 nontrivial zeros of zeta.
- Trivial zero scope: `-2, -4, -6, -8`.

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

The zero ordinates are declared as the external audit scope only. They are not legal construction primitives for `M` or `A`.

## Native layer L

`L` is the functional-equation-symmetric layer of the completed zeta expression: conductor 1, gamma factor `pi^(-s/2) Gamma(s/2)`, symmetry `xi(s)=xi(1-s)`, and finite symbolic probe records on the strip.

Native probe family used in this attempt:

1. `l_0`: Schur-square fixed-center probe `Re(s)-1/2`.
2. `l_1`: gamma-factor pole/cancellation parity probe for trivial zeros.
3. `l_2`: finite Loewner budget probe from the native membrane.
4. `l_3`: formal symmetry-pair probe `s <-> 1-s`.

## Dissolving layer D

`D` is zero-localization on `Re(s)=1/2` in the same strip. Dissolving probes are formal finite probes sensitive to:

1. candidate critical-line membership,
2. candidate height localization,
3. residue/contour-style zero-local response.

## SAU / NDO signature

The package uses the NDO certificate shape from the SAU paper:

```text
[U not_down_q, C(U) down_B a^sharp]
```

The declared carrier tries to make `(M,A,R,T)` the promoted support and the finite zero-local audit record the descended `a^sharp`.
