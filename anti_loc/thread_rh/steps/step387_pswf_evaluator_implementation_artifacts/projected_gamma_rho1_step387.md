# Step 387 Projected Gamma at rho_1

## Implementation
- PSWFs: `scipy.special.pro_ang1(0,n,c,x)` with `c=pi*T_1`, normalized on 256 Gauss-Legendre nodes over `[-1,1]`.
- Kernel: Auvray-Ma-Marinescu punctured-disc proxy `B_p^{D*}(R)=R^p/(2*pi*(p-2)!)*sum ell^(p-1) exp(-R ell)` with `p=k+2`.
- Coordinate: standard local PSWF coordinate with height window `1/(2*pi)`; exact `U_infty` Sonine/Mellin transport is not applied.

## Components
- k=5: |L_projected_proxy|=4.23295252667866357e-63
- k=10: |L_projected_proxy|=1.38864909631565645e-52
- k=15: |L_projected_proxy|=2.69194426687216611e-43

Fitted proxy gamma from `log|L|=a-gamma*k`: `-4.55990658217845368e+00`.
Fit RMSE in log-space: `6.66723803091416101e-01`.
Structural comparator `pi/(T_1 log(T_1/(2pi)))`: `2.74139452528282535e-01`.
Relative error: `1.76335291769360154e+01`.

Verdict: `proxy_mismatch_structural_law_not_reproduced`.
