import SixBirdsDualityConfinement.DualityConfinement.ConcreteCore
import Mathlib.LinearAlgebra.Isomorphisms

/-! Finite-dimensional Douglas factorization, constructed on the range and
extended by zero on its orthogonal complement. -/
namespace SixBirdsDualityConfinement.DualityConfinement.ConcreteDouglas
open SixBirdsDualityConfinement.DualityConfinement.ConcreteCore
variable {H K1 K2 : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H]
  [FiniteDimensional ℝ H] [NormedAddCommGroup K1] [InnerProductSpace ℝ K1]
  [FiniteDimensional ℝ K1] [NormedAddCommGroup K2] [InnerProductSpace ℝ K2]
  [FiniteDimensional ℝ K2]

theorem gram_domination_iff_norm (V : H →L[ℝ] K1) (W : H →L[ℝ] K2) :
    (W.adjoint.comp W - V.adjoint.comp V).IsPositive ↔ ∀ h, ‖V h‖ ≤ ‖W h‖ := by
  constructor
  · intro hp h
    have hh := hp.inner_nonneg_left h
    simp only [ContinuousLinearMap.sub_apply, ContinuousLinearMap.comp_apply,
      inner_sub_left, ContinuousLinearMap.adjoint_inner_left, real_inner_self_eq_norm_sq] at hh
    exact (sq_le_sq₀ (norm_nonneg _) (norm_nonneg _)).mp (sub_nonneg.mp hh)
  · intro hn
    refine ⟨(ContinuousLinearMap.isPositive_adjoint_comp_self W).isSymmetric.sub
      (ContinuousLinearMap.isPositive_adjoint_comp_self V).isSymmetric, ?_⟩
    intro h
    change 0 ≤ inner ℝ ((W.adjoint.comp W - V.adjoint.comp V) h) h
    simp only [ContinuousLinearMap.sub_apply, ContinuousLinearMap.comp_apply,
      inner_sub_left, ContinuousLinearMap.adjoint_inner_left, real_inner_self_eq_norm_sq]
    exact sub_nonneg.mpr ((sq_le_sq₀ (norm_nonneg _) (norm_nonneg _)).mpr (hn h))

/-- Reverse Douglas implication, using the actual operator norm. -/
theorem douglas_reverse (V : H →L[ℝ] K1) (W : H →L[ℝ] K2)
    (T : K2 →L[ℝ] K1) (hT : ‖T‖ ≤ 1) (hfac : V = T.comp W) :
    (W.adjoint.comp W - V.adjoint.comp V).IsPositive := by
  apply (gram_domination_iff_norm V W).mpr
  intro h
  rw [hfac, ContinuousLinearMap.comp_apply]
  exact (T.le_opNorm (W h)).trans (by nlinarith [norm_nonneg (W h)])

/-- The forward implication constructs the factor; it is not a supplied field. -/
theorem douglas_forward (V : H →L[ℝ] K1) (W : H →L[ℝ] K2)
    (hp : (W.adjoint.comp W - V.adjoint.comp V).IsPositive) :
    ∃ T : K2 →L[ℝ] K1, ‖T‖ ≤ 1 ∧ V = T.comp W := by
  classical
  have hn := (gram_domination_iff_norm V W).mp hp
  have hker : W.toLinearMap.ker ≤ V.toLinearMap.ker := by
    intro h hh
    change V h = 0
    have hw : W h = 0 := hh
    apply norm_eq_zero.mp
    exact le_antisymm (by simpa only [hw, norm_zero] using hn h) (norm_nonneg _)
  let R : W.toLinearMap.range →ₗ[ℝ] K1 :=
    (W.toLinearMap.ker.liftQ V.toLinearMap hker).comp
      W.toLinearMap.quotKerEquivRange.symm.toLinearMap
  have hR (h : H) : R ⟨W h, ⟨h, rfl⟩⟩ = V h := by
    dsimp only [R, LinearMap.comp_apply, LinearEquiv.coe_toLinearMap]
    exact congrArg (W.toLinearMap.ker.liftQ V.toLinearMap hker)
      (W.toLinearMap.quotKerEquivRange_symm_apply_image h ⟨h, rfl⟩)
  have hRn (z : W.toLinearMap.range) : ‖R z‖ ≤ ‖z‖ := by
    obtain ⟨h, hh⟩ := z.property
    have hz : z = ⟨W h, ⟨h, rfl⟩⟩ := Subtype.ext hh.symm
    rw [hz, hR]
    exact hn h
  let T : K2 →L[ℝ] K1 := R.toContinuousLinearMap.comp W.toLinearMap.range.orthogonalProjection
  refine ⟨T, ?_, ?_⟩
  · apply T.opNorm_le_bound zero_le_one
    intro z
    exact (hRn _).trans (by simpa only [one_mul] using
      W.toLinearMap.range.norm_orthogonalProjection_apply_le z)
  · ext h
    change V h = R (W.toLinearMap.range.orthogonalProjection (W h))
    have he := W.toLinearMap.range.orthogonalProjection_mem_subspace_eq_self
      (⟨W h, ⟨h, rfl⟩⟩ : W.toLinearMap.range)
    rw [he, hR]

theorem douglas_factorization (V : H →L[ℝ] K1) (W : H →L[ℝ] K2) :
    (W.adjoint.comp W - V.adjoint.comp V).IsPositive ↔
      ∃ T : K2 →L[ℝ] K1, ‖T‖ ≤ 1 ∧ V = T.comp W := by
  constructor
  · exact douglas_forward V W
  · rintro ⟨T, hT, hfac⟩
    exact douglas_reverse V W T hT hfac

end SixBirdsDualityConfinement.DualityConfinement.ConcreteDouglas
