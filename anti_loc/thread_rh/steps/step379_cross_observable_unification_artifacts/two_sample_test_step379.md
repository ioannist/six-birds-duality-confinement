# Step 379 Two-Sample Test

Samples:

- exceptional Step 377/378 zeros: `[34, 41, 64, 71, 79, 80, 92]` (`n=7`)
- baseline Step 368 zeros: `j=1..15` (`n=15`)

Absolute residual comparison:

- mean `|R|` exceptional: `6.24245689789771241e+00`
- mean `|R|` baseline: `5.88115221898721674e-01`
- ratio exceptional/baseline: `10.614343`
- Welch t statistic on `|R|`: `1.859302`
- Welch df: `6.015813`
- two-sided p-value: `1.12203709956184713e-01`

Signed residual comparison:

- mean `R` exceptional: `6.20236962804306291e+00`
- mean `R` baseline: `-5.33845785365701445e-02`
- signs exceptional: `{'positive': 6, 'negative': 1, 'zero': 0}`
- signs baseline: `{'positive': 8, 'negative': 7, 'zero': 0}`
- Welch t statistic on signed `R`: `2.045194`
- Welch df: `6.047268`
- two-sided p-value: `8.64497635512605639e-02`

Verdict rule: unification requires exceptional mean `|R|` greater than `2x` baseline. Observed ratio is `10.614343`, so this test gives `unification_confirmed_exceptional_residuals_large`.
