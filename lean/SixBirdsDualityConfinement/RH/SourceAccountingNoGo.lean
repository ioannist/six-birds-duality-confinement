import SixBirdsDualityConfinement.RH.BareSourceConverse
import SixBirdsDualityConfinement.RH.UpdatedAORXiInterfaces

/-! Calibration of the revised AOR source-accounting interface on the
bare classical RH shell. Accounting a source state presupposes the
gamma record; the record is target-equivalent on this shell. -/

noncomputable section
namespace SixBirdsDualityConfinement.RH.SourceAccountingNoGo

open ClassicalZeroLedger ClassicalBareShell
open SixBirdsNeedles.AOR
open SixBirdsNeedles.AOR.AuditKernel

universe u x y z cone trace scale

/-- For every shell, adding revised AOR `Accounted` evidence to the
already supplied gamma source record does not change its inhabitation.
The wrapper verifies fields of a gamma; it does not supply a gamma. -/
theorem accounted_source_exists_iff_gamma_nonempty
    {R : Involution.RealCoordinate.{u}}
    {shell : SatSelShell.SatSelShell R} :
    (∃ gamma : RHConditional.GammaSdtcSelberg.{u, x, y, z, cone, trace, scale} shell,
      Accounted (UpdatedAORXiInterfaces.sourceState gamma)) ↔
      Nonempty (RHConditional.GammaSdtcSelberg.{u, x, y, z, cone, trace, scale} shell) := by
  constructor
  · rintro ⟨gamma, _⟩
    exact ⟨gamma⟩
  · rintro ⟨gamma⟩
    exact ⟨gamma, UpdatedAORXiInterfaces.source_accounted gamma⟩

/-- The existence of an AOR-accounted revised source state is exactly
critical-strip RH on the bare classical shell. Its accounting proof
does not construct the Selberg trace source. -/
theorem exists_accounted_source_iff_criticalStripRH :
    (∃ gamma : RHConditional.GammaSdtcSelberg.{0, 0, 0, 0, 0, 0, 0} bareShell,
      Accounted (UpdatedAORXiInterfaces.sourceState gamma)) ↔
      CriticalStripRH := by
  exact accounted_source_exists_iff_gamma_nonempty.trans
    BareSourceConverse.gamma_nonempty_iff_criticalStripRH

end SixBirdsDualityConfinement.RH.SourceAccountingNoGo
