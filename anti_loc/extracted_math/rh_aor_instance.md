# Consolidated math artifact — RH AOR-instance recasting

Source: paper-side AOR-instance recasting of the RH conditional
landing chain, drafted 2026-05-25 by an external AOR-expert model
working from the duality-confinement and RH papers. The agent's
output is preserved at `paper/rh/aor_thread.md`. This extract was
revised on 2026-05-25 after a math-content audit; the audit verdict
report is preserved at `paper/rh/aor_review.md`.

The mathematical role of this artifact is the AOR-instance
membership reading of the closure stack
`Γ_{SDTC-Selberg} ⟹ RH` of `rh_construction.md`. It does not derive
the recognition source, eliminate the `Audit_L` admissibility
hypothesis, or replace the typed real-coordinate disclosure by a
substantive analytic-number-theoretic derivation. It repackages the
same closure records as a local-record `RefStableAOR` membership
witness for the formed Selberg shell `Sel`, citing the AOR
meta-theory of Tsiokos2026AOR for the membership-class semantics.

Labels are stable: `def:rh:aor-<short-name>`, `thm:rh:aor-<short-name>`.
The single remark `rem:rh:aor-partial-status` is paper-only.

Mechanization scope: minimal AOR primitives (residual type enum,
discharge status enum, discharge atom, AOR-instance carrier wrapper,
record-level `RefStableAOR` predicate) defined in a new
`AORPrimitives` module; the AOR-instance carrier and theorems in a
new `AORInstance` module. The membership predicate is provable in
Lean as a typed-interface composition over the bridge fields of the
existing `GammaSdtcSelberg` carrier and the `Audit_L_witness` /
`Audit_L_channel_status` fields of `SatSelShell`. No data-bearing AOR
R-records and no AOR meta-theory derivations are mechanized in this
repo; the meta-theory (cost table of Tsiokos2026AOR
`def:aor:cost-table`, forced-residual theorem
`thm:aor:forced-residual`, refinement-stable characterisation
`thm:aor:refinement-stable-characterisation`, hierarchy
`thm:aor:hierarchy`) is cited at paper level only.

---

## AORPrimitives (minimal AOR meta-theory carriers)

This section records the minimal AOR primitives needed to type the
RH AOR-instance recasting in Lean. The AOR paper of Tsiokos2026AOR
develops the full atlas (twelve residual types, eleven base AOR-8
statuses plus four asymptotic statuses, 132-entry cost table, three
membership classes). The repo encodes only the parts cited by the RH
AOR-instance theorems.

These primitives have no `paper_label` of their own and do not appear
in `paper/notes/statements-of-record.yml`. They are infrastructure
for the labelled definitions and theorems below. The module is
`SixBirdsDualityConfinement.RH.AORPrimitives`.

Required primitives:

- `ResidualType` — enum-like typed listing of the residual primary
  types cited by the RH discharges: `source`, `transport`, `role`,
  `target`, `limit`, `presentation`, `meta`. These are the subset of
  the twelve-type AOR atlas (Tsiokos2026AOR
  `def:aor:residual-types-twelve`) used by this paper. Δ_descent,
  Δ_interface, Δ_local, Δ_global, Δ_horizon, Δ_scale, Δ_sym are not
  needed and not declared.
- `DischargeStatus` — enum-like typed listing of the statuses cited
  by the RH discharges: `zero`, `bridged`, `approved_other`,
  `outside_scope`, `nonclaim`, `by_construction`,
  `asymptotic_budgeted`. These are the subset of the AOR-8 catalogue
  (Tsiokos2026AOR `def:aor:aor-8-statuses`) plus the
  `by_construction` status used for definition-side mechanical
  records and the asymptotic-extension `asymptotic_budgeted` status
  (Tsiokos2026AOR `def:aor:asymptotic-statuses`) used for the
  recognition-source `Δ_limit` component. Every value in this enum
  is a closed (non-`open`) status; the repo does not model the
  `open` status.
- `DischargeAtom` — the minimal triple `(primary, forced_secondaries,
  status)` recording one residual atom's primary residual type, the
  forced secondary types required by Tsiokos2026AOR
  `thm:aor:forced-residual` for that primary, and its declared
  closed discharge status. A discharge witness for a record is a
  finite list of `DischargeAtom` values; each compound record below
  emits multiple atoms.
