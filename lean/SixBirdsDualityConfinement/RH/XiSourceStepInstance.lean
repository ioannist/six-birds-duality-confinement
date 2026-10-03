import SixBirdsDualityConfinement.RH.JTransportNoGo
import SixBirdsNeedles.XiCore.SourceStep

/-! The actual zero-window displacement as a source-free XI step under
the signed completed-zeta involution. This supplies an exact source
identity, not a strict residual gain. -/

noncomputable section
namespace SixBirdsDualityConfinement.RH.XiSourceStepInstance

open ClassicalZeroLedger FiniteZeroWindows ActualInvolution JTransportNoGo
open SixBirdsNeedles.XiCore

def windowXiSourceStep
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    XiSourceStep (EuclideanSpace ℝ {ρ // ρ ∈ W}) ℝ where
  native := invariantProbe W
  transport := -((windowJTransport W hW).toLinearIsometry.toContinuousLinearMap)
  before := displacementVector m W
  after := displacementVector m W
  source := 0
  balance := by
    change displacementVector m W =
      -windowJTransport W hW (displacementVector m W) + 0
    rw [windowJTransport_displacement_neg m hm W hW]
    simp

/-- The common XI return specializes to an exact source-free fixed point.
The signed J transport has unit residual gain on this actual state. -/
theorem windowXiSourceStep_xi_return
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    hilbertKernelXi (invariantProbe W) (displacementVector m W) =
      hilbertKernelXi (invariantProbe W)
        (-windowJTransport W hW (displacementVector m W)) := by
  have h := (windowXiSourceStep m hm W hW).xi_return_source_zero (by rfl)
  simpa [windowXiSourceStep] using h

/-- The actual signed-J source step has unit XI gain on the displacement.
Any assumed strict gain on these states therefore forces zero residual. -/
theorem windowXiSourceStep_unit_gain
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    let S := windowXiSourceStep m hm W hW
    ‖hilbertKernelXi S.native (S.transport S.before)‖ ^ 2 =
      ‖hilbertKernelXi S.native S.before‖ ^ 2 := by
  dsimp [windowXiSourceStep]
  rw [windowJTransport_displacement_neg m hm W hW]
  simp

/-- Any attempted strict transport bound on an actual reflected zero
window must be paid by its projected source. Here that source is exactly
zero, so the generic compensation inequality has zero on the right. -/
theorem windowXiSourceStep_source_compensation
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W)
    (a : ℝ)
    (htransport :
      ‖hilbertKernelXi (invariantProbe W)
        (-windowJTransport W hW (displacementVector m W))‖ ≤
        a * ‖hilbertKernelXi (invariantProbe W)
          (displacementVector m W)‖) :
    (1 - a) * ‖hilbertKernelXi (invariantProbe W)
      (displacementVector m W)‖ ≤ 0 := by
  have h := (windowXiSourceStep m hm W hW).xi_source_lower_bound_of_fixed_point
    rfl a (by simpa [windowXiSourceStep] using htransport)
  simpa [windowXiSourceStep] using h

theorem windowXiSourceStep_strict_gain_forces_zero
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W)
    (a : ℝ) (ha : a < 1)
    (htransport :
      ‖hilbertKernelXi (invariantProbe W)
        (-windowJTransport W hW (displacementVector m W))‖ ≤
        a * ‖hilbertKernelXi (invariantProbe W)
          (displacementVector m W)‖) :
    displacementVector m W = 0 := by
  have hres :=
    (windowXiSourceStep m hm W hW).xi_fixed_point_zero_of_strict_transport_source_zero
      rfl rfl a ha (by simpa [windowXiSourceStep] using htransport)
  have hker : displacementVector m W ∈ (invariantProbe W).ker :=
    invariantProbe_displacement_zero_J m hm W hW
  have hxi : hilbertKernelXi (invariantProbe W) (displacementVector m W) =
      displacementVector m W :=
    (invariantProbe W).ker.starProjection_eq_self_iff.mpr hker
  simpa only [windowXiSourceStep, hxi] using hres

/-- A proposed payment from only the proved native currency and the actual
source of the canonical signed-J step. The coefficient can be arbitrary:
both channels vanish on these genuine zero-window displacements. -/
def CanonicalJNativeSourceBudget (C : ℝ) : Prop :=
  ∀ n : ℕ,
    let S := windowXiSourceStep unitWeights (fun _ => rfl)
      (canonicalJReflectedWindow n) (canonicalJReflectedWindow_reflected n)
    ‖hilbertKernelXi S.native S.before‖ ^ 2 ≤
      C * (‖hilbertNativeCurrency S.native S.before‖ ^ 2 +
        ‖hilbertKernelXi S.native S.source‖ ^ 2)

/-- Native plus actual source payment supplies no independent RH closure:
on the canonical windows this budget holds exactly when classical
critical-strip RH holds. Any viable common law needs a further proved
channel that sees the J-odd displacement. -/
theorem canonicalJNativeSourceBudget_iff_criticalStripRH (C : ℝ) :
    CanonicalJNativeSourceBudget C ↔ CriticalStripRH := by
  have hnative (n : ℕ) :
      hilbertNativeCurrency (invariantProbe (canonicalJReflectedWindow n))
        (displacementVector unitWeights (canonicalJReflectedWindow n)) = 0 := by
    have hker := invariantProbe_displacement_zero_J unitWeights (fun _ => rfl)
      (canonicalJReflectedWindow n) (canonicalJReflectedWindow_reflected n)
    exact (invariantProbe (canonicalJReflectedWindow n)).ker.starProjection_orthogonal_apply_eq_zero hker
  constructor
  · intro h
    apply criticalStripRH_of_canonical_J_subunitKernelXiClosure
    refine ⟨0, le_refl _, by norm_num, ?_⟩
    intro n _
    have hb := h n
    change ‖hilbertKernelXi (invariantProbe (canonicalJReflectedWindow n))
      (displacementVector unitWeights (canonicalJReflectedWindow n))‖ ^ 2 ≤
      C * (‖hilbertNativeCurrency (invariantProbe (canonicalJReflectedWindow n))
        (displacementVector unitWeights (canonicalJReflectedWindow n))‖ ^ 2 +
        ‖hilbertKernelXi (invariantProbe (canonicalJReflectedWindow n)) (0 :
          EuclideanSpace ℝ {ρ // ρ ∈ canonicalJReflectedWindow n})‖ ^ 2) at hb
    simpa [hnative n] using hb
  · intro hRH n
    have hgap := (canonicalJFixedFraction_iff_criticalStripRH 0 (le_refl _) (by norm_num)).mpr hRH n
    change ‖hilbertKernelXi (invariantProbe (canonicalJReflectedWindow n))
      (displacementVector unitWeights (canonicalJReflectedWindow n))‖ ^ 2 ≤
      C * (‖hilbertNativeCurrency (invariantProbe (canonicalJReflectedWindow n))
        (displacementVector unitWeights (canonicalJReflectedWindow n))‖ ^ 2 +
        ‖hilbertKernelXi (invariantProbe (canonicalJReflectedWindow n)) (0 :
          EuclideanSpace ℝ {ρ // ρ ∈ canonicalJReflectedWindow n})‖ ^ 2)
    simpa [hnative n] using hgap

#print axioms windowXiSourceStep_xi_return
#print axioms windowXiSourceStep_unit_gain
#print axioms windowXiSourceStep_source_compensation
#print axioms windowXiSourceStep_strict_gain_forces_zero
#print axioms canonicalJNativeSourceBudget_iff_criticalStripRH

end SixBirdsDualityConfinement.RH.XiSourceStepInstance
