import SixBirdsDualityConfinement.RH.DivisorMultiplicityMoment
import SixBirdsDualityConfinement.RH.FullClassicalRHBridge

/-!
The RH displacement charge as a heat-time jet of genuine finite zero
divisors. This is a zero-side observable identity. It does not identify
the zero heat trace with a Navier state source or bound its jet.
-/

noncomputable section

namespace SixBirdsDualityConfinement.RH.GaussianDivisorHeatMoment

open Real
open SixBirdsDualityConfinement.RH.ClassicalZeroLedger
open SixBirdsDualityConfinement.RH.FiniteZeroWindows
open SixBirdsDualityConfinement.RH.ArithmeticJensenWindows
open SixBirdsDualityConfinement.RH.ShiftedJensenMoment
open SixBirdsDualityConfinement.RH.DivisorMultiplicityMoment
open SixBirdsDualityConfinement.RH.FullClassicalRHBridge

def zeroHeatTrace (a : ℝ) (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) (t : ℝ) : ℝ :=
  ∑ ρ ∈ W, (m ρ : ℝ) * exp (-t * radialSq a ρ.val)

def zeroHeatTraceFirst (a : ℝ) (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) (t : ℝ) : ℝ :=
  ∑ ρ ∈ W, -(m ρ : ℝ) * radialSq a ρ.val *
    exp (-t * radialSq a ρ.val)

def zeroHeatTraceSecond (a : ℝ) (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) (t : ℝ) : ℝ :=
  ∑ ρ ∈ W, (m ρ : ℝ) * radialSq a ρ.val ^ 2 *
    exp (-t * radialSq a ρ.val)

/-- A finite zero-divisor Gaussian trace as the *real center* moves
across the critical line. This is the same center variable used by the
real slice of the directional Navier Gaussian observation. -/
def zeroCenterTrace (t : ℝ) (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) (a : ℝ) : ℝ :=
  ∑ ρ ∈ W, (m ρ : ℝ) * exp (-t * radialSq a ρ.val)

def zeroCenterTraceFirst (t : ℝ) (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) (a : ℝ) : ℝ :=
  ∑ ρ ∈ W, (m ρ : ℝ) *
    (2 * t * (ρ.val.re - (1 / 2 + a))) *
      exp (-t * radialSq a ρ.val)

/-- The real-weighted form is needed to embed the signed RH displacement
vector into a Gaussian Fourier profile. -/
def weightedZeroCenterTrace (t : ℝ) (w : NontrivialZero → ℝ)
    (W : Finset NontrivialZero) (a : ℝ) : ℝ :=
  ∑ ρ ∈ W, w ρ * exp (-t * radialSq a ρ.val)

def weightedZeroCenterTraceFirst (t : ℝ) (w : NontrivialZero → ℝ)
    (W : Finset NontrivialZero) (a : ℝ) : ℝ :=
  ∑ ρ ∈ W, w ρ *
    (2 * t * (ρ.val.re - (1 / 2 + a))) *
      exp (-t * radialSq a ρ.val)

def zeroCenterTraceSecond (t : ℝ) (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) (a : ℝ) : ℝ :=
  ∑ ρ ∈ W, (m ρ : ℝ) *
    (4 * t ^ 2 * (ρ.val.re - (1 / 2 + a)) ^ 2 - 2 * t) *
      exp (-t * radialSq a ρ.val)

private theorem centerLinear_hasDerivAt (s : ℂ) (a : ℝ) :
    HasDerivAt (fun b : ℝ => s.re - (1 / 2 + b)) (-1) a := by
  convert (hasDerivAt_const a s.re).sub
    ((hasDerivAt_const a (1 / 2 : ℝ)).add (hasDerivAt_id a)) using 1
    <;> simp

private theorem radialSq_hasDerivAt_center (s : ℂ) (a : ℝ) :
    HasDerivAt (fun b : ℝ => radialSq b s)
      (-2 * (s.re - (1 / 2 + a))) a := by
  convert ((centerLinear_hasDerivAt s a).pow 2).add
    (hasDerivAt_const a (s.im ^ 2)) using 1
    <;> simp

theorem gaussianCenter_hasDerivAt (t : ℝ) (s : ℂ) (a : ℝ) :
    HasDerivAt (fun b : ℝ => exp (-t * radialSq b s))
      (2 * t * (s.re - (1 / 2 + a)) *
        exp (-t * radialSq a s)) a := by
  have harg : HasDerivAt (fun b : ℝ => -t * radialSq b s)
      (2 * t * (s.re - (1 / 2 + a))) a := by
    convert (radialSq_hasDerivAt_center s a).const_mul (-t) using 1 <;> ring
  convert (Real.hasDerivAt_exp (-t * radialSq a s)).comp a harg using 1 <;> ring

