# Step 430 Residual Statistics

## Audit Convention

The user-specified `410` rows are represented as:

- `384` zeta exceptional zeros through `j <= 2000` from steps 426 and 428.
- `26` step-422 cross-family anchor rows. This inherited 26-row set contains `7` zeta anchors and `19` Dirichlet rows; the seven zeta anchors are duplicates of cells already included in the zeta n=2000 set. Thus the unique mathematical cells are `403`, while the requested audit table has `410` rows.

## Counts

- Total audit rows tested: `410`.
- `zeta_n2000`: `384`.
- `step422_cross_family_anchor`: `26` (`7` zeta anchors + `19` Dirichlet rows).
- Residuals below `1e-30`: `410/410`.

## Residuals

| component | count | max abs residual | mean abs residual | <1e-30 |
|---|---:|---:|---:|---:|
| zeta_n2000 | 384 | 1.46522045783e-36 | 5.62441802311e-37 | 384/384 |
| step422 anchors | 26 | 1.5602452956e-79 | 4.67911401019e-80 | 26/26 |
| anchor Dirichlet rows | 19 | 1.26506375319e-79 | 3.3513092409e-80 | 19/19 |
| all audit rows | 410 | 1.46522045783e-36 | 5.26774761189e-37 | 410/410 |

## By Component And Character

| component | character | count | max abs residual | mean abs residual | <1e-30 |
|---|---|---:|---:|---:|---:|
| `step422_cross_family_anchor` | `chi_11` | 4 | 2.74097146524e-80 | 1.58132969148e-80 | 4/4 |
| `step422_cross_family_anchor` | `chi_13` | 3 | 1.68675167092e-80 | 1.47590771205e-80 | 3/3 |
| `step422_cross_family_anchor` | `chi_15` | 1 | 0.0 | 0.0 | 1/1 |
| `step422_cross_family_anchor` | `chi_3` | 2 | 1.26506375319e-79 | 1.04367759638e-79 | 2/2 |
| `step422_cross_family_anchor` | `chi_4` | 1 | 4.42772313616e-80 | 4.42772313616e-80 | 1/1 |
| `step422_cross_family_anchor` | `chi_5` | 3 | 7.1686946014e-80 | 3.93575389881e-80 | 3/3 |
| `step422_cross_family_anchor` | `chi_7` | 4 | 2.9518154241e-80 | 1.9503066195e-80 | 4/4 |
| `step422_cross_family_anchor` | `chi_8` | 1 | 8.01207043686e-80 | 8.01207043686e-80 | 1/1 |
| `step422_cross_family_anchor` | `zeta` | 7 | 1.5602452956e-79 | 8.28315552682e-80 | 7/7 |
| `zeta_n2000` | `zeta` | 384 | 1.46522045783e-36 | 5.62441802311e-37 | 384/384 |

## Formula Verified

Step 429 phase-line formula used verbatim:

```text
Arg L'(rho, chi) = -Arg(i F_chi(rho)) (mod pi)
```
