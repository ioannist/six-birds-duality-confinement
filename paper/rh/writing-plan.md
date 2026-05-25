# Writing Plan — RH closure (Paper 2)

Status: Phase 9 deliverable produced 2026-05-23. Paper-2-focused
take-home runbook for the drafting arc.

Scope: this file is the **Paper-2-only** writing plan, modeled on
`paper/duality_confinement/writing-plan.md` and the sibling
hiddenness `paper/writing-plan.md` row format. It consolidates the
per-section dispatch table for Paper 2 (RH closure) into a single
document with operational protocol, per-row prep-artifact
references, the mode-swap procedure, and the review cadence.

Companions (do not duplicate):

- `paper/writing-plan.md` — the **cross-paper** manager runbook
  (Paper 1 + Paper 2 sequential discipline, cross-paper coherence
  pass, governing memories list).
- `paper/duality_confinement/writing-plan.md` — Paper-1 (DC)
  writing plan; Paper 2 may not begin drafting until Paper 1
  completes its arc.
- `paper/rh/notes/drafting-plan.md` — the **fine-granularity**
  subsection-level dispatch table (one row = one codex turn;
  splits this file's per-section rows into A/B passes + flow
  reviews per `feedback_no_batching.md`).
- `paper/notes/prep-plan.md` — the closed prep arc (Phases 0–9)
  whose deliverables this writing plan consumes.

## Sequential precondition (HARD)

Paper 2 drafting does NOT begin until Paper 1 (Duality Confinement)
has reached Phase I.G closure: full validator chain green; PDF
read end-to-end; committed and pushed. **Paper 1 closed at commit
`fc1d23a` on 2026-05-23**; Paper 2's drafting arc is now unblocked.

Per `paper/writing-plan.md` § "Sequential discipline (no
interleaving)": no parallel work, no parallel codex dispatches, no
mixing of Paper-1 fix dispatches with Paper-2 drafting dispatches
during the active drafting window.

## Paper identity

- **Working title** (locked at Phase 0): *"A Six Birds Closure of
  the Riemann Hypothesis via Self-Dual Trace Confinement on the
  Saturated Selberg Trace Layer"*.
- **Headline result**: the conditional landing chain
  `Γ_{SDTC-Selberg} ⟹ RH` (mechanized as `rhConditional`); takes
  the recognition source as an explicit hypothesis parameter and
  applies Paper 1's master theorem plus translation theorem T.
  Lean realization
  `SixBirdsDualityConfinement.RH.RHConditional.rhConditional`.
- **Construction-grade theorem**: translation theorem T
  (`translationT`): `A_Z(ζ) = 0 ⟺ RH` on the typed zero ledger
  of `Sel^!_{ζ,tr}`. Short proof from positivity (positive sum +
  positive multiplicities); the forward direction is what the
  landing chain consumes.
- **Math source-of-record**:
  `anti_loc/extracted_math/rh_construction.md` (Phase A
  consolidation; 7 sections matching mechanization queue).
- **Audit summary §A3 (real-part-type abstraction)**:
  `anti_loc/extracted_math/audit_summary.md` §A3 — the Lean
  encoding parameterizes the real-part coordinate by a typed
  `RealCoordinate`; identification with actual ℝ-valued real
  parts of nontrivial zeros of `ζ` is by construction-parameter
  assignment. Disclosed in body in `sec:involution_and_ledger`
  and in App D representation notes.
- **Inventory**: 11 rows (10 mechanize_now + 1 recognition_source);
  see `formalization/inventory/rh_paper_inventory.toml`.
- **Manifest**: 10 entries; see
  `lean/manifests/rh_manifest.toml`.
- **Codex drafting thread UUID**:
  `019e54cc-8015-7570-a50e-582aca58ca74` (same UUID as the RH
  mechanization thread; reuse per
  `feedback_paper_writing_role_split.md`). Save at
  `paper/rh/.codex_thread_id` after the mode-swap dispatch
  returns its acknowledgment.

## Paper-2 cross-paper rule

Paper 2 cites Paper 1 **substantively** for three things:

1. **The duality-confinement master theorem.** In
   `sec:landing_chain`, the master theorem statement is
   **reproduced verbatim** where it is invoked (not silently
   paraphrased); cite as `\cite{TsiokosSDTC2026}` plus
   paper-prose pointer "[Paper 1 §master-theorem]". No `\Cref` to
   Paper 1 internal labels (Paper 1's labels are not in Paper 2's
   `\Cref` namespace).
