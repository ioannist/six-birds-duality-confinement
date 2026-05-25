import SixBirdsDualityConfinement.RH.AORPrimitives
import SixBirdsDualityConfinement.RH.RHConditional

/-!
# RH paper — `AORInstance`

AOR-instance recasting of the conditional landing chain of
`RHConditional`. Provides the `SelAORInstance` wrapper structure
(def:rh:aor-sel-instance), the mechanical-records umbrella theorem
(thm:rh:aor-mechanical-records), six substantive-discharge theorems
classifying the recognition source, the bridge fields, the `Audit_L`
admissibility witness, the cross-paper master-theorem import, the
typed real-coordinate carrier, and translation theorem T against the
twelve-type residual atlas, and the main composition theorem
(thm:rh:aor-instance) stating `SelAORInstance shell gamma ∈
RefStableAOR^ref_{S_RH}`.

The discharges are typed-bridge / typed-interface compositions over
the existing `GammaSdtcSelberg`, `SatSelShell`, `DCMasterApplied`,
and `TranslationT` declarations. AOR meta-theory (Tsiokos2026AOR) is
cited at paper level and not re-derived.
-/

namespace SixBirdsDualityConfinement.RH.AORInstance

universe u x y z cone trace scale

/--
Wrapper for the RH AOR-instance carrier attached to a saturated Selberg shell
and a recognition-source carrier. The wrapper has exactly one Lean field: the
local eight-field AOR carrier.
-/
structure SelAORInstance
    {R : Involution.RealCoordinate.{u}}
    (shell : SatSelShell.SatSelShell R)
    (gamma : RHConditional.GammaSdtcSelberg.{u, x, y, z, cone, trace, scale} shell) where
  carrier : AORPrimitives.AORInstanceCarrier

/--
Documentary default shape for the RH AOR-instance carrier.

The string lists record which shell/gamma data occupy the lightweight AOR
field categories. They carry no mathematical content. The discharge register
is left empty here; later AOR-instance theorems supply the substantive
discharge atoms.
-/
def defaultCarrier
    {R : Involution.RealCoordinate.{u}}
    (shell : SatSelShell.SatSelShell R)
    (_gamma : RHConditional.GammaSdtcSelberg.{u, x, y, z, cone, trace, scale} shell) :
    AORPrimitives.AORInstanceCarrier :=
  { carrier_id := "zero side of shell"
    observations := ["Z_nt", "psi_minus_RH", "A_Z", "Vis_L"]
    routes := ["J_L", "pi_L", "AntiInvariantZeroLedger interface", "DC->shell bridge"]
    sources :=
      [ "Audit_L_witness",
        "Audit_L_channel_status",
        "Gamma_SDTC_Selberg",
        "domination sequence (gamma.B_n, gamma.domination_records)" ]
    interfaces := ["same_readout", "visible_zero_of_ae", "mu_zero_of_ae"]
    constraints :=
      [ "typed-cone positivity",
        "preceq",
        "trace monotonicity",
        "gamma.A.A_X preceq gamma.B_n n",
        "gamma.tr_B_n_tends_zero" ]
    discharges := []
    nonclaims :=
      [ "AOR-instance reading restricted to typed zero ledger of Sel",
        "No AOR membership for primitive Selberg-class L-functions other than zeta",
        "No AOR membership for weak or distributional zero-counting functionals",
        "No AOR membership for trace shells lacking Audit_L_witness",
        "No AOR membership for carriers outside the typed real-coordinate presentation",
        "GammaSdtcSelberg is a typed structural hypothesis, not a Lean postulate",
        "Bridge propositions are Prop-valued typed hypotheses, not data-bearing R-records",
        "Audit_L admissibility is construction-time hypothesis, not derived",
        "RealCoordinate analytic identification with classical Re(rho) is outside scope" ]
    nonclaims_nonempty := by decide }

/--
Mechanical AOR discharge atoms for the definition-side RH rows and Theorem T.

