import SixBirdsDualityConfinement.RH.ReservePaymentNoGo
import SixBirdsNeedles.AOR.ReplayCostNecessity

/-!
An exact AOR replay control on actual completed-zeta zeros. A recheck
operation leaves the evidence state unchanged and charges the complete
ledger for the squared horizontal displacement of the chosen zero.
A finite budget for every raw recheck history is equivalent to
critical-strip RH. This is a necessity test for proposed source stock,
not a construction of the missing analytic payment.
-/

noncomputable section
namespace SixBirdsDualityConfinement.RH.AORReplayNoGo

open ClassicalZeroLedger FiniteZeroWindows
open SixBirdsNeedles.AOR
open SixBirdsNeedles.AOR.AuditKernel
open SixBirdsNeedles.AOR.WitnessOperations
open SixBirdsNeedles.AOR.OperationCascade
open SixBirdsNeedles.AOR.ScopedLedgerTraceLayer

def checkTheory : Theory where
  Record := Unit
  stratum := fun _ => .residual
  Status := fun _ => Unit
  Payload := fun _ _ => Unit
  readout := fun _ _ => True
  payload_sound := by intros; trivial
  depends := fun _ _ => False

def checkStart : State checkTheory where
  demanded := fun _ => False
  supplied := fun _ => False

/-- Rechecking a zero supplies no fresh evidence and changes no state. -/
def recheck : Operation checkTheory where
  Input := fun _ => NontrivialZero
  run := fun _ _ => empty checkTheory

/-- Complete decoded-native-plus-residual XI currency on a singleton
actual-zero window with no native probe. -/
def xiRecheckCharge (ρ : NontrivialZero) : ℝ :=
  ReservePaymentNoGo.completeWindowCharge unitWeights {ρ}
    (0 : EuclideanSpace ℝ {σ // σ ∈ ({ρ} : Finset NontrivialZero)} →L[ℝ] ℝ)

theorem xiRecheckCharge_eq_sq (ρ : NontrivialZero) :
    xiRecheckCharge ρ = displacement ρ ^ 2 := by
  rw [xiRecheckCharge, ReservePaymentNoGo.completeWindowCharge_eq_windowEnergy]
  simp [windowEnergy, unitWeights]

/-- The exact positive XI charge is assigned to one of the six
complete-ledger components. -/
def recheckLedger : CompleteCharge.Ledger recheck where
  amount := fun k _ ρ => if k = .adequacyResidual then xiRecheckCharge ρ else 0
  nonneg := by
    intro k S ρ
    split_ifs
    · rw [xiRecheckCharge_eq_sq]
      exact sq_nonneg _
    · exact le_refl _

theorem raw_recheck_budget_implies_criticalStripRH
    (hbudget : ScopedUniformLedgerBudget checkStart recheckLedger
      (fun {_} _ => True)) : CriticalStripRH := by
  intro s hz hlo hhi
  let ρ : NontrivialZero :=
    ⟨s, (completed_zero_iff_zeta_zero_of_re_pos s hlo).mpr hz, hlo, hhi⟩
  have hloop : applyBatch checkStart (recheck.run checkStart ρ) = checkStart :=
    apply_empty checkStart
  have hzero :=
    (ReplayCostNecessity.raw_budget_forces_replay_zero
      recheckLedger checkStart checkStart (.nil checkStart) ρ hloop hbudget).2
      CompleteCharge.Kind.adequacyResidual
  have hsquared : displacement ρ ^ 2 = 0 := by
    simpa [recheckLedger, xiRecheckCharge_eq_sq] using hzero
  have hdisp : displacement ρ = 0 := eq_zero_of_pow_eq_zero hsquared
  exact sub_eq_zero.mp hdisp

theorem raw_recheck_budget_iff_criticalStripRH :
    ScopedUniformLedgerBudget checkStart recheckLedger
      (fun {_} _ => True) ↔ CriticalStripRH := by
  constructor
  · exact raw_recheck_budget_implies_criticalStripRH
  · intro hRH
    have hcost (S : State checkTheory) (ρ : NontrivialZero) :
        recheckLedger.total S ρ = 0 := by
      have hz : displacement ρ = 0 := by
        exact sub_eq_zero.mpr
          (hRH ρ.val
            ((completed_zero_iff_zeta_zero_of_re_pos ρ.val ρ.property.2.1).mp
              ρ.property.1)
            ρ.property.2.1 ρ.property.2.2)
      simp [CompleteCharge.Ledger.total, recheckLedger,
        xiRecheckCharge_eq_sq, hz]
    have htrace : ∀ {S V : State checkTheory}
        (trace : Trace recheck S V), recheckLedger.traceTotal trace = 0 := by
      intro S V trace
      induction trace with
      | nil S => simp [CompleteCharge.Ledger.traceTotal]
      | @step S V ρ tail ih =>
          simp [CompleteCharge.Ledger.traceTotal, hcost, ih]
    exact ⟨0, fun V trace _ => (htrace trace).le⟩

end SixBirdsDualityConfinement.RH.AORReplayNoGo
