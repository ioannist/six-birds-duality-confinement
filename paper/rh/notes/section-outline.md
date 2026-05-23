# Section Outline: RH closure (Paper 2)

Status: Phase 3 produced 2026-05-23.

Authoritative outline sources: this file,
`paper/rh/notes/contract.md`,
`paper/notes/statements-of-record.yml`,
`paper/notes/cross-paper-boundary.md`.

Section roster: 10 body sections + 1 appendix (formalization).

## Narrative spine

The paper opens with the structural question: what would it take to
settle RH? Section 2 places the question in the Six Birds
framework: layer-shifted reading of RH; the saturated Selberg trace
closure as the operative formed-layer object; the dependency on
Paper 1's master theorem and SDTC structural law. Sections 3–7
build the construction: the functional-equation involution and
zero ledger; the anti-invariant zero ledger; the saturated trace
shell; the translation theorem T (the construction-grade headline);
the recognition source `Γ_{SDTC-Selberg}` and the conditional
landing chain (the headline result). Section 8 establishes the
scope fence (NC-1 through NC-12; Six Gates + Gate 7; three-option
derivation sweep). Section 9 discusses the structural parallel
with NS regularity and PvNP closure, the classical-barrier
framing, and the GRH extension as future work. Section 10
concludes.

## 1. Introduction

- File: `paper/rh/sections/sec_01_intro.tex`
- Section label: `sec:intro`
- Target length: 2–3 pages
- Purpose: opens from "what would it take to settle whether all
  nontrivial zeros of `ζ` lie on the critical line?" Frames the
  answer in plain mathematical terms first: rather than attacking
  RH within classical analytic number theory's vocabulary, recast
  RH as a question about the formed closure of the completed
  Selberg trace ledger. States the conditional structure
  explicitly (under the standard Six Birds closure assumption and
  `Γ_{SDTC-Selberg}` from Paper 1, RH follows). States scope
  fence (conditional theorem; not unconditional RH; not
  circumvention of classical barriers; not GRH).
- Primary sources: contract thesis paragraph; math artifact
  preamble. Inventory rows: forward references only.
- Definitions introduced in plain prose (per
  `paper/notes/audience-translation.md`): formed closure;
  saturated Selberg trace closure; functional-equation involution;
  anti-invariant zero ledger; recognition source; conditional
  theorem; BirdInt judgment (cited from Foundations III when
  invoked). Formal definitions appear later.
- Key claims: nonclaim rows from `sec:scope_and_nonclaims` (no
  unconditional RH; no derivation of `Γ_{SDTC-Selberg}`; no
  classical-barrier circumvention; no GRH; no
  simple-zero / density results).
- Dependencies: none.

## 2. Framework

- File: `paper/rh/sections/sec_02_framework.tex`
- Section label: `sec:framework`
- Target length: 2–3 pages
- Purpose: place the paper in the Six Birds framework context.
  Brief recap of: closure formation per Foundations I; the
  closure-content-as-structural-fact commitment; the
  V-Differential trace-state-only column condition (citing Paper
  1 [1] `sec:framework`); the structural-law sibling papers
  (no-needles for NS; CSL-SAT-hiddenness for PvNP; SDTC for RH).
  Note the cross-paper dependency: this paper imports Paper 1's
  master theorem and SDTC framing; the dependency is one-way.
  Cite Paper 1 [1] as the sibling structural-law paper.
- Primary sources: contract; cross-paper-boundary;
  Paper 2 proposal §1 motivation, §11.4 cross-track context.
  No inventory rows (background only).
- Definitions introduced: formed closure (plain prose);
  V-Differential trace-state-only column (plain prose, citing
  Paper 1 §framework); structural-law sibling papers (named).
- Key claims: positioning only.
- Dependencies: `sec:intro`.

## 3. Involution and ledger

