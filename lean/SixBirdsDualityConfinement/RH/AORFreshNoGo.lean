import SixBirdsDualityConfinement.RH.AORReplayNoGo

/-!
Fresh-demand control for one actual completed-zeta zero. The first
request is charged its exact XI currency; the retained demand makes later
checks free. The operation supplies no AOR certificate. Its ledger
always has a finite budget, but covers the original positive recheck
cost exactly when the zero is on the line. The initial fuel is the
target's XI charge, not an independent analytic source receipt.
-/

noncomputable section
open scoped Classical
namespace SixBirdsDualityConfinement.RH.AORFreshNoGo

open ClassicalZeroLedger FiniteZeroWindows
open SixBirdsDualityConfinement.RH.AORReplayNoGo
open SixBirdsNeedles.AOR
open SixBirdsNeedles.AOR.AuditKernel
open SixBirdsNeedles.AOR.WitnessOperations
open SixBirdsNeedles.AOR.ScopedLedgerTraceLayer

/-- A demand is retained after the first check; no certificate is supplied. -/
def freshCheck : Operation checkTheory where
  Input := fun _ => Unit
  run := fun _ _ => ⟨[()], []⟩

/-- The fresh check leaves the demanded record unpaid in the revised AOR
evidence kernel. Its finite ledger bound below cannot be read as an
`Accounted` proof. -/
theorem freshCheck_not_accounted :
    ¬ Accounted (applyBatch checkStart (freshCheck.run checkStart ())) := by
  intro haccounted
  have hdemand : Reach (applyBatch checkStart (freshCheck.run checkStart ())) () :=
    Reach.root (Or.inr (by simp [freshCheck]))
  obtain ⟨s, p, hsupply⟩ := haccounted () hdemand
  simp [applyBatch, checkStart, freshCheck] at hsupply

/-- Only the first check is charged at the exact XI currency. -/
def freshLedger (ρ : NontrivialZero) : CompleteCharge.Ledger freshCheck where
  amount := fun k S _ =>
    if k = .adequacyResidual then
      if S.demanded () then 0 else xiRecheckCharge ρ
    else 0
  nonneg := by
    intro k S i
    by_cases hk : k = .adequacyResidual
    · by_cases hs : S.demanded ()
      · simp [hk, hs]
      · simp [hk, hs, xiRecheckCharge_eq_sq, sq_nonneg]
    · simp [hk]

def freshFuel (ρ : NontrivialZero) (S : State checkTheory) : ℝ :=
  if S.demanded () then 0 else xiRecheckCharge ρ

private theorem freshLedger_total (ρ : NontrivialZero)
    (S : State checkTheory) (i : Unit) :
    (freshLedger ρ).total S i = freshFuel ρ S := by
  simp [CompleteCharge.Ledger.total, freshLedger, freshFuel]

theorem first_check_total (ρ : NontrivialZero) :
    (freshLedger ρ).total checkStart () = xiRecheckCharge ρ := by
  rw [freshLedger_total]
  simp [freshFuel, checkStart]

theorem retained_check_zero (ρ : NontrivialZero)
    (S : State checkTheory) (h : S.demanded ()) :
    (freshLedger ρ).total S () = 0 := by
  rw [freshLedger_total]
  simp [freshFuel, h]

theorem raw_fresh_histories_paid_by_XI (ρ : NontrivialZero) :
    ∀ V (trace : SixBirdsNeedles.AOR.OperationCascade.Trace freshCheck checkStart V),
      (freshLedger ρ).traceTotal trace ≤ xiRecheckCharge ρ := by
  have hnonneg : ∀ S : State checkTheory, 0 ≤ freshFuel ρ S := by
    intro S
    by_cases h : S.demanded ()
    · simp [freshFuel, h]
    · simp [freshFuel, h, xiRecheckCharge_eq_sq, sq_nonneg]
  have hpay : ∀ (S : State checkTheory) (i : freshCheck.Input S),
      freshFuel ρ (applyBatch S (freshCheck.run S i)) +
        (freshLedger ρ).total S i ≤ freshFuel ρ S := by
    intro S i
    have hafter : (applyBatch S (freshCheck.run S i)).demanded () := by
      exact Or.inr (by simp [freshCheck])
    rw [freshLedger_total]
    simp [freshFuel, hafter]
  have hB := scoped_bound_of_local_payment checkStart (freshLedger ρ)
    (fun _ _ => True) (freshFuel ρ) hnonneg
    (fun S i _ => hpay S i)
  have hallowed : ∀ {S V : State checkTheory}
      (trace : SixBirdsNeedles.AOR.OperationCascade.Trace freshCheck S V),
      AllowedTrace (fun _ _ => True) trace := by
    intro S V trace
    induction trace with
    | nil S => exact .nil S
    | step i tail ih => exact .step i tail True.intro ih
  intro V trace
  have h := hB V trace (hallowed trace)
  simpa [freshFuel, checkStart] using h

theorem fresh_payment (ρ : NontrivialZero) :
    ScopedUniformLedgerBudget checkStart (freshLedger ρ)
      (fun {_} _ => True) :=
  ⟨xiRecheckCharge ρ, fun V trace _ => raw_fresh_histories_paid_by_XI ρ V trace⟩

/-- The original repeated observation still incurs its XI charge. -/
def persistentLedger (ρ : NontrivialZero) : CompleteCharge.Ledger freshCheck where
  amount := fun k _ _ => if k = .adequacyResidual then xiRecheckCharge ρ else 0
  nonneg := by
    intro k S i
    by_cases hk : k = .adequacyResidual
    · simp [hk, xiRecheckCharge_eq_sq, sq_nonneg]
    · simp [hk]

theorem fresh_covers_persistent_iff_zero (ρ : NontrivialZero) :
    CompleteCharge.Ledger.Covers (freshLedger ρ) (persistentLedger ρ) ↔
      displacement ρ = 0 := by
  constructor
  · intro hcover
    let S := applyBatch checkStart (freshCheck.run checkStart ())
    have hdemand : S.demanded () := by
      exact Or.inr (by simp [freshCheck])
    have h := hcover CompleteCharge.Kind.adequacyResidual S ()
    have hxi : xiRecheckCharge ρ ≤ 0 := by
      simpa [freshLedger, persistentLedger, hdemand] using h
    rw [xiRecheckCharge_eq_sq] at hxi
    nlinarith [sq_nonneg (displacement ρ)]
  · intro hz k S i
    simp [freshLedger, persistentLedger, xiRecheckCharge_eq_sq, hz]

theorem all_fresh_ledgers_honest_iff_criticalStripRH :
    (∀ ρ : NontrivialZero,
      CompleteCharge.Ledger.Covers (freshLedger ρ) (persistentLedger ρ)) ↔
      CriticalStripRH := by
  constructor
  · intro h s hs hlo hhi
    let ρ : NontrivialZero :=
      ⟨s, (completed_zero_iff_zeta_zero_of_re_pos s hlo).mpr hs, hlo, hhi⟩
    have hz := (fresh_covers_persistent_iff_zero ρ).mp (h ρ)
    exact sub_eq_zero.mp hz
  · intro h ρ
    apply (fresh_covers_persistent_iff_zero ρ).mpr
    exact sub_eq_zero.mpr (h ρ.val
      ((completed_zero_iff_zeta_zero_of_re_pos ρ.val ρ.property.2.1).mp
        ρ.property.1) ρ.property.2.1 ρ.property.2.2)

end SixBirdsDualityConfinement.RH.AORFreshNoGo
