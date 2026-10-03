import SixBirdsDualityConfinement.RH.ShiftedJensenMoment

/-!
The shifted zero moments can use the genuine positive multiplicities of
the arithmetic entire function's Jensen divisor. A separate theorem
shows that the full disk divisor support is exactly the critical-strip
zero window. No boundary reconstruction, moment estimate, or source-work
estimate is asserted.
-/

noncomputable section
open Complex Metric Filter
open scoped Topology
namespace SixBirdsDualityConfinement.RH.DivisorMultiplicityMoment

open ClassicalZeroLedger FiniteZeroWindows ArithmeticXiJensen
open ArithmeticJensenWindows ShiftedJensenMoment

private theorem arithmeticXiEntire_analytic_univ :
    AnalyticOnNhd ℂ arithmeticXiEntire Set.univ :=
  Complex.analyticOnNhd_univ_iff_differentiable.mpr
    arithmeticXiEntire_differentiable

def arithmeticZeroMultiplicity (ρ : NontrivialZero) : ℕ :=
  (MeromorphicOn.divisor arithmeticXiEntire Set.univ ρ.val).natAbs

theorem arithmeticZeroMultiplicity_eq_disk
    (c : ℂ) (R : ℝ) (ρ : NontrivialZero)
    (hρ : ρ.val ∈ closedBall c |R|) :
    arithmeticZeroMultiplicity ρ =
      (MeromorphicOn.divisor arithmeticXiEntire
        (closedBall c |R|) ρ.val).natAbs := by
  have huniv : MeromorphicOn arithmeticXiEntire Set.univ :=
    arithmeticXiEntire_analytic_univ.meromorphicOn
  have hdisk : MeromorphicOn arithmeticXiEntire (closedBall c |R|) :=
    fun z hz => arithmeticXiEntire_analytic_univ.meromorphicOn z (Set.mem_univ z)
  simp [arithmeticZeroMultiplicity,
    MeromorphicOn.divisor_apply huniv (Set.mem_univ ρ.val),
    MeromorphicOn.divisor_apply hdisk hρ]

theorem disk_divisor_nonneg (c : ℂ) (R : ℝ) :
    0 ≤ MeromorphicOn.divisor arithmeticXiEntire (closedBall c |R|) := by
  let U := closedBall c |R|
  have han : AnalyticOnNhd ℂ arithmeticXiEntire U :=
    fun z hz => arithmeticXiEntire_analytic_univ z (Set.mem_univ z)
  exact ((han.meromorphicNFOn).divisor_nonneg_iff_analyticOnNhd).mpr han

theorem arithmeticZeroMultiplicity_eq_divisor
    (c : ℂ) (R : ℝ) (ρ : NontrivialZero)
    (hρ : ρ.val ∈ closedBall c |R|) :
    (arithmeticZeroMultiplicity ρ : ℤ) =
      MeromorphicOn.divisor arithmeticXiEntire (closedBall c |R|) ρ.val := by
  rw [arithmeticZeroMultiplicity_eq_disk c R ρ hρ]
  rw [Int.natCast_natAbs,
    abs_of_nonneg (disk_divisor_nonneg c R ρ.val)]

theorem arithmeticZeroMultiplicity_pos_on_disk
    (c : ℂ) (R : ℝ) (ρ : NontrivialZero)
    (hρ : ρ ∈ zeroDiskWindow c R) :
    0 < arithmeticZeroMultiplicity ρ := by
  have hmem := (mem_zeroDiskWindow c R ρ).mp hρ
  have hzeta : riemannZeta ρ.val = 0 :=
    (completed_zero_iff_zeta_zero_of_re_pos ρ.val ρ.property.2.1).mp
      ρ.property.1
  have hsupport : ρ.val ∈ Function.support
      (MeromorphicOn.divisor arithmeticXiEntire (closedBall c |R|)) :=
    (arithmeticXi_circle_divisor_support_iff_zeta_zero
      c R ρ.val hmem ρ.property.2.1 ρ.property.2.2).mpr hzeta
  apply Nat.pos_of_ne_zero
  intro hm
  apply hsupport
  have heq := arithmeticZeroMultiplicity_eq_divisor c R ρ hmem
  simpa [hm] using heq.symm

theorem arithmeticZeroMultiplicity_pos (ρ : NontrivialZero) :
    0 < arithmeticZeroMultiplicity ρ := by
  obtain ⟨n, hn⟩ := (canonicalJensenWindow_eventuallyCovered ρ).exists
  exact arithmeticZeroMultiplicity_pos_on_disk
    (criticalLineCenter 0) n ρ hn

