import SixBirdsDualityConfinement.EvenSourceParity
import SixBirdsDualityConfinement.RH.GappedSourceWorkTrial
import SixBirdsDualityConfinement.RH.ArithmeticJensenWindows

/-!
The restorative source on the actual Jensen divisor windows is J-odd.
Requiring it to have the even equivariant parity characteristic of an
even nonlinearity forces the RH displacement to vanish. This tests a
possible common source-provenance class. It does not assert that the
Navier Duhamel operator satisfies the corresponding physical symmetry.
-/

noncomputable section
open Filter
open scoped NNReal Topology
namespace SixBirdsDualityConfinement.RH.EvenSourceParityNoGo

open ClassicalZeroLedger FiniteZeroWindows ActualInvolution JTransportNoGo
open ArithmeticJensenWindows GappedSourceWorkTrial
open SixBirdsDualityConfinement.EvenSourceParity

theorem gappedWindowSource_J_even_iff_displacement_zero
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    let S := gappedWindowSourceStep m W 1
    (windowJTransport W hW) S.source = S.source ↔
      displacementVector m W = 0 := by
  dsimp only
  constructor
  · intro heven
    let S := gappedWindowSourceStep m W 1
    let J := (windowJTransport W hW).toLinearIsometry.toContinuousLinearMap
    have hodd : J S.before = -S.before := by
      change windowJTransport W hW (displacementVector m W) =
        -displacementVector m W
      exact windowJTransport_displacement_neg m hm W hW
    have hcomm : ∀ v, J (S.transport v) = S.transport (J v) := by
      intro v
      exact (gappedOrdinateHeatTransport_commutes_J W hW 1 v).symm
    have heven' : J S.source = S.source := heven
    have hstrict : ∀ v, v ≠ 0 → ‖S.transport v‖ < ‖v‖ := by
      intro v hv
      exact gappedOrdinateHeatTransport_norm_lt W 1 (by norm_num) v hv
    have hz := fixed_odd_even_source_zero_of_strict_transport
      S J rfl hodd hcomm heven' hstrict
    exact hz
  · intro hd
    simp [gappedWindowSourceStep, hd]

def CanonicalJensenEvenSource : Prop :=
  ∀ n : ℕ,
    let W := canonicalJensenWindow n
    (windowJTransport W (canonicalJensenWindow_reflected n))
      (gappedWindowSourceStep unitWeights W 1).source =
        (gappedWindowSourceStep unitWeights W 1).source

/-- Even-source provenance on every actual heat-built Jensen window is
already equivalent to RH. It cannot be verified as a separate easy
membership fact for the RH instance of a shared quadratic-source class. -/
theorem canonicalJensenEvenSource_iff_criticalStripRH :
    CanonicalJensenEvenSource ↔ CriticalStripRH := by
  constructor
  · intro heven
    apply criticalStripRH_of_exhaustive_vanishing_budget
      unitWeights unitWeights_positive canonicalJensenWindow
      canonicalJensenWindow_eventuallyCovered (fun _ => 0)
      tendsto_const_nhds
    intro n
    have hd := (gappedWindowSource_J_even_iff_displacement_zero
      unitWeights (fun _ => rfl) (canonicalJensenWindow n)
      (canonicalJensenWindow_reflected n)).mp (heven n)
    rw [← displacementVector_norm_sq unitWeights
      (canonicalJensenWindow n), hd]
    norm_num
  · intro hRH n
    have hz : windowEnergy unitWeights (canonicalJensenWindow n) = 0 := by
      apply (windowEnergy_eq_zero_iff unitWeights unitWeights_positive _).mpr
      intro ρ _
      exact sub_eq_zero.mpr (hRH ρ.val
        ((completed_zero_iff_zeta_zero_of_re_pos ρ.val ρ.property.2.1).mp
          ρ.property.1)
        ρ.property.2.1 ρ.property.2.2)
    have hv : ‖displacementVector unitWeights
        (canonicalJensenWindow n)‖ ^ 2 = 0 := by
      rwa [displacementVector_norm_sq]
    have hd : displacementVector unitWeights
        (canonicalJensenWindow n) = 0 := by
      apply norm_eq_zero.mp
      nlinarith [norm_nonneg (displacementVector unitWeights
        (canonicalJensenWindow n))]
    exact (gappedWindowSource_J_even_iff_displacement_zero
      unitWeights (fun _ => rfl) (canonicalJensenWindow n)
      (canonicalJensenWindow_reflected n)).mpr hd

#print axioms gappedWindowSource_J_even_iff_displacement_zero
#print axioms canonicalJensenEvenSource_iff_criticalStripRH

end SixBirdsDualityConfinement.RH.EvenSourceParityNoGo
