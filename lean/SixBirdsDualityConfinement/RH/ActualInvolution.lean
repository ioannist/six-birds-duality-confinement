import SixBirdsDualityConfinement.RH.FiniteZeroWindows
import SixBirdsDualityConfinement.RH.CompletedZetaConjugation

/-!
The manuscript's critical-line involution on actual complex coordinates.
The functional equation gives `s ↦ 1 - s`. The conjugation theorem in
`CompletedZetaConjugation` supplies the additional symmetry needed to
restrict `s ↦ 1 - star(s)` to actual completed-zeta zeros.
-/

noncomputable section

namespace SixBirdsDualityConfinement.RH.ActualInvolution

open ClassicalZeroLedger
open CompletedZetaConjugation
open FiniteZeroWindows
open SixBirdsNeedles.XiCore
open Filter
open scoped InnerProduct InnerProductSpace
open scoped Topology

def J (s : ℂ) : ℂ := 1 - star s

theorem J_re (s : ℂ) : (J s).re = 1 - s.re := by
  simp [J, Complex.sub_re]

theorem J_im (s : ℂ) : (J s).im = s.im := by
  simp [J, Complex.sub_im]

theorem J_involutive (s : ℂ) : J (J s) = s := by
  apply Complex.ext
  · simp [J_re]
  · simp [J_im]

theorem J_fixed_iff (s : ℂ) : J s = s ↔ s.re = (1 / 2 : ℝ) := by
  constructor
  · intro h
    have hre := congrArg Complex.re h
    rw [J_re] at hre
    linarith
  · intro h
    apply Complex.ext
    · rw [J_re]
      linarith
    · rw [J_im]

def J_zero (ρ : NontrivialZero) : NontrivialZero :=
  ⟨J ρ.val, by
    change completedRiemannZeta (1 - star ρ.val) = 0
    rw [completedRiemannZeta_one_sub, completedRiemannZeta_conj, ρ.property.1]
    simp,
    by rw [J_re]; linarith [ρ.property.2.2],
    by rw [J_re]; linarith [ρ.property.2.1]⟩

theorem J_zero_involutive (ρ : NontrivialZero) : J_zero (J_zero ρ) = ρ := by
  apply Subtype.ext
  exact J_involutive ρ.val

theorem J_zero_fixed_iff (ρ : NontrivialZero) :
    J_zero ρ = ρ ↔ ρ.val.re = (1 / 2 : ℝ) := by
  rw [Subtype.ext_iff]
  exact J_fixed_iff ρ.val

theorem displacement_J_zero (ρ : NontrivialZero) :
    displacement (J_zero ρ) = -displacement ρ := by
  change (J ρ.val).re - (1 / 2 : ℝ) = -(ρ.val.re - (1 / 2 : ℝ))
  rw [J_re]
  ring

def JReflectedWindow (W : Finset NontrivialZero) : Prop :=
  ∀ ρ ∈ W, J_zero ρ ∈ W

def closeJReflection (W : Finset NontrivialZero) : Finset NontrivialZero := by
  classical
  exact W ∪ W.image J_zero

theorem closeJReflection_reflected (W : Finset NontrivialZero) :
    JReflectedWindow (closeJReflection W) := by
  classical
  intro ρ hρ
  change ρ ∈ W ∪ W.image J_zero at hρ
  change J_zero ρ ∈ W ∪ W.image J_zero
  rcases Finset.mem_union.mp hρ with h | h
  · exact Finset.mem_union_right _ (Finset.mem_image_of_mem J_zero h)
  · obtain ⟨σ, hσ, hσρ⟩ := Finset.mem_image.mp h
    rw [← hσρ, J_zero_involutive]
    exact Finset.mem_union_left _ hσ

theorem closeJReflection_eventuallyCovered
    (W : ℕ → Finset NontrivialZero) (hW : EventuallyCovered W) :
    EventuallyCovered (fun n => closeJReflection (W n)) := by
  classical
  intro ρ
  exact (hW ρ).mono fun n hn => Finset.mem_union_left _ hn