2. **The SDTC structural-law framing.** Cited in `sec:framework`,
   `sec:recognition_source`, and `sec:landing_chain` as the source
   of the Selberg-class instance `Γ_{SDTC-Selberg}`.
3. **The V-Differential trace-state-only column condition.**
   Cited in `sec:framework` as the structural-law classification
   that places SDTC inside the V-Differential program.

Per `paper/notes/cross-paper-boundary.md`: cross-paper citations
take the form `\cite{TsiokosSDTC2026}` plus paper-prose pointers
("[Paper 1] §framework", "[Paper 1] §master-theorem"). The master
theorem reproduction in `sec:landing_chain` is verbatim — any drift
is a Phase I.F cross-paper coherence defect.

Paper 2 does NOT cite Paper 2 results (no self-citation). Paper 2
does not import or cite the no-needles or CSL-SAT-hiddenness
structural-law papers beyond paper-prose mentions in
`sec:framework` (deferred to user's external-reference pipeline).

## Citation restriction (Paper 2)

Allowed bibtex keys (from `paper/references.bib`):

- `TsiokosSDTC2026` — Paper 1 sibling cross-citation (the master
  theorem, SDTC framing, V-Differential placement)
- `TsiokosFoundationsII2026` — Foundations II (the seven
  admissibility schemas that `Sel^!_{ζ,tr}` carries; BirdInt
  vocabulary)
- `TsiokosFoundationsIII2026` — Foundations III (BirdInt judgment
  shape; no-overreading-suppression theorem cited in App D's
  six-gates audit detail)

Three Tsiokos cites total (Paper 1 uses two; Paper 2 uses three).

No external bibtex keys in this drafting arc. Classical references
(Riemann 1859; Titchmarsh; Edwards; Iwaniec–Kowalski for analytic
number theory; Selberg's original papers; Iwaniec's "Spectral
Methods" for the Selberg trace formula; Weil's "Sur les 'formules
explicites'"; Bombieri's expository papers for Weil positivity;
Hilbert–Pólya, Connes, de Branges, Beurling–Nyman for classical
RH-attack barriers) are deferred to the user's post-prep external-
reference pipeline; drafting prose treats them as descriptive
without `\cite{}` for deferred bibkeys.

## Governing memory files (currently active in paper-writing mode)

- `feedback_no_batching.md` — strict per-subsection protocol; one
  codex task per dispatch; section-level flow review is the only
  batching exception.
- `feedback_paper_writing_role_split.md` — Claude is manager +
  reviewer; codex is writer; codex writes files directly via
  `--full-auto`; resume codex by UUID.
- `feedback_general_audience_accessibility.md` — audience framing:
  working mathematician with no Six Birds background; tiered
  rigor; standard math vocabulary preferred; framework-native
  terms defined on first use.
- `feedback_academic_register.md` — register discipline: no
  internal verdict tokens, JSON paths, ticket IDs, or Lean
  identifier strings in body prose; appendices carry that
  bookkeeping.
- `feedback_anchor_to_six_birds_literature.md` — anchor
  conventions mirror the sibling hiddenness papers
  (`/home/repos/six-birds-hiddenness/paper/hiddenness/` and
  `/home/repos/six-birds-hiddenness/paper/pvnp/`).
- `feedback_pdf_review_discipline.md` — rebuild + PDF readback per
  drafting turn that touches body content.
- `feedback_table_typesetting.md` — wide-table discipline;
  redesign overflowing tables rather than landscape them; long
  Lean identifiers belong in App D, not body tables.
- `feedback_lean_traceability_disclosure.md` — Lean coverage
  wording per the 4-mode table in
  `paper/notes/proof-presentation-policy.md`; the typed-structure-
  carrier wording for the recognition source `Γ_{SDTC-Selberg}`
  is mandatory.

Plus the always-live: `reference_codex_cli.md`,
`feedback_codex_bootstrap_stdin.md`.

## Protocol

- **One codex task per dispatch.** Never two subsections; never
  one subsection plus one operational artifact. Tables and
  figures are each separate tasks. Section-level flow review
  after a section is fully drafted subsection-by-subsection is
  the ONLY batching exception. Protocol violation triggers a
  delete-and-restart order per `feedback_no_batching.md`.
- **Resume by UUID.** Always read from `paper/rh/.codex_thread_id`
  (created at mode-swap); a typo'd UUID silently spawns a fresh
  thread per `reference_codex_cli.md`.
- **No sub-agents.** No `Agent` tool calls during Paper-2
  drafting. All work happens in the main conversation with codex
  as the only delegated executor.
- **No parallel tool calls during paper work.** Sequential
  dispatch and sequential tool calls only.
- **Codex writes files directly** via `--full-auto`. Claude
  reviews the resulting `.tex`, never the returned text alone.
- **Build + PDF read after every drafting dispatch.** Run
  `make paper-preflight-rh` after every codex turn that touches
  paper sources; read the affected pages of
  `paper/rh/build/main.pdf` per
  `feedback_pdf_review_discipline.md`.
- **Defects route back through codex via the same session.** No
  silent edits by the manager (per
  `feedback_paper_writing_role_split.md`).
- **Review checklist** applies to every codex output in this
  order: (0) audience accessibility (FIRST PASS, before
  everything else); (1) correctness against the math artifact +
  statements-of-record; (2) grounding in repo state (no
  fabricated counts, labels, or Lean identifiers); (3) flow
  within the section and into the next; (4) readability; (5)
  notation/macro compliance per `paper/notation_and_terminology.md`
  + `paper/rh/includes/paper_macros.tex`; (6) scaffold
  conformance (file path, label, no off-scaffold dependencies);
  (7) citations (only the canonical three Tsiokos keys above).
- **Lean disclosure wording** per
  `paper/notes/proof-presentation-policy.md` and
  `paper/notes/mechanization-rebinding-policy.md`; the rebinding
  policy gives the canonical paper-side wording per inventory row.
  Critically:
  - `obl:rh:gamma-sdtc-selberg` uses **typed-structure-carrier**
    wording (NOT "Lean axiom"; NOT "Lean proves"); discloses
    inline placement in `RHConditional.lean` per
    `lean/codex_kickoff.md` §12 and the forbidden-tokens rule
    (no `axiom`/`opaque`/`constant`/`sorry`/`admit` anywhere in
    the source tree).
  - `def:rh:nontrivial-zero-ledger` discloses the real-part-type
    abstraction (audit §A3).
  - `def:rh:sat-sel-shell` discloses the admissibility-as-
    Foundations-II-hypothesis encoding (the opaque `Audit_L`
    field; not derived in this paper).
  - `thm:rh:dc-master-applied` uses the typed-bridge composition
    wording: "Lean checks the RH-specific application of the master
    theorem as `dcMasterApplied`, composing Paper 1 [1]'s
    `masterTheorem` with the bridge fields `same_readout`,
    `visible_zero_of_ae`, and `mu_zero_of_ae` carried by the
    `GammaSdtcSelberg` record" (not a direct instantiation of the
    abstract DC ledger on the shell).
  - `thm:rh:conditional` uses the typed-bridge conditional-theorem
    framing: "Lean composes the conditional landing chain as
    `rhConditional`, taking the recognition source as the explicit
    hypothesis parameter `γ : GammaSdtcSelberg shell` and applying
    `dcMasterApplied` through its bridge fields followed by
    `translationTForward`".