- `AORInstanceCarrier` — a typed wrapper structure with nine
  fields total: the eight AOR field categories of Tsiokos2026AOR
  (carrier identifier, observations, routes, sources, interfaces,
  constraints, residual discharges, nonclaim register), plus the
  structural `nonclaims_nonempty` witness paired with the nonclaim
  register. Three fields are load-bearing in the minimal scope:
  `discharges : List DischargeAtom` (the residual-discharge
  register), `nonclaims : List String` (the nonclaim register), and
  `nonclaims_nonempty : nonclaims ≠ []` (the structural proof that
  the nonclaim register is populated for every declared scope
  boundary). The other six fields are lightweight typed tags
  (`carrier_id : String`, `observations : List String`,
  `routes : List String`, `sources : List String`,
  `interfaces : List String`, `constraints : List String`) that
  record the AOR field-category labels assigned to the underlying
  `shell` and `gamma` records but do not carry independent
  Lean-substantive content; the load-bearing content lives in the
  existing `shell` and `gamma` records that the AOR-instance
  wrapper takes as inputs. The nine-field shape keeps the
  AOR-instance object structurally honest, makes the nonclaim
  register a real audit channel rather than a black-box `Prop`,
  and lets the Minimal scope avoid re-encoding the substantive
  observation, route, source, interface, and constraint data
  already declared on `shell` and `gamma`.
- `RefStableAOR` — a `Prop`-valued predicate over an
  `AORInstanceCarrier`. The predicate is satisfied when every
  declared `DischargeAtom` in `discharges` has a closed status from
  the enum above (every status in this paper's enum is closed by
  construction), every forced-secondary type declared on a primary
  atom is realized as some other atom's primary type in the same
  discharge list, and the carrier's `nonclaims` list is non-empty
  (carried by the structural `nonclaims_nonempty : nonclaims ≠ []`
  field). This is the
  record-level reading: `RefStableAOR` is a local syntactic
  predicate over the carrier's typed discharge list. It is **not**
  the AOR meta-theory's full refinement-stable characterisation
  (Tsiokos2026AOR `thm:aor:refinement-stable-characterisation`),
  which is cited at paper level but not re-derived; this paper
  uses the record-level predicate as the witness consumed by
  `thm:rh:aor-instance`.

Proof obligations: the primitives are definitional. The
`RefStableAOR` predicate is provable by structural composition over
the listed `DischargeAtom` values. It carries no AOR meta-theorem
content (the meta-theory's cascade termination
`thm:aor:cascade-termination`, confluence
`thm:aor:cascade-confluence`, asymptotic soundness
`thm:aor:asymptotic-soundness`, refinement-stable characterisation
`thm:aor:refinement-stable-characterisation`, and hierarchy
`thm:aor:hierarchy` are paper-level imports from Tsiokos2026AOR, not
re-proven in this repo).

---

## AORInstance (the RH instance recasting)

### def:rh:aor-sel-instance

The **AOR-instance carrier for the saturated completed Selberg trace
shell** is the typed wrapper
```
SelAORInstance(shell, gamma)
```
indexed by:
- `shell : SatSelShell R` — the saturated completed Selberg trace
  closure of `def:rh:sat-sel-shell`,
- `gamma : GammaSdtcSelberg shell` — the Selberg-class recognition
  source carrier of `obl:rh:gamma-sdtc-selberg`.

At the paper level, the wrapper populates the eight AOR field
categories from existing data already declared on `shell` and
`gamma`:
- carrier ← zero side of `shell` (the typed nontrivial-zero ledger
  `Z_ζ^nt` with the audit-quotient data `Q_L`, `M_L`, `π_L` of
  `def:rh:sat-sel-shell`),
- observations ← `Z_nt`, `ψ_-^RH`, `A_Z`, `Vis_L`,
- routes ← `J_L`, `π_L`, the `AntiInvariantZeroLedger` interface
  reading of `ψ_-^RH` (the abstract anti-invariant projector
  `P_-` is deliberately not encoded in Lean per the typed-cone
  scope of the RH paper), the typed bridge from the abstract DC
  apparatus to the shell,