theorem exists_JReflected_eventuallyCovered :
    ∃ W : ℕ → Finset NontrivialZero,
      (∀ n, JReflectedWindow (W n)) ∧ EventuallyCovered W := by
  letI : Countable NontrivialZero :=
    ClassicalZeroCountable.nontrivialZero_countable
  letI : Encodable NontrivialZero := Encodable.ofCountable _
  exact ⟨fun n => closeJReflection (codedWindow n),
    fun n => closeJReflection_reflected (codedWindow n),
    closeJReflection_eventuallyCovered codedWindow codedWindow_eventuallyCovered⟩

/-- Cancellation uses the imaginary-part-preserving involution on actual
zeros, with its own symmetry hypothesis on the weights. -/
theorem weighted_displacement_sum_zero_J
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    ∑ ρ ∈ W, Real.sqrt (m ρ) * displacement ρ = 0 := by
  classical
  let f : NontrivialZero → ℝ := fun ρ => Real.sqrt (m ρ) * displacement ρ
  change ∑ ρ ∈ W, f ρ = 0
  apply Finset.sum_involution (fun ρ _ => J_zero ρ)
  · intro ρ _
    dsimp [f]
    rw [hm, displacement_J_zero]
    ring
  · intro ρ _ hf heq
    have hd := displacement_J_zero ρ
    rw [heq] at hd
    have hz : displacement ρ = 0 := by linarith
    exact hf (by simp [f, hz])
  · exact hW
  · intro ρ _
    exact J_zero_involutive ρ

theorem invariantProbe_displacement_zero_J
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    invariantProbe W (displacementVector m W) = 0 := by
  classical
  change inner ℝ (invariantVector W) (displacementVector m W) = 0
  rw [invariantVector, displacementVector, EuclideanSpace.inner_toLp_toLp]
  simp only [dotProduct, star_trivial, mul_one]
  simpa [Finset.univ_eq_attach] using
    (Finset.sum_attach W (fun ρ => Real.sqrt (m ρ) * displacement ρ)).trans
      (weighted_displacement_sum_zero_J m hm W hW)

