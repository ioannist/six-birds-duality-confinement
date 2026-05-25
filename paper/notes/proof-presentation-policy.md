# Proof Presentation Policy

Status: Phase I.A.1 produced 2026-05-23 (paper-writing pre-drafting workspace).

Purpose: specifies how each theorem-like statement appears in either
paper: full proof in body, sketch in body with full proof in
appendix, appendix-only treatment, Lean-substantive citation,
projection-disclosure citation, definition entry, or
standard-reference citation. It also gives the Lean-disclosure
wording table that `paper/<axis>/appendices/app_d_formalization.tex`
mirrors during Phase I.D.

This file is the binding wording source for any drafting dispatch
that mentions Lean. The Lean-disclosure discipline is from
`~/.claude/projects/-home-repos-six-birds-duality-confinement/memory/feedback_lean_traceability_disclosure.md`.

## Proof-presentation modes

| Mode | Body content | Appendix content | Lean disclosure |
| --- | --- | --- | --- |
| `body_full` | Full proof in body prose. Use when the proof is short, central, and reader-helpful. | None required unless the proof becomes long. | Optional; if Lean covers the row, cite only with allowed wording. |
| `body_sketch` | A 1–3 paragraph sketch in body covering the key idea, the hypotheses used, and the structure of the argument. | Full proof (if needed) goes in `app:formalization` or a dedicated proof appendix. | Inline Lean disclosure only where it helps the reader; use wording from the disclosure table. |
| `appendix_only` | Statement-only mention in body, or no body mention if the item is purely appendix support. | Full statement / explanation / proof in appendix. | Use the Lean-disclosure table if the row has any Lean coverage. |
| `lean_substantive` | Statement appears in body; the proof may be described as Lean-verified when the paper statement matches the Lean statement. Short mathematical explanation may still accompany for readability. | None required for proof coverage; the formalization appendix lists the row. | Use "Lean proves the statement" only when `lean_coverage = theorem`, `semantic_alignment = faithful`, AND the Lean theorem derives the statement from primitives within its declared scope (no typed-interface bridges or typed-carrier packaging). For rows where the Lean theorem composes the statement over typed hypotheses or unpacks it from a typed carrier, prefer "Lean checks/composes/records the statement [as a typed-interface composition / via the typed `<Carrier>` fields / over the bridge hypothesis `<name>`]." For narrowed rows, disclose the narrowing. |
| `lean_traceability_only` | Statement or scope note may appear in body; proof-side prose is written by the writer. Lean is not cited as the proof. | Appendix records traceability schema, carrier fields, or proof-carrying record fields. | Use "tracked by the formalization harness," "encoded as a structural recognition-source carrier," or "checked as a conditional schema over explicit hypotheses." |
| `standard_reference` | Statement appears in body with proof attributed to a standard mathematical result (e.g. Douglas factorization in operator theory; classical functional-equation symmetry in analytic number theory). | None required unless adaptation is needed. | None, unless a separate Lean row also exists. |
| `definition_entry` | Definition appears in body or appendix. No proof presented because the row is definitional. | None required; formalization appendix may map the paper definition to its Lean declaration. | Use "realized in Lean as `<Module.Name>`" if `semantic_alignment = faithful`; for narrowed rows, say "realized in Lean with [parameter] exposed as a free argument" or "narrowed to [specific carrier]." Never say "Lean proves" for a definition. |

## Lean-disclosure wording discipline

