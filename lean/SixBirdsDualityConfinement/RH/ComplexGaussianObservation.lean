import SixBirdsDualityConfinement.RH.ActualInvolution
import Mathlib.Analysis.Complex.Trigonometric

/-!
The Gaussian in a zeta explicit formula is evaluated at the complex spectral
coordinate `γ = (ρ - 1/2)/i`, not merely at the real height `Im ρ`.
These pointwise algebraic facts show that its modulus detects real
displacement from the critical line. They do not supply an explicit formula
or a bound on the RH XI zero-window charge.
-/

noncomputable section
open scoped InnerProduct InnerProductSpace
namespace SixBirdsDualityConfinement.RH.ComplexGaussianObservation

open ActualInvolution ClassicalZeroLedger FiniteZeroWindows
open SixBirdsNeedles.XiCore

def spectralCoordinate (s : ℂ) : ℂ :=
  ⟨s.im, (1 / 2 : ℝ) - s.re⟩

def spectralGaussian (a : ℝ) (s : ℂ) : ℂ :=
  Complex.exp (-(a : ℂ) * spectralCoordinate s ^ 2)

theorem spectralCoordinate_re (s : ℂ) :
    (spectralCoordinate s).re = s.im := rfl

theorem spectralCoordinate_im (s : ℂ) :
    (spectralCoordinate s).im = (1 / 2 : ℝ) - s.re := rfl

theorem spectralCoordinate_J (s : ℂ) :
    spectralCoordinate (J s) = star (spectralCoordinate s) := by
  apply Complex.ext
  · simp [spectralCoordinate, J_im]
  · simp [spectralCoordinate, J_re]
    ring

theorem spectralGaussian_J (a : ℝ) (s : ℂ) :
    spectralGaussian a (J s) = star (spectralGaussian a s) := by
  rw [spectralGaussian, spectralGaussian, spectralCoordinate_J]
  rw [Complex.star_def, ← Complex.exp_conj]
  congr 1
  simp

theorem spectralGaussian_norm (a : ℝ) (s : ℂ) :
    ‖spectralGaussian a s‖ =
      Real.exp (-a * (s.im ^ 2 - (s.re - 1 / 2) ^ 2)) := by
  rw [spectralGaussian, Complex.norm_exp]
  congr 1
  simp only [spectralCoordinate, pow_two, Complex.neg_re, Complex.neg_im,
    Complex.mul_re, Complex.ofReal_re, Complex.ofReal_im]
  ring_nf

theorem spectralGaussian_re (a : ℝ) (s : ℂ) :
    (spectralGaussian a s).re =
      Real.exp (-a * (s.im ^ 2 - (s.re - 1 / 2) ^ 2)) *
        Real.cos (2 * a * s.im * (s.re - 1 / 2)) := by
  rw [spectralGaussian, Complex.exp_re]
  have hre : (-(a : ℂ) * spectralCoordinate s ^ 2).re =
      -a * (s.im ^ 2 - (s.re - 1 / 2) ^ 2) := by
    simp only [spectralCoordinate, pow_two, Complex.neg_re, Complex.neg_im,
      Complex.mul_re, Complex.ofReal_re, Complex.ofReal_im]
    ring_nf
  have him : (-(a : ℂ) * spectralCoordinate s ^ 2).im =
      2 * a * s.im * (s.re - 1 / 2) := by
    simp only [spectralCoordinate, pow_two, Complex.neg_re, Complex.neg_im,
      Complex.mul_re, Complex.mul_im, Complex.ofReal_re, Complex.ofReal_im]
    ring_nf
  rw [hre, him]

/-- A reflected pair contributes the real part of the complex Gaussian
to a linear trace. The modulus excess alone is not its contribution. -/
theorem spectralGaussian_J_pair_trace (a : ℝ) (s : ℂ) :
    spectralGaussian a s + spectralGaussian a (J s) =
      ((2 * (spectralGaussian a s).re : ℝ) : ℂ) := by
  rw [spectralGaussian_J, Complex.star_def]
  exact Complex.add_conj _

/-- A concrete point inside the critical strip has negative real Gaussian
trace at one width, even though its Gaussian modulus is positive. It is a
synthetic point, with no assertion that it is a zeta zero. -/
theorem synthetic_offline_gaussian_re_negative :
    (spectralGaussian 1 (⟨3 / 4, 2 * Real.pi⟩ : ℂ)).re < 0 := by
  rw [spectralGaussian_re]
  have hphase :
      2 * (1 : ℝ) * (2 * Real.pi) * (3 / 4 - 1 / 2) = Real.pi := by ring
  rw [hphase, Real.cos_pi]
  nlinarith [Real.exp_pos (-(1 : ℝ) *
    ((2 * Real.pi) ^ 2 - (3 / 4 - 1 / 2) ^ 2))]

