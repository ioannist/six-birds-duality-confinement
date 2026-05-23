# Step 442 Smuggling Check

## Constraint cited: C_zero_height_audit_currency_smuggling

Failure shape from the ledger:

> G_constitutive_closure can build formal Loewner-Schur membrane data, but the audit currency A cannot predict the first nontrivial zeta-zero heights from functional-equation/gamma/operator primitives alone; inserting the 10 heights imports zeta-side spectral data.

Formal prohibition:

> audit_currency_for_zero_locations_must_derive_numerical_zero_heights_from_declared_operator_theoretic_primitives_without_direct_zeta_evaluation_zero_tables_or_equivalent_spectral_input

## Constraint cited: C_native_membrane_no_L_side_smuggling

Failure shape from the ledger:

> Designs may smuggle L-function side data (zeta-values special values Dirichlet L data prime counting modular forms) into the predictive native membrane Khat_j or into the audit currency a^sharp.

Formal prohibition:

> predictive_native_membrane_M_and_audit_currency_A_must_be_constructed_from_operator_theoretic_functional_analytic_or_native_probe_primitives_ONLY_no_explicit_zeta_values_or_L_function_side_data_may_appear_in_the_definition_or_construction_of_M_or_A

## Primitive-by-primitive declaration

| primitive | status |
|---|---|
| Loewner cone / Schur identity / pseudoinverse | operator-theoretic, allowed |
| gamma factor metadata | allowed in declared native zeta scope |
| functional-equation involution | allowed in declared native zeta scope |
| formal de Branges `E -> E#`, kernel `K_E` | operator-theoretic, allowed |
| zero heights | not used; passes `C_zero_height_audit_currency_smuggling` |
| `E_xi` as concrete analytic function | target-function data unless derived; fails native no-smuggling if used as oracle |
| kernel positivity of `E_xi` | RH-adjacent predicate; must be derived, cannot be stipulated |

## Verdict

`A_pos` passes the specific zero-height-smuggling constraint but fails Stage I because positivity for `E_xi` is not derived from allowed primitives. New constraint added: `C_positivity_audit_kernel_positivity_must_derive`.
