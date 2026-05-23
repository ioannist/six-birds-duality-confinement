# Step 340 Results Summary

Cross-rho robustness test for the Step 339 product-form H6 bridge candidate.

Prior-step extracts used verbatim:
- Step 305: certified rho_2 checks include `667.785` at k=10 and about `8.74e6` at k=20.
- Step 320: `h_chi(s)=L(s,chi) M(G_star)(s)` and `M(G_star)(s)=int G_star(t) t^{-s} dt`.
- Step 339: fitted product coefficients with `b0=-2.40963`, exponent sum `1.04073`, and holdout max residual `0.00893202095224` at rho_1.

Actual rho_2 target values:
- k=1: `0.156932434070174603`
- k=2: `0.447448762557034548`
- k=3: `1.07009800716785016`
- k=5: `6.16328034252697333`
- k=10: `667.784977579807984`
- k=15: `75532.1352971284619`
- k=20: `8744612.78570535797`

Fixed Step 339 b0 max residual on rho_2: `0.935983109276`.
Rho_2-specific b0 calibrated at k=10: `-1.01426434274`; delta from Step 339 b0: `1.39536564945`.
Shared a(chi) with rho_2-specific b0 max residual: `3.08309698613`.

Interpretation: the exponent vector is not enough with the original rho_1 intercept. A rho_2-specific intercept calibrated at k=10 also fails cross-k consistency, so the Step 339 product bridge is rho-specific rather than structurally cross-rho robust.

Final verdict: `V_H6_multiplicative_bridge_cross_rho_fails`.
Runtime: `70.229` seconds.
