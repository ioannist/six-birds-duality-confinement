import SixBirdsDualityConfinement.RH.FiniteZeroWindows

/-! Identity-audit decoder geometry and coercivity obstructions on actual zero windows.
The residual projection identity is already proved by XiCore's
`auditResidual_id_eq_hilbertKernelXi`; its right side is `L.ker.starProjection`. -/
noncomputable section
namespace SixBirdsDualityConfinement.RH.ConcreteWindowXI

open ClassicalZeroLedger FiniteZeroWindows SixBirdsNeedles.XiCore
open scoped InnerProduct InnerProductSpace

/-- The identity-audit decoded native map is the orthogonal complement projection. -/
theorem identity_auditDecoder_comp
    {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [NormedAddCommGroup F] [InnerProductSpace ℝ F]
    [FiniteDimensional ℝ F] (L : E →L[ℝ] F) :
    auditDecoder (ContinuousLinearMap.id ℝ E) (ContinuousLinearMap.id ℝ E) L ∘L L =
      L.kerᗮ.starProjection := by
  have h := decoder_comp (ContinuousLinearMap.id ℝ E) L
  simpa [auditDecoder, auditCross, auditCurrency, decoder, gram, pinv_id_real,
    ContinuousLinearMap.comp_assoc] using h

/-- A scalar probe cannot be injective on a window space with at least two coordinates. -/
theorem invariantProbe_not_injective (W : Finset NontrivialZero) (hcard : 2 ≤ W.card) :
    ¬ Function.Injective (invariantProbe W) := by
  classical
  intro hinj
  have hd := LinearMap.finrank_le_finrank_of_injective
    (f := (invariantProbe W).toLinearMap) hinj
  have hsmall : W.card ≤ 1 := by simpa using hd
  omega

/-- Native coercivity on the range of its own full fixed-target residual is impossible
on any window with at least two actual zeros. -/
theorem invariantProbe_no_residual_coercivity
    (W : Finset NontrivialZero) (hcard : 2 ≤ W.card) :
    ¬ ∃ c : ℝ, 0 < c ∧ ∀ x ∈
      (auditResidual (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {rho // rho ∈ W}))
        (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {rho // rho ∈ W}))
        (invariantProbe W)).range,
      c * ‖x‖ ≤ ‖invariantProbe W x‖ := by
  classical
  rintro ⟨c, hc, hcoerc⟩
  have hcoerc' : ∀ x ∈
      (xi (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {rho // rho ∈ W}))
        (invariantProbe W)).range, c * ‖x‖ ≤ ‖invariantProbe W x‖ := by
    simpa only [auditResidual_id_eq_xi] using hcoerc
  have hz := native_coercive_on_own_residual_forces_injective (invariantProbe W)
    _ le_rfl c hc hcoerc'
  apply invariantProbe_not_injective W hcard
  exact LinearMap.ker_eq_bot.mp (LinearMap.ker_eq_bot'.mpr hz)

end SixBirdsDualityConfinement.RH.ConcreteWindowXI
