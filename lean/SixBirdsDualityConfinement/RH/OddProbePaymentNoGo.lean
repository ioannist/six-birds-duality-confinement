import SixBirdsDualityConfinement.RH.JTransportNoGo

/-!
The canonical J-odd repair of the invariant zero-window probe detects the
actual displacement, but moves its complete XI energy into native
currency. Its native payment on exhaustive windows is exactly RH.
-/

noncomputable section
open Filter
open scoped Topology
open scoped InnerProduct InnerProductSpace
namespace SixBirdsDualityConfinement.RH.OddProbePaymentNoGo

open ClassicalZeroLedger FiniteZeroWindows ActualInvolution JTransportNoGo
open SixBirdsNeedles.XiCore

def oddProbe (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ] EuclideanSpace ℝ {ρ // ρ ∈ W} :=
  ContinuousLinearMap.id ℝ _ -
    (windowJTransport W hW).toLinearIsometry.toContinuousLinearMap

theorem oddProbe_displacement
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    oddProbe W hW (displacementVector m W) =
      (2 : ℝ) • displacementVector m W := by
  simp [oddProbe, windowJTransport_displacement_neg m hm W hW]
  module

theorem displacement_orthogonal_oddProbe_kernel
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    displacementVector m W ∈ (oddProbe W hW).kerᗮ := by
  intro w hw
  have hwJ : windowJTransport W hW w = w := by
    change oddProbe W hW w = 0 at hw
    simp only [oddProbe, ContinuousLinearMap.sub_apply,
      ContinuousLinearMap.id_apply] at hw
    change w - windowJTransport W hW w = 0 at hw
    exact (sub_eq_zero.mp hw).symm
  have hinner := (windowJTransport W hW).inner_map_map w (displacementVector m W)
  rw [hwJ, windowJTransport_displacement_neg m hm W hW, inner_neg_right] at hinner
  linarith

theorem oddProbe_kernelXi_displacement_zero
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    hilbertKernelXi (oddProbe W hW) (displacementVector m W) = 0 := by
  exact (oddProbe W hW).ker.starProjection_apply_eq_zero_iff.mpr
    (displacement_orthogonal_oddProbe_kernel m hm W hW)

theorem oddProbe_native_displacement
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    hilbertNativeCurrency (oddProbe W hW) (displacementVector m W) =
      displacementVector m W := by
  exact ((oddProbe W hW).kerᗮ).starProjection_eq_self_iff.mpr
    (displacement_orthogonal_oddProbe_kernel m hm W hW)

theorem oddProbe_native_cost_eq_windowEnergy
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    ‖hilbertNativeCurrency (oddProbe W hW) (displacementVector m W)‖ ^ 2 =
      windowEnergy m W := by
  rw [oddProbe_native_displacement m hm W hW]
  exact displacementVector_norm_sq m W

/-- The shared subunit-XI closure predicate becomes unconditional if
the RH native probe is enlarged to see the entire J-odd displacement.
The strong theorem still needs the independent native budget below. -/
theorem canonicalOddSubunitKernelXiFamily :
    SubunitKernelXiFamily (fun _ : ℕ => True)
      (fun n => oddProbe (canonicalJReflectedWindow n)
        (canonicalJReflectedWindow_reflected n))
      (fun n => displacementVector unitWeights (canonicalJReflectedWindow n)) := by
  refine ⟨0, le_rfl, by norm_num, ?_⟩
  intro n _
  rw [oddProbe_kernelXi_displacement_zero unitWeights
    (fun _ => rfl) (canonicalJReflectedWindow n)
    (canonicalJReflectedWindow_reflected n)]
  simp

def CanonicalOddNativeZero : Prop :=
  ∀ n : ℕ,
    ‖hilbertNativeCurrency
      (oddProbe (canonicalJReflectedWindow n)
        (canonicalJReflectedWindow_reflected n))
      (displacementVector unitWeights (canonicalJReflectedWindow n))‖ ^ 2 = 0

/-- The J-odd probe removes the XI blind spot, but paying its
native charge by zero on every exhaustive window is exactly RH. -/
theorem canonicalOddNativeZero_iff_criticalStripRH :
    CanonicalOddNativeZero ↔ CriticalStripRH := by
  constructor
  · intro h
    apply (canonicalJTransportFraction_iff_criticalStripRH 0 (by norm_num)).mp
    intro n
    have hz : windowEnergy unitWeights (canonicalJReflectedWindow n) = 0 := by
      rw [← oddProbe_native_cost_eq_windowEnergy unitWeights
        (fun _ => rfl) (canonicalJReflectedWindow n)
        (canonicalJReflectedWindow_reflected n)]
      exact h n
    exact (windowJTransport_subunit_iff_zero unitWeights
      (canonicalJReflectedWindow n) (canonicalJReflectedWindow_reflected n)
      0 (by norm_num)).mpr hz
  · intro hRH n
    have hc := (canonicalJTransportFraction_iff_criticalStripRH 0
      (by norm_num)).mpr hRH n
    have hz := (windowJTransport_subunit_iff_zero unitWeights
      (canonicalJReflectedWindow n) (canonicalJReflectedWindow_reflected n)
      0 (by norm_num)).mp hc
    rw [oddProbe_native_cost_eq_windowEnergy unitWeights
      (fun _ => rfl) (canonicalJReflectedWindow n)
      (canonicalJReflectedWindow_reflected n)]
    exact hz

def CanonicalOddNativeVanishingBudget : Prop :=
  ∃ b : ℕ → ℝ, Tendsto b atTop (𝓝 0) ∧
    ∀ n : ℕ,
      ‖hilbertNativeCurrency
        (oddProbe (canonicalJReflectedWindow n)
          (canonicalJReflectedWindow_reflected n))
        (displacementVector unitWeights (canonicalJReflectedWindow n))‖ ^ 2 ≤ b n

/-- Even permitting a source-supplied native budget tending to zero,
the odd-probe payment is target-equivalent on exhaustive windows. -/
theorem canonicalOddNativeVanishingBudget_iff_criticalStripRH :
    CanonicalOddNativeVanishingBudget ↔ CriticalStripRH := by
  constructor
  · rintro ⟨b, hb, hcost⟩
    apply criticalStripRH_of_exhaustive_vanishing_budget
      unitWeights unitWeights_positive canonicalJReflectedWindow
      canonicalJReflectedWindow_eventuallyCovered b hb
    intro n
    rw [← oddProbe_native_cost_eq_windowEnergy unitWeights
      (fun _ => rfl) (canonicalJReflectedWindow n)
      (canonicalJReflectedWindow_reflected n)]
    exact hcost n
  · intro hRH
    refine ⟨fun _ => 0, tendsto_const_nhds, ?_⟩
    intro n
    have hzero := (canonicalOddNativeZero_iff_criticalStripRH.mpr hRH) n
    exact le_of_eq hzero

#print axioms oddProbe_kernelXi_displacement_zero
#print axioms oddProbe_native_cost_eq_windowEnergy
#print axioms canonicalOddSubunitKernelXiFamily
#print axioms canonicalOddNativeZero_iff_criticalStripRH
#print axioms canonicalOddNativeVanishingBudget_iff_criticalStripRH

end SixBirdsDualityConfinement.RH.OddProbePaymentNoGo
