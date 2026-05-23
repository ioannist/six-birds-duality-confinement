import SixBirdsDualityConfinement.RH.DCMasterApplied
import SixBirdsDualityConfinement.RH.TranslationT

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

universe u x y z cone trace scale

/--
Typed recognition-source carrier `Gamma_{SDTC-Selberg}`. A value of this
structure supplies, in one record, all Duality-Confinement apparatus parameters
(involutive ledger, separating readout, anti-invariant ledger,
completed-domination records, typed-cone primitives) together with the explicit
bridge propositions (`same_readout`, `mu_zero_of_ae`, `visible_zero_of_ae`)
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
  mu_zero_of_ae : A.psi_minus_ae_zero → shell.A_Z.A_Z = shell.A_Z.zero
  visible_zero_of_ae :
    A.psi_minus_ae_zero →
      ∀ x : ledger.X, x ∈ ledger.mu_support →
        A.psi_minus x = sep.zero_Y
  B_n : Nat → A.Cone
  domination_records : ∀ n : Nat, A.preceq A.A_X (B_n n)
  B_n_positive : ∀ n : Nat, A.Positive (B_n n)
  tr_B_n_tends_zero : Prop
  h_tr_B_n_tends_zero : tr_B_n_tends_zero
  TraceNonnegative : A.TraceValue → Prop
  positive_trace_nonnegative :
    ∀ C : A.Cone, A.Positive C → TraceNonnegative (A.tr C)
  TraceZero : A.TraceValue
  squeeze_trace_zero :
    TraceNonnegative (A.tr A.A_X) →
      (∀ n : Nat, A.TraceLE (A.tr A.A_X) (A.tr (B_n n))) →
        (∀ n : Nat, A.Positive (B_n n)) →
          tr_B_n_tends_zero →
            A.tr A.A_X = TraceZero
  trace_zero_positive_zero :
    A.tr A.A_X = TraceZero → A.A_X = A.zero

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
    DCMasterApplied.dcMasterApplied
      shell gamma.sep gamma.A gamma.same_readout
      gamma.mu_zero_of_ae gamma.visible_zero_of_ae gamma.B_n
      gamma.domination_records gamma.B_n_positive
      gamma.tr_B_n_tends_zero gamma.h_tr_B_n_tends_zero
      gamma.TraceNonnegative gamma.positive_trace_nonnegative
      gamma.TraceZero gamma.squeeze_trace_zero
      gamma.trace_zero_positive_zero
  exact TranslationT.translationTForward shell.A_Z hAZ

end SixBirdsDualityConfinement.RH.RHConditional
