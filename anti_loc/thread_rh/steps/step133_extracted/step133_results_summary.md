# Step 133: Omega-truncated Dirichlet-polynomial architecture for GCD-log blind-sector suppression

## Purpose
Step 130 showed that the unrestricted BPRZ shifted-main-term kernel has squarefree Boolean near-null directions. Step 131 showed that the actual zeta/Müntz residual class may avoid those directions because zeta incidence convolution makes deep blind modes read only high-divisibility seed coefficients. Step 132 proved the finite Boolean mechanism.

Step 133 imports the Heap--Soundararajan Omega-block architecture as the standard analytic-number-theory template for controlling those high-divisibility seed tails.

## Main result
For a blind Walsh family B with upward closure up(B),

    Pi_B Z_y b = Pi_B Z_y P_up(B) b.

Therefore the GCD-log blind overlap is bounded by the zeta-convolved high-divisibility tail of the seed. If the seed is exactly supported below the blind threshold, the blind modes vanish exactly. If not, the residual is a declared Omega-tail defect.

## Heap--Soundararajan import
HS use prime blocks, truncated Omega counts, and short Dirichlet polynomials N(s, alpha) that mimic zeta powers while keeping length under control. In the framework, this supplies a non-smuggled architecture for declaring cutoffs K_j and controlling high-Omega tails. It does not by itself prove the operator lower frame.

## Conditional salvage of BPRZ
If the GCD-log kernel has lower bound gamma_q on the nonblind class and the actual residual coefficient image has blind overlap delta_N, then

    <Zb, K_q Zb> >= gamma_q (1 - delta_N^2) ||Zb||^2.

A positive floor delta_N < 1 is enough when gamma_q diverges; exact delta_N -> 0 is sufficient but stronger than needed.

## Remaining hard input
The new analytic obligation is to prove, for the actual regularized Burnol/Müntz residual seed b_N,

    ||Pi_blind Z_y b_N|| / ||Z_y b_N|| -> 0

or at least a uniform bound < 1.

This is a high-divisibility/Omega-tail estimate, not an AFE re-derivation.