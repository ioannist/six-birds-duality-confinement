import SixBirdsDualityConfinement.RH.Involution
import SixBirdsDualityConfinement.RH.ZeroLedger
import SixBirdsDualityConfinement.RH.AntiInvariantZeroLedger
import SixBirdsDualityConfinement.RH.SatSelShell
import SixBirdsDualityConfinement.RH.TranslationT
import SixBirdsDualityConfinement.RH.DCMasterApplied
import SixBirdsDualityConfinement.RH.RHConditional
import SixBirdsDualityConfinement.RH.AORPrimitives
import SixBirdsDualityConfinement.RH.AORInstance

/-!
Umbrella module for the RH paper axis (Paper 2).

Per-section modules under `SixBirdsDualityConfinement/RH/` are
imported above in document order matching
`formalization/traceability/queue_rh.csv`. Codex populates each
module's body during Phase G.

The recognition source `Γ_{SDTC-Selberg}` is explicitly out of scope
for Lean derivation per the RH proposal §11.4. It is encoded as a
typed `structure` carrier (`obl:rh:gamma-sdtc-selberg`) named
`GammaSdtcSelberg`, declared inline in `RHConditional.lean` (the
conditional theorem is its only consumer). The conditional theorem
takes a value of this structure as an explicit hypothesis parameter.
The forbidden-tokens rule bans `axiom`/`opaque`/`constant`/`sorry`/`admit`
anywhere in the source tree.

The inventory row `obl:rh:gamma-sdtc-selberg` is not listed in the
section_module_map because `GammaSdtcSelberg` is not a standalone module:
it is colocated with `RHConditional` as an inline structure next to its only
consumer, per `lean/codex_kickoff.md` §12. The row carries
`intended_status = out_of_scope_recognition_source`, which the validator
chain treats as a non-queueable item, so no per-module slot is reserved for it.
-/
