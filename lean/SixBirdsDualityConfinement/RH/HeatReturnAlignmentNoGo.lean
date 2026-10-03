import SixBirdsDualityConfinement.RH.OrdinateHeatReturn

/-!
The synthetic Gaussian heat return on actual RH zero windows is aligned
with its residual state. Navier's proved convection cancellation uses a
different kinetic pairing, so that cancellation cannot be transferred to
this RH return source by the common heat multiplier alone.
-/

noncomputable section
open scoped NNReal InnerProduct InnerProductSpace
namespace SixBirdsDualityConfinement.RH.HeatReturnAlignmentNoGo

open ClassicalZeroLedger FiniteZeroWindows OrdinateHeatReturn

theorem ordinate_heat_deficit_inner_eq_sum
    (W : Finset NontrivialZero) (t : ℝ≥0)
    (v : EuclideanSpace ℝ {ρ // ρ ∈ W}) :
    inner ℝ v (v - ordinateHeatTransport W t v) =
      ∑ ρ : {ρ // ρ ∈ W},
        (1 - Real.exp (-(t : ℝ) * ρ.val.val.im ^ 2)) * (v ρ) ^ 2 := by
  rw [PiLp.inner_apply]
  apply Finset.sum_congr rfl
  intro ρ hρ
  simp [ordinateHeatTransport_apply, RCLike.inner_apply]
  ring

private theorem deficit_term_nonneg (t : ℝ≥0)
    (ρ : NontrivialZero) (x : ℝ) :
    0 ≤ (1 - Real.exp (-(t : ℝ) * ρ.val.im ^ 2)) * x ^ 2 := by
  have hmask : 0 ≤ 1 - Real.exp (-(t : ℝ) * ρ.val.im ^ 2) := by
    apply sub_nonneg.mpr
    apply Real.exp_le_one_iff.mpr
    have ht : 0 ≤ (t : ℝ) := t.property
    nlinarith [sq_nonneg ρ.val.im]
  exact mul_nonneg hmask (sq_nonneg _)

theorem ordinate_heat_deficit_inner_nonneg
    (W : Finset NontrivialZero) (t : ℝ≥0)
    (v : EuclideanSpace ℝ {ρ // ρ ∈ W}) :
    0 ≤ inner ℝ v (v - ordinateHeatTransport W t v) := by
  rw [ordinate_heat_deficit_inner_eq_sum]
  apply Finset.sum_nonneg
  intro ρ hρ
  exact deficit_term_nonneg t ρ.val (v ρ)

/-- If heat truly damps one occupied coordinate, the return source has
strictly positive alignment with the state. -/
theorem ordinate_heat_deficit_inner_pos_of_coordinate
    (W : Finset NontrivialZero) (t : ℝ≥0) (ht : 0 < t)
    (v : EuclideanSpace ℝ {ρ // ρ ∈ W})
    (ρ : {ρ // ρ ∈ W}) (hheight : ρ.val.val.im ≠ 0)
    (hv : v ρ ≠ 0) :
    0 < inner ℝ v (v - ordinateHeatTransport W t v) := by
  rw [ordinate_heat_deficit_inner_eq_sum]
  apply (Finset.sum_pos_iff_of_nonneg
    (fun σ _ => deficit_term_nonneg t σ.val (v σ))).mpr
  refine ⟨ρ, Finset.mem_univ _, ?_⟩
  have hsq : 0 < ρ.val.val.im ^ 2 := sq_pos_of_ne_zero hheight
  have hneg : -((t : ℝ) * ρ.val.val.im ^ 2) < 0 := by
    have ht' : 0 < (t : ℝ) := ht
    nlinarith
  have hmask : 0 < 1 - Real.exp (-(t : ℝ) * ρ.val.val.im ^ 2) := by
    simpa [neg_mul] using
      (sub_pos.mpr (Real.exp_lt_one_iff.mpr hneg) :
        0 < 1 - Real.exp (-((t : ℝ) * ρ.val.val.im ^ 2)))
  exact mul_pos hmask (sq_pos_of_ne_zero hv)

theorem window_heat_source_inner_pos_of_coordinate
    (m : NontrivialZero → ℕ) (W : Finset NontrivialZero)
    (t : ℝ≥0) (ht : 0 < t)
    (ρ : {ρ // ρ ∈ W}) (hheight : ρ.val.val.im ≠ 0)
    (hdisplacement : (displacementVector m W) ρ ≠ 0) :
    0 < inner ℝ (displacementVector m W)
      (windowOrdinateHeatSourceStep m W t).source := by
  rw [windowOrdinateHeatSourceStep_source]
  exact ordinate_heat_deficit_inner_pos_of_coordinate W t ht
    (displacementVector m W) ρ hheight hdisplacement

end SixBirdsDualityConfinement.RH.HeatReturnAlignmentNoGo