| Lean coverage | Semantic alignment | Permitted wording | Forbidden wording | Notes |
| --- | --- | --- | --- | --- |
| `theorem` | `faithful` | When the Lean theorem derives the statement from primitives within its declared scope: "Lean proves …"; "a Lean derivation establishes …"; "verified in Lean"; "checked in Lean." When the Lean theorem composes the statement over typed-interface hypotheses or repackages it from a typed carrier: "Lean checks/composes the statement [via the typed `<Carrier>` fields / over the bridge hypothesis `<name>` / as a typed-interface composition]." | "Lean proves …" when the Lean theorem only composes the statement over a typed interface or unpacks a typed carrier and the carrier/bridge is load-bearing for the conclusion. | This is the strongest substantive citation when applicable. The interface-composition variant is the audited form for rows whose Lean realization is a typed-interface composition; see per-row notes below. Applies to the 12 theorem rows currently in SoR with `faithful` alignment. |
| `theorem` | `narrowed_surrogate` | "Lean proves the [specific clause]; the [other clause / general statement] is recorded as a paper-side claim with the narrowing disclosed in the formalization appendix." | "Lean proves the full statement." | Not currently used. If a row's encoding choice narrows the statement (e.g., the typed-cone abstraction narrows the operator-theoretic master theorem), the body must say "Lean proves the abstract typed-positive-cone version; the operator-theoretic generalization is an open extension." |
| `partial` | any | "Lean proves [specific fragment] under [specific elevated hypotheses]; the remaining content is established here." | "Lean proves" without qualification; "verified in Lean" without qualification. | Not currently used in this project. |
| `definition` | `faithful` | "realized in Lean as `<Module.Name>`." | "Lean proves" (definitions are not proved). | The default for all 10 definition rows in the project. |
| `definition` | `narrowed_surrogate` | "realized in Lean with the [parameter] exposed as a free argument" or "realized in Lean with the [structural component] exposed via [auxiliary record]." | "Lean defines exactly the math statement" if the realization is narrowed. | Not currently used. Anticipated cases: if any future encoding exposes a typed parameter that the paper definition does not name. |
| `recognition_source` | `not_applicable` | "encoded as a structural recognition-source carrier"; "the recognition source is supplied by Paper 1 and tracked in `SixBirdsDualityConfinement.RH.RHConditional` as a typed structure `GammaSdtcSelberg`" | "Lean axiom"; "the axiom of …"; "Lean proves the recognition source." | Applies only to `obl:rh:gamma-sdtc-selberg`. Honesty discipline: the project's forbidden-tokens rule bans Lean `axiom`/`opaque`/`constant`; the typed-structure-carrier encoding is the lawful realization. The carrier is declared inline in `RHConditional.lean` (sanctioned by kickoff §12 — type lives next to its only consumer). |
| `not_mechanized` | `not_applicable` | No Lean mention. Body uses the wording from `paper/notes/scope-fence.md` for support-only / out-of-scope rows. | "Lean proves"; "verified in Lean"; "mechanized in Lean"; any Lean citation. | Applies to `def:duality_confinement:defected-budget` (support_only — context for `prop:duality_confinement:optimized-trace-budget` but not itself mechanized in the manifest). |

## Per-row Lean-coverage mapping (current, post Phase H.4 sync)

Consult `paper/notes/statements-of-record.yml` for the canonical
record. Summary:

### Duality Confinement axis (13 rows)

