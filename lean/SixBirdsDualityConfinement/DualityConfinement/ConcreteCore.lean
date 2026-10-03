import Mathlib.Analysis.InnerProductSpace.Positive
import Mathlib.Analysis.InnerProductSpace.Trace
import Mathlib.Topology.Order.OrderClosed
import Mathlib.Tactic

/-! Concrete real Hilbert-space operators underlying self-dual trace confinement. -/
namespace SixBirdsDualityConfinement.DualityConfinement.ConcreteCore
open Filter InnerProductSpace
open scoped Topology
variable {Y : Type*} [NormedAddCommGroup Y] [InnerProductSpace ℝ Y]

/-- Anti-invariant projection of an isometric involution. -/
noncomputable def pminus (S : Y ≃ₗᵢ[ℝ] Y) : Y →L[ℝ] Y :=
  (1 / 2 : ℝ) • (ContinuousLinearMap.id ℝ Y - S.toContinuousLinearEquiv.toContinuousLinearMap)

@[simp] theorem pminus_apply (S : Y ≃ₗᵢ[ℝ] Y) (v : Y) :
    pminus S v = (1 / 2 : ℝ) • (v - S v) := rfl

theorem pminus_anti (S : Y ≃ₗᵢ[ℝ] Y) (hS : Function.Involutive S) (v : Y) :
    S (pminus S v) = -pminus S v := by
  simp only [pminus_apply, map_smul, map_sub, hS v]
  rw [← neg_sub, smul_neg]

theorem pminus_eq_self (S : Y ≃ₗᵢ[ℝ] Y) {v : Y} (hv : S v = -v) :
    pminus S v = v := by
  simp only [pminus_apply, hv, sub_neg_eq_add, ← two_smul ℝ v, smul_smul]
  norm_num

theorem pminus_idempotent (S : Y ≃ₗᵢ[ℝ] Y) (hS : Function.Involutive S) :
    (pminus S).comp (pminus S) = pminus S := by
  ext v
  exact pminus_eq_self S (pminus_anti S hS v)

theorem pminus_range (S : Y ≃ₗᵢ[ℝ] Y) (hS : Function.Involutive S) (v : Y) :
    v ∈ LinearMap.range (pminus S).toLinearMap ↔ S v = -v := by
  constructor
  · rintro ⟨w, rfl⟩
    exact pminus_anti S hS w
  · intro hv
    exact ⟨v, pminus_eq_self S hv⟩

theorem pminus_symmetric (S : Y ≃ₗᵢ[ℝ] Y) (hS : Function.Involutive S) :
    (pminus S).IsSymmetric := by
  intro v w
  change inner ℝ (pminus S v) w = inner ℝ v (pminus S w)
  have hs : inner ℝ (S v) w = inner ℝ v (S w) := by
    simpa only [hS w] using S.inner_map_map v (S w)
  simp only [pminus_apply, real_inner_smul_left, real_inner_smul_right,
    inner_sub_left, inner_sub_right, hs]

/-- The residual is orthogonal to the entire anti-invariant eigenspace. -/
theorem pminus_orthogonal (S : Y ≃ₗᵢ[ℝ] Y) (hS : Function.Involutive S)
    (v w : Y) (hw : S w = -w) : inner ℝ (v - pminus S v) w = 0 := by
  have hs : inner ℝ (pminus S v) w = inner ℝ v (pminus S w) :=
    pminus_symmetric S hS v w
  rw [inner_sub_left, hs, pminus_eq_self S hw, sub_self]

theorem pminus_selfAdjoint [CompleteSpace Y] (S : Y ≃ₗᵢ[ℝ] Y)
    (hS : Function.Involutive S) : IsSelfAdjoint (pminus S) :=
  ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mpr (pminus_symmetric S hS)

/-- The actual anti-invariant readout, with no separation built into it. -/
noncomputable def psiMinus {X : Type*} (S : Y ≃ₗᵢ[ℝ] Y) (psi : X → Y) : X → Y :=
  fun x => pminus S (psi x)

theorem psiMinus_equivariant {X : Type*} (J : X → X) (S : Y ≃ₗᵢ[ℝ] Y)
    (hS : Function.Involutive S) (psi : X → Y) (heq : ∀ x, psi (J x) = S (psi x))
    (x : X) : psiMinus S psi (J x) = -psiMinus S psi x := by
  simp only [psiMinus, pminus_apply, heq, hS (psi x)]
  rw [← neg_sub, smul_neg]

theorem psiMinus_fixed {X : Type*} (J : X → X) (S : Y ≃ₗᵢ[ℝ] Y)
    (hS : Function.Involutive S) (psi : X → Y) (heq : ∀ x, psi (J x) = S (psi x))
    {x : X} (hx : J x = x) : psiMinus S psi x = 0 := by
  have h := psiMinus_equivariant J S hS psi heq x
  rw [hx] at h
  have hh : (2 : ℝ) • psiMinus S psi x = 0 := by
    rw [two_smul]
    exact eq_neg_iff_add_eq_zero.mp h
  exact (smul_eq_zero.mp hh).resolve_left (by norm_num)

variable [FiniteDimensional ℝ Y]

