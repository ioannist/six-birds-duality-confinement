import SixBirdsDualityConfinement.DualityConfinement.ConcreteCore
import SixBirdsNeedles.MainCore.PositiveTrace
import SixBirdsNeedles.MainCore.Exhaustion
import Mathlib.Topology.MetricSpace.HausdorffDistance

/-! Concrete self-dual trace confinement on arbitrary complete real Hilbert spaces.
The operator is the norm-Bochner integral of the anti-invariant rank-one field.
Square integrability and a.e. strong measurability are explicit hypotheses;
separation, domination and decay remain explicit application inputs. Neither
ambient separability nor measurability of the involution is assumed. -/
noncomputable section
open MeasureTheory Filter
open scoped InnerProduct InnerProductSpace ENNReal Topology
namespace SixBirdsDualityConfinement.DualityConfinement.ConcreteHilbert
open ConcreteCore
open SixBirdsNeedles.MainCore
open SixBirdsNeedles.XiCore
variable {X Y ι : Type*} [MeasurableSpace X]
  [NormedAddCommGroup Y] [InnerProductSpace ℝ Y] [CompleteSpace Y]

/-- The paper's anti-invariant Hilbert-space ledger. -/
def ledger (μ : Measure X) (S : Y ≃ₗᵢ[ℝ] Y) (ψ : X → Y) : Y →L[ℝ] Y :=
  objectLedger μ (psiMinus S ψ)

/-- Positive trace class is represented by positivity and finite extended trace. -/
def PositiveTraceClass (b : HilbertBasis ι ℝ Y) (A : Y →L[ℝ] Y) : Prop :=
  A.IsPositive ∧ positiveTrace b A < ⊤

/-- The trace-class representation does not depend on the Hilbert basis. -/
theorem positiveTraceClass_basis_iff {κ : Type*} (b : HilbertBasis ι ℝ Y)
    (c : HilbertBasis κ ℝ Y) (A : Y →L[ℝ] Y) :
    PositiveTraceClass b A ↔ PositiveTraceClass c A := by
  constructor
  · rintro ⟨hA, hb⟩
    exact ⟨hA, by simpa only [← positiveTrace_basis_independent b c A hA] using hb⟩
  · rintro ⟨hA, hc⟩
    exact ⟨hA, by simpa only [positiveTrace_basis_independent b c A hA] using hc⟩

omit [CompleteSpace Y] in
/-- A.e. strong measurability of the original readout suffices. -/
theorem psiMinus_aestronglyMeasurable (μ : Measure X) (S : Y ≃ₗᵢ[ℝ] Y)
    (ψ : X → Y) (hψ : AEStronglyMeasurable ψ μ) :
    AEStronglyMeasurable (psiMinus S ψ) μ :=
  (pminus S).continuous.comp_aestronglyMeasurable hψ

/-- L4.3: positivity of the actual norm-Bochner ledger. -/
theorem ledger_positive (μ : Measure X) (S : Y ≃ₗᵢ[ℝ] Y) (ψ : X → Y)
    (hψ : AEStronglyMeasurable ψ μ)
    (hL2 : Integrable (fun x => ‖psiMinus S ψ x‖ ^ 2) μ) :
    (ledger μ S ψ).IsPositive :=
  objectLedger_positive μ _ (psiMinus_aestronglyMeasurable μ S ψ hψ) hL2

/-- L4.3: every matrix coefficient is the corresponding scalar integral. -/
theorem ledger_inner (μ : Measure X) (S : Y ≃ₗᵢ[ℝ] Y) (ψ : X → Y)
    (hψ : AEStronglyMeasurable ψ μ)
    (hL2 : Integrable (fun x => ‖psiMinus S ψ x‖ ^ 2) μ) (h k : Y) :
    ⟪ledger μ S ψ h, k⟫_ℝ =
      ∫ x, ⟪psiMinus S ψ x, h⟫_ℝ * ⟪psiMinus S ψ x, k⟫_ℝ ∂μ := by
  simpa only [ledger, real_inner_comm, mul_comm] using
    objectLedger_inner μ _ (psiMinus_aestronglyMeasurable μ S ψ hψ) hL2 k h

