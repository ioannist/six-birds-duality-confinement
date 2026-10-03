import SixBirdsDualityConfinement.RH.ArithmeticXiJensen

/-!
Finite RH zero windows cut out by compact Jensen disks of the actual
arithmetic entire completion. The divisor has finite support on each
disk, so these windows require no arbitrary encoding of zeros. Disks
centered on the critical line are `J`-reflected, and growing disks are
exhaustive. No source-work estimate follows from this construction.
-/

noncomputable section
open Complex Metric Filter
open scoped Topology
namespace SixBirdsDualityConfinement.RH.ArithmeticJensenWindows

open ClassicalZeroLedger FiniteZeroWindows ActualInvolution ArithmeticXiJensen
open SixBirdsNeedles.XiCore

def zeroDiskSet (c : ℂ) (R : ℝ) : Set NontrivialZero :=
  {ρ | ρ.val ∈ closedBall c |R|}

theorem zeroDiskSet_finite (c : ℂ) (R : ℝ) :
    (zeroDiskSet c R).Finite := by
  let D := MeromorphicOn.divisor arithmeticXiEntire (closedBall c |R|)
  have hD : D.support.Finite :=
    D.finiteSupport (isCompact_closedBall c |R|)
  apply Set.Finite.of_injOn (t := D.support) (f := Subtype.val)
  · intro ρ hρ
    have hzero : riemannZeta ρ.val = 0 :=
      (completed_zero_iff_zeta_zero_of_re_pos ρ.val ρ.property.2.1).mp
        ρ.property.1
    exact (arithmeticXi_circle_divisor_support_iff_zeta_zero
      c R ρ.val hρ ρ.property.2.1 ρ.property.2.2).mpr hzero
  · intro ρ₁ h₁ ρ₂ h₂ h
    exact Subtype.ext h
  · exact hD

def zeroDiskWindow (c : ℂ) (R : ℝ) : Finset NontrivialZero := by
  classical
  exact (zeroDiskSet_finite c R).toFinset

theorem mem_zeroDiskWindow (c : ℂ) (R : ℝ) (ρ : NontrivialZero) :
    ρ ∈ zeroDiskWindow c R ↔ ρ.val ∈ closedBall c |R| := by
  simp [zeroDiskWindow, zeroDiskSet]

/-- Every divisor point of the entire completion on a Jensen disk is
represented by exactly one actual critical-strip zero in the finite
window. This is support equality, not yet a boundary moment formula. -/
theorem zeroDiskWindow_image_eq_divisor_support (c : ℂ) (R : ℝ) :
    (fun ρ : NontrivialZero => ρ.val) ''
        (↑(zeroDiskWindow c R) : Set NontrivialZero) =
      Function.support
        (MeromorphicOn.divisor arithmeticXiEntire (closedBall c |R|)) := by
  ext s
  constructor
  · rintro ⟨ρ, hρ, rfl⟩
    have hmem := (mem_zeroDiskWindow c R ρ).mp hρ
    have hzeta : riemannZeta ρ.val = 0 :=
      (completed_zero_iff_zeta_zero_of_re_pos ρ.val ρ.property.2.1).mp
        ρ.property.1
    exact (arithmeticXi_circle_divisor_support_iff_classical_zero
      c R ρ.val hmem).mpr ⟨hzeta, ρ.property.2.1, ρ.property.2.2⟩
  · intro hsupport
    have hmem : s ∈ closedBall c |R| :=
      (MeromorphicOn.divisor arithmeticXiEntire (closedBall c |R|)).supportWithinDomain
        hsupport
    obtain ⟨hzeta, hlo, hhi⟩ :=
      (arithmeticXi_circle_divisor_support_iff_classical_zero
        c R s hmem).mp hsupport
    let ρ : NontrivialZero :=
      ⟨s, (completed_zero_iff_zeta_zero_of_re_pos s hlo).mpr hzeta,
        hlo, hhi⟩
    exact ⟨ρ, (mem_zeroDiskWindow c R ρ).mpr hmem, rfl⟩

def criticalLineCenter (T : ℝ) : ℂ := ⟨1 / 2, T⟩

theorem criticalLineCenter_J_fixed (T : ℝ) :
    J (criticalLineCenter T) = criticalLineCenter T := by
  apply (J_fixed_iff _).mpr
  rfl

theorem J_sub_criticalLineCenter (T : ℝ) (s : ℂ) :
    J s - criticalLineCenter T = -(star (s - criticalLineCenter T)) := by
  apply Complex.ext
  · simp [J_re, criticalLineCenter, Complex.sub_re]
    ring
  · simp [J_im, criticalLineCenter, Complex.sub_im]
    ring

theorem J_dist_criticalLineCenter (T : ℝ) (s : ℂ) :
    dist (J s) (criticalLineCenter T) =
      dist s (criticalLineCenter T) := by
  rw [dist_eq_norm, dist_eq_norm, J_sub_criticalLineCenter,
    norm_neg, norm_star]

theorem zeroDiskWindow_J_reflected (T R : ℝ) :
    JReflectedWindow (zeroDiskWindow (criticalLineCenter T) R) := by
  intro ρ hρ
  rw [mem_zeroDiskWindow] at hρ ⊢
  change dist (J ρ.val) (criticalLineCenter T) ≤ |R|
  rw [J_dist_criticalLineCenter]
  exact hρ

def canonicalJensenWindow (n : ℕ) : Finset NontrivialZero :=
  zeroDiskWindow (criticalLineCenter 0) n

