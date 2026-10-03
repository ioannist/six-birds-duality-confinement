import SixBirdsDualityConfinement.RH.RHConditional
import SixBirdsDualityConfinement.RH.ActualInvolution
import Mathlib.NumberTheory.LSeries.RiemannZeta

/-!
An exact classical-zero instance of the generic RH shell interface. All
completed-zeta zeros in the open critical strip are represented. The trace,
visibility, and audit fields are explicitly bare placeholders, so this is not
a constructed Selberg trace shell or a source for `GammaSdtcSelberg`.
-/

noncomputable section
open scoped ENNReal

namespace SixBirdsDualityConfinement.RH.ClassicalBareShell

abbrev realCoordinate : Involution.RealCoordinate where
  Real := ℝ
  zero := 0
  half := 1 / 2
  neg := Neg.neg
  sub := Sub.sub
  oneMinus := fun x => 1 - x
  oneMinus_involutive := by intro x; ring
  oneMinus_fixed_iff := by intro x; constructor <;> intro h <;> linarith
  sub_half_eq_zero_iff := by
    intro x
    change x - (1 / 2 : ℝ) = 0 ↔ x = 1 / 2
    exact sub_eq_zero
  sub_oneMinus_half := by
    intro x
    change (1 - x) - (1 / 2 : ℝ) = -(x - 1 / 2)
    ring

def toComplex (s : Involution.Complex realCoordinate) : ℂ :=
  ⟨s.re, s.im⟩

def fromComplex (s : ℂ) : Involution.Complex realCoordinate :=
  ⟨s.re, s.im⟩

theorem toComplex_fromComplex (s : ℂ) : toComplex (fromComplex s) = s := by
  cases s
  rfl

theorem fromComplex_toComplex (s : Involution.Complex realCoordinate) :
    fromComplex (toComplex s) = s := by
  cases s
  rfl

/-- The shell's coordinate involution is the actual analytic reflection
`s ↦ 1 - conj(s)`, not merely an isomorphic named operation. -/
theorem feInvolution_toComplex (s : ℂ) :
    toComplex ((Involution.feInvolution realCoordinate).J_L (fromComplex s)) =
      ActualInvolution.J s := by
  apply Complex.ext
  · simp [toComplex, fromComplex, Involution.feInvolution,
      Involution.Complex.oneMinusConj, realCoordinate, ActualInvolution.J_re]
  · simp [toComplex, fromComplex, Involution.feInvolution,
      Involution.Complex.oneMinusConj, realCoordinate, ActualInvolution.J_im]

def zeroLedger : ZeroLedger.NontrivialZeroLedger realCoordinate where
  LambdaValue := ℂ
  Lambda_zeta := fun s => completedRiemannZeta (toComplex s)
  IsZero := fun v => v = 0
  Z_zeta_nt := ClassicalZeroLedger.NontrivialZero
  rho := fun ρ => fromComplex ρ.val
  lt := fun x y => x < y
  one := (1 : ℝ)
  in_critical_strip := by intro ρ; exact ⟨ρ.property.2.1, ρ.property.2.2⟩
  lambda_vanishes := by intro ρ; simpa [toComplex_fromComplex] using ρ.property.1
  rho_injective := by
    intro ρ τ h
    apply Subtype.ext
    exact congrArg toComplex h
  zero_complete := by
    intro s hz hlo hhi
    refine ⟨⟨toComplex s, hz, hlo, hhi⟩, ?_⟩
    exact fromComplex_toComplex s
  m_rho := fun _ => 1
  m_rho_positive := by intro _; decide
  mu_L := fun _ => 1
  mu_L_singleton := by intro _; rfl

abbrev bareShell : SatSelShell.SatSelShell realCoordinate where
  H_L := Unit
  I_tr := Unit
  EQ_tr := Unit
  EM_zero := Unit
  Q_L := Unit
  M_L := Unit
  pi_L := id
  J_L := Involution.feInvolution realCoordinate
  J_L_is_fe_involution := rfl
  Z_nt := zeroLedger
  Lambda_L := zeroLedger.Lambda_zeta
  Lambda_L_agrees_zero_ledger := rfl
  A_Z := {
    abs_sq := fun x => ENNReal.ofReal (x ^ 2)
    abs_sq_zero_iff := by
      intro x
      constructor
      · intro h
        have hs : x ^ 2 ≤ 0 := (ENNReal.ofReal_eq_zero.mp h)
        nlinarith [sq_nonneg x]
      · intro h
        simp [h]
  }
  Vis_L := fun _ _ => Unit
  Audit_L := Unit
  Audit_L_witness := ()
  Audit_L_channel_status := .inapplicableOutsideScope

/-- The bare shell's involution preserves its actual-zero ledger and agrees
with the analytically justified zero-set reflection. -/
theorem bareShell_zero_reflection (ρ : ClassicalZeroLedger.NontrivialZero) :
    bareShell.Z_nt.rho (ActualInvolution.J_zero ρ) =
      bareShell.J_L.J_L (bareShell.Z_nt.rho ρ) := by
  change fromComplex (ActualInvolution.J ρ.val) =
    (Involution.feInvolution realCoordinate).J_L (fromComplex ρ.val)
  calc
    fromComplex (ActualInvolution.J ρ.val) =
        fromComplex (toComplex
          ((Involution.feInvolution realCoordinate).J_L (fromComplex ρ.val))) :=
      congrArg fromComplex (feInvolution_toComplex ρ.val).symm
    _ = (Involution.feInvolution realCoordinate).J_L (fromComplex ρ.val) :=
      fromComplex_toComplex _

/-- The classical-zero coverage bridge is constructible for the bare shell;
the analytic gamma source is still a separate hypothesis. -/
def identification : RHConditional.ClassicalZeroIdentification bareShell where
  toReal := id
  half_eq := rfl
  covers := by
    intro ρ
    exact ⟨ρ, rfl⟩

/-- The bare shell's ledger is the actual global positive sum with unit
weights, definitionally using the same completed-zeta zero subtype. -/
theorem bareShell_sum_eq_classical :
    bareShell.A_Z.A_Z = ClassicalZeroLedger.antiInvariantSum (fun _ => 1) := by
  rfl

theorem bareShell_gamma_implies_criticalStripRH
    (gamma : RHConditional.GammaSdtcSelberg bareShell) :
    ClassicalZeroLedger.CriticalStripRH :=
  RHConditional.rhConditionalClassical bareShell gamma identification

end SixBirdsDualityConfinement.RH.ClassicalBareShell