/-- L4.3: the extended trace equals the finite total squared readout energy. -/
theorem ledger_trace (b : HilbertBasis ι ℝ Y) (μ : Measure X)
    (S : Y ≃ₗᵢ[ℝ] Y) (ψ : X → Y) (hψ : AEStronglyMeasurable ψ μ)
    (hL2 : Integrable (fun x => ‖psiMinus S ψ x‖ ^ 2) μ) :
    positiveTrace b (ledger μ S ψ) = ENNReal.ofReal (∫ x, ‖psiMinus S ψ x‖ ^ 2 ∂μ) := by
  rw [ledger, objectLedger_trace b μ _ (psiMinus_aestronglyMeasurable μ S ψ hψ) hL2,
    ← ofReal_integral_eq_lintegral_ofReal hL2 (Eventually.of_forall fun x => sq_nonneg _)]

/-- L4.3: the ledger is positive trace class in every Hilbert basis. -/
theorem ledger_traceClass (b : HilbertBasis ι ℝ Y) (μ : Measure X)
    (S : Y ≃ₗᵢ[ℝ] Y) (ψ : X → Y) (hψ : AEStronglyMeasurable ψ μ)
    (hL2 : Integrable (fun x => ‖psiMinus S ψ x‖ ^ 2) μ) :
    PositiveTraceClass b (ledger μ S ψ) := by
  refine ⟨ledger_positive μ S ψ hψ hL2, ?_⟩
  rw [ledger_trace b μ S ψ hψ hL2]
  exact ENNReal.ofReal_lt_top

/-- T5.1 and T7.1 converse: operator collapse is equivalent to a.e. readout vanishing. -/
theorem ledger_zero_iff (μ : Measure X) (S : Y ≃ₗᵢ[ℝ] Y) (ψ : X → Y)
    (hψ : AEStronglyMeasurable ψ μ)
    (hL2 : Integrable (fun x => ‖psiMinus S ψ x‖ ^ 2) μ) :
    ledger μ S ψ = 0 ↔ ∀ᵐ x ∂μ, psiMinus S ψ x = 0 :=
  objectLedger_zero_iff_general μ _ (psiMinus_aestronglyMeasurable μ S ψ hψ) hL2

/-- T5.1: separation converts zero readout to fixedness for the original measure.
The fixed locus and its complement need not be measurable. -/
theorem separation_confinement (μ : Measure X) (S : Y ≃ₗᵢ[ℝ] Y) (ψ : X → Y)
    (J : X → X) (hψ : AEStronglyMeasurable ψ μ)
    (hL2 : Integrable (fun x => ‖psiMinus S ψ x‖ ^ 2) μ)
    (hsep : ∀ᵐ x ∂μ, psiMinus S ψ x = 0 ↔ J x = x) (hz : ledger μ S ψ = 0) :
    (∀ᵐ x ∂μ, J x = x) ∧ μ {x | J x ≠ x} = 0 := by
  have hr := (ledger_zero_iff μ S ψ hψ hL2).mp hz
  have hfix : ∀ᵐ x ∂μ, J x = x := by
    filter_upwards [hr, hsep] with x hx hs
    exact hs.mp hx
  exact ⟨hfix, ae_iff.mp hfix⟩

/-- T5.1, atom form: a positive-mass singleton sees zero readout pointwise. -/
theorem atom_readout_of_zero (μ : Measure X) (S : Y ≃ₗᵢ[ℝ] Y) (ψ : X → Y)
    (hψ : AEStronglyMeasurable ψ μ)
    (hL2 : Integrable (fun x => ‖psiMinus S ψ x‖ ^ 2) μ)
    (hz : ledger μ S ψ = 0) (x : X) (hx : 0 < μ {x}) : psiMinus S ψ x = 0 := by
  have hr := (ledger_zero_iff μ S ψ hψ hL2).mp hz
  have hn : μ {y | psiMinus S ψ y ≠ 0} = 0 := ae_iff.mp hr
  by_contra h
  have hs : {x} ⊆ {y | psiMinus S ψ y ≠ 0} := by
    intro y hy
    simpa only [Set.mem_singleton_iff.mp hy] using h
  have hle : μ {x} ≤ μ {y | psiMinus S ψ y ≠ 0} := measure_mono hs
  rw [hn] at hle
  exact (not_le_of_gt hx) hle