| Paper label | env_kind | lean_coverage | semantic_alignment | proof_presentation | Permitted Lean wording |
| --- | --- | --- | --- | --- | --- |
| `def:duality_confinement:involutive-object-ledger` | definition | `definition` | `faithful` | `definition_entry` | "realized in Lean as `SixBirdsDualityConfinement.DualityConfinement.Involution.InvolutiveObjectLedger`" |
| `def:duality_confinement:separating-readout` | definition | `definition` | `faithful` | `definition_entry` | "realized in Lean as `SixBirdsDualityConfinement.DualityConfinement.Separation.SeparatingReadout`" |
| `def:duality_confinement:anti-invariant-ledger` | definition | `definition` | `faithful` | `definition_entry` | "realized in Lean as `SixBirdsDualityConfinement.DualityConfinement.AntiInvariantLedger.AntiInvariantLedger`" |
| `lem:duality_confinement:trace-identity` | lemma | `theorem` | `faithful` | `lean_substantive` (typed-interface composition) | "Lean records the trace identity as `traceIdentity`; the equality is a constructor unfolding from the `AntiInvariantLedger` typed-cone field `trace_identity`, not an analytic derivation." |
| `thm:duality_confinement:separation-confinement` | theorem | `theorem` | `faithful` | `lean_substantive` (typed-interface composition) | "Lean checks the separation–confinement theorem as `separationConfinement`, composing the trace identity and separation with the measure-reading bridges `mu_zero_of_ae` and `visible_zero_of_ae` supplied as typed hypotheses." |
| `thm:duality_confinement:quantitative-confinement` | theorem | `theorem` | `faithful` | `lean_substantive` (typed-interface composition) | "Lean checks the quantitative-confinement bound as `quantitativeConfinement`, composing the trace identity with the Markov-style scalar step supplied as the typed `markov_bound` hypothesis." |
| `def:duality_confinement:completed-domination-bridge` | definition | `definition` | `faithful` | `definition_entry` | "realized in Lean as `SixBirdsDualityConfinement.DualityConfinement.Domination.CompletedDominationBridge`" |
| `thm:duality_confinement:douglas-domination` | theorem | `theorem` | `faithful` | `lean_substantive` (typed-interface composition) | "Lean packages the Douglas equivalence at the typed-cone level as `douglasDomination`, repackaging the two directions stored as `order_to_factor` and `factor_to_order` fields of the typed `DouglasData` carrier (per the typed-cone encoding choice; see audit_summary §A1). Not a Lean derivation of the equivalence from operator-square-root primitives." |
| `thm:duality_confinement:master-theorem` | theorem | `theorem` | `faithful` | `lean_substantive` | "Lean proves the duality-confinement master theorem as `masterTheorem`" |
| `def:duality_confinement:exhaustive-moving-ledger` | definition | `definition` | `faithful` | `definition_entry` | "realized in Lean as `SixBirdsDualityConfinement.DualityConfinement.ExhaustiveSqueeze.ExhaustiveMovingLedger`" |
| `thm:duality_confinement:exhaustive-squeeze` | theorem | `theorem` | `faithful` | `lean_substantive` (typed-interface composition) | "Lean checks the exhaustive squeeze as `exhaustiveSqueeze`, consuming the ambient bound supplied as the moving-ledger's `exhaustive_bound` field (not derived from monotonicity-of-transport primitives) and composing it with the supplied trace squeeze." |
| `def:duality_confinement:defected-budget` | definition | `not_mechanized` | `not_applicable` | `definition_entry` | **No Lean mention.** Paper introduces the defected-budget shape as motivation for the optimized scalar trace budget; no formalization claim. |
| `prop:duality_confinement:optimized-trace-budget` | proposition | `theorem` | `faithful` | `lean_substantive` | "the optimized scalar trace budget is **tracked by the formalization harness** as `optimizedTraceBudget`; the AM-GM step is taken as a typed-Scalar axiom in the abstract setting (see audit_summary §A2). A substantive derivation requires introducing typed real-arithmetic structure." |

### RH axis (11 rows)