/-- Ordinary linear trace as a linear functional on continuous operators. -/
noncomputable def opTrace : (Y →L[ℝ] Y) →ₗ[ℝ] ℝ :=
  (LinearMap.trace ℝ Y).comp (ContinuousLinearMap.coeLM ℝ)

@[simp] theorem opTrace_rankOne (v : Y) :
    opTrace (rankOne ℝ v v) = ‖v‖ ^ 2 := by
  exact (trace_rankOne v v).trans (real_inner_self_eq_norm_sq v)

theorem positive_trace_nonneg {T : Y →L[ℝ] Y} (hT : T.IsPositive) :
    0 ≤ opTrace T := by
  obtain ⟨m, u, rfl⟩ := ContinuousLinearMap.isPositive_iff_eq_sum_rankOne.mp hT
  simp only [map_sum, opTrace_rankOne]
  exact Finset.sum_nonneg fun i _ => sq_nonneg ‖u i‖

theorem positive_trace_zero {T : Y →L[ℝ] Y} (hT : T.IsPositive)
    (hz : opTrace T = 0) : T = 0 := by
  obtain ⟨m, u, rfl⟩ := ContinuousLinearMap.isPositive_iff_eq_sum_rankOne.mp hT
  simp only [map_sum, opTrace_rankOne] at hz
  have hu : ∀ i : Fin m, u i = 0 := by
    intro i
    have hi := (Finset.sum_eq_zero_iff_of_nonneg
      (fun i (_ : i ∈ Finset.univ) => sq_nonneg ‖u i‖)).mp hz i (Finset.mem_univ i)
    exact norm_eq_zero.mp (sq_eq_zero_iff.mp hi)
  simp [hu]

theorem trace_mono {A B : Y →L[ℝ] Y} (h : (B - A).IsPositive) :
    opTrace A ≤ opTrace B := by
  have hh := positive_trace_nonneg h
  simpa only [map_sub, sub_nonneg] using hh

/-- Positive trace squeeze for actual operators and an actual limit. -/
theorem cone_squeeze {A : Y →L[ℝ] Y} (hA : A.IsPositive)
    (B : ℕ → Y →L[ℝ] Y) (hdom : ∀ n, (B n - A).IsPositive)
    (hlim : Tendsto (fun n => opTrace (B n)) atTop (𝓝 0)) : A = 0 := by
  apply positive_trace_zero hA
  exact le_antisymm
    (le_of_tendsto_of_tendsto tendsto_const_nhds hlim
      (Eventually.of_forall fun n => trace_mono (hdom n)))
    (positive_trace_nonneg hA)

omit [FiniteDimensional ℝ Y] in
theorem conjugation_positive {Z : Type*} [NormedAddCommGroup Z]
    [InnerProductSpace ℝ Z] [CompleteSpace Z] [CompleteSpace Y]
    {T : Z →L[ℝ] Z} (hT : T.IsPositive) (iota : Z →L[ℝ] Y) :
    (iota.comp (T.comp iota.adjoint)).IsPositive :=
  hT.conj_adjoint iota

omit [FiniteDimensional ℝ Y] in
theorem conjugation_mono {Z : Type*} [NormedAddCommGroup Z]
    [InnerProductSpace ℝ Z] [CompleteSpace Z] [CompleteSpace Y]
    {A B : Z →L[ℝ] Z} (h : (B - A).IsPositive) (iota : Z →L[ℝ] Y) :
    (iota.comp (B.comp iota.adjoint) - iota.comp (A.comp iota.adjoint)).IsPositive := by
  simpa only [ContinuousLinearMap.sub_comp, ContinuousLinearMap.comp_sub]
    using conjugation_positive h iota

/-- Moving spaces may depend on the stage. Positivity of moving `A`, `B` and
of the tail is unnecessary once the two domination inequalities are supplied. -/
theorem exhaustive_squeeze [CompleteSpace Y]
    {A_X : Y →L[ℝ] Y} (hX : A_X.IsPositive)
    {Z : ℕ → Type*} [∀ n, NormedAddCommGroup (Z n)]
    [∀ n, InnerProductSpace ℝ (Z n)] [∀ n, FiniteDimensional ℝ (Z n)]
    (iota : ∀ n, Z n →L[ℝ] Y) (A B : ∀ n, Z n →L[ℝ] Z n)
    (T : ℕ → Y →L[ℝ] Y)
    (hdom : ∀ n, (B n - A n).IsPositive)
    (hex : ∀ n, ((iota n).comp ((A n).comp (iota n).adjoint) + T n - A_X).IsPositive)
    (hlim : Tendsto (fun n => opTrace ((iota n).comp ((B n).comp (iota n).adjoint)) +
      opTrace (T n)) atTop (𝓝 0)) : A_X = 0 := by
  apply cone_squeeze hX (fun n => (iota n).comp ((B n).comp (iota n).adjoint) + T n)
  · intro n
    have hh := (conjugation_mono (hdom n) (iota n)).add (hex n)
    convert hh using 1
    abel
  · simpa only [map_add] using hlim

end SixBirdsDualityConfinement.DualityConfinement.ConcreteCore
