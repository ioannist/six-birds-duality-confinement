# Step 344 Results Summary

Repeated the Step 339 multiplicative H6 bridge with `G_prime`.

Prior-step extracts used verbatim:
- Step 339 G_star coefficients: `b0=-2.40963`, `sum a=1.041`, holdout k=20 residual `0.89%`.
- Step 331/333 certified G_prime zeta-side values are recomputed here with the same dps=80 Leibniz evaluator.
- Step 320/322/329 roots are used for the seven character carriers.

Sample `|L_k^chi(rho_chi,G_prime)|` at k=10:
- chi_3: `1090.67184523327299`
- chi_4: `992.162207887616321`
- chi_5a: `3130.44330300883843`
- chi_5b: `2258.98820534360316`
- chi_7b: `3595.65918840640062`
- chi_11c: `3662.77081085843231`
- chi_13a: `4493.45750786509936`

G_prime intercept b0': `-2.67495717463`.
G_prime exponent sum: `0.767396971929`.
Training max residual k=1..10: `4.89549760178e-6`.
Holdout max residual k=11/12/15/20: `0.0313956916477`.
All exponents within 50% of G_star coefficients: `False`.

Final verdict: `V_H6_multiplicative_G_prime_holdout_fails`.
Runtime: `62.544` seconds.
