import SixBirdsDualityConfinement.DualityConfinement.ConcreteCore
import SixBirdsDualityConfinement.DualityConfinement.ConcreteBudget
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap
import Mathlib.MeasureTheory.Integral.Bochner.Set

/-! Bochner squared ledgers with arbitrary measures and finite-dimensional responses.
No preservation of the measure by the involution is required. -/
namespace SixBirdsDualityConfinement.DualityConfinement.ConcreteMeasured
open Filter InnerProductSpace MeasureTheory
open SixBirdsDualityConfinement.DualityConfinement.ConcreteCore
open SixBirdsDualityConfinement.DualityConfinement.ConcreteBudget
open scoped Topology
variable {X Y : Type*} [MeasurableSpace X] [NormedAddCommGroup Y]
  [InnerProductSpace ℝ Y] [FiniteDimensional ℝ Y]

/-- The Bochner integral of actual positive rank-one operators. -/
noncomputable def measuredLedger (mu : Measure X) (r : X → Y) : Y →L[ℝ] Y :=
  ∫ x, rankOne ℝ (r x) (r x) ∂mu

omit [FiniteDimensional ℝ Y] in
theorem psiMinus_stronglyMeasurable (S : Y ≃ₗᵢ[ℝ] Y) (psi : X → Y)
    (hpsi : StronglyMeasurable psi) : StronglyMeasurable (psiMinus S psi) :=
  (pminus S).continuous.comp_stronglyMeasurable hpsi

omit [FiniteDimensional ℝ Y] in
theorem rankOne_integrable (mu : Measure X) (r : X → Y)
    (hr : AEStronglyMeasurable r mu) (hi : Integrable (fun x => ‖r x‖ ^ 2) mu) :
    Integrable (fun x => rankOne ℝ (r x) (r x)) mu := by
  have hc : Continuous (fun v : Y => rankOne ℝ v v) :=
    (rankOne ℝ).continuous.clm_apply continuous_id
  apply hi.mono' (hc.comp_aestronglyMeasurable hr)
  exact Eventually.of_forall fun x => by simp [pow_two]

/-- Bochner integration preserves the real positive cone. -/
theorem integral_positive (mu : Measure X) (F : X → Y →L[ℝ] Y)
    (hi : Integrable F mu) (hp : ∀ᵐ x ∂mu, (F x).IsPositive) :
    (∫ x, F x ∂mu).IsPositive := by
  let L (u v : Y) : (Y →L[ℝ] Y) →L[ℝ] ℝ :=
    (innerSL ℝ v).comp (ContinuousLinearMap.apply ℝ Y u)
  have hcomm (u v : Y) : inner ℝ v ((∫ x, F x ∂mu) u) =
      ∫ x, inner ℝ v (F x u) ∂mu := (L u v).integral_comp_comm hi |>.symm
  apply (ContinuousLinearMap.isPositive_iff _).mpr
  constructor
  · intro u v
    change inner ℝ ((∫ x, F x ∂mu) u) v = inner ℝ u ((∫ x, F x ∂mu) v)
    rw [real_inner_comm, hcomm, hcomm]
    apply integral_congr_ae
    filter_upwards [hp] with x hx
    simpa only [real_inner_comm] using hx.inner_left_eq_inner_right u v
  · intro v
    rw [real_inner_comm, hcomm]
    apply integral_nonneg_of_ae
    filter_upwards [hp] with x hx
    exact hx.inner_nonneg_right v

theorem measuredLedger_positive (mu : Measure X) (r : X → Y)
    (hr : AEStronglyMeasurable r mu) (hi : Integrable (fun x => ‖r x‖ ^ 2) mu) :
    (measuredLedger mu r).IsPositive :=
  integral_positive mu _ (rankOne_integrable mu r hr hi)
    (Eventually.of_forall fun x => isPositive_rankOne_self (r x))

theorem measuredLedger_trace (mu : Measure X) (r : X → Y)
    (hr : AEStronglyMeasurable r mu) (hi : Integrable (fun x => ‖r x‖ ^ 2) mu) :
    opTrace (measuredLedger mu r) = ∫ x, ‖r x‖ ^ 2 ∂mu := by
  have hh := (opTrace (Y := Y)).toContinuousLinearMap.integral_comp_comm
    (rankOne_integrable mu r hr hi)
  change (∫ x, opTrace (rankOne ℝ (r x) (r x)) ∂mu) =
    opTrace (measuredLedger mu r) at hh
  simpa only [opTrace_rankOne] using hh.symm

