import Mathlib.NumberTheory.LSeries.RiemannZeta
import Mathlib.MeasureTheory.Measure.MeasureSpace
import Mathlib.Tactic

/-!
The global zero ledger used by the classical RH statement. Unlike a finite
list of selected zeros, this subtype contains every zero of mathlib's
completed Riemann zeta function in the open critical strip. The extended
nonnegative sum is defined even if it is infinite.
-/

noncomputable section
open scoped ENNReal

namespace SixBirdsDualityConfinement.RH.ClassicalZeroLedger

def NontrivialZero :=
  {s : ℂ // completedRiemannZeta s = 0 ∧ 0 < s.re ∧ s.re < 1}

def weightedTerm (m : NontrivialZero → ℕ) (ρ : NontrivialZero) : ℝ≥0∞ :=
  (m ρ : ℝ≥0∞) * ENNReal.ofReal ((ρ.val.re - (1 / 2 : ℝ)) ^ 2)

def antiInvariantSum (m : NontrivialZero → ℕ) : ℝ≥0∞ :=
  ∑' ρ : NontrivialZero, weightedTerm m ρ

theorem weightedTerm_eq_zero_iff (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, 0 < m ρ) (ρ : NontrivialZero) :
    weightedTerm m ρ = 0 ↔ ρ.val.re = (1 / 2 : ℝ) := by
  unfold weightedTerm
  rw [mul_eq_zero]
  have hm0 : (m ρ : ℝ≥0∞) ≠ 0 := by exact_mod_cast (Nat.ne_of_gt (hm ρ))
  simp only [hm0, false_or, ENNReal.ofReal_eq_zero]
  constructor
  · intro h
    have hsq : 0 ≤ (ρ.val.re - (1 / 2 : ℝ)) ^ 2 := sq_nonneg _
    have hz : (ρ.val.re - (1 / 2 : ℝ)) ^ 2 = 0 := le_antisymm h hsq
    nlinarith [sq_nonneg (ρ.val.re - (1 / 2 : ℝ))]
  · intro h
    rw [h]
    norm_num

theorem antiInvariantSum_eq_zero_iff (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, 0 < m ρ) :
    antiInvariantSum m = 0 ↔
      ∀ s : ℂ, completedRiemannZeta s = 0 →
        0 < s.re → s.re < 1 → s.re = (1 / 2 : ℝ) := by
  rw [antiInvariantSum, ENNReal.tsum_eq_zero]
  constructor
  · intro h s hz hlo hhi
    exact (weightedTerm_eq_zero_iff m hm ⟨s, hz, hlo, hhi⟩).mp (h ⟨s, hz, hlo, hhi⟩)
  · intro h ρ
    exact (weightedTerm_eq_zero_iff m hm ρ).mpr
      (h ρ.val ρ.property.1 ρ.property.2.1 ρ.property.2.2)

/-- On the open right half-plane, completed and ordinary zeta have the
same zeros. The critical strip is contained in this domain. -/
theorem completed_zero_iff_zeta_zero_of_re_pos (s : ℂ) (hpos : 0 < s.re) :
    completedRiemannZeta s = 0 ↔ riemannZeta s = 0 := by
  have hs : s ≠ 0 := by
    intro h
    simp [h] at hpos
  rw [riemannZeta_def_of_ne_zero hs]
  simp [Complex.Gammaℝ_ne_zero_of_re_pos hpos]

/-- The exact classical critical-strip formulation consumed by the global
positive ledger. This does not yet assert the separately formalized exclusion
of zeros outside the strip. -/
def CriticalStripRH : Prop :=
  ∀ s : ℂ, riemannZeta s = 0 → 0 < s.re → s.re < 1 → s.re = (1 / 2 : ℝ)

/-- Mathlib's full `RiemannHypothesis` implies this critical-strip
statement. The converse is proved separately in `FullClassicalRHBridge`,
using the Gamma-factor exceptions and zero localization of the entire
completion. -/
theorem criticalStripRH_of_riemannHypothesis
    (hRH : RiemannHypothesis) : CriticalStripRH := by
  intro s hz hlo hhi
  apply hRH s hz
  · rintro ⟨n, rfl⟩
    norm_num at hlo
    have hn : (0 : ℝ) ≤ n := Nat.cast_nonneg n
    linarith
  · intro hs
    rw [hs] at hhi
    norm_num at hhi

theorem antiInvariantSum_eq_zero_iff_criticalStripRH (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, 0 < m ρ) :
    antiInvariantSum m = 0 ↔ CriticalStripRH := by
  rw [antiInvariantSum_eq_zero_iff m hm]
  constructor
  · intro h s hz hlo hhi
    exact h s ((completed_zero_iff_zeta_zero_of_re_pos s hlo).mpr hz) hlo hhi
  · intro h s hz hlo hhi
    exact h s ((completed_zero_iff_zeta_zero_of_re_pos s hlo).mp hz) hlo hhi

end SixBirdsDualityConfinement.RH.ClassicalZeroLedger