- sources ← `Audit_L_witness` together with `Audit_L_channel_status`,
  `Γ_{SDTC-Selberg}`, the completed domination sequence `(gamma.B_n,
  gamma.domination_records)`,
- interfaces ← the bridge propositions `same_readout`,
  `visible_zero_of_ae`, `mu_zero_of_ae` carried by `gamma`,
- constraints ← positivity in the typed cone, the order `⪯`, trace
  monotonicity, the DC-ledger domination `gamma.A.A_X ⪯ gamma.B_n n`
  and the asymptotic trace condition `gamma.tr_B_n_tends_zero` (the
  shell-side reading `A_Z ⪯ B_n` and `tr B_n → 0` is paper-level
  prose; the Lean source-of-truth records both sides on the abstract
  DC ledger `gamma.A.A_X` and obtains the shell relation only after
  `thm:rh:aor-gamma-bridge-discharge` composes the bridge fields),
- residual discharges ← the seven discharge records of the theorems
  below, expressed as a finite list of `DischargeAtom` values,
- nonclaim register ← the entries of `sec:scope_and_nonclaims` of
  the RH paper plus the AOR-instance-specific nonclaims of
  `rem:rh:aor-partial-status` below (in particular: non-ζ
  Selberg-class L-functions; weak or distributional zero-counting
  functionals; trace shells lacking `Audit_L_witness`; carriers
  outside the typed real-coordinate presentation).

This is a definition, not a derivation. It places existing typed
records into the AOR field order; no new analytic content is
introduced. Lean realises `SelAORInstance` as a wrapper structure
in `SixBirdsDualityConfinement.RH.AORInstance` indexed by `shell`
and `gamma` with a single field `carrier : AORInstanceCarrier`.
A companion `def defaultCarrier shell gamma : AORInstanceCarrier`
provides a documentary default-shape carrier with:
- the six lightweight tag/list fields (`carrier_id`,
  `observations`, `routes`, `sources`, `interfaces`,
  `constraints`) populated with `String` / `List String` labels
  derived from the eight AOR field categories listed above;
- `discharges := []` (the discharge atoms come from the
  discharge defs below and are assembled in `assembledCarrier`); and
- `nonclaims : List String` populated with nine documentary
  entries drawn from `rem:rh:aor-partial-status`, paired with the
  structural `nonclaims_nonempty : nonclaims ≠ []` witness
  discharged by `decide`.

A second companion `def assembledCarrier shell gamma :
AORInstanceCarrier` builds the carrier consumed by the main
AOR-instance theorem by record-updating `defaultCarrier` with
`discharges := mechanicalRecords ++ recognitionDischarge ++ ...`
(concatenation of all seven discharge defs in document order).

The substantive content (the actual observations, routes, sources,
interfaces, constraints) lives in the existing `shell` and `gamma`
records that `SelAORInstance` takes as inputs; the six tag fields
record which `shell`/`gamma` items occupy which AOR category, while
the load-bearing fields (`discharges`, `nonclaims`, and the
structural `nonclaims_nonempty` witness) carry the typed discharge
and nonclaim data that `RefStableAOR` consumes.

---

### thm:rh:aor-mechanical-records

**Statement.** For the scope `S_RH`, the following six paper rows are
AOR-mechanical: `def:rh:fe-involution`, `def:rh:psi-minus-rh`,
`def:rh:nontrivial-zero-ledger`, `def:rh:anti-invariant-zero-ledger`,
`def:rh:sat-sel-shell`, `thm:rh:translation-T`. The five
definition-side rows discharge at status `by_construction` (they
introduce typed records); translation theorem T discharges at status
`zero` over the `AntiInvariantZeroLedger` interface (typed-interface
composition).

