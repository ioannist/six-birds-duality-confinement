# Step 343 Results Summary

Computed Branch C zeta-side `|L_k(rho_j,G_star)|` for `rho_1..rho_5`, k=1..20, using the same Leibniz evaluator as Steps 340--342.

Prior-step extracts used verbatim:
- Step 269/304: `rho_1` reference includes k=1 around `0.289`, k=10 `165.44`, k=20 `554847`.
- Step 340: `rho_2` k=10 `667.785`, k=20 `8.74e6`.
- Step 341: `rho_3` full k=1..20 table is used as the consistency reference; conflicting inherited high values are not forced.

Selected ratio spreads r_j(k)=|L_k(rho_j)|/|L_k(rho_1)| over k=1,2,3,5,10,15,20:
- rho_2: min `0.98857564`, max `15.760403`, max/min `15.942537`
- rho_3: min `1.5256905`, max `57.555148`, max/min `37.724`
- rho_4: min `1.6083124`, max `203.83208`, max/min `126.73662`
- rho_5: min `1.0894303`, max `306.89967`, max/min `281.70655`

Best selected-k candidate by average max relative error: `pure_height_ratio_r=(T/T1)^f` with average max-relative `0.288886`.
No candidate is uniformly accurate: ratios vary strongly with k and with the zero index.

Final verdict: `V_zeta_internal_ratio_no_clean_form`.
Runtime: `31.109` seconds.
