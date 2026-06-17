# Math + Lean Companion-form discipline (2026-05-27)

Target shape for both RH and DC papers: **math body with full proofs;
per-theorem footnote at honest fidelity; appendix as canonical
disclosure venue.** Three layers, three jobs, none doing the others'
work.

This document is the rule book for every codex dispatch in this
restructure. Quote it; do not paraphrase it.

## The three layers

### Layer 1 — Body = math

- Every load-bearing concept gets a formal environment (`\begin{definition}`,
  `\begin{theorem}`, `\begin{lemma}`, `\begin{proposition}`). Central
  objects living only as prose paragraphs is a failure mode; promote
  them.
- **Every theorem in the body gets a full mathematical proof.** Not a
  sketch that defers to mechanization. The reader of the body should
  never need to consult the Lean code to verify the argument.
- Proofs read as standard mathematical prose: hypotheses unpacked,
  cases enumerated, conclusions derived. No "Lean proves the iff
  packaging" or "Lean composes the bridge fields" inside proof flow.
- **The following do NOT appear in body prose**:
  - Lean module / declaration / structure-field names (`\texttt{...}`,
    `\nolinkurl{Module.X}`, `same_readout`, `mu_zero_of_ae`, etc.).
  - Phrases of the form "Lean composes / records / projects /
    packages / encodes / checks / proves" describing what Lean
    does at this point.
  - Narrowing-disclosure prose ("the Lean realization carries...",
    "the formalization harness tracks...", "the disclosure in App D
    records this narrowing").
- Where the formal argument leans on a classical result, cite it as
  a one-line input; do not reprove, sketch, or pretend the framework
  derives it.

### Layer 2 — Footnotes = honest mechanization claim

After each numbered theorem's proof (or attached to its title), exactly
one footnote. **The footnote wording must match the actual coverage
mode**, per the table in §App D / per `statements-of-record.yml`.

#### Footnote wording table

| Coverage mode | Permitted footnote wording |
|---|---|
| `lean_substantive` (pure derivation, faithful alignment) | "Verified in Lean as `Namespace.identifier`; see App~\ref{app:formalization}." |
| `lean_substantive` (typed-interface composition, faithful) | "Verified in Lean as `Namespace.identifier` via typed-interface composition over the `<Carrier>` fields; see App~\ref{app:formalization}." |
| `lean_substantive` (typed-bridge composition, faithful) | "Verified in Lean as `Namespace.identifier` via typed-bridge composition over the recognition-source carrier; see App~\ref{app:formalization}." |
| `lean_substantive` (faithful but narrowed/partial alignment) | "Verified in Lean as `Namespace.identifier`; the Lean conclusion is the X form of the paper statement, with the narrowing recorded in App~\ref{app:formalization}." |
| `projection_over_record` / literal-data definition | "Tracked in the formalization harness as `Namespace.identifier`, a conditional schema over the recognition-source record; see App~\ref{app:formalization}." (Do NOT say "Lean proves" or "verified in Lean".) |
| `definition_entry` (faithful typed mirror, trivial) | No footnote needed; the appendix table is sufficient. |
| `definition_entry` (with representation note, e.g. A3 real-coordinate, admissibility-as-hypothesis) | "Realized in Lean as `Namespace.identifier`; the X representation choice is recorded in App~\ref{app:formalization}." |
| `typed_carrier` (recognition source as carrier structure) | "Encoded in Lean as a typed structure carrier `Namespace.identifier`, not as a Lean axiom; downstream theorems take a value of this carrier as an explicit hypothesis. See App~\ref{app:formalization}." |
| `harness_tracked` (projection over explicit hypothesis) | "Tracked in the formalization harness as `Namespace.identifier`, a projection over the explicit hypothesis X; see App~\ref{app:formalization}." |

**Wording is canonical, not editorial.** Calling a `projection_over_record`
theorem "verified in Lean" misrepresents the work. A careful reviewer
will catch this.

#### What the footnote does NOT contain

- Full module hierarchies, axiom-audit details, narrowing detail
  tables. Those live in App D.
- More than one or two sentences. The footnote is a pointer + a
  fidelity qualifier; the detail is App D's job.
- Operational vocabulary the body has been kept clean of.

### Layer 3 — Appendix = canonical disclosure venue

App D carries:

1. **The disclosure-mode taxonomy table.** The four-row table mapping
   each Lean coverage mode to its permitted footnote wording. This is
   the rule book the body footnotes obey.
2. **The per-theorem coverage table.** Columns: paper label,
   paper-prose name, Lean declaration, proof mode, coverage,
   alignment. Every body theorem appears here.
3. **Representation notes (where applicable).** For the RH paper:
   the A3 real-coordinate abstraction note; the admissibility-as-Audit_L
   hypothesis note; the recognition-source-carrier (typed bridge)
   subsection. For the DC paper: the AM–GM-as-typed-scalar-hypothesis
   note; the response-space typed-carrier note; the anti-invariant
   readout-as-typed-field note; the Douglas-factorization-typed-cone
   packaging note.
4. **Cross-paper Lean import** (if applicable). The Lean theorem that
   imports a result from another paper's mechanization.
5. **No-smuggling gates** (if applicable). The audit-gate enumeration
   for the conditional theorem.
6. **Code and data availability.** Repo URL, manifest path,
   per-axis source location.

**Do not strip App D's machinery.** This is the canonical venue. The
body footnotes are short specifically because App D is the long form.

## What stays, what moves, what disappears

### Stays in body
- All theorem statements, all proofs (proofs that were sketches → full
  math), all definitions, all numbered remarks, all mathematical
  commentary, all classical-RH-program comparison prose, all
  conceptual motivation, all scope-and-non-claims paragraphs (NC-1
  through NC-N).

### Moves from body to footnote
- The mechanization existence claim per theorem (one footnote per
  theorem).
- The Lean declaration name (referenced once in the footnote, not in
  body prose).
- The fidelity qualifier ("verified", "tracked", "narrowed",
  "encoded as typed structure carrier", etc.) per the wording table.

### Moves from body to appendix
- Narrowing-disclosure prose.
- Parametric-hypothesis disclosure.
- Projection-vs-derivation distinction.
- Lean module hierarchy and namespace layout.
- Axiom-audit trust base.
- Narrowing-detail tables.
- "Lean composes the master theorem with the bridge fields..." mechanism descriptions
  (kept ONLY where they describe genuine mathematical content of the
  proof — but reframed as mathematical statements, not operational
  Lean talk).

### Disappears entirely
- Sentences in body of the form "The Lean realization carries...",
  "the formalization harness tracks...", "the disclosure in App D
  records this narrowing".
- Lean identifier names in body prose (no `\texttt{translationTForward}`,
  no `\nolinkurl{RH.Foo.bar}`, no `same_readout`).

## Honesty over compression

- Don't hide narrowed surrogates behind generic "verified in Lean".
  Disclose at footnote weight, narrowing detail in App D.
- Don't pretend a projection-packaged theorem is a faithful derivation.
- Don't strip the mechanization to make the paper read cleaner. The
  mechanization is part of the work; the fix is *to put it in its
  proper place (footnotes + appendix)*, not to delete it.

## Test for correctness

After each section's rewrite, check:

1. **Body with footnotes hidden.** Does it read as a self-contained
   math paper? If yes, Layer 1 is right.
2. **Footnotes alone.** Do they describe what's mechanized, at what
   fidelity, with the correct wording per coverage type? If yes,
   Layer 2 is right.
3. **Appendix.** Does it give a complete paper-claim → Lean-identifier
   table with proof mode and alignment, plus the canonical
   disclosure-mode taxonomy? If yes, Layer 3 is right.

All three layers passing → companion form.

## Operational discipline

- One subsection per codex dispatch. No batching.
- No sub-agents.
- Sequential dispatch in document order.
- Codex writes files directly into the scaffold; Claude reviews
  every output against this discipline before next dispatch.
- Codex resumes the saved thread via `lean/.codex_thread_id_rh`
  (RH) and `lean/.codex_thread_id_duality_confinement` (DC).
- Rebuild after each dispatch; visually inspect rendered PDF before
  next dispatch.
- Commit at section boundaries.

## Coverage modes per RH theorem (consult this for footnote wording)

Source: original App D Table 1 + statements-of-record.yml.

- `def:rh:fe-involution` — definition_entry, faithful → no footnote
- `def:rh:psi-minus-rh` — definition_entry, faithful → no footnote
- `def:rh:nontrivial-zero-ledger` — definition_entry with A3 real-part
  representation note → footnote: "Realized in Lean as
  `RH.ZeroLedger.NontrivialZeroLedger`; the typed real-coordinate
  representation is recorded in App~\ref{app:formalization} (A3)."
- `def:rh:anti-invariant-zero-ledger` — definition_entry, faithful →
  no footnote (or brief)
- `def:rh:sat-sel-shell` — definition_entry with admissibility-as-Audit_L
  note → footnote: "Realized in Lean as `RH.SatSelShell.SatSelShell`;
  admissibility under the seven Foundations-II schemas is carried by
  the `Audit_L` field, recorded in App~\ref{app:formalization}."
- `thm:rh:translation-T-forward` — lean substantive, typed-interface
  composition over `AntiInvariantZeroLedger` fields, faithful →
  footnote: "Verified in Lean as `RH.TranslationT.translationTForward`
  via typed-interface composition over the `AntiInvariantZeroLedger`
  fields; see App~\ref{app:formalization}."
- `thm:rh:translation-T-reverse` — same coverage mode, declaration
  `RH.TranslationT.translationTReverse`.
- `thm:rh:translation-T` — same coverage mode, declaration
  `RH.TranslationT.translationT`.
- `obl:rh:gamma-sdtc-selberg` — typed_carrier → footnote: "Encoded
  in Lean as a typed structure carrier `RH.RHConditional.GammaSdtcSelberg`,
  not as a Lean axiom; downstream theorems take a value of this
  carrier as an explicit hypothesis. See App~\ref{app:formalization}."
- `thm:rh:dc-master-applied` — lean substantive, typed-bridge
  composition, faithful → footnote: "Verified in Lean as
  `RH.DCMasterApplied.dcMasterApplied` via typed-bridge composition
  over the recognition-source carrier; see App~\ref{app:formalization}."
- `thm:rh:conditional` — lean substantive, typed-bridge composition
  taking γ explicitly → footnote: "Verified in Lean as
  `RH.RHConditional.rhConditional`, taking a value of
  `GammaSdtcSelberg shell` as an explicit hypothesis; see
  App~\ref{app:formalization}."
- `def:rh:aor-sel-instance` — definition_entry with literal-classification
  framing → footnote: "Realized in Lean as `RH.AORInstance.SelAORInstance`
  with the canonical assembled value `RH.AORInstance.assembledCarrier`;
  see App~\ref{app:formalization}."
- `thm:rh:aor-mechanical-records` — projection_over_record / literal-data
  definition → footnote: "Tracked in the formalization harness as
  `RH.AORInstance.aorMechanicalRecords`, a literal-data definition
  returning the mechanical-stratum discharge list; see
  App~\ref{app:formalization}."
- `thm:rh:aor-recognition-discharge` — projection_over_record → footnote:
  "Tracked in the formalization harness as `RH.AORInstance.aorRecognitionDischarge`,
  a literal-data definition with status `approved_other` deferred to
  \cite{TsiokosSDTC2026}; see App~\ref{app:formalization}."
- `thm:rh:aor-gamma-bridge-discharge` — projection_over_record →
  footnote: "Tracked in the formalization harness as
  `RH.AORInstance.aorGammaBridgeDischarge`, a literal-data definition
  with status `bridged` on the carrier bridge propositions; see
  App~\ref{app:formalization}."
- `thm:rh:aor-auditL-discharge` — projection_over_record → footnote:
  "Tracked in the formalization harness as `RH.AORInstance.aorAuditLDischarge`,
  a literal-data definition with status `by_construction` on the
  audit field of $\Sel$; see App~\ref{app:formalization}."
- `thm:rh:aor-dc-master-import-discharge` — projection_over_record →
  footnote: "Tracked in the formalization harness as
  `RH.AORInstance.aorDCMasterImportDischarge`, a literal-data
  definition with status `approved_other` deferred to
  \cite{TsiokosSDTC2026}; see App~\ref{app:formalization}."
- `thm:rh:aor-real-coordinate-discharge` — projection_over_record →
  footnote: "Tracked in the formalization harness as
  `RH.AORInstance.aorRealCoordinateDischarge`, a literal-data
  definition with status `by_construction`; the A3 representation note
  applies. See App~\ref{app:formalization}."
- `thm:rh:aor-translation-interface-discharge` — projection_over_record
  → footnote: "Tracked in the formalization harness as
  `RH.AORInstance.aorTranslationInterfaceDischarge`, a literal-data
  definition with status `by_construction`; substantive content lives
  in \Cref{sec:translation_theorem}. See App~\ref{app:formalization}."
- `thm:rh:aor-instance` — lean substantive (case-on-secondary-type
  dispatch over local refinement-stable predicate); partial alignment
  (the Lean conclusion is the local syntactic refinement-stable
  membership predicate over the carrier fields rather than the full
  audit-closure refinement-stable characterisation) → footnote:
  "Verified in Lean as `RH.AORInstance.aorInstance` against the local
  `RH.AORPrimitives.RefStableAOR` predicate over the assembled-carrier
  fields; the partial alignment relative to the full audit-closure
  refinement-stable characterisation of \citet{TsiokosAOR2026} is
  recorded in App~\ref{app:formalization}."
- `rem:rh:aor-partial-status` — remark; no footnote (it IS the
  partial-status disclosure; just preserved as-is, or trimmed to the
  appendix-pointer form).

## Coverage modes per DC theorem (consult when working on DC paper)

See original App D in `paper/duality_confinement/appendices/app_d_formalization.tex`
Table 1 + coverage table. Key items:

- `thm:master-theorem` — lean substantive, pure derivation, faithful
  → footnote: "Verified in Lean as
  `DualityConfinement.MasterTheorem.masterTheorem`; see
  App~\ref{app:formalization}."
- `lem:trace-identity` — lean substantive, typed-interface composition
  over `AntiInvariantLedger` field, faithful → footnote similar.
- `thm:separation-confinement` — lean substantive, typed-bridge
  composition with measure-reading bridges (`mu_zero_of_ae`,
  `visible_zero_of_ae`), faithful → footnote.
- `thm:quantitative-confinement` — lean substantive, typed-bridge
  composition with Markov interface, faithful → footnote.
- `thm:douglas-domination` — lean substantive, typed-carrier
  packaging via `DouglasData`, faithful → footnote.
- `thm:exhaustive-squeeze` — lean substantive, ambient bound
  supplied as moving-ledger field, faithful → footnote.
- `prop:optimized-trace-budget` — harness_tracked; the AM–GM step
  is supplied as a typed-scalar hypothesis → footnote: "Tracked in
  the formalization harness as
  `DefectedBudget.optimizedTraceBudget`; the AM–GM step is supplied
  as a typed-scalar hypothesis (§A2). See App~\ref{app:formalization}."
- `def:defected-budget` — support_only, no Lean citation → no footnote.
