import SixBirdsDualityConfinement.RH.ActualInvolution
import SixBirdsDualityConfinement.RH.FullClassicalRHBridge
import SixBirdsDualityConfinement.DualityConfinement.ConcreteConverse

/-! Concrete DC on finite windows of actual completed-zeta zeros. The response
is the horizontal displacement, with the negative identity as its involution.
The two vanishing-domination source predicates are equivalent to Mathlib RH;
no analytic source law supplying either predicate is assumed or derived. -/
noncomputable section
namespace SixBirdsDualityConfinement.RH.ConcreteZeroWindowDC

open ClassicalZeroLedger FiniteZeroWindows ActualInvolution FullClassicalRHBridge
open SixBirdsDualityConfinement.DualityConfinement.ConcreteCore
open SixBirdsDualityConfinement.DualityConfinement.ConcreteFinite
open SixBirdsDualityConfinement.DualityConfinement.ConcreteConverse
open Filter InnerProductSpace
open scoped Topology

/-- The isometric response involution is the negative identity on the real line. -/
def realNeg : ℝ ≃ₗᵢ[ℝ] ℝ := LinearIsometryEquiv.neg ℝ

theorem realNeg_involutive : Function.Involutive realNeg := by
  intro v
  exact neg_neg v

/-- Restrict the actual height-preserving zero involution to a reflected window. -/
def windowJ (W : Finset NontrivialZero) (hW : JReflectedWindow W)
    (rho : {rho // rho ∈ W}) : {rho // rho ∈ W} :=
  ⟨J_zero rho.val, hW rho.val rho.property⟩

theorem windowJ_involutive (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    Function.Involutive (windowJ W hW) := by
  intro rho
  exact Subtype.ext (J_zero_involutive rho.val)

/-- Horizontal displacement of each actual zero; zeros are not quotiented by real part. -/
def windowPsi (W : Finset NontrivialZero) (rho : {rho // rho ∈ W}) : ℝ :=
  displacement rho.val

theorem windowPsi_equivariant (W : Finset NontrivialZero) (hW : JReflectedWindow W)
    (rho : {rho // rho ∈ W}) :
    windowPsi W (windowJ W hW rho) = realNeg (windowPsi W rho) :=
  displacement_J_zero rho.val

theorem windowPsi_minus (W : Finset NontrivialZero) :
    psiMinus realNeg (windowPsi W) = windowPsi W := by
  funext rho
  exact pminus_eq_self realNeg (by rfl)

theorem windowPsi_separates (W : Finset NontrivialZero) (hW : JReflectedWindow W)
    (rho : {rho // rho ∈ W}) :
    windowPsi W rho = 0 ↔ windowJ W hW rho = rho := by
  change displacement rho.val = 0 ↔ windowJ W hW rho = rho
  rw [displacement, sub_eq_zero, Subtype.ext_iff]
  exact (J_zero_fixed_iff rho.val).symm

/-- Natural weights on the window, viewed as real weights for the concrete ledger. -/
def windowWeight (m : NontrivialZero → ℕ) (W : Finset NontrivialZero)
    (rho : {rho // rho ∈ W}) : ℝ := m rho.val

/-- Actual finite rank-one operator ledger, for arbitrary natural weights. -/
def weightedLedger (m : NontrivialZero → ℕ) (W : Finset NontrivialZero) : ℝ →L[ℝ] ℝ := by
  classical
  exact finiteLedger (windowWeight m W) (windowPsi W)

/-- Unit weights give every zero in the window strictly positive visible mass. -/
def ledger (W : Finset NontrivialZero) : ℝ →L[ℝ] ℝ := weightedLedger unitWeights W

theorem rankOne_real (v : ℝ) :
    rankOne ℝ v v = (v ^ 2) • ContinuousLinearMap.id ℝ ℝ := by
  ext
  simp [rankOne_apply, RCLike.inner_apply, pow_two]

theorem weightedLedger_positive (m : NontrivialZero → ℕ) (W : Finset NontrivialZero) :
    (weightedLedger m W).IsPositive := by
  classical
  exact finiteLedger_positive _ (fun rho => Nat.cast_nonneg _) _

/-- The operator is exactly the existing finite-window energy times the identity. -/
theorem weightedLedger_eq_energy (m : NontrivialZero → ℕ) (W : Finset NontrivialZero) :
    weightedLedger m W = windowEnergy m W • ContinuousLinearMap.id ℝ ℝ := by
  classical
  unfold weightedLedger finiteLedger
  simp_rw [rankOne_real, smul_smul]
  rw [← Finset.sum_smul]
  congr 1
  simpa only [windowWeight, windowPsi, Finset.univ_eq_attach] using
    Finset.sum_attach W (fun rho => (m rho : ℝ) * displacement rho ^ 2)

theorem weightedLedger_trace (m : NontrivialZero → ℕ) (W : Finset NontrivialZero) :
    opTrace (weightedLedger m W) = windowEnergy m W := by
  classical
  rw [weightedLedger, finiteLedger_trace]
  simp only [windowPsi, Real.norm_eq_abs, sq_abs]
  simpa only [windowWeight, Finset.univ_eq_attach] using
    Finset.sum_attach W (fun rho => (m rho : ℝ) * displacement rho ^ 2)

theorem ledger_eq_energy (W : Finset NontrivialZero) :
    ledger W = windowEnergy unitWeights W • ContinuousLinearMap.id ℝ ℝ :=
  weightedLedger_eq_energy unitWeights W

theorem ledger_trace (W : Finset NontrivialZero) :
    opTrace (ledger W) = windowEnergy unitWeights W := weightedLedger_trace unitWeights W

/-- Energy is monotone for any fixed natural weights, without reflection assumptions. -/
theorem windowEnergy_mono (m : NontrivialZero → ℕ) {U W : Finset NontrivialZero}
    (hUW : U ⊆ W) : windowEnergy m U ≤ windowEnergy m W := by
  classical
  exact Finset.sum_le_sum_of_subset_of_nonneg hUW (fun rho _ _ => term_nonneg m rho)

/-- A genuine concrete positive domination sequence for one actual-zero window. -/
def WindowRecords (W : Finset NontrivialZero) : Prop :=
  ∃ B : ℕ → (ℝ →L[ℝ] ℝ), (∀ k, (B k - ledger W).IsPositive) ∧
    Tendsto (fun k => opTrace (B k)) atTop (𝓝 0)

/-- This implication invokes the concrete finite DC master theorem and its fixedness return. -/
theorem windowRecords_fixed (W : Finset NontrivialZero) (hW : JReflectedWindow W)
    (hrec : WindowRecords W) : ∀ rho ∈ W, J_zero rho = rho := by
  classical
  obtain ⟨B, hdom, hlim⟩ := hrec
  obtain ⟨_, _, hfixed, _⟩ := finite_master_fixed (windowWeight unitWeights W)
    (fun rho => Nat.cast_nonneg _) (windowPsi W) (windowJ W hW)
    (fun rho _ => windowPsi_separates W hW rho) B hdom hlim
  intro rho hrho
  exact congrArg Subtype.val (hfixed ⟨rho, hrho⟩ (by norm_num [windowWeight, unitWeights]))

/-- Fixed zeros produce the constant zero records by the concrete converse theorem. -/
theorem windowRecords_of_fixed (W : Finset NontrivialZero) (hW : JReflectedWindow W)
    (hfixed : ∀ rho ∈ W, J_zero rho = rho) : WindowRecords W := by
  classical
  obtain ⟨_, hdom, hlim⟩ := finite_converse (windowWeight unitWeights W)
    (fun rho => Nat.cast_nonneg _) (windowPsi W) (by
      intro rho _
      exact (windowPsi_separates W hW rho).mpr (Subtype.ext (hfixed rho.val rho.property)))
  exact ⟨fun _ => 0, hdom, hlim⟩

theorem windowRecords_iff_fixed (W : Finset NontrivialZero) (hW : JReflectedWindow W) :
    WindowRecords W ↔ ∀ rho ∈ W, J_zero rho = rho :=
  ⟨windowRecords_fixed W hW, windowRecords_of_fixed W hW⟩

theorem windowRecords_of_riemannHypothesis (hRH : RiemannHypothesis)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) : WindowRecords W := by
  have hfixed := all_zero_fixed_iff_criticalStripRH.mpr
    (criticalStripRH_iff_riemannHypothesis.mpr hRH)
  exact windowRecords_of_fixed W hW (fun rho _ => hfixed rho)

/-- Concrete DC on any exhaustive sequence of reflected actual-zero windows. -/
theorem windowRecords_family_iff_riemannHypothesis
    (W : ℕ → Finset NontrivialZero) (hW : ∀ n, JReflectedWindow (W n))
    (hcover : EventuallyCovered W) :
    (∀ n, WindowRecords (W n)) ↔ RiemannHypothesis := by
  constructor
  · intro hrec
    apply criticalStripRH_iff_riemannHypothesis.mp
    apply all_zero_fixed_iff_criticalStripRH.mp
    intro rho
    obtain ⟨n, hn⟩ := (hcover rho).exists
    exact windowRecords_fixed _ (hW n) (hrec n) rho hn
  · intro hRH n
    exact windowRecords_of_riemannHypothesis hRH _ (hW n)

/-- Independent records on every canonical reflected window have exactly RH strength. -/
theorem windowRecords_iff_riemannHypothesis :
    (∀ n, WindowRecords (canonicalJReflectedWindow n)) ↔ RiemannHypothesis :=
  windowRecords_family_iff_riemannHypothesis canonicalJReflectedWindow
    canonicalJReflectedWindow_reflected canonicalJReflectedWindow_eventuallyCovered

/-- One diagonal domination sequence for the moving canonical actual-zero windows. -/
def MovingRecords : Prop :=
  ∃ B : ℕ → (ℝ →L[ℝ] ℝ),
    (∀ n, (B n - ledger (canonicalJReflectedWindow n)).IsPositive) ∧
    Tendsto (fun n => opTrace (B n)) atTop (𝓝 0)

/-- A diagonal domination sequence for any family of finite actual-zero windows. -/
def MovingWindowRecords (W : ℕ → Finset NontrivialZero) : Prop :=
  ∃ B : ℕ → (ℝ →L[ℝ] ℝ), (∀ n, (B n - ledger (W n)).IsPositive) ∧
    Tendsto (fun n => opTrace (B n)) atTop (𝓝 0)

/-- Eventual coverage suffices for the fixed trace floor; reflectedness is unnecessary. -/
theorem moving_trace_floor_family (W : ℕ → Finset NontrivialZero)
    (hcover : EventuallyCovered W) (B : ℕ → (ℝ →L[ℝ] ℝ))
    (hdom : ∀ n, (B n - ledger (W n)).IsPositive) (rho : NontrivialZero) :
    ∀ᶠ n in atTop, displacement rho ^ 2 ≤ opTrace (B n) := by
  apply (hcover rho).mono
  intro n hn
  have hterm : displacement rho ^ 2 ≤ windowEnergy unitWeights (W n) := by
    simpa [unitWeights] using term_le_window unitWeights (W n) rho hn
  have htrace := trace_mono (hdom n)
  rw [ledger_trace] at htrace
  exact hterm.trans htrace

/-- An off-line zero creates a positive trace floor in any eventually covering family. -/
theorem offLine_trace_floor_family (W : ℕ → Finset NontrivialZero)
    (hcover : EventuallyCovered W) (B : ℕ → (ℝ →L[ℝ] ℝ))
    (hdom : ∀ n, (B n - ledger (W n)).IsPositive)
    (rho : NontrivialZero) (hoff : rho.val.re ≠ (1 / 2 : ℝ)) :
    ∃ c : ℝ, 0 < c ∧ ∀ᶠ n in atTop, c ≤ opTrace (B n) := by
  refine ⟨displacement rho ^ 2, ?_, moving_trace_floor_family W hcover B hdom rho⟩
  apply sq_pos_of_ne_zero
  simpa only [displacement, sub_ne_zero] using hoff

/-- Every zero supplies a permanent trace floor as soon as the windows cover it. -/
theorem moving_trace_floor (B : ℕ → (ℝ →L[ℝ] ℝ))
    (hdom : ∀ n, (B n - ledger (canonicalJReflectedWindow n)).IsPositive)
    (rho : NontrivialZero) :
    ∀ᶠ n in atTop, displacement rho ^ 2 ≤ opTrace (B n) := by
  apply (canonicalJReflectedWindow_eventuallyCovered rho).mono
  intro n hn
  have hterm := term_le_window unitWeights (canonicalJReflectedWindow n) rho hn
  have htrace := trace_mono (hdom n)
  rw [ledger_trace] at htrace
  have hterm' : displacement rho ^ 2 ≤ windowEnergy unitWeights (canonicalJReflectedWindow n) := by
    simpa [unitWeights] using hterm
  exact hterm'.trans htrace

/-- An off-line actual zero forces a fixed strictly positive trace floor on all late windows. -/
theorem offLine_trace_floor (B : ℕ → (ℝ →L[ℝ] ℝ))
    (hdom : ∀ n, (B n - ledger (canonicalJReflectedWindow n)).IsPositive)
    (rho : NontrivialZero) (hoff : rho.val.re ≠ (1 / 2 : ℝ)) :
    ∃ c : ℝ, 0 < c ∧ ∀ᶠ n in atTop, c ≤ opTrace (B n) := by
  refine ⟨displacement rho ^ 2, ?_, moving_trace_floor B hdom rho⟩
  apply sq_pos_of_ne_zero
  simpa only [displacement, sub_ne_zero] using hoff

/-- Diagonal concrete domination on arbitrary exhaustive reflected windows is RH-equivalent. -/
theorem movingWindowRecords_iff_riemannHypothesis
    (W : ℕ → Finset NontrivialZero) (hW : ∀ n, JReflectedWindow (W n))
    (hcover : EventuallyCovered W) : MovingWindowRecords W ↔ RiemannHypothesis := by
  constructor
  · rintro ⟨B, hdom, hlim⟩
    apply criticalStripRH_iff_riemannHypothesis.mp
    apply all_zero_fixed_iff_criticalStripRH.mp
    intro rho
    have hle : displacement rho ^ 2 ≤ 0 := le_of_tendsto_of_tendsto
      tendsto_const_nhds hlim (moving_trace_floor_family W hcover B hdom rho)
    have hz : displacement rho = 0 := sq_eq_zero_iff.mp (le_antisymm hle (sq_nonneg _))
    exact (J_zero_fixed_iff rho).mpr (sub_eq_zero.mp hz)
  · intro hRH
    have hzero : ∀ n, ledger (W n) = 0 := by
      intro n
      classical
      obtain ⟨hz, _, _⟩ := finite_converse (windowWeight unitWeights (W n))
        (fun rho => Nat.cast_nonneg _) (windowPsi (W n)) (by
          intro rho _
          have hf := all_zero_fixed_iff_criticalStripRH.mpr
            (criticalStripRH_iff_riemannHypothesis.mpr hRH)
          exact (windowPsi_separates _ (hW n) rho).mpr (Subtype.ext (hf rho.val)))
      exact hz
    refine ⟨fun _ => 0, ?_, ?_⟩
    · intro n
      simp [hzero n]
    · simpa only [map_zero] using (tendsto_const_nhds (x := (0 : ℝ)))

/-- The canonical diagonal source is a specialization of the general window theorem. -/
theorem movingRecords_iff_riemannHypothesis : MovingRecords ↔ RiemannHypothesis :=
  movingWindowRecords_iff_riemannHypothesis canonicalJReflectedWindow
    canonicalJReflectedWindow_reflected canonicalJReflectedWindow_eventuallyCovered

end SixBirdsDualityConfinement.RH.ConcreteZeroWindowDC