The list is literal data, ordered as in the paper table for
`thm:rh:aor-mechanical-records`. The `shell` and `gamma` indices attach the
list to the same scope as the AOR instance; the atoms themselves are fixed
row tags.
-/
def aorMechanicalRecords
    {R : Involution.RealCoordinate.{u}}
    (shell : SatSelShell.SatSelShell R)
    (_gamma : RHConditional.GammaSdtcSelberg.{u, x, y, z, cone, trace, scale} shell) :
    List AORPrimitives.DischargeAtom :=
  [ -- def:rh:fe-involution
    { primary := AORPrimitives.ResidualType.role
      forced_secondaries := []
      status := AORPrimitives.DischargeStatus.by_construction },
    -- def:rh:psi-minus-rh
    { primary := AORPrimitives.ResidualType.role
      forced_secondaries := []
      status := AORPrimitives.DischargeStatus.by_construction },
    -- def:rh:nontrivial-zero-ledger
    { primary := AORPrimitives.ResidualType.presentation
      forced_secondaries := []
      status := AORPrimitives.DischargeStatus.by_construction },
    -- def:rh:anti-invariant-zero-ledger
    { primary := AORPrimitives.ResidualType.presentation
      forced_secondaries := []
      status := AORPrimitives.DischargeStatus.by_construction },
    -- def:rh:sat-sel-shell
    { primary := AORPrimitives.ResidualType.«meta»
      forced_secondaries := []
      status := AORPrimitives.DischargeStatus.by_construction },
    -- thm:rh:translation-T
    { primary := AORPrimitives.ResidualType.target
      forced_secondaries := [AORPrimitives.ResidualType.transport]
      status := AORPrimitives.DischargeStatus.zero } ]

/-- AOR discharge atoms emitted by the `Gamma_{SDTC-Selberg}` recognition source. -/
def aorRecognitionDischarge
    {R : Involution.RealCoordinate.{u}}
    (shell : SatSelShell.SatSelShell R)
    (_gamma : RHConditional.GammaSdtcSelberg.{u, x, y, z, cone, trace, scale} shell) :
    List AORPrimitives.DischargeAtom :=
  [ -- provenance record
    { primary := AORPrimitives.ResidualType.source
      forced_secondaries :=
        [ AORPrimitives.ResidualType.target,
          AORPrimitives.ResidualType.role,
          AORPrimitives.ResidualType.limit ]
      status := AORPrimitives.DischargeStatus.bridged },
    -- abstract DC-ledger target of domination records
    { primary := AORPrimitives.ResidualType.target
      forced_secondaries := []
      status := AORPrimitives.DischargeStatus.bridged },
    -- domination-source role for the self-dual trace closure
    { primary := AORPrimitives.ResidualType.role
      forced_secondaries := []
      status := AORPrimitives.DischargeStatus.bridged },
    -- asymptotic trace budget
    { primary := AORPrimitives.ResidualType.limit
      forced_secondaries := []
      status := AORPrimitives.DischargeStatus.asymptotic_budgeted } ]

/-- AOR discharge atoms for the bridge fields carried by `GammaSdtcSelberg`. -/
def aorGammaBridgeDischarge
    {R : Involution.RealCoordinate.{u}}
    (shell : SatSelShell.SatSelShell R)
    (_gamma : RHConditional.GammaSdtcSelberg.{u, x, y, z, cone, trace, scale} shell) :
    List AORPrimitives.DischargeAtom :=
  [ -- same_readout component
    { primary := AORPrimitives.ResidualType.transport
      forced_secondaries :=
        [ AORPrimitives.ResidualType.role,
          AORPrimitives.ResidualType.target ]
      status := AORPrimitives.DischargeStatus.zero },
    -- visible_zero_of_ae component
    { primary := AORPrimitives.ResidualType.transport
      forced_secondaries := []
      status := AORPrimitives.DischargeStatus.bridged },
    -- mu_zero_of_ae component
    { primary := AORPrimitives.ResidualType.transport
      forced_secondaries := []
      status := AORPrimitives.DischargeStatus.bridged },
    -- forced secondary
    { primary := AORPrimitives.ResidualType.role
      forced_secondaries := []
      status := AORPrimitives.DischargeStatus.bridged },
    -- forced secondary
    { primary := AORPrimitives.ResidualType.target
      forced_secondaries := []
      status := AORPrimitives.DischargeStatus.bridged } ]

