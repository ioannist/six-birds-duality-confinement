import SixBirdsDualityConfinement.DualityConfinement.Involution

/-!
# Duality Confinement paper -- `AntiInvariantLedger`

Typed anti-invariant ledger `A_X` over a typed positive cone, with the
trace identity built into the constructor.
-/

namespace SixBirdsDualityConfinement.DualityConfinement.AntiInvariantLedger

universe u v w z q

/--
The anti-invariant object ledger `A_X` attached to an involutive object
ledger and an anti-invariant readout.

The operator integral is represented by the typed positive-cone element
`A_X`.  The trace-class regime is encoded by the fields `tr`,
`integral_sq_norm`, and `trace_identity`, while `zero_iff_ae_zero`
records the positivity consequence that the zero cone element is
equivalent to vanishing of `psi_minus` almost everywhere.
-/
structure AntiInvariantLedger
    (ledger :
      Involution.InvolutiveObjectLedger.{u, v, w}) where
  psi_minus : ledger.X → ledger.Y
  Cone : Type z
  TraceValue : Type q
  zero : Cone
  A_X : Cone
  Positive : Cone → Prop
  positive_A_X : Positive A_X
  preceq : Cone → Cone → Prop
  tr : Cone → TraceValue
  TraceLE : TraceValue → TraceValue → Prop
  trace_mono :
    ∀ A B : Cone, preceq A B → TraceLE (tr A) (tr B)
  integral_sq_norm : TraceValue
  trace_identity : tr A_X = integral_sq_norm
  psi_minus_ae_zero : Prop
  zero_iff_ae_zero : A_X = zero ↔ psi_minus_ae_zero

/--
Trace identity for the typed anti-invariant ledger.

Because the constructor records `A_X` in the trace-class regime, the
trace identity is projection from the ledger data.  The accompanying
equivalence is the encoded positivity consequence for a positive
trace-class element with zero trace.
-/
theorem traceIdentity
    {ledger :
      Involution.InvolutiveObjectLedger.{u, v, w}}
    (A : AntiInvariantLedger.{u, v, w, z, q} ledger) :
    A.tr A.A_X = A.integral_sq_norm ∧
      (A.A_X = A.zero ↔ A.psi_minus_ae_zero) :=
  And.intro A.trace_identity A.zero_iff_ae_zero

end SixBirdsDualityConfinement.DualityConfinement.AntiInvariantLedger
