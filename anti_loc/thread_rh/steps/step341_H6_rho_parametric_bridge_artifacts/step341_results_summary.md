# Step 341 Results Summary

Constructive rho-parametric multiplicative H6 bridge test:
`log|L_k(rho,G_star)| = c0 + c1 T + c2 log T + sum_chi (a0_chi+a1_chi T) log|L_k^chi|`.

Prior-step extracts used verbatim:
- Step 320: `h_chi(s)=L(s,chi) M(G_star)(s)` and `M(G_star)(s)=int G_star(t) t^{-s} dt`.
- Step 339: product bridge passed rho_1 holdout through k=20.
- Step 340: fixed Step 339 coefficients failed rho_2 with max residual `0.935983109276`; even rho_2-specific intercept failed with max residual `3.08309698613`.

rho_3 actual values k=1..20:
- k=1: `0.242197270518363877`
- k=2: `0.890336695283949164`
- k=3: `2.55111377300433437`
- k=4: `6.77194002120196141`
- k=5: `17.4844174815515589`
- k=6: `44.7135471562087255`
- k=7: `114.149737887428086`
- k=8: `291.971218985252544`
- k=9: `749.522241812479791`
- k=10: `1932.60752705489886`
- k=11: `5006.52972520683465`
- k=12: `13030.7970645979647`
- k=13: `34072.0319202863234`
- k=14: `89484.2141811014816`
- k=15: `236014.579001549868`
- k=16: `625030.555260102793`
- k=17: `1661756.09352564627`
- k=18: `4434856.39033683893`
- k=19: `11879268.4348626261`
- k=20: `31934302.0199024965`

Design rank from SVD least squares: `16` of `17` columns; condition estimate `3.068330e+18`.
Training max residual over rho_1/rho_2, k=1..10: `3.34042888598e-5`.
rho_3 holdout max residual over k=1,5,10,15,20: `2.62794210281`.

Final verdict: `V_H6_rho_parametric_bridge_cross_rho3_fails`.
Runtime: `83.359` seconds.