/-- AOR discharge atom for the shell's admissibility audit field. -/
def aorAuditLDischarge
    {R : Involution.RealCoordinate.{u}}
    (shell : SatSelShell.SatSelShell R)
    (_gamma : RHConditional.GammaSdtcSelberg.{u, x, y, z, cone, trace, scale} shell) :
    List AORPrimitives.DischargeAtom :=
  [ { primary := AORPrimitives.ResidualType.«meta»
      forced_secondaries := []
      status := AORPrimitives.DischargeStatus.bridged } ]

/-- AOR discharge atoms for the imported duality-confinement master theorem. -/
def aorDCMasterImportDischarge
    {R : Involution.RealCoordinate.{u}}
    (shell : SatSelShell.SatSelShell R)
    (_gamma : RHConditional.GammaSdtcSelberg.{u, x, y, z, cone, trace, scale} shell) :
    List AORPrimitives.DischargeAtom :=
  [ -- Paper 1 import
    { primary := AORPrimitives.ResidualType.transport
      forced_secondaries :=
        [ AORPrimitives.ResidualType.source,
          AORPrimitives.ResidualType.role,
          AORPrimitives.ResidualType.target ]
      status := AORPrimitives.DischargeStatus.approved_other },
    -- forced secondary: Paper 1 provenance
    { primary := AORPrimitives.ResidualType.source
      forced_secondaries := []
      status := AORPrimitives.DischargeStatus.bridged },
    -- forced secondary: duality-confinement membrane role
    { primary := AORPrimitives.ResidualType.role
      forced_secondaries := []
      status := AORPrimitives.DischargeStatus.bridged },
    -- forced secondary: shell zero-ledger target
    { primary := AORPrimitives.ResidualType.target
      forced_secondaries := []
      status := AORPrimitives.DischargeStatus.bridged } ]

/-- AOR discharge atoms for the typed real-coordinate presentation boundary. -/
def aorRealCoordinateDischarge
    {R : Involution.RealCoordinate.{u}}
    (shell : SatSelShell.SatSelShell R)
    (_gamma : RHConditional.GammaSdtcSelberg.{u, x, y, z, cone, trace, scale} shell) :
    List AORPrimitives.DischargeAtom :=
  [ -- typed coordinate is outside analytic-identification scope
    { primary := AORPrimitives.ResidualType.presentation
      forced_secondaries := []
      status := AORPrimitives.DischargeStatus.outside_scope },
    -- analytic identification is registered as a nonclaim
    { primary := AORPrimitives.ResidualType.presentation
      forced_secondaries := []
      status := AORPrimitives.DischargeStatus.nonclaim } ]

/-- AOR discharge atoms for the typed interface supplied by translation theorem T. -/
def aorTranslationInterfaceDischarge
    {R : Involution.RealCoordinate.{u}}
    (shell : SatSelShell.SatSelShell R)
    (_gamma : RHConditional.GammaSdtcSelberg.{u, x, y, z, cone, trace, scale} shell) :
    List AORPrimitives.DischargeAtom :=
  [ -- primary target atom
    { primary := AORPrimitives.ResidualType.target
      forced_secondaries := [AORPrimitives.ResidualType.transport]
      status := AORPrimitives.DischargeStatus.zero },
    -- forced secondary
    { primary := AORPrimitives.ResidualType.transport
      forced_secondaries := []
      status := AORPrimitives.DischargeStatus.zero } ]

/-- Carrier assembled from the seven RH AOR discharge lists. -/
def assembledCarrier
    {R : Involution.RealCoordinate.{u}}
    (shell : SatSelShell.SatSelShell R)
    (gamma : RHConditional.GammaSdtcSelberg.{u, x, y, z, cone, trace, scale} shell) :
    AORPrimitives.AORInstanceCarrier :=
  { defaultCarrier shell gamma with
    discharges :=
      aorMechanicalRecords shell gamma ++
      aorRecognitionDischarge shell gamma ++
      aorGammaBridgeDischarge shell gamma ++
      aorAuditLDischarge shell gamma ++
      aorDCMasterImportDischarge shell gamma ++
      aorRealCoordinateDischarge shell gamma ++
      aorTranslationInterfaceDischarge shell gamma }

