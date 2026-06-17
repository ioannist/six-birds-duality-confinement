import SixBirdsDualityConfinement.RH.AntiInvariantZeroLedger

/-!
# RH paper — `SatSelShell`

Saturated completed Selberg trace shell packaging the trace instrument,
quotient and audit data, functional-equation involution, typed zero ledger, and
anti-invariant zero ledger used downstream.
-/

namespace SixBirdsDualityConfinement.RH.SatSelShell

universe u v w q h i eqv em ql ml vis audit

/--
The saturated completed Selberg trace closure `Sel^!_{zeta,tr}`.

This is the construction-time shell used downstream: it keeps the
completed history carrier, trace instrument, saturated observables,
predictive events, quotient carriers, comparison map, functional-
equation involution, completed L-function handle, nontrivial zero
ledger, anti-invariant zero ledger, visibility map, and audit
provenance/admissibility data in one typed record.
-/
structure SatSelShell
    (R : Involution.RealCoordinate.{u}) where
  H_L : Type h
  I_tr : Type i
  EQ_tr : Type eqv
  EM_zero : Type em
  Q_L : Type ql
  M_L : Type ml
  pi_L : M_L → Q_L
  J_L : Involution.FunctionalEquationInvolution R
  J_L_is_fe_involution : J_L = Involution.feInvolution R
  Z_nt : ZeroLedger.NontrivialZeroLedger.{u, v, w} R
  Lambda_L : Involution.Complex R → Z_nt.LambdaValue
  Lambda_L_agrees_zero_ledger : Lambda_L = Z_nt.Lambda_zeta
  A_Z : AntiInvariantZeroLedger.AntiInvariantZeroLedger.{u, v, w, q} Z_nt
  Vis_L : H_L → I_tr → Type vis
  Audit_L : Type audit
  Audit_L_witness : Audit_L
  Audit_L_channel_status : SixBirdsDualityConfinement.F2ChannelStatus

end SixBirdsDualityConfinement.RH.SatSelShell
