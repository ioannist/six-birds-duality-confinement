# U^flat-double-prime: Four-State Rich-Rewrite Mode B Design

## State Space

Sigma'' = {alpha, beta, gamma, delta}.

- alpha: composite Hecke-zeta atom. It carries the pair (H_{chi,k}, Z_{rho,k}) in one finite state.
- beta: residual-decomposition atom. It stores (lambda_mag, lambda_phase, lambda_operator).
- gamma: transfer-conditioning atom. It stores admissibility constraints and rich rewrite parameters.
- delta: defect witness.

This differs from U^flat and U^flat-prime by using fewer states but more expressive rewrites on each state.

## Rewrite Rules

- R_load_both: (chi,rho,k) -> alpha[H_{chi,k}, Z_{rho,k}].
- R_decompose: alpha -> beta(lambda_mag, lambda_phase, lambda_operator).
- R_constrain: beta -> gamma after applying polynomial magnitude/phase constraints.
- R_compose_transfer: gamma-family -> transfer candidate tau''.
- R_block: gamma -> delta when any admissibility threshold fails.
- R_admit: gamma -> descended value only when no defect is present.

## Stage III Transfer Family

The rich rewrite R_constrain permits per-character polynomial constraints:

- magnitude: log |T(H_{chi,k})| = A_chi + B_chi x + C_chi x^2, where x = log |H_{chi,k}|;
- phase: arg T(H_{chi,k}) = arg H_{chi,k} + D_chi + E_chi k + F_chi k^2.

The target transfer tau is not a primitive of the carrier; it is the output of R_compose_transfer after R_decompose and R_constrain.
