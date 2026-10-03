import SixBirdsDualityConfinement.RH.RHConditional
import SixBirdsDualityConfinement.RH.FullClassicalRHBridge
import SixBirdsNeedles.AOR.Core
import SixBirdsNeedles.XiCore.ResidualCapacity
import SixBirdsNeedles.XiCore.OperatorLadders

/-!
Interfaces to the revised AOR evidence kernel and XI residual calculus. The AOR
state below stores proofs already supplied by `GammaSdtcSelberg`; it does not
construct that gamma or establish an external analytic trace estimate. The XI
theorem is a second, explicitly conditional route on actual completed-zeta
zeros. Its probe and residual hypotheses are independent research obligations.
-/

noncomputable section
open Filter
open scoped Topology
open scoped InnerProduct InnerProductSpace

namespace SixBirdsDualityConfinement.RH.UpdatedAORXiInterfaces

open SixBirdsNeedles.AOR
open SixBirdsNeedles.AOR.AuditKernel
open SixBirdsNeedles.XiCore

universe u x y z cone trace scale

inductive SourceObligation where
  | domination
  | positivity
  | traceDecay
  | zeroVisibility
  | readout

def sourceClaim {R : Involution.RealCoordinate.{u}}
    {shell : SatSelShell.SatSelShell R}
    (gamma : RHConditional.GammaSdtcSelberg.{u, x, y, z, cone, trace, scale} shell) :
    SourceObligation → Prop
  | .domination => ∀ n, gamma.A.preceq gamma.A.A_X (gamma.B_n n)
  | .positivity => ∀ n, gamma.A.Positive (gamma.B_n n)
  | .traceDecay => Tendsto (fun n => gamma.traceReal (gamma.A.tr (gamma.B_n n))) atTop (𝓝 0)
  | .zeroVisibility => ∀ ρ, gamma.zero_object ρ ∈ gamma.ledger.mu_support
  | .readout => ∀ ρ,
      gamma.A.psi_minus (gamma.zero_object ρ) =
        gamma.encode (R.sub (shell.Z_nt.rho ρ).re R.half)