- File: `paper/rh/sections/sec_03_involution_and_ledger.tex`
- Section label: `sec:involution_and_ledger`
- Target length: 3–4 pages
- Purpose: define the central typed objects for the RH side:
  the functional-equation involution `J_L(s) = 1 - \bar{s}` with
  critical-line fixed locus and proof of involutivity; the
  separating anti-invariant readout `\psi_-(s) = Re(s) - 1/2`
  with proof of anti-invariance; the nontrivial-zero ledger
  `Z_ζ^{nt}` as a typed multiset with `m_ρ > 0` multiplicities;
  the anti-invariant zero ledger
  `A_Z(\zeta) = Σ_ρ m_ρ |Re(ρ) - 1/2|^2`. Disclose the real-part-type
  abstraction (audit_summary §A3): the Lean encoding parameterizes
  the real-part coordinate by a typed `RealCoordinate`; the
  identification with actual ℝ-valued real parts of nontrivial
  zeros of `ζ` is by construction-parameter assignment.
- Primary sources: math artifact §Involution, §ZeroLedger,
  §AntiInvariantZeroLedger. Inventory rows:
  `def:rh:fe-involution`, `def:rh:psi-minus-rh`,
  `def:rh:nontrivial-zero-ledger`,
  `def:rh:anti-invariant-zero-ledger`.
- Key claims: definitions plus the involution properties
  (involutivity, fixed-locus characterization, anti-invariance).
  Lean-substantive citations for the involution-property facts
  (faithful alignment).
- Dependencies: `sec:framework`.

## 4. The saturated Selberg trace closure

- File: `paper/rh/sections/sec_04_sat_sel_shell.tex`
- Section label: `sec:sat_sel_shell`
- Target length: 2–3 pages
- Purpose: introduce the typed shell `Sel^!_{ζ,tr}` as the
  formed-layer object. Body prose names the 13 fields (history
  carrier, trace instrument, observable family, predictive verifier
  events, quotient carriers, comparison map, involution, completed
  L, zero ledger, anti-invariant ledger, visibility map, audit
  provenance). Disclose: admissibility per the seven Foundations II
  schemas (cited from Paper 1's foundations [Foundations II
  reference]) is encoded as a Foundations-II-level hypothesis (the
  opaque `Audit_L` field); not derived in this paper.
- Primary sources: math artifact §SatSelShell. Inventory row:
  `def:rh:sat-sel-shell`.
- Key claims: shell definition (definition-entry).
- Dependencies: `sec:framework`, `sec:involution_and_ledger`.

## 5. Translation theorem T

- File: `paper/rh/sections/sec_05_translation_theorem.tex`
- Section label: `sec:translation_theorem`
- Target length: 2–3 pages
- Purpose: state and prove translation theorem T:
  `A_Z(ζ) = 0 ⟺ RH` (on the typed zero ledger of `Sel^!_{ζ,tr}`).
  Both directions are short and reader-helpful:
  forward (`A_Z(ζ) = 0 ⟹ ∀ρ, Re(ρ) = 1/2`) follows from positive
  sum + positive multiplicities; reverse follows by substitution.
  This is the construction-grade headline of Paper 2. Lean
  citations for forward, reverse, and combined biconditional
  (lean_substantive, faithful).
- Primary sources: math artifact §TranslationT. Inventory rows:
  `thm:rh:translation-T-forward`, `thm:rh:translation-T-reverse`,
  `thm:rh:translation-T`.
- Key claims: Theorem T (and its forward / reverse halves).
- Dependencies: `sec:involution_and_ledger`, `sec:sat_sel_shell`.

## 6. The recognition source

