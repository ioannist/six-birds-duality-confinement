import SixBirdsDualityConfinement.RH.ActualInvolution

/-! The actual completed-zeta `J` symmetry transports zero-window
displacements isometrically. It supplies cancellation in the invariant
native probe but no strict decay of the blind XI state. -/
noncomputable section
namespace SixBirdsDualityConfinement.RH.JTransportNoGo

open ClassicalZeroLedger FiniteZeroWindows ActualInvolution
open SixBirdsNeedles.XiCore

def windowJEquiv (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    {ρ // ρ ∈ W} ≃ {ρ // ρ ∈ W} where
  toFun ρ := ⟨J_zero ρ.val, hW ρ.val ρ.property⟩
  invFun ρ := ⟨J_zero ρ.val, hW ρ.val ρ.property⟩
  left_inv ρ := Subtype.ext (J_zero_involutive ρ.val)
  right_inv ρ := Subtype.ext (J_zero_involutive ρ.val)

def windowJTransport (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    EuclideanSpace ℝ {ρ // ρ ∈ W} ≃ₗᵢ[ℝ]
      EuclideanSpace ℝ {ρ // ρ ∈ W} :=
  LinearIsometryEquiv.piLpCongrLeft 2 ℝ ℝ (windowJEquiv W hW)

theorem windowJTransport_displacement_neg
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    windowJTransport W hW (displacementVector m W) =
      -displacementVector m W := by
  ext ρ
  change Real.sqrt (m (J_zero ρ.val)) * displacement (J_zero ρ.val) =
    -(Real.sqrt (m ρ.val) * displacement ρ.val)
  rw [hm, displacement_J_zero]
  ring

theorem windowJTransport_displacement_norm
    (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    ‖windowJTransport W hW (displacementVector m W)‖ ^ 2 =
      windowEnergy m W := by
  rw [LinearIsometryEquiv.norm_map]
  exact displacementVector_norm_sq m W

/-- Every bounded linear observation invariant under the actual zero-set
involution annihilates the J-odd displacement. This is a generic parity
obstruction; it does not assert that a proposed arithmetic observation has
been mapped onto this window carrier. -/
theorem invariant_linear_observation_displacement_zero
    {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F]
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W)
    (L : EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ] F)
    (hJ : ∀ v, L (windowJTransport W hW v) = L v) :
    L (displacementVector m W) = 0 := by
  have h := hJ (displacementVector m W)
  rw [windowJTransport_displacement_neg m hm W hW, map_neg] at h
  have hs : L (displacementVector m W) = -L (displacementVector m W) := h.symm
  have htwo : (2 : ℝ) • L (displacementVector m W) = 0 := by
    rw [two_smul]
    nth_rewrite 2 [hs]
    exact add_neg_cancel _
  exact (smul_eq_zero.mp htwo).resolve_left (by norm_num)

/-- Symmetrization by the actual completed-zeta involution. It is a
strictly reducing map on anti-invariant displacements, but return to the
original displacement must be checked separately. -/
def windowJAverage (W : Finset NontrivialZero) (hW : JReflectedWindow W)
    (v : EuclideanSpace ℝ {ρ // ρ ∈ W}) :
    EuclideanSpace ℝ {ρ // ρ ∈ W} :=
  (1 / 2 : ℝ) • (v + windowJTransport W hW v)

theorem windowJAverage_displacement_zero
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    windowJAverage W hW (displacementVector m W) = 0 := by
  rw [windowJAverage, windowJTransport_displacement_neg m hm W hW]
  simp

/-- Recovering the original displacement after symmetrization is
equivalent to its original XI energy already vanishing. -/
theorem windowJAverage_return_iff_zero_energy
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    windowJAverage W hW (displacementVector m W) =
      displacementVector m W ↔ windowEnergy m W = 0 := by
  rw [windowJAverage_displacement_zero m hm W hW]
  constructor
  · intro hv
    rw [← displacementVector_norm_sq, ← hv]
    simp
  · intro hz
    have hnorm : ‖displacementVector m W‖ ^ 2 = 0 := by
      simpa only [displacementVector_norm_sq] using hz
    have hv : displacementVector m W = 0 := by
      apply norm_eq_zero.mp
      nlinarith [norm_nonneg (displacementVector m W)]
    exact hv.symm

/-- A rescaled actual `J` transport has strict forward decay. Its
inverse has the reciprocal amplification, so this normalization alone
cannot control the original displacement. -/
def windowJHalfTransport (W : Finset NontrivialZero) (hW : JReflectedWindow W)
    (v : EuclideanSpace ℝ {ρ // ρ ∈ W}) :
    EuclideanSpace ℝ {ρ // ρ ∈ W} :=
  (1 / 2 : ℝ) • windowJTransport W hW v

def windowJDoubleReturn (W : Finset NontrivialZero) (hW : JReflectedWindow W)
    (v : EuclideanSpace ℝ {ρ // ρ ∈ W}) :
    EuclideanSpace ℝ {ρ // ρ ∈ W} :=
  (2 : ℝ) • windowJTransport W hW v

theorem windowJDoubleReturn_half_displacement
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    windowJDoubleReturn W hW
      (windowJHalfTransport W hW (displacementVector m W)) =
        displacementVector m W := by
  rw [windowJHalfTransport, windowJTransport_displacement_neg m hm W hW,
    windowJDoubleReturn, map_smul, map_neg,
    windowJTransport_displacement_neg m hm W hW]
  module

theorem windowJHalfTransport_hilbertXi_quarter
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    ‖hilbertKernelXi (invariantProbe W)
      (windowJHalfTransport W hW (displacementVector m W))‖ ^ 2 =
      (1 / 4 : ℝ) *
        ‖hilbertKernelXi (invariantProbe W) (displacementVector m W)‖ ^ 2 := by
  rw [windowJHalfTransport, windowJTransport_displacement_neg m hm W hW,
    map_smul, map_neg, norm_smul, norm_neg]
  norm_num
  ring

theorem windowJDoubleReturn_hilbertXi_gain_four
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    ‖hilbertKernelXi (invariantProbe W)
      (windowJDoubleReturn W hW
        (windowJHalfTransport W hW (displacementVector m W)))‖ ^ 2 =
      (4 : ℝ) * ‖hilbertKernelXi (invariantProbe W)
        (windowJHalfTransport W hW (displacementVector m W))‖ ^ 2 := by
  rw [windowJDoubleReturn_half_displacement m hm W hW,
    windowJHalfTransport_hilbertXi_quarter m hm W hW]
  ring

/-- On the actual displacement, involution transport preserves the
Hilbert XI residual norm, not just the full-state norm. -/
theorem windowJTransport_hilbertXi_norm
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    ‖hilbertKernelXi (invariantProbe W)
      (windowJTransport W hW (displacementVector m W))‖ ^ 2 =
      ‖hilbertKernelXi (invariantProbe W) (displacementVector m W)‖ ^ 2 := by
  rw [windowJTransport_displacement_neg m hm W hW, map_neg, norm_neg]

theorem windowJTransport_hilbertXi_eq_windowEnergy
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    ‖hilbertKernelXi (invariantProbe W)
      (windowJTransport W hW (displacementVector m W))‖ ^ 2 =
      windowEnergy m W := by
  rw [windowJTransport_hilbertXi_norm m hm W hW]
  have hvker : displacementVector m W ∈ (invariantProbe W).ker :=
    invariantProbe_displacement_zero_J m hm W hW
  change ‖(invariantProbe W).ker.starProjection (displacementVector m W)‖ ^ 2 = _
  rw [Submodule.starProjection_eq_self_iff.mpr hvker]
  exact displacementVector_norm_sq m W

/-- Strict decay of the actual involution transport on a window is
equivalent to vanishing of that window's positive displacement energy.
The involution supplies no contraction on a nonzero displacement. -/
theorem windowJTransport_subunit_iff_zero
    (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W)
    (q : ℝ) (hq : q < 1) :
    ‖windowJTransport W hW (displacementVector m W)‖ ^ 2 ≤
      q * ‖displacementVector m W‖ ^ 2 ↔
        windowEnergy m W = 0 := by
  rw [windowJTransport_displacement_norm, displacementVector_norm_sq]
  have he : 0 ≤ windowEnergy m W := by
    rw [← displacementVector_norm_sq]
    positivity
  constructor
  · intro h
    nlinarith
  · intro h
    simp [h]

def CanonicalJTransportFraction (q : ℝ) : Prop :=
  ∀ n : ℕ,
    ‖windowJTransport (canonicalJReflectedWindow n)
      (canonicalJReflectedWindow_reflected n)
      (displacementVector unitWeights (canonicalJReflectedWindow n))‖ ^ 2 ≤
      q * ‖displacementVector unitWeights (canonicalJReflectedWindow n)‖ ^ 2

/-- A subunit fraction for the actual `J` transport is exactly the RH
target. Thus functional-equation transport alone cannot be treated as
the missing strict source law. -/
theorem canonicalJTransportFraction_iff_criticalStripRH
    (q : ℝ) (hq : q < 1) :
    CanonicalJTransportFraction q ↔ CriticalStripRH := by
  constructor
  · intro hc
    apply criticalStripRH_of_exhaustive_vanishing_budget
      unitWeights unitWeights_positive canonicalJReflectedWindow
      canonicalJReflectedWindow_eventuallyCovered
      (fun _ => (0 : ℝ)) tendsto_const_nhds
    intro n
    have hz := (windowJTransport_subunit_iff_zero unitWeights
      (canonicalJReflectedWindow n) (canonicalJReflectedWindow_reflected n)
      q hq).mp (hc n)
    exact le_of_eq hz
  · intro hRH n
    have hz : windowEnergy unitWeights (canonicalJReflectedWindow n) = 0 := by
      apply (windowEnergy_eq_zero_iff_J_fixed unitWeights unitWeights_positive _).mpr
      intro ρ _
      apply (J_zero_fixed_iff ρ).mpr
      exact hRH ρ.val
        ((completed_zero_iff_zeta_zero_of_re_pos ρ.val ρ.property.2.1).mp
          ρ.property.1)
        ρ.property.2.1 ρ.property.2.2
    exact (windowJTransport_subunit_iff_zero unitWeights
      (canonicalJReflectedWindow n) (canonicalJReflectedWindow_reflected n)
      q hq).mpr hz

def CanonicalJAverageReturn : Prop :=
  ∀ n : ℕ,
    windowJAverage (canonicalJReflectedWindow n)
      (canonicalJReflectedWindow_reflected n)
      (displacementVector unitWeights (canonicalJReflectedWindow n)) =
        displacementVector unitWeights (canonicalJReflectedWindow n)

/-- Averaging does annihilate the canonical anti-invariant XI state,
but faithful return on every exhaustive window is exactly RH. -/
theorem canonicalJAverageReturn_iff_criticalStripRH :
    CanonicalJAverageReturn ↔ CriticalStripRH := by
  constructor
  · intro hret
    apply (canonicalJTransportFraction_iff_criticalStripRH 0 (by norm_num)).mp
    intro n
    have hz := (windowJAverage_return_iff_zero_energy unitWeights
      (fun _ => rfl) (canonicalJReflectedWindow n)
      (canonicalJReflectedWindow_reflected n)).mp (hret n)
    exact (windowJTransport_subunit_iff_zero unitWeights
      (canonicalJReflectedWindow n) (canonicalJReflectedWindow_reflected n)
      0 (by norm_num)).mpr hz
  · intro hRH n
    have hc := (canonicalJTransportFraction_iff_criticalStripRH 0
      (by norm_num)).mpr hRH n
    have hz := (windowJTransport_subunit_iff_zero unitWeights
      (canonicalJReflectedWindow n) (canonicalJReflectedWindow_reflected n)
      0 (by norm_num)).mp hc
    exact (windowJAverage_return_iff_zero_energy unitWeights
      (fun _ => rfl) (canonicalJReflectedWindow n)
      (canonicalJReflectedWindow_reflected n)).mpr hz

end SixBirdsDualityConfinement.RH.JTransportNoGo
