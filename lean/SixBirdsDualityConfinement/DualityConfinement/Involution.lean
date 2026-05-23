import SixBirdsDualityConfinement.Terminology

/-!
Duality Confinement paper — module Involution.

Stub. Populated by codex during Phase G per the queue at
`formalization/traceability/queue_duality_confinement.csv`.
-/

namespace SixBirdsDualityConfinement.DualityConfinement.Involution

universe u v w

/--
An involutive object ledger `X_hat = (X, J, mu, psi, Y, J_iso)`.

The carrier `X` is enumerated by `mu_support`, giving the finite
object-ledger regime.  The response space `Y` is kept as an abstract
typed real-Hilbert carrier: only the operations needed to state that
`J_iso` is linear and isometric are recorded here.  The anti-invariant
projector and trace ledger are introduced in the later ledger modules.
-/
structure InvolutiveObjectLedger where
  X : Type u
  J : X → X
  J_involutive : ∀ x : X, J (J x) = x
  Weight : Type v
  WeightPositive : Weight → Prop
  mu : X → Weight
  mu_positive : ∀ x : X, WeightPositive (mu x)
  mu_support : List X
  mu_support_complete : ∀ x : X, x ∈ mu_support
  Y : Type u
  Scalar : Type w
  add : Y → Y → Y
  smul : Scalar → Y → Y
  inner : Y → Y → Scalar
  norm : Y → Scalar
  J_iso : Y → Y
  J_iso_involutive : ∀ y : Y, J_iso (J_iso y) = y
  J_iso_linear :
    ∀ (a : Scalar) (y z : Y),
      J_iso (add (smul a y) z) = add (smul a (J_iso y)) (J_iso z)
  J_iso_isometry : ∀ y : Y, norm (J_iso y) = norm y
  psi : X → Y
  psi_equivariant : ∀ x : X, psi (J x) = J_iso (psi x)

end SixBirdsDualityConfinement.DualityConfinement.Involution
