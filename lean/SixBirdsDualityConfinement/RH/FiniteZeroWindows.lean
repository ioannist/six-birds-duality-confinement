import SixBirdsDualityConfinement.RH.ClassicalZeroCountable
import SixBirdsNeedles.XiCore.AuditResidual
import SixBirdsNeedles.XiCore.HilbertKernelXi
import Mathlib.Data.Finset.Option
import Mathlib.Topology.Order.OrderClosed

/-!
Finite windows of actual completed-zeta zeros. The budget theorem is an exact
return principle: an eventually covered zero has a fixed nonnegative term,
so an exhaustive window budget tending to zero forces that term to vanish.
No existence or decay of such a budget is asserted here.
-/

noncomputable section
open Filter
open scoped Topology
open scoped InnerProduct InnerProductSpace

namespace SixBirdsDualityConfinement.RH.FiniteZeroWindows

open ClassicalZeroLedger
open SixBirdsNeedles.XiCore

def displacement (ρ : NontrivialZero) : ℝ := ρ.val.re - (1 / 2 : ℝ)

/-- Unit weights detect every off-line zero without assuming a theorem about
its analytic multiplicity. -/
def unitWeights : NontrivialZero → ℕ := fun _ => 1

theorem unitWeights_positive : ∀ ρ, 0 < unitWeights ρ := by
  intro ρ
  simp [unitWeights]

/-- The completed zeta functional equation supplies this zero-set involution.
It reverses the real displacement even though it is not the manuscript's
imaginary-part-preserving involution `1 - conj(s)`. -/
def reflectZero (ρ : NontrivialZero) : NontrivialZero :=
  ⟨1 - ρ.val, by
    rw [completedRiemannZeta_one_sub]
    exact ρ.property.1,
    by
      have h := ρ.property.2.2
      simp only [Complex.sub_re, Complex.one_re]
      linarith,
    by
      have h := ρ.property.2.1
      simp only [Complex.sub_re, Complex.one_re]
      linarith⟩

theorem reflectZero_involutive (ρ : NontrivialZero) :
    reflectZero (reflectZero ρ) = ρ := by
  apply Subtype.ext
  simp [reflectZero]

theorem displacement_reflectZero (ρ : NontrivialZero) :
    displacement (reflectZero ρ) = -displacement ρ := by
  simp [displacement, reflectZero, Complex.sub_re]
  ring

theorem unitWeights_reflection_symmetric :
    ∀ ρ, unitWeights (reflectZero ρ) = unitWeights ρ := by
  intro ρ
  rfl

def ReflectedWindow (W : Finset NontrivialZero) : Prop :=
  ∀ ρ ∈ W, reflectZero ρ ∈ W

def closeReflection (W : Finset NontrivialZero) : Finset NontrivialZero :=
  by
    classical
    exact W ∪ W.image reflectZero

theorem mem_closeReflection_self (W : Finset NontrivialZero)
    (ρ : NontrivialZero) (hρ : ρ ∈ W) : ρ ∈ closeReflection W := by
  classical
  exact Finset.mem_union_left _ hρ

theorem closeReflection_reflected (W : Finset NontrivialZero) :
    ReflectedWindow (closeReflection W) := by
  classical
  intro ρ hρ
  change ρ ∈ W ∪ W.image reflectZero at hρ
  change reflectZero ρ ∈ W ∪ W.image reflectZero
  rcases Finset.mem_union.mp hρ with h | h
  · exact Finset.mem_union_right _ (Finset.mem_image_of_mem reflectZero h)
  · obtain ⟨σ, hσ, hσρ⟩ := Finset.mem_image.mp h
    rw [← hσρ, reflectZero_involutive]
    exact Finset.mem_union_left _ hσ

theorem closeReflection_eventuallyCovered
    (W : ℕ → Finset NontrivialZero)
    (hW : ∀ ρ : NontrivialZero, ∀ᶠ n in atTop, ρ ∈ W n) :
    ∀ ρ : NontrivialZero, ∀ᶠ n in atTop, ρ ∈ closeReflection (W n) := by
  intro ρ
  exact (hW ρ).mono fun n hn => mem_closeReflection_self (W n) ρ hn

def windowEnergy (m : NontrivialZero → ℕ) (W : Finset NontrivialZero) : ℝ :=
  ∑ ρ ∈ W, (m ρ : ℝ) * displacement ρ ^ 2

theorem term_nonneg (m : NontrivialZero → ℕ) (ρ : NontrivialZero) :
    0 ≤ (m ρ : ℝ) * displacement ρ ^ 2 :=
  mul_nonneg (Nat.cast_nonneg _) (sq_nonneg _)

theorem term_le_window (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) (ρ : NontrivialZero) (hρ : ρ ∈ W) :
    (m ρ : ℝ) * displacement ρ ^ 2 ≤ windowEnergy m W := by
  exact Finset.single_le_sum (fun σ _ => term_nonneg m σ) hρ

theorem windowEnergy_eq_zero_iff (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, 0 < m ρ) (W : Finset NontrivialZero) :
    windowEnergy m W = 0 ↔ ∀ ρ ∈ W, displacement ρ = 0 := by
  constructor
  · intro h ρ hρ
    have ht := term_le_window m W ρ hρ
    rw [h] at ht
    have hmpos : (0 : ℝ) < m ρ := Nat.cast_pos.mpr (hm ρ)
    have hs : displacement ρ ^ 2 ≤ 0 := by
      nlinarith [sq_nonneg (displacement ρ)]
    nlinarith [sq_nonneg (displacement ρ)]
  · intro h
    unfold windowEnergy
    apply Finset.sum_eq_zero
    intro ρ hρ
    simp [h ρ hρ]

/-- The finite real window is exactly the finite restriction of the
classical extended-nonnegative zero ledger. This is independent of XI. -/
theorem ofReal_windowEnergy_eq_finite_classical_ledger
    (m : NontrivialZero → ℕ) (W : Finset NontrivialZero) :
    ENNReal.ofReal (windowEnergy m W) =
      ∑ ρ ∈ W, weightedTerm m ρ := by
  rw [windowEnergy, ENNReal.ofReal_sum_of_nonneg]
  · apply Finset.sum_congr rfl
    intro ρ _
    rw [weightedTerm, ← ENNReal.ofReal_natCast,
      ← ENNReal.ofReal_mul (Nat.cast_nonneg (m ρ))]
    rfl
  · intro ρ _
    exact term_nonneg m ρ

theorem finite_window_le_global_classical_ledger
    (m : NontrivialZero → ℕ) (W : Finset NontrivialZero) :
    ENNReal.ofReal (windowEnergy m W) ≤ antiInvariantSum m := by
  rw [ofReal_windowEnergy_eq_finite_classical_ledger, antiInvariantSum]
  exact ENNReal.sum_le_tsum W

/-- The actual finite zero window, with positive weights, as a Hilbert vector.
This is a faithful finite readout of the classical zero coordinates. -/
def displacementVector (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) : EuclideanSpace ℝ {ρ // ρ ∈ W} :=
  WithLp.toLp 2 (fun ρ => Real.sqrt (m ρ.val) * displacement ρ.val)

theorem displacementVector_norm_sq (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) :
    ‖displacementVector m W‖ ^ 2 = windowEnergy m W := by
  classical
  rw [EuclideanSpace.norm_sq_eq]
  simp only [displacementVector, PiLp.toLp_apply, Real.norm_eq_abs, sq_abs,
    mul_pow, Real.sq_sqrt (Nat.cast_nonneg _)]
  simpa [windowEnergy, Finset.univ_eq_attach] using
    (Finset.sum_attach W (fun ρ => (m ρ : ℝ) * displacement ρ ^ 2))

/-- Functional-equation pairs cancel in the invariant sum. This uses only
symmetry of multiplicities, not RH. -/
theorem weighted_displacement_sum_zero
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : ReflectedWindow W) :
    ∑ ρ ∈ W, Real.sqrt (m ρ) * displacement ρ = 0 := by
  classical
  let f : NontrivialZero → ℝ := fun ρ => Real.sqrt (m ρ) * displacement ρ
  change ∑ ρ ∈ W, f ρ = 0
  apply Finset.sum_involution (fun ρ _ => reflectZero ρ)
  · intro ρ _
    dsimp [f]
    rw [hm, displacement_reflectZero]
    ring
  · intro ρ _ hf heq
    have hd := displacement_reflectZero ρ
    rw [heq] at hd
    have hz : displacement ρ = 0 := by linarith
    exact hf (by simp [f, hz])
  · exact hW
  · intro ρ _
    exact reflectZero_involutive ρ

