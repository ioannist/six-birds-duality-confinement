import SixBirdsDualityConfinement.RH.JTransportNoGo

/-!
Gaussian probes depending only on the imaginary ordinate of actual completed-
zeta zeros are invariant under the genuine critical-line involution. They
therefore miss the J-odd zero-window displacement at every heat time. This is
a scoped obstruction for even ordinate traces, not an explicit formula or a
no-go theorem for source laws with J-odd data.
-/

noncomputable section
open scoped InnerProduct InnerProductSpace
namespace SixBirdsDualityConfinement.RH.OrdinateGaussianNoGo

open ClassicalZeroLedger FiniteZeroWindows ActualInvolution JTransportNoGo

def ordinateGaussianVector (W : Finset NontrivialZero) (t : ℝ) :
    EuclideanSpace ℝ {ρ // ρ ∈ W} :=
  WithLp.toLp 2 (fun ρ => Real.exp (-t * ρ.val.val.im ^ 2))

def ordinateGaussianProbe (W : Finset NontrivialZero) (t : ℝ) :
    EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ] ℝ :=
  innerSL ℝ (ordinateGaussianVector W t)

theorem ordinateGaussianVector_J_fixed
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) (t : ℝ) :
    windowJTransport W hW (ordinateGaussianVector W t) =
      ordinateGaussianVector W t := by
  ext ρ
  change Real.exp (-t * (J ρ.val.val).im ^ 2) =
    Real.exp (-t * ρ.val.val.im ^ 2)
  rw [J_im]

theorem ordinateGaussianProbe_J_invariant
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) (t : ℝ)
    (v : EuclideanSpace ℝ {ρ // ρ ∈ W}) :
    ordinateGaussianProbe W t (windowJTransport W hW v) =
      ordinateGaussianProbe W t v := by
  change inner ℝ (ordinateGaussianVector W t)
      (windowJTransport W hW v) =
    inner ℝ (ordinateGaussianVector W t) v
  have h := (windowJTransport W hW).inner_map_map
    (ordinateGaussianVector W t) v
  rw [ordinateGaussianVector_J_fixed W hW t] at h
  exact h

/-- Every Gaussian heat time gives zero reading on the actual J-odd
displacement. Even all such readings cannot by themselves pay its XI cost. -/
theorem ordinateGaussianProbe_displacement_zero
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) (t : ℝ) :
    ordinateGaussianProbe W t (displacementVector m W) = 0 := by
  exact invariant_linear_observation_displacement_zero m hm W hW
    (ordinateGaussianProbe W t)
    (ordinateGaussianProbe_J_invariant W hW t)

/-- A proposed finite tariff using only one even Gaussian-ordinate reading
per canonical zero window. The heat times may be chosen arbitrarily. -/
def CanonicalOrdinateGaussianBudget (C : ℝ) (t : ℕ → ℝ) : Prop :=
  ∀ n : ℕ,
    ‖SixBirdsNeedles.XiCore.hilbertKernelXi
        (invariantProbe (canonicalJReflectedWindow n))
        (displacementVector unitWeights (canonicalJReflectedWindow n))‖ ^ 2 ≤
      C * ‖ordinateGaussianProbe (canonicalJReflectedWindow n) (t n)
        (displacementVector unitWeights (canonicalJReflectedWindow n))‖ ^ 2

/-- On the actual exhaustive zero windows, that budget has exactly RH's
strength because every proposed payment reading vanishes by J parity. -/
theorem canonicalOrdinateGaussianBudget_iff_criticalStripRH
    (C : ℝ) (t : ℕ → ℝ) :
    CanonicalOrdinateGaussianBudget C t ↔ CriticalStripRH := by
  constructor
  · intro h
    apply (canonicalJFixedFraction_iff_criticalStripRH 0 (by norm_num)
      (by norm_num)).mp
    intro n
    have hb := h n
    rw [ordinateGaussianProbe_displacement_zero unitWeights
      (fun _ => rfl) (canonicalJReflectedWindow n)
      (canonicalJReflectedWindow_reflected n) (t n)] at hb
    simpa [CanonicalJFixedFraction] using hb
  · intro hRH n
    have hb := (canonicalJFixedFraction_iff_criticalStripRH 0
      (by norm_num) (by norm_num)).mpr hRH n
    simpa [CanonicalJFixedFraction,
      ordinateGaussianProbe_displacement_zero unitWeights
        (fun _ => rfl) (canonicalJReflectedWindow n)
        (canonicalJReflectedWindow_reflected n) (t n)] using hb

end SixBirdsDualityConfinement.RH.OrdinateGaussianNoGo
