import SixBirdsDualityConfinement.RH.Involution
import SixBirdsDualityConfinement.RH.ZeroLedger
import SixBirdsDualityConfinement.RH.AntiInvariantZeroLedger
import SixBirdsDualityConfinement.RH.SatSelShell
import SixBirdsDualityConfinement.RH.TranslationT
import SixBirdsDualityConfinement.RH.DCMasterApplied
import SixBirdsDualityConfinement.RH.RHConditional

/-!
Umbrella module for the RH paper axis (Paper 2).

Per-section modules under `SixBirdsDualityConfinement/RH/` are
imported above in document order matching
`formalization/traceability/queue_rh.csv`. Codex populates each
module's body during Phase G.

The recognition source `Γ_{SDTC-Selberg}` is explicitly out of scope
for Lean derivation per the RH proposal §11.4. It is encoded as a
typed `structure` carrier (`obl:rh:gamma-sdtc-selberg`) in a separate
`RecognitionSource.lean` module that downstream theorems
(`DCMasterApplied`, `RHConditional`) take as an explicit hypothesis
parameter. The forbidden-tokens rule bans `axiom`/`opaque`/`constant`/`sorry`/`admit`
anywhere in the source tree.

Note: `RecognitionSource.lean` is added by codex during Phase G as
part of the `RHConditional` dispatch (the conditional theorem is its
only consumer; the type lives next to its only consumer); it is not
listed in the section_module_map because the obligation row in the
inventory has `intended_status = out_of_scope_recognition_source`,
which the validator chain treats as a non-queueable item.
-/
