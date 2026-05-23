# Step 442 Positivity-Form Choice

## Mechanism chosen

This second `G_constitutive_closure` carrier attempt chooses the de Branges Hilbert-space positivity mechanism.

Primary anchor: de Branges, *Hilbert Spaces of Entire Functions* (1968). The relevant typed structure is a Hermite-Biehler entire function `E`, its reflected function `E#(z)=overline(E(overline z))`, and the reproducing kernel

```text
K_E(w,z) = (E(z) overline(E(w)) - E#(z) overline(E#(w))) / (2 pi i (overline w - z)).
```

For a genuine de Branges space `H(E)`, kernel positivity is structural. Zero localization is then handled by positivity of the reproducing-kernel geometry rather than by predicting individual zero heights.

## Why de Branges was selected

This directly engineers against Step 441's new constraint `C_zero_height_audit_currency_smuggling`: the audit currency is not a list of zero heights. It is a positivity form.

## Known obstruction

The construction still requires deriving the relevant Hermite-Biehler / kernel-positivity conditions for the zeta-associated `E_xi`. This is the historical obstruction in de Branges-style zeta programs; Conrey-Li-type objections show that the needed positivity/growth conditions cannot simply be assumed for `xi`.

## Step 442 status

The positivity-form audit avoids explicit height smuggling but does not complete Stage I because kernel positivity for `E_xi` is not derived from the allowed primitives.
