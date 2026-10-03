import SixBirdsDualityConfinement.RH.ActualInvolution
import Mathlib.Analysis.Complex.JensenFormula
import Mathlib.NumberTheory.LSeries.Nonvanishing

/-!
The actual entire completion `s(s-1)Λ(s)` of completed Riemann zeta,
expressed through Mathlib's entire pole-corrected `Λ₀`. Jensen's formula
then gives a direct identity from circle averages of this arithmetic
function to its zero divisor. This is a zero-side arithmetic bridge, not
a source-work inequality or a prime explicit formula.
-/

noncomputable section
open Complex Metric Real
namespace SixBirdsDualityConfinement.RH.ArithmeticXiJensen

open ClassicalZeroLedger
open ActualInvolution CompletedZetaConjugation

def arithmeticXiEntire (s : ℂ) : ℂ :=
  s * (s - 1) * completedRiemannZeta₀ s + 1

theorem arithmeticXiEntire_differentiable :
    Differentiable ℂ arithmeticXiEntire := by
  unfold arithmeticXiEntire
  exact ((differentiable_id.mul
    (differentiable_id.sub_const 1)).mul
      differentiable_completedZeta₀).add_const 1

theorem arithmeticXiEntire_one_sub (s : ℂ) :
    arithmeticXiEntire (1 - s) = arithmeticXiEntire s := by
  unfold arithmeticXiEntire
  rw [completedRiemannZeta₀_one_sub]
  ring

theorem arithmeticXiEntire_eq_completed (s : ℂ)
    (hs0 : s ≠ 0) (hs1 : s ≠ 1) :
    arithmeticXiEntire s =
      s * (s - 1) * completedRiemannZeta s := by
  rw [completedRiemannZeta_eq]
  unfold arithmeticXiEntire
  have h1s : (1 : ℂ) - s ≠ 0 := sub_ne_zero.mpr hs1.symm
  field_simp [hs0, h1s]
  ring

theorem arithmeticXiEntire_zero_iff_completed
    (s : ℂ) (hlo : 0 < s.re) (hhi : s.re < 1) :
    arithmeticXiEntire s = 0 ↔ completedRiemannZeta s = 0 := by
  have hs0 : s ≠ 0 := by
    intro h
    simp [h] at hlo
  have hs1 : s ≠ 1 := by
    intro h
    simp [h] at hhi
  rw [arithmeticXiEntire_eq_completed s hs0 hs1]
  simp [hs0, sub_ne_zero.mpr hs1]

theorem arithmeticXiEntire_zero_iff_zeta
    (s : ℂ) (hlo : 0 < s.re) (hhi : s.re < 1) :
    arithmeticXiEntire s = 0 ↔ riemannZeta s = 0 :=
  (arithmeticXiEntire_zero_iff_completed s hlo hhi).trans
    (completed_zero_iff_zeta_zero_of_re_pos s hlo)

/-- The entire arithmetic completion has no zeros in the closed right
half-plane `Re s ≥ 1`. This uses Mathlib's proved zeta nonvanishing
there, including the special value at `s = 1`. -/
theorem arithmeticXiEntire_ne_zero_of_one_le_re
    (s : ℂ) (hs : 1 ≤ s.re) : arithmeticXiEntire s ≠ 0 := by
  by_cases hs1 : s = 1
  · subst s
    have h1 : arithmeticXiEntire 1 = arithmeticXiEntire 0 := by
      simpa using arithmeticXiEntire_one_sub (0 : ℂ)
    rw [h1]
    norm_num [arithmeticXiEntire]
  have hs0 : s ≠ 0 := by
    intro h
    simp [h] at hs
    linarith
  have hpos : 0 < s.re := by linarith
  have hzeta : riemannZeta s ≠ 0 := riemannZeta_ne_zero_of_one_le_re hs
  have hcompleted : completedRiemannZeta s ≠ 0 :=
    (completed_zero_iff_zeta_zero_of_re_pos s hpos).not.mpr hzeta
  rw [arithmeticXiEntire_eq_completed s hs0 hs1]
  exact mul_ne_zero (mul_ne_zero hs0 (sub_ne_zero.mpr hs1)) hcompleted

