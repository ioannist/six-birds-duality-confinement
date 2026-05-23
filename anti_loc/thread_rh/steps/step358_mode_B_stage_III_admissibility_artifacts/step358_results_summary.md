# Step 358 Results Summary

Formalized H6 as the `R_admit` admissibility gate on `U^flat`:

`Admit(tau)` requires small magnitude residual, small phase residual, and a
certified operator-compatible transfer.

Two finite U-internal transfer families were tested on `rho_1` training and
`rho_2/rho_3` hold-out:

## tau_character_scalar

`T_chi(H) = C_chi H`.

- training `rho_1` RMSE: `1.2174`
- hold-out `rho_2` RMSE: `1.6258`
- hold-out `rho_3` RMSE: `2.5367`
- operator status: missing certificate

## tau_character_affine_log

Finite log-magnitude and phase rewrite by character.

- training `rho_1` RMSE: `1.3486`
- hold-out `rho_2` RMSE: `1.2269`
- hold-out `rho_3` RMSE: `3.0039`
- operator status: missing certificate

## Comparison To Mode C

Mode C's weighted geometric family overfit: training residual near `4e-5`
but target hold-out failed.  Mode B's finite U-internal operations do not
overfit; they fail already at training.

## Verdict

`V_mode_B_stage_III_fails_training_transfer_not_found`.

No admissible transfer candidate was found.  Under the Stage III criterion,
this counts as one Mode B retract.