/-- On the critical-strip restriction of a single Jensen disk, these
shifted moments use the exact divisor multiplicities at every point. -/
theorem divisor_shifted_moment_identity (n : ℕ) :
    radialMoment4 1 arithmeticZeroMultiplicity (canonicalJensenWindow n) +
      radialMoment4 (-1) arithmeticZeroMultiplicity (canonicalJensenWindow n) -
      2 * radialMoment4 0 arithmeticZeroMultiplicity (canonicalJensenWindow n) -
      4 * radialMoment2 0 arithmeticZeroMultiplicity (canonicalJensenWindow n) -
      2 * windowMass arithmeticZeroMultiplicity (canonicalJensenWindow n) =
        8 * windowEnergy arithmeticZeroMultiplicity (canonicalJensenWindow n) :=
  shifted_moment_identity arithmeticZeroMultiplicity (canonicalJensenWindow n)

/-- Positive analytic multiplicities make the divisor-weighted energy
dominate the unit-weight XI charge used by the existing RH endpoint. -/
theorem canonicalJensen_unit_xi_le_divisor_energy (n : ℕ) :
    ‖SixBirdsNeedles.XiCore.hilbertKernelXi
      (invariantProbe (canonicalJensenWindow n))
      (displacementVector unitWeights (canonicalJensenWindow n))‖ ^ 2 ≤
        windowEnergy arithmeticZeroMultiplicity (canonicalJensenWindow n) := by
  rw [canonicalJensenWindow_xi_eq_energy]
  unfold windowEnergy
  apply Finset.sum_le_sum
  intro ρ hρ
  have hm : (1 : ℝ) ≤ (arithmeticZeroMultiplicity ρ : ℝ) := by
    exact_mod_cast arithmeticZeroMultiplicity_pos_on_disk
      (criticalLineCenter 0) n ρ hρ
  simpa [unitWeights] using
    mul_le_mul_of_nonneg_right hm (sq_nonneg (displacement ρ))

/-- The pointwise polynomial kernel whose divisor sum detects squared
horizontal displacement. It is evaluated on one fixed Jensen disk. -/
def radialDefect (s : ℂ) : ℝ :=
  radialSq 1 s ^ 2 + radialSq (-1) s ^ 2 -
    2 * radialSq 0 s ^ 2 - 4 * radialSq 0 s - 2

theorem radialDefect_eq (s : ℂ) :
    radialDefect s = 8 * (s.re - 1 / 2) ^ 2 :=
  shifted_radial_fourth_difference s

/-- A polynomial-weighted sum over the *full* Jensen divisor on one disk.
Unlike shifted circle averages, every term uses the same disk support. -/
def divisorRadialDefect (c : ℂ) (R : ℝ) : ℝ :=
  ∑ᶠ s, ((MeromorphicOn.divisor arithmeticXiEntire
    (closedBall c |R|) s : ℤ) : ℝ) * radialDefect s