/-- T5.1, atom form with pointwise qualitative separation. -/
theorem atom_fixed_of_zero (μ : Measure X) (S : Y ≃ₗᵢ[ℝ] Y) (ψ : X → Y)
    (J : X → X) (hψ : AEStronglyMeasurable ψ μ)
    (hL2 : Integrable (fun x => ‖psiMinus S ψ x‖ ^ 2) μ)
    (hz : ledger μ S ψ = 0) (x : X) (hx : 0 < μ {x})
    (hsep : psiMinus S ψ x = 0 ↔ J x = x) : J x = x :=
  hsep.mp (atom_readout_of_zero μ S ψ hψ hL2 hz x hx)

/-- T5.2: outer-measure confinement on an arbitrary threshold set.
The estimate is valid for every extended-real threshold, including zero. -/
theorem quantitative_threshold (b : HilbertBasis ι ℝ Y) (μ : Measure X)
    (S : Y ≃ₗᵢ[ℝ] Y) (ψ : X → Y) (hψ : AEStronglyMeasurable ψ μ)
    (hL2 : Integrable (fun x => ‖psiMinus S ψ x‖ ^ 2) μ)
    (δ : X → ℝ≥0∞) (ε : ℝ≥0∞) {m : ℝ} (hm : 0 < m)
    (hsep : ∀ x, ε ≤ δ x → m ≤ ‖psiMinus S ψ x‖) :
    μ {x | ε ≤ δ x} ≤ positiveTrace b (ledger μ S ψ) / ENNReal.ofReal (m ^ 2) :=
  quantitative_confinement b μ _ (psiMinus_aestronglyMeasurable μ S ψ hψ) hL2
    {x | ε ≤ δ x} hm hsep

/-- T5.2: distance-to-fixed-locus instance, with distance infinity to an empty locus.
No Borel compatibility, measurability or nonemptiness of the fixed locus is needed. -/
theorem quantitative_distance [MetricSpace X] (b : HilbertBasis ι ℝ Y)
    (μ : Measure X) (S : Y ≃ₗᵢ[ℝ] Y) (ψ : X → Y) (J : X → X)
    (hψ : AEStronglyMeasurable ψ μ)
    (hL2 : Integrable (fun x => ‖psiMinus S ψ x‖ ^ 2) μ)
    (ε : ℝ≥0∞) {m : ℝ} (hm : 0 < m)
    (hsep : ∀ x, ε ≤ Metric.infEDist x {y | J y = y} → m ≤ ‖psiMinus S ψ x‖) :
    μ {x | ε ≤ Metric.infEDist x {y | J y = y}} ≤
      positiveTrace b (ledger μ S ψ) / ENNReal.ofReal (m ^ 2) :=
  quantitative_threshold b μ S ψ hψ hL2 _ ε hm hsep

