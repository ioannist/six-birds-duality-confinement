import SixBirdsDualityConfinement.RH.JTransportNoGo

/-! A gain test for every faithful linear transport on actual zero windows.
The test does not assume that a particular analytic transport exists. It
shows that reversible changes of coordinates cannot create a strict
residual-return margin on a nonzero displacement. -/

noncomputable section
namespace SixBirdsDualityConfinement.RH.FaithfulTransportNoGo

open ClassicalZeroLedger FiniteZeroWindows ActualInvolution
open SixBirdsNeedles.XiCore

/-- If a bounded linear return exactly recovers a state, its amplification
must cancel any strict forward contraction on that nonzero state. -/
theorem faithful_linear_gain_forces_zero
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (T S : E →L[ℝ] E) (v : E) (a : ℝ)
    (hreturn : S (T v) = v)
    (hforward : ‖T v‖ ^ 2 ≤ a * ‖v‖ ^ 2)
    (hgain : a * ‖S‖ ^ 2 < 1) :
    v = 0 := by
  by_contra hv
  have hpos : 0 < ‖v‖ ^ 2 :=
    sq_pos_of_pos (norm_pos_iff.mpr hv)
  have hback : ‖v‖ ^ 2 ≤ ‖S‖ ^ 2 * ‖T v‖ ^ 2 := by
    have h := S.le_opNorm (T v)
    rw [hreturn] at h
    simpa only [mul_pow] using
      (pow_le_pow_left₀ (norm_nonneg _) h 2)
  have hscaled : ‖S‖ ^ 2 * ‖T v‖ ^ 2 ≤
      (a * ‖S‖ ^ 2) * ‖v‖ ^ 2 := by
    have h := mul_le_mul_of_nonneg_left hforward (sq_nonneg ‖S‖)
    nlinarith [h]
  have hstrict : (a * ‖S‖ ^ 2) * ‖v‖ ^ 2 < ‖v‖ ^ 2 := by
    nlinarith [mul_lt_mul_of_pos_right hgain hpos]
  exact (not_lt_of_ge (hback.trans hscaled)) hstrict

/-- On every actual `J`-closed zero window the displacement lies entirely
in the XI residual channel. A faithful linear transport with a strict
forward/return gain therefore forces its XI energy to vanish. -/
theorem window_faithful_gain_forces_zero_energy
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W)
    (T S : EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ]
      EuclideanSpace ℝ {ρ // ρ ∈ W})
    (a : ℝ)
    (hreturn : S (T (displacementVector m W)) = displacementVector m W)
    (hforward :
      ‖hilbertKernelXi (invariantProbe W) (T (displacementVector m W))‖ ^ 2 ≤
        a * ‖hilbertKernelXi (invariantProbe W)
          (displacementVector m W)‖ ^ 2)
    (hblind : invariantProbe W (T (displacementVector m W)) = 0)
    (hgain : a * ‖S‖ ^ 2 < 1) :
    windowEnergy m W = 0 := by
  have hvker : invariantProbe W (displacementVector m W) = 0 :=
    invariantProbe_displacement_zero_J m hm W hW
  have hxi (v : EuclideanSpace ℝ {ρ // ρ ∈ W})
      (hv : invariantProbe W v = 0) :
      hilbertKernelXi (invariantProbe W) v = v :=
    (invariantProbe W).ker.starProjection_eq_self_iff.mpr hv
  rw [hxi _ hblind, hxi _ hvker] at hforward
  have hz := faithful_linear_gain_forces_zero T S
    (displacementVector m W) a hreturn hforward hgain
  rw [← displacementVector_norm_sq, hz, norm_zero, zero_pow (by norm_num)]

/-- Any such strict faithful linear loop uniformly on the canonical
actual-zero windows already entails the classical critical-strip RH. -/
theorem canonical_faithful_gain_implies_criticalStripRH
    (T S : ∀ n : ℕ,
      EuclideanSpace ℝ {ρ // ρ ∈ canonicalJReflectedWindow n} →L[ℝ]
        EuclideanSpace ℝ {ρ // ρ ∈ canonicalJReflectedWindow n})
    (a : ℕ → ℝ)
    (hreturn : ∀ n,
      S n (T n (displacementVector unitWeights (canonicalJReflectedWindow n))) =
        displacementVector unitWeights (canonicalJReflectedWindow n))
    (hforward : ∀ n,
      ‖hilbertKernelXi (invariantProbe (canonicalJReflectedWindow n))
        (T n (displacementVector unitWeights (canonicalJReflectedWindow n)))‖ ^ 2 ≤
          a n * ‖hilbertKernelXi (invariantProbe (canonicalJReflectedWindow n))
            (displacementVector unitWeights (canonicalJReflectedWindow n))‖ ^ 2)
    (hblind : ∀ n,
      invariantProbe (canonicalJReflectedWindow n)
        (T n (displacementVector unitWeights (canonicalJReflectedWindow n))) = 0)
    (hgain : ∀ n, a n * ‖S n‖ ^ 2 < 1) :
    CriticalStripRH := by
  apply criticalStripRH_of_exhaustive_vanishing_budget
    unitWeights unitWeights_positive canonicalJReflectedWindow
    canonicalJReflectedWindow_eventuallyCovered
    (fun _ => (0 : ℝ)) tendsto_const_nhds
  intro n
  exact le_of_eq (window_faithful_gain_forces_zero_energy
    unitWeights (fun _ => rfl) (canonicalJReflectedWindow n)
    (canonicalJReflectedWindow_reflected n)
    (T n) (S n) (a n) (hreturn n) (hforward n) (hblind n) (hgain n))

end SixBirdsDualityConfinement.RH.FaithfulTransportNoGo
