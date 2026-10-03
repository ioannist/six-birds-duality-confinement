import SixBirdsDualityConfinement.RH.ClassicalZeroLedger
import Mathlib.Analysis.Analytic.IsolatedZeros
import Mathlib.Analysis.Complex.CauchyIntegral
import Mathlib.Topology.Compactness.Lindelof

/-!
Countability of the actual completed-zeta zero subtype in the open strip.
The proof uses an entire numerator of completed zeta, which is nonzero at
zero, and the isolated-zeros theorem. This removes the conditional
encodability premise from the existence of exhaustive finite zero windows.
-/

noncomputable section
open Set Filter
open scoped Topology

namespace SixBirdsDualityConfinement.RH.ClassicalZeroCountable

open ClassicalZeroLedger

/-- Entire numerator: away from `0` and `1`, this is
`s * (1-s) * completedRiemannZeta s`. -/
def completedNumerator (s : ℂ) : ℂ :=
  s * (1 - s) * completedRiemannZeta₀ s - 1

theorem completedNumerator_differentiable :
    Differentiable ℂ completedNumerator := by
  unfold completedNumerator
  exact ((differentiable_id.mul (differentiable_id.const_sub 1)).mul
    differentiable_completedZeta₀).sub_const 1

theorem completedNumerator_zero_set_countable :
    Set.Countable {s : ℂ | completedNumerator s = 0} := by
  have ha : AnalyticOnNhd ℂ completedNumerator Set.univ :=
    Complex.analyticOnNhd_univ_iff_differentiable.mpr
      completedNumerator_differentiable
  have hne : ¬ EqOn completedNumerator 0 Set.univ := by
    intro h
    have h0 := h (Set.mem_univ (0 : ℂ))
    norm_num [completedNumerator] at h0
  have hevent := (ha.eqOn_zero_or_eventually_ne_zero_of_preconnected
    isPreconnected_univ).resolve_left hne
  have hdisc : IsDiscrete {s : ℂ | completedNumerator s = 0} := by
    have hcod : {s : ℂ | completedNumerator s = 0}ᶜ ∈
        codiscreteWithin Set.univ := by
      simpa only [Set.compl_setOf] using hevent
    simpa using isDiscrete_of_codiscreteWithin hcod
  haveI : DiscreteTopology {s : ℂ // completedNumerator s = 0} :=
    hdisc.to_subtype
  haveI : Countable {s : ℂ // completedNumerator s = 0} :=
    countable_of_Lindelof_of_discrete
  change Countable {s : ℂ // completedNumerator s = 0}
  exact inferInstance

theorem completedNumerator_eq_mul_completed (s : ℂ)
    (hs0 : s ≠ 0) (hs1 : s ≠ 1) :
    completedNumerator s = s * (1 - s) * completedRiemannZeta s := by
  rw [completedRiemannZeta_eq]
  unfold completedNumerator
  have h1s : 1 - s ≠ 0 := by
    intro h
    exact hs1 (sub_eq_zero.mp h).symm
  field_simp [hs0, h1s]
  ring

/-- The actual subtype used by the RH positive ledger is countable. -/
theorem nontrivialZero_countable : Countable NontrivialZero := by
  have hsub :
      {s : ℂ | completedRiemannZeta s = 0 ∧ 0 < s.re ∧ s.re < 1} ⊆
        {s : ℂ | completedNumerator s = 0} := by
    intro s hs
    have hs0 : s ≠ 0 := by
      intro h
      simp [h] at hs
    have hs1 : s ≠ 1 := by
      intro h
      simp [h] at hs
    change completedRiemannZeta s = 0 ∧ 0 < s.re ∧ s.re < 1 at hs
    change completedNumerator s = 0
    rw [completedNumerator_eq_mul_completed s hs0 hs1, hs.1]
    simp
  have hcount := completedNumerator_zero_set_countable.mono hsub
  exact hcount.to_subtype

end SixBirdsDualityConfinement.RH.ClassicalZeroCountable