## Mode swap (one-time, before first drafting dispatch)

Before any drafting dispatch, send the codex thread a single
mode-swap message. Template (substitute UUID from above):

```
codex exec resume --json --full-auto 019e54cc-8015-7570-a50e-582aca58ca74 <<'EOF'
Mode swap: this thread now operates in paper-drafting mode for
Paper 2 (RH closure). Mechanization is closed (Phase H of
PLAN_mechanization.md closed 2026-05-23; 22 manifest entries with
faithful semantic alignment). The paper-writing prep arc (Phases
0-9 of paper/notes/prep-plan.md) is closed (commits efd35b9 +
2807481). Paper 1 (Duality Confinement) drafting closed at commit
fc1d23a on 2026-05-23.

Authoritative inputs for Paper 2 drafting:

Paper-2-specific:
- paper/rh/writing-plan.md (this thread's dispatch table)
- paper/rh/notes/contract.md (thesis)
- paper/rh/notes/section-outline.md (locked section labels +
  per-section purpose)
- paper/rh/notes/drafting-plan.md (subsection granularity: A/B/flow
  passes)
- paper/rh/notes/claim-revision-register.md (revised wordings)
- paper/rh/notes/artifact-plan.md (canonical artifact paths +
  cross-paper imports)
- paper/rh/notes/notation.md (notation workspace; cross-paper
  consistency table)
- paper/rh/notes/figure-table-plan.md (planned floats)
- paper/rh/includes/paper_macros.tex (controlled macros)

Cross-paper:
- paper/writing-plan.md (cross-paper sequential discipline)
- paper/duality_confinement/writing-plan.md (Paper 1 writing plan,
  for reference on the master-theorem statement to reproduce
  verbatim)
- paper/duality_confinement/sections/sec_07_master_theorem.tex
  (the canonical Paper-1 master-theorem statement to reproduce
  verbatim in Paper 2 sec:landing_chain)
- paper/notation_and_terminology.md (notation authority)
- paper/notes/prose-names.md (Lean decl -> paper-prose name map)
- paper/notes/statements-of-record.yml (24 rows; the 11 RH rows
  are the ones this paper resolves)
- paper/notes/statements-of-record.md (review-friendly rendering)
- paper/notes/audience-translation.md (framework terms -> plain
  math first-use)
- paper/notes/scope-fence.md (nonclaim wording discipline)
- paper/notes/anticipated-objections.md (prepared mitigation
  language)
- paper/notes/proof-presentation-policy.md (4-mode Lean-disclosure
  wording table)
- paper/notes/mechanization-rebinding-policy.md (per-row canonical
  paper-side wording, including the typed-structure-carrier
  wording for GammaSdtcSelberg)
- paper/notes/cross-paper-boundary.md (one-way dependency rule;
  Paper 2 cites Paper 1 substantively; master-theorem verbatim
  reproduction discipline)
- paper/notes/out-of-scope-ledger.md (Paper 2 dropped material:
  unconditional ZFC RH, classical-barrier circumvention, GRH,
  framework-derivable Gamma)
- paper/notes/preflight-signoff.md (preflight gate)
- paper/references.bib (Tsiokos-only bibliography)
- paper/notes/references-selection.md (per-paper picks; Paper 2
  uses 3 Tsiokos cites)
- anti_loc/extracted_math/rh_construction.md (math source-of-record)
- anti_loc/extracted_math/audit_summary.md (representation notes,
  especially §A3 real-part-type abstraction)

Discipline:
- Codex writes files directly via --full-auto; one section /
  subsection per dispatch (see drafting-plan.md for subsection
  granularity).
- Body prose uses paper-prose names (prose-names.md); Lean
  identifiers appear ONLY in app:formalization tables.
- Wording per proof-presentation-policy.md (4 modes); never
  silently paraphrase a mechanized statement. The
  typed-structure-carrier wording for Gamma_{SDTC-Selberg} is
  MANDATORY (NOT "Lean axiom", NOT "Lean proves").
- Paper 2 cites Paper 1 substantively: \\cite{TsiokosSDTC2026}
  plus paper-prose pointer. Master theorem reproduced VERBATIM in
  sec:landing_chain (no silent paraphrase). No \\Cref to Paper 1
  internal labels (they are not in Paper 2's \\Cref namespace).
- Cite only TsiokosSDTC2026, TsiokosFoundationsII2026,
  TsiokosFoundationsIII2026. Classical references (Riemann 1859,
  Selberg, Weil, Hilbert-Polya, Connes, de Branges, etc.) deferred
  to the user's post-prep pipeline; drafting prose treats them
  descriptively without \\cite.
- Conditional-structure discipline: every reference to the
  headline result must state the conditional structure (the
  outside-Six-Birds reading is the conditional theorem
  Gamma_{SDTC-Selberg} =>  RH, NOT unconditional standard-ZFC RH).
- Build + lint after every dispatch via
  `make paper-preflight-rh`.

Acknowledge by listing the locked section labels for Paper 2 (no
body prose in this response). Subsequent dispatches will issue
per-subsection drafting tasks per drafting-plan.md.
EOF
```