/-- All zeros of the arithmetic entire completion lie inside the open
critical strip. This is localization, not the Riemann hypothesis. -/
theorem arithmeticXiEntire_zero_in_critical_strip
    (s : ℂ) (hz : arithmeticXiEntire s = 0) :
    0 < s.re ∧ s.re < 1 := by
  have hright : s.re < 1 := by
    by_contra h
    exact (arithmeticXiEntire_ne_zero_of_one_le_re s (le_of_not_gt h)) hz
  have hleft : 0 < s.re := by
    by_contra h
    have hmirror : 1 ≤ (1 - s).re := by
      simp only [Complex.sub_re, Complex.one_re]
      linarith
    exact (arithmeticXiEntire_ne_zero_of_one_le_re (1 - s) hmirror)
      ((arithmeticXiEntire_one_sub s).trans hz)
  exact ⟨hleft, hright⟩

theorem arithmeticXiEntire_conj_strip
    (s : ℂ) (hlo : 0 < s.re) (hhi : s.re < 1) :
    arithmeticXiEntire (star s) = star (arithmeticXiEntire s) := by
  have hs0 : s ≠ 0 := by
    intro h
    simp [h] at hlo
  have hs1 : s ≠ 1 := by
    intro h
    simp [h] at hhi
  have hstar0 : star s ≠ 0 := by simpa using hs0
  have hstar1 : star s ≠ 1 := by
    intro h
    apply hs1
    have hh := congrArg star h
    simpa using hh
  rw [arithmeticXiEntire_eq_completed (star s) hstar0 hstar1,
    arithmeticXiEntire_eq_completed s hs0 hs1,
    completedRiemannZeta_conj]
  simp only [Complex.star_def, map_mul, map_sub, map_one]

theorem arithmeticXiEntire_J_strip
    (s : ℂ) (hlo : 0 < s.re) (hhi : s.re < 1) :
    arithmeticXiEntire (J s) = star (arithmeticXiEntire s) := by
  change arithmeticXiEntire (1 - star s) = _
  rw [arithmeticXiEntire_one_sub]
  exact arithmeticXiEntire_conj_strip s hlo hhi

private theorem arithmeticXiEntire_analyticOnNhd :
    AnalyticOnNhd ℂ arithmeticXiEntire Set.univ :=
  Complex.analyticOnNhd_univ_iff_differentiable.mpr
    arithmeticXiEntire_differentiable

private theorem arithmeticXiEntire_order_ne_top (s : ℂ) :
    meromorphicOrderAt arithmeticXiEntire s ≠ ⊤ := by
  have hmeromorphic : MeromorphicOn arithmeticXiEntire Set.univ :=
    arithmeticXiEntire_analyticOnNhd.meromorphicOn
  have hnf : MeromorphicNFOn arithmeticXiEntire Set.univ :=
    arithmeticXiEntire_analyticOnNhd.meromorphicNFOn
  have h0 : arithmeticXiEntire 0 ≠ 0 := by
    norm_num [arithmeticXiEntire]
  have horderEq : meromorphicOrderAt arithmeticXiEntire 0 = 0 :=
    (hnf (z := 0) (Set.mem_univ _)).meromorphicOrderAt_eq_zero_iff.mpr h0
  have horder0 : meromorphicOrderAt arithmeticXiEntire 0 ≠ ⊤ := by
    rw [horderEq]
    exact WithTop.zero_ne_top
  exact hmeromorphic.meromorphicOrderAt_ne_top_of_isPreconnected
    isPreconnected_univ (Set.mem_univ (0 : ℂ)) (Set.mem_univ s) horder0

