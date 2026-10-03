import SixBirdsDualityConfinement.RH.OrdinateHeatReturn

/-!
On an actual J-reflected zero window, changing the transport to any
J-commuting linear map cannot create native currency for the displacement
or its exact fixed-point return source. This rules out a native-only tariff
for that whole class of RH operations. It does not rule out a source law
using an independently proved zero-sensitive quantity.
-/

noncomputable section
open scoped NNReal InnerProduct InnerProductSpace
namespace SixBirdsDualityConfinement.RH.EquivariantNativeTariffNoGo

open ClassicalZeroLedger FiniteZeroWindows ActualInvolution JTransportNoGo
open JEquivariantSourceAudit SixBirdsNeedles.XiCore
open OrdinateHeatReturn

theorem commuting_window_native_tariff_iff_zero
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W)
    (T : EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ]
      EuclideanSpace ℝ {ρ // ρ ∈ W})
    (hcomm : ∀ v, T (windowJTransport W hW v) =
      windowJTransport W hW (T v))
    (C : ℝ) :
    (‖hilbertKernelXi (invariantProbe W) (displacementVector m W)‖ ^ 2 ≤
      C * (‖hilbertNativeCurrency (invariantProbe W)
          (displacementVector m W)‖ ^ 2 +
        ‖hilbertNativeCurrency (invariantProbe W)
          (displacementVector m W - T (displacementVector m W))‖ ^ 2)) ↔
      windowEnergy m W = 0 := by
  let d := displacementVector m W
  have hbalance : d = T d + (d - T d) := by abel
  have hnative := commuting_window_step_native_currency_zero m hm W hW T hcomm
    (d - T d) hbalance
  have hker : d ∈ (invariantProbe W).ker :=
    invariantProbe_displacement_zero_J m hm W hW
  have hxi : ‖hilbertKernelXi (invariantProbe W) d‖ ^ 2 =
      windowEnergy m W := by
    change ‖(invariantProbe W).ker.starProjection d‖ ^ 2 = _
    rw [Submodule.starProjection_eq_self_iff.mpr hker]
    exact displacementVector_norm_sq m W
  rw [show displacementVector m W = d from rfl]
  rw [hnative.1, hnative.2.2, hxi]
  norm_num
  constructor
  · intro h
    have hnonneg : 0 ≤ windowEnergy m W := by
      rw [← displacementVector_norm_sq]
      positivity
    nlinarith
  · intro h
    simp [h]

/-- A uniform native-only tariff for the actual exhaustive zero windows,
with an arbitrary chosen transport on each window. -/
def CanonicalCommutingNativeTariff (C : ℝ)
    (T : ∀ n : ℕ,
      EuclideanSpace ℝ {ρ // ρ ∈ canonicalJReflectedWindow n} →L[ℝ]
        EuclideanSpace ℝ {ρ // ρ ∈ canonicalJReflectedWindow n}) : Prop :=
  ∀ n : ℕ,
    let W := canonicalJReflectedWindow n
    let d := displacementVector unitWeights W
    ‖hilbertKernelXi (invariantProbe W) d‖ ^ 2 ≤
      C * (‖hilbertNativeCurrency (invariantProbe W) d‖ ^ 2 +
        ‖hilbertNativeCurrency (invariantProbe W) (d - T n d)‖ ^ 2)

/-- No family of J-commuting transports can make native currency pay the
fixed-point source on the actual RH windows. For every scalar tariff, the
resulting budget has exactly the strength of classical critical-strip RH. -/
theorem canonical_commuting_native_tariff_iff_criticalStripRH
    (C : ℝ)
    (T : ∀ n : ℕ,
      EuclideanSpace ℝ {ρ // ρ ∈ canonicalJReflectedWindow n} →L[ℝ]
        EuclideanSpace ℝ {ρ // ρ ∈ canonicalJReflectedWindow n})
    (hcomm : ∀ n v, T n
      (windowJTransport (canonicalJReflectedWindow n)
        (canonicalJReflectedWindow_reflected n) v) =
      windowJTransport (canonicalJReflectedWindow n)
        (canonicalJReflectedWindow_reflected n) (T n v)) :
    CanonicalCommutingNativeTariff C T ↔ CriticalStripRH := by
  have hxi (n : ℕ) :
      ‖hilbertKernelXi (invariantProbe (canonicalJReflectedWindow n))
        (displacementVector unitWeights (canonicalJReflectedWindow n))‖ ^ 2 =
        windowEnergy unitWeights (canonicalJReflectedWindow n) := by
    rw [← windowJTransport_hilbertXi_eq_windowEnergy unitWeights
      (fun _ => rfl) (canonicalJReflectedWindow n)
      (canonicalJReflectedWindow_reflected n)]
    exact (windowJTransport_hilbertXi_norm unitWeights
      (fun _ => rfl) (canonicalJReflectedWindow n)
      (canonicalJReflectedWindow_reflected n)).symm
  have hlocal (n : ℕ) := commuting_window_native_tariff_iff_zero
    unitWeights (fun _ => rfl) (canonicalJReflectedWindow n)
    (canonicalJReflectedWindow_reflected n) (T n) (hcomm n) C
  constructor
  · intro h
    apply (canonicalJFixedFraction_iff_criticalStripRH 0
      (by norm_num) (by norm_num)).mp
    intro n
    have hz := (hlocal n).mp (h n)
    rw [hxi n, hz]
    simp
  · intro hRH n
    have hb := ((canonicalJFixedFraction_iff_criticalStripRH 0
      (by norm_num) (by norm_num)).mpr hRH) n
    rw [hxi n, zero_mul] at hb
    have hn : 0 ≤ windowEnergy unitWeights (canonicalJReflectedWindow n) := by
      rw [← displacementVector_norm_sq]
      positivity
    have hz : windowEnergy unitWeights (canonicalJReflectedWindow n) = 0 :=
      le_antisymm hb hn
    exact (hlocal n).mpr hz

/-- The actual Gaussian ordinate-heat family is inside the preceding
no-go class for any choice of positive or zero heat times. -/
theorem canonical_ordinate_heat_native_tariff_iff_criticalStripRH
    (C : ℝ) (t : ℕ → ℝ≥0) :
    CanonicalCommutingNativeTariff C
      (fun n => ordinateHeatTransport (canonicalJReflectedWindow n) (t n)) ↔
        CriticalStripRH := by
  apply canonical_commuting_native_tariff_iff_criticalStripRH C
    (fun n => ordinateHeatTransport (canonicalJReflectedWindow n) (t n))
  intro n v
  exact ordinateHeatTransport_commutes_J (canonicalJReflectedWindow n)
    (canonicalJReflectedWindow_reflected n) (t n) v

end SixBirdsDualityConfinement.RH.EquivariantNativeTariffNoGo
