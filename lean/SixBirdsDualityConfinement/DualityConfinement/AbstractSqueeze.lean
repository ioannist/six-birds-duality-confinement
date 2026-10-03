import Mathlib.Topology.Instances.Real.Lemmas
import Mathlib.Topology.Order.OrderClosed

/-! Abstract positive real-trace squeeze. No algebra or order laws on the carrier
are needed. Trace faithfulness is required only at the chosen element. -/
namespace SixBirdsDualityConfinement.DualityConfinement.AbstractSqueeze
open Filter
open scoped Topology

/-- Vanishing upper trace budgets force a positive element to vanish.
The hypothesis `tau 0 = 0` is unnecessary. -/
theorem abstract_trace_squeeze {C : Type*} [Zero C]
    (le : C → C → Prop) (Positive : C → Prop) (tau : C → ℝ)
    (hnonneg : ∀ c, Positive c → 0 ≤ tau c)
    (hmono : ∀ a b, le a b → tau a ≤ tau b)
    (a : C) (ha : Positive a) (hfaithful : tau a = 0 → a = 0)
    (b : ℕ → C) (hdom : ∀ n, le a (b n))
    (hlim : Tendsto (tau ∘ b) atTop (𝓝 0)) : a = 0 := by
  apply hfaithful
  exact le_antisymm
    (le_of_tendsto_of_tendsto tendsto_const_nhds hlim
      (Eventually.of_forall fun n => hmono a (b n) (hdom n)))
    (hnonneg a ha)

end SixBirdsDualityConfinement.DualityConfinement.AbstractSqueeze
