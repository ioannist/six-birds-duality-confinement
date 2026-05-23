# Step 371 Saddle Equation

## Raw proxy saddle inherited from Step 270

For `h(z)=zeta(z) M(G)(z)`,

`h^(k)(rho)=k!/(2*pi*i) int h(z)/(z-rho)^(k+1) dz`

and the stationary equation is

`(log h)'(z_*)=(k+1)/(z_*-rho)`.

This is valid for the raw proxy `delta_Dk=(zeta*M(G))^(k)(rho)`.

## Projected Branch C saddle

For the actual Branch C matrix element,

`L_{rho,k}(G)=<M_zeta G, P_infty T_a^* partial_{\bar rho}^k K_a^Gamma(.,rho)>`.

Writing the critical-line Mellin variable as `s=1/2+i tau`, a formal stationary
condition for the modulus of the integrand is

`partial_tau log |M_zeta G(1/2+i tau)|`
`+ partial_tau log |P_infty T_a^* partial_{\bar rho}^k K_a^Gamma(1/2+i tau,rho)| = 0`.

Equivalently, in a complex local chart,

`partial_s log[M_zeta G(s)] + partial_s log[P_infty T_a^* partial_{\bar rho}^k K_a^Gamma(s,rho)] = 0`.

The missing term is the asymptotic expansion of

`P_infty T_a^* partial_{\bar rho}^k K_a^Gamma(s,rho)`.

## Heuristic density solution

Using only the zero-density scale, the local density is

`nu(T)=log(T/(2*pi))/(2*pi)`,

so the mean spacing is

`Delta(T)=2*pi/log(T/(2*pi))`.

The half-spacing projected-kernel excursion gives

`|tau_*-T| approx Delta(T)/2 = pi/log(T/(2*pi))`.

Dividing by the height scale `T` gives the heuristic action coefficient

`gamma(T) approx |tau_*-T|/T = pi/(T*log(T/(2*pi)))`.

This is the saddle solution used for the numerical comparison, but it remains a
density-saddle heuristic until the projected-kernel asymptotic is proved.
