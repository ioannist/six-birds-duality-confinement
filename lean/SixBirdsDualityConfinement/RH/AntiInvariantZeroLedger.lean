import SixBirdsDualityConfinement.RH.ZeroLedger
import Mathlib.MeasureTheory.Measure.MeasureSpace

/-!
# RH paper — `AntiInvariantZeroLedger`

The ledger is an actual extended nonnegative sum over the entire typed zero
carrier. A faithful squared-readout map is the only algebraic interface;
positivity, summand detection, and both directions of Translation T are
proved below instead of being fields of the ledger.
-/

noncomputable section
open scoped ENNReal

namespace SixBirdsDualityConfinement.RH.AntiInvariantZeroLedger

universe u v w

structure AntiInvariantZeroLedger
    {R : Involution.RealCoordinate.{u}}
    (Z : ZeroLedger.NontrivialZeroLedger.{u, v, w} R) where
  /-- Realizes the squared horizontal displacement as a nonnegative value. -/
  abs_sq : R.Real → ℝ≥0∞
  abs_sq_zero_iff : ∀ x : R.Real, abs_sq x = 0 ↔ x = R.zero

def AntiInvariantZeroLedger.term {R : Involution.RealCoordinate.{u}}
    {Z : ZeroLedger.NontrivialZeroLedger.{u, v, w} R}
    (A : AntiInvariantZeroLedger Z) (ρ : Z.Z_zeta_nt) : ℝ≥0∞ :=
  (Z.m_rho ρ : ℝ≥0∞) * A.abs_sq (R.sub (Z.rho ρ).re R.half)

def AntiInvariantZeroLedger.A_Z {R : Involution.RealCoordinate.{u}}
    {Z : ZeroLedger.NontrivialZeroLedger.{u, v, w} R}
    (A : AntiInvariantZeroLedger Z) : ℝ≥0∞ :=
  ∑' ρ : Z.Z_zeta_nt, A.term ρ

def AntiInvariantZeroLedger.zero {R : Involution.RealCoordinate.{u}}
    {Z : ZeroLedger.NontrivialZeroLedger.{u, v, w} R}
    (_A : AntiInvariantZeroLedger Z) : ℝ≥0∞ := 0

theorem AntiInvariantZeroLedger.term_zero_iff_on_line {R : Involution.RealCoordinate.{u}}
    {Z : ZeroLedger.NontrivialZeroLedger.{u, v, w} R}
    (A : AntiInvariantZeroLedger Z) (ρ : Z.Z_zeta_nt) :
    A.term ρ = 0 ↔ (Z.rho ρ).re = R.half := by
  unfold AntiInvariantZeroLedger.term
  rw [mul_eq_zero]
  have hm : (Z.m_rho ρ : ℝ≥0∞) ≠ 0 := by
    exact_mod_cast (Nat.ne_of_gt (Z.m_rho_positive ρ))
  simp only [hm, false_or]
  exact (A.abs_sq_zero_iff _).trans (R.sub_half_eq_zero_iff _)

theorem AntiInvariantZeroLedger.sum_zero_iff_on_line {R : Involution.RealCoordinate.{u}}
    {Z : ZeroLedger.NontrivialZeroLedger.{u, v, w} R}
    (A : AntiInvariantZeroLedger Z) :
    A.A_Z = A.zero ↔ ∀ ρ : Z.Z_zeta_nt, (Z.rho ρ).re = R.half := by
  simp only [AntiInvariantZeroLedger.A_Z, AntiInvariantZeroLedger.zero, ENNReal.tsum_eq_zero]
  exact forall_congr' fun ρ => A.term_zero_iff_on_line ρ

end SixBirdsDualityConfinement.RH.AntiInvariantZeroLedger
