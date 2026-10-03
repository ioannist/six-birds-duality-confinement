import Mathlib.Analysis.SpecialFunctions.Gaussian.FourierTransform
import SixBirdsDualityConfinement.RH.ComplexGaussianObservation
import SixBirdsDualityConfinement.RH.DivisorMultiplicityMoment

/-!
The center integral of one complex Gaussian does not depend on its
complex spectral coordinate. This is the precise loss of information
for the unweighted *linear* center integral; it says nothing about
nonlinear or center-local observations.
-/

namespace SixBirdsDualityConfinement.RH.GaussianCenterIntegralBlindness

noncomputable section
open MeasureTheory
open ComplexGaussianObservation ClassicalZeroLedger
open ArithmeticJensenWindows DivisorMultiplicityMoment

theorem center_integral_complex_gaussian (a : ℝ) (ha : 0 < a) (z : ℂ) :
    ∫ c : ℝ, Complex.exp (-(2 * (a : ℂ)) * (z - (c : ℂ)) ^ 2) =
      ((Real.pi : ℂ) / (2 * (a : ℂ))) ^ (1 / 2 : ℂ) := by
  have hb : (-(2 * (a : ℂ))).re < 0 := by simp [ha]
  have hfun :
      (fun c : ℝ => Complex.exp (-(2 * (a : ℂ)) * (z - (c : ℂ)) ^ 2)) =
        (fun c : ℝ => Complex.exp
          ((-(2 * (a : ℂ))) * (c : ℂ) ^ 2 +
            (4 * (a : ℂ) * z) * (c : ℂ) + (-(2 * (a : ℂ)) * z ^ 2))) := by
    funext c
    congr 1
    ring
  rw [hfun, integral_cexp_quadratic hb]
  have ha0 : (a : ℂ) ≠ 0 := by exact_mod_cast ne_of_gt ha
  have hcancel :
      -(2 * (a : ℂ)) * z ^ 2 -
        (4 * (a : ℂ) * z) ^ 2 / (4 * (-(2 * (a : ℂ)))) = 0 := by
    field_simp
    ring
  rw [hcancel]
  simp

theorem center_integral_real_gaussian (a : ℝ) (ha : 0 < a) (z : ℂ) :
    ∫ c : ℝ, (Complex.exp (-(2 * (a : ℂ)) * (z - (c : ℂ)) ^ 2)).re =
      (((Real.pi : ℂ) / (2 * (a : ℂ))) ^ (1 / 2 : ℂ)).re := by
  have hb : (-(2 * (a : ℂ))).re < 0 := by simp [ha]
  have hfun :
      (fun c : ℝ => Complex.exp (-(2 * (a : ℂ)) * (z - (c : ℂ)) ^ 2)) =
        (fun c : ℝ => Complex.exp
          ((-(2 * (a : ℂ))) * (c : ℂ) ^ 2 +
            (4 * (a : ℂ) * z) * (c : ℂ) + (-(2 * (a : ℂ)) * z ^ 2))) := by
    funext c
    congr 1
    ring
  have hi : Integrable
      (fun c : ℝ => Complex.exp (-(2 * (a : ℂ)) * (z - (c : ℂ)) ^ 2)) := by
    rw [hfun]
    exact integrable_cexp_quadratic' hb _ _
  change (∫ c : ℝ, RCLike.re
      (Complex.exp (-(2 * (a : ℂ)) * (z - (c : ℂ)) ^ 2))) = _
  rw [integral_re hi, center_integral_complex_gaussian a ha z]
  rfl

theorem center_integrable_real_gaussian (a : ℝ) (ha : 0 < a) (z : ℂ) :
    Integrable (fun c : ℝ =>
      (Complex.exp (-(2 * (a : ℂ)) * (z - (c : ℂ)) ^ 2)).re) := by
  have hb : (-(2 * (a : ℂ))).re < 0 := by simp [ha]
  have hfun :
      (fun c : ℝ => Complex.exp (-(2 * (a : ℂ)) * (z - (c : ℂ)) ^ 2)) =
        (fun c : ℝ => Complex.exp
          ((-(2 * (a : ℂ))) * (c : ℂ) ^ 2 +
            (4 * (a : ℂ) * z) * (c : ℂ) + (-(2 * (a : ℂ)) * z ^ 2))) := by
    funext c
    congr 1
    ring
  have hi : Integrable
      (fun c : ℝ => Complex.exp (-(2 * (a : ℂ)) * (z - (c : ℂ)) ^ 2)) := by
    rw [hfun]
    exact integrable_cexp_quadratic' hb _ _
  exact hi.re

theorem center_integral_finite_weighted_window
    {ι : Type*} (W : Finset ι) (m : ι → ℝ) (z : ι → ℂ)
    (a : ℝ) (ha : 0 < a) :
    ∫ c : ℝ, ∑ i ∈ W,
      m i * (Complex.exp (-(2 * (a : ℂ)) * (z i - (c : ℂ)) ^ 2)).re =
        (∑ i ∈ W, m i) *
          (((Real.pi : ℂ) / (2 * (a : ℂ))) ^ (1 / 2 : ℂ)).re := by
  rw [integral_finset_sum]
  · simp_rw [integral_const_mul, center_integral_real_gaussian a ha]
    rw [← Finset.sum_mul]
  · intro i hi
    exact (center_integrable_real_gaussian a ha (z i)).const_mul _

/-- On the actual completed-zeta zero carrier, the unweighted *linear*
center integral remembers only total multiplicity. Horizontal zero
displacements disappear. This is a scoped obstruction to paying the RH
XI charge with this particular integrated reading. -/
theorem actual_zero_window_center_integral
    (W : Finset NontrivialZero) (m : NontrivialZero → ℕ)
    (a : ℝ) (ha : 0 < a) :
    ∫ c : ℝ, ∑ ρ ∈ W, (m ρ : ℝ) *
      (Complex.exp (-(2 * (a : ℂ)) *
        (spectralCoordinate ρ.val - (c : ℂ)) ^ 2)).re =
      (∑ ρ ∈ W, (m ρ : ℝ)) *
        (((Real.pi : ℂ) / (2 * (a : ℂ))) ^ (1 / 2 : ℂ)).re :=
  center_integral_finite_weighted_window W
    (fun ρ => (m ρ : ℝ)) (fun ρ => spectralCoordinate ρ.val) a ha

/-- The same loss for the genuine analytic divisor multiplicities on a
canonical Jensen window of the completed zeta function. -/
theorem canonical_arithmetic_divisor_center_integral
    (n : ℕ) (a : ℝ) (ha : 0 < a) :
    ∫ c : ℝ, ∑ ρ ∈ canonicalJensenWindow n,
      (arithmeticZeroMultiplicity ρ : ℝ) *
        (Complex.exp (-(2 * (a : ℂ)) *
          (spectralCoordinate ρ.val - (c : ℂ)) ^ 2)).re =
      (∑ ρ ∈ canonicalJensenWindow n,
        (arithmeticZeroMultiplicity ρ : ℝ)) *
          (((Real.pi : ℂ) / (2 * (a : ℂ))) ^ (1 / 2 : ℂ)).re :=
  actual_zero_window_center_integral
    (canonicalJensenWindow n) arithmeticZeroMultiplicity a ha

#print axioms center_integral_complex_gaussian
#print axioms center_integral_real_gaussian
#print axioms center_integral_finite_weighted_window
#print axioms actual_zero_window_center_integral
#print axioms canonical_arithmetic_divisor_center_integral

end
end SixBirdsDualityConfinement.RH.GaussianCenterIntegralBlindness
