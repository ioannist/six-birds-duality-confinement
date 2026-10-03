import SixBirdsDualityConfinement.RH.Involution
import SixBirdsDualityConfinement.RH.ZeroLedger
import SixBirdsDualityConfinement.RH.AntiInvariantZeroLedger
import SixBirdsDualityConfinement.RH.SatSelShell
import SixBirdsDualityConfinement.RH.TranslationT
import SixBirdsDualityConfinement.RH.ClassicalZeroLedger
import SixBirdsDualityConfinement.RH.ActualInvolution
import SixBirdsDualityConfinement.RH.ConcreteZeroWindowDC
import SixBirdsDualityConfinement.RH.ConcreteWindowXI
import SixBirdsDualityConfinement.RH.JTransportNoGo
import SixBirdsDualityConfinement.RH.OrdinateGaussianNoGo
import SixBirdsDualityConfinement.RH.JEquivariantSourceAudit
import SixBirdsDualityConfinement.RH.OrdinateHeatReturn
import SixBirdsDualityConfinement.RH.ComplexGaussianObservation
import SixBirdsDualityConfinement.RH.GaussianCenterIntegralBlindness
import SixBirdsDualityConfinement.RH.ArithmeticXiJensen
import SixBirdsDualityConfinement.RH.ArithmeticJensenWindows
import SixBirdsDualityConfinement.RH.ShiftedJensenMoment
import SixBirdsDualityConfinement.RH.DivisorMultiplicityMoment
import SixBirdsDualityConfinement.RH.GaussianDivisorHeatMoment
import SixBirdsDualityConfinement.RH.FullClassicalRHBridge
import SixBirdsDualityConfinement.RH.EvenSourceParityNoGo
import SixBirdsDualityConfinement.RH.EquivariantNativeTariffNoGo
import SixBirdsDualityConfinement.RH.HeatReturnAlignmentNoGo
import SixBirdsDualityConfinement.RH.OddProbePaymentNoGo
import SixBirdsDualityConfinement.RH.FaithfulTransportNoGo
import SixBirdsDualityConfinement.RH.ReservePaymentNoGo
import SixBirdsDualityConfinement.RH.AORReplayNoGo
import SixBirdsDualityConfinement.RH.AORFreshNoGo
import SixBirdsDualityConfinement.RH.ClassicalZeroCountable
import SixBirdsDualityConfinement.RH.FiniteZeroWindows
import SixBirdsDualityConfinement.RH.RealPartWindowDC
import SixBirdsDualityConfinement.RH.DCMasterApplied
import SixBirdsDualityConfinement.RH.RHConditional
import SixBirdsDualityConfinement.RH.ClassicalBareShell
import SixBirdsDualityConfinement.RH.BareSourceConverse
import SixBirdsDualityConfinement.RH.AORPrimitives
import SixBirdsDualityConfinement.RH.AORInstance
import SixBirdsDualityConfinement.RH.UpdatedAORXiInterfaces
import SixBirdsDualityConfinement.RH.SourceAccountingNoGo
import SixBirdsDualityConfinement.RH.XiSourceStepInstance

/-!
Umbrella module for the RH paper axis (Paper 2).

Per-section modules under `SixBirdsDualityConfinement/RH/` are
imported above, together with the classical-zero repair and countability,
finite-window XI
calibration, real-part quotient DC realization, and the updated AOR/XI
interface module. `BareSourceConverse` is an adversarial control: for the
bare classical shell, a generic gamma record can be built from RH itself.
`SourceAccountingNoGo` carries that calibration through the revised AOR
accounting wrapper.

The recognition source `Γ_{SDTC-Selberg}` is explicitly out of scope
for Lean derivation per the RH proposal §11.4. It is encoded as a
typed `structure` carrier (`obl:rh:gamma-sdtc-selberg`) named
`GammaSdtcSelberg`, declared inline in `RHConditional.lean`. The conditional theorem
takes a value of this structure as an explicit hypothesis parameter.
The forbidden-tokens rule bans `axiom`/`opaque`/`constant`/`sorry`/`admit`
anywhere in the source tree.

The inventory row `obl:rh:gamma-sdtc-selberg` is not listed in the
section_module_map because `GammaSdtcSelberg` is not a standalone module:
it is colocated with `RHConditional` as an inline structure. The row carries
`intended_status = out_of_scope_recognition_source`, which the validator
chain treats as a non-queueable item, so no per-module slot is reserved for it.
-/
