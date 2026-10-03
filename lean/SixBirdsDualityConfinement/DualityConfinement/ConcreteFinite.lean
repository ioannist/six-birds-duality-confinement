import SixBirdsDualityConfinement.DualityConfinement.ConcreteCore

/-! Finite positive weighted ledgers. Use `r = psiMinus S psi` for SDTC. -/
namespace SixBirdsDualityConfinement.DualityConfinement.ConcreteFinite
open Filter InnerProductSpace
open SixBirdsDualityConfinement.DualityConfinement.ConcreteCore
open scoped Topology
variable {X Y : Type*} [Fintype X] [NormedAddCommGroup Y]
  [InnerProductSpace ℝ Y] [FiniteDimensional ℝ Y]

/-- The finite weighted squared ledger. -/
noncomputable def finiteLedger (mu : X → ℝ) (r : X → Y) : Y →L[ℝ] Y :=
  ∑ x, mu x • rankOne ℝ (r x) (r x)

omit [FiniteDimensional ℝ Y] in
/-- Every matrix coefficient of the finite ledger is its weighted Gram sum. -/
theorem finiteLedger_coefficient (mu : X → ℝ) (r : X → Y) (h k : Y) :
    inner ℝ (finiteLedger mu r h) k =
      ∑ x, mu x * (inner ℝ (r x) h * inner ℝ (r x) k) := by
  classical
  simp [finiteLedger, rankOne_apply, sum_inner, real_inner_smul_left]

omit [FiniteDimensional ℝ Y] in
theorem finiteLedger_positive (mu : X → ℝ) (hmu : ∀ x, 0 ≤ mu x) (r : X → Y) :
    (finiteLedger mu r).IsPositive := by
  apply ContinuousLinearMap.isPositive_sum
  intro x _
  exact (isPositive_rankOne_self (r x)).smul_of_nonneg (hmu x)

theorem finiteLedger_trace (mu : X → ℝ) (r : X → Y) :
    opTrace (finiteLedger mu r) = ∑ x, mu x * ‖r x‖ ^ 2 := by
  simp [finiteLedger]

theorem finiteLedger_visible_zero (mu : X → ℝ) (hmu : ∀ x, 0 ≤ mu x) (r : X → Y)
    (hz : finiteLedger mu r = 0) {x : X} (hx : 0 < mu x) : r x = 0 := by
  have hs : ∑ x, mu x * ‖r x‖ ^ 2 = 0 := by
    rw [← finiteLedger_trace, hz, map_zero]
  have ht := (Finset.sum_eq_zero_iff_of_nonneg
    (fun x (_ : x ∈ Finset.univ) => mul_nonneg (hmu x) (sq_nonneg ‖r x‖))).mp hs
  have hh : ‖r x‖ ^ 2 = 0 := (mul_eq_zero.mp (ht x (Finset.mem_univ x))).resolve_left hx.ne'
  exact norm_eq_zero.mp (sq_eq_zero_iff.mp hh)

/-- Operator collapse and vanishing on the visible support. -/
theorem finite_master (mu : X → ℝ) (hmu : ∀ x, 0 ≤ mu x) (r : X → Y)
    (B : ℕ → Y →L[ℝ] Y)
    (hdom : ∀ n, (B n - finiteLedger mu r).IsPositive)
    (hlim : Tendsto (fun n => opTrace (B n)) atTop (𝓝 0)) :
    finiteLedger mu r = 0 ∧ ∀ x, 0 < mu x → r x = 0 := by
  have hz := cone_squeeze (finiteLedger_positive mu hmu r) B hdom hlim
  exact ⟨hz, fun _ hx => finiteLedger_visible_zero mu hmu r hz hx⟩

/-- Fixedness only uses separation where the weights are positive. -/
theorem finite_fixed_of_zero (mu : X → ℝ) (hmu : ∀ x, 0 ≤ mu x) (r : X → Y)
    (J : X → X) (hsep : ∀ x, 0 < mu x → (r x = 0 ↔ J x = x))
    (hz : finiteLedger mu r = 0) : ∀ x, 0 < mu x → J x = x := by
  intro x hx
  exact (hsep x hx).mp (finiteLedger_visible_zero mu hmu r hz hx)

/-- Mass outside the fixed locus, including invisible points of zero weight. -/
theorem finite_nonfixed_mass [DecidableEq X] (mu : X → ℝ) (hmu : ∀ x, 0 ≤ mu x)
    (J : X → X) (hfixed : ∀ x, 0 < mu x → J x = x) :
    ∑ x ∈ Finset.univ.filter (fun x => J x ≠ x), mu x = 0 := by
  apply Finset.sum_eq_zero
  intro x hx
  have hn := (Finset.mem_filter.mp hx).2
  exact le_antisymm (le_of_not_gt fun hp => hn (hfixed x hp)) (hmu x)