theorem zeroCenterTrace_hasDerivAt (t : ℝ) (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) (a : ℝ) :
    HasDerivAt (zeroCenterTrace t m W) (zeroCenterTraceFirst t m W a) a := by
  unfold zeroCenterTrace zeroCenterTraceFirst
  apply HasDerivAt.fun_sum
  intro ρ hρ
  convert (gaussianCenter_hasDerivAt t ρ.val a).const_mul (m ρ : ℝ) using 1
    <;> ring

theorem weightedZeroCenterTrace_hasDerivAt
    (t : ℝ) (w : NontrivialZero → ℝ)
    (W : Finset NontrivialZero) (a : ℝ) :
    HasDerivAt (weightedZeroCenterTrace t w W)
      (weightedZeroCenterTraceFirst t w W a) a := by
  unfold weightedZeroCenterTrace weightedZeroCenterTraceFirst
  apply HasDerivAt.fun_sum
  intro ρ hρ
  convert (gaussianCenter_hasDerivAt t ρ.val a).const_mul (w ρ) using 1
    <;> ring

theorem zeroCenterTraceFirst_hasDerivAt (t : ℝ) (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) (a : ℝ) :
    HasDerivAt (zeroCenterTraceFirst t m W)
      (zeroCenterTraceSecond t m W a) a := by
  unfold zeroCenterTraceFirst zeroCenterTraceSecond
  apply HasDerivAt.fun_sum
  intro ρ hρ
  have hlin : HasDerivAt
      (fun b : ℝ => 2 * t * (ρ.val.re - (1 / 2 + b))) (-2 * t) a := by
    convert (centerLinear_hasDerivAt ρ.val a).const_mul (2 * t) using 1
      <;> simp
  convert ((hlin.mul (gaussianCenter_hasDerivAt t ρ.val a)).const_mul
    (m ρ : ℝ)) using 1
  · funext y
    dsimp
    ring
  · dsimp
    ring

def zeroCenterWeightedEnergy (t : ℝ) (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) : ℝ :=
  ∑ ρ ∈ W, (m ρ : ℝ) *
    (ρ.val.re - 1 / 2) ^ 2 * exp (-t * radialSq 0 ρ.val)

/-- Transverse center curvature of a finite Gaussian zero trace is
exactly the positive Gaussian-weighted RH horizontal charge. The
ordinary trace term removes the Gaussian's universal `-2t` curvature.
This is an observation identity, with no source bound. -/
theorem center_curvature_eq_weighted_horizontal_energy
    (t : ℝ) (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) :
    zeroCenterTraceSecond t m W 0 +
      2 * t * zeroCenterTrace t m W 0 =
        4 * t ^ 2 * zeroCenterWeightedEnergy t m W := by
  unfold zeroCenterTraceSecond zeroCenterTrace zeroCenterWeightedEnergy
  rw [Finset.mul_sum]
  rw [Finset.mul_sum]
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro ρ hρ
  ring

