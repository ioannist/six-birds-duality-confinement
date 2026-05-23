# Step 371 Results Summary

The exact inherited Branch C matrix element is

`L_{rho,k}(G)=<M_zeta G,P_infty y_{rho,k}>`.

Step 153 identifies the pulled evaluator as

`U_infty(J_a^*Y^a_{w,k})=T_a^* partial_{\bar w}^k K_a^Gamma(.,w)`.

So the projected integral is governed by

`P_infty T_a^* partial_{\bar rho}^k K_a^Gamma(.,rho)`.

The available records do not contain the large-`k` asymptotic of this
load-bearing projected kernel.  Step 270 gives only the raw-proxy saddle

`(log h)'(z_*)=(k+1)/(z_*-rho)`

for `h=zeta*M(G)`, and explicitly says this is not automatically the projected
Branch C saddle.

The partial derivation is:

`nu(T)=dN/dT=log(T/(2*pi))/(2*pi)`,
`Delta(T)=1/nu(T)=2*pi/log(T/(2*pi))`,
and a symmetric projected-kernel half-spacing saddle gives

`gamma(T)=Delta(T)/(2T)=pi/(T*log(T/(2*pi)))`.

Numerical check against the Step 324 15-zero gamma data gives zero-parameter
height-law RMSE `0.023707`.  Step 370's fit with a free spacing term gave
RMSE `0.015480`, and the four-parameter Step 324 model gave `0.014046`.

Verdict: `partial_density_saddle_mechanism_identified_exact_projected_kernel_asymptotic_missing`.

This is not a theorem-grade Branch C height law.  The named missing external
piece is an explicit large-`k` stationary-phase expansion for the projected
Burnol/Sonine kernel `P_infty T_a^* partial^k K_a^Gamma`.