/-- XI's actual-state residual identity now uses the zero-set involution
whose fixed locus is the critical line. It remains an identity, not a
source estimate forcing the right side to vanish. -/
theorem fixedTarget_J_window_quadratic_eq_windowEnergy
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    RCLike.re (inner ℝ (displacementVector m W)
      ((auditResidual (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (invariantProbe W)) (displacementVector m W))) =
      windowEnergy m W := by
  rw [auditResidual_id_eq_xi]
  exact (xi_fullReadout_native_kernel _ _
    (invariantProbe_displacement_zero_J m hm W hW)).trans
      (displacementVector_norm_sq m W)

/-- The exact XI payment still needs a source-derived vanishing budget.
This theorem isolates that remaining quantitative input on genuine
`1 - conj`-closed windows. -/
theorem criticalStripRH_of_J_window_XI_budget
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (hsym : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : ℕ → Finset NontrivialZero)
    (hW : ∀ n, JReflectedWindow (W n))
    (hcover : EventuallyCovered W)
    (b : ℕ → ℝ) (hb : Tendsto b atTop (𝓝 0))
    (hbudget : ∀ n,
      RCLike.re (inner ℝ (displacementVector m (W n))
        ((auditResidual (ContinuousLinearMap.id ℝ
            (EuclideanSpace ℝ {ρ // ρ ∈ W n}))
          (ContinuousLinearMap.id ℝ
            (EuclideanSpace ℝ {ρ // ρ ∈ W n}))
          (invariantProbe (W n))) (displacementVector m (W n)))) ≤ b n) :
    CriticalStripRH := by
  apply criticalStripRH_of_exhaustive_vanishing_budget m hm W hcover b hb
  intro n
  rw [← fixedTarget_J_window_quadratic_eq_windowEnergy m hsym (W n) (hW n)]
  exact hbudget n

theorem windowEnergy_eq_zero_iff_J_fixed
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (W : Finset NontrivialZero) :
    windowEnergy m W = 0 ↔ ∀ ρ ∈ W, J_zero ρ = ρ := by
  rw [windowEnergy_eq_zero_iff m hm W]
  exact forall_congr' fun ρ => by
    apply imp_congr_right
    intro _
    rw [J_zero_fixed_iff]
    simp [displacement, sub_eq_zero]

/-- This is the exact classical readout of the actual-zero involution,
without a separately assumed conjugation symmetry or a selected ledger. -/
theorem all_zero_fixed_iff_criticalStripRH :
    (∀ ρ : NontrivialZero, J_zero ρ = ρ) ↔ CriticalStripRH := by
  constructor
  · intro h s hz hlo hhi
    have hcomp := (completed_zero_iff_zeta_zero_of_re_pos s hlo).mpr hz
    exact (J_zero_fixed_iff ⟨s, hcomp, hlo, hhi⟩).mp
      (h ⟨s, hcomp, hlo, hhi⟩)
  · intro h ρ
    apply (J_zero_fixed_iff ρ).mpr
    exact h ρ.val
      ((completed_zero_iff_zeta_zero_of_re_pos ρ.val ρ.property.2.1).mp ρ.property.1)
      ρ.property.2.1 ρ.property.2.2

/-- A fixed exhaustive family of actual-zero windows closed under the
height-preserving involution `s ↦ 1 - conj(s)`. -/
def canonicalJReflectedWindow : ℕ → Finset NontrivialZero :=
  Classical.choose exists_JReflected_eventuallyCovered

theorem canonicalJReflectedWindow_reflected (n : ℕ) :
    JReflectedWindow (canonicalJReflectedWindow n) :=
  (Classical.choose_spec exists_JReflected_eventuallyCovered).1 n

theorem canonicalJReflectedWindow_eventuallyCovered :
    EventuallyCovered canonicalJReflectedWindow :=
  (Classical.choose_spec exists_JReflected_eventuallyCovered).2

/-- The common varying-carrier XI absorption theorem reaches the classical
critical-strip statement on the paper's actual critical-line involution.
The native budget is zero by the proved `J` pair cancellation. -/
theorem criticalStripRH_of_J_subunitKernelXiFamily
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (hsym : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : ℕ → Finset NontrivialZero)
    (hW : ∀ n, JReflectedWindow (W n))
    (hcover : EventuallyCovered W)
    (hc : SubunitKernelXiFamily (fun _ : ℕ => True)
      (fun n => invariantProbe (W n))
      (fun n => displacementVector m (W n))) :
    CriticalStripRH := by
  have hn : ∀ n, True →
      ‖hilbertNativeCurrency (invariantProbe (W n))
        (displacementVector m (W n))‖ ^ 2 ≤ (0 : ℝ) := by
    intro n _
    have hvker : displacementVector m (W n) ∈ (invariantProbe (W n)).ker :=
      invariantProbe_displacement_zero_J m hsym (W n) (hW n)
    change ‖(invariantProbe (W n)).kerᗮ.starProjection
      (displacementVector m (W n))‖ ^ 2 ≤ 0
    rw [(invariantProbe (W n)).ker.starProjection_orthogonal_apply_eq_zero hvker]
    norm_num
  obtain ⟨q, _, hq, hbound⟩ :=
    SubunitKernelXiFamily.full_bounds (fun _ : ℕ => True)
      (fun n => invariantProbe (W n))
      (fun n => displacementVector m (W n))
      (fun _ => (0 : ℝ)) hc hn
  apply criticalStripRH_of_exhaustive_vanishing_budget m hm W hcover
    (fun _ => (0 : ℝ)) tendsto_const_nhds
  intro n
  rw [← displacementVector_norm_sq]
  have hb := hbound n trivial
  simpa using hb

/-- Canonical conditional RH endpoint with exactly the same kernel-XI
closure predicate used by the spectral Navier instance, now on genuine
`J`-closed zero windows. -/
theorem criticalStripRH_of_canonical_J_subunitKernelXiClosure
    (hc : SubunitKernelXiFamily (fun _ : ℕ => True)
      (fun n => invariantProbe (canonicalJReflectedWindow n))
      (fun n => displacementVector unitWeights (canonicalJReflectedWindow n))) :
    CriticalStripRH :=
  criticalStripRH_of_J_subunitKernelXiFamily unitWeights unitWeights_positive
    (fun _ => rfl) canonicalJReflectedWindow
    canonicalJReflectedWindow_reflected canonicalJReflectedWindow_eventuallyCovered hc

/-- On these actual `J`-closed zero windows the conditional premise is
exactly as strong as critical-strip RH. This is an adversarial calibration,
not a proof that a source law supplies the closure. -/
theorem canonical_J_subunitKernelXiClosure_iff_criticalStripRH :
    SubunitKernelXiFamily (fun _ : ℕ => True)
      (fun n => invariantProbe (canonicalJReflectedWindow n))
      (fun n => displacementVector unitWeights (canonicalJReflectedWindow n)) ↔
      CriticalStripRH := by
  constructor
  · exact criticalStripRH_of_canonical_J_subunitKernelXiClosure
  · intro hRH
    refine ⟨0, le_refl _, by norm_num, ?_⟩
    intro n _
    have hz : windowEnergy unitWeights (canonicalJReflectedWindow n) = 0 := by
      apply (windowEnergy_eq_zero_iff unitWeights unitWeights_positive _).mpr
      intro ρ _
      exact sub_eq_zero.mpr (hRH ρ.val
        ((completed_zero_iff_zeta_zero_of_re_pos ρ.val ρ.property.2.1).mp
          ρ.property.1)
        ρ.property.2.1 ρ.property.2.2)
    have hv : ‖displacementVector unitWeights (canonicalJReflectedWindow n)‖ ^ 2 = 0 := by
      rwa [displacementVector_norm_sq]
    have hv0 : displacementVector unitWeights (canonicalJReflectedWindow n) = 0 := by
      apply norm_eq_zero.mp
      nlinarith [norm_nonneg (displacementVector unitWeights
        (canonicalJReflectedWindow n))]
    simp [hv0]

/-- The actual RH window condition with a specified fraction, before
existentially choosing a fraction for the family. -/
def CanonicalJFixedFraction (q : ℝ) : Prop :=
  ∀ n : ℕ,
    ‖hilbertKernelXi (invariantProbe (canonicalJReflectedWindow n))
      (displacementVector unitWeights (canonicalJReflectedWindow n))‖ ^ 2 ≤
      q * ‖displacementVector unitWeights (canonicalJReflectedWindow n)‖ ^ 2

/-- Every specified subunit fraction has exactly the same RH content.
Sharing the numerical fraction with another family cannot by itself
couple the two realized-state closure obligations. -/
theorem canonicalJFixedFraction_iff_criticalStripRH
    (q : ℝ) (hq0 : 0 ≤ q) (hq : q < 1) :
    CanonicalJFixedFraction q ↔ CriticalStripRH := by
  constructor
  · intro hc
    apply criticalStripRH_of_canonical_J_subunitKernelXiClosure
    exact ⟨q, hq0, hq, fun n _ => hc n⟩
  · intro hRH n
    have hz : windowEnergy unitWeights (canonicalJReflectedWindow n) = 0 := by
      apply (windowEnergy_eq_zero_iff unitWeights unitWeights_positive _).mpr
      intro ρ _
      exact sub_eq_zero.mpr (hRH ρ.val
        ((completed_zero_iff_zeta_zero_of_re_pos ρ.val ρ.property.2.1).mp
          ρ.property.1)
        ρ.property.2.1 ρ.property.2.2)
    have hv : ‖displacementVector unitWeights (canonicalJReflectedWindow n)‖ ^ 2 = 0 := by
      rwa [displacementVector_norm_sq]
    have hv0 : displacementVector unitWeights (canonicalJReflectedWindow n) = 0 := by
      apply norm_eq_zero.mp
      nlinarith [norm_nonneg (displacementVector unitWeights
        (canonicalJReflectedWindow n))]
    simp [hv0]

/-- Any proposed second application `P q` sharing only the numerical XI
fraction factors from the RH condition. A substantive joint condition must
connect the actual states or their source operations. -/
theorem canonicalJSharedFraction_factorization (P : ℝ → Prop) :
    (∃ q : ℝ, 0 ≤ q ∧ q < 1 ∧ CanonicalJFixedFraction q ∧ P q) ↔
      CriticalStripRH ∧ ∃ q : ℝ, 0 ≤ q ∧ q < 1 ∧ P q := by
  constructor
  · rintro ⟨q, hq0, hq, hRHq, hP⟩
    exact ⟨(canonicalJFixedFraction_iff_criticalStripRH q hq0 hq).mp hRHq,
      ⟨q, hq0, hq, hP⟩⟩
  · rintro ⟨hRH, ⟨q, hq0, hq, hP⟩⟩
    exact ⟨q, hq0, hq,
      (canonicalJFixedFraction_iff_criticalStripRH q hq0 hq).mpr hRH, hP⟩

end SixBirdsDualityConfinement.RH.ActualInvolution