theorem finite_master_fixed [DecidableEq X] (mu : X → ℝ) (hmu : ∀ x, 0 ≤ mu x)
    (r : X → Y) (J : X → X) (hsep : ∀ x, 0 < mu x → (r x = 0 ↔ J x = x))
    (B : ℕ → Y →L[ℝ] Y)
    (hdom : ∀ n, (B n - finiteLedger mu r).IsPositive)
    (hlim : Tendsto (fun n => opTrace (B n)) atTop (𝓝 0)) :
    finiteLedger mu r = 0 ∧ (∀ x, 0 < mu x → r x = 0) ∧
      (∀ x, 0 < mu x → J x = x) ∧
      ∑ x ∈ Finset.univ.filter (fun x => J x ≠ x), mu x = 0 := by
  obtain ⟨hz, hr⟩ := finite_master mu hmu r B hdom hlim
  have hf := finite_fixed_of_zero mu hmu r J hsep hz
  exact ⟨hz, hr, hf, finite_nonfixed_mass mu hmu J hf⟩

/-- Finite Markov estimate on any selected set. -/
theorem finite_quantitative (mu : X → ℝ) (hmu : ∀ x, 0 ≤ mu x)
    (r : X → Y) (s : Finset X) {m : ℝ} (hm : 0 < m)
    (hlower : ∀ x ∈ s, m ≤ ‖r x‖) :
    ∑ x ∈ s, mu x ≤ opTrace (finiteLedger mu r) / m ^ 2 := by
  apply (le_div_iff₀ (sq_pos_of_pos hm)).mpr
  calc
    (∑ x ∈ s, mu x) * m ^ 2 = ∑ x ∈ s, mu x * m ^ 2 := Finset.sum_mul _ _ _
    _ ≤ ∑ x ∈ s, mu x * ‖r x‖ ^ 2 := by
      apply Finset.sum_le_sum
      intro x hx
      exact mul_le_mul_of_nonneg_left (sq_le_sq₀ hm.le (norm_nonneg _) |>.mpr (hlower x hx)) (hmu x)
    _ ≤ ∑ x, mu x * ‖r x‖ ^ 2 := by
      apply Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ s)
      intro x _ _
      exact mul_nonneg (hmu x) (sq_nonneg _)
    _ = opTrace (finiteLedger mu r) := (finiteLedger_trace mu r).symm

/-- Threshold version; no positivity of `eps` is needed for this estimate. -/
theorem finite_quantitative_threshold (mu : X → ℝ) (hmu : ∀ x, 0 ≤ mu x)
    (r : X → Y) (d : X → ℝ) (eps : ℝ) {m : ℝ} (hm : 0 < m)
    (hlower : ∀ x, eps ≤ d x → m ≤ ‖r x‖) :
    ∑ x ∈ Finset.univ.filter (fun x => eps ≤ d x), mu x ≤
      opTrace (finiteLedger mu r) / m ^ 2 := by
  classical
  exact finite_quantitative mu hmu r _ hm (fun x hx => hlower x (Finset.mem_filter.mp hx).2)

/-- Exhaustive squeeze, followed by all finite fixedness and mass consequences. -/
theorem finite_exhaustive_fixed [DecidableEq X] (mu : X → ℝ) (hmu : ∀ x, 0 ≤ mu x)
    (r : X → Y) (J : X → X) (hsep : ∀ x, 0 < mu x → (r x = 0 ↔ J x = x))
    {Z : ℕ → Type*} [∀ n, NormedAddCommGroup (Z n)]
    [∀ n, InnerProductSpace ℝ (Z n)] [∀ n, FiniteDimensional ℝ (Z n)]
    (iota : ∀ n, Z n →L[ℝ] Y) (A B : ∀ n, Z n →L[ℝ] Z n) (T : ℕ → Y →L[ℝ] Y)
    (hdom : ∀ n, (B n - A n).IsPositive)
    (hex : ∀ n, ((iota n).comp ((A n).comp (iota n).adjoint) + T n - finiteLedger mu r).IsPositive)
    (hlim : Tendsto (fun n => opTrace ((iota n).comp ((B n).comp (iota n).adjoint)) +
      opTrace (T n)) atTop (𝓝 0)) :
    finiteLedger mu r = 0 ∧ (∀ x, 0 < mu x → r x = 0) ∧
      (∀ x, 0 < mu x → J x = x) ∧
      ∑ x ∈ Finset.univ.filter (fun x => J x ≠ x), mu x = 0 := by
  have hz := exhaustive_squeeze (finiteLedger_positive mu hmu r) iota A B T hdom hex hlim
  have hf := finite_fixed_of_zero mu hmu r J hsep hz
  exact ⟨hz, fun _ hx => finiteLedger_visible_zero mu hmu r hz hx, hf,
    finite_nonfixed_mass mu hmu J hf⟩

end SixBirdsDualityConfinement.DualityConfinement.ConcreteFinite
