# Step 358 Admissibility Formalization

The target transfer is not a primitive of `U^flat`.

For a candidate transfer rewrite sequence `tau`, admissibility is defined by
the existing `R_admit` gate:

`R_admit(a[chi,k]) ->_tau b[rho,k]`

succeeds iff all three residual components pass:

1. magnitude:
   `lambda_mag(tau(H_chi,k), Z_rho,k) < epsilon_mag`;
2. phase:
   `lambda_phase(tau(H_chi,k), Z_rho,k) < epsilon_phase`;
3. operator:
   `lambda_operator(tau) < epsilon_op`.

The tested numerical threshold is the same bridge-grade scale used in prior
steps: combined mag/phase residual below `0.05` would be a candidate before
operator audit.  No tested transfer reaches that threshold, and all tested
transfers also fail the operator gate because no kernel-preserving certificate
is supplied.

## U^flat-Internal Transfer Families

Two finite state-transition families were tested:

1. `tau_character_scalar`:
   `a[chi,k] -> b_candidate[chi,k]` with
   `T_chi(H) = C_chi H`.

2. `tau_character_affine_log`:
   `a[chi,k] -> b_candidate[chi,k]` with separate finite updates for
   log-magnitude and phase:
   `log|T_chi(H)| = alpha_chi + beta_chi log|H|`,
   `arg T_chi(H) = p_chi + q_chi arg(H)`.

Both are operational rewrites indexed by finite state labels.  Neither adds
the target transfer as an axiom.
