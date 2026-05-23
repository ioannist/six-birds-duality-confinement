# Step 371 Integral Derivation Attempt

## Exact inherited integral / kernel structure

Step 172 states the Branch C per-label obligation as:

`L_{rho,k}(G)=<M_zeta G,P_infty y_{rho,k}>`

on the Burnol/Sonine pulled-evaluator carrier.  Step 153 gives the pulled
zero-evaluator identity.  With

`M(f)(s)=pi^{-s/2} Gamma(s/2) fhat(s)`

and with `K_a^Gamma(s,w)` the reproducing kernel of the completed Mellin image
of Burnol's augmented Sonine space, Step 153 records

`M_Gamma(Y^a_{w,k})(s)=partial_{\bar w}^k K_a^Gamma(s,w)`

and

`U_infty(J_a^*Y^a_{w,k}) = T_a^* partial_{\bar w}^k K_a^Gamma(.,w)`.

Thus the actual projected matrix element has the schematic Mellin form

`L_{rho,k}(G)=<M_zeta G, P_infty T_a^* partial_{\bar rho}^k K_a^Gamma(.,rho)>`.

Step 153 also records the ambient Hardy shadow

`K_a^Gamma(.,w)=P_{L_a^Gamma} K_a^{Gamma,amb}(.,w)`

with

`K_a^{Gamma,amb}(s,w)=A_infty(s) overline(A_infty(w)) s/(s-1) overline(w/(w-1)) a^{s+\bar w-1}/(s+\bar w-1)`.

The projection `P_{L_a^Gamma}` is explicitly load-bearing.  Dropping it gives
only a Hardy-shadow formula, not the Burnol/Sonine evaluator.

## What can be derived from the available records

Step 270 provides a Cauchy saddle only for the raw analytic proxy

`delta_Dk(rho,G)=(zeta*M(G))^(k)(rho)`.

For that proxy,

`h^(k)(rho)=k!/(2*pi*i) int h(z)/(z-rho)^(k+1) dz`

and the saddle equation is

`(log h)'(z_*)=(k+1)/(z_*-rho)`.

Step 270 explicitly warns that this saddle is valid for `h=zeta*M(G)`, not
automatically for the projected Branch C quantity, because the actual quantity
is `L_k=delta_Dk-I_k-R_k`.

For the projected Burnol/Sonine element, the formal saddle equation is instead

`partial_s log[M_zeta G(s)] + partial_s log[P_infty T_a^* partial_{\bar rho}^k K_a^Gamma(s,rho)] = 0`

on the critical-line Mellin contour, after choosing a local chart and branch.
The second term is exactly the missing projected-kernel asymptotic.

## Density-based saddle heuristic

The Riemann-von Mangoldt local density at height `T` is

`nu(T)=dN/dT=(1/(2*pi))*log(T/(2*pi))`.

The corresponding mean local zero spacing is

`Delta(T)=1/nu(T)=2*pi/log(T/(2*pi))`.

If the projected kernel saddle is governed by a symmetric half-spacing
excursion from the zero label, the dimensionless action is

`gamma_density(T)=Delta(T)/(2T)=pi/(T*log(T/(2*pi)))`.

This explains the formula selected by Step 370 and ties it to the density of
states.  However, the half-spacing saddle assumption is not proved from
`P_infty T_a^* partial^k K_a^Gamma` in the inherited records.

## Result

The integral records support a partial structural mechanism:

`projected evaluator saddle` -> `local zero-density scale` -> `half-spacing action`.

They do not supply a theorem-grade derivation of the exact prefactor `pi`,
because the large-`k` asymptotic of the load-bearing projected kernel
`P_{L_a^Gamma}K_a^{Gamma,amb}` is absent.
