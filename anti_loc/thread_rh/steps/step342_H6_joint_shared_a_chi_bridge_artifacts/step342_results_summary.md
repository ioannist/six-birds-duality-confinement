# Step 342 Results Summary

Joint shared-exponent multiplicative H6 fit:
`log|L_k(rho_j,G_star)| = b0(rho_j) + sum_chi a(chi) log|L_k^chi|`.

Prior-step extracts used verbatim:
- Step 320: `h_chi(s)=L(s,chi) M(G_star)(s)` and `M(G_star)(s)=int G_star(t) t^{-s} dt`.
- Step 339: product bridge passed rho_1 holdout with max residual `0.00893202095224`.
- Step 340/341: rho-cross tests showed single-rho coefficients and richer rho-parametric coefficients did not generalize.

Design rank: `10` of `10`; condition estimate `2.888656e+07`.
Max training residual over 30 cells: `0.826955557461`.
- rho_1: max `0.826955557461`, mean `0.348198539745`
- rho_2: max `0.211046413824`, mean `0.107793323489`
- rho_3: max `0.686238362188`, mean `0.245604642378`
rho_4 b0 calibrated at k=10: `3.24417739619`.
rho_4 k=20 holdout residual: `0.677749032941`.

Final verdict: `V_H6_joint_shared_a_chi_training_fails`.
Runtime: `88.594` seconds.