| Paper label | env_kind | lean_coverage | semantic_alignment | proof_presentation | Permitted Lean wording |
| --- | --- | --- | --- | --- | --- |
| `def:rh:fe-involution` | definition | `definition` | `faithful` | `definition_entry` | "realized in Lean as `SixBirdsDualityConfinement.RH.Involution.feInvolution`" |
| `def:rh:psi-minus-rh` | definition | `definition` | `faithful` | `definition_entry` | "realized in Lean as `SixBirdsDualityConfinement.RH.Involution.psiMinusRh`" |
| `def:rh:nontrivial-zero-ledger` | definition | `definition` | `faithful` | `definition_entry` | "realized in Lean as `SixBirdsDualityConfinement.RH.ZeroLedger.NontrivialZeroLedger`" |
| `def:rh:anti-invariant-zero-ledger` | definition | `definition` | `faithful` | `definition_entry` | "realized in Lean as `SixBirdsDualityConfinement.RH.AntiInvariantZeroLedger.AntiInvariantZeroLedger`" |
| `def:rh:sat-sel-shell` | definition | `definition` | `faithful` | `definition_entry` | "realized in Lean as `SixBirdsDualityConfinement.RH.SatSelShell.SatSelShell`" |
| `thm:rh:translation-T-forward` | theorem | `theorem` | `faithful` | `lean_substantive` (typed-interface composition) | "Lean checks the forward direction of Theorem T as `translationTForward`, composing the implication stored as the `zero_sum_to_zero_term` and `zero_term_to_critical_line` fields of `AntiInvariantZeroLedger` rather than deriving it from typed scalar arithmetic." |
| `thm:rh:translation-T-reverse` | theorem | `theorem` | `faithful` | `lean_substantive` (typed-interface composition) | "Lean checks the reverse direction of Theorem T as `translationTReverse`, composing the implication stored as fields of `AntiInvariantZeroLedger`." |
| `thm:rh:translation-T` | theorem | `theorem` | `faithful` | `lean_substantive` (typed-interface composition) | "Lean checks Theorem T as `translationT` by combining the forward and reverse typed-interface compositions above." |
| `obl:rh:gamma-sdtc-selberg` | obligation | `recognition_source` | `not_applicable` | `appendix_only` | "the recognition source `Γ_{SDTC-Selberg}` is supplied by Paper 1's SDTC structural law applied to the Selberg-class instance; encoded in Lean as a typed structure carrier `GammaSdtcSelberg` declared inline in `SixBirdsDualityConfinement.RH.RHConditional`. The forbidden-tokens rule bans `axiom`/`opaque`/`constant`; the carrier encoding is the lawful realization." |
| `thm:rh:dc-master-applied` | theorem | `theorem` | `faithful` | `lean_substantive` (typed-bridge composition) | "Lean checks the RH-specific application of the master theorem as `dcMasterApplied`, composing Paper 1's `masterTheorem` with the bridge fields `same_readout`, `visible_zero_of_ae`, and `mu_zero_of_ae` carried by the `GammaSdtcSelberg` record. Not a direct instantiation of the abstract DC ledger on the shell." |
| `thm:rh:conditional` | theorem | `theorem` | `faithful` | `lean_substantive` (typed-bridge composition) | "Lean composes the conditional landing chain `Γ_{SDTC-Selberg} ⟹ RH` as `rhConditional`, taking the recognition source as an explicit hypothesis parameter `γ : GammaSdtcSelberg shell` and applying `dcMasterApplied` through its bridge fields followed by `translationTForward`." |

## Decision rules for difficult cases

- When `lean_coverage = theorem` AND `semantic_alignment = faithful`
  AND the paper destination is `body`, the default is a body
  statement with either a full body proof (mode `body_full`) or a
  short explanatory sketch plus the faithful "verified in Lean"
  citation (mode `lean_substantive`).
- When `lean_coverage = theorem` AND the encoding strategy
  introduces a narrowing (e.g., Douglas factorization at the
  typed-cone level vs full operator-theoretic), the body must say
  what the typed-encoding scope is. The current case is
  `thm:duality_confinement:douglas-domination`: cite as "Lean
  derives Douglas factorization at the typed-cone level"; do not
  say "Lean proves Douglas factorization in full operator
  generality."
- When `lean_coverage = not_mechanized` AND the paper destination is
  `body` or `appendix`, no Lean citation is allowed; the writer
  supplies the role of the definition in body prose. Currently
  applies to `def:duality_confinement:defected-budget`.
- When a row is `lean_coverage = recognition_source`, body prose must
  use the recognition-source / typed-structure-carrier wording from
  the disclosure table; **never** the substantive-Lean wording.
  Currently applies to `obl:rh:gamma-sdtc-selberg`.
