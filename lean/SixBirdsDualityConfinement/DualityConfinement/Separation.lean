import SixBirdsDualityConfinement.DualityConfinement.Involution

/-!
Duality Confinement paper — module Separation.

Stub. Populated by codex during Phase G per the queue at
`formalization/traceability/queue_duality_confinement.csv`.
-/

namespace SixBirdsDualityConfinement.DualityConfinement.Separation

universe u v w z

/--
A separating anti-invariant readout for an involutive object ledger.

The qualitative field states separation on the visible finite support:
`psi_minus x = 0` exactly on the fixed locus of `J`.  The quantitative
fields encode the modulus form over an abstract positive scale, with
`dist_to_fix` representing `dist(x, Fix(J))` and `norm_psi_minus`
representing `||psi_minus x||`.
-/
structure SeparatingReadout
    (ledger :
      Involution.InvolutiveObjectLedger.{u, v, w}) where
  psi_minus : ledger.X → ledger.Y
  zero_Y : ledger.Y
  separates_fixed_locus_on_visible :
    ∀ x : ledger.X,
      x ∈ ledger.mu_support →
        (psi_minus x = zero_Y ↔ ledger.J x = x)
  Scale : Type z
  ScalePositive : Scale → Prop
  ScaleGE : Scale → Scale → Prop
  dist_to_fix : ledger.X → Scale
  norm_psi_minus : ledger.X → Scale
  modulus : Scale → Scale
  modulus_positive :
    ∀ ε : Scale, ScalePositive ε → ScalePositive (modulus ε)
  quantitatively_separating :
    ∀ ε : Scale,
      ScalePositive ε →
        ∀ x : ledger.X,
          ScaleGE (dist_to_fix x) ε →
            ScaleGE (norm_psi_minus x) (modulus ε)

end SixBirdsDualityConfinement.DualityConfinement.Separation
