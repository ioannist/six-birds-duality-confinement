import SixBirdsDualityConfinement.RH.ArithmeticJensenWindows

/-!
A zero-sensitive repair of the centered Jensen radial reading. A single
center mixes horizontal displacement with ordinate. Fourth radial
moments at three fixed real centers recover squared horizontal
displacement exactly, on every finite actual zeta-zero window. The
moments are divisor observables of the heat-built entire function,
but no estimate on their combination is asserted.
-/

noncomputable section
namespace SixBirdsDualityConfinement.RH.ShiftedJensenMoment

open ClassicalZeroLedger FiniteZeroWindows ArithmeticJensenWindows
open SixBirdsNeedles.XiCore

def shiftedCenter (a : ℝ) : ℂ := ⟨1 / 2 + a, 0⟩

def radialSq (a : ℝ) (s : ℂ) : ℝ :=
  (s.re - (1 / 2 + a)) ^ 2 + s.im ^ 2

theorem radialSq_eq_norm_sq (a : ℝ) (s : ℂ) :
    radialSq a s = ‖s - shiftedCenter a‖ ^ 2 := by
  rw [← Complex.normSq_eq_norm_sq]
  simp [radialSq, shiftedCenter, Complex.normSq_apply,
    Complex.sub_re, Complex.sub_im]
  ring

/-- A pointwise polarization identity: the three radial measurements
recover exactly the squared distance from the critical line. -/
theorem shifted_radial_fourth_difference (s : ℂ) :
    radialSq 1 s ^ 2 + radialSq (-1) s ^ 2 -
      2 * radialSq 0 s ^ 2 - 4 * radialSq 0 s - 2 =
        8 * (s.re - 1 / 2) ^ 2 := by
  unfold radialSq
  ring

/-- A synthetic strip point off the line and one on the line have the
same centered radial reading. They are not asserted to be zeta zeros. -/
private def offLineTestPoint : ℂ := ⟨13 / 20, 1 / 5⟩
private def onLineTestPoint : ℂ := ⟨1 / 2, 1 / 4⟩

theorem centered_radial_reading_blind_control :
    radialSq 0 offLineTestPoint = radialSq 0 onLineTestPoint ∧
      offLineTestPoint.re ≠ (1 / 2 : ℝ) ∧
      onLineTestPoint.re = (1 / 2 : ℝ) := by
  constructor
  · norm_num [radialSq, offLineTestPoint, onLineTestPoint]
  · constructor
    · norm_num [offLineTestPoint]
    · norm_num [onLineTestPoint]

def radialMoment2 (a : ℝ) (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) : ℝ :=
  ∑ ρ ∈ W, (m ρ : ℝ) * radialSq a ρ.val

def radialMoment4 (a : ℝ) (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) : ℝ :=
  ∑ ρ ∈ W, (m ρ : ℝ) * radialSq a ρ.val ^ 2

def windowMass (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) : ℝ :=
  ∑ ρ ∈ W, (m ρ : ℝ)

/-- The same identity on any finite actual zero window, with arbitrary
nonnegative natural multiplicity weights. -/
theorem shifted_moment_identity (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) :
    radialMoment4 1 m W + radialMoment4 (-1) m W -
      2 * radialMoment4 0 m W - 4 * radialMoment2 0 m W -
        2 * windowMass m W = 8 * windowEnergy m W := by
  simp only [radialMoment4, radialMoment2, windowMass, windowEnergy,
    Finset.mul_sum, ← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro ρ hρ
  have h := shifted_radial_fourth_difference ρ.val
  unfold displacement
  nlinarith

/-- On the divisor-derived Jensen windows, the three-center radial
moment defect is exactly eight times the *actual* Hilbert XI energy. -/
theorem canonicalJensen_shifted_moment_eq_xi (n : ℕ) :
    radialMoment4 1 unitWeights (canonicalJensenWindow n) +
      radialMoment4 (-1) unitWeights (canonicalJensenWindow n) -
      2 * radialMoment4 0 unitWeights (canonicalJensenWindow n) -
      4 * radialMoment2 0 unitWeights (canonicalJensenWindow n) -
      2 * windowMass unitWeights (canonicalJensenWindow n) =
        8 * ‖hilbertKernelXi (invariantProbe (canonicalJensenWindow n))
          (displacementVector unitWeights (canonicalJensenWindow n))‖ ^ 2 := by
  rw [shifted_moment_identity,
    canonicalJensenWindow_xi_eq_energy]

/-- A vanishing bound for the three-center moment defect, on the same
exhaustive actual divisor windows, conditionally reaches classical RH.
The heat/Mellin/Jensen identities do not supply this bound. -/
theorem criticalStripRH_of_shifted_moment_budget
    (b : ℕ → ℝ) (hb : Filter.Tendsto b Filter.atTop (nhds 0))
    (hbudget : ∀ n,
      radialMoment4 1 unitWeights (canonicalJensenWindow n) +
        radialMoment4 (-1) unitWeights (canonicalJensenWindow n) -
        2 * radialMoment4 0 unitWeights (canonicalJensenWindow n) -
        4 * radialMoment2 0 unitWeights (canonicalJensenWindow n) -
        2 * windowMass unitWeights (canonicalJensenWindow n) ≤ b n) :
    CriticalStripRH := by
  apply criticalStripRH_of_exhaustive_vanishing_budget
    unitWeights unitWeights_positive canonicalJensenWindow
    canonicalJensenWindow_eventuallyCovered b hb
  intro n
  have hnonneg : 0 ≤ windowEnergy unitWeights
      (canonicalJensenWindow n) := by
    unfold windowEnergy
    exact Finset.sum_nonneg (fun ρ _ => term_nonneg unitWeights ρ)
  have h := hbudget n
  rw [shifted_moment_identity] at h
  nlinarith

#print axioms radialSq_eq_norm_sq
#print axioms shifted_radial_fourth_difference
#print axioms centered_radial_reading_blind_control
#print axioms shifted_moment_identity
#print axioms canonicalJensen_shifted_moment_eq_xi
#print axioms criticalStripRH_of_shifted_moment_budget

end SixBirdsDualityConfinement.RH.ShiftedJensenMoment