/-- Every matrix coefficient of the measured ledger is its integrated Gram coefficient. -/
theorem measuredLedger_coefficient (mu : Measure X) (r : X → Y)
    (hr : AEStronglyMeasurable r mu) (hi : Integrable (fun x => ‖r x‖ ^ 2) mu)
    (h k : Y) : inner ℝ (measuredLedger mu r h) k =
      ∫ x, inner ℝ (r x) h * inner ℝ (r x) k ∂mu := by
  let L : (Y →L[ℝ] Y) →L[ℝ] ℝ :=
    (innerSL ℝ k).comp (ContinuousLinearMap.apply ℝ Y h)
  have hc := L.integral_comp_comm (rankOne_integrable mu r hr hi)
  change (∫ x, inner ℝ k (rankOne ℝ (r x) (r x) h) ∂mu) =
    inner ℝ k (measuredLedger mu r h) at hc
  rw [real_inner_comm, ← hc]
  apply integral_congr_ae
  exact Eventually.of_forall fun x => by
    simp [rankOne_apply, real_inner_smul_right, real_inner_comm]

/-- Zero squared mass gives almost-everywhere vanishing, including for infinite measures. -/
theorem measuredLedger_ae_zero (mu : Measure X) (r : X → Y)
    (hr : AEStronglyMeasurable r mu) (hi : Integrable (fun x => ‖r x‖ ^ 2) mu)
    (hz : measuredLedger mu r = 0) : ∀ᵐ x ∂mu, r x = 0 := by
  have hs : ∫ x, ‖r x‖ ^ 2 ∂mu = 0 := by
    rw [← measuredLedger_trace mu r hr hi, hz, map_zero]
  have hh := (integral_eq_zero_iff_of_nonneg (fun x => sq_nonneg ‖r x‖) hi).mp hs
  filter_upwards [hh] with x hx
  exact norm_eq_zero.mp (sq_eq_zero_iff.mp hx)

theorem measured_master (mu : Measure X) (r : X → Y)
    (hr : AEStronglyMeasurable r mu) (hi : Integrable (fun x => ‖r x‖ ^ 2) mu)
    (B : ℕ → Y →L[ℝ] Y)
    (hdom : ∀ n, (B n - measuredLedger mu r).IsPositive)
    (hlim : Tendsto (fun n => opTrace (B n)) atTop (𝓝 0)) :
    measuredLedger mu r = 0 ∧ ∀ᵐ x ∂mu, r x = 0 := by
  have hz := cone_squeeze (measuredLedger_positive mu r hr hi) B hdom hlim
  exact ⟨hz, measuredLedger_ae_zero mu r hr hi hz⟩

/-- Neither a measurable fixed set nor a measurable involution is needed for
this outer-measure null-set consequence of almost-everywhere separation. -/
theorem measured_fixed_of_zero (mu : Measure X) (r : X → Y)
    (hr : AEStronglyMeasurable r mu) (hi : Integrable (fun x => ‖r x‖ ^ 2) mu)
    (J : X → X) (hsep : ∀ᵐ x ∂mu, r x = 0 ↔ J x = x)
    (hz : measuredLedger mu r = 0) : mu {x | J x ≠ x} = 0 := by
  apply ae_iff.mp
  filter_upwards [measuredLedger_ae_zero mu r hr hi hz, hsep] with x hx hsep
  exact hsep.mp hx

theorem measured_master_fixed (mu : Measure X) (r : X → Y)
    (hr : AEStronglyMeasurable r mu) (hi : Integrable (fun x => ‖r x‖ ^ 2) mu)
    (J : X → X) (hsep : ∀ᵐ x ∂mu, r x = 0 ↔ J x = x)
    (B : ℕ → Y →L[ℝ] Y)
    (hdom : ∀ n, (B n - measuredLedger mu r).IsPositive)
    (hlim : Tendsto (fun n => opTrace (B n)) atTop (𝓝 0)) :
    measuredLedger mu r = 0 ∧ (∀ᵐ x ∂mu, r x = 0) ∧ mu {x | J x ≠ x} = 0 := by
  obtain ⟨hz, ha⟩ := measured_master mu r hr hi B hdom hlim
  exact ⟨hz, ha, measured_fixed_of_zero mu r hr hi J hsep hz⟩

/-- Markov estimate on any subset. Even measurability of the subset is unnecessary. -/
theorem measured_quantitative (mu : Measure X) (r : X → Y)
    (hr : AEStronglyMeasurable r mu) (hi : Integrable (fun x => ‖r x‖ ^ 2) mu)
    (s : Set X) {m : ℝ} (hm : 0 < m) (hlower : ∀ x ∈ s, m ≤ ‖r x‖) :
    mu s ≤ ENNReal.ofReal (opTrace (measuredLedger mu r) / m ^ 2) := by
  have hscaled : Integrable (fun x => ‖r x‖ ^ 2 / m ^ 2) mu := hi.div_const _
  have hb := hscaled.measure_le_integral
    (Eventually.of_forall fun x => div_nonneg (sq_nonneg _) (sq_nonneg _))
    (s := s) (fun x hx => (le_div_iff₀ (sq_pos_of_pos hm)).mpr (by
      simpa only [one_mul] using
        (sq_le_sq₀ hm.le (norm_nonneg _)).mpr (hlower x hx)))
  simpa only [integral_div, measuredLedger_trace mu r hr hi] using hb