/-- Every positive Gaussian width has a strictly larger modulus at an
off-line spectral coordinate than at the same real height on the line. -/
theorem spectralGaussian_norm_gt_height_gaussian
    (a : ℝ) (ha : 0 < a) (s : ℂ)
    (hs : s.re ≠ (1 / 2 : ℝ)) :
    Real.exp (-a * s.im ^ 2) < ‖spectralGaussian a s‖ := by
  rw [spectralGaussian_norm]
  apply Real.exp_lt_exp.mpr
  have hd : 0 < (s.re - (1 / 2 : ℝ)) ^ 2 := by
    apply sq_pos_of_ne_zero
    intro h
    apply hs
    linarith
  nlinarith

/-- This observation applies to the actual completed-zeta zero carrier.
It detects one off-line coordinate pointwise, without asserting that a
prime-side formula controls its size. -/
theorem actualZero_spectralGaussian_norm_gt_height_gaussian
    (a : ℝ) (ha : 0 < a) (ρ : NontrivialZero)
    (hρ : displacement ρ ≠ 0) :
    Real.exp (-a * ρ.val.im ^ 2) < ‖spectralGaussian a ρ.val‖ := by
  apply spectralGaussian_norm_gt_height_gaussian a ha ρ.val
  intro h
  apply hρ
  simp [displacement, h]

theorem actualZero_spectralGaussian_J (a : ℝ) (ρ : NontrivialZero) :
    spectralGaussian a (J_zero ρ).val =
      star (spectralGaussian a ρ.val) :=
  spectralGaussian_J a ρ.val

/-- The normalized log modulus removes the ordinary height damping and
recovers the squared real displacement exactly. It is a nonlinear
zero-side observation; the linear explicit formula does not give it. -/
def gaussianLogExcess (a : ℝ) (ρ : NontrivialZero) : ℝ :=
  Real.log ‖spectralGaussian a ρ.val‖ + a * ρ.val.im ^ 2

theorem gaussianLogExcess_eq (a : ℝ) (ρ : NontrivialZero) :
    gaussianLogExcess a ρ = a * displacement ρ ^ 2 := by
  unfold gaussianLogExcess displacement
  rw [spectralGaussian_norm, Real.log_exp]
  ring

def windowGaussianLogExcess (a : ℝ) (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) : ℝ :=
  ∑ ρ ∈ W, (m ρ : ℝ) * gaussianLogExcess a ρ

/-- At a fixed positive width, this nonlinear full-window observation is
exactly the scalar width times the actual RH zero-window XI energy. -/
theorem windowGaussianLogExcess_eq_windowEnergy
    (a : ℝ) (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) :
    windowGaussianLogExcess a m W = a * windowEnergy m W := by
  unfold windowGaussianLogExcess
  simp_rw [gaussianLogExcess_eq]
  calc
    ∑ ρ ∈ W, (m ρ : ℝ) * (a * displacement ρ ^ 2) =
        ∑ ρ ∈ W, a * ((m ρ : ℝ) * displacement ρ ^ 2) := by
          apply Finset.sum_congr rfl
          intro ρ hρ
          ring
    _ = a * windowEnergy m W := by
      rw [windowEnergy, Finset.mul_sum]

/-- On genuine `J`-reflected zero windows the same nonlinear observation is
exactly the XI residual energy, scaled by its Gaussian width. This is an
identity on actual zeros, not a prime-side source payment. -/
theorem windowGaussianLogExcess_eq_xi
    (a : ℝ) (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    windowGaussianLogExcess a m W =
      a * ‖hilbertKernelXi (invariantProbe W)
        (displacementVector m W)‖ ^ 2 := by
  rw [windowGaussianLogExcess_eq_windowEnergy]
  have hvker : displacementVector m W ∈ (invariantProbe W).ker :=
    invariantProbe_displacement_zero_J m hm W hW
  have hxi : ‖hilbertKernelXi (invariantProbe W)
      (displacementVector m W)‖ ^ 2 = windowEnergy m W := by
    change ‖(invariantProbe W).ker.starProjection (displacementVector m W)‖ ^ 2 = _
    rw [Submodule.starProjection_eq_self_iff.mpr hvker]
    exact displacementVector_norm_sq m W
  rw [hxi]

end SixBirdsDualityConfinement.RH.ComplexGaussianObservation