theorem divisorRadialDefect_eq_window_energy (c : ℂ) (R : ℝ) :
    divisorRadialDefect c R =
      8 * windowEnergy arithmeticZeroMultiplicity (zeroDiskWindow c R) := by
  let W := zeroDiskWindow c R
  let D := MeromorphicOn.divisor arithmeticXiEntire (closedBall c |R|)
  have hsupport : Function.support
      (fun s : ℂ => ((D s : ℤ) : ℝ) * radialDefect s) ⊆
        ↑(W.image Subtype.val) := by
    intro s hs
    have hD : D s ≠ 0 := by
      intro hz
      exact hs (by simp [hz])
    have hmem : s ∈ Function.support D := hD
    rw [← zeroDiskWindow_image_eq_divisor_support c R] at hmem
    obtain ⟨ρ, hρ, rfl⟩ := hmem
    exact Finset.mem_image.mpr ⟨ρ, hρ, rfl⟩
  change (∑ᶠ s, ((D s : ℤ) : ℝ) * radialDefect s) = _
  rw [finsum_eq_sum_of_support_subset _ hsupport]
  rw [Finset.sum_image (fun ρ hρ σ hσ h => Subtype.val_injective h)]
  calc
    (∑ ρ ∈ W, ((D ρ.val : ℤ) : ℝ) * radialDefect ρ.val) =
        ∑ ρ ∈ W, (arithmeticZeroMultiplicity ρ : ℝ) *
          (8 * displacement ρ ^ 2) := by
      apply Finset.sum_congr rfl
      intro ρ hρ
      have hmem := (mem_zeroDiskWindow c R ρ).mp hρ
      have hm := arithmeticZeroMultiplicity_eq_divisor c R ρ hmem
      have hcast : ((D ρ.val : ℤ) : ℝ) =
          (arithmeticZeroMultiplicity ρ : ℝ) := by
        exact_mod_cast hm.symm
      rw [hcast, radialDefect_eq]
      rfl
    _ = 8 * windowEnergy arithmeticZeroMultiplicity W := by
      simp only [windowEnergy, Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro ρ hρ
      ring

/-- The full polynomial-weighted Jensen divisor on one canonical disk
dominates eight times the existing unit-weight RH Hilbert XI residual. -/
theorem canonicalJensen_xi_le_divisorRadialDefect (n : ℕ) :
    8 * ‖SixBirdsNeedles.XiCore.hilbertKernelXi
      (invariantProbe (canonicalJensenWindow n))
      (displacementVector unitWeights (canonicalJensenWindow n))‖ ^ 2 ≤
      divisorRadialDefect (criticalLineCenter 0) n := by
  rw [divisorRadialDefect_eq_window_energy]
  exact mul_le_mul_of_nonneg_left
    (canonicalJensen_unit_xi_le_divisor_energy n) (by norm_num)

/-- An actual divisor-side vanishing budget would pay the classical RH
endpoint. Neither Jensen's boundary identity nor the shared free heat
representation proves this quantitative budget. -/
theorem criticalStripRH_of_divisorRadialDefect_budget
    (b : ℕ → ℝ) (hb : Tendsto b atTop (nhds 0))
    (hbudget : ∀ n : ℕ,
      divisorRadialDefect (criticalLineCenter 0) n ≤ b n) :
    CriticalStripRH := by
  apply criticalStripRH_of_exhaustive_vanishing_budget
    unitWeights unitWeights_positive canonicalJensenWindow
    canonicalJensenWindow_eventuallyCovered b hb
  intro n
  have hxi := canonicalJensen_xi_le_divisorRadialDefect n
  rw [canonicalJensenWindow_xi_eq_energy] at hxi
  have hnonneg : 0 ≤ windowEnergy unitWeights
      (canonicalJensenWindow n) := by
    unfold windowEnergy
    exact Finset.sum_nonneg (fun ρ _ => term_nonneg unitWeights ρ)
  nlinarith [hbudget n]

/-- A vanishing bound on the divisor-weighted defect conditionally reaches
the classical zeta-zero statement. The bound itself remains unproved. -/
theorem criticalStripRH_of_divisor_shifted_moment_budget
    (b : ℕ → ℝ) (hb : Tendsto b atTop (nhds 0))
    (hbudget : ∀ n,
      radialMoment4 1 arithmeticZeroMultiplicity (canonicalJensenWindow n) +
        radialMoment4 (-1) arithmeticZeroMultiplicity (canonicalJensenWindow n) -
        2 * radialMoment4 0 arithmeticZeroMultiplicity (canonicalJensenWindow n) -
        4 * radialMoment2 0 arithmeticZeroMultiplicity (canonicalJensenWindow n) -
        2 * windowMass arithmeticZeroMultiplicity (canonicalJensenWindow n) ≤ b n) :
    CriticalStripRH := by
  apply criticalStripRH_of_exhaustive_vanishing_budget
    arithmeticZeroMultiplicity arithmeticZeroMultiplicity_pos
    canonicalJensenWindow canonicalJensenWindow_eventuallyCovered b hb
  intro n
  have hnonneg : 0 ≤ windowEnergy arithmeticZeroMultiplicity
      (canonicalJensenWindow n) := by
    unfold windowEnergy
    exact Finset.sum_nonneg (fun ρ _ => term_nonneg arithmeticZeroMultiplicity ρ)
  have h := hbudget n
  rw [divisor_shifted_moment_identity] at h
  nlinarith

#print axioms arithmeticZeroMultiplicity_eq_divisor
#print axioms arithmeticZeroMultiplicity_pos
#print axioms divisor_shifted_moment_identity
#print axioms canonicalJensen_unit_xi_le_divisor_energy
#print axioms divisorRadialDefect_eq_window_energy
#print axioms canonicalJensen_xi_le_divisorRadialDefect
#print axioms criticalStripRH_of_divisorRadialDefect_budget
#print axioms criticalStripRH_of_divisor_shifted_moment_budget

end SixBirdsDualityConfinement.RH.DivisorMultiplicityMoment