**Proof.** The functional-equation involution, the anti-invariant
readout, the nontrivial-zero ledger, the anti-invariant zero ledger,
and the saturated trace shell are introduced as typed records
(`feInvolution`, `psiMinusRh`, `NontrivialZeroLedger`,
`AntiInvariantZeroLedger`, `SatSelShell`). Each emits a
`DischargeAtom` with status `by_construction` carrying its primary
type from its mathematical role (`role` for the involution and
readout, `presentation` for the ledger types, `meta` for the
shell). Theorem T (`translationT`) works entirely inside those
records: its forward direction reads `A_Z = 0` and returns the typed
critical-line statement on `Z_nt`; its reverse direction reads the
critical-line statement and returns `A_Z = 0`. Theorem T therefore
emits a `DischargeAtom` with primary `Δ_target`, forced-secondary
`[Δ_transport]`, and status `zero` (atom proof shape is shared with
`thm:rh:aor-translation-interface-discharge` below).

**Mechanization.** A `def` returning a literal `List DischargeAtom`
of six atoms, classified per the table below:

| Row | primary | forced_secondaries | status |
|---|---|---|---|
| `def:rh:fe-involution` | `Δ_role` | `[]` | `by_construction` |
| `def:rh:psi-minus-rh` | `Δ_role` | `[]` | `by_construction` |
| `def:rh:nontrivial-zero-ledger` | `Δ_presentation` | `[]` | `by_construction` |
| `def:rh:anti-invariant-zero-ledger` | `Δ_presentation` | `[]` | `by_construction` |
| `def:rh:sat-sel-shell` | `Δ_meta` | `[]` | `by_construction` |
| `thm:rh:translation-T` | `Δ_target` | `[Δ_transport]` | `zero` |

The empty forced-secondary lists on the five definition-side atoms
reflect that `by_construction` discharges introduce typed records
whose primary type subsumes any role/target/presentation
obligations; the AOR cost table (Tsiokos2026AOR `def:aor:cost-table`)
records no forced secondaries for `by_construction` discharges of
these primaries. The `translationT` atom carries the
`[Δ_transport]` secondary in keeping with
`thm:rh:aor-translation-interface-discharge`. The discharge list is
consumed by `thm:rh:aor-instance` below.

---

### thm:rh:aor-recognition-discharge

**Statement.** The record `Γ_{SDTC-Selberg}` discharges as four
typed atoms: a primary `Δ_source` atom at status `bridged` (the
provenance record), plus three forced-secondary atoms at the same
typed bridge composition over `gamma`: a `Δ_target` atom at status
`bridged` (the abstract DC ledger `gamma.A.A_X` as the target of the
domination records), a `Δ_role` atom at status `bridged`
("domination source for the self-dual trace closure"), and a
`Δ_limit` atom at status `asymptotic_budgeted` (the asymptotic
trace condition `gamma.tr_B_n_tends_zero`). The forced secondaries
are required by Tsiokos2026AOR `thm:aor:forced-residual` for primary
`Δ_source`.

**Note on the Lean-source target.** The Lean-source domination
records are `gamma.A.A_X ⪯ gamma.B_n n` on the abstract DC
anti-invariant ledger of `gamma.A`. The paper-level reading "the
recognition source supplies `A_Z ⪯ B_n` on the shell" is obtained
only after the bridge composition of
`thm:rh:aor-gamma-bridge-discharge` connects `gamma.A.A_X` with
`shell.A_Z`. This discharge theorem alone speaks of the abstract DC
ledger.

**Note on the asymptotic status.** The trace-vanishing condition
`gamma.tr_B_n_tends_zero` is taken directly as the witness payload
of an `asymptotic_budgeted` discharge per the AOR cost table
(Tsiokos2026AOR `def:aor:cost-table`; `def:aor:asymptotic-statuses`):
a nonnegative trace sequence with limit zero supplies the uniform
finite tail budget required by `asymptotic_budgeted` (the trace
itself is the budget). The repo does not route this through
`summable` (a nonnegative sequence tending to zero need not be
summable — for example `1/n`) or through `contractive` (which would
require per-stage ratios that the recognition source does not
expose). A future strengthening that exhibits summable or
contractive ratios on the domination sequence could promote the
status to `summable` or `contractive` per the AOR soundness chain
`eventual_zero ⇒ contractive ⇒ summable ⇒ asymptotic_budgeted`
(Tsiokos2026AOR `thm:aor:asymptotic-soundness`); the present paper
declares the weakest sufficient status only.

