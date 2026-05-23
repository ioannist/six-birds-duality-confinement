# Step 444 Three-Attempt Cross-Step Evidence

| step | audit-currency mechanism | concrete-branch failure | formal-branch failure | constraint |
|---:|---|---|---|---|
| 441 | height-predictor | needs zeta evaluation / zero tables | insufficient: no heights at all | `C_zero_height_audit_currency_smuggling` |
| 442 | de Branges kernel positivity | concrete `E_xi` imports xi / target positivity | abstract `E` does not yield kernel positivity | `C_positivity_audit_kernel_positivity_must_derive` |
| 443 | Weil explicit-formula positivity | concrete `W` needs zeros or primes | formal `W` has no numeric adequacy content | `C_weil_positivity_explicit_formula_smuggling` |

## Verbatim result-summary citations

Step 441:

> Stage I retracts. The package verifies the formal Loewner/Schur machinery but cannot construct the audit currency for the first 10 nontrivial zero heights from operator-theoretic primitives alone. New constraint added to the ledger: `C_zero_height_audit_currency_smuggling`.

Step 442:

> Stage I retracts. The second carrier attempt fixes the height-smuggling failure but exposes a positivity-specific failure: kernel positivity for `E_xi` must be derived, not stipulated or imported.

Step 443:

> Stage I retracts. Weil positivity confirms the audit-currency derivability tension across three structurally distinct attempts. This is a saturation observation only; `G_constitutive_closure` is not globally exhausted here.

## Consolidated pattern

For all three tested mechanisms:

```text
concrete + RH-distinguishing => arithmetic smuggling
formal + non-smuggling => insufficient for adequacy closure
```
