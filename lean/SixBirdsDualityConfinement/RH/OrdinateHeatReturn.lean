import SixBirdsDualityConfinement.RH.JEquivariantSourceAudit

/-!
A genuine diagonal Gaussian heat multiplier on each finite actual RH zero
window, using the imaginary ordinate as its frequency. It is the same
spectral multiplier form as Navier heat, but the zero-window displacement
is a fixed target, so the source required to return it is the complete
heat deficit. This source is state-dependent, not an arithmetic prime
receipt.
-/

noncomputable section
open scoped NNReal InnerProduct InnerProductSpace
namespace SixBirdsDualityConfinement.RH.OrdinateHeatReturn

open ClassicalZeroLedger FiniteZeroWindows ActualInvolution JTransportNoGo
open JEquivariantSourceAudit SixBirdsNeedles.XiCore

def ordinateHeatTransport (W : Finset NontrivialZero) (t : ℝ≥0) :
    EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ]
      EuclideanSpace ℝ {ρ // ρ ∈ W} :=
  LinearMap.toContinuousLinearMap {
    toFun := fun v => WithLp.toLp 2
      (fun ρ => Real.exp (-(t : ℝ) * ρ.val.val.im ^ 2) * v ρ)
    map_add' := by
      intro v w
      ext ρ
      simp [mul_add]
    map_smul' := by
      intro c v
      ext ρ
      change Real.exp (-(t : ℝ) * ρ.val.val.im ^ 2) * (c * v ρ) =
        c * (Real.exp (-(t : ℝ) * ρ.val.val.im ^ 2) * v ρ)
      ring
  }

theorem ordinateHeatTransport_apply
    (W : Finset NontrivialZero) (t : ℝ≥0)
    (v : EuclideanSpace ℝ {ρ // ρ ∈ W}) (ρ : {ρ // ρ ∈ W}) :
    ordinateHeatTransport W t v ρ =
      Real.exp (-(t : ℝ) * ρ.val.val.im ^ 2) * v ρ := rfl

theorem ordinateHeatTransport_norm_le
    (W : Finset NontrivialZero) (t : ℝ≥0)
    (v : EuclideanSpace ℝ {ρ // ρ ∈ W}) :
    ‖ordinateHeatTransport W t v‖ ≤ ‖v‖ := by
  have hsq : ‖ordinateHeatTransport W t v‖ ^ 2 ≤ ‖v‖ ^ 2 := by
    rw [EuclideanSpace.norm_sq_eq, EuclideanSpace.norm_sq_eq]
    apply Finset.sum_le_sum
    intro ρ hρ
    rw [ordinateHeatTransport_apply, norm_mul]
    let a : ℝ := Real.exp (-(t : ℝ) * ρ.val.val.im ^ 2)
    have ha0 : 0 ≤ a := (Real.exp_pos _).le
    have ha1 : a ≤ 1 := by
      apply Real.exp_le_one_iff.mpr
      dsimp [a]
      have ht : 0 ≤ (t : ℝ) := t.property
      nlinarith [sq_nonneg ρ.val.val.im]
    rw [Real.norm_of_nonneg ha0]
    have hv : 0 ≤ ‖v ρ‖ := norm_nonneg _
    nlinarith [mul_nonneg ha0 hv, mul_nonneg (sub_nonneg.mpr ha1) hv]
  nlinarith [norm_nonneg (ordinateHeatTransport W t v), norm_nonneg v]

/-- Heat strictly damps a nonzero coordinate at positive time whenever its
zero has nonzero imaginary height. This pointwise statement needs no global
zero-free theorem for the real interval inside the strip. -/
theorem ordinateHeatTransport_coordinate_strict
    (W : Finset NontrivialZero) (t : ℝ≥0) (ht : 0 < t)
    (v : EuclideanSpace ℝ {ρ // ρ ∈ W}) (ρ : {ρ // ρ ∈ W})
    (hρ : ρ.val.val.im ≠ 0) (hv : v ρ ≠ 0) :
    ‖ordinateHeatTransport W t v ρ‖ < ‖v ρ‖ := by
  rw [ordinateHeatTransport_apply, norm_mul,
    Real.norm_of_nonneg (Real.exp_pos _).le]
  have hsq : 0 < ρ.val.val.im ^ 2 := sq_pos_of_ne_zero hρ
  have hneg : -((t : ℝ) * ρ.val.val.im ^ 2) < 0 := by
    have ht' : 0 < (t : ℝ) := ht
    nlinarith
  have hmask : Real.exp (-((t : ℝ) * ρ.val.val.im ^ 2)) < 1 :=
    Real.exp_lt_one_iff.mpr hneg
  have hcoord : 0 < ‖v ρ‖ := norm_pos_iff.mpr hv
  simpa using mul_lt_mul_of_pos_right hmask hcoord

/-- The heat multiplier depends only on the ordinate, which the genuine
`J` involution preserves. -/
theorem ordinateHeatTransport_commutes_J
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) (t : ℝ≥0)
    (v : EuclideanSpace ℝ {ρ // ρ ∈ W}) :
    ordinateHeatTransport W t (windowJTransport W hW v) =
      windowJTransport W hW (ordinateHeatTransport W t v) := by
  ext ρ
  change Real.exp (-(t : ℝ) * ρ.val.val.im ^ 2) *
      v ⟨J_zero ρ.val, hW ρ.val ρ.property⟩ =
    Real.exp (-(t : ℝ) * (J_zero ρ.val).val.im ^ 2) *
      v ⟨J_zero ρ.val, hW ρ.val ρ.property⟩
  change Real.exp (-(t : ℝ) * ρ.val.val.im ^ 2) *
      v ⟨J_zero ρ.val, hW ρ.val ρ.property⟩ =
    Real.exp (-(t : ℝ) * (J ρ.val.val).im ^ 2) *
      v ⟨J_zero ρ.val, hW ρ.val ρ.property⟩
  rw [J_im]

/-- This is an exact fixed-point source step. No arithmetic estimate of
its source is supplied by the definition. -/
def windowOrdinateHeatSourceStep
    (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) (t : ℝ≥0) :
    XiSourceStep (EuclideanSpace ℝ {ρ // ρ ∈ W}) ℝ where
  native := invariantProbe W
  transport := ordinateHeatTransport W t
  before := displacementVector m W
  after := displacementVector m W
  source := displacementVector m W -
    ordinateHeatTransport W t (displacementVector m W)
  balance := by abel

theorem windowOrdinateHeatSourceStep_source
    (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) (t : ℝ≥0) :
    (windowOrdinateHeatSourceStep m W t).source =
      displacementVector m W -
        ordinateHeatTransport W t (displacementVector m W) := rfl

/-- Every coordinate of the source is precisely the heat deficit of that
coordinate's real displacement. It is not the independent prime source. -/
theorem windowOrdinateHeatSourceStep_source_coordinate
    (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) (t : ℝ≥0) (ρ : {ρ // ρ ∈ W}) :
    (windowOrdinateHeatSourceStep m W t).source ρ =
      (1 - Real.exp (-(t : ℝ) * ρ.val.val.im ^ 2)) *
        (displacementVector m W) ρ := by
  rw [windowOrdinateHeatSourceStep_source]
  change (displacementVector m W) ρ -
      (ordinateHeatTransport W t (displacementVector m W)) ρ = _
  rw [ordinateHeatTransport_apply]
  ring

/-- In each zero coordinate, the fixed-point source pays exactly the norm
removed by the Gaussian heat multiplier. There is no spare contraction
margin from the transport identity itself. -/
theorem windowOrdinateHeatSourceStep_exact_coordinate_gap
    (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) (t : ℝ≥0) (ρ : {ρ // ρ ∈ W}) :
    ‖(windowOrdinateHeatSourceStep m W t).source ρ‖ =
      ‖(displacementVector m W) ρ‖ -
        ‖ordinateHeatTransport W t (displacementVector m W) ρ‖ := by
  let h : ℝ := Real.exp (-(t : ℝ) * ρ.val.val.im ^ 2)
  have hnonneg : 0 ≤ h := (Real.exp_pos _).le
  have hle : h ≤ 1 := by
    apply Real.exp_le_one_iff.mpr
    dsimp [h]
    have ht : 0 ≤ (t : ℝ) := t.property
    nlinarith [sq_nonneg ρ.val.val.im]
  rw [windowOrdinateHeatSourceStep_source_coordinate,
    ordinateHeatTransport_apply]
  change ‖(1 - h) * (displacementVector m W) ρ‖ =
    ‖(displacementVector m W) ρ‖ -
      ‖h * (displacementVector m W) ρ‖
  rw [norm_mul, norm_mul,
    Real.norm_of_nonneg (sub_nonneg.mpr hle),
    Real.norm_of_nonneg hnonneg]
  ring

/-- At positive time and nonzero ordinate, the return source vanishes in a
coordinate exactly when that coordinate of the displacement vanishes. -/
theorem windowOrdinateHeatSourceStep_source_coordinate_zero_iff
    (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) (t : ℝ≥0) (ht : 0 < t)
    (ρ : {ρ // ρ ∈ W}) (hρ : ρ.val.val.im ≠ 0) :
    (windowOrdinateHeatSourceStep m W t).source ρ = 0 ↔
      (displacementVector m W) ρ = 0 := by
  rw [windowOrdinateHeatSourceStep_source_coordinate]
  have hsq : 0 < ρ.val.val.im ^ 2 := sq_pos_of_ne_zero hρ
  have hneg : -((t : ℝ) * ρ.val.val.im ^ 2) < 0 := by
    have ht' : 0 < (t : ℝ) := ht
    nlinarith
  have hfactor : 1 - Real.exp (-((t : ℝ) * ρ.val.val.im ^ 2)) ≠ 0 := by
    have he : Real.exp (-((t : ℝ) * ρ.val.val.im ^ 2)) < 1 :=
      Real.exp_lt_one_iff.mpr hneg
    exact ne_of_gt (sub_pos.mpr he)
  simp [hfactor]

/-- The actual native currencies of the state, heat image, and exact
return source all vanish on a J-reflected window. -/
theorem windowOrdinateHeatSourceStep_native_currency_zero
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) (t : ℝ≥0) :
    let S := windowOrdinateHeatSourceStep m W t
    hilbertNativeCurrency S.native S.before = 0 ∧
      hilbertNativeCurrency S.native (S.transport S.before) = 0 ∧
      hilbertNativeCurrency S.native S.source = 0 := by
  dsimp only [windowOrdinateHeatSourceStep]
  exact commuting_window_step_native_currency_zero m hm W hW
    (ordinateHeatTransport W t)
    (ordinateHeatTransport_commutes_J W hW t)
    (displacementVector m W -
      ordinateHeatTransport W t (displacementVector m W))
    (by abel)

/-- On a reflected window, the entire return source is XI residual. Heat
does not turn the missing RH payment into native currency. -/
theorem windowOrdinateHeatSourceStep_source_is_xi
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (J_zero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : JReflectedWindow W) (t : ℝ≥0) :
    let S := windowOrdinateHeatSourceStep m W t
    hilbertKernelXi S.native S.source = S.source := by
  dsimp only [windowOrdinateHeatSourceStep]
  obtain ⟨_, _, hs⟩ := commuting_window_step_native_channels_zero m hm W hW
    (ordinateHeatTransport W t)
    (ordinateHeatTransport_commutes_J W hW t)
    (displacementVector m W -
      ordinateHeatTransport W t (displacementVector m W))
    (by abel)
  exact (invariantProbe W).ker.starProjection_eq_self_iff.mpr hs

end SixBirdsDualityConfinement.RH.OrdinateHeatReturn