theorem measured_quantitative_threshold (mu : Measure X) (r : X → Y)
    (hr : AEStronglyMeasurable r mu) (hi : Integrable (fun x => ‖r x‖ ^ 2) mu)
    (d : X → ℝ) (eps : ℝ) {m : ℝ} (hm : 0 < m)
    (hlower : ∀ x, eps ≤ d x → m ≤ ‖r x‖) :
    mu {x | eps ≤ d x} ≤ ENNReal.ofReal (opTrace (measuredLedger mu r) / m ^ 2) :=
  measured_quantitative mu r hr hi _ hm hlower

/-- Exhaustive squeeze with the measured ledger and its fixed-locus return. -/
theorem measured_exhaustive_fixed (mu : Measure X) (r : X → Y)
    (hr : AEStronglyMeasurable r mu) (hi : Integrable (fun x => ‖r x‖ ^ 2) mu)
    (J : X → X) (hsep : ∀ᵐ x ∂mu, r x = 0 ↔ J x = x)
    {Z : ℕ → Type*} [∀ n, NormedAddCommGroup (Z n)]
    [∀ n, InnerProductSpace ℝ (Z n)] [∀ n, FiniteDimensional ℝ (Z n)]
    (iota : ∀ n, Z n →L[ℝ] Y) (A B : ∀ n, Z n →L[ℝ] Z n) (T : ℕ → Y →L[ℝ] Y)
    (hdom : ∀ n, (B n - A n).IsPositive)
    (hex : ∀ n, ((iota n).comp ((A n).comp (iota n).adjoint) + T n - measuredLedger mu r).IsPositive)
    (hlim : Tendsto (fun n => opTrace ((iota n).comp ((B n).comp (iota n).adjoint)) +
      opTrace (T n)) atTop (𝓝 0)) :
    measuredLedger mu r = 0 ∧ (∀ᵐ x ∂mu, r x = 0) ∧ mu {x | J x ≠ x} = 0 := by
  have hz := exhaustive_squeeze (measuredLedger_positive mu r hr hi) iota A B T hdom hex hlim
  exact ⟨hz, measuredLedger_ae_zero mu r hr hi hz,
    measured_fixed_of_zero mu r hr hi J hsep hz⟩

/-- Vanishing optimized budgets confine a measured ledger and its readout. -/
theorem measured_budget_sequence (mu : Measure X) (r : X → Y)
    (hr : AEStronglyMeasurable r mu) (hi : Integrable (fun x => ‖r x‖ ^ 2) mu)
    (K E : ℕ → Y →L[ℝ] Y)
    (hK : ∀ n, (K n).IsPositive) (hE : ∀ n, (E n).IsPositive)
    (hdom : ∀ n (t : ℝ), 0 < t →
      ((1 + t) • K n + (1 + t⁻¹) • E n - measuredLedger mu r).IsPositive)
    (hKlim : Tendsto (fun n => opTrace (K n)) atTop (𝓝 0))
    (hElim : Tendsto (fun n => opTrace (E n)) atTop (𝓝 0)) :
    measuredLedger mu r = 0 ∧ ∀ᵐ x ∂mu, r x = 0 := by
  have hz := budget_sequence_zero (measuredLedger mu r)
    (measuredLedger_positive mu r hr hi) K E hK hE hdom hKlim hElim
  exact ⟨hz, measuredLedger_ae_zero mu r hr hi hz⟩

/-- With almost-everywhere separation, vanishing budgets leave only the fixed locus. -/
theorem measured_budget_sequence_fixed (mu : Measure X) (r : X → Y)
    (hr : AEStronglyMeasurable r mu) (hi : Integrable (fun x => ‖r x‖ ^ 2) mu)
    (J : X → X) (hsep : ∀ᵐ x ∂mu, r x = 0 ↔ J x = x)
    (K E : ℕ → Y →L[ℝ] Y)
    (hK : ∀ n, (K n).IsPositive) (hE : ∀ n, (E n).IsPositive)
    (hdom : ∀ n (t : ℝ), 0 < t →
      ((1 + t) • K n + (1 + t⁻¹) • E n - measuredLedger mu r).IsPositive)
    (hKlim : Tendsto (fun n => opTrace (K n)) atTop (𝓝 0))
    (hElim : Tendsto (fun n => opTrace (E n)) atTop (𝓝 0)) :
    measuredLedger mu r = 0 ∧ (∀ᵐ x ∂mu, r x = 0) ∧ mu {x | J x ≠ x} = 0 := by
  obtain ⟨hz, ha⟩ := measured_budget_sequence mu r hr hi K E hK hE hdom hKlim hElim
  exact ⟨hz, ha, measured_fixed_of_zero mu r hr hi J hsep hz⟩

end SixBirdsDualityConfinement.DualityConfinement.ConcreteMeasured
