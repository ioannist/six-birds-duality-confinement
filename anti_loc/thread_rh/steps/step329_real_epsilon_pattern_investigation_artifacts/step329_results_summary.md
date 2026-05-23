# Step 329 Results Summary

Verdict: `V_real_epsilon_pattern_confirmed_inside_extrapolated_kernel_not_Burnol_theorem`.

The Step 328 construction uses the completed Dirichlet L-function as `E_chi` in Burnol's two-term kernel shape
`(E(z)conj(E(w)) - E(1-z)conj(E(1-w)))/(z+conj(w)-1)`.
For real self-dual characters with epsilon = 1, the sampled numerator cancels to numerical zero. For non-self-dual characters, it does not.

Additional character outcomes:
- `chi_7b`: status `valid_new_order_6`, epsilon `0.386513572759155288186919+0.922283718859306965671514j`, max|kappa| `1.89858770177713474`.
- `chi_8b`: status `invalid_requested_character_no_order_4_character_mod_8`, epsilon `NA`, max|kappa| `NA`.
- `chi_11c`: status `valid_new_order_10`, epsilon `0.957620076587575619739039+0.288034353708730036260581j`, max|kappa| `2.41738998266287439`.
- `chi_13a`: status `valid_new_quadratic_control`, epsilon `1.0-2.92387963387758904631304e-81j`, max|kappa| `2.13112518643226391e-81`.

Largest self-dual max|kappa| among valid tested rows: `2.13112518643e-81`.
Smallest non-self-dual max|kappa| among valid tested rows: `0.212755567375`.

`chi_8b` was requested as a primitive order-4 character mod 8, but no such character exists because `(Z/8Z)^x` has exponent 2.

Interpretation: the pattern is a structural property of the Step 328 extrapolated kernel symmetry. Since the Dirichlet-twisted kernel itself is not explicitly supplied by Burnol in this finite form, this is not a paper-grounded theorem about Burnol-Sonine projections.
