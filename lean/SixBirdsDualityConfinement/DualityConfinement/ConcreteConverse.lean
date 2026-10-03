import SixBirdsDualityConfinement.DualityConfinement.ConcreteFinite
import SixBirdsDualityConfinement.DualityConfinement.ConcreteMeasured

/-! Converse confinement: vanishing readouts produce zero ledgers and a genuine
constant zero domination sequence. Fixedness implies readout vanishing by
anti-invariance alone; separation is not needed in this direction. -/
namespace SixBirdsDualityConfinement.DualityConfinement.ConcreteConverse
open Filter InnerProductSpace MeasureTheory
open SixBirdsDualityConfinement.DualityConfinement.ConcreteCore
open SixBirdsDualityConfinement.DualityConfinement.ConcreteFinite
open SixBirdsDualityConfinement.DualityConfinement.ConcreteMeasured
open scoped Topology
variable {X Y : Type*} [NormedAddCommGroup Y] [InnerProductSpace ℝ Y]

/-- With nonnegative weights, vanishing on visible points kills the weighted ledger. -/
theorem finiteLedger_zero_of_visible_zero [Fintype X] (mu : X → ℝ) (hmu : ∀ x, 0 ≤ mu x)
    (r : X → Y) (hr : ∀ x, 0 < mu x → r x = 0) : finiteLedger mu r = 0 := by
  unfold finiteLedger
  apply Finset.sum_eq_zero
  intro x _
  by_cases hx : 0 < mu x
  · have hz : rankOne ℝ (r x) (r x) = 0 := rankOne_eq_zero.mpr (Or.inl (hr x hx))
    rw [hz, smul_zero]
  · have hmuz : mu x = 0 := le_antisymm (le_of_not_gt hx) (hmu x)
    simp [hmuz]

/-- The converse provides an actual vanishing-trace domination sequence. -/
theorem finite_converse [Fintype X] [FiniteDimensional ℝ Y]
    (mu : X → ℝ) (hmu : ∀ x, 0 ≤ mu x) (r : X → Y)
    (hr : ∀ x, 0 < mu x → r x = 0) :
    finiteLedger mu r = 0 ∧
      (∀ _ : ℕ, ((0 : Y →L[ℝ] Y) - finiteLedger mu r).IsPositive) ∧
      Tendsto (fun _ : ℕ => opTrace (0 : Y →L[ℝ] Y)) atTop (𝓝 0) := by
  have hz := finiteLedger_zero_of_visible_zero mu hmu r hr
  refine ⟨hz, ?_, ?_⟩
  · intro _
    simp [hz]
  · simpa only [map_zero] using (tendsto_const_nhds (x := (0 : ℝ)))

/-- Equivariant anti-invariant readouts vanish at visible fixed points. -/
theorem psiMinus_visible_zero_of_fixed (mu : X → ℝ) (J : X → X)
    (S : Y ≃ₗᵢ[ℝ] Y) (hS : Function.Involutive S) (psi : X → Y)
    (heq : ∀ x, psi (J x) = S (psi x)) (hfixed : ∀ x, 0 < mu x → J x = x) :
    ∀ x, 0 < mu x → psiMinus S psi x = 0 := by
  intro x hx
  exact psiMinus_fixed J S hS psi heq (hfixed x hx)

theorem finiteLedger_zero_of_visible_fixed [Fintype X] (mu : X → ℝ) (hmu : ∀ x, 0 ≤ mu x)
    (J : X → X) (S : Y ≃ₗᵢ[ℝ] Y) (hS : Function.Involutive S) (psi : X → Y)
    (heq : ∀ x, psi (J x) = S (psi x)) (hfixed : ∀ x, 0 < mu x → J x = x) :
    finiteLedger mu (psiMinus S psi) = 0 :=
  finiteLedger_zero_of_visible_zero mu hmu _
    (psiMinus_visible_zero_of_fixed mu J S hS psi heq hfixed)

/-- AE vanishing makes the Bochner ledger zero without extra integrability or
measurability assumptions: its integrand is AE equal to the zero function. -/
theorem measuredLedger_zero_of_ae_zero [MeasurableSpace X] (mu : Measure X) (r : X → Y)
    (hr : ∀ᵐ x ∂mu, r x = 0) : measuredLedger mu r = 0 := by
  unfold measuredLedger
  calc
    (∫ x, rankOne ℝ (r x) (r x) ∂mu) = ∫ _ : X, (0 : Y →L[ℝ] Y) ∂mu := by
      apply integral_congr_ae
      filter_upwards [hr] with x hx
      exact rankOne_eq_zero.mpr (Or.inl hx)
    _ = 0 := integral_zero _ _

theorem measured_converse [MeasurableSpace X] [FiniteDimensional ℝ Y] (mu : Measure X) (r : X → Y)
    (hr : ∀ᵐ x ∂mu, r x = 0) :
    measuredLedger mu r = 0 ∧
      (∀ _ : ℕ, ((0 : Y →L[ℝ] Y) - measuredLedger mu r).IsPositive) ∧
      Tendsto (fun _ : ℕ => opTrace (0 : Y →L[ℝ] Y)) atTop (𝓝 0) := by
  have hz := measuredLedger_zero_of_ae_zero mu r hr
  refine ⟨hz, ?_, ?_⟩
  · intro _
    simp [hz]
  · simpa only [map_zero] using (tendsto_const_nhds (x := (0 : ℝ)))

/-- Fixedness implies vanishing without separation or measurability of J. -/
theorem psiMinus_ae_zero_of_fixed [MeasurableSpace X] (mu : Measure X) (J : X → X)
    (S : Y ≃ₗᵢ[ℝ] Y) (hS : Function.Involutive S) (psi : X → Y)
    (heq : ∀ x, psi (J x) = S (psi x)) (hfixed : ∀ᵐ x ∂mu, J x = x) :
    ∀ᵐ x ∂mu, psiMinus S psi x = 0 := by
  filter_upwards [hfixed] with x hx
  exact psiMinus_fixed J S hS psi heq hx

theorem measuredLedger_zero_of_ae_fixed [MeasurableSpace X] (mu : Measure X) (J : X → X)
    (S : Y ≃ₗᵢ[ℝ] Y) (hS : Function.Involutive S) (psi : X → Y)
    (heq : ∀ x, psi (J x) = S (psi x)) (hfixed : ∀ᵐ x ∂mu, J x = x) :
    measuredLedger mu (psiMinus S psi) = 0 :=
  measuredLedger_zero_of_ae_zero mu _ (psiMinus_ae_zero_of_fixed mu J S hS psi heq hfixed)
end SixBirdsDualityConfinement.DualityConfinement.ConcreteConverse
