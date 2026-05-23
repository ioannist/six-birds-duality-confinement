# Step 412 Cross-Selberg Hadamard Summary

## Inherited Statements Cited

- Step 381: ζ-side close-pair Hadamard mechanism identified `7/7` exceptional zeros.
- Step 389: `L(s, chi_3)` had `48/50` negative and `2` exceptional zeros.
- Step 411: `L(s, chi_3)` close-pair term identified `2/2` exceptional zeros, but matched only `10/48` non-exceptional baseline zeros.

## Characters Tested

The new characters were:

```text
chi_4 mod 4: L(s, chi_4) = 4^(-s) * (zeta(s,1/4) - zeta(s,3/4)).
chi_5 mod 5 real quadratic: L(s, chi_5) = 5^(-s) * (zeta(s,1/5) - zeta(s,2/5) - zeta(s,3/5) + zeta(s,4/5)).
```

For both, the first `30` critical-line zeros were computed using the Step 389 style two-dimensional root refinement.

## New Results

| L-function | zeros | exceptional `Re L'' >= 0` | exceptional j | exception matches | non-exception matches | predicted positive |
|---|---:|---:|---|---:|---:|---:|
| `L(s, chi_4)` | 30 | 1 | 30 | 0/1 | 3/29 | 26/30 |
| `L(s, chi_5)` | 30 | 3 | 11;22;28 | 3/3 | 3/27 | 27/30 |

The `chi_4` exception at `j=30` is a counterexample to the close-pair-only exception predictor: actual `Re L''` is positive, while `Re L''_near` is negative.

## Aggregate Exception Detection

| source | exception match |
|---|---:|
| ζ, Step 381 | 7/7 |
| `L(s, chi_3)`, Step 411 | 2/2 |
| `L(s, chi_4)`, Step 412 | 0/1 |
| `L(s, chi_5)`, Step 412 | 3/3 |
| total | 12/13 = 92.31% |

## Interpretation

The exception-detection rate remains above the requested `90%` threshold across four L-functions, so the close-pair Hadamard mechanism has strong cross-family support as an exception detector.

However, it is not a full sign classifier. For the new characters, it predicts positive signs for `53/60` zeros while only `4/60` are actually exceptional. Regular Hadamard terms, conductor/parity data, and archimedean factors are essential for the baseline sign.