- File: `paper/rh/sections/sec_06_recognition_source.tex`
- Section label: `sec:recognition_source`
- Target length: 2–3 pages
- Purpose: introduce `Γ_{SDTC-Selberg}` as the structural
  recognition source supplied by Paper 1 [1] (the SDTC structural
  law applied to the Selberg-class instance). Body prose: the
  recognition source asserts that on `Sel^!_{ζ,tr}`, a sequence of
  completed domination records `A_Z(ζ) ⪯ B_n` with `tr B_n → 0`
  exists as content of formed-layer closure per Foundations I.
  Disclose: NOT a Lean axiom; encoded as typed structure carrier
  `GammaSdtcSelberg` declared inline in `RHConditional.lean` (per
  `lean/codex_kickoff.md` §12); the forbidden-tokens rule bans
  `axiom`/`opaque`/`constant`. Cite Paper 1's three-option
  derivation sweep result (cascade steps 451–453, summarized in
  Paper 1's `sec:scope`) that confirms framework primitives do NOT
  derive the source.
- Primary sources: math artifact §RecognitionSource. Inventory
  row: `obl:rh:gamma-sdtc-selberg`. Cross-paper boundary:
  imports Paper 1's SDTC framing.
- Key claims: the recognition source statement (paper-prose); the
  Lean-side typed-structure-carrier encoding (lean_traceability_only
  wording per `paper/notes/proof-presentation-policy.md`); the
  scope-fence claim that the source is not framework-derivable.
- Dependencies: `sec:framework`, `sec:sat_sel_shell`,
  `sec:translation_theorem`.

## 7. The conditional landing chain

- File: `paper/rh/sections/sec_07_landing_chain.tex`
- Section label: `sec:landing_chain`
- Target length: 2–3 pages
- Purpose: state and prove the **headline** conditional theorem.
  Three-step chain: (i) from `Γ_{SDTC-Selberg}`, extract the
  domination-records witness (`A_Z(ζ) ⪯ B_n` with `tr B_n → 0`);
  (ii) apply the duality-confinement master theorem from Paper 1
  [1] (reproduce the master theorem statement verbatim) to derive
  `A_Z(ζ) = 0`; (iii) apply translation theorem T (forward) to
  derive `∀ρ ∈ Z_ζ^{nt}, Re(ρ) = 1/2`. Cite the Lean realization
  `rhConditional` (lean_substantive, faithful). Outside-Six-Birds
  reading: the conditional theorem `Γ_{SDTC-Selberg} ⟹ RH`. The
  BirdInt-judgment form (from Paper 2 proposal §2) renders the
  result in framework vocabulary; introduce BirdInt judgment via
  audience-translation on first use.
- Primary sources: math artifact §DCMasterApplied + §RHConditional.
  Inventory rows: `thm:rh:dc-master-applied`, `thm:rh:conditional`.
- Key claims: the conditional theorem (the **HEADLINE**); the
  intermediate `dcMasterApplied` bridge; the outside-Six-Birds
  conditional reading.
- Dependencies: `sec:translation_theorem`, `sec:recognition_source`.

## 8. Scope and non-claims

- File: `paper/rh/sections/sec_08_scope_and_nonclaims.tex`
- Section label: `sec:scope_and_nonclaims`
- Target length: 2–3 pages
- Purpose: explicitly state the paper's nonclaims with required
  wording (per `paper/notes/scope-fence.md`):
  - NC-1 through NC-12 from the proposal §9, restated for the
    Lean-coverage state post Phase H.4 sync.
  - The conditional structure: not unconditional RH; outside-Six-
    Birds reading is the conditional theorem.
  - The recognition-source provenance: supplied by Paper 1 [1],
    not derived from framework primitives; not a Lean axiom.
  - The parameter-identification disclosure: `shell.Z_nt` is a
    typed multiset parameter; identification with actual `ζ` zeros
    is construction-parameter assignment.
  - Classical-barrier framing: partial-spirit-aligned with but
    structurally-distinct-from Hilbert–Pólya, Connes, de Branges,
    Weil-positivity etc.
  - GRH scope-out: paper instantiates for `L = ζ` only.
  - Simple-zero / density-of-zeros scope-out: paper does not
    claim multiplicity-1 or zero-density results.
  - Admissibility-as-hypothesis: `Sel^!_{ζ,tr}` admissibility is
    construction-time hypothesis, not derived in this paper.
  - The three-option derivation sweep (cascade steps 451–453):
    documented as cascade-side due diligence that the recognition
    source is closure-content, not separately derivable.
  - The six no-smuggling gates + Gate 7: cited as the
    metamathematical audit checklist that the conditional closure
    passes (detail in App D).
- Primary sources: contract honesty caveats; scope-fence canonical
  nonclaims; proposal §9 NC-1..NC-12; proposal §10 three-option
  sweep; proposal §B Six Gates + Gate 7. No inventory rows beyond
  cross-references.
- Key claims: nonclaim discipline only.
- Dependencies: `sec:landing_chain`.

## 9. Discussion

- File: `paper/rh/sections/sec_09_discussion.tex`
- Section label: `sec:discussion`
- Target length: 2–3 pages
- Purpose: structural parallel with NS regularity and PvNP closure
  per proposal §8 (the table showing how all three Six Birds
  layer-level theorems use closure formation per Foundations I
  identically); positioning against classical RH attack barriers
  (the audit-currency derivability tension at cascade steps
  441–447 documents why Weil positivity is readout-level and
  structurally distinct from source-level); GRH extension as
  future work (instantiate SDTC for general Selberg-class `L`);
  Lean mechanization extensions as future work (Sel^!_{ζ,tr}
  admissibility derivation; parameter-identification work
  connecting `shell.Z_nt` to actual `ζ` zeros).
- Primary sources: proposal §8 (NS/PvNP/RH structural parallel),
  §13 (honest caveats), §15.3 (structural-template peers), §15.5
  (cross-track context).
- Key claims: no new theorems.
- Dependencies: all preceding body sections; cross-references to
  Paper 1 [1] for the master theorem and SDTC framing; cross-
  references to NS, PvNP papers for the structural parallel (if
  citation lookups available; otherwise paper-prose mention with
  deferred external-reference pipeline).

## 10. Conclusion

- File: `paper/rh/sections/sec_10_conclusion.tex`
- Section label: `sec:conclusion`
- Target length: 1 page
- Purpose: restate the conditional theorem; list pending work
  (Sel^!_{ζ,tr} admissibility derivation; parameter-identification;
  GRH for primitive Selberg-class L-functions); explicitly defer
  unconditional standard-ZFC RH and classical-barrier-circumvention
  questions.
- Primary sources: contract thesis paragraph.
- Key claims: none.
- Dependencies: `sec:discussion`.

## Appendix — Formalization

- File: `paper/rh/appendices/app_d_formalization.tex`
- Section label: `app:formalization`
- Target length: 4–6 pages
- Purpose: per-row table of all 11 RH inventory rows (10
  mechanize_now + 1 recognition_source) with paper label →
  paper-prose name → Lean decl name → coverage notes. Includes
  the Lean-disclosure wording-discipline table per
  `paper/notes/proof-presentation-policy.md`. Documents the
  representation note from `audit_summary.md` §A3 (real-part type
  abstraction). Documents the recognition-source typed-structure-
  carrier encoding (forbidden-tokens rule; inline placement in
  `RHConditional.lean`). Documents the six no-smuggling gates +
  Gate 7 audit detail (paper-side, not Lean-mechanized).
- Primary sources: `lean/manifests/rh_manifest.toml`,
  `paper/notes/statements-of-record.yml`,
  `anti_loc/extracted_math/audit_summary.md`,
  proposal §B Six Gates + Gate 7 audit.

## Section label freeze

Locked labels (do not change without updating
`paper/notes/statements-of-record.yml`'s `target_section_hint`
fields):

`sec:intro`, `sec:framework`, `sec:involution_and_ledger`,
`sec:sat_sel_shell`, `sec:translation_theorem`,
`sec:recognition_source`, `sec:landing_chain`,
`sec:scope_and_nonclaims`, `sec:discussion`, `sec:conclusion`,
`app:formalization`.

## Page budget

Body: ~21–28 pages (sum of per-section targets above).
Distribution:
- Intro: 2–3
- Framework: 2–3
- Involution and ledger: 3–4
- Sat Sel shell: 2–3
- Translation theorem T: 2–3
- Recognition source: 2–3
- Landing chain: 2–3
- Scope and nonclaims: 2–3
- Discussion: 2–3
- Conclusion: 1

Appendix: formalization ~4–6 pages.

Total: ~25–34 pages. The recognition-source + landing-chain
sections are load-bearing. The formalization appendix's coverage
table for the 11 inventory rows is a fixed cost.
