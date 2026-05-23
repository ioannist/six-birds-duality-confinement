# Step 442 Results Summary

## Choice

Chosen positivity-form mechanism: de Branges Hilbert-space reproducing-kernel positivity, anchored in de Branges 1968.

## A_pos

`A_pos` is the typed finite predicate that a de Branges kernel Gram matrix for a candidate `E_xi` is positive semidefinite on a finite test-node set, with Hermite-Biehler positivity as the intended structural condition.

## Smuggling check

`A_pos` passes `C_zero_height_audit_currency_smuggling`: it uses no nontrivial zero heights. It fails the stronger derivability requirement because concrete `E_xi` imports the target zeta function unless independently derived, and formal `E_xi` does not prove kernel positivity.

## Numerics

A1-A4 pass for the rebuilt finite Schur package. Schur identity error: `1.48249658577e-82`. Residual eigenvalues: `['0.0009', '0.0016', '0.0049']`. Adequacy budget: `Xi_Z=0.0049 I`.

## Gates

6 gates: 2 pass, 1 partial, 3 fail. Grammar-local checks: 1 pass, 1 fail. `C_zero_height_audit_currency_smuggling`: pass. New constraint: fail/add `C_positivity_audit_kernel_positivity_must_derive`.

## Verdict

Stage I retracts. The second carrier attempt fixes the height-smuggling failure but exposes a positivity-specific failure: kernel positivity for `E_xi` must be derived, not stipulated or imported.
