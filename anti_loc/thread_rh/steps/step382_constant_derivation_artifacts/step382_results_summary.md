# Step 382 Results Summary

Derivation chain:

1. Hadamard: `g'_near = +/- i/s_min`.
2. Branch C saddle: close-pair correction enters `Re(g'_near delta z*)`.
3. Therefore `R_j` has the form `C0 + C1/s_min`.
4. Step 381 fit gives `C1=10.17670932369573`, `C0=-4.472883537971084`.

Slope:

- best structural candidate: `pi^2 = 9.86960440108935862`
- empirical: `10.176709323695727`
- relative error: `0.0301772324273129153794689619087`

Offset:

- structural candidate: `-3pi/2 = -4.71238898038468986`
- empirical: `-4.472883537971084`
- relative error: `0.0535460940085746977810798124296`

Best purely numerical slope candidate is `pi^2+1/3` and best numerical offset candidate is `-sqrt(20)`, but these are not accepted as structural without a derivation.

Verdict: `partial_constants_match_pi2_and_minus_3pi_over_2; saddle_displacement_unproved`. Both proposed structural constants are within 10%, but the Burnol/Sonine saddle displacement and regular Hadamard remainder are not yet derived rigorously.