/-- Revised AOR's evidence kernel records exactly which gamma fields are
supplied. No string status counts as a certificate. -/
def sourceTheory {R : Involution.RealCoordinate.{u}}
    {shell : SatSelShell.SatSelShell R}
    (gamma : RHConditional.GammaSdtcSelberg.{u, x, y, z, cone, trace, scale} shell) :
    Theory where
  Record := SourceObligation
  stratum := fun _ => .residual
  Status := fun _ => Unit
  Payload := fun r _ => { u : Unit // sourceClaim gamma r }
  readout := fun r _ => sourceClaim gamma r
  payload_sound := by intro r s h; exact h.property
  depends := fun _ _ => False

def sourceState {R : Involution.RealCoordinate.{u}}
    {shell : SatSelShell.SatSelShell R}
    (gamma : RHConditional.GammaSdtcSelberg.{u, x, y, z, cone, trace, scale} shell) :
    State (sourceTheory gamma) where
  demanded := fun _ => True
  supplied := fun _ => True

/-- Each source row has a proof payload, but only because the gamma parameter
already carries those proofs. This theorem does not produce gamma. -/
theorem source_accounted {R : Involution.RealCoordinate.{u}}
    {shell : SatSelShell.SatSelShell R}
    (gamma : RHConditional.GammaSdtcSelberg.{u, x, y, z, cone, trace, scale} shell) :
    Accounted (sourceState gamma) := by
  intro r _
  refine ⟨(), ⟨(), ?_⟩, trivial⟩
  cases r with
  | domination => exact gamma.domination_records
  | positivity => exact gamma.B_n_positive
  | traceDecay => exact gamma.trace_decay
  | zeroVisibility => exact gamma.zero_object_visible
  | readout => exact gamma.readout_formula

/-- A finite-dimensional XI residual can close the actual critical-strip
statement only after a null-legal probe, a faithful response equation at
every completed-zeta zero, and vanishing of the residual at those probes. -/
theorem xi_residual_zero_implies_criticalStripRH
    {E F G : Type*}
    [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
    [NormedAddCommGroup F] [InnerProductSpace ℝ F] [FiniteDimensional ℝ F]
    [NormedAddCommGroup G] [InnerProductSpace ℝ G] [FiniteDimensional ℝ G]
    (C : E →L[ℝ] E) (hC : C.IsPositive)
    (D : E →L[ℝ] G) (L : E →L[ℝ] F)
    (hD : NullLegal C D) (hL : NullLegal C L)
    (probe : ClassicalZeroLedger.NontrivialZero → G)
    (test : ClassicalZeroLedger.NontrivialZero → E)
    (hlegal : ∀ ρ, L (test ρ) = 0 ∧ auditCost C (test ρ) ≤ 1)
    (hresponse : ∀ ρ,
      ‖inner ℝ (probe ρ) (D (test ρ))‖ ^ 2 =
        (ρ.val.re - (1 / 2 : ℝ)) ^ 2)
    (hzero : ∀ ρ,
      RCLike.re ⟪probe ρ, auditResidual C D L (probe ρ)⟫_ℝ = 0) :
    ClassicalZeroLedger.CriticalStripRH := by
  intro s hs hlo hhi
  let ρ : ClassicalZeroLedger.NontrivialZero :=
    ⟨s, (ClassicalZeroLedger.completed_zero_iff_zeta_zero_of_re_pos s hlo).mpr hs,
      hlo, hhi⟩
  obtain ⟨_, _, _, _, hbound⟩ := audit_residual_capacity C hC D L hD hL (probe ρ)
  have hsq : (ρ.val.re - (1 / 2 : ℝ)) ^ 2 ≤ 0 := by
    rw [← hresponse ρ, ← hzero ρ]
    exact hbound (test ρ) (hlegal ρ).1 (hlegal ρ).2
  have : ρ.val.re = (1 / 2 : ℝ) := by
    nlinarith [sq_nonneg (ρ.val.re - (1 / 2 : ℝ))]
  exact this

/-- The revised XI residual-capacity interface reaches Mathlib's full
classical RH predicate after the proved critical-strip-to-global bridge.
The null-legal response and zero-residual fields remain explicit
hypotheses; this theorem does not manufacture them. -/
theorem xi_residual_zero_implies_riemannHypothesis
    {E F G : Type*}
    [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
    [NormedAddCommGroup F] [InnerProductSpace ℝ F] [FiniteDimensional ℝ F]
    [NormedAddCommGroup G] [InnerProductSpace ℝ G] [FiniteDimensional ℝ G]
    (C : E →L[ℝ] E) (hC : C.IsPositive)
    (D : E →L[ℝ] G) (L : E →L[ℝ] F)
    (hD : NullLegal C D) (hL : NullLegal C L)
    (probe : ClassicalZeroLedger.NontrivialZero → G)
    (test : ClassicalZeroLedger.NontrivialZero → E)
    (hlegal : ∀ ρ, L (test ρ) = 0 ∧ auditCost C (test ρ) ≤ 1)
    (hresponse : ∀ ρ,
      ‖inner ℝ (probe ρ) (D (test ρ))‖ ^ 2 =
        (ρ.val.re - (1 / 2 : ℝ)) ^ 2)
    (hzero : ∀ ρ,
      RCLike.re ⟪probe ρ, auditResidual C D L (probe ρ)⟫_ℝ = 0) :
    RiemannHypothesis :=
  FullClassicalRHBridge.riemannHypothesis_of_criticalStripRH
    (xi_residual_zero_implies_criticalStripRH C hC D L hD hL
      probe test hlegal hresponse hzero)

#print axioms xi_residual_zero_implies_riemannHypothesis

end SixBirdsDualityConfinement.RH.UpdatedAORXiInterfaces
