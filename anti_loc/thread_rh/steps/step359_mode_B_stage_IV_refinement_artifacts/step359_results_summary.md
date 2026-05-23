# Step 359 Results Summary

Mode B Stage IV refined the Stage III under-fit failure.

## Converse Probe

Adding a seventh transfer-witness state `f` does not achieve admissibility
unless `f` is allowed to store target values directly.  That lookup variant
would make training residual zero but fails primitive exclusion and negative
controls, so it is rejected as smuggling.

## Failure Decomposition

For `tau_character_scalar` on `rho_1` training:

- cells: `70`
- mean `lambda_mag`: `0.8558`
- mean `lambda_phase`: `0.4166`
- dominant with operator marker included: operator `46`, magnitude `22`, phase `2`
- considering only mag/phase: magnitude dominates `59/70`

Thus the concrete numeric failure is mostly magnitude under-fit, while the
operator certificate remains a separate hard gate.

## Earning At Scale

Mode B contributes a useful state-structured diagnostic:

`H6 obstruction = numeric under-fit at R_compare + missing certificate at R_operator_audit`.

## Equivalence Audit

Mode B and Mode C failures are structurally distinct:

- Mode C: overfit in training, then hold-out failure.
- Mode B: under-fit already at training, plus explicit operator-gate failure.

## Verdict

`V_mode_B_stage_IV_passes_sharper_underfit_operator_diagnostic`.

Mode B Stage IV passes as refinement, despite the Stage III transfer failure.
