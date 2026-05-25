/-!
# RH paper — `AORPrimitives`

Minimal AOR meta-theory primitives used by `RH.AORInstance`.

This module defines five primitives for the AOR-instance recasting:
the residual-type and discharge-status enums, the typed discharge
record, the eight-field AOR-instance carrier, and the `RefStableAOR`
membership predicate. The minimal scope is intentional: the full AOR
meta-theory of Tsiokos2026AOR (eight-stratum decomposition, twelve-type
atlas, 132-entry cost table, hierarchy theorems) is cited at paper
level and not re-derived here.

The `RefStableAOR` predicate below is the local syntactic predicate over
the carrier's typed discharge list. It is not the AOR meta-theory's full
refinement-stable characterisation theorem.
-/

namespace SixBirdsDualityConfinement.RH.AORPrimitives

/-- Residual primary types used by the RH AOR-instance discharges. -/
inductive ResidualType : Type where
  | source : ResidualType
  | transport : ResidualType
  | role : ResidualType
  | target : ResidualType
  | limit : ResidualType
  | presentation : ResidualType
  | «meta» : ResidualType
  deriving DecidableEq

/--
Closed discharge statuses used by the RH AOR-instance discharges.

The local enum deliberately has no open status; every constructor is treated
as closed by construction by `RefStableAOR`.
-/
inductive DischargeStatus : Type where
  | zero : DischargeStatus
  | bridged : DischargeStatus
  | approved_other : DischargeStatus
  | outside_scope : DischargeStatus
  | nonclaim : DischargeStatus
  | by_construction : DischargeStatus
  | asymptotic_budgeted : DischargeStatus
  deriving DecidableEq

/-- One residual atom in the local AOR discharge register. -/
structure DischargeAtom : Type where
  primary : ResidualType
  forced_secondaries : List ResidualType
  status : DischargeStatus
  deriving DecidableEq

/--
Eight-field carrier for the local RH AOR instance.

The first six fields are lightweight typed tags. The load-bearing fields are
the residual-discharge register and the nonclaim-register population
requirement.
-/
structure AORInstanceCarrier : Type where
  carrier_id : String
  observations : List String
  routes : List String
  sources : List String
  interfaces : List String
  constraints : List String
  discharges : List DischargeAtom
  nonclaims_nonempty : Prop

/--
Local refinement-stable AOR predicate for the RH carrier.

Every forced secondary residual type declared by a discharge atom must be
realized as the primary residual type of some atom in the same discharge list;
the nonclaim register must also be populated. Closed-status checking is
vacuous because every local `DischargeStatus` constructor is closed.
-/
def RefStableAOR (carrier : AORInstanceCarrier) : Prop :=
  carrier.nonclaims_nonempty ∧
    ∀ atom : DischargeAtom, atom ∈ carrier.discharges →
      ∀ secondary : ResidualType, secondary ∈ atom.forced_secondaries →
        ∃ witness : DischargeAtom,
          witness ∈ carrier.discharges ∧ witness.primary = secondary

end SixBirdsDualityConfinement.RH.AORPrimitives
