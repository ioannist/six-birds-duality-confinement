import SixBirdsDualityConfinement.RH.FiniteZeroWindows
import SixBirdsDualityConfinement.DualityConfinement.MasterTheorem

/-!
The finite real-part quotient of an actual completed-zeta zero window.
Its involution has the correct RH fixed locus, unlike `rho ↦ 1-rho` on
complex zeros. This module derives the exact energy bridge to the RH ledger;
it does not supply a vanishing domination sequence.
-/

noncomputable section
open Filter
open scoped Topology

namespace SixBirdsDualityConfinement.RH.RealPartWindowDC

open ClassicalZeroLedger FiniteZeroWindows
open SixBirdsDualityConfinement.DualityConfinement
open SixBirdsNeedles.XiCore

def coordinateSupport (W : Finset NontrivialZero) : Finset ℝ :=
  W.image (fun ρ => ρ.val.re)

def Coordinate (W : Finset NontrivialZero) :=
  {x : ℝ // x ∈ coordinateSupport W}

def coordinateWeight (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) (x : ℝ) : ℝ :=
  ∑ ρ ∈ W, if ρ.val.re = x then (m ρ : ℝ) else 0

def coordinateEnergy (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) : ℝ :=
  ∑ x ∈ coordinateSupport W, coordinateWeight m W x * (x - 1 / 2) ^ 2

theorem coordinateEnergy_eq_windowEnergy (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) :
    coordinateEnergy m W = windowEnergy m W := by
  classical
  unfold coordinateEnergy coordinateWeight windowEnergy
  calc
    ∑ x ∈ coordinateSupport W,
        (∑ ρ ∈ W, if ρ.val.re = x then (m ρ : ℝ) else 0) * (x - 1 / 2) ^ 2
      = ∑ x ∈ coordinateSupport W, ∑ ρ ∈ W,
          if ρ.val.re = x then (m ρ : ℝ) * displacement ρ ^ 2 else 0 := by
            apply Finset.sum_congr rfl
            intro x hx
            rw [Finset.sum_mul]
            apply Finset.sum_congr rfl
            intro ρ hρ
            split_ifs with h
            · simp [displacement, h]
            · simp
    _ = ∑ ρ ∈ W, ∑ x ∈ coordinateSupport W,
          if ρ.val.re = x then (m ρ : ℝ) * displacement ρ ^ 2 else 0 := by
            rw [Finset.sum_comm]
    _ = ∑ ρ ∈ W, (m ρ : ℝ) * displacement ρ ^ 2 := by
          apply Finset.sum_congr rfl
          intro ρ hρ
          have hmem : ρ.val.re ∈ coordinateSupport W :=
            Finset.mem_image_of_mem _ hρ
          simp [hmem]

theorem coordinateWeight_nonneg (m : NontrivialZero → ℕ)
    (W : Finset NontrivialZero) (x : ℝ) :
    0 ≤ coordinateWeight m W x := by
  classical
  unfold coordinateWeight
  apply Finset.sum_nonneg
  intro ρ _
  split_ifs <;> positivity

theorem coordinateWeight_positive (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, 0 < m ρ) (W : Finset NontrivialZero)
    (x : Coordinate W) : 0 < coordinateWeight m W x.val := by
  classical
  obtain ⟨ρ, hρ, hx⟩ := Finset.mem_image.mp x.property
  have hterm : 0 < (if ρ.val.re = x.val then (m ρ : ℝ) else 0) := by
    simp [hx, Nat.cast_pos.mpr (hm ρ)]
  have hle : (if ρ.val.re = x.val then (m ρ : ℝ) else 0) ≤
      coordinateWeight m W x.val := by
    apply Finset.single_le_sum _ hρ
    intro σ _
    split_ifs <;> positivity
  exact hterm.trans_le hle

def reflectCoordinate (W : Finset NontrivialZero)
    (hW : ReflectedWindow W) (x : Coordinate W) : Coordinate W := by
  classical
  refine ⟨1 - x.val, ?_⟩
  obtain ⟨ρ, hρ, hx⟩ := Finset.mem_image.mp x.property
  apply Finset.mem_image.mpr
  refine ⟨reflectZero ρ, hW ρ hρ, ?_⟩
  simp [reflectZero, Complex.sub_re, ← hx]

theorem reflectCoordinate_involutive (W : Finset NontrivialZero)
    (hW : ReflectedWindow W) (x : Coordinate W) :
    reflectCoordinate W hW (reflectCoordinate W hW x) = x := by
  apply Subtype.ext
  simp [reflectCoordinate]

def coordinateDisplacement (W : Finset NontrivialZero)
    (x : Coordinate W) : ℝ := x.val - 1 / 2

theorem coordinateDisplacement_reflect (W : Finset NontrivialZero)
    (hW : ReflectedWindow W) (x : Coordinate W) :
    coordinateDisplacement W (reflectCoordinate W hW x) =
      -coordinateDisplacement W x := by
  simp [coordinateDisplacement, reflectCoordinate]
  ring

theorem coordinateDisplacement_zero_iff_fixed
    (W : Finset NontrivialZero) (hW : ReflectedWindow W)
    (x : Coordinate W) :
    coordinateDisplacement W x = 0 ↔ reflectCoordinate W hW x = x := by
  constructor
  · intro h
    apply Subtype.ext
    change 1 - x.val = x.val
    dsimp [coordinateDisplacement] at h
    linarith
  · intro h
    have hv := congrArg Subtype.val h
    change 1 - x.val = x.val at hv
    dsimp [coordinateDisplacement]
    linarith

/-- A finite DC object ledger whose objects are distinct real parts of the
actual zeros in `W`. Fibers of the quotient carry their total positive
weight. This avoids imposing the wrong fixed locus on complex zeros. -/
def coordinateLedger (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, 0 < m ρ) (W : Finset NontrivialZero)
    (hW : ReflectedWindow W) : Involution.InvolutiveObjectLedger where
  X := Coordinate W
  J := reflectCoordinate W hW
  J_involutive := reflectCoordinate_involutive W hW
  Weight := ℝ
  WeightPositive := fun r => 0 < r
  mu := fun x => coordinateWeight m W x.val
  mu_positive := coordinateWeight_positive m hm W
  mu_support := (coordinateSupport W).attach.toList
  mu_support_complete := by
    intro x
    exact Finset.mem_toList.mpr (Finset.mem_attach _ x)
  Y := ℝ
  Scalar := ℝ
  add := (· + ·)
  smul := (· * ·)
  inner := (· * ·)
  norm := abs
  J_iso := Neg.neg
  J_iso_involutive := by intro y; simp
  J_iso_linear := by intro a y z; ring
  J_iso_isometry := by intro y; simp
  psi := coordinateDisplacement W
  psi_equivariant := coordinateDisplacement_reflect W hW

/-- The same real-part quotient has an exact separating readout and identity
modulus. Both sides of its quantitative condition are the actual absolute
horizontal displacement. -/
def coordinateSeparation (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, 0 < m ρ) (W : Finset NontrivialZero)
    (hW : ReflectedWindow W) :
    Separation.SeparatingReadout (coordinateLedger m hm W hW) where
  psi_minus := coordinateDisplacement W
  zero_Y := by change ℝ; exact 0
  separates_fixed_locus_on_visible := by
    intro x _
    exact coordinateDisplacement_zero_iff_fixed W hW x
  Scale := ℝ
  ScalePositive := fun ε => 0 < ε
  ScaleGE := (· ≥ ·)
  dist_to_fix := fun x => |coordinateDisplacement W x|
  norm_psi_minus := fun x => |coordinateDisplacement W x|
  modulus := id
  modulus_positive := by intro ε hε; exact hε
  quantitatively_separating := by intro ε hε x hx; exact hx

/-- In the real cone model, the DC energy is the quotient's weighted sum.
The zero/pointwise bridge is proved from positive weights. -/
def coordinateAntiInvariantLedger (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, 0 < m ρ) (W : Finset NontrivialZero)
    (hW : ReflectedWindow W) :
    AntiInvariantLedger.AntiInvariantLedger (coordinateLedger m hm W hW) where
  psi_minus := coordinateDisplacement W
  Cone := ℝ
  TraceValue := ℝ
  zero := 0
  A_X := coordinateEnergy m W
  Positive := fun a => 0 ≤ a
  positive_A_X := by
    rw [coordinateEnergy_eq_windowEnergy]
    unfold windowEnergy
    exact Finset.sum_nonneg fun ρ _ => term_nonneg m ρ
  preceq := (· ≤ ·)
  tr := id
  TraceLE := (· ≤ ·)
  trace_mono := by intro a b h; exact h
  integral_sq_norm := coordinateEnergy m W
  trace_identity := rfl
  psi_minus_ae_zero := ∀ x : Coordinate W, coordinateDisplacement W x = 0
  zero_iff_ae_zero := by
    rw [coordinateEnergy_eq_windowEnergy]
    constructor
    · intro h x
      obtain ⟨ρ, hρ, hx⟩ := Finset.mem_image.mp x.property
      have hd := (windowEnergy_eq_zero_iff m hm W).mp h ρ hρ
      simpa [coordinateDisplacement, displacement, hx] using hd
    · intro h
      apply (windowEnergy_eq_zero_iff m hm W).mpr
      intro ρ hρ
      let x : Coordinate W := ⟨ρ.val.re, Finset.mem_image_of_mem _ hρ⟩
      simpa [x, coordinateDisplacement, displacement] using h x

theorem coordinateAX_eq_windowEnergy (m : NontrivialZero → ℕ)
    (hm : ∀ ρ, 0 < m ρ) (W : Finset NontrivialZero)
    (hW : ReflectedWindow W) :
    (coordinateAntiInvariantLedger m hm W hW).A_X = windowEnergy m W :=
  coordinateEnergy_eq_windowEnergy m W

/-- The actual finite RH positive ledger is simultaneously a DC cone energy
and the fixed-target original-energy XI residual evaluated on the zero state.
This is an exact bridge, not an analytic upper bound on that shared energy. -/
theorem coordinateAX_eq_fixedTarget_xi_quadratic
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (hsym : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : ReflectedWindow W) :
    (coordinateAntiInvariantLedger m hm W hW).A_X =
      RCLike.re (inner ℝ (displacementVector m W)
        ((auditResidual (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
          (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
          (invariantProbe W)) (displacementVector m W))) := by
  rw [coordinateAX_eq_windowEnergy m hm W hW,
    fixedTarget_window_quadratic_eq_windowEnergy m hsym W hW]

/-- A source-supplied XI operator payment bounds the concrete DC energy of
the same actual zero window. This is the precise RH-side interface to the
operator residual bound in the physical Navier--Stokes membrane. -/
theorem coordinateAX_le_operatorResidualBudget
    (m : NontrivialZero → ℕ)
    (hsym : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : ReflectedWindow W)
    (Omega : EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ]
      EuclideanSpace ℝ {ρ // ρ ∈ W})
    (hXi : Loewner
      (auditResidual (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (invariantProbe W)) Omega) :
    coordinateEnergy m W ≤
      RCLike.re (inner ℝ (displacementVector m W)
        (Omega (displacementVector m W))) := by
  rw [coordinateEnergy_eq_windowEnergy]
  exact windowEnergy_le_operatorResidualBudget m hsym W hW Omega hXi

def coordinateXiBudget
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (W : Finset NontrivialZero) (hW : ReflectedWindow W)
    (Omega : EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ]
      EuclideanSpace ℝ {ρ // ρ ∈ W}) :
    (coordinateAntiInvariantLedger m hm W hW).Cone := by
  change ℝ
  exact RCLike.re (inner ℝ (displacementVector m W)
    (Omega (displacementVector m W)))

/-- The XI operator payment is literally a domination record for the
constructed DC cone, with no abstract bridge field in between. -/
theorem coordinateDC_domination_of_Xi
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (hsym : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : ReflectedWindow W)
    (Omega : EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ]
      EuclideanSpace ℝ {ρ // ρ ∈ W})
    (hXi : Loewner
      (auditResidual (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (invariantProbe W)) Omega) :
    (coordinateAntiInvariantLedger m hm W hW).preceq
      (coordinateAntiInvariantLedger m hm W hW).A_X
      (coordinateXiBudget m hm W hW Omega) := by
  change coordinateEnergy m W ≤
    RCLike.re (inner ℝ (displacementVector m W)
      (Omega (displacementVector m W)))
  exact coordinateAX_le_operatorResidualBudget m hsym W hW Omega hXi

/-- The imported DC master theorem now has a concrete actual-zero-window
instance. Its only nonconstructed input is the displayed real domination
sequence with a genuine topological zero limit. -/
theorem coordinateFixed_of_vanishing_domination
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (W : Finset NontrivialZero) (hW : ReflectedWindow W)
    (B : ℕ → ℝ) (hdom : ∀ n, coordinateEnergy m W ≤ B n)
    (hBpos : ∀ n, 0 ≤ B n) (hBlim : Tendsto B atTop (𝓝 0)) :
    ∀ x : Coordinate W, reflectCoordinate W hW x = x := by
  let A := coordinateAntiInvariantLedger m hm W hW
  let sep := coordinateSeparation m hm W hW
  have hsame : ∀ x : Coordinate W, A.psi_minus x = sep.psi_minus x := by
    intro x
    rfl
  have hvisible : A.psi_minus_ae_zero →
      ∀ x : Coordinate W, x ∈ (coordinateLedger m hm W hW).mu_support →
        A.psi_minus x = sep.zero_Y := by
    intro h x hx
    exact h x
  have hfixed :
      ∀ x : Coordinate W,
        x ∈ (coordinateLedger m hm W hW).mu_support →
          (coordinateLedger m hm W hW).J x = x := by
    apply MasterTheorem.masterTheoremFixedLocus sep A hsame hvisible B
    · exact hdom
    · exact hBpos
    · exact hBlim
    · intro C hC
      exact hC
    · intro hnonneg htrace hpositive hlimit
      change 0 ≤ coordinateEnergy m W at hnonneg
      have hle : coordinateEnergy m W ≤ 0 :=
        le_of_tendsto_of_tendsto tendsto_const_nhds hlimit
          (Filter.Eventually.of_forall htrace)
      change coordinateEnergy m W = 0
      exact le_antisymm hle hnonneg
    · intro h
      exact h
  intro x
  exact hfixed x ((coordinateLedger m hm W hW).mu_support_complete x)

/-- A fixed zero window is confined by the actual DC master theorem when a
family of XI operator payments has a vanishing actual-state charge. The
existence of that family is the explicit unresolved analytic input. -/
theorem coordinateFixed_of_vanishing_Xi_payment
    (m : NontrivialZero → ℕ) (hm : ∀ ρ, 0 < m ρ)
    (hsym : ∀ ρ, m (reflectZero ρ) = m ρ)
    (W : Finset NontrivialZero) (hW : ReflectedWindow W)
    (Omega : ℕ → EuclideanSpace ℝ {ρ // ρ ∈ W} →L[ℝ]
      EuclideanSpace ℝ {ρ // ρ ∈ W})
    (hXi : ∀ n, Loewner
      (auditResidual (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (ContinuousLinearMap.id ℝ (EuclideanSpace ℝ {ρ // ρ ∈ W}))
        (invariantProbe W)) (Omega n))
    (hlim : Tendsto (fun n =>
      RCLike.re (inner ℝ (displacementVector m W)
        (Omega n (displacementVector m W)))) atTop (𝓝 0)) :
    ∀ x : Coordinate W, reflectCoordinate W hW x = x := by
  let B : ℕ → ℝ := fun n => RCLike.re (inner ℝ (displacementVector m W)
    (Omega n (displacementVector m W)))
  apply coordinateFixed_of_vanishing_domination m hm W hW B
  · intro n
    exact coordinateAX_le_operatorResidualBudget m hsym W hW (Omega n) (hXi n)
  · intro n
    have hA : 0 ≤ coordinateEnergy m W := by
      rw [coordinateEnergy_eq_windowEnergy]
      unfold windowEnergy
      exact Finset.sum_nonneg fun ρ _ => term_nonneg m ρ
    exact hA.trans (coordinateAX_le_operatorResidualBudget m hsym W hW
      (Omega n) (hXi n))
  · exact hlim

end SixBirdsDualityConfinement.RH.RealPartWindowDC
