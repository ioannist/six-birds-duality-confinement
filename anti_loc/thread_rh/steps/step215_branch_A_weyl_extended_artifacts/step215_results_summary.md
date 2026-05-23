# Step 215 Results Summary

## Target

Extend the Step 214 Branch A Weyl-sequence diagnostic to the first 20 zeta zeros, test the alternative CAND2 zeta-form model for `kappa`, and address the weak-null and lim-inf caveats.

## Numerical Setup

- `u_n = kappa_{rho_n,0}^{1/2} / ||kappa_{rho_n,0}^{1/2}||`.
- CAND1: Burnol-boundary kernel model `K_{1/2}^Gamma(1/2+i tau, rho_n)`.
- CAND2: zeta-form single-term comparison model from Step 207.
- Operator: `C_l = (I - P_infty) M_{m_l} P_infty`, with `l = log 2`.
- Grid: Gauss-Legendre on `[-100,100]`, 140 nodes.
- Precision: mpmath 70 dps for zero/E-function components; PSWF finite model with 24 retained terms.
- Error budget: conservative displayed norm uncertainty `5e-2`.

## Findings

CAND1 remains bounded away from zero for all `n=1..20`.

- Minimum over `n=1..20`: `0.7937590184564269`.
- Conservative lower after error: `0.7437590184564269`.
- Tail minimum over `n=11..20`: `1.4403036850155422`.
- Tail lower after error: `1.3903036850155421`.

CAND2 also stays nonzero on `n=1..10`, but with a weaker lower bound.

- Minimum over `n=1..10`: `0.2388748880100559`.
- Conservative lower after error: `0.1888748880100559`.

The weak-null check did **not** pass on the finite sampled span.

- Max pairwise normalized inner product over all pairs: `0.9999887398876486`.
- Max pairwise normalized inner product over the tail `n=11..20`: `0.9999845657507579`.
- This prevents theorem-grade Weyl-sequence certification.

## Verdict

`V_weyl_extended_obstruction_diagnostic`.

The Step 214 lower-bound pattern is strengthened: the CAND1 tail does not decay, and CAND2 gives a positive comparison lower bound. However, the weak-null caveat is not closed, so this remains a strong finite-grid diagnostic, not a proof that `q_eta(C_l P_eta) != 0`.
