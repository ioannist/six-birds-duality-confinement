# Step 385 P_infty Kernel Form Attempt

From Step 173, in the log-Mellin model on `s=1/2+i tau`,

`P_infty = S_lambda`

with

`S_lambda = I - P_lambda - sum_n |u_n><u_n|`,

where

`u_n = (I-P_lambda)phi_n^lambda / sqrt(1-mu_n)`,

and `QP_lambda Q phi_n^lambda = mu_n phi_n^lambda`.

Transported to the Mellin line, this gives the operational kernel

`K_infty^op(s,s') = delta(tau-tau') - sinc_lambda(tau-tau') - sum_n Psi_n^lambda(s) conjugate(Psi_n^lambda(s'))`,

where

`sinc_lambda(x)=sin(lambda x)/(pi x)`.

Thus for any Mellin-side vector `F`,

`(P_infty F)(s) = F(s) - (P_lambda F)(s) - sum_n Psi_n^lambda(s) <F,Psi_n^lambda>`.

The Branch C vector is

`eta_{rho,k}=T_a^* partial_{\bar rho}^k K_a^Gamma(.,rho)`.

Therefore

`P_infty eta_{rho,k}(s) = eta_{rho,k}(s) - P_lambda eta_{rho,k}(s) - sum_n Psi_n^lambda(s) c_{n,k}(rho)`,

with

`c_{n,k}(rho)=<T_a^* partial_{\bar rho}^k K_a^Gamma(.,rho), Psi_n^lambda>`.

This is explicit enough to define the projection action, but not enough to extract a closed large-`k` scale. The missing object is the asymptotic of `c_{n,k}(rho)` uniformly through the PSWF transition range.
