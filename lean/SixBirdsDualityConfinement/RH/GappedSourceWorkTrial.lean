import SixBirdsDualityConfinement.SourceWorkTrial
import SixBirdsDualityConfinement.RH.JEquivariantSourceAudit

/-!
A trial strict Gaussian heat source-work closure on the actual RH zero-window
carrier. The scalar factor `exp(-t)` gives every spectral coordinate a positive
gap, including height zero. The return source is synthetic: it is defined
as the exact heat deficit, not derived from primes or theta data.
-/

noncomputable section
open scoped NNReal InnerProduct InnerProductSpace
namespace SixBirdsDualityConfinement.RH.GappedSourceWorkTrial

open ClassicalZeroLedger FiniteZeroWindows ActualInvolution JTransportNoGo
open JEquivariantSourceAudit OrdinateHeatReturn SixBirdsNeedles.XiCore
open SixBirdsDualityConfinement.SourceWorkTrial

def gappedOrdinateHeatTransport (W : Finset NontrivialZero) (t : ℝ≥0) :
    EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ]
      EuclideanSpace ℝ {ρ // ρ ∈ W} :=
  Real.exp (-(t : ℝ)) • ordinateHeatTransport W t

theorem gappedOrdinateHeatTransport_norm_lt
    (W : Finset NontrivialZero) (t : ℝ≥0) (ht : 0 < t)
    (v : EuclideanSpace ℝ {ρ // ρ ∈ W}) (hv : v ≠ 0) :
    ‖gappedOrdinateHeatTransport W t v‖ < ‖v‖ := by
  rw [gappedOrdinateHeatTransport, ContinuousLinearMap.smul_apply,
    norm_smul, Real.norm_of_nonneg (Real.exp_pos _).le]
  have hfactor : Real.exp (-(t : ℝ)) < 1 := by
    apply Real.exp_lt_one_iff.mpr
    have ht' : 0 < (t : ℝ) := ht
    linarith
  have hpos : 0 < Real.exp (-(t : ℝ)) := Real.exp_pos _
  have hnorm : 0 < ‖v‖ := norm_pos_iff.mpr hv
  have hbase := ordinateHeatTransport_norm_le W t v
  nlinarith [mul_le_mul_of_nonneg_left hbase hpos.le]

theorem gappedOrdinateHeatTransport_commutes_J
    (W : Finset NontrivialZero) (hW : JReflectedWindow W)
    (t : ℝ≥0) (v : EuclideanSpace ℝ {ρ // ρ ∈ W}) :
    gappedOrdinateHeatTransport W t (windowJTransport W hW v) =
      windowJTransport W hW (gappedOrdinateHeatTransport W t v) := by
  simp only [gappedOrdinateHeatTransport, ContinuousLinearMap.smul_apply,
    map_smul]
  rw [ordinateHeatTransport_commutes_J W hW t v]

def gappedWindowSourceStep (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) (t : ℝ≥0) :
    XiSourceStep (EuclideanSpace ℝ {ρ // ρ ∈ W}) ℝ where
  native := invariantProbe W
  transport := gappedOrdinateHeatTransport W t
  before := displacementVector m W
  after := displacementVector m W
  source := displacementVector m W -
    gappedOrdinateHeatTransport W t (displacementVector m W)
  balance := by abel

/-- Applying the trial source-work law to a fixed RH window forces its
actual displacement to vanish. The only supplied premise is the same
abstract work inequality used in the Navier trial. -/
theorem gapped_work_closure_forces_zero
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W)
    (t : ℝ≥0) (ht : 0 < t)
    (θ C : ℝ) (hθ : θ < 1)
    (hwork : StrongSourceWork θ C (gappedWindowSourceStep m W t)) :
    displacementVector m W = 0 := by
  let d := displacementVector m W
  let H := gappedOrdinateHeatTransport W t
  let S := gappedWindowSourceStep m W t
  have hchannels := commuting_window_step_native_channels_zero m hm W hW H
    (gappedOrdinateHeatTransport_commutes_J W hW t) (d - H d) (by abel)
  have hnative : hilbertNativeCurrency S.native S.after = 0 := by
    change hilbertNativeCurrency (invariantProbe W) d = 0
    exact (invariantProbe W).ker.starProjection_orthogonal_apply_eq_zero hchannels.1
  have hxi_d : hilbertKernelXi S.native S.before = d := by
    change (invariantProbe W).ker.starProjection d = d
    exact (invariantProbe W).ker.starProjection_eq_self_iff.mpr hchannels.1
  have hxi_Hd : hilbertKernelXi S.native (S.transport S.before) = H d := by
    change (invariantProbe W).ker.starProjection (H d) = H d
    exact (invariantProbe W).ker.starProjection_eq_self_iff.mpr hchannels.2.1
  have hheat : 0 ≤ dissipationGap S := by
    rw [dissipationGap, hxi_d, hxi_Hd]
    by_cases hd : d = 0
    · simp [hd]
    · have hstrict := gappedOrdinateHeatTransport_norm_lt W t ht d hd
      nlinarith [norm_nonneg (H d), norm_nonneg d]
  have hgap := fixed_native_zero_forces_zero_gap S θ C hθ rfl hnative hheat hwork
  rw [dissipationGap, hxi_d, hxi_Hd] at hgap
  by_contra hd
  have hstrict := gappedOrdinateHeatTransport_norm_lt W t ht d hd
  nlinarith [norm_nonneg (H d), norm_nonneg d]

def RHSourceWorkClosure (θ C : ℝ) : Prop :=
  ∀ n : ℕ,
    StrongSourceWork θ C
      (gappedWindowSourceStep unitWeights
        (canonicalJReflectedWindow n) 1)

/-- The common trial inequality reaches the classical zeta-zero statement
on exhaustive actual windows. This is only a conditional application: the
work inequality has not been derived from arithmetic source data. -/
theorem criticalStripRH_of_gapped_source_work
    (θ C : ℝ) (hθ : θ < 1)
    (hwork : RHSourceWorkClosure θ C) : CriticalStripRH := by
  apply (canonicalJFixedFraction_iff_criticalStripRH 0
    (by norm_num) (by norm_num)).mp
  intro n
  have hd := gapped_work_closure_forces_zero unitWeights (fun _ => rfl)
    (canonicalJReflectedWindow n) (canonicalJReflectedWindow_reflected n)
    1 (by norm_num) θ C hθ (hwork n)
  simp [hd]

/-- The trial RH source-work premise has exactly RH's strength: once RH
holds, every canonical displacement vanishes and the work law is trivial.
Thus this synthetic fixed-point family does not supply an independent
arithmetic payment for the shared closure campaign. -/
theorem gapped_source_work_iff_criticalStripRH
    (θ C : ℝ) (hθ : θ < 1) :
    RHSourceWorkClosure θ C ↔ CriticalStripRH := by
  constructor
  · exact criticalStripRH_of_gapped_source_work θ C hθ
  · intro hRH n
    have hz : windowEnergy unitWeights (canonicalJReflectedWindow n) = 0 := by
      apply (windowEnergy_eq_zero_iff unitWeights unitWeights_positive _).mpr
      intro ρ _
      exact sub_eq_zero.mpr (hRH ρ.val
        ((completed_zero_iff_zeta_zero_of_re_pos ρ.val ρ.property.2.1).mp
          ρ.property.1)
        ρ.property.2.1 ρ.property.2.2)
    have hv : ‖displacementVector unitWeights
        (canonicalJReflectedWindow n)‖ ^ 2 = 0 := by
      rwa [displacementVector_norm_sq]
    have hd : displacementVector unitWeights
        (canonicalJReflectedWindow n) = 0 := by
      apply norm_eq_zero.mp
      nlinarith [norm_nonneg (displacementVector unitWeights
        (canonicalJReflectedWindow n))]
    simp [StrongSourceWork, sourceWork, dissipationGap,
      gappedWindowSourceStep, hd]

#print axioms gapped_source_work_iff_criticalStripRH

end SixBirdsDualityConfinement.RH.GappedSourceWorkTrial