After codex acknowledges, save the file `paper/rh/.codex_thread_id`
containing the same UUID. This file is the drafting-context flag,
distinct from the mechanization-context flag at
`lean/.codex_thread_id_rh`.

## Per-section dispatch table

Section granularity starts here: 10 body sections + 1 appendix.
During drafting, this file's per-section rows are split into A/B
subsection passes + flow-review dispatches per
`paper/rh/notes/drafting-plan.md` (the per-codex-dispatch table).
The mode-swap is dispatch 0; this file's row 1 (sec:intro) becomes
dispatch 1; row 3 (sec:involution_and_ledger) splits into
dispatches 3A + 3B + 3F; row 5 (sec:translation_theorem) splits
into 5A + 5B + 5F; row 7 (sec:landing_chain) splits into 7A + 7B
+ 7F.

| Subsection id | Target file | Prerequisites | Prep artifacts to reference in prompt | Expected length |
| --- | --- | --- | --- | --- |
| `sec:intro` | `paper/rh/sections/sec_01_intro.tex` | Mode-swap | contract.md (thesis paragraph); section-outline.md (sec:intro row); audience-translation.md rows for `formed closure`, `saturated Selberg trace closure`, `functional-equation involution`, `anti-invariant zero ledger`, `recognition source`, `conditional theorem`, `BirdInt judgment`; scope-fence.md (Paper 2 nonclaim rows: conditional theorem; not unconditional RH; not classical-barrier circumvention; not GRH; not framework-derivable Gamma); anticipated-objections.md (Paper 2 objections — Weil-positivity, classical barriers, conditional vs unconditional, real-part-type abstraction); cross-paper-boundary.md (Paper 2 cites Paper 1 substantively; \cite{TsiokosSDTC2026} for SDTC framing pointer on first use) | 2–3 pages |
| `sec:framework` | `paper/rh/sections/sec_02_framework.tex` | `sec:intro` | section-outline.md (sec:framework row); audience-translation.md rows for `Six Birds framework`, `closure formation per Foundations I`, `closure-content-as-structural-fact`, `V-Differential trace-state-only column condition`, `structural-law sibling papers`; references-selection.md (cite TsiokosSDTC2026 for the master theorem + SDTC framing + V-Differential placement; cite TsiokosFoundationsII2026 and TsiokosFoundationsIII2026 for foundations vocabulary); cross-paper-boundary.md (one-way dependency note: Paper 2 imports from Paper 1; this paper cites Paper 1 substantively); no inventory rows resolved here (background only) | 2–3 pages |
| `sec:involution_and_ledger` | `paper/rh/sections/sec_03_involution_and_ledger.tex` | `sec:framework` | statements-of-record.yml rows `def:rh:fe-involution` (line ~211), `def:rh:psi-minus-rh` (line ~225), `def:rh:nontrivial-zero-ledger` (line ~239), `def:rh:anti-invariant-zero-ledger` (line ~253); prose-names.md rows for each; mechanization-rebinding-policy.md RH rows 1–4; audit_summary.md §A3 (real-part-type abstraction — disclosed in body when the nontrivial-zero ledger is defined); proof-presentation-policy.md (`definition_entry` mode); math-artifact §Involution + §ZeroLedger + §AntiInvariantZeroLedger; notation.md (RH) symbols `\JL`, `\psimRH`, `\Lzeta`, `\Znt`, `\AZ`; sec:involution_and_ledger splits into 3A (J_L + psi_- proof) + 3B (zero ledgers + audit §A3 disclosure) per drafting-plan.md | 3–4 pages |
| `sec:sat_sel_shell` | `paper/rh/sections/sec_04_sat_sel_shell.tex` | `sec:framework`, `sec:involution_and_ledger` | statements-of-record.yml row `def:rh:sat-sel-shell` (line ~267); prose-names.md row "saturated completed Selberg trace closure"; mechanization-rebinding-policy.md RH row 5 (admissibility-as-Foundations-II-hypothesis encoding; the opaque `Audit_L` field); proof-presentation-policy.md (`definition_entry`); cite `TsiokosFoundationsII2026` for the seven admissibility schemas; math-artifact §SatSelShell; notation.md (RH) symbol `\Sel`, `\Itr`; descriptive prose for Selberg trace formula (Selberg's papers, Iwaniec — NO `\cite`, deferred); single dispatch (no A/B split) | 2–3 pages |
| `sec:translation_theorem` | `paper/rh/sections/sec_05_translation_theorem.tex` | `sec:involution_and_ledger`, `sec:sat_sel_shell` | statements-of-record.yml rows `thm:rh:translation-T` (~309 — the biconditional, HEADLINE for translation theorem T), `thm:rh:translation-T-forward` (~281), `thm:rh:translation-T-reverse` (~295); prose-names.md rows; mechanization-rebinding-policy.md RH rows 6, 7, 8 (all lean_substantive, faithful); proof-presentation-policy.md (`lean_substantive`); math-artifact §TranslationT; claim-revision-register.md R12 (drop construction-grade vocabulary; use "proven by direct positivity argument" instead); sec:translation_theorem splits into 5A (statement of the biconditional) + 5B (forward and reverse halves) per drafting-plan.md | 2–3 pages |
| `sec:recognition_source` | `paper/rh/sections/sec_06_recognition_source.tex` | `sec:framework`, `sec:sat_sel_shell`, `sec:translation_theorem` | statements-of-record.yml row `obl:rh:gamma-sdtc-selberg` (~323); prose-names.md row "the recognition source `\GamSDTCSelberg`"; mechanization-rebinding-policy.md RH row 9 (typed-structure-carrier wording; inline placement in `RHConditional.lean` per `lean/codex_kickoff.md` §12; forbidden-tokens rule); proof-presentation-policy.md (typed-structure-carrier mode — the third disclosure mode); claim-revision-register.md R2 (typed-structure-carrier encoding) + R6 (three-option derivation sweep paper-prose only); audit_summary.md (mention if relevant); cite `TsiokosSDTC2026` for SDTC framing import + Paper 1's three-option derivation sweep result (paper-prose only; no `\Cref` to Paper 1 internal labels); math-artifact §RecognitionSource; anticipated-objections.md (Paper 2 obj on "isn't this just a Lean axiom?" and "why isn't Gamma derivable?") | 2–3 pages |
| `sec:landing_chain` | `paper/rh/sections/sec_07_landing_chain.tex` | `sec:translation_theorem`, `sec:recognition_source` | statements-of-record.yml rows `thm:rh:dc-master-applied` (~341), `thm:rh:conditional` (~355, **HEADLINE**); prose-names.md rows; mechanization-rebinding-policy.md RH rows 10, 11; proof-presentation-policy.md (`lean_substantive` for both); claim-revision-register.md R1 (conditional-theorem framing) + R5 (cross-paper master-theorem citation: verbatim reproduction of Paper 1's master theorem statement); cross-paper-boundary.md (VERBATIM reproduction of Paper 1's master theorem; \cite{TsiokosSDTC2026}; no \Cref to Paper 1 internal labels); paper/duality_confinement/sections/sec_07_master_theorem.tex (the canonical Paper 1 master-theorem statement source to reproduce verbatim); math-artifact §DCMasterApplied + §RHConditional; figure-table-plan.md `fig:landing-chain-diagram` + `tab:landing-chain` plans; sec:landing_chain splits into 7A (dcMasterApplied: bridge of Paper 1's master theorem to Sel^!_{ζ,tr}; VERBATIM master-theorem reproduction) + 7B (rhConditional: the headline conditional theorem + BirdInt judgment form) per drafting-plan.md | 2–3 pages |
| `sec:scope_and_nonclaims` | `paper/rh/sections/sec_08_scope_and_nonclaims.tex` | `sec:landing_chain` | scope-fence.md (Paper 2 nonclaim rows: NC-1 through NC-12 from proposal §9 restated for Lean-coverage state post Phase H.4 sync); claim-revision-register.md R8 (NC framing), R9 (classical-barrier framing), R10 (GRH out of scope); anticipated-objections.md (full Paper 2 set: conditional vs unconditional, Weil-positivity, Hilbert-Polya, Connes, de Branges, classical barriers, real-part-type identification); out-of-scope-ledger.md (Paper 2 dropped material: unconditional ZFC RH, classical-barrier circumvention, GRH, framework-derivable Gamma, simple-zero/density results); descriptive prose for classical barriers — NO `\cite`; three-option derivation sweep mentioned paper-prose-only (per claim-revision-register R6); no inventory rows resolved here (cross-references only) | 2–3 pages |
| `sec:discussion` | `paper/rh/sections/sec_09_discussion.tex` | `sec:scope_and_nonclaims` | anticipated-objections.md (Paper 2 objections — full set; mitigation language already drafted); claim-revision-register.md R9 (classical-barrier framing: partial-spirit-aligned with but structurally-distinct-from; not circumvention), R10 (GRH future work), R11 (NS/PvNP structural parallel — paper-prose only, no \cite for sibling-track keys other than TsiokosSDTC2026 for Paper 1); references-selection.md (descriptive prose for classical RH-attack barriers — Hilbert-Polya, Connes adelic/NCG, de Branges, Beurling-Nyman, Weil-positivity — NO `\cite`); cross-paper-boundary.md (forward to Paper 1 for SDTC framing; Paper 2 has no further forward references); no inventory rows | 2–3 pages |
| `sec:conclusion` | `paper/rh/sections/sec_10_conclusion.tex` | `sec:discussion` | contract.md (thesis paragraph for restatement); out-of-scope-ledger.md (pending work: Sel^!_{ζ,tr} admissibility derivation; parameter-identification connecting shell.Z_nt to actual ζ zeros; GRH for primitive Selberg-class L-functions); claim-revision-register.md R1 (conditional framing restated); artifact-plan.md (reproducibility-statement note: same repo as Paper 1; single paragraph) | 1 page |
| `app:formalization` | `paper/rh/appendices/app_d_formalization.tex` | all body sections accepted | mechanization-rebinding-policy.md (canonical paper-side wording table to mirror as appendix wording-discipline summary); proof-presentation-policy.md (4-mode wording table — reproduce here as canonical reference); statements-of-record.yml (all 11 RH rows for the per-row coverage table); statements-of-record.md (review-friendly rendering); prose-names.md (RH section — Lean decl ↔ paper-prose name); artifact-plan.md (Lean module path per row; cross-paper-import note for `dcMasterApplied` importing Paper 1's `masterTheorem`); audit_summary.md §A3 (real-part-type abstraction representation note); manifest `lean/manifests/rh_manifest.toml` (entries list); inventory `formalization/inventory/rh_paper_inventory.toml` (cross-reference); trust base `lean/manifests/trust_base.txt`; six-gates audit detail (paper-side, not Lean-mechanized; cite `TsiokosFoundationsIII2026` for the no-overreading-suppression theorem); figure-table-plan.md `tab:formalization-coverage` plan + `tab:recognition-source-carrier` plan + `tab:six-gates` plan; pass A: wording-discipline + typed-cone overview + audit §A3 + recognition-source typed-structure-carrier disclosure + cross-paper-import note; pass B: per-row coverage table for 11 inventory rows + six-gates audit detail | 5–7 pages |

## Float dispatches

Each float (figure or table) is its own dispatch. Schedule each
after the body section that depends on it but before the section-
level flow review of that section. Per
`feedback_table_typesetting.md`: redesign tables that overflow
rather than landscape them; long Lean identifiers in App D, not
in body-table row labels.

Float candidates (per `paper/rh/notes/figure-table-plan.md`):

- `tab:sat-sel-shell-fields` — 13 fields of `Sel^!_{ζ,tr}` (in `sec:sat_sel_shell`)
- `fig:sat-sel-shell-schematic` — typed-shell schematic (after `sec:sat_sel_shell`)
- `tab:landing-chain` — the three-step chain (`Γ_{SDTC-Selberg}` → `A_Z(ζ) = 0` → RH) with the cited theorems per step (in `sec:landing_chain`)
- `fig:landing-chain-diagram` — visual of the three-step chain (after `sec:landing_chain`)
- `tab:nonclaims` — NC-1 through NC-12 with required wording (in `sec:scope_and_nonclaims`)
- `tab:six-gates` — the six no-smuggling gates + Gate 7 audit checklist (in App D)
- `tab:ns-pvnp-rh-parallel` — structural parallel with NS regularity / PvNP closure (in `sec:discussion`; descriptive references only, no `\cite` for sibling-track papers)
- `tab:formalization-coverage` — 11-row coverage table (in App D)
- `tab:representation-notes` — audit §A3 disclosure (in App D)
- `tab:recognition-source-carrier` — typed-structure-carrier disclosure (in App D)

Each float dispatch consumes the planned artifact under
`paper/rh/{figures,tables}/`. As of prep-arc close, those
directories are empty (each has a README.md placeholder pointing
at the figure-table-plan); the actual `.tex` files are created by
codex during the float dispatches.

## Review cadence

- **Per-dispatch review** happens immediately after codex returns.
  Manager runs `make paper-preflight-rh`, reads the changed source,
  reads the resulting PDF for material prose change, applies the
  8-criterion checklist (`feedback_paper_writing_role_split.md`).
- **Per-section flow review** happens after the last subsection of
  a section is drafted and accepted. May be a single codex task
  focused only on flow, transitions, internal consistency, and
  unresolved TODOs. It does NOT draft the next section. This is
  the ONE batching exception per `feedback_no_batching.md`.
- **Per-paper polish review** happens after the last body section
  and the appendix are drafted and accepted. Manager runs an
  end-to-end PDF read and dispatches one codex polish pass scoped
  to consistency, cross-references, theorem/proof presentation,
  table/figure placement, and the **verbatim-reproduction audit**
  for the master-theorem statement in `sec:landing_chain`.
  Defects route back through codex via the same session
  (`feedback_paper_writing_role_split.md`).
- **Cross-paper review (Phase I.F)** happens after both papers
  complete drafting per `paper/writing-plan.md`. Verifies the
  cross-paper-boundary discipline: Paper 2's master-theorem
  reproduction in `sec:landing_chain` matches Paper 1's
  `sec:master_theorem` statement character-for-character (modulo
  RH-specialized parameter names); shared symbols
  (`\Fix`, `\Pminus`, `\psim`, `\AX`, `\Kminus`, `\Jiso`, `\IOL`,
  `\GamSDTC`) render identically across both PDFs; bibliography
  consistency.

## Per-paper polish discipline (Paper 2 close)

- Run `make paper-preflight-rh` and verify clean: no
  Underfull/Overfull, no Float-too-large, no Cref-Cref artifacts,
  no undefined references or citations.
- End-to-end PDF read by the manager: scan for dangling
  references, double-word `\Cref`, table overflow, appendix-form
  departures from foundations-paper convention, and academic-
  register slips (per `feedback_pdf_review_discipline.md`).
- **Verbatim-reproduction audit**: cross-check that the master
  theorem statement reproduced in `sec:landing_chain` matches
  Paper 1's `sec:master_theorem` statement
  character-for-character (modulo RH-specialized parameter names).
  Any drift routes back through a fix dispatch.
- Defects routed back through codex via the same session; no
  silent edits by the manager.
- After the polish pass: section labels are frozen (already locked
  at Phase 3 of the prep arc; polish re-confirms no drift).
- Reproducibility statement (single paragraph) populated in
  `sec:conclusion` per
  `paper/rh/notes/artifact-plan.md` — same repo as Paper 1
  (https://github.com/ioannist/six-birds-duality-confinement);
  no need for a separate availability statement.

## Drafting order (Paper 2)

Per `paper/writing-plan.md` § "Sequential discipline (no
interleaving)":

0. **Sequential precondition met** (Paper 1 closed at commit
   `fc1d23a` on 2026-05-23; Paper 2's drafting arc is unblocked).
1. Mode-swap dispatch (no body prose; codex acknowledges
   transition + lists locked section labels).
2. Body sections in document order: `sec:intro` →
   `sec:framework` → `sec:involution_and_ledger` →
   `sec:sat_sel_shell` → `sec:translation_theorem` →
   `sec:recognition_source` → `sec:landing_chain` →
   `sec:scope_and_nonclaims` → `sec:discussion` →
   `sec:conclusion`. Per-section flow review after each section's
   subsection dispatches close (manager judgment for single-pass
   sections).
3. Title + abstract + keywords dispatch on `main.tex` (after all
   body sections accepted; per
   `paper/rh/notes/drafting-plan.md` dispatch 11).
4. Appendix `app:formalization` dispatches (A: wording-discipline
   summary + typed-cone overview + audit §A3 + recognition-source
   typed-structure-carrier disclosure + cross-paper-import note;
   B: per-row coverage table for 11 inventory rows + six-gates
   audit detail).
5. End-to-end polish dispatch (whole-paper consistency; includes
   the verbatim-reproduction audit for the master theorem).
6. Final manager-side PDF read; defects route back via additional
   codex dispatches if needed.
7. Paper 2 closure: committed + pushed; `make paper-preflight-rh`
   clean; section labels frozen; submission/ deliverables
   populated per the per-axis drafting-plan.

After step 7 (Paper 2 reaches "Phase I.G closure" in the
cross-paper writing-plan's vocabulary), **Phase I.F (cross-paper
coherence)** runs per `paper/writing-plan.md` — both papers'
notation consistency; Paper 2's verbatim master-theorem
reproduction; bibliography consistency.

## Status

This writing plan is the Phase 9 deliverable for Paper 2. Drafting
begins when the operator signals readiness (Paper 1 is closed;
the sequential precondition is met). The mode-swap dispatch to
the codex thread is the first action of the drafting arc; this
file's per-section table is the take-home runbook for that arc.

## Pointers

- Cross-paper writing plan: `paper/writing-plan.md`
- Paper 1 writing plan: `paper/duality_confinement/writing-plan.md`
- Per-subsection drafting plan: `paper/rh/notes/drafting-plan.md`
- Section outline (label freeze):
  `paper/rh/notes/section-outline.md`
- Contract (thesis): `paper/rh/notes/contract.md`
- Claim-revision register: `paper/rh/notes/claim-revision-register.md`
- Artifact plan: `paper/rh/notes/artifact-plan.md`
- Notation workspace: `paper/rh/notes/notation.md`
- Figure/table plan: `paper/rh/notes/figure-table-plan.md`
- Math source-of-record:
  `anti_loc/extracted_math/rh_construction.md`
- Audit summary (representation notes, especially §A3):
  `anti_loc/extracted_math/audit_summary.md`
- Paper 1 master theorem (the canonical statement to reproduce
  verbatim in Paper 2 `sec:landing_chain`):
  `paper/duality_confinement/sections/sec_07_master_theorem.tex`
- Sibling hiddenness writing plan (cross-paper model):
  `/home/repos/six-birds-hiddenness/paper/writing-plan.md`
- Paper-writing memories:
  `~/.claude/projects/-home-repos-six-birds-duality-confinement/memory/`
- Paper 1 closure commit: `fc1d23a` (`git show fc1d23a --stat`)
