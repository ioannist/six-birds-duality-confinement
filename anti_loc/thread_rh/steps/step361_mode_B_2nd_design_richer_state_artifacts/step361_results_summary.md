# Step 361 Results Summary

U^flat-prime was constructed with richer state space Sigma' = {a,b,c,d,e,f,g,h}.

## SAU

All six SAU gates passed at the design level.

## Stage II Preview

Fifty atom reproductions were run:

- 35 Hecke atom cells: 7 characters x k=1..5.
- 15 zeta atom cells: 3 targets x k=1..5.

All 50 reproduced with relative error 0.

## Stage III

The richer transfer family used:

- log |T(H_chi,k)| = A_chi + B_chi log |H_chi,k|;
- arg T(H_chi,k) = arg H_chi,k + C_chi + D_chi k;
- an internal operator-realization penalty of 0.25 because no external certificate is present.

Residual RMSE(lambda_total):

- rho_1 training: 0.2657549597854174
- rho_2 holdout: 1.982740773308652
- rho_3 holdout: 2.534982204826251

## Verdict

U_flat_prime_stage_III_fails_holdout;_second_Mode_B_design_retract.

The richer design escapes the exact Step 358 scalar under-fit pattern but does not solve Stage III.  It accumulates design-class evidence that H6 is not reachable by this finite state-indexed transfer family.