theorem zeroCenterWeightedEnergy_eq_zero_iff
    (t : ℝ) (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (W : Finset NontrivialZero) :
    zeroCenterWeightedEnergy t m W = 0 ↔
      ∀ ρ ∈ W, displacement ρ = 0 := by
  have hterm : ∀ ρ ∈ W,
      0 ≤ (m ρ : ℝ) * (ρ.val.re - 1 / 2) ^ 2 *
        exp (-t * radialSq 0 ρ.val) := by
    intro ρ hρ
    positivity
  constructor
  · intro h ρ hρ
    have hz := (Finset.sum_eq_zero_iff_of_nonneg hterm).mp h ρ hρ
    have hmpos : (0 : ℝ) < m ρ := Nat.cast_pos.mpr (hm ρ)
    have hepos : 0 < exp (-t * radialSq 0 ρ.val) := Real.exp_pos _
    have hd : (ρ.val.re - 1 / 2) ^ 2 = 0 := by
      have hprod : (m ρ : ℝ) * (ρ.val.re - 1 / 2) ^ 2 = 0 :=
        (mul_eq_zero.mp hz).resolve_right (ne_of_gt hepos)
      exact (mul_eq_zero.mp hprod).resolve_left (ne_of_gt hmpos)
    unfold displacement
    nlinarith [sq_nonneg (ρ.val.re - 1 / 2)]
  · intro h
    unfold zeroCenterWeightedEnergy
    apply Finset.sum_eq_zero
    intro ρ hρ
    have hd : ρ.val.re - 1 / 2 = 0 := by
      simpa only [displacement] using h ρ hρ
    change (m ρ : ℝ) * (ρ.val.re - 1 / 2) ^ 2 *
      exp (-t * radialSq 0 ρ.val) = 0
    rw [hd]
    ring

/-- At any fixed positive Gaussian width, vanishing center curvature
on every exhaustive actual zero window is exactly full RH. The identity
detects the charge but supplies no bound on it. -/
theorem canonical_center_curvature_zero_iff_riemannHypothesis
    (t : ℝ) (ht : 0 < t) :
    (∀ n : ℕ,
      zeroCenterTraceSecond t arithmeticZeroMultiplicity
          (canonicalJensenWindow n) 0 +
        2 * t * zeroCenterTrace t arithmeticZeroMultiplicity
          (canonicalJensenWindow n) 0 = 0) ↔ RiemannHypothesis := by
  constructor
  · intro h
    apply riemannHypothesis_of_criticalStripRH
    apply criticalStripRH_of_exhaustive_vanishing_budget
      unitWeights unitWeights_positive canonicalJensenWindow
      canonicalJensenWindow_eventuallyCovered (fun _ => 0)
      tendsto_const_nhds
    intro n
    have hz := h n
    rw [center_curvature_eq_weighted_horizontal_energy] at hz
    have hweighted : zeroCenterWeightedEnergy t arithmeticZeroMultiplicity
        (canonicalJensenWindow n) = 0 := by
      have ht4 : 0 < 4 * t ^ 2 := by positivity
      nlinarith
    have hdisp := (zeroCenterWeightedEnergy_eq_zero_iff t
      arithmeticZeroMultiplicity arithmeticZeroMultiplicity_pos
      (canonicalJensenWindow n)).mp hweighted
    have henergy := (windowEnergy_eq_zero_iff unitWeights
      unitWeights_positive (canonicalJensenWindow n)).mpr hdisp
    simpa [henergy]
  · intro hRH n
    have hstrip := criticalStripRH_of_riemannHypothesis hRH
    have hdisp : ∀ ρ ∈ canonicalJensenWindow n,
        displacement ρ = 0 := by
      intro ρ hρ
      exact sub_eq_zero.mpr (hstrip ρ.val
        ((completed_zero_iff_zeta_zero_of_re_pos ρ.val ρ.property.2.1).mp
          ρ.property.1) ρ.property.2.1 ρ.property.2.2)
    rw [center_curvature_eq_weighted_horizontal_energy]
    have hz := (zeroCenterWeightedEnergy_eq_zero_iff t
      arithmeticZeroMultiplicity arithmeticZeroMultiplicity_pos
      (canonicalJensenWindow n)).mpr hdisp
    simp [hz]

theorem zeroHeatTrace_hasDerivAt (a : ℝ) (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) (t : ℝ) :
    HasDerivAt (zeroHeatTrace a m W) (zeroHeatTraceFirst a m W t) t := by
  unfold zeroHeatTrace zeroHeatTraceFirst
  apply HasDerivAt.fun_sum
  intro ρ hρ
  convert (Real.hasDerivAt_exp (-t * radialSq a ρ.val)).comp t
    ((hasDerivAt_id t).neg.mul_const (radialSq a ρ.val)) |>.const_mul (m ρ : ℝ) using 1
    ; ring

theorem zeroHeatTraceFirst_hasDerivAt (a : ℝ) (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) (t : ℝ) :
    HasDerivAt (zeroHeatTraceFirst a m W)
      (zeroHeatTraceSecond a m W t) t := by
  unfold zeroHeatTraceFirst zeroHeatTraceSecond
  apply HasDerivAt.fun_sum
  intro ρ hρ
  convert (Real.hasDerivAt_exp (-t * radialSq a ρ.val)).comp t
    ((hasDerivAt_id t).neg.mul_const (radialSq a ρ.val))
      |>.const_mul (-(m ρ : ℝ) * radialSq a ρ.val) using 1
    ; ring

theorem zeroHeatTrace_zero (a : ℝ) (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) :
    zeroHeatTrace a m W 0 = windowMass m W := by
  simp [zeroHeatTrace, windowMass]

theorem zeroHeatTraceFirst_zero (a : ℝ) (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) :
    zeroHeatTraceFirst a m W 0 = -radialMoment2 a m W := by
  simp [zeroHeatTraceFirst, radialMoment2, ← Finset.sum_neg_distrib]

theorem zeroHeatTraceSecond_zero (a : ℝ) (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) :
    zeroHeatTraceSecond a m W 0 = radialMoment4 a m W := by
  simp [zeroHeatTraceSecond, radialMoment4]

theorem heat_jet_horizontal_defect (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) :
    zeroHeatTraceSecond 1 m W 0 + zeroHeatTraceSecond (-1) m W 0 -
      2 * zeroHeatTraceSecond 0 m W 0 +
      4 * zeroHeatTraceFirst 0 m W 0 -
      2 * zeroHeatTrace 0 m W 0 = 8 * windowEnergy m W := by
  rw [zeroHeatTraceSecond_zero, zeroHeatTraceSecond_zero,
    zeroHeatTraceSecond_zero, zeroHeatTraceFirst_zero,
    zeroHeatTrace_zero]
  convert shifted_moment_identity m W using 1; ring

theorem canonical_divisor_heat_jet_dominates_XI (n : ℕ) :
    8 * ‖SixBirdsNeedles.XiCore.hilbertKernelXi
      (invariantProbe (canonicalJensenWindow n))
      (displacementVector unitWeights (canonicalJensenWindow n))‖ ^ 2 ≤
    zeroHeatTraceSecond 1 arithmeticZeroMultiplicity (canonicalJensenWindow n) 0 +
      zeroHeatTraceSecond (-1) arithmeticZeroMultiplicity (canonicalJensenWindow n) 0 -
      2 * zeroHeatTraceSecond 0 arithmeticZeroMultiplicity (canonicalJensenWindow n) 0 +
      4 * zeroHeatTraceFirst 0 arithmeticZeroMultiplicity (canonicalJensenWindow n) 0 -
      2 * zeroHeatTrace 0 arithmeticZeroMultiplicity (canonicalJensenWindow n) 0 := by
  rw [heat_jet_horizontal_defect]
  exact mul_le_mul_of_nonneg_left (canonicalJensen_unit_xi_le_divisor_energy n)
    (by norm_num)

/-- This states precisely the zero-side heat-jet estimate needed for the
classical conclusion. The vanishing budget remains an explicit premise. -/
theorem riemannHypothesis_of_divisor_heat_jet_budget
    (b : ℕ → ℝ) (hb : Filter.Tendsto b Filter.atTop (nhds 0))
    (hbudget : ∀ n : ℕ,
      zeroHeatTraceSecond 1 arithmeticZeroMultiplicity (canonicalJensenWindow n) 0 +
        zeroHeatTraceSecond (-1) arithmeticZeroMultiplicity (canonicalJensenWindow n) 0 -
        2 * zeroHeatTraceSecond 0 arithmeticZeroMultiplicity (canonicalJensenWindow n) 0 +
        4 * zeroHeatTraceFirst 0 arithmeticZeroMultiplicity (canonicalJensenWindow n) 0 -
        2 * zeroHeatTrace 0 arithmeticZeroMultiplicity (canonicalJensenWindow n) 0 ≤ b n) :
    RiemannHypothesis := by
  apply riemannHypothesis_of_criticalStripRH
  apply criticalStripRH_of_divisor_shifted_moment_budget b hb
  intro n
  have h := hbudget n
  rw [zeroHeatTraceSecond_zero, zeroHeatTraceSecond_zero,
    zeroHeatTraceSecond_zero, zeroHeatTraceFirst_zero,
    zeroHeatTrace_zero] at h
  convert h using 1; ring

#print axioms zeroHeatTrace_hasDerivAt
#print axioms zeroHeatTraceFirst_hasDerivAt
#print axioms zeroCenterTrace_hasDerivAt
#print axioms weightedZeroCenterTrace_hasDerivAt
#print axioms zeroCenterTraceFirst_hasDerivAt
#print axioms center_curvature_eq_weighted_horizontal_energy
#print axioms zeroCenterWeightedEnergy_eq_zero_iff
#print axioms canonical_center_curvature_zero_iff_riemannHypothesis
#print axioms heat_jet_horizontal_defect
#print axioms canonical_divisor_heat_jet_dominates_XI
#print axioms riemannHypothesis_of_divisor_heat_jet_budget

end SixBirdsDualityConfinement.RH.GaussianDivisorHeatMoment