/-- Within any Jensen disk, the divisor's support in the critical strip is
exactly the actual Riemann-zeta zero set. This identifies the divisor in
the circle identity with the RH carrier without assuming RH. -/
theorem arithmeticXi_circle_divisor_support_iff_zeta_zero
    (c : ℂ) (R : ℝ) (s : ℂ)
    (hs : s ∈ closedBall c |R|)
    (hlo : 0 < s.re) (hhi : s.re < 1) :
    s ∈ Function.support
      (MeromorphicOn.divisor arithmeticXiEntire (closedBall c |R|)) ↔
      riemannZeta s = 0 := by
  let U := closedBall c |R|
  have hnf : MeromorphicNFOn arithmeticXiEntire U :=
    fun z hz => arithmeticXiEntire_analyticOnNhd.meromorphicNFOn
      (z := z) (Set.mem_univ z)
  have hsupport := hnf.zero_set_eq_divisor_support
    (fun u => arithmeticXiEntire_order_ne_top u)
  rw [← hsupport]
  simp only [Set.mem_inter_iff, Set.mem_preimage, Set.mem_singleton_iff]
  exact and_iff_right hs |>.trans (arithmeticXiEntire_zero_iff_zeta s hlo hhi)

/-- The full divisor support on a Jensen disk consists exactly of the
actual critical-strip zeta zeros on that disk; the entire completion
has no additional zero locations outside the strip. -/
theorem arithmeticXi_circle_divisor_support_iff_classical_zero
    (c : ℂ) (R : ℝ) (s : ℂ)
    (hs : s ∈ closedBall c |R|) :
    s ∈ Function.support
      (MeromorphicOn.divisor arithmeticXiEntire (closedBall c |R|)) ↔
      riemannZeta s = 0 ∧ 0 < s.re ∧ s.re < 1 := by
  let U := closedBall c |R|
  have hnf : MeromorphicNFOn arithmeticXiEntire U :=
    fun z hz => arithmeticXiEntire_analyticOnNhd.meromorphicNFOn
      (z := z) (Set.mem_univ z)
  have hsupport := hnf.zero_set_eq_divisor_support
    (fun u => arithmeticXiEntire_order_ne_top u)
  constructor
  · intro hd
    rw [← hsupport] at hd
    have hstrip := arithmeticXiEntire_zero_in_critical_strip s hd.2
    exact ⟨(arithmeticXiEntire_zero_iff_zeta s hstrip.1 hstrip.2).mp hd.2,
      hstrip.1, hstrip.2⟩
  · rintro ⟨hzeta, hlo, hhi⟩
    exact (arithmeticXi_circle_divisor_support_iff_zeta_zero
      c R s hs hlo hhi).mpr hzeta

/-- Jensen's exact identity on an arbitrary circle for the actual entire
arithmetic completion. Its divisor term counts the genuine zeros; no
estimate on their horizontal displacement is implied. -/
theorem arithmeticXiEntire_jensen (c : ℂ) (R : ℝ) (hR : R ≠ 0) :
    circleAverage (Real.log ‖arithmeticXiEntire ·‖) c R =
      ∑ᶠ u, MeromorphicOn.divisor arithmeticXiEntire (closedBall c |R|) u *
        Real.log (R * ‖c - u‖⁻¹) +
      MeromorphicOn.divisor arithmeticXiEntire (closedBall c |R|) c *
        Real.log R +
      Real.log ‖meromorphicTrailingCoeffAt arithmeticXiEntire c‖ := by
  have hanalytic : AnalyticOnNhd ℂ arithmeticXiEntire Set.univ :=
    Complex.analyticOnNhd_univ_iff_differentiable.mpr
      arithmeticXiEntire_differentiable
  exact MeromorphicOn.circleAverage_log_norm hR
    (fun x _ => hanalytic.meromorphicOn x (Set.mem_univ x))

#print axioms arithmeticXiEntire_zero_iff_zeta
#print axioms arithmeticXiEntire_zero_in_critical_strip
#print axioms arithmeticXiEntire_J_strip
#print axioms arithmeticXi_circle_divisor_support_iff_zeta_zero
#print axioms arithmeticXi_circle_divisor_support_iff_classical_zero
#print axioms arithmeticXiEntire_jensen

end SixBirdsDualityConfinement.RH.ArithmeticXiJensen
