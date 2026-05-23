import SixBirdsDualityConfinement.Terminology

/-!
# RH paper — `Involution`

Functional-equation involution `J_L(s) = 1 - conj(s)`, separating
anti-invariant readout `psi_-(s) = Re(s) - 1/2`, and their elementary
properties: involutivity, critical-line fixed locus, and anti-invariance.
-/

namespace SixBirdsDualityConfinement.RH.Involution

universe u

/--
A mathlib-free real-coordinate interface for the RH critical-line
calculus.  The distinguished point `half` represents `1 / 2`; the
operation `oneMinus` represents `x ↦ 1 - x`; and `sub x half`
represents the centered readout `x - 1 / 2`.
-/
structure RealCoordinate where
  Real : Type u
  zero : Real
  half : Real
  neg : Real → Real
  sub : Real → Real → Real
  oneMinus : Real → Real
  oneMinus_involutive : ∀ x : Real, oneMinus (oneMinus x) = x
  oneMinus_fixed_iff : ∀ x : Real, oneMinus x = x ↔ x = half
  sub_half_eq_zero_iff : ∀ x : Real, sub x half = zero ↔ x = half
  sub_oneMinus_half : ∀ x : Real, sub (oneMinus x) half = neg (sub x half)

/--
Minimal typed complex-number record for the RH functional-equation
involution.  It stores real and imaginary coordinates over the
chosen coordinate model.
-/
structure Complex (R : RealCoordinate.{u}) where
  re : R.Real
  im : R.Real

/-- Complex conjugation in the local typed complex model. -/
def Complex.conj {R : RealCoordinate.{u}} (s : Complex R) : Complex R :=
  { re := s.re, im := R.neg s.im }

/-- The coordinate realization of `1 - conj(s)`. -/
def Complex.oneMinusConj {R : RealCoordinate.{u}} (s : Complex R) : Complex R :=
  { re := R.oneMinus s.re, im := s.im }

/--
The RH functional-equation involution `J_L(s) = 1 - conj(s)`,
bundled with its fixed-locus and involutivity laws.
-/
structure FunctionalEquationInvolution (R : RealCoordinate.{u}) where
  J_L : Complex R → Complex R
  J_L_formula : ∀ s : Complex R, J_L s = Complex.oneMinusConj s
  fixed_locus : ∀ s : Complex R, J_L s = s ↔ s.re = R.half
  involutive : ∀ s : Complex R, J_L (J_L s) = s

/--
The functional-equation involution on the local typed complex plane:
`J_L(s) := 1 - conj(s)`.  Its fixed locus is the critical line
`Re(s) = 1 / 2`, and it is involutive.
-/
def feInvolution (R : RealCoordinate.{u}) :
    FunctionalEquationInvolution R where
  J_L := Complex.oneMinusConj
  J_L_formula := by
    intro s
    rfl
  fixed_locus := by
    intro s
    constructor
    · intro h
      exact (R.oneMinus_fixed_iff s.re).mp (congrArg Complex.re h)
    · intro h
      cases s with
      | mk re im =>
          dsimp [Complex.oneMinusConj] at h ⊢
          rw [(R.oneMinus_fixed_iff re).mpr h]
  involutive := by
    intro s
    cases s with
    | mk re im =>
        dsimp [Complex.oneMinusConj]
        rw [R.oneMinus_involutive re]

/--
A separating anti-invariant readout for the RH involution.  The field
`psi_minus` is the centered real-part readout, its anti-invariance is
recorded against `J_L`, and its zero set is exactly `Fix(J_L)`.
-/
structure SeparatingAntiInvariantReadout
    (R : RealCoordinate.{u})
    (J : FunctionalEquationInvolution R) where
  psi_minus : Complex R → R.Real
  psi_minus_formula :
    ∀ s : Complex R, psi_minus s = R.sub s.re R.half
  anti_invariant :
    ∀ s : Complex R, psi_minus (J.J_L s) = R.neg (psi_minus s)
  vanishes_exactly_on_fix :
    ∀ s : Complex R, psi_minus s = R.zero ↔ J.J_L s = s

/--
The RH separating anti-invariant readout
`psi_-(s) := Re(s) - 1 / 2`.  It is anti-invariant under `J_L` and
vanishes exactly on the fixed locus of the functional-equation
involution.
-/
def psiMinusRh (R : RealCoordinate.{u}) :
    SeparatingAntiInvariantReadout R (feInvolution R) where
  psi_minus := fun s => R.sub s.re R.half
  psi_minus_formula := by
    intro s
    rfl
  anti_invariant := by
    intro s
    change R.sub (R.oneMinus s.re) R.half = R.neg (R.sub s.re R.half)
    exact R.sub_oneMinus_half s.re
  vanishes_exactly_on_fix := by
    intro s
    constructor
    · intro h
      exact ((feInvolution R).fixed_locus s).mpr
        ((R.sub_half_eq_zero_iff s.re).mp h)
    · intro h
      exact (R.sub_half_eq_zero_iff s.re).mpr
        (((feInvolution R).fixed_locus s).mp h)

end SixBirdsDualityConfinement.RH.Involution
