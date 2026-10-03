import SixBirdsDualityConfinement.RH.DCMasterApplied
import SixBirdsDualityConfinement.RH.TranslationT
import SixBirdsDualityConfinement.RH.ClassicalZeroLedger
import Mathlib.Topology.Order.OrderClosed

/-!
# RH paper — `RHConditional`

Conditional landing chain. This module defines the typed recognition-source
carrier `GammaSdtcSelberg`, packaging the bridge hypotheses required by
`DCMasterApplied.dcMasterApplied`, and proves `rhConditional`: given a
saturated Selberg shell and a value of the carrier, every typed nontrivial zero
in the shell has real-part coordinate `R.half`. The carrier is a typed bridge
assumption, not a derived instantiation of the DC apparatus on the shell; it
supplies the DC apparatus together with the bridge propositions that connect it
to the shell's `A_Z` ledger.
-/

namespace SixBirdsDualityConfinement.RH.RHConditional

open Filter
open scoped Topology

universe u x y z cone trace scale

/--
Typed recognition-source carrier `Gamma_{SDTC-Selberg}`. A value of this
structure supplies, in one record, all Duality-Confinement apparatus parameters
(involutive ledger, separating readout, anti-invariant ledger,
completed-domination records, typed-cone primitives) together with the explicit
bridge propositions (`same_readout`, `visible_zero_of_ae`, and the
zero-object visibility/readout map)
needed by `DCMasterApplied.dcMasterApplied` to conclude `shell.A_Z.A_Z =
shell.A_Z.zero`. These bridge propositions are typed hypotheses: the DC
carrier/readout/operator-ledger data is assumed compatible with `shell.A_Z`,
not derived from it. The project forbidden-token rule keeps this carrier in
record form rather than as a logical postulate.
-/
structure GammaSdtcSelberg
    {R : Involution.RealCoordinate.{u}}
    (shell : SatSelShell.SatSelShell R) where
  ledger :
    _root_.SixBirdsDualityConfinement.DualityConfinement.Involution.InvolutiveObjectLedger.{x, y, z}
  sep :
    _root_.SixBirdsDualityConfinement.DualityConfinement.Separation.SeparatingReadout.{x, y, z, scale}
      ledger
  A :
    _root_.SixBirdsDualityConfinement.DualityConfinement.AntiInvariantLedger.AntiInvariantLedger.{x, y, z, cone, trace}
      ledger
  same_readout : ∀ x : ledger.X, A.psi_minus x = sep.psi_minus x
  visible_zero_of_ae :
    A.psi_minus_ae_zero →
      ∀ x : ledger.X, x ∈ ledger.mu_support →
        A.psi_minus x = sep.zero_Y
  zero_object : shell.Z_nt.Z_zeta_nt → ledger.X
  zero_object_visible :
    ∀ ρ : shell.Z_nt.Z_zeta_nt,
      zero_object ρ ∈ ledger.mu_support
  encode : R.Real → ledger.Y
  encode_faithful :
    ∀ r : R.Real, encode r = sep.zero_Y → r = R.zero
  readout_formula :
    ∀ ρ : shell.Z_nt.Z_zeta_nt,
      A.psi_minus (zero_object ρ) =
        encode (R.sub (shell.Z_nt.rho ρ).re R.half)
  B_n : Nat → A.Cone
  domination_records : ∀ n : Nat, A.preceq A.A_X (B_n n)
  B_n_positive : ∀ n : Nat, A.Positive (B_n n)
  traceReal : A.TraceValue → ℝ
  traceReal_mono :
    ∀ a b : A.TraceValue, A.TraceLE a b → traceReal a ≤ traceReal b
  traceReal_nonneg :
    ∀ C : A.Cone, A.Positive C → 0 ≤ traceReal (A.tr C)
  traceReal_zero_reflect :
    ∀ t : A.TraceValue, traceReal t = 0 → t = A.tr A.zero
  trace_decay : Tendsto (fun n => traceReal (A.tr (B_n n))) atTop (𝓝 0)
  trace_zero_faithful :
    A.tr A.A_X = A.tr A.zero → A.A_X = A.zero

/--
Conditional landing chain: given a saturated Selberg shell `shell` and a typed
recognition-source carrier `gamma : GammaSdtcSelberg shell`, every typed
nontrivial zero in `shell` has real-part coordinate `R.half`. The proof
composes `DCMasterApplied.dcMasterApplied` (yielding
`shell.A_Z.A_Z = shell.A_Z.zero` from `gamma`'s bridge hypotheses) with
`TranslationT.translationTForward` (yielding the pointwise critical-line
statement from `A_Z = 0`). The conclusion is conditional on `gamma`; the
carrier is not derived in Lean.
-/
theorem rhConditional
    {R : Involution.RealCoordinate.{u}}
    (shell : SatSelShell.SatSelShell R)
    (gamma : GammaSdtcSelberg shell) :
    ∀ ρ : shell.Z_nt.Z_zeta_nt, (shell.Z_nt.rho ρ).re = R.half := by
  have hAZ : shell.A_Z.A_Z = shell.A_Z.zero :=
    DCMasterApplied.dcMasterAppliedRealTrace
      shell gamma.sep gamma.A gamma.same_readout
      gamma.visible_zero_of_ae gamma.zero_object
      gamma.zero_object_visible gamma.encode
      gamma.encode_faithful gamma.readout_formula gamma.B_n
      gamma.domination_records gamma.traceReal gamma.traceReal_mono
      gamma.traceReal_nonneg gamma.trace_decay gamma.traceReal_zero_reflect
      gamma.trace_zero_faithful
  exact TranslationT.translationTForward shell.A_Z hAZ

/-- A bridge to actual completed-zeta zeros. It records only carrier coverage
and coordinate fidelity; it contains no critical-line or domination proof. -/
structure ClassicalZeroIdentification
    {R : Involution.RealCoordinate.{u}}
    (shell : SatSelShell.SatSelShell R) where
  toReal : R.Real → ℝ
  half_eq : toReal R.half = (1 / 2 : ℝ)
  covers : ∀ ρ : ClassicalZeroLedger.NontrivialZero,
    ∃ τ : shell.Z_nt.Z_zeta_nt,
      toReal (shell.Z_nt.rho τ).re = ρ.val.re

/-- The conditional RH conclusion on the actual classical critical-strip
zero set. The classical identification is a separate, explicit hypothesis. -/
theorem rhConditionalClassical
    {R : Involution.RealCoordinate.{u}}
    (shell : SatSelShell.SatSelShell R)
    (gamma : GammaSdtcSelberg shell)
    (ident : ClassicalZeroIdentification shell) :
    ClassicalZeroLedger.CriticalStripRH := by
  intro s hz hlo hhi
  have hcompleted : completedRiemannZeta s = 0 :=
    (ClassicalZeroLedger.completed_zero_iff_zeta_zero_of_re_pos s hlo).mpr hz
  obtain ⟨τ, hτ⟩ := ident.covers ⟨s, hcompleted, hlo, hhi⟩
  calc
    s.re = ident.toReal (shell.Z_nt.rho τ).re := hτ.symm
    _ = ident.toReal R.half := congrArg ident.toReal (rhConditional shell gamma τ)
    _ = (1 / 2 : ℝ) := ident.half_eq

end SixBirdsDualityConfinement.RH.RHConditional
