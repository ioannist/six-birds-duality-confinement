import SixBirdsDualityConfinement.DualityConfinement.MasterTheorem
import SixBirdsDualityConfinement.RH.SatSelShell

/-!
# RH paper — `DCMasterApplied`

Application of the Duality-Confinement master theorem to Selberg-class data
carried by a `SatSelShell`. The DC apparatus is supplied as parameters
together with explicit bridge propositions (`same_readout`, `mu_zero_of_ae`,
`visible_zero_of_ae`) that connect the abstract DC conclusion to the shell's
`A_Z` ledger. The bridge propositions are typed hypotheses, not derivations:
this theorem combines them with `MasterTheorem.masterTheorem` to conclude
`S.A_Z.A_Z = S.A_Z.zero`.
-/

namespace SixBirdsDualityConfinement.RH.DCMasterApplied

universe u v w q x y z cone trace scale

/--
Typed bridge: the Duality-Confinement master theorem of
`MasterTheorem.masterTheorem`, fed through user-supplied bridge hypotheses,
yields `S.A_Z.A_Z = S.A_Z.zero` on the saturated Selberg shell `S`. The DC
apparatus parameters are supplied as bridge data, not derived from the shell.
-/
theorem dcMasterApplied
    {R : Involution.RealCoordinate.{u}}
    (S : SatSelShell.SatSelShell R)
    {ledger :
      _root_.SixBirdsDualityConfinement.DualityConfinement.Involution.InvolutiveObjectLedger.{x, y, z}}
    (sep :
      _root_.SixBirdsDualityConfinement.DualityConfinement.Separation.SeparatingReadout.{x, y, z, scale}
        ledger)
    (A :
      _root_.SixBirdsDualityConfinement.DualityConfinement.AntiInvariantLedger.AntiInvariantLedger.{x, y, z, cone, trace}
        ledger)
    (same_readout :
      ∀ x : ledger.X, A.psi_minus x = sep.psi_minus x)
    (mu_zero_of_ae :
      A.psi_minus_ae_zero → S.A_Z.A_Z = S.A_Z.zero)
    (visible_zero_of_ae :
      A.psi_minus_ae_zero →
        ∀ x : ledger.X, x ∈ ledger.mu_support →
          A.psi_minus x = sep.zero_Y)
    (B_n : Nat → A.Cone)
    (domination_records :
      ∀ n : Nat, A.preceq A.A_X (B_n n))
    (B_n_positive : ∀ n : Nat, A.Positive (B_n n))
    (tr_B_n_tends_zero : Prop)
    (h_tr_B_n_tends_zero : tr_B_n_tends_zero)
    (TraceNonnegative : A.TraceValue → Prop)
    (positive_trace_nonnegative :
      ∀ C : A.Cone, A.Positive C → TraceNonnegative (A.tr C))
    (TraceZero : A.TraceValue)
    (squeeze_trace_zero :
      TraceNonnegative (A.tr A.A_X) →
        (∀ n : Nat, A.TraceLE (A.tr A.A_X) (A.tr (B_n n))) →
          (∀ n : Nat, A.Positive (B_n n)) →
            tr_B_n_tends_zero →
              A.tr A.A_X = TraceZero)
    (trace_zero_positive_zero :
      A.tr A.A_X = TraceZero → A.A_X = A.zero) :
    S.A_Z.A_Z = S.A_Z.zero := by
  exact
    _root_.SixBirdsDualityConfinement.DualityConfinement.MasterTheorem.masterTheorem
        sep A same_readout (S.A_Z.A_Z = S.A_Z.zero)
        mu_zero_of_ae visible_zero_of_ae B_n domination_records
        B_n_positive tr_B_n_tends_zero h_tr_B_n_tends_zero
        TraceNonnegative positive_trace_nonnegative TraceZero
        squeeze_trace_zero trace_zero_positive_zero

end SixBirdsDualityConfinement.RH.DCMasterApplied
