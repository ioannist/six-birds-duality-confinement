# RH AOR-instance math-extract — review audit trail

Three review rounds were performed on `anti_loc/extracted_math/rh_aor_instance.md`
between 2026-05-25 (initial draft) and 2026-05-25 (final pass) by an
external AOR-expert reviewer. The extract was revised between each
round to address the cited findings. This file preserves the
verdicts as the audit trail referenced by the extract header.

The audited scope was the math-content design of the RH AOR-instance
recasting only (atlas typing, primitive scope, mechanizability,
fidelity to the agent's section, cross-paper citations). Codex Lean
mechanization had not yet begun at the time of these reviews.

---

## Round 1 verdict — BLOCK

### Axis A — REVISE

- `def:rh:aor-sel-instance`: mostly faithful to `paper/rh/aor_thread.md`,
  but the extract says the carrier constraints include `A_Z ⪯ B_n`
  directly. The current Lean/RH disclosure discipline says
  `gamma.domination_records` are over the abstract DC ledger
  `gamma.A.A_X`; the link to shell `A_Z` is via bridge fields. Fix:
  distinguish paper-level reading "`A_Z ⪯ B_n`" from Lean-source
  truth "`gamma.A.A_X ⪯ gamma.B_n n`, then bridge to shell `A_Z`."

- `thm:rh:aor-recognition-discharge`: faithful to the agent's
  theorem, but inherits the same direct-`A_Z` simplification. Fix:
  say the recognition source supplies domination records for the DC
  anti-invariant ledger carried by `gamma`, and the `A_Z`
  interpretation is obtained only after
  `thm:rh:aor-gamma-bridge-discharge`.

- `rem:rh:aor-partial-status` / `Out-of-scope`: the extract
  preserves the partial-status disclosure, but drops AOR-specific
  scope limits from the agent's conclusion addition: no AOR
  membership for primitive Selberg-class L-functions beyond ζ,
  weak/distributional zero-counting functionals, trace shells
  lacking `Audit_L`, or carriers outside the typed real-coordinate
  presentation. Fix: add these to the nonclaim register or
  Out-of-scope section.

### Axis B — REVISE

- `thm:rh:aor-recognition-discharge`: primary `Δ_source` with forced
  `{Δ_target, Δ_role, Δ_limit}` is correct. The defect is
  representational: the mechanization plan records only one
  `DischargeRecord` with status `bridged`, so the `Δ_limit` status
  `asymptotic_trace_vanishing` is lost. Fix: either split out a
  second `DischargeRecord` for the limit component, or extend
  `DischargeRecord` with component statuses.

- `thm:rh:aor-recognition-discharge`: if `asymptotic_trace_vanishing`
  is intended as the AOR atlas status, define its relation to the
  AOR chain `eventual_zero ⇒ contractive ⇒ summable ⇒
  asymptotic_budgeted`. Otherwise rename it to the atlas status
  `asymptotic_budgeted` and describe trace-vanishing as the witness.
  Current text does not locate the status in the chain.

- `thm:rh:aor-gamma-bridge-discharge`: `Δ_transport` with forced
  `{Δ_role, Δ_target}` is plausible and matches the brief. But the
  "same_readout component at zero" is not representable by the
  primitive triple `(primary, secondaries, status)`. Fix: split
  `same_readout` into its own zero-status discharge record, or add
  nested/component discharge records.

- `thm:rh:aor-real-coordinate-discharge`: `Δ_presentation` with
  `outside_scope`/`nonclaim` is correct. Mechanically, though,
  there is no existing "construction-parameter assignment record on
  `shell`" to project. Fix: either add that field to
  `SelAORInstance`, or state the proof uses the explicit
  `R : RealCoordinate` parameter plus the nonclaim register.

### Axis C — BLOCK

- `thm:rh:aor-mechanical-records`: not mechanizable under the stated
  primitives. It mentions `AORInstanceCarrier.Mechanical` and
  `by_construction`, but neither is listed in `AORPrimitives`. Fix:
  add a `Mechanical` witness type and `by_construction` status, or
  rewrite the theorem to return ordinary `DischargeRecord`s using
  existing statuses.

- `thm:rh:aor-recognition-discharge` and
  `thm:rh:aor-gamma-bridge-discharge`: as above, Minimal primitives
  cannot encode component statuses. Codex would either drop the
  limit/zero facts or invent an unplanned structure. Fix before
  dispatch.

- `thm:rh:aor-auditL-discharge`: "projection from `shell.Audit_L`"
  is too weak: `Audit_L` is a type field; the witness/status live
  in `Audit_L_witness` / `Audit_L_channel_status` in the shell. Fix
  the proof shape to cite the witness/status fields.

- `thm:rh:aor-instance`: mechanizable only if `RefStableAOR` is
  deliberately defined as a local syntactic predicate over closed
  discharge records. It is not mechanizable if it is meant to invoke
  Tsiokos2026AOR's refinement-stable characterisation theorem. Fix:
  explicitly name the Lean predicate something like
  `RefStableAORRecord` or add a sentence that this is a local record
  predicate, not the full AOR meta-theorem.

### Axis D — REVISE

- `AORPrimitives`: under-includes concepts actually used later:
  `by_construction`, `Mechanical`, component/nested discharge
  records, and either `open` or an explicit closed-status predicate.
  Fix by adding these or removing their use.

- `AORPrimitives`: `RefStableAOR` says every residual has non-`open`
  status, but `open` is not in `DischargeStatus`. Fix: either add
  `open` and prove records are not open, or define `ClosedStatus`
  directly over the listed statuses.

- `def:rh:aor-sel-instance`: "anti-invariant projection implicit in
  `A_Z`" risks reintroducing a projector that the RH/DC disclosure
  explicitly says Lean does not construct. Fix: call this the typed
  `AntiInvariantZeroLedger` interface / `ψ_-^RH` readout, not an
  implicit projection route.

- `Out-of-scope`: honest but incomplete; add the AOR-instance scope
  exclusions from the agent's conclusion addition, especially
  non-ζ Selberg-class L-functions and weak/distributional
  zero-counting.

- Non-elimination discipline: PASS.

### Axis E — REVISE

- Paper 1 references: mostly accurate.

- AOR references: too generic for a canonical mechanization extract.
  The review brief names `Thm:aor:forced-residual` and
  `thm:aor:refinement-stable-characterisation`; the extract should
  cite those exact theorem names where it assigns forced
  secondaries and where it refuses to mechanize full
  refinement-stable semantics. Fix: add explicit paper-level
  citations to the forced-residual theorem, cost table, and
  refinement-stable characterisation.

- Typed-bridge wording: PASS with one caveat. The extract mostly
  uses "typed bridge composition" / "not derived" language. The
  caveat is the direct `A_Z ⪯ B_n` phrasing discussed above; it
  should be adjusted to avoid contradicting the RH paper's
  Round-4/5 bridge disclosure.

### Summary Verdict

Do not dispatch Codex on this extract as-is. The atlas typing is
directionally sound, but the Minimal primitives do not yet type the
planned theorem statements because `Mechanical`, `by_construction`,
nested/component statuses, and the asymptotic limit-status record
are missing. The smallest unblocker is to revise the
extract/primitives so every status actually mentioned is
representable, split or extend discharge records for `Δ_limit` and
`same_readout`, and restore the dropped AOR-specific nonclaims.

---

## Round 2 verdict — REVISE (small)

### Axis A — REVISE

- `def:rh:aor-sel-instance`: the revised extract no longer matches
  the stated mechanization plan of an eight-field
  `AORInstanceCarrier`. It says Lean will encode only `discharges`
  and `nonclaims_nonempty`, with the other six categories paper-side.
  That is defensible as a smaller Lean scope, but it is a silent
  weakening relative to the task statement and the agent's section,
  which presents eight typed fields. Fix: either restore an
  eight-field carrier, even if most fields are lightweight
  metadata/Prop fields, or explicitly revise the plan to "two-field
  record-level carrier plus paper-side eight-category
  classification."

- `def:rh:aor-sel-instance`: good correction relative to the earlier
  direct `A_Z ⪯ B_n` issue. The extract now distinguishes
  `gamma.A.A_X ⪯ gamma.B_n n` from the paper-level shell reading.
  This is less literal to the agent's original section, but
  mathematically better and faithful to the RH disclosure
  discipline.

- `rem:rh:aor-partial-status`: PASS. The missing AOR-specific scope
  exclusions from the previous pass are now preserved.

### Axis B — REVISE

- `thm:rh:aor-recognition-discharge`: the asymptotic-status
  explanation is mathematically wrong as written. A nonnegative
  sequence tending to zero is not "in particular summable on a
  cofinal tail" (e.g. `1/n`). Fix: do not route trace-vanishing
  through summability. Say either "trace-vanishing is taken
  directly as the witness payload for `asymptotic_budgeted` per the
  AOR cost table," or add a real summability/ratio hypothesis if
  you want to use the chain through `summable`.

- `thm:rh:aor-recognition-discharge`: primary `Δ_source` with
  forced `{Δ_target, Δ_role, Δ_limit}` is now representable by four
  atoms. PASS subject to the asymptotic fix above.

- `thm:rh:aor-gamma-bridge-discharge`: PASS. The split into five
  atoms fixes the prior component-status problem; `same_readout` at
  `zero` and the other bridge fields at `bridged` are now
  expressible.

- `thm:rh:aor-real-coordinate-discharge`: mostly correct, but
  `nonclaim` is in `DischargeStatus` while this row emits only an
  `outside_scope` atom plus a nonclaim-register entry. Fix: either
  emit a paired `nonclaim` atom or remove `nonclaim` from
  `DischargeStatus` and keep nonclaims solely in the register.

### Axis C — REVISE

- `AORPrimitives`: the local `RefStableAOR` scope is now clear and
  avoids requiring the full AOR refinement-stable characterisation
  theorem. PASS.

- `thm:rh:aor-instance`: the statement mixes two conclusions. It
  states `RefStableAOR (SelAORInstance(shell, gamma))` and then
  adds that the typed zero ledger has no zeros off `Fix(J_L)`, but
  the mechanization paragraph only promises a proof of
  `RefStableAOR`. Fix: choose one of:
  - make the Lean theorem return a conjunction
    `RefStableAOR ... ∧ ∀ ρ, ...`;
  - or say the critical-line sentence is a paper-level consequence
    obtained separately from `rhConditional` / `TranslationT`, not
    part of the AOR-instance Lean theorem.

- `thm:rh:aor-auditL-discharge`: mechanizability depends on what
  "channel acceptance" means. The existing Lean field has type
  `F2ChannelStatus`, but no equality to `activeProjection` is
  present. Fix: either avoid "acceptance" wording and use it as
  recorded channel status only, or add an explicit acceptance
  predicate/equality if the discharge requires acceptance.

- `thm:rh:aor-mechanical-records`: now mechanizable as a
  `List DischargeAtom`, but only if each mechanical atom's
  forced-secondary list is either empty or explicitly populated.
  Fix: specify the forced-secondary lists for these six atoms, even
  if all are `[]`.

### Axis D — REVISE

- `AORPrimitives`: possible over-inclusion: `nonclaim` appears as a
  discharge status but is not actually used by any emitted atom.
  Fix as above: use it in a paired atom or remove it.

- `AORPrimitives`: the two-field carrier is sufficient for the
  local predicate, but not for the stated eight-field AOR carrier
  plan. This is the main scope mismatch. Fix by aligning the text
  and implementation plan.

- `Out-of-scope`: PASS.

- Non-elimination discipline: PASS.

### Axis E — PASS

- Paper 1 references are accurate.

- AOR references are now specific enough: forced residuals, cost
  table, asymptotic soundness, refinement-stable characterisation,
  hierarchy, termination, and confluence are named explicitly. The
  only correction needed is the asymptotic implication claim under
  Axis B.

- Typed-bridge language is consistent with the RH paper's
  disclosure discipline.

### Summary Verdict

Proceed after a small revision pass, not as-is. The previous
structural blockers are largely fixed, but the extract still needs
three cleanups before Codex should inherit it: correct the false
"trace-vanishing implies summable" statement, resolve the two-field
vs eight-field `AORInstanceCarrier` mismatch, and clarify whether
`thm:rh:aor-instance` proves only `RefStableAOR` or also returns
the typed critical-line conclusion.

---

## Round 3 verdict — REVISE (narrow)

### Axis A — REVISE

- `def:rh:aor-sel-instance` vs `AORPrimitives`: the extract now says
  `AORInstanceCarrier` has eight fields, but later says the eight
  AOR categories "are not separate fields of the Lean structure."
  Fix this wording. It should say either:
  - `SelAORInstance` contains/constructs an eight-field
    `AORInstanceCarrier`, with six lightweight tag/list fields plus
    `discharges` and `nonclaims_nonempty`; or
  - the Lean wrapper is not eight-field, and the primitives section
    should stop claiming it is.

- `thm:rh:aor-recognition-discharge`: PASS. The extract now
  correctly distinguishes Lean-source domination on `gamma.A.A_X`
  from paper-level `A_Z` reading after bridge composition.

- `rem:rh:aor-partial-status`: PASS. The AOR-specific exclusions
  from the agent's section are now preserved.

- Minor hygiene: the extract references `paper/rh/aor_review.md`,
  but that file is currently missing. Either add it or remove the
  claim.

### Axis B — PASS

- Recognition source typing is now defensible: `Δ_source` primary,
  forced `Δ_target`, `Δ_role`, `Δ_limit`, with `Δ_limit` emitted
  separately at `asymptotic_budgeted`.

- The asymptotic chain issue is fixed. The extract no longer claims
  limit-zero implies summability; it explicitly avoids the
  `summable` and `contractive` promotions.

- Bridge fields, `Audit_L`, DC master import, real-coordinate
  discharge, and Translation T now have complete atom/status
  representations. The paired `outside_scope` + `nonclaim`
  presentation atoms are especially clean.

### Axis C — REVISE

- Main mechanizability is now plausible: each labelled theorem
  returns a `List DischargeAtom`, and `thm:rh:aor-instance` returns
  only `RefStableAOR (SelAORInstance shell gamma)`. The earlier
  overclaim about also returning the critical-line theorem is fixed.

- Remaining mechanization risk is the same carrier-shape ambiguity
  from Axis A. Codex needs a single target: either implement eight
  fields directly, or implement a wrapper with an embedded
  eight-field carrier. The extract currently says both.

- `thm:rh:aor-mechanical-records`: PASS. Forced-secondary lists are
  now explicit.

### Axis D — REVISE

- Minimal scope is sufficient after the latest revisions:
  `ResidualType`, `DischargeStatus`, `DischargeAtom`,
  `AORInstanceCarrier`, and local `RefStableAOR` type all rows.

- No evident over-inclusion remains: `nonclaim` is now used by the
  real-coordinate paired atom.

- Out-of-scope disclosure is now honest and complete, including
  non-ζ Selberg-class L-functions, weak/distributional zero-counting,
  missing `Audit_L_witness`, and carriers outside the typed
  real-coordinate presentation.

- Revision needed only for the carrier-scope wording conflict: the
  extract must not describe the eight categories as both Lean
  fields and non-fields.

### Axis E — PASS

- Paper 1 citation language is accurate: `dcMasterApplied` is
  described as a bridge to Paper 1's `masterTheorem`, not a
  re-proof.

- AOR citations are specific and placed correctly: cost table,
  forced-residual theorem, asymptotic soundness, refinement-stable
  characterisation, and hierarchy are all named where relevant.

- Typed-bridge composition language matches the RH paper's
  disclosure discipline: the extract says composition through
  `GammaSdtcSelberg` bridge fields and keeps `Audit_L`,
  `RealCoordinate`, and recognition-source content as supplied
  records rather than derived facts.

### Summary Verdict

REVISE, narrowly. The substantive AOR atlas typing and
non-elimination discipline are now sound enough for mechanization
planning. The smallest unblocker is to resolve the carrier-shape
contradiction in `def:rh:aor-sel-instance` / `AORPrimitives`, and
either add the referenced `paper/rh/aor_review.md` or remove that
reference.

---

## Disposition

After Round 3 the extract was patched to (a) describe
`SelAORInstance` as constructing an eight-field `AORInstanceCarrier`
(with six lightweight tag fields plus the two load-bearing fields),
resolving the carrier-shape contradiction; and (b) save this audit
file at the location the extract references. With those two narrow
fixes, the extract is the agreed scaffolding plan for the upcoming
Codex Lean dispatches.

---

## Round 4 verdict — REVISE (followed by revision pass)

After the AOR-instance Lean mechanization landed as commit
`bcc7ff0`, a second-pass review surfaced these findings:

### Axis A — REVISE
Forced-secondary rule under-encoded: recognition, bridge, and
DC-import primaries emitted their forced secondaries as separate
atoms with empty secondary lists, but the extract describes these
as forced secondaries OF the primary residuals. Fix: put the
forced lists on the primary atoms while keeping the witness atoms.

### Axis B — REVISE
1. Proof had 21 rcases for a 24-atom register (Lean deduplicates
   equal list members). Cosmetic finding; mathematical content
   unchanged. **Disposition: skipped** — occurrence-level not
   required for `RefStableAOR`'s set-of-primaries semantics.
2. `nonclaims_nonempty := True` is a tautological register
   witness. Fix: store an actual nonclaim list and prove it
   nonempty.

### Axis C — PASS
All eight theorem declarations clean; `aorInstance` axiom closure
`[propext]` within trust base; zero forbidden tokens.

### Axis D — REVISE
The discharge defs do not use the gamma/shell fields the extract
claimed they project from (recognition: no
`gamma.B_n`/`gamma.domination_records`/`gamma.tr_B_n_tends_zero`;
bridge: no `gamma.same_readout`/`.visible_zero_of_ae`/`.mu_zero_of_ae`;
auditL: no `shell.Audit_L_witness`/`.Audit_L_channel_status`;
DC-import: no `DCMasterApplied.dcMasterApplied`;
translation: no `TranslationT.translationT`). Fix: either add
witness/spec theorems, OR revise extract/registry wording to
"literal AOR classification indexed by shell/gamma."

### Axis E — PASS
Minimal scope preserved; `RefStableAOR` local syntactic predicate;
no AOR meta-theory imports; RH conditional not promoted to
unconditional.

### Axis F — REVISE
1. Seven entries marked `status = "theorem"` but Lean uses `def`s.
   Fix: convert to definition coverage or add theorem wrappers.
2. Source line anchors loose (e.g., `def:rh:aor-sel-instance`
   pointed at line 113; label starts at line 131).

### Disposition

A revision pass addressed all REVISE findings without rollback:

1. **Fix Dispatch 6** (codex, same RH session): replaced
   `nonclaims_nonempty : Prop` in `AORInstanceCarrier` with paired
   `nonclaims : List String` + `nonclaims_nonempty : nonclaims ≠ []`
   structural witness. Updated `RefStableAOR` accordingly.
   `deriving DecidableEq` added to ResidualType, DischargeStatus,
   DischargeAtom for downstream `decide` proofs.

2. **Fix Dispatch 7** (codex, same RH session): populated
   forced_secondaries on the four primary atoms (recognition source
   `[target, role, limit]`; bridge same_readout `[role, target]`;
   DC-import `[source, role, target]`; translation
   `[transport]` — already correct). Populated `defaultCarrier.nonclaims`
   with nine documentary entries from `rem:rh:aor-partial-status`.
   Refit `aorInstance` proof: case-on-secondary-type pattern with
   explicit witness atom per residual type (7 cases). Axiom closure
   remains `[propext]`.

3. **Axis D + F-1 fix** (Claude, no codex): rather than add witness
   theorems, revised extract and registry to honest
   "literal AOR classification" framing. The discharge defs return
   fixed-shape literal lists indexed by shell/gamma but not
   computed from their fields; substantive composition lives in
   aorInstance. Manifest/SoR `status` changed from `theorem` to
   `definition` for the seven list-producing defs; `[[claim]]` →
   `[[definition]]` in the manifest; `lean_coverage: theorem` →
   `definition` in the SoR. The aorInstance row stays as `theorem`.

4. **Axis F-2 fix**: re-anchored all AOR rows' `line_start` /
   `line_end` to the actual extract heading lines (def:rh:aor-sel-instance
   was off by 18; others off by 1-2). Inventory `kind = "theorem"`
   changed to `"definition"` for the seven discharge entries.

Per-entry status after revision:

| Label | kind/coverage | status |
|---|---|---|
| def:rh:aor-sel-instance | definition | wrapper structure |
| thm:rh:aor-mechanical-records | definition | literal classification (6 atoms) |
| thm:rh:aor-recognition-discharge | definition | literal classification (4 atoms) |
| thm:rh:aor-gamma-bridge-discharge | definition | literal classification (5 atoms) |
| thm:rh:aor-auditL-discharge | definition | literal classification (1 atom) |
| thm:rh:aor-dc-master-import-discharge | definition | literal classification (4 atoms) |
| thm:rh:aor-real-coordinate-discharge | definition | literal classification (2 paired atoms) |
| thm:rh:aor-translation-interface-discharge | definition | literal classification (2 atoms) |
| thm:rh:aor-instance | theorem | RefStableAOR membership proof |

Validators green; axiom closure of `aorInstance` is `[propext]`
(within trust base). The mechanization is now claim-tight as the
implementation of the extract.