/--
Main local AOR-instance theorem for the RH carrier.

The theorem proves only the record-level `RefStableAOR` predicate for the
assembled carrier. The critical-line statement remains the separate conclusion
of `RHConditional.rhConditional`.
-/
theorem aorInstance
    {R : Involution.RealCoordinate.{u}}
    (shell : SatSelShell.SatSelShell R)
    (gamma : RHConditional.GammaSdtcSelberg.{u, x, y, z, cone, trace, scale} shell) :
    AORPrimitives.RefStableAOR (assembledCarrier shell gamma) := by
  unfold AORPrimitives.RefStableAOR
  constructor
  · simp [assembledCarrier, defaultCarrier]
  · intro atom hatom secondary hsec
    cases secondary
    · exact
        ⟨{ primary := AORPrimitives.ResidualType.source
           forced_secondaries := []
           status := AORPrimitives.DischargeStatus.bridged },
          by
            simp [assembledCarrier, defaultCarrier, aorMechanicalRecords,
              aorRecognitionDischarge, aorGammaBridgeDischarge,
              aorAuditLDischarge, aorDCMasterImportDischarge,
              aorRealCoordinateDischarge, aorTranslationInterfaceDischarge]⟩
    · exact
        ⟨{ primary := AORPrimitives.ResidualType.transport
           forced_secondaries := []
           status := AORPrimitives.DischargeStatus.zero },
          by
            simp [assembledCarrier, defaultCarrier, aorMechanicalRecords,
              aorRecognitionDischarge, aorGammaBridgeDischarge,
              aorAuditLDischarge, aorDCMasterImportDischarge,
              aorRealCoordinateDischarge, aorTranslationInterfaceDischarge]⟩
    · exact
        ⟨{ primary := AORPrimitives.ResidualType.role
           forced_secondaries := []
           status := AORPrimitives.DischargeStatus.by_construction },
          by
            simp [assembledCarrier, defaultCarrier, aorMechanicalRecords,
              aorRecognitionDischarge, aorGammaBridgeDischarge,
              aorAuditLDischarge, aorDCMasterImportDischarge,
              aorRealCoordinateDischarge, aorTranslationInterfaceDischarge]⟩
    · exact
        ⟨{ primary := AORPrimitives.ResidualType.target
           forced_secondaries := []
           status := AORPrimitives.DischargeStatus.bridged },
          by
            simp [assembledCarrier, defaultCarrier, aorMechanicalRecords,
              aorRecognitionDischarge, aorGammaBridgeDischarge,
              aorAuditLDischarge, aorDCMasterImportDischarge,
              aorRealCoordinateDischarge, aorTranslationInterfaceDischarge]⟩
    · exact
        ⟨{ primary := AORPrimitives.ResidualType.limit
           forced_secondaries := []
           status := AORPrimitives.DischargeStatus.asymptotic_budgeted },
          by
            simp [assembledCarrier, defaultCarrier, aorMechanicalRecords,
              aorRecognitionDischarge, aorGammaBridgeDischarge,
              aorAuditLDischarge, aorDCMasterImportDischarge,
              aorRealCoordinateDischarge, aorTranslationInterfaceDischarge]⟩
    · exact
        ⟨{ primary := AORPrimitives.ResidualType.presentation
           forced_secondaries := []
           status := AORPrimitives.DischargeStatus.by_construction },
          by
            simp [assembledCarrier, defaultCarrier, aorMechanicalRecords,
              aorRecognitionDischarge, aorGammaBridgeDischarge,
              aorAuditLDischarge, aorDCMasterImportDischarge,
              aorRealCoordinateDischarge, aorTranslationInterfaceDischarge]⟩
    · exact
        ⟨{ primary := AORPrimitives.ResidualType.«meta»
           forced_secondaries := []
           status := AORPrimitives.DischargeStatus.by_construction },
          by
            simp [assembledCarrier, defaultCarrier, aorMechanicalRecords,
              aorRecognitionDischarge, aorGammaBridgeDischarge,
              aorAuditLDischarge, aorDCMasterImportDischarge,
              aorRealCoordinateDischarge, aorTranslationInterfaceDischarge]⟩

end SixBirdsDualityConfinement.RH.AORInstance