/-- T6.2: Douglas factorization on complete real Hilbert spaces, including nonclosed ranges. -/
theorem douglas_factorization {H K₁ K₂ : Type*}
    [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
    [NormedAddCommGroup K₁] [InnerProductSpace ℝ K₁] [CompleteSpace K₁]
    [NormedAddCommGroup K₂] [InnerProductSpace ℝ K₂] [CompleteSpace K₂]
    (V : H →L[ℝ] K₁) (W : H →L[ℝ] K₂) :
    Loewner (V.adjoint ∘L V) (W.adjoint ∘L W) ↔
      ∃ T : K₂ →L[ℝ] K₁, ‖T‖ ≤ 1 ∧ V = T ∘L W :=
  douglas_domination V W

omit [CompleteSpace Y] in
/-- Positive bounded operators are nonnegative in the paper's quadratic order. -/
theorem positive_loewner_zero {A : Y →L[ℝ] Y} (hA : A.IsPositive) : Loewner 0 A := by
  intro y
  simpa only [ContinuousLinearMap.zero_apply, inner_zero_right, map_zero] using
    hA.re_inner_nonneg_right y

/-- T7.1: vanishing positive-trace domination collapses the actual fixed ledger. -/
theorem ledger_master (b : HilbertBasis ι ℝ Y) (μ : Measure X)
    (S : Y ≃ₗᵢ[ℝ] Y) (ψ : X → Y) (hψ : AEStronglyMeasurable ψ μ)
    (hL2 : Integrable (fun x => ‖psiMinus S ψ x‖ ^ 2) μ)
    (B : ℕ → Y →L[ℝ] Y) (_hB : ∀ n, (B n).IsPositive)
    (hdom : ∀ n, Loewner (ledger μ S ψ) (B n))
    (hlim : Tendsto (fun n => positiveTrace b (B n)) atTop (𝓝 0)) :
    ledger μ S ψ = 0 ∧ (∀ᵐ x ∂μ, psiMinus S ψ x = 0) := by
  have hz := ledger_squeeze b μ _ (psiMinus_aestronglyMeasurable μ S ψ hψ) hL2 B hdom hlim
  exact ⟨hz, (ledger_zero_iff μ S ψ hψ hL2).mp hz⟩

/-- T7.1 with a.e. qualitative separation, retaining all fixed-ledger conclusions. -/
theorem ledger_master_fixed (b : HilbertBasis ι ℝ Y) (μ : Measure X)
    (S : Y ≃ₗᵢ[ℝ] Y) (ψ : X → Y) (J : X → X) (hψ : AEStronglyMeasurable ψ μ)
    (hL2 : Integrable (fun x => ‖psiMinus S ψ x‖ ^ 2) μ)
    (hsep : ∀ᵐ x ∂μ, psiMinus S ψ x = 0 ↔ J x = x)
    (B : ℕ → Y →L[ℝ] Y) (hB : ∀ n, (B n).IsPositive)
    (hdom : ∀ n, Loewner (ledger μ S ψ) (B n))
    (hlim : Tendsto (fun n => positiveTrace b (B n)) atTop (𝓝 0)) :
    ledger μ S ψ = 0 ∧ (∀ᵐ x ∂μ, psiMinus S ψ x = 0) ∧
      (∀ᵐ x ∂μ, J x = x) ∧ μ {x | J x ≠ x} = 0 := by
  obtain ⟨hz, hr⟩ := ledger_master b μ S ψ hψ hL2 B hB hdom hlim
  exact ⟨hz, hr, separation_confinement μ S ψ J hψ hL2 hsep hz⟩

omit [CompleteSpace Y] in
/-- T7.1 converse needs no integrability or measurability hypotheses. -/
theorem ledger_zero_of_ae (μ : Measure X) (S : Y ≃ₗᵢ[ℝ] Y) (ψ : X → Y)
    (hz : ∀ᵐ x ∂μ, psiMinus S ψ x = 0) : ledger μ S ψ = 0 := by
  unfold ledger objectLedger
  calc
    _ = ∫ _x : X, (0 : Y →L[ℝ] Y) ∂μ := by
      apply integral_congr_ae
      filter_upwards [hz] with x hx
      exact InnerProductSpace.rankOne_eq_zero.mpr (Or.inl hx)
    _ = 0 := integral_zero _ _

omit [CompleteSpace Y] in
/-- The explicit zero budget satisfies positivity, quadratic domination and trace decay. -/
theorem zero_budget_records (b : HilbertBasis ι ℝ Y) (μ : Measure X)
    (S : Y ≃ₗᵢ[ℝ] Y) (ψ : X → Y) (hz : ledger μ S ψ = 0) :
    (∀ _n : ℕ, (0 : Y →L[ℝ] Y).IsPositive ∧ Loewner (ledger μ S ψ) 0) ∧
      Tendsto (fun _ : ℕ => positiveTrace b (0 : Y →L[ℝ] Y)) atTop (𝓝 0) := by
  refine ⟨fun _ => ⟨ContinuousLinearMap.isPositive_zero, ?_⟩, ?_⟩
  · rw [hz]
    exact fun _ => le_rfl
  · simp [positiveTrace]

/-- T7.1 and its converse characterize the existence of positive vanishing budget records. -/
theorem ledger_records_iff (b : HilbertBasis ι ℝ Y) (μ : Measure X)
    (S : Y ≃ₗᵢ[ℝ] Y) (ψ : X → Y) (hψ : AEStronglyMeasurable ψ μ)
    (hL2 : Integrable (fun x => ‖psiMinus S ψ x‖ ^ 2) μ) :
    (∃ B : ℕ → Y →L[ℝ] Y, (∀ n, (B n).IsPositive) ∧
      (∀ n, Loewner (ledger μ S ψ) (B n)) ∧
      Tendsto (fun n => positiveTrace b (B n)) atTop (𝓝 0)) ↔
      ∀ᵐ x ∂μ, psiMinus S ψ x = 0 := by
  constructor
  · rintro ⟨B, hB, hdom, hlim⟩
    exact (ledger_master b μ S ψ hψ hL2 B hB hdom hlim).2
  · intro hr
    have hz := ledger_zero_of_ae μ S ψ hr
    obtain ⟨hrecords, hlim⟩ := zero_budget_records b μ S ψ hz
    exact ⟨fun _ => 0, fun n => (hrecords n).1, fun n => (hrecords n).2, hlim⟩

omit [CompleteSpace Y] in
/-- Equivariance annihilates the anti-invariant readout on a.e. fixed points. -/
theorem psiMinus_zero_of_ae_fixed (μ : Measure X) (J : X → X) (S : Y ≃ₗᵢ[ℝ] Y)
    (hS : Function.Involutive S) (ψ : X → Y) (heq : ∀ x, ψ (J x) = S (ψ x))
    (hfix : ∀ᵐ x ∂μ, J x = x) : ∀ᵐ x ∂μ, psiMinus S ψ x = 0 := by
  filter_upwards [hfix] with x hx
  exact psiMinus_fixed J S hS ψ heq hx

omit [CompleteSpace Y] in
/-- T7.1 fixed-locus converse, without any measurability assumption on J. -/
theorem ledger_zero_of_ae_fixed (μ : Measure X) (J : X → X) (S : Y ≃ₗᵢ[ℝ] Y)
    (hS : Function.Involutive S) (ψ : X → Y) (heq : ∀ x, ψ (J x) = S (ψ x))
    (hfix : ∀ᵐ x ∂μ, J x = x) : ledger μ S ψ = 0 :=
  ledger_zero_of_ae μ S ψ (psiMinus_zero_of_ae_fixed μ J S hS ψ heq hfix)

/-- T8.2: ambient exhaustion with bounded inclusions and explicit positive tails.
No bases in the moving spaces, finite-dimensionality or isometry of iota are needed. -/
theorem ledger_exhaustive {Yn : ℕ → Type*}
    [∀ n, NormedAddCommGroup (Yn n)] [∀ n, InnerProductSpace ℝ (Yn n)]
    [∀ n, CompleteSpace (Yn n)] (b : HilbertBasis ι ℝ Y) (μ : Measure X)
    (S : Y ≃ₗᵢ[ℝ] Y) (ψ : X → Y) (hψ : AEStronglyMeasurable ψ μ)
    (hL2 : Integrable (fun x => ‖psiMinus S ψ x‖ ^ 2) μ)
    (A B : ∀ n, Yn n →L[ℝ] Yn n) (iota : ∀ n, Yn n →L[ℝ] Y)
    (T : ℕ → Y →L[ℝ] Y) (_hA : ∀ n, (A n).IsPositive)
    (hB : ∀ n, (B n).IsPositive) (hT : ∀ n, (T n).IsPositive)
    (hstage : ∀ n, Loewner (A n) (B n))
    (hexhaust : ∀ n, Loewner (ledger μ S ψ) (iota n ∘L A n ∘L (iota n).adjoint + T n))
    (hlim : Tendsto (fun n => positiveTrace b (iota n ∘L B n ∘L (iota n).adjoint) +
      positiveTrace b (T n)) atTop (𝓝 0)) :
    ledger μ S ψ = 0 ∧ (∀ᵐ x ∂μ, psiMinus S ψ x = 0) := by
  have hz := exhaustive_ledger_squeeze b μ _ (psiMinus_aestronglyMeasurable μ S ψ hψ)
    hL2 A B iota T (fun n => positive_loewner_zero (hB n))
    (fun n => positive_loewner_zero (hT n)) hstage hexhaust hlim
  exact ⟨hz, (ledger_zero_iff μ S ψ hψ hL2).mp hz⟩

/-- T8.2 with qualitative separation, on the original object measure. -/
theorem ledger_exhaustive_fixed {Yn : ℕ → Type*}
    [∀ n, NormedAddCommGroup (Yn n)] [∀ n, InnerProductSpace ℝ (Yn n)]
    [∀ n, CompleteSpace (Yn n)] (b : HilbertBasis ι ℝ Y) (μ : Measure X)
    (S : Y ≃ₗᵢ[ℝ] Y) (ψ : X → Y) (J : X → X) (hψ : AEStronglyMeasurable ψ μ)
    (hL2 : Integrable (fun x => ‖psiMinus S ψ x‖ ^ 2) μ)
    (hsep : ∀ᵐ x ∂μ, psiMinus S ψ x = 0 ↔ J x = x)
    (A B : ∀ n, Yn n →L[ℝ] Yn n) (iota : ∀ n, Yn n →L[ℝ] Y)
    (T : ℕ → Y →L[ℝ] Y) (hA : ∀ n, (A n).IsPositive)
    (hB : ∀ n, (B n).IsPositive) (hT : ∀ n, (T n).IsPositive)
    (hstage : ∀ n, Loewner (A n) (B n))
    (hexhaust : ∀ n, Loewner (ledger μ S ψ) (iota n ∘L A n ∘L (iota n).adjoint + T n))
    (hlim : Tendsto (fun n => positiveTrace b (iota n ∘L B n ∘L (iota n).adjoint) +
      positiveTrace b (T n)) atTop (𝓝 0)) :
    ledger μ S ψ = 0 ∧ (∀ᵐ x ∂μ, psiMinus S ψ x = 0) ∧
      (∀ᵐ x ∂μ, J x = x) ∧ μ {x | J x ≠ x} = 0 := by
  obtain ⟨hz, hr⟩ := ledger_exhaustive b μ S ψ hψ hL2 A B iota T hA hB hT hstage hexhaust hlim
  exact ⟨hz, hr, separation_confinement μ S ψ J hψ hL2 hsep hz⟩

omit [CompleteSpace Y] in
/-- Finite positive traces remain finite under source/error addition. -/
theorem positiveTrace_sum_ne_top (b : HilbertBasis ι ℝ Y) (K Es : Y →L[ℝ] Y)
    (hK : PositiveTraceClass b K) (hEs : PositiveTraceClass b Es) :
    positiveTrace b (K + Es) ≠ ⊤ := by
  rw [positiveTrace_add b K Es (positive_loewner_zero hK.1) (positive_loewner_zero hEs.1)]
  exact ENNReal.add_ne_top.mpr ⟨hK.2.ne, hEs.2.ne⟩

/-- P8.4: scalar optimization, including non-attained zero-component endpoints. -/
theorem scalar_budget_infimum {a b : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b) :
    sInf (Set.range (fun t : {t : ℝ // 0 < t} => (1 + (t : ℝ)) * a + (1 + (t : ℝ)⁻¹) * b)) =
      (Real.sqrt a + Real.sqrt b) ^ 2 :=
  optimized_trace_infimum ha hb

omit [CompleteSpace Y] in
/-- P8.4: the infimum is taken over the traces of the actual operator budgets. -/
theorem optimized_budget_infimum (b : HilbertBasis ι ℝ Y) (K Es Eb : Y →L[ℝ] Y)
    (hK : PositiveTraceClass b K) (hEs : PositiveTraceClass b Es)
    (hEb : PositiveTraceClass b Eb) :
    sInf (Set.range (fun t : {t : ℝ // 0 < t} =>
      (positiveTrace b ((1 + (t : ℝ)) • (K + Es) + (1 + (t : ℝ)⁻¹) • Eb)).toReal)) =
      (Real.sqrt (positiveTrace b (K + Es)).toReal +
        Real.sqrt (positiveTrace b Eb).toReal) ^ 2 :=
  optimized_operator_trace b (K + Es) Eb (positive_loewner_zero (hK.1.add hEs.1))
    (positive_loewner_zero hEb.1) ENNReal.toReal_nonneg ENNReal.toReal_nonneg
    (ENNReal.ofReal_toReal (positiveTrace_sum_ne_top b K Es hK hEs)).symm
    (ENNReal.ofReal_toReal hEb.2.ne).symm

/-- P8.4: all positive scalar splits imply the sharp optimized trace bound.
The finite-trace hypotheses precede every use of toReal. -/
theorem ledger_optimized_budget (b : HilbertBasis ι ℝ Y) (μ : Measure X)
    (S : Y ≃ₗᵢ[ℝ] Y) (ψ : X → Y) (hψ : AEStronglyMeasurable ψ μ)
    (hL2 : Integrable (fun x => ‖psiMinus S ψ x‖ ^ 2) μ)
    (K Es Eb : Y →L[ℝ] Y) (hK : PositiveTraceClass b K)
    (hEs : PositiveTraceClass b Es) (hEb : PositiveTraceClass b Eb)
    (hdom : ∀ t : ℝ, 0 < t →
      Loewner (ledger μ S ψ) ((1 + t) • (K + Es) + (1 + t⁻¹) • Eb)) :
    positiveTrace b (ledger μ S ψ) ≤ ENNReal.ofReal
      ((Real.sqrt (positiveTrace b (K + Es)).toReal + Real.sqrt (positiveTrace b Eb).toReal) ^ 2) ∧
    (positiveTrace b (ledger μ S ψ)).toReal ≤
      (Real.sqrt (positiveTrace b (K + Es)).toReal + Real.sqrt (positiveTrace b Eb).toReal) ^ 2 := by
  have hreal : (positiveTrace b (ledger μ S ψ)).toReal ≤
      (Real.sqrt (positiveTrace b (K + Es)).toReal + Real.sqrt (positiveTrace b Eb).toReal) ^ 2 := by
    rw [← optimized_budget_infimum b K Es Eb hK hEs hEb]
    apply le_csInf (Set.range_nonempty _)
    rintro u ⟨t, rfl⟩
    have htrace := youngBudget_trace_real b (K + Es) Eb
      (positive_loewner_zero (hK.1.add hEs.1)) (positive_loewner_zero hEb.1)
      ENNReal.toReal_nonneg ENNReal.toReal_nonneg
      (ENNReal.ofReal_toReal (positiveTrace_sum_ne_top b K Es hK hEs)).symm
      (ENNReal.ofReal_toReal hEb.2.ne).symm t.property
    have hfinite : positiveTrace b (youngBudget (K + Es) Eb t) ≠ ⊤ := by
      rw [htrace]
      exact ENNReal.ofReal_ne_top
    exact ENNReal.toReal_mono hfinite (positiveTrace_mono b (hdom t t.property))
  refine ⟨?_, hreal⟩
  calc
    positiveTrace b (ledger μ S ψ) = ENNReal.ofReal (positiveTrace b (ledger μ S ψ)).toReal :=
      (ENNReal.ofReal_toReal (ledger_traceClass b μ S ψ hψ hL2).2.ne).symm
    _ ≤ _ := ENNReal.ofReal_le_ofReal hreal

/-- P8.4, sequence form: vanishing source and bridge trace budgets eliminate the ledger. -/
theorem ledger_budget_sequence (b : HilbertBasis ι ℝ Y) (μ : Measure X)
    (S : Y ≃ₗᵢ[ℝ] Y) (ψ : X → Y) (hψ : AEStronglyMeasurable ψ μ)
    (hL2 : Integrable (fun x => ‖psiMinus S ψ x‖ ^ 2) μ)
    (K Es Eb : ℕ → Y →L[ℝ] Y) (hK : ∀ n, PositiveTraceClass b (K n))
    (hEs : ∀ n, PositiveTraceClass b (Es n)) (hEb : ∀ n, PositiveTraceClass b (Eb n))
    (hdom : ∀ (n : ℕ) (t : ℝ), 0 < t → Loewner (ledger μ S ψ)
      ((1 + t) • (K n + Es n) + (1 + t⁻¹) • Eb n))
    (ha : Tendsto (fun n => (positiveTrace b (K n + Es n)).toReal) atTop (𝓝 0))
    (hb : Tendsto (fun n => (positiveTrace b (Eb n)).toReal) atTop (𝓝 0)) :
    ledger μ S ψ = 0 ∧ (∀ᵐ x ∂μ, psiMinus S ψ x = 0) := by
  have hlim := optimized_trace_tendsto_zero _ _ ha hb
  have hbound (n : ℕ) := (ledger_optimized_budget b μ S ψ hψ hL2
    (K n) (Es n) (Eb n) (hK n) (hEs n) (hEb n) (hdom n)).2
  have hzreal : (positiveTrace b (ledger μ S ψ)).toReal = 0 :=
    le_antisymm (ge_of_tendsto hlim (Eventually.of_forall hbound)) ENNReal.toReal_nonneg
  have hztrace : positiveTrace b (ledger μ S ψ) = 0 := by
    rw [← ENNReal.ofReal_toReal (ledger_traceClass b μ S ψ hψ hL2).2.ne, hzreal,
      ENNReal.ofReal_zero]
  have hz := (positiveTrace_zero_iff b _ (ledger_positive μ S ψ hψ hL2)).mp hztrace
  exact ⟨hz, (ledger_zero_iff μ S ψ hψ hL2).mp hz⟩

/-- P8.4, sequence form with a.e. separation: the original measure is confined. -/
theorem ledger_budget_sequence_fixed (b : HilbertBasis ι ℝ Y) (μ : Measure X)
    (S : Y ≃ₗᵢ[ℝ] Y) (ψ : X → Y) (J : X → X) (hψ : AEStronglyMeasurable ψ μ)
    (hL2 : Integrable (fun x => ‖psiMinus S ψ x‖ ^ 2) μ)
    (hsep : ∀ᵐ x ∂μ, psiMinus S ψ x = 0 ↔ J x = x)
    (K Es Eb : ℕ → Y →L[ℝ] Y) (hK : ∀ n, PositiveTraceClass b (K n))
    (hEs : ∀ n, PositiveTraceClass b (Es n)) (hEb : ∀ n, PositiveTraceClass b (Eb n))
    (hdom : ∀ (n : ℕ) (t : ℝ), 0 < t → Loewner (ledger μ S ψ)
      ((1 + t) • (K n + Es n) + (1 + t⁻¹) • Eb n))
    (ha : Tendsto (fun n => (positiveTrace b (K n + Es n)).toReal) atTop (𝓝 0))
    (hb : Tendsto (fun n => (positiveTrace b (Eb n)).toReal) atTop (𝓝 0)) :
    ledger μ S ψ = 0 ∧ (∀ᵐ x ∂μ, psiMinus S ψ x = 0) ∧
      (∀ᵐ x ∂μ, J x = x) ∧ μ {x | J x ≠ x} = 0 := by
  obtain ⟨hz, hr⟩ := ledger_budget_sequence b μ S ψ hψ hL2 K Es Eb hK hEs hEb hdom ha hb
  exact ⟨hz, hr, separation_confinement μ S ψ J hψ hL2 hsep hz⟩

end SixBirdsDualityConfinement.DualityConfinement.ConcreteHilbert