**Mechanization.** A `def` returning a literal `List DischargeAtom`
of four atoms, indexed by `shell` and `gamma` but not computed from
their fields. The four atoms tag the recognition-source content as
the AOR-primitive triple `(primary, forced_secondaries, status)`
with the values stated in the Statement above. The connection to
`gamma.B_n`, `gamma.domination_records`, and `gamma.tr_B_n_tends_zero`
is paper-level: those gamma fields ARE the recognition-source
content that this classification tags. The Lean substantive
composition (consuming the atom list to discharge `RefStableAOR`)
lives in `thm:rh:aor-instance`.

---

### thm:rh:aor-gamma-bridge-discharge

**Statement.** The bridge propositions of `GammaSdtcSelberg`
discharge as five typed atoms. The first three are
field-by-field on `Δ_transport`: a `same_readout` atom at status
`zero` (strict pointwise equality between the abstract DC readout
and the shell readout), a `visible_zero_of_ae` atom at status
`bridged` (visible-support refinement), and a `mu_zero_of_ae` atom
at status `bridged` (the implication transporting "ψ_- vanishes
μ-almost everywhere" to the shell equality `A_Z = 0`). The remaining
two atoms record the forced secondaries required by Tsiokos2026AOR
`thm:aor:forced-residual` for primary `Δ_transport`: a `Δ_role`
atom at status `bridged` and a `Δ_target` atom at status `bridged`.

**Proof.** The abstract DC apparatus speaks about an involutive
object ledger, its anti-invariant readout, its anti-invariant
ledger, and a measure-theoretic fixed-locus consequence. The RH
shell speaks about `J_L`, `ψ_-^RH`, `A_Z`, and the typed zero
ledger. The bridge fields assert that the readouts agree pointwise
where the theorem needs them (`same_readout`, discharged at status
`zero`), that the visible-zero side refines the shell support
(`visible_zero_of_ae`, bridged), and that the abstract conclusion
"ψ_- vanishes μ-almost everywhere" yields the concrete shell
equality `A_Z = 0` (`mu_zero_of_ae`, bridged). The role and target
forced secondaries are discharged by the same typed bridge.

**Mechanization.** A `def` returning a literal `List DischargeAtom`
of five atoms, indexed by `shell` and `gamma` but not computed from
their fields. The field-by-field atom split keeps the per-component
status (`zero` for `same_readout`, `bridged` for the others)
representable in the primitive triple. The connection to
`gamma.same_readout`, `gamma.visible_zero_of_ae`, and
`gamma.mu_zero_of_ae` is paper-level: those bridge propositions ARE
the content that this classification tags as a Δ_transport
discharge with forced secondaries Δ_role and Δ_target. The Lean
substantive composition lives in `thm:rh:aor-instance`.

---

### thm:rh:aor-auditL-discharge

**Statement.** The admissibility audit of `Sel` discharges as one
typed atom: primary `Δ_meta` at status `bridged`, witnessed by
`shell.Audit_L_witness` together with `shell.Audit_L_channel_status`
(the typed Foundations-II admissibility witness and the channel
status carried at shell construction time). The discharge does not
derive admissibility inside this paper.

**Proof.** The shell definition records `Audit_L` as the typed audit
field. The admissibility witness is the value
`shell.Audit_L_witness : shell.Audit_L`, and the channel-status
record `shell.Audit_L_channel_status :
SixBirdsDualityConfinement.F2ChannelStatus` carries the recorded
Foundations-II channel status (the value is whatever the shell
construction assigned; the present paper does not assert any
particular `F2ChannelStatus` equation such as
`= activeProjection`). AOR membership requires that the carrier's
closure apparatus be meta-audited. In the present paper that
meta-audit is supplied as a construction-time hypothesis rather
than unfolded into derived predicates. The correct status is
therefore `bridged`: the carrier provides the admissibility witness
and the recorded channel-status field, while the paper registers a
nonclaim of a separate derivation of that status.

**Mechanization.** A `def` returning a literal singleton `List
DischargeAtom` with primary `ResidualType.meta`,
forced_secondaries `[]`, and status `DischargeStatus.bridged`,
indexed by `shell` and `gamma` but not computed from
`shell.Audit_L_witness` or `shell.Audit_L_channel_status`. The
connection to those shell fields is paper-level: the recorded
admissibility witness and channel status ARE the meta-audit content
that this classification tags as Δ_meta/bridged.

---

### thm:rh:aor-dc-master-import-discharge

**Statement.** The use of the duality-confinement master theorem of
Tsiokos2026SDTC, realised in Lean by `dcMasterApplied`'s bridge to
Paper 1's `masterTheorem`, discharges as four typed atoms: a
primary `Δ_transport` atom at status `approved_other` (the cited
Paper 1 import) plus three forced-secondary atoms for primary
`Δ_transport` (a `Δ_source` atom at `bridged` recording the Paper 1
citation as the provenance, a `Δ_role` atom at `bridged` recording
"duality-confinement membrane theorem" as the role, and a
`Δ_target` atom at `bridged` recording `shell.A_Z = shell.A_Z.zero`
as the target after the bridge fields of
`thm:rh:aor-gamma-bridge-discharge` apply).

**Proof.** The master theorem is not re-proved in this paper. It is
imported as the abstract typed positive-cone theorem of Paper 1. The
imported theorem consumes positive domination records and a
vanishing trace budget and returns the zero anti-invariant ledger.
The status `approved_other` is admissible for primary `Δ_transport`
per the AOR cost table (Tsiokos2026AOR `def:aor:cost-table`); the
forced secondaries are listed in Tsiokos2026AOR
`thm:aor:forced-residual` for the primary `Δ_transport`.

**Mechanization.** A `def` returning a literal `List DischargeAtom`
of four atoms, indexed by `shell` and `gamma` but not invoking or
witnessing `DCMasterApplied.dcMasterApplied`. The connection to the
cross-paper import is paper-level: the cited Paper 1 master
theorem (via `dcMasterApplied`) IS the imported content that this
classification tags as Δ_transport/approved_other with three forced
secondaries.

---

### thm:rh:aor-real-coordinate-discharge

**Statement.** The typed real-coordinate carrier discharges as two
paired typed atoms: a primary `Δ_presentation` atom at status
`outside_scope` (the supplied typed `RealCoordinate` carrier is
declared outside the analytic-number-theoretic identification
scope), paired with a second `Δ_presentation` atom at status
`nonclaim` (the analytic identification with the classical real-part
function on zeta zeros is explicitly registered as a nonclaim).
Both atoms are forced-secondary-free `[]`; the cost-table pairing
between `outside_scope` and `nonclaim` is the AOR-required pattern
for presentation residuals discharged outside their formal scope
(Tsiokos2026AOR `def:aor:cost-table`).

**Proof.** The paper statement writes `Re(ρ) - 1/2`. The formalised
carrier uses the typed `Involution.RealCoordinate` parameter `R`
supplying the operations and positivity principles needed by
Theorem T. The identification of `R` with the classical real part of
a zeta zero is paper-side construction-parameter content; this paper
does not derive that analytic identification in Lean. The
presentation residual is closed not by deriving the analytic
identification but by emitting the paired `outside_scope` and
`nonclaim` discharge atoms; the corresponding nonclaim register
entry is added to the carrier's nonclaim register.

**Mechanization.** A `def` returning a literal `List DischargeAtom`
of two atoms — `(primary = ResidualType.presentation,
forced_secondaries = [], status = DischargeStatus.outside_scope)`
and `(primary = ResidualType.presentation,
forced_secondaries = [], status = DischargeStatus.nonclaim)` —
indexed by `shell` and `gamma` but not computed from the `R :
Involution.RealCoordinate` parameter. The connection is paper-level:
`R` IS the typed real-coordinate carrier that this classification
tags as paired presentation discharges, and the paired
nonclaim-register entry lives in the carrier's `nonclaims` list.

---

### thm:rh:aor-translation-interface-discharge

**Statement.** Translation theorem T discharges as one typed atom:
primary `Δ_target` with forced secondary `[Δ_transport]`, both at
status `zero` (typed-interface composition closes both axes at zero
on the `AntiInvariantZeroLedger` carrier). The theorem transports
the typed equality `A_Z = 0` to the typed critical-line readout on
`Z_nt`, and conversely.

**Proof.** The proof of Theorem T is a positive-sum argument over
the declared ledger. The target `A_Z` is a finite typed sum of
nonnegative multiplicity-weighted square displacements, and the zero
target is equivalent to the vanishing of every displacement. The
target-readout and transport obligations are not external analytic
claims; they are the internal typed-interface content of
`thm:rh:translation-T-forward` and `thm:rh:translation-T-reverse`.

**Mechanization.** A `def` returning a literal `List DischargeAtom`
of two atoms (the primary `Δ_target` atom with forced_secondaries
`[Δ_transport]` and the matching `Δ_transport` witness atom), both
at status `zero`, indexed by `shell` and `gamma` but not invoking
`TranslationT.translationT`. The connection is paper-level: the
typed-interface composition over `AntiInvariantZeroLedger` fields
that justifies the zero status IS the content of
`TranslationT.translationT`; the classification tags that content
as a Δ_target/zero discharge with a Δ_transport forced secondary.

---

### thm:rh:aor-instance

**Statement (Lean).** Under the discharges recorded in
`thm:rh:aor-mechanical-records`, `thm:rh:aor-recognition-discharge`,
`thm:rh:aor-gamma-bridge-discharge`, `thm:rh:aor-auditL-discharge`,
`thm:rh:aor-dc-master-import-discharge`,
`thm:rh:aor-real-coordinate-discharge`, and
`thm:rh:aor-translation-interface-discharge`, the saturated completed
Selberg trace shell satisfies the record-level `RefStableAOR`
predicate on the assembled-carrier shape:
```
RefStableAOR (assembledCarrier shell gamma)
```
where `assembledCarrier shell gamma` is the
`AORInstanceCarrier` value obtained from `defaultCarrier shell gamma`
by overwriting its `discharges` field with the concatenation of the
seven discharge lists above (in document order:
mechanicalRecords ++ recognitionDischarge ++ gammaBridgeDischarge ++
auditLDischarge ++ dcMasterImportDischarge ++
realCoordinateDischarge ++ translationInterfaceDischarge). The
wrapper structure `SelAORInstance shell gamma` of
`def:rh:aor-sel-instance` is the typed slot for that assembled
carrier; the Lean theorem is stated directly over `assembledCarrier`
to keep the proof's case analysis aligned with the literal discharge
list.

**Statement (paper-level consequence).** At the record level of this
AOR instance, the typed zero ledger of `Sel` has no nontrivial zeros
off the fixed locus `Fix(J_L)`. This consequence is not a separate
Lean output of the AOR-instance theorem: it is the conclusion of
`thm:rh:conditional` read in the AOR membership register, obtained
through the same closure stack (recognition source → DC master
theorem → translation theorem T forward). The Lean realisation
returns only `RefStableAOR (assembledCarrier shell gamma)`; the
paper-level critical-line reading is a downstream paper-prose
consequence composed from `RHConditional.rhConditional`.

**Proof.** The seven discharge defs above each produce a literal
`List DischargeAtom`. Their concatenation populates the `discharges`
field of `assembledCarrier shell gamma`. The proof of `RefStableAOR`
proceeds by case analysis on the secondary residual type (the
`secondary` variable introduced by the universally quantified
forced-secondary clause): for each of the seven `ResidualType`
constructors, the proof exhibits an explicit witness atom from the
assembled discharge list whose primary type matches that
constructor. The case analysis is on the secondary type rather than
on the atom (or atom/secondary pair) because `RefStableAOR`'s
forced-secondary clause is set-theoretic over primary types: only
membership of SOME atom with the right primary in the discharge
list is required. The witness atoms picked match the audit semantics
of the requesting primary (e.g., the `role` witness is picked from
the bridged role atoms of recognition / bridge / DC-import, not from
the `by_construction` role atoms of mechanical records, to keep the
audit class aligned). The structural `nonclaims_nonempty :
nonclaims ≠ []` clause is discharged by `decide` on the concrete
nine-entry `nonclaims` list of `defaultCarrier`. The paper-level
critical-line consequence stated above follows separately:
translation theorem T converts `A_Z = 0` (obtained through the same
closure stack as `thm:rh:conditional`) into the critical-line
statement on `Z_nt`, and the AOR-instance recasting therefore
inherits the same conclusion at the record level.

**Scope of the membership predicate.** `RefStableAOR` in this paper
is the local syntactic predicate over the carrier's typed discharge
list; it is *not* the AOR meta-theory's full refinement-stable
characterisation (Tsiokos2026AOR
`thm:aor:refinement-stable-characterisation`), which is cited at
paper level and not re-derived here. The record-level reading is
sufficient for the AOR-instance theorem: the paper claim is
membership at the record level under the declared discharge
assignment, not a derivation of the AOR refinement-stable
characterisation.

**Mechanization.** A theorem returning a single value of type
`RefStableAOR (assembledCarrier shell gamma)`. The proof composes the
discharge lists of the seven theorems above into the carrier's
residual-discharge register and discharges the `RefStableAOR`
predicate by structural composition. Provable as a typed-interface
composition. The Lean theorem does **not** return the critical-line
statement on `Z_nt`; that statement remains the conclusion of
`RHConditional.rhConditional`, and the AOR-instance theorem records
the record-level membership independently.

---

### rem:rh:aor-partial-status (paper-only)

The present AOR-instance theorem is a paper-level classification of
the existing closure records. The Lean realisation in
`AORInstance.lean` carries the bridge propositions as `Prop`-valued
typed hypotheses inherited from `GammaSdtcSelberg`. The AOR-instance
proof therefore projects the discharges through the carrier-attached
wrapper: it checks that the carrier has the required propositions,
but it does not inspect data-bearing R-record values. Promotion of
the recognition source, bridge fields, admissibility witness, and
real-coordinate assignment to data-bearing AOR records is deferred.

The AOR-instance reading additionally restricts to the typed zero
ledger of `Sel` and the saturated completed Selberg trace shell over
`Λ_ζ`. No AOR-membership claim is made for:
- primitive Selberg-class L-functions other than `ζ`,
- weak or distributional zero-counting functionals,
- trace shells lacking the declared `Audit_L_witness` admissibility
  field,
- carriers outside the typed real-coordinate presentation disclosed
  in `sec:involution_and_ledger` and in the formalisation appendix.

This remark is paper-only and is not added to the manifest or to
`paper/notes/statements-of-record.yml`.

---

## Out-of-scope

The following are intentionally not mechanized in this repo:
- The AOR meta-theory of Tsiokos2026AOR: the eight-stratum
  decomposition (`thm:aor:eight-stratum-decomposition`), the
  twelve-type residual atlas in full
  (`def:aor:residual-types-twelve`), the 132-entry cost table
  (`def:aor:cost-table`), the forced-residual theorem
  (`thm:aor:forced-residual`), the cascade termination
  (`thm:aor:cascade-termination`), the cascade confluence
  (`thm:aor:cascade-confluence`), the asymptotic soundness chain
  (`thm:aor:asymptotic-soundness`), the refinement-stable
  characterisation (`thm:aor:refinement-stable-characterisation`),
  and the hierarchy theorem (`thm:aor:hierarchy`). All of these are
  cited at paper level.
- Data-bearing R-record promotion: the bridge fields remain
  `Prop`-valued typed hypotheses; promotion to data-bearing AOR
  records is a future strengthening.
- Substantive admissibility derivation for `Audit_L`: handled at
  meta-theory level by Foundations II; here taken as construction-time
  hypothesis carried by `Audit_L_witness` and
  `Audit_L_channel_status`.
- Substantive real-coordinate identification: the typed
  `Involution.RealCoordinate` parameter `R` remains
  parameter-assigned at shell instantiation; classical analytic
  identification is `outside_scope`/`nonclaim`.
- AOR-membership claims outside the typed zero ledger of `Sel`:
  non-`ζ` Selberg-class L-functions, weak or distributional
  zero-counting functionals, trace shells lacking `Audit_L_witness`,
  and carriers outside the typed real-coordinate presentation are
  all explicitly out of scope per `rem:rh:aor-partial-status`.