- When a row's `target_destination = appendix`, body prose may name
  the result (with `\Cref{app:…}`) but full statement / proof lives
  in the appendix. Body should give a one-paragraph motivation.
  Currently applies to `obl:rh:gamma-sdtc-selberg` (proof_presentation
  = `appendix_only`).
- **Typed-interface composition cases**. When the Lean realization
  composes the statement over typed-interface hypotheses or
  repackages it from a typed carrier, body prose must use the
  "Lean checks/composes/records [via …]" wording instead of "Lean
  proves …", and the qualifier `(typed-interface composition)` (or
  `(typed-bridge composition)` when bridge propositions are the
  load-bearing fields) must accompany the `lean_substantive` mode
  in the per-row mapping above. The App D coverage row must also
  flag the typed-interface/bridge composition in its Proof mode
  cell. Currently applies to: `lem:trace-identity` (constructor
  field), `thm:separation-confinement` (`mu_zero_of_ae`,
  `visible_zero_of_ae`), `thm:quantitative-confinement`
  (`markov_bound`), `thm:douglas-domination` (`DouglasData`
  fields), `thm:exhaustive-squeeze` (`exhaustive_bound` field),
  `thm:rh:translation-T-{forward,reverse}` and `thm:rh:translation-T`
  (`AntiInvariantZeroLedger` fields), `thm:rh:dc-master-applied`
  and `thm:rh:conditional` (`GammaSdtcSelberg` bridge fields).

## Project-specific representation notes (carry into body prose)

These notes from `anti_loc/extracted_math/audit_summary.md` must be
disclosed in the relevant body subsection or in App D, not silently
hidden behind generic "verified in Lean" prose:

- **§A1 (Douglas factorization encoding)**: the typed-cone encoding
  bundles the equivalence into the `DouglasData` carrier; downstream
  theorems read the equivalence off the carrier. Body prose around
  `thm:duality_confinement:douglas-domination` must note that this is
  the typed-cone formulation, not the full operator-theoretic Douglas
  theorem.
- **§A2 (AM-GM as typed-Scalar axiom)**: `optimizedTraceBudget` takes
  the AM-GM inequality as a hypothesis rather than deriving it from
  `(x - y)² ≥ 0`. Body prose around
  `prop:duality_confinement:optimized-trace-budget` must use
  "tracked by the formalization harness" wording and disclose the
  abstract-Scalar limitation. App D must explicitly document the
  limitation.
- **§A3 (real-part type for the RH zero ledger)**: the real-part
  coordinate is parameterized by a typed ordered-field carrier with
  `half`, `oneMinus`, `sub`, and `(x - 1/2)² = 0 ⟹ x = 1/2` axioms.
  Body prose around `def:rh:nontrivial-zero-ledger` and
  `thm:rh:translation-T` must note that the Lean statement
  abstracts the real-part type; the identification with actual ℝ-valued
  real parts of nontrivial zeros of `ζ` is by construction-parameter
  assignment.

## Substance bar review pattern

For each body-side Lean citation, the reviewer asks (in this order):

1. **Is the wording within the row's allowed cell?** Check
   `lean_coverage × semantic_alignment` against the disclosure table.
2. **Is the narrowing / encoding-scope disclosed when present?** For
   the three project-specific representation notes above, the body
   must say what is encoded vs what is open.
3. **Is the prose audience-accessible?** A reader without Six Birds
   background should be able to follow the proof or sketch (per
   `paper/notes/audience-translation.md`).
4. **Are framework-native terms used only after translation?** Per
   `paper/notes/audience-translation.md`.
5. **Are reserved symbols not repurposed?** Per
   `paper/notation_and_terminology.md`.
6. **Are nonclaims preserved per the scope fence?** Per
   `paper/notes/scope-fence.md`.

A drafting turn that violates any of these gates is rejected; the
fix prompt to codex names the violating row and the disclosure
table cell.
