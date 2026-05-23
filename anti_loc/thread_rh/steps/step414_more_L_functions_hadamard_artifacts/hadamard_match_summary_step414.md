# Step 414 Hadamard Match Summary

## Inherited Statements Cited

- Step 381: ζ-side close-pair Hadamard mechanism identified `7/7` exceptional zeros.
- Step 389: `L(s, chi_3)` empirical sign table had `2` exceptions in 50 zeros.
- Step 411: `L(s, chi_3)` close-pair term identified `2/2` exceptional zeros.
- Step 412: `L(s, chi_4)` and `L(s, chi_5)` were added.
- Step 413: the apparent `chi_4` miss was a boundary truncation artifact; after adding `T31`, the close-pair mechanism is restored.

## New Characters

Real primitive quadratic characters were used:

```text
chi_7: Legendre symbol mod 7.
chi_8: Kronecker character (8/n), values +1 on 1,7 mod 8 and -1 on 3,5 mod 8.
chi_11: Legendre symbol mod 11.
```

For each character, `31` zeros were computed and the first `30` were tested. The extra zero supplies forward-neighbor coverage and avoids the Step 412 boundary artifact.

## New Results

| L-function | tested zeros | stored zeros | exceptional zeros | exceptional j | Hadamard exception match | non-exception match | predicted positive |
|---|---:|---:|---:|---|---:|---:|---:|
| `L(s, chi_7)` | 30 | 31 | 4 | 10;17;25;26 | 4/4 | 3/26 | 27/30 |
| `L(s, chi_8)` | 30 | 31 | 1 | 24 | 1/1 | 3/29 | 27/30 |
| `L(s, chi_11)` | 30 | 31 | 4 | 4;11;21;28 | 4/4 | 5/26 | 25/30 |

## Aggregate

Inherited:

```text
zeta + chi_3 + chi_4 + chi_5 = 13/13 exceptional matches.
```

New:

```text
chi_7 + chi_8 + chi_11 = 9/9 exceptional matches.
```

Total:

```text
22/22 exceptional matches = 100%.
```

## Interpretation

The close-pair Hadamard mechanism remains perfect as an exception detector across the tested family. It is still not a complete sign classifier: among the 90 newly tested zeros, the predictor marked `79` positive signs while only `9` were actually exceptional. The missing piece is baseline suppression by the regular Hadamard remainder and archimedean/conductor terms.