/-- Canonical Jensen disks form a nested finite exhaustion. This is a
geometric property of the actual zero windows, independent of RH. -/
theorem canonicalJensenWindow_subset_succ (n : ℕ) :
    canonicalJensenWindow n ⊆ canonicalJensenWindow (n + 1) := by
  intro ρ hρ
  rw [canonicalJensenWindow, mem_zeroDiskWindow] at hρ ⊢
  change dist ρ.val (criticalLineCenter 0) ≤ |(n : ℝ)| at hρ
  change dist ρ.val (criticalLineCenter 0) ≤ |((n + 1 : ℕ) : ℝ)|
  have hn : (n : ℝ) ≤ ((n + 1 : ℕ) : ℝ) := by exact_mod_cast Nat.le_succ n
  rw [abs_of_nonneg (Nat.cast_nonneg n)] at hρ
  rw [abs_of_nonneg (Nat.cast_nonneg (n + 1))]
  exact hρ.trans hn

theorem canonicalJensenWindow_reflected (n : ℕ) :
    JReflectedWindow (canonicalJensenWindow n) :=
  zeroDiskWindow_J_reflected 0 n

theorem canonicalJensenWindow_eventuallyCovered :
    EventuallyCovered canonicalJensenWindow := by
  intro ρ
  obtain ⟨N, hN⟩ := exists_nat_gt
    (dist ρ.val (criticalLineCenter 0))
  apply Filter.eventually_atTop.2
  refine ⟨N, ?_⟩
  intro n hn
  rw [canonicalJensenWindow, mem_zeroDiskWindow]
  change dist ρ.val (criticalLineCenter 0) ≤ |(n : ℝ)|
  rw [abs_of_nonneg (Nat.cast_nonneg n)]
  exact hN.le.trans (by exact_mod_cast hn)

/-- The zero charge on the arithmetic disk windows is exactly the
Hilbert XI residual under the actual invariant probe. -/
theorem canonicalJensenWindow_xi_eq_energy (n : ℕ) :
    ‖hilbertKernelXi (invariantProbe (canonicalJensenWindow n))
      (displacementVector unitWeights (canonicalJensenWindow n))‖ ^ 2 =
      windowEnergy unitWeights (canonicalJensenWindow n) := by
  let W := canonicalJensenWindow n
  have hker : displacementVector unitWeights W ∈ (invariantProbe W).ker :=
    invariantProbe_displacement_zero_J unitWeights (fun _ => rfl) W
      (canonicalJensenWindow_reflected n)
  change ‖(invariantProbe W).ker.starProjection
    (displacementVector unitWeights W)‖ ^ 2 = _
  rw [Submodule.starProjection_eq_self_iff.mpr hker]
  exact displacementVector_norm_sq unitWeights W

/-- The actual positive zero-window XI charge accumulates as the
arithmetic Jensen radius grows. A Navier high-tail XI decreases with
its cutoff, so the two limit directions cannot be identified merely
by matching Gaussian kernels. -/
theorem canonicalJensenWindow_energy_mono (n : ℕ) :
    windowEnergy unitWeights (canonicalJensenWindow n) ≤
      windowEnergy unitWeights (canonicalJensenWindow (n + 1)) := by
  unfold windowEnergy
  apply Finset.sum_le_sum_of_subset_of_nonneg
    (canonicalJensenWindow_subset_succ n)
  intro ρ hρ hnot
  exact term_nonneg unitWeights ρ

theorem canonicalJensenWindow_xi_mono (n : ℕ) :
    ‖hilbertKernelXi (invariantProbe (canonicalJensenWindow n))
      (displacementVector unitWeights (canonicalJensenWindow n))‖ ^ 2 ≤
    ‖hilbertKernelXi (invariantProbe (canonicalJensenWindow (n + 1)))
      (displacementVector unitWeights (canonicalJensenWindow (n + 1)))‖ ^ 2 := by
  rw [canonicalJensenWindow_xi_eq_energy,
    canonicalJensenWindow_xi_eq_energy]
  exact canonicalJensenWindow_energy_mono n

/-- A vanishing residual budget on these exhaustive arithmetic windows
reaches classical critical-strip RH. This theorem exposes the still
unpaid quantitative premise; Jensen's identity does not prove it. -/
theorem criticalStripRH_of_jensen_XI_budget
    (b : ℕ → ℝ) (hb : Tendsto b atTop (𝓝 0))
    (hbudget : ∀ n,
      RCLike.re (inner ℝ
        (displacementVector unitWeights (canonicalJensenWindow n))
        ((auditResidual (ContinuousLinearMap.id ℝ
            (EuclideanSpace ℝ {ρ // ρ ∈ canonicalJensenWindow n}))
          (ContinuousLinearMap.id ℝ
            (EuclideanSpace ℝ {ρ // ρ ∈ canonicalJensenWindow n}))
          (invariantProbe (canonicalJensenWindow n)))
          (displacementVector unitWeights (canonicalJensenWindow n)))) ≤ b n) :
    CriticalStripRH :=
  criticalStripRH_of_J_window_XI_budget unitWeights unitWeights_positive
    (fun _ => rfl) canonicalJensenWindow canonicalJensenWindow_reflected
    canonicalJensenWindow_eventuallyCovered b hb hbudget

#print axioms zeroDiskSet_finite
#print axioms zeroDiskWindow_J_reflected
#print axioms zeroDiskWindow_image_eq_divisor_support
#print axioms canonicalJensenWindow_eventuallyCovered
#print axioms canonicalJensenWindow_xi_eq_energy
#print axioms canonicalJensenWindow_energy_mono
#print axioms canonicalJensenWindow_xi_mono
#print axioms criticalStripRH_of_jensen_XI_budget

end SixBirdsDualityConfinement.RH.ArithmeticJensenWindows