def invariantVector (W : Finset NontrivialZero) :
    EuclideanSpace ℝ {ρ // ρ ∈ W} :=
  WithLp.toLp 2 (fun _ => (1 : ℝ))

def invariantProbe (W : Finset NontrivialZero) :
    EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ] ℝ :=
  innerSL ℝ (invariantVector W)

theorem invariantProbe_ne_zero_of_nonempty
    (W : Finset NontrivialZero) (hW : W.Nonempty) :
    invariantProbe W ≠ 0 := by
  classical
  obtain ⟨ρ, hρ⟩ := hW
  intro h
  have hmap : innerSL ℝ (invariantVector W) =
      innerSL ℝ (0 : EuclideanSpace ℝ {ρ // ρ ∈ W}) := by
    simpa [invariantProbe] using h
  have hvec := innerSL_inj.mp hmap
  have hcoord := congrArg
    (fun x : EuclideanSpace ℝ {ρ // ρ ∈ W} => x ⟨ρ, hρ⟩) hvec
  norm_num [invariantVector] at hcoord

theorem invariantProbe_displacement_zero
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : ReflectedWindow W) :
    invariantProbe W (displacementVector m W) = 0 := by
  classical
  change inner ℝ (invariantVector W) (displacementVector m W) = 0
  rw [invariantVector, displacementVector, EuclideanSpace.inner_toLp_toLp]
  simp only [dotProduct, star_trivial, mul_one]
  simpa [Finset.univ_eq_attach] using
    (Finset.sum_attach W (fun ρ => Real.sqrt (m ρ) * displacement ρ)).trans
      (weighted_displacement_sum_zero m hm W hW)

/-- For a rank-one target whose representing vector is invisible to the
native observation, the exact XI residual is its squared Hilbert norm. -/
theorem xi_rankOne_native_kernel
    {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [NormedAddCommGroup F]
    [InnerProductSpace ℝ F] [FiniteDimensional ℝ F]
    (v : E) (L : E →L[ℝ] F) (hv : L v = 0) :
    RCLike.re (inner ℝ (1 : ℝ) ((xi (innerSL ℝ v) L) 1)) = ‖v‖ ^ 2 := by
  have hvker : v ∈ L.ker := hv
  have hres : residualMap (innerSL ℝ v) L = innerSL ℝ v := by
    ext x
    change inner ℝ v (L.ker.starProjection x) = inner ℝ v x
    rw [← ContinuousLinearMap.adjoint_inner_left,
      adjoint_projection, Submodule.starProjection_eq_self_iff.mpr hvker]
  rw [projection_identity, hres, gram_quadratic,
    ContinuousLinearMap.adjoint_innerSL_apply]
  simp

/-- In this version the target observation is the fixed identity map. Only
the realized state `v` changes. On a state invisible to the native probe,
the residual sees its entire squared norm. -/
theorem xi_fullReadout_native_kernel
    {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [NormedAddCommGroup F]
    [InnerProductSpace ℝ F] [FiniteDimensional ℝ F]
    (v : E) (L : E →L[ℝ] F) (hv : L v = 0) :
    RCLike.re (inner ℝ v ((xi (ContinuousLinearMap.id ℝ E) L) v)) =
      ‖v‖ ^ 2 := by
  have hvker : v ∈ L.ker := hv
  rw [projection_identity, gram_quadratic]
  change ‖(ContinuousLinearMap.adjoint L.ker.starProjection) v‖ ^ 2 = ‖v‖ ^ 2
  rw [adjoint_projection, Submodule.starProjection_eq_self_iff.mpr hvker]

/-- For the fixed identity target, XI acts as the identity on every vector
invisible to the native observation. Thus such a vector belongs to the
support of the residual operator, not just to its quadratic readout. -/
theorem xi_fullReadout_native_kernel_apply
    {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [NormedAddCommGroup F]
    [InnerProductSpace ℝ F] [FiniteDimensional ℝ F]
    (v : E) (L : E →L[ℝ] F) (hv : L v = 0) :
    xi (ContinuousLinearMap.id ℝ E) L v = v := by
  have hvker : v ∈ L.ker := hv
  rw [projection_identity]
  change L.ker.starProjection ((L.ker.starProjection†) v) = v
  rw [adjoint_projection, Submodule.starProjection_eq_self_iff.mpr hvker]
  exact Submodule.starProjection_eq_self_iff.mpr hvker

/-- Operator-norm decay is stronger than decay of the actual-state XI
quadratic: one nonzero native-blind direction gives a fixed norm floor. -/
theorem xi_fullReadout_opNorm_ge_one_of_native_kernel
    {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [NormedAddCommGroup F]
    [InnerProductSpace ℝ F] [FiniteDimensional ℝ F]
    (v : E) (L : E →L[ℝ] F) (hv : L v = 0) (hne : v ≠ 0) :
    (1 : ℝ) ≤ ‖xi (ContinuousLinearMap.id ℝ E) L‖ := by
  have hvpos : 0 < ‖v‖ := norm_pos_iff.mpr hne
  have hb := (xi (ContinuousLinearMap.id ℝ E) L).le_opNorm v
  rw [xi_fullReadout_native_kernel_apply v L hv] at hb
  exact le_of_mul_le_mul_right (by simpa using hb) hvpos

/-- The native map cannot itself be coercive on the full support of its
fixed-target XI residual unless it has trivial kernel. This is the exact
support-coercivity hypothesis of `XiCore.CoerciveReturn` specialized to
`S=L` and `X=xi id L`; it is not supplied by the XI identity. -/
theorem native_coercive_on_own_residual_forces_injective
    {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [NormedAddCommGroup F]
    [InnerProductSpace ℝ F] [FiniteDimensional ℝ F]
    (L : E →L[ℝ] F) (M : Submodule ℝ E)
    (hM : (xi (ContinuousLinearMap.id ℝ E) L).range ≤ M)
    (c : ℝ) (hc : 0 < c)
    (hS : ∀ x ∈ M, c * ‖x‖ ≤ ‖L x‖) :
    ∀ x, L x = 0 → x = 0 := by
  intro x hx
  have hX : xi (ContinuousLinearMap.id ℝ E) L x = x :=
    xi_fullReadout_native_kernel_apply x L hx
  have hxM : x ∈ M := hM ⟨x, hX⟩
  have hb := hS x hxM
  rw [hx, norm_zero] at hb
  have hn : ‖x‖ = 0 := by nlinarith [norm_nonneg x]
  exact norm_eq_zero.mp hn

/-- On an actual reflected zero window, support coercivity of the native
invariant probe would already force its entire positive displacement ledger
to vanish. This tests the varying-space coercive-return route at its real
RH instance rather than treating coercivity as a free structural fact. -/
theorem invariantProbe_support_coercivity_forces_zero
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : ReflectedWindow W)
    (M : Submodule ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
    (hM : (xi (ContinuousLinearMap.id ℝ
      (EuclideanSpace ℝ {ρ // ρ ∈ W})) (invariantProbe W)).range ≤ M)
    (c : ℝ) (hc : 0 < c)
    (hS : ∀ x ∈ M, c * ‖x‖ ≤ ‖invariantProbe W x‖) :
    windowEnergy m W = 0 := by
  have hv := native_coercive_on_own_residual_forces_injective
    (invariantProbe W) M hM c hc hS
    (displacementVector m W)
    (invariantProbe_displacement_zero m hm W hW)
  rw [← displacementVector_norm_sq m W, hv]
  simp

theorem pinv_id_real
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] :
    pinv (ContinuousLinearMap.id ℝ E) = ContinuousLinearMap.id ℝ E := by
  simpa [Submodule.starProjection_top] using
    pinv_comp (ContinuousLinearMap.id ℝ E)

/-- The exact original-energy currency law behind XI's promotion theorem.
It applies to arbitrary positive audits, including the identity audit on
RH zero windows and the Sobolev Gram audit used by the read-only Navier
physical membrane. It supplies an operator identity, not either problem's
independent closure payment. -/
theorem originalEnergyCurrencyDecomposition
    {E F G : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [NormedAddCommGroup F]
    [InnerProductSpace ℝ F] [FiniteDimensional ℝ F]
    [NormedAddCommGroup G] [InnerProductSpace ℝ G]
    [FiniteDimensional ℝ G]
    (C : E →L[ℝ] E) (hC : C.IsPositive)
    (D : E →L[ℝ] G) (L : E →L[ℝ] F) :
    auditCurrency C D =
      auditDecoder C D L ∘L auditCurrency C L ∘L (auditDecoder C D L)† +
        auditResidual C D L :=
  SixBirdsNeedles.XiCore.audit_currency_decomposition C hC D L

/-- The original-energy XI residual specializes exactly to the normalized
Schur residual when the audit energy is the identity. -/
theorem auditResidual_id_eq_xi
    {E F G : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [NormedAddCommGroup F]
    [InnerProductSpace ℝ F] [FiniteDimensional ℝ F]
    [NormedAddCommGroup G] [InnerProductSpace ℝ G]
    [FiniteDimensional ℝ G]
    (D : E →L[ℝ] G) (L : E →L[ℝ] F) :
    auditResidual (ContinuousLinearMap.id ℝ E) D L = xi D L := by
  simp [auditResidual, auditCurrency, auditDecoder, auditCross, xi, gram,
    decoder, pinv_id_real, ContinuousLinearMap.comp_assoc]

/-- For the identity audit and full target, the decoded native payment plus
the XI residual is exactly the full target currency for every native probe.
Changing the probe can move this currency between channels, but cannot
reduce their complete operator sum. -/
theorem fullReadout_complete_currency
    {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [NormedAddCommGroup F]
    [InnerProductSpace ℝ F] [FiniteDimensional ℝ F]
    (L : E →L[ℝ] F) :
    auditDecoder (ContinuousLinearMap.id ℝ E)
        (ContinuousLinearMap.id ℝ E) L ∘L
      auditCurrency (ContinuousLinearMap.id ℝ E) L ∘L
      (auditDecoder (ContinuousLinearMap.id ℝ E)
        (ContinuousLinearMap.id ℝ E) L)† +
      auditResidual (ContinuousLinearMap.id ℝ E)
        (ContinuousLinearMap.id ℝ E) L =
      ContinuousLinearMap.id ℝ E := by
  have h := originalEnergyCurrencyDecomposition
    (ContinuousLinearMap.id ℝ E) ContinuousLinearMap.isPositive_id
    (ContinuousLinearMap.id ℝ E) L
  simpa [auditCurrency, pinv_id_real] using h.symm

/-- Every native probe gives the same *complete* payment on the actual
zero-window state: decoded native currency plus XI residual is exactly the
positive RH ledger. This identity uses neither reflection symmetry nor an
analytic source estimate. -/
theorem window_complete_currency_eq_windowEnergy
    {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F]
    [FiniteDimensional ℝ F]
    (m : NontrivialZero → ℕ) (W : Finset NontrivialZero)
    (L : EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ] F) :
    RCLike.re (inner ℝ (displacementVector m W)
      ((auditDecoder (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
          (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W})) L ∘L
        auditCurrency (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W})) L ∘L
        (auditDecoder (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
          (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W})) L)† +
        auditResidual (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
          (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W})) L)
        (displacementVector m W))) = windowEnergy m W := by
  rw [fullReadout_complete_currency]
  simpa using displacementVector_norm_sq m W

/-- An off-line zero forces strictly positive *complete* payment for every
native probe. Making the residual vanish by changing the probe cannot erase
the cost, because the decoded native channel retains it. -/
theorem offLine_zero_forces_positive_complete_currency
    {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F]
    [FiniteDimensional ℝ F]
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (W : Finset NontrivialZero) (ρ : NontrivialZero) (hρ : ρ ∈ W)
    (hoff : displacement ρ ≠ 0)
    (L : EuclideanSpace ℝ {σ // σ ∈ W} →L[ℝ] F) :
    0 < RCLike.re (inner ℝ (displacementVector m W)
      ((auditDecoder (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {σ // σ ∈ W}))
          (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {σ // σ ∈ W})) L ∘L
        auditCurrency (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {σ // σ ∈ W})) L ∘L
        (auditDecoder (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {σ // σ ∈ W}))
          (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {σ // σ ∈ W})) L)† +
        auditResidual (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {σ // σ ∈ W}))
          (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {σ // σ ∈ W})) L)
        (displacementVector m W))) := by
  rw [window_complete_currency_eq_windowEnergy]
  have hterm : 0 < (m ρ : ℝ) * displacement ρ ^ 2 :=
    mul_pos (Nat.cast_pos.mpr (hm ρ)) (sq_pos_of_ne_zero hoff)
  exact hterm.trans_le (term_le_window m W ρ hρ)

/-- A native observation with a nonzero blind vector cannot have zero
full-readout XI residual. This is an obstruction to obtaining the RH budget
from symmetry alone. -/
theorem fullReadout_residual_ne_zero_of_native_blind_vector
    {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [NormedAddCommGroup F]
    [InnerProductSpace ℝ F] [FiniteDimensional ℝ F]
    (L : E →L[ℝ] F) (v : E) (hv : L v = 0) (hne : v ≠ 0) :
    auditResidual (ContinuousLinearMap.id ℝ E)
      (ContinuousLinearMap.id ℝ E) L ≠ 0 := by
  intro hzero
  have hq := xi_fullReadout_native_kernel v L hv
  rw [← auditResidual_id_eq_xi, hzero] at hq
  simp only [ContinuousLinearMap.zero_apply, inner_zero_right, map_zero] at hq
  have hn : ‖v‖ = 0 := by nlinarith [norm_nonneg v]
  exact hne (norm_eq_zero.mp hn)

/-- A two-coordinate calibration where the native probe is genuinely
nonzero yet the fixed full-target XI residual cannot vanish. -/
def twoChannelNative : EuclideanSpace ℝ (Fin 2) →L[ℝ] ℝ :=
  innerSL ℝ (WithLp.toLp 2 ![(1 : ℝ), 0])

def twoChannelBlind : EuclideanSpace ℝ (Fin 2) :=
  WithLp.toLp 2 ![(0 : ℝ), 1]

theorem twoChannelNative_blind : twoChannelNative twoChannelBlind = 0 := by
  norm_num [twoChannelNative, twoChannelBlind, EuclideanSpace.inner_toLp_toLp,
    dotProduct]

theorem twoChannelBlind_ne_zero : twoChannelBlind ≠ 0 := by
  intro h
  have h1 := congrArg (fun x : EuclideanSpace ℝ (Fin 2) => x 1) h
  norm_num [twoChannelBlind] at h1

theorem twoChannel_residual_nonzero :
    auditResidual (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ (Fin 2)))
      (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ (Fin 2))) twoChannelNative ≠ 0 :=
  fullReadout_residual_ne_zero_of_native_blind_vector
    twoChannelNative twoChannelBlind twoChannelNative_blind twoChannelBlind_ne_zero

/-- Setting the native observation equal to the whole target makes XI zero,
but leaves the complete target value in native currency. This cannot be
counted as an independent payment of the RH window ledger. -/
theorem fullNative_residual_zero
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] :
    auditResidual (ContinuousLinearMap.id ℝ E)
      (ContinuousLinearMap.id ℝ E) (ContinuousLinearMap.id ℝ E) = 0 := by
  rw [auditResidual_id_eq_xi]
  have h := exact_adequacy (ContinuousLinearMap.id ℝ E)
    (ContinuousLinearMap.id ℝ E)
  apply h.1.mpr
  apply h.2.1.mpr
  exact ⟨ContinuousLinearMap.id ℝ E, by simp⟩

/-- A native observation determined by the invariant probe alone. It reads
the entire subspace that the invariant sum misses, without using the
displacement vector to define the operator. -/
def blindSubspaceNative (W : Finset NontrivialZero) :
    EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ]
      EuclideanSpace ℝ {ρ // ρ ∈ W} :=
  (invariantProbe W).ker.starProjection

theorem blindSubspaceNative_displacement
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : ReflectedWindow W) :
    blindSubspaceNative W (displacementVector m W) =
      displacementVector m W := by
  exact Submodule.starProjection_eq_self_iff.mpr
    (invariantProbe_displacement_zero m hm W hW)

/-- This probe can make the residual vanish on the actual RH state
unconditionally; residual vanishing alone is therefore no RH return once
the native probe is allowed to change. -/
theorem blindSubspaceNative_actual_residual_zero
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : ReflectedWindow W) :
    RCLike.re (inner ℝ (displacementVector m W)
      ((auditResidual (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (blindSubspaceNative W)) (displacementVector m W))) = 0 := by
  rw [auditResidual_id_eq_xi, projection_identity, gram_quadratic]
  simp only [residualMap, ContinuousLinearMap.id_comp, adjoint_projection]
  change ‖((blindSubspaceNative W).ker.starProjection)
    (displacementVector m W)‖ ^ 2 = 0
  have hv : displacementVector m W ∈ (blindSubspaceNative W).kerᗮ := by
    rw [blindSubspaceNative, Submodule.ker_starProjection]
    exact (invariantProbe W).ker.le_orthogonal_orthogonal
      (invariantProbe_displacement_zero m hm W hW)
  rw [(Submodule.starProjection_apply_eq_zero_iff (K :=
    (blindSubspaceNative W).ker)).mpr hv]
  simp

/-- The same probe moves the whole RH window energy into native currency.
Its zero XI residual is a reclassification of the cost, not an estimate
that would force the displacement to vanish. -/
theorem blindSubspaceNative_actual_currency_eq_windowEnergy
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : ReflectedWindow W) :
    RCLike.re (inner ℝ (displacementVector m W)
      ((auditCurrency (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (blindSubspaceNative W)) (displacementVector m W))) =
      windowEnergy m W := by
  rw [show auditCurrency (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
    (blindSubspaceNative W) = gram (blindSubspaceNative W) by
      simp [auditCurrency, gram, pinv_id_real]]
  rw [gram_quadratic]
  simp only [blindSubspaceNative, adjoint_projection]
  rw [show (invariantProbe W).ker.starProjection (displacementVector m W) =
      displacementVector m W from
    blindSubspaceNative_displacement m hm W hW]
  exact displacementVector_norm_sq m W

/-- False-target control: if a window contains an off-line zero, this
state-independent native probe still has zero XI residual on the actual
state, while its native currency is strictly positive. -/
theorem blindSubspaceNative_offLine_control
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (hsym : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : ReflectedWindow W)
    (ρ : NontrivialZero) (hρ : ρ ∈ W)
    (hoff : displacement ρ ≠ 0) :
    RCLike.re (inner ℝ (displacementVector m W)
      ((auditResidual (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {σ // σ ∈ W}))
        (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {σ // σ ∈ W}))
        (blindSubspaceNative W)) (displacementVector m W))) = 0 ∧
    0 < RCLike.re (inner ℝ (displacementVector m W)
      ((auditCurrency (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {σ // σ ∈ W}))
        (blindSubspaceNative W)) (displacementVector m W))) := by
  refine ⟨blindSubspaceNative_actual_residual_zero m hsym W hW, ?_⟩
  rw [blindSubspaceNative_actual_currency_eq_windowEnergy m hsym W hW]
  have hterm : 0 < (m ρ : ℝ) * displacement ρ ^ 2 :=
    mul_pos (Nat.cast_pos.mpr (hm ρ)) (sq_pos_of_ne_zero hoff)
  exact hterm.trans_le (term_le_window m W ρ hρ)

/-- The Navier-style native/residual/transport payment cannot have a
vanishing *operator* transport constant for the RH full-identity target on a
nonzero carrier. XI promotion already forces the full identity currency
below that transport scalar, so its scalar is at least one. This is an
operator-level obstruction independent of the actual zero state. -/
theorem fullReadout_transport_floor
    {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [NormedAddCommGroup F]
    [InnerProductSpace ℝ F] [FiniteDimensional ℝ F]
    (v : E) (hv : v ≠ 0) (L : E →L[ℝ] F)
    (Theta : F →L[ℝ] F) (Omega : E →L[ℝ] E) (H : ℝ)
    (hL : Loewner
      (auditCurrency (ContinuousLinearMap.id ℝ E) L) Theta)
    (hXi : Loewner
      (auditResidual (ContinuousLinearMap.id ℝ E)
        (ContinuousLinearMap.id ℝ E) L) Omega)
    (htransport : Loewner
      (auditDecoder (ContinuousLinearMap.id ℝ E)
        (ContinuousLinearMap.id ℝ E) L ∘L Theta ∘L
        (auditDecoder (ContinuousLinearMap.id ℝ E)
          (ContinuousLinearMap.id ℝ E) L)† + Omega)
      (H • ContinuousLinearMap.id ℝ E)) :
    1 ≤ H := by
  have hC : (ContinuousLinearMap.id ℝ E).IsPositive :=
    ContinuousLinearMap.isPositive_id
  have hfull := audit_promotion (ContinuousLinearMap.id ℝ E) hC
    (ContinuousLinearMap.id ℝ E) L Theta Omega hL hXi
  have hbound := (hfull v).trans (htransport v)
  have hscalar : inner ℝ v v ≤ H * inner ℝ v v := by
    simpa [auditCurrency, pinv_id_real, real_inner_smul_right] using hbound
  exact (mul_le_mul_iff_of_pos_right (real_inner_self_pos.mpr hv)).mp (by
    simpa only [one_mul] using hscalar)

/-- Every nonempty zero window has a nonzero coordinate carrier. Thus the
same native/residual/transport conditions used by the physical membrane
force its scalar operator payment to be at least one on the RH full target,
regardless of whether the actual zero displacement vanishes. -/
theorem window_fullReadout_transport_floor
    (W : Finset NontrivialZero) (hW : W.Nonempty)
    (L : EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ] ℝ)
    (Theta : ℝ →L[ℝ] ℝ)
    (Omega : EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ]
      EuclideanSpace ℝ {ρ // ρ ∈ W}) (H : ℝ)
    (hL : Loewner
      (auditCurrency (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W})) L)
      Theta)
    (hXi : Loewner
      (auditResidual (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W})) L) Omega)
    (htransport : Loewner
      (auditDecoder (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W})) L ∘L
        Theta ∘L
        (auditDecoder (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
          (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W})) L)† + Omega)
      (H • ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))) :
    1 ≤ H := by
  obtain ⟨ρ, hρ⟩ := hW
  have hv : invariantVector W ≠ 0 := by
    intro h
    have hc := congrArg
      (fun x : EuclideanSpace ℝ {ρ // ρ ∈ W} => x ⟨ρ, hρ⟩) h
    norm_num [invariantVector] at hc
  exact fullReadout_transport_floor (invariantVector W) hv L Theta Omega H
    hL hXi htransport

/-- This is an exact, nonzero-native-probe XI realization of each reflected
finite zero window. The target is the classical displacement vector; the
native probe records its invariant sum, which cancels by the functional
equation. The equality supplies no bound on the residual. -/
theorem xi_window_quadratic_eq_windowEnergy
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : ReflectedWindow W) :
    RCLike.re (inner ℝ (1 : ℝ)
      ((xi (innerSL ℝ (displacementVector m W)) (invariantProbe W)) 1)) =
      windowEnergy m W := by
  calc
    _ = ‖displacementVector m W‖ ^ 2 :=
      xi_rankOne_native_kernel _ _ (invariantProbe_displacement_zero m hm W hW)
    _ = windowEnergy m W := displacementVector_norm_sq m W

/-- The same exact identity in the original-energy XI API used by the
Navier--Stokes physical membrane. -/
theorem auditResidual_window_quadratic_eq_windowEnergy
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : ReflectedWindow W) :
    RCLike.re (inner ℝ (1 : ℝ)
      ((auditResidual (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (innerSL ℝ (displacementVector m W)) (invariantProbe W)) 1)) =
      windowEnergy m W := by
  rw [auditResidual_id_eq_xi]
  exact xi_window_quadratic_eq_windowEnergy m hm W hW

/-- The tighter fixed-target model: the target map is the identity on the
finite zero window, and the actual displacement vector is the tested state.
This is analogous to the fixed physical target map evaluated on an actual
Navier--Stokes state. It still supplies no analytic residual budget. -/
theorem fixedTarget_window_quadratic_eq_windowEnergy
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : ReflectedWindow W) :
    RCLike.re (inner ℝ (displacementVector m W)
      ((auditResidual (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (invariantProbe W)) (displacementVector m W))) =
      windowEnergy m W := by
  rw [auditResidual_id_eq_xi]
  exact (xi_fullReadout_native_kernel _ _
    (invariantProbe_displacement_zero m hm W hW)).trans
      (displacementVector_norm_sq m W)

/-- The exact RH instance of the XI operator-residual payment shape used
in the Navier--Stokes physical membrane. The operator bound is an explicit
premise; the conclusion is only its evaluation on the actual zero state. -/
theorem windowEnergy_le_operatorResidualBudget
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : ReflectedWindow W)
    (Omega : EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ]
      EuclideanSpace ℝ {ρ // ρ ∈ W})
    (hXi : Loewner
      (auditResidual (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (invariantProbe W)) Omega) :
    windowEnergy m W ≤
      RCLike.re (inner ℝ (displacementVector m W)
        (Omega (displacementVector m W))) := by
  rw [← fixedTarget_window_quadratic_eq_windowEnergy m hm W hW]
  exact hXi (displacementVector m W)

/-- An off-line zero makes the exact XI residual strictly positive in any
reflected window that contains it. This is a false-target control on the
finite construction, not a claim that such a zero exists. -/
theorem offLine_zero_forces_positive_xi
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (hsym : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : ReflectedWindow W)
    (ρ : NontrivialZero) (hρ : ρ ∈ W) (hoff : displacement ρ ≠ 0) :
    0 < RCLike.re (inner ℝ (1 : ℝ)
      ((auditResidual (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (innerSL ℝ (displacementVector m W)) (invariantProbe W)) 1)) := by
  rw [auditResidual_window_quadratic_eq_windowEnergy m hsym W hW]
  have hterm : 0 < (m ρ : ℝ) * displacement ρ ^ 2 :=
    mul_pos (Nat.cast_pos.mpr (hm ρ)) (sq_pos_of_ne_zero hoff)
  exact hterm.trans_le (term_le_window m W ρ hρ)

theorem offLine_zero_forces_positive_fixedTarget_xi
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (hsym : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : ReflectedWindow W)
    (ρ : NontrivialZero) (hρ : ρ ∈ W) (hoff : displacement ρ ≠ 0) :
    0 < RCLike.re (inner ℝ (displacementVector m W)
      ((auditResidual (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (invariantProbe W)) (displacementVector m W))) := by
  rw [fixedTarget_window_quadratic_eq_windowEnergy m hsym W hW]
  have hterm : 0 < (m ρ : ℝ) * displacement ρ ^ 2 :=
    mul_pos (Nat.cast_pos.mpr (hm ρ)) (sq_pos_of_ne_zero hoff)
  exact hterm.trans_le (term_le_window m W ρ hρ)

/-- Every zero enters some permanent finite window. This is an explicit
coverage obligation; a finite sample by itself cannot establish RH. -/
def EventuallyCovered (W : ℕ → Finset NontrivialZero) : Prop :=
  ∀ ρ : NontrivialZero, ∀ᶠ n in atTop, ρ ∈ W n

/-- An explicit exhaustive sequence from any encoding of the actual
completed-zeta zero subtype. The imported analytic countability theorem
supplies such an encoding noncomputably. -/
def codedWindow [Encodable NontrivialZero] (n : ℕ) : Finset NontrivialZero :=
  by
    classical
    exact (Finset.range n).biUnion fun k => (Encodable.decode k : Option NontrivialZero).toFinset

theorem codedWindow_eventuallyCovered [Encodable NontrivialZero] :
    EventuallyCovered codedWindow := by
  classical
  intro ρ
  apply Filter.eventually_atTop.2
  refine ⟨Encodable.encode ρ + 1, ?_⟩
  intro n hn
  simp only [codedWindow, Finset.mem_biUnion]
  refine ⟨Encodable.encode ρ, Finset.mem_range.mpr (by omega), ?_⟩
  simp [Encodable.encodek]

theorem codedReflectedWindow_eventuallyCovered [Encodable NontrivialZero] :
    EventuallyCovered (fun n => closeReflection (codedWindow n)) :=
  closeReflection_eventuallyCovered codedWindow codedWindow_eventuallyCovered

theorem codedReflectedWindow_reflected [Encodable NontrivialZero] (n : ℕ) :
    ReflectedWindow (closeReflection (codedWindow n)) :=
  closeReflection_reflected (codedWindow n)

/-- Countability of the completed-zeta zero set gives an unconditional
existence theorem for exhaustive, reflection-closed finite windows. -/
theorem exists_reflected_eventuallyCovered :
    ∃ W : ℕ → Finset NontrivialZero,
      (∀ n, ReflectedWindow (W n)) ∧ EventuallyCovered W := by
  letI : Countable NontrivialZero :=
    ClassicalZeroCountable.nontrivialZero_countable
  letI : Encodable NontrivialZero := Encodable.ofCountable _
  exact ⟨fun n => closeReflection (codedWindow n),
    codedReflectedWindow_reflected, codedReflectedWindow_eventuallyCovered⟩

/-- A fixed exhaustive family of reflected windows on actual completed-zeta
zeros. Its existence follows from the imported zero-countability theorem. -/
def canonicalReflectedWindow : ℕ → Finset NontrivialZero :=
  Classical.choose exists_reflected_eventuallyCovered

theorem canonicalReflectedWindow_reflected (n : ℕ) :
    ReflectedWindow (canonicalReflectedWindow n) :=
  (Classical.choose_spec exists_reflected_eventuallyCovered).1 n

theorem canonicalReflectedWindow_eventuallyCovered :
    EventuallyCovered canonicalReflectedWindow :=
  (Classical.choose_spec exists_reflected_eventuallyCovered).2

/-- A genuine vanishing budget on exhaustive windows gives critical-strip RH.
The budget hypothesis is RH-strength and is not supplied by this theorem. -/
theorem criticalStripRH_of_exhaustive_vanishing_budget
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (W : ℕ → Finset NontrivialZero) (hcover : EventuallyCovered W)
    (b : ℕ → ℝ) (hb : Tendsto b atTop (𝓝 0))
    (hbudget : ∀ n, windowEnergy m (W n) ≤ b n) : CriticalStripRH := by
  intro s hz hlo hhi
  let ρ : NontrivialZero :=
    ⟨s, (completed_zero_iff_zeta_zero_of_re_pos s hlo).mpr hz, hlo, hhi⟩
  have hevent : ∀ᶠ n in atTop, (m ρ : ℝ) * displacement ρ ^ 2 ≤ b n :=
    (hcover ρ).mono fun n hn => (term_le_window m (W n) ρ hn).trans (hbudget n)
  have hnonpos : (m ρ : ℝ) * displacement ρ ^ 2 ≤ 0 :=
    le_of_tendsto_of_tendsto tendsto_const_nhds hb hevent
  have hmpos : (0 : ℝ) < m ρ := Nat.cast_pos.mpr (hm ρ)
  have hsq : displacement ρ ^ 2 ≤ 0 := by
    nlinarith [sq_nonneg (displacement ρ)]
  have hzero : displacement ρ = 0 := by nlinarith [sq_nonneg (displacement ρ)]
  exact sub_eq_zero.mp hzero

/-- A proposed use of the varying-space coercive XI return with the native
invariant probe as delivery map already assumes enough support coercivity to
prove RH. The missing datum is not merely a dimension-uniform constant:
even pointwise positive coercivity on the residual support forces zero window
energy. -/
theorem criticalStripRH_of_invariantProbe_support_coercivity
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (hsym : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : ℕ → Finset NontrivialZero)
    (hW : ∀ n, ReflectedWindow (W n))
    (hcover : EventuallyCovered W)
    (M : ∀ n, Submodule ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W n}))
    (hM : ∀ n, (xi (ContinuousLinearMap.id ℝ
      (EuclideanSpace ℝ {ρ // ρ ∈ W n})) (invariantProbe (W n))).range ≤ M n)
    (c : ℕ → ℝ) (hc : ∀ n, 0 < c n)
    (hS : ∀ n x, x ∈ M n → c n * ‖x‖ ≤ ‖invariantProbe (W n) x‖) :
    CriticalStripRH := by
  apply criticalStripRH_of_exhaustive_vanishing_budget m hm W hcover
    (fun _ => 0) tendsto_const_nhds
  intro n
  rw [invariantProbe_support_coercivity_forces_zero m hsym (W n) (hW n)
    (M n) (hM n) (c n) (hc n) (hS n)]

/-- The precise RH closure condition phrased in the same original-energy XI
residual API used by the Navier--Stokes physical membrane. The existence of
these budgets is the unresolved RH-strength analytic obligation. -/
theorem criticalStripRH_of_exhaustive_xi_budget
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (hsym : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : ℕ → Finset NontrivialZero)
    (hW : ∀ n, ReflectedWindow (W n))
    (hcover : EventuallyCovered W)
    (b : ℕ → ℝ) (hb : Tendsto b atTop (𝓝 0))
    (hxi : ∀ n,
      RCLike.re (inner ℝ (1 : ℝ)
        ((auditResidual
          (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W n}))
          (innerSL ℝ (displacementVector m (W n))) (invariantProbe (W n))) 1)) ≤ b n) :
    CriticalStripRH := by
  apply criticalStripRH_of_exhaustive_vanishing_budget m hm W hcover b hb
  intro n
  rw [← auditResidual_window_quadratic_eq_windowEnergy m hsym (W n) (hW n)]
  exact hxi n

/-- The fixed-target version is the preferred comparator to the physical
Navier--Stokes membrane: `D = id` is frozen before the zero displacement
state is evaluated. The scalar budget is still RH-strength. -/
theorem criticalStripRH_of_fixedTarget_xi_budget
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (hsym : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : ℕ → Finset NontrivialZero)
    (hW : ∀ n, ReflectedWindow (W n))
    (hcover : EventuallyCovered W)
    (b : ℕ → ℝ) (hb : Tendsto b atTop (𝓝 0))
    (hxi : ∀ n,
      RCLike.re (inner ℝ (displacementVector m (W n))
        ((auditResidual
          (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W n}))
          (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W n}))
          (invariantProbe (W n))) (displacementVector m (W n)))) ≤ b n) :
    CriticalStripRH := by
  apply criticalStripRH_of_exhaustive_vanishing_budget m hm W hcover b hb
  intro n
  rw [← fixedTarget_window_quadratic_eq_windowEnergy m hsym (W n) (hW n)]
  exact hxi n

/-- If a source independently supplies the same operator payment shape as
the Navier physical witness, and its actual-state charge vanishes along
exhaustive windows, then RH follows. Neither premise is constructed here. -/
theorem criticalStripRH_of_operatorResidualBudget
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (hsym : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : ℕ → Finset NontrivialZero)
    (hW : ∀ n, ReflectedWindow (W n))
    (hcover : EventuallyCovered W)
    (Omega : ∀ n, EuclideanSpace ℝ {ρ // ρ ∈ W n} →L[ℝ]
      EuclideanSpace ℝ {ρ // ρ ∈ W n})
    (hXi : ∀ n, Loewner
      (auditResidual (ContinuousLinearMap.id ℝ
        (EuclideanSpace ℝ {ρ // ρ ∈ W n}))
        (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W n}))
        (invariantProbe (W n))) (Omega n))
    (b : ℕ → ℝ) (hb : Tendsto b atTop (𝓝 0))
    (hpaid : ∀ n,
      RCLike.re (inner ℝ (displacementVector m (W n))
        ((Omega n) (displacementVector m (W n)))) ≤ b n) :
    CriticalStripRH := by
  apply criticalStripRH_of_exhaustive_vanishing_budget m hm W hcover b hb
  intro n
  exact (windowEnergy_le_operatorResidualBudget m hsym (W n) (hW n)
    (Omega n) (hXi n)).trans (hpaid n)

/-- A budget of zero for every exhaustive reflected window is equivalent to
critical-strip RH. Thus calling that budget "strong closure" without an
independent analytic source would only repackage the target. -/
theorem exhaustive_xi_zero_iff_criticalStripRH
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (hsym : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : ℕ → Finset NontrivialZero)
    (hW : ∀ n, ReflectedWindow (W n))
    (hcover : EventuallyCovered W) :
    (∀ n,
      RCLike.re (inner ℝ (1 : ℝ)
        ((auditResidual
          (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W n}))
          (innerSL ℝ (displacementVector m (W n))) (invariantProbe (W n))) 1)) = 0) ↔
      CriticalStripRH := by
  constructor
  · intro hzero
    apply criticalStripRH_of_exhaustive_xi_budget m hm hsym W hW hcover
      (fun _ => 0) tendsto_const_nhds
    intro n
    rw [hzero n]
  · intro hRH n
    rw [auditResidual_window_quadratic_eq_windowEnergy m hsym (W n) (hW n)]
    apply (windowEnergy_eq_zero_iff m hm (W n)).mpr
    intro ρ _
    exact sub_eq_zero.mpr (hRH ρ.val
      ((completed_zero_iff_zeta_zero_of_re_pos ρ.val ρ.property.2.1).mp ρ.property.1)
      ρ.property.2.1 ρ.property.2.2)

/-- The same equivalence for the fixed target map. The quadratic is
evaluated on the actual displacement state, not all test directions. -/
theorem exhaustive_fixedTarget_xi_zero_iff_criticalStripRH
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (hsym : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : ℕ → Finset NontrivialZero)
    (hW : ∀ n, ReflectedWindow (W n))
    (hcover : EventuallyCovered W) :
    (∀ n,
      RCLike.re (inner ℝ (displacementVector m (W n))
        ((auditResidual
          (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W n}))
          (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W n}))
          (invariantProbe (W n))) (displacementVector m (W n)))) = 0) ↔
      CriticalStripRH := by
  constructor
  · intro hzero
    apply criticalStripRH_of_fixedTarget_xi_budget m hm hsym W hW hcover
      (fun _ => 0) tendsto_const_nhds
    intro n
    rw [hzero n]
  · intro hRH n
    rw [fixedTarget_window_quadratic_eq_windowEnergy m hsym (W n) (hW n)]
    apply (windowEnergy_eq_zero_iff m hm (W n)).mpr
    intro ρ _
    exact sub_eq_zero.mpr (hRH ρ.val
      ((completed_zero_iff_zeta_zero_of_re_pos ρ.val ρ.property.2.1).mp ρ.property.1)
      ρ.property.2.1 ρ.property.2.2)

/-- Even allowing a merely vanishing upper sequence, the existence of a
fixed-target scalar XI payment on exhaustive windows is equivalent to RH.
Thus the budget must be independently derived from zeta data to explain RH. -/
theorem exists_vanishing_fixedTarget_xi_budget_iff_criticalStripRH
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (hsym : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : ℕ → Finset NontrivialZero)
    (hW : ∀ n, ReflectedWindow (W n))
    (hcover : EventuallyCovered W) :
    (∃ b : ℕ → ℝ, Tendsto b atTop (𝓝 0) ∧
      ∀ n,
        RCLike.re (inner ℝ (displacementVector m (W n))
          ((auditResidual
            (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W n}))
            (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W n}))
            (invariantProbe (W n))) (displacementVector m (W n)))) ≤ b n) ↔
      CriticalStripRH := by
  constructor
  · rintro ⟨b, hb, hbudget⟩
    exact criticalStripRH_of_fixedTarget_xi_budget m hm hsym W hW hcover b hb hbudget
  · intro hRH
    refine ⟨fun _ => 0, tendsto_const_nhds, ?_⟩
    intro n
    rw [(exhaustive_fixedTarget_xi_zero_iff_criticalStripRH
      m hm hsym W hW hcover).mpr hRH n]

/-- With no independent restriction on `Omega`, even the existence of a
Loewner operator payment whose actual-state charge tends to zero is RH-
equivalent. The reverse direction may choose the residual operator itself. -/
theorem exists_operatorResidualBudget_iff_criticalStripRH
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (hsym : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : ℕ → Finset NontrivialZero)
    (hW : ∀ n, ReflectedWindow (W n))
    (hcover : EventuallyCovered W) :
    (∃ Omega : ∀ n, EuclideanSpace ℝ {ρ // ρ ∈ W n} →L[ℝ]
        EuclideanSpace ℝ {ρ // ρ ∈ W n},
      (∀ n, Loewner
        (auditResidual (ContinuousLinearMap.id ℝ
          (EuclideanSpace ℝ {ρ // ρ ∈ W n}))
          (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W n}))
          (invariantProbe (W n))) (Omega n)) ∧
      ∃ b : ℕ → ℝ, Tendsto b atTop (𝓝 0) ∧
        ∀ n,
          RCLike.re (inner ℝ (displacementVector m (W n))
            ((Omega n) (displacementVector m (W n)))) ≤ b n) ↔
      CriticalStripRH := by
  constructor
  · rintro ⟨Omega, hXi, b, hb, hpaid⟩
    exact criticalStripRH_of_operatorResidualBudget m hm hsym W hW hcover
      Omega hXi b hb hpaid
  · intro hRH
    let Omega : ∀ n, EuclideanSpace ℝ {ρ // ρ ∈ W n} →L[ℝ]
        EuclideanSpace ℝ {ρ // ρ ∈ W n} := fun n =>
      auditResidual (ContinuousLinearMap.id ℝ
        (EuclideanSpace ℝ {ρ // ρ ∈ W n}))
        (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W n}))
        (invariantProbe (W n))
    refine ⟨Omega, ?_, fun _ => 0, tendsto_const_nhds, ?_⟩
    · intro n x
      exact le_refl _
    · intro n
      change RCLike.re (inner ℝ (displacementVector m (W n))
        ((auditResidual
          (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W n}))
          (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W n}))
          (invariantProbe (W n))) (displacementVector m (W n)))) ≤ 0
      rw [(exhaustive_fixedTarget_xi_zero_iff_criticalStripRH
        m hm hsym W hW hcover).mpr hRH n]

/-- A bare finite total over the successive complete charges of any
eventually exhaustive zero windows is already equivalent to critical-strip
RH. This tests and rejects a proposed common closure premise that merely
asks for integrability of the actual target charge. A useful shared
principle must derive such payment from independent operation laws. -/
theorem summable_windowEnergy_iff_criticalStripRH
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (W : ℕ → Finset NontrivialZero) (hcover : EventuallyCovered W) :
    Summable (fun n => windowEnergy m (W n)) ↔ CriticalStripRH := by
  constructor
  · intro hs
    exact criticalStripRH_of_exhaustive_vanishing_budget m hm W hcover
      (fun n => windowEnergy m (W n)) hs.tendsto_atTop_zero
      (fun _ => le_refl _)
  · intro hRH
    have hz : ∀ n, windowEnergy m (W n) = 0 := by
      intro n
      apply (windowEnergy_eq_zero_iff m hm (W n)).mpr
      intro ρ _
      exact sub_eq_zero.mpr (hRH ρ.val
        ((completed_zero_iff_zeta_zero_of_re_pos ρ.val ρ.property.2.1).mp
          ρ.property.1)
        ρ.property.2.1 ρ.property.2.2)
    simpa only [hz] using (summable_zero : Summable (fun _ : ℕ => (0 : ℝ)))

set_option maxRecDepth 2048 in
/-- The fixed Hilbert XI kernel projection agrees with the finite Schur
residual on the actual zero window. The same Hilbert absorption theorem is
used for the Navier strong Fourier state. -/
theorem windowEnergy_zero_via_hilbert_xi_absorption
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : ReflectedWindow W)
    (q : ℝ) (hq : q < 1)
    (hgap : RCLike.re (inner ℝ (displacementVector m W)
      ((auditResidual
        (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (invariantProbe W)) (displacementVector m W))) ≤
      q * windowEnergy m W) :
    windowEnergy m W = 0 := by
  let v := displacementVector m W
  let L := invariantProbe W
  let C := ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W})
  have hvker : v ∈ L.ker :=
    invariantProbe_displacement_zero m hm W hW
  have hxi : hilbertKernelXi L v = v :=
    L.ker.starProjection_eq_self_iff.mpr hvker
  have hnative : hilbertNativeCurrency L v = 0 :=
    L.ker.starProjection_orthogonal_apply_eq_zero hvker
  have hschur : auditResidual C C L = hilbertKernelXi L :=
    auditResidual_id_eq_hilbertKernelXi L
  have hres : ‖hilbertKernelXi L v‖ ^ 2 ≤ q * ‖v‖ ^ 2 := by
    have hh := hgap
    change inner ℝ v ((auditResidual C C L) v) ≤ q * windowEnergy m W at hh
    rw [hschur, hxi, ← displacementVector_norm_sq] at hh
    rw [hxi]
    simpa [v, real_inner_self_eq_norm_sq] using hh
  have hn : ‖hilbertNativeCurrency L v‖ ^ 2 ≤ (0 : ℝ) := by
    rw [hnative]
    norm_num
  have hb := hilbert_xi_absorption L v 0 q hq hn hres
  have hb' : ‖v‖ ^ 2 ≤ 0 := by simpa using hb
  rw [displacementVector_norm_sq] at hb'
  exact le_antisymm hb' (by rw [← displacementVector_norm_sq]; positivity)

/-- The common varying-carrier strong XI closure on actual reflected zero
windows reaches the classical critical-strip statement. The native budget
is proved zero from symmetry, not supplied as another premise. -/
theorem criticalStripRH_of_subunitKernelXiFamily
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (hsym : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : ℕ → Finset NontrivialZero)
    (hW : ∀ n, ReflectedWindow (W n))
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
      invariantProbe_displacement_zero m hsym (W n) (hW n)
    change ‖(invariantProbe (W n)).kerᗮ.starProjection
      (displacementVector m (W n))‖ ^ 2 ≤ 0
    rw [(invariantProbe (W n)).ker.starProjection_orthogonal_apply_eq_zero hvker]
    norm_num
  obtain ⟨q, _, hq, hbound⟩ :=
    SubunitKernelXiFamily.full_bounds (fun _ : ℕ => True)
      (fun n => invariantProbe (W n))
      (fun n => displacementVector m (W n))
      (fun _ => (0 : ℝ)) hc hn
  apply (exhaustive_fixedTarget_xi_zero_iff_criticalStripRH
    m hm hsym W hW hcover).mp
  intro n
  rw [fixedTarget_window_quadratic_eq_windowEnergy m hsym (W n) (hW n),
    ← displacementVector_norm_sq]
  have hb := hbound n trivial
  have hb0 : ‖displacementVector m (W n)‖ ^ 2 ≤ 0 := by simpa using hb
  exact le_antisymm hb0 (sq_nonneg _)

/-- The sole unproved premise is the shared subunit kernel-XI closure on the
fixed family of actual zero-window states. Window coverage, reflection, and
positive weights are supplied by established constructions. -/
theorem criticalStripRH_of_canonical_subunitKernelXiClosure
    (hc : SubunitKernelXiFamily (fun _ : ℕ => True)
      (fun n => invariantProbe (canonicalReflectedWindow n))
      (fun n => displacementVector unitWeights (canonicalReflectedWindow n))) :
    CriticalStripRH :=
  criticalStripRH_of_subunitKernelXiFamily unitWeights unitWeights_positive
    unitWeights_reflection_symmetric canonicalReflectedWindow
    canonicalReflectedWindow_reflected canonicalReflectedWindow_eventuallyCovered hc

set_option maxRecDepth 2048 in
/-- The shared original-energy XI absorption law forces one actual reflected window to vanish:
the invariant native probe has zero decoded payment on its displacement. -/
theorem windowEnergy_zero_via_shared_xi_absorption
    (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : ReflectedWindow W)
    (q : ℝ) (hq : q < 1)
    (hgap : RCLike.re (inner ℝ (displacementVector m W)
      ((auditResidual
        (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (invariantProbe W)) (displacementVector m W))) ≤
      q * windowEnergy m W) :
    windowEnergy m W = 0 := by
  let v := displacementVector m W
  let L := invariantProbe W
  let C := ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W})
  have hres : inner ℝ v ((auditResidual C C L) v) = windowEnergy m W :=
    fixedTarget_window_quadratic_eq_windowEnergy m hm W hW
  have hfull : inner ℝ v ((auditCurrency C C) v) = windowEnergy m W := by
    simp [C, auditCurrency, pinv_id_real, v, displacementVector_norm_sq]
  have hsplit := congrArg
    (fun A : EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ]
      EuclideanSpace ℝ {ρ // ρ ∈ W} => inner ℝ v (A v))
    (audit_currency_decomposition C ContinuousLinearMap.isPositive_id C L)
  simp only [ContinuousLinearMap.add_apply, inner_add_right] at hsplit
  have hnative : inner ℝ v
      ((auditDecoder C C L ∘L auditCurrency C L ∘L
        (auditDecoder C C L)†) v) ≤ 0 := by
    rw [hfull, hres] at hsplit
    linarith
  have hresidual : inner ℝ v ((auditResidual C C L) v) ≤
      q * inner ℝ v ((auditCurrency C C) v) := by
    rw [hfull]
    exact hgap
  have hb := realized_audit_xi_absorption_real C
    ContinuousLinearMap.isPositive_id C L v 0 q hq hnative hresidual
  rw [hfull] at hb
  have hnonneg : 0 ≤ windowEnergy m W := by
    rw [← displacementVector_norm_sq]
    positivity
  have hb' : windowEnergy m W ≤ 0 := by simpa using hb
  exact le_antisymm hb' hnonneg

/-- A subunit residual fraction on the actual state is another exact RH
equivalent for the invariant native probe. Since that probe annihilates the
displacement, its XI residual already equals the whole target energy. This
calibrates the strength of the supplied conditional closure; the theorem does
not claim that the closure premise holds unconditionally. -/
theorem subunit_fixedTarget_xi_gap_iff_criticalStripRH
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (hsym : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : ℕ → Finset NontrivialZero)
    (hW : ∀ n, ReflectedWindow (W n))
    (hcover : EventuallyCovered W)
    (q : ℝ) (hq : q < 1) :
    (∀ n,
      RCLike.re (inner ℝ (displacementVector m (W n))
        ((auditResidual
          (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W n}))
          (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W n}))
          (invariantProbe (W n))) (displacementVector m (W n)))) ≤
        q * windowEnergy m (W n)) ↔ CriticalStripRH := by
  constructor
  · intro hgap
    apply (exhaustive_fixedTarget_xi_zero_iff_criticalStripRH
      m hm hsym W hW hcover).mp
    intro n
    have hz := windowEnergy_zero_via_hilbert_xi_absorption
      m hsym (W n) (hW n) q hq (hgap n)
    rw [fixedTarget_window_quadratic_eq_windowEnergy m hsym (W n) (hW n)]
    exact hz
  · intro hRH n
    have hz := (exhaustive_fixedTarget_xi_zero_iff_criticalStripRH
      m hm hsym W hW hcover).mpr hRH n
    rw [hz, ← fixedTarget_window_quadratic_eq_windowEnergy m hsym (W n) (hW n)]
    simp only [hz, mul_zero, le_refl]

/-- Calibration of the fixed canonical closure: on this native-blind RH
family, the supplied subunit condition is exactly classical critical-strip
RH. This records its logical strength; it is not an unconditional payment. -/
theorem canonical_subunitKernelXiClosure_iff_criticalStripRH :
    SubunitKernelXiFamily (fun _ : ℕ => True)
      (fun n => invariantProbe (canonicalReflectedWindow n))
      (fun n => displacementVector unitWeights (canonicalReflectedWindow n)) ↔
      CriticalStripRH := by
  constructor
  · exact criticalStripRH_of_canonical_subunitKernelXiClosure
  · intro hRH
    refine ⟨0, le_refl _, by norm_num, ?_⟩
    intro n _
    have hz := (exhaustive_fixedTarget_xi_zero_iff_criticalStripRH
      unitWeights unitWeights_positive unitWeights_reflection_symmetric
      canonicalReflectedWindow canonicalReflectedWindow_reflected
      canonicalReflectedWindow_eventuallyCovered).mpr hRH n
    rw [fixedTarget_window_quadratic_eq_windowEnergy unitWeights
      unitWeights_reflection_symmetric (canonicalReflectedWindow n)
      (canonicalReflectedWindow_reflected n)] at hz
    have hv : ‖displacementVector unitWeights
        (canonicalReflectedWindow n)‖ ^ 2 = 0 := by
      rwa [displacementVector_norm_sq]
    have hv0 : displacementVector unitWeights (canonicalReflectedWindow n) = 0 := by
      apply norm_eq_zero.mp
      nlinarith [norm_nonneg (displacementVector unitWeights
        (canonicalReflectedWindow n))]
    simp [hv0]

/-- A formal two-coordinate reflection model, not an assertion of actual
off-line zeta zeros. It isolates the exact information supplied by symmetry
and XI before any zeta-specific source law is added. -/
def reflectedPairVector : EuclideanSpace ℝ (Fin 2) :=
  WithLp.toLp 2 ![(1 : ℝ), -1]

def reflectedPairInvariantProbe : EuclideanSpace ℝ (Fin 2) →L[ℝ] ℝ :=
  innerSL ℝ (WithLp.toLp 2 ![(1 : ℝ), 1])

def reflectedPairSwap (v : EuclideanSpace ℝ (Fin 2)) :
    EuclideanSpace ℝ (Fin 2) :=
  WithLp.toLp 2 ![v 1, v 0]

theorem reflectedPairSwap_involutive (v : EuclideanSpace ℝ (Fin 2)) :
    reflectedPairSwap (reflectedPairSwap v) = v := by
  ext i
  fin_cases i <;> rfl

theorem reflectedPairSwap_displacement :
    reflectedPairSwap reflectedPairVector = -reflectedPairVector := by
  ext i
  fin_cases i <;> norm_num [reflectedPairSwap, reflectedPairVector]

theorem reflectedPair_invariant_blind :
    reflectedPairInvariantProbe reflectedPairVector = 0 := by
  norm_num [reflectedPairInvariantProbe, reflectedPairVector,
    EuclideanSpace.inner_toLp_toLp, dotProduct]

theorem reflectedPairInvariantProbe_ne_zero : reflectedPairInvariantProbe ≠ 0 := by
  intro h
  have hc := congrArg (fun f : EuclideanSpace ℝ (Fin 2) →L[ℝ] ℝ =>
    f (WithLp.toLp 2 ![(1 : ℝ), 1])) h
  norm_num [reflectedPairInvariantProbe, EuclideanSpace.inner_toLp_toLp,
    dotProduct] at hc

theorem reflectedPair_norm_sq : ‖reflectedPairVector‖ ^ 2 = 2 := by
  rw [EuclideanSpace.norm_sq_eq]
  norm_num [reflectedPairVector]

/-- The fixed-target residual operator remains large even when an actual
state is zero. A varying-space theorem demanding operator-norm decay therefore
cannot be justified from actual-state confinement alone. -/
theorem reflectedPair_fullTarget_xi_opNorm_floor :
    (1 : ℝ) ≤ ‖xi (ContinuousLinearMap.id ℝ
      (EuclideanSpace ℝ (Fin 2))) reflectedPairInvariantProbe‖ := by
  have hne : reflectedPairVector ≠ 0 := by
    intro hz
    have h := reflectedPair_norm_sq
    rw [hz, norm_zero] at h
    norm_num at h
  exact xi_fullReadout_opNorm_ge_one_of_native_kernel
    reflectedPairVector reflectedPairInvariantProbe
    reflectedPair_invariant_blind hne

/-- Reflection symmetry, a nonzero invariant probe, and the exact XI
identity coexist with a positive anti-invariant displacement. Thus these
structural facts alone cannot be a source theorem proving RH. -/
theorem reflectedPair_fullTarget_xi_positive :
    RCLike.re (inner ℝ reflectedPairVector
      ((auditResidual (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ (Fin 2)))
        (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ (Fin 2)))
        reflectedPairInvariantProbe) reflectedPairVector)) = 2 := by
  rw [auditResidual_id_eq_xi]
  exact (xi_fullReadout_native_kernel reflectedPairVector
    reflectedPairInvariantProbe reflectedPair_invariant_blind).trans reflectedPair_norm_sq

/-- No change of native probe removes the positive complete charge in the
formal reflected-pair model; it can only move that charge between decoded
native currency and XI residual. -/
theorem reflectedPair_complete_currency_eq_two
    (L : EuclideanSpace ℝ (Fin 2) →L[ℝ] ℝ) :
    RCLike.re (inner ℝ reflectedPairVector
      ((auditDecoder (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ (Fin 2)))
          (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ (Fin 2))) L ∘L
        auditCurrency (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ (Fin 2))) L ∘L
        (auditDecoder (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ (Fin 2)))
          (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ (Fin 2))) L)† +
        auditResidual (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ (Fin 2)))
          (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ (Fin 2))) L)
        reflectedPairVector)) = 2 := by
  rw [fullReadout_complete_currency]
  simpa using reflectedPair_norm_sq

end SixBirdsDualityConfinement.RH.FiniteZeroWindows
