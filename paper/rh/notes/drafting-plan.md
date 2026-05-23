# RH Drafting Plan

Status: Phase 9 produced 2026-05-23 (paper-writing prep arc closed).

This plan is the manager-side runbook for drafting Paper 2 (RH
closure). It refines `paper/writing-plan.md`'s per-section table
into per-codex-dispatch units. Each row below is exactly one
codex turn (the no-batching protocol per
`feedback_no_batching.md`).

Assumes Phases 0–8 of `paper/notes/prep-plan.md` are closed and
all prep artifacts are in place. The drafting arc consumes those
inputs; it does not re-derive any of them.

**Sequential precondition.** This plan does not begin executing
until Paper 1 (Duality Confinement) has reached Phase I.G closure
(committed, pushed, validator-chain green, preflight green). The
one-way dependency Paper 2 → Paper 1 means Paper 2's drafting
references Paper 1's mechanized master theorem, SDTC framing, and
V-Differential placement.

## Hard constraints (every dispatch)

- **One codex task per dispatch.** Never two subsections.
  Section-level flow review is the only batching exception.
- **Resume by UUID only.** Drafting thread is the same UUID as the
  RH mechanization thread:
  `019e54cc-8015-7570-a50e-582aca58ca74`. Saved at
  `paper/rh/.codex_thread_id` for drafting-mode operational tooling
  (created at mode-swap dispatch).
- **Codex writes files directly** via `--full-auto`. The manager
  reviews the resulting `.tex`, never the returned text alone.
- **Build + PDF read after every drafting dispatch.** Run
  `make paper-preflight-rh`; read the affected pages of
  `paper/rh/build/main.pdf`.
- **Citations: Tsiokos-only, per `paper/references.bib`.** Allowed
  bibtex keys for Paper 2: `TsiokosSDTC2026` (sibling Paper 1
  cross-cite), `TsiokosFoundationsII2026`,
  `TsiokosFoundationsIII2026`. External classical analytic-number-
  theory references (Riemann 1859, Selberg, Weil, Connes,
  Hilbert–Pólya, de Branges, etc.) added in the post-prep
  external-reference pipeline, NOT in this drafting arc. Codex
  prompts must state this restriction.
- **Cross-paper boundary.** Paper 2 cites Paper 1 for the master
  theorem, SDTC framing, V-Differential placement. The cross-paper
  citations are via `\cite{TsiokosSDTC2026}` and prose like "the
  duality-confinement master theorem of [1] (Theorem 7.X)". The
  master theorem statement is reproduced verbatim where invoked
  (in `sec:landing_chain`), not silently paraphrased. No `\Cref`
  to Paper 1 internal labels — Paper 1's labels are not visible
  in Paper 2's `\Cref` namespace.
- **Review checklist** applies to every dispatch in this order
  (per `feedback_paper_writing_role_split.md`):
  1. audience accessibility for a working mathematician with no
     Six Birds background;
  2. correctness against the math artifact + statements-of-record;
  3. grounding (no fabricated counts, labels, or Lean identifiers
     that don't exist in the registry);
  4. flow within the section and into the next;
  5. readability;
  6. notation/macro compliance per
     `paper/notation_and_terminology.md` +
     `paper/rh/includes/paper_macros.tex`;
  7. scaffold conformance (file path, label, no off-scaffold
     dependencies);
  8. citations (only the canonical Tsiokos keys above).
- **Lean disclosure discipline** per
  `paper/notes/proof-presentation-policy.md` and
  `paper/notes/mechanization-rebinding-policy.md`:
  - `lean_substantive` rows with `faithful` alignment may say
    "Lean proves" (e.g., `translationT`, `dcMasterApplied`,
    `rhConditional`).
  - `def:rh:nontrivial-zero-ledger` row must disclose the
    real-part-type abstraction (per `audit_summary.md` §A3).
  - `def:rh:sat-sel-shell` row must disclose the
    admissibility-as-Foundations-II-hypothesis encoding (the
    opaque `Audit_L` field; not derived in this paper).
  - `obl:rh:gamma-sdtc-selberg` row uses the typed-structure-
    carrier wording (NOT "Lean axiom"; NOT "Lean proves");
    discloses inline placement in `RHConditional.lean` per
    `lean/codex_kickoff.md` §12 and the forbidden-tokens rule.
- **Academic register** per `feedback_academic_register.md`. No
  internal verdict tokens, no JSON paths, no Lean identifier
  strings in body prose; the formalization appendix carries that
  bookkeeping.
- **Audience translation** per
  `paper/notes/audience-translation.md`. Native terms (formed
  closure; saturated Selberg trace closure; recognition source;
  BirdInt judgment; lawful trace instrument; etc.) introduced
  via plain-prose first-use plus the canonical first example.

## Subsection granularity (dispatch units)

Document-order subsection list. Each row is one codex dispatch.
Mode-swap is dispatch 0. After each section completes its
subsection dispatches, a section-level flow review dispatch closes
the section (manager judgment on whether the flow review is needed
for single-subsection sections).

| # | Dispatch | Target | Notes |
| ---: | --- | --- | --- |
| 0 | mode-swap | (no file write) | Codex acknowledges transition from mechanization to drafting; lists open questions; lists locked section labels |
| 1 | sec:intro | `sections/sec_01_intro.tex` | 2–3 pages; opens with "what would it take to settle whether all nontrivial zeros of `ζ` lie on the critical line?"; plain math first, framework idiom after; states the conditional structure explicitly (under the standard Six Birds closure assumption and `Γ_{SDTC-Selberg}` from Paper 1, RH follows); scope fence (conditional theorem; not unconditional RH; not classical-barrier circumvention; not GRH). Forward-references definitions defined in §3+. Cites `TsiokosSDTC2026` for the SDTC framing pointer. |
| 1F | sec:intro flow | (review) | Section flow check before advancing |
| 2 | sec:framework | `sections/sec_02_framework.tex` | 2–3 pages; Six Birds framework context: closure formation per Foundations I; closure-content-as-structural-fact; V-Differential trace-state-only column citing Paper 1; structural-law sibling papers (no-needles for NS; CSL-SAT-hiddenness for PvNP; SDTC for RH). One-way dependency note. Cites `TsiokosSDTC2026`, `TsiokosFoundationsII2026`, `TsiokosFoundationsIII2026`. No inventory rows (background only). |
| 2F | sec:framework flow | (review) | |
| 3A | sec:involution_and_ledger-A | `sections/sec_03_involution_and_ledger.tex` | First pass: functional-equation involution `J_L(s) = 1 - \bar{s}` with critical-line fixed locus and proof of involutivity; separating anti-invariant readout `\psi_-(s) = Re(s) - 1/2` with proof of anti-invariance. Rows `def:rh:fe-involution`, `def:rh:psi-minus-rh`. Lean disclosure: "realized in Lean as `feInvolution` / `psiMinusRh`". |
| 3B | sec:involution_and_ledger-B | `sections/sec_03_involution_and_ledger.tex` | Append: nontrivial-zero ledger `Z_ζ^{nt}` as typed multiset with `m_ρ > 0` multiplicities; anti-invariant zero ledger `A_Z(\zeta) = Σ_ρ m_ρ |Re(ρ) - 1/2|^2`. Disclose the real-part-type abstraction (audit_summary §A3): real-part coordinate is parameterized by a typed `RealCoordinate`; identification with actual ℝ-valued real parts is by construction-parameter assignment. Rows `def:rh:nontrivial-zero-ledger`, `def:rh:anti-invariant-zero-ledger`. |
| 3F | sec:involution_and_ledger flow | (review) | |
| 4 | sec:sat_sel_shell | `sections/sec_04_sat_sel_shell.tex` | 2–3 pages (single dispatch, definition + admissibility-disclosure pair). Introduce typed shell `Sel^!_{ζ,tr}` as formed-layer object; name the 13 fields; disclose: admissibility per the seven Foundations II schemas is encoded as the opaque `Audit_L` field (not derived in this paper). Cites Paper 1 [1] for foundations references. Row `def:rh:sat-sel-shell`. Lean disclosure: "realized in Lean as `SatSelShell`". |
| 4F | sec:sat_sel_shell flow | (review) | |
| 5A | sec:translation_theorem-A | `sections/sec_05_translation_theorem.tex` | First pass: statement of translation theorem T as biconditional `A_Z(\zeta) = 0 ⟺ RH` (on typed zero ledger of `Sel^!_{ζ,tr}`); construction-grade headline framing. Row `thm:rh:translation-T`. Lean disclosure: "Lean proves the translation theorem T as `translationT`". |
| 5B | sec:translation_theorem-B | `sections/sec_05_translation_theorem.tex` | Append: forward direction (`A_Z(\zeta) = 0 ⟹ ∀ρ, Re(ρ) = 1/2`) from positive sum + positive multiplicities; reverse direction by substitution. Both reader-helpful and short. Rows `thm:rh:translation-T-forward`, `thm:rh:translation-T-reverse`. Lean disclosure: "Lean proves the forward / reverse halves as `translationTForward` / `translationTReverse`". |
| 5F | sec:translation_theorem flow | (review) | |
| 6 | sec:recognition_source | `sections/sec_06_recognition_source.tex` | 2–3 pages; introduce `Γ_{SDTC-Selberg}` as structural recognition source supplied by Paper 1 [1] (SDTC structural law applied to Selberg-class instance). State: on `Sel^!_{ζ,tr}`, a sequence of completed domination records `A_Z(\zeta) ⪯ B_n` with `tr B_n → 0` exists as content of formed-layer closure per Foundations I. Disclose: NOT a Lean axiom; encoded as typed structure carrier `GammaSdtcSelberg` declared inline in `RHConditional.lean` per `lean/codex_kickoff.md` §12; forbidden-tokens rule bans `axiom`/`opaque`/`constant`/`sorry`/`admit`. Cite Paper 1's three-option derivation sweep result (paper-prose only; no `\Cref` to Paper 1 internal labels). Row `obl:rh:gamma-sdtc-selberg`. Lean disclosure: typed-structure-carrier wording per mechanization-rebinding-policy. |
| 6F | sec:recognition_source flow | (review) | |
| 7A | sec:landing_chain-A | `sections/sec_07_landing_chain.tex` | First pass: state the headline conditional theorem. Three-step chain: (i) from `Γ_{SDTC-Selberg}`, extract the domination-records witness; (ii) apply duality-confinement master theorem from Paper 1 [1] (REPRODUCE THE MASTER THEOREM STATEMENT VERBATIM per `cross-paper-boundary.md`) to derive `A_Z(\zeta) = 0`; (iii) apply translation theorem T (forward) to derive `∀ρ ∈ Z_ζ^{nt}, Re(ρ) = 1/2`. Row `thm:rh:dc-master-applied`. Lean disclosure: "Lean derives `dcMasterApplied`, instantiating Paper 1 [1]'s `masterTheorem` via the bridge parameter `mu_zero_of_ae`". |
| 7B | sec:landing_chain-B | `sections/sec_07_landing_chain.tex` | Append: the conditional landing chain `Γ_{SDTC-Selberg} ⟹ RH` and its BirdInt-judgment form. Introduce BirdInt judgment via audience-translation on first use. Outside-Six-Birds reading: the conditional theorem `Γ_{SDTC-Selberg} ⟹ RH`. Row `thm:rh:conditional` (the HEADLINE of Paper 2). Lean disclosure: "Lean proves the conditional landing chain as `rhConditional`, with the recognition source supplied as an explicit hypothesis parameter `γ : GammaSdtcSelberg shell`". |
| 7F | sec:landing_chain flow | (review) | |
| 8 | sec:scope_and_nonclaims | `sections/sec_08_scope_and_nonclaims.tex` | 2–3 pages; nonclaims with required wording per `paper/notes/scope-fence.md`. Articulate NC-1 through NC-12 from proposal §9 restated for Lean-coverage state post Phase H.4 sync; conditional structure (not unconditional RH); recognition-source provenance (supplied by Paper 1, not derived from framework primitives, not a Lean axiom); parameter-identification disclosure (`shell.Z_nt` is typed multiset parameter); classical-barrier framing (partial-spirit-aligned with but structurally-distinct-from Hilbert–Pólya, Connes, de Branges, Weil-positivity); GRH scope-out (`L = ζ` only); simple-zero / density-of-zeros scope-out; admissibility-as-hypothesis; three-option derivation sweep (paper-prose only); six no-smuggling gates + Gate 7 (detail in App D). |
| 8F | sec:scope_and_nonclaims flow | (review) | |
| 9 | sec:discussion | `sections/sec_09_discussion.tex` | 2–3 pages; structural parallel with NS regularity and PvNP closure (proposal §8); positioning against classical RH attack barriers (Weil positivity is readout-level structurally distinct from source-level per audit-currency derivability tension); GRH extension as future work; Lean mechanization extensions as future work (`Sel^!_{ζ,tr}` admissibility derivation; parameter-identification connecting `shell.Z_nt` to actual `ζ` zeros). |
| 9F | sec:discussion flow | (review) | |
| 10 | sec:conclusion | `sections/sec_10_conclusion.tex` | 1 page; restate the conditional theorem; list pending work (admissibility derivation; parameter-identification; GRH); explicitly defer unconditional standard-ZFC RH and classical-barrier-circumvention questions. |
| 10F | sec:conclusion flow | (review) | |
| 11 | title/abstract/keywords | `main.tex` | Set `\title{A Six Birds Closure of the Riemann Hypothesis via Self-Dual Trace Confinement on the Saturated Selberg Trace Layer}`; set `pdftitle`; write abstract per contract thesis paragraph in 200-300 words (conditional theorem framing explicit in the abstract); set keywords (suggested: "Riemann hypothesis; conditional theorem; Selberg-class trace; self-dual trace confinement; closure formation; Six Birds Theory"); remove TODO placeholders. |
| 12A | app:formalization-A | `appendices/app_d_formalization.tex` | Wording-discipline summary (mirror `paper/notes/proof-presentation-policy.md`); representation note (audit_summary §A3 real-part-type abstraction); recognition-source typed-structure-carrier disclosure (forbidden-tokens rule; inline placement in `RHConditional.lean`); cross-paper-import note (`dcMasterApplied` imports Paper 1's `masterTheorem`). |
| 12B | app:formalization-B | `appendices/app_d_formalization.tex` | Append: per-row coverage table for 11 RH inventory rows (10 mechanize_now + 1 recognition_source). Per `feedback_table_typesetting.md`, long Lean identifiers belong in this appendix, not body tables. Six no-smuggling gates + Gate 7 audit detail (paper-side, not Lean-mechanized). |
| 13 | end-to-end polish | (all touched files) | Section-level flow + cross-section consistency + cross-reference audit + caption sanity. Codex reviews the whole paper as a unit and proposes adjustments. |
| 14 | final PDF read | (no file write — Claude action) | Manager-side end-to-end PDF read; defects routed back via additional codex dispatches if needed |

## Per-dispatch prompt template

Each dispatch prompt (resumed by UUID) carries:

1. Paper identity: "Paper 2 (RH closure), file
   `paper/rh/sections/sec_NN_<slug>.tex`, label `sec:<slug>`. One
   subsection only."
2. Hard restriction lines:
   - "Cite only `TsiokosSDTC2026`, `TsiokosFoundationsII2026`,
     `TsiokosFoundationsIII2026`. No external bibtex keys; the
     user adds external references (Riemann 1859, Selberg, Weil,
     etc.) in a later pipeline. Do not invent keys."
   - "Paper 2 cites Paper 1 for the master theorem (verbatim
     reproduction where invoked), SDTC framing, and V-Differential
     placement. Cite as `\cite{TsiokosSDTC2026}` plus paper-prose
     pointer; do not `\Cref` Paper 1 internal labels."
   - "Audience: a working mathematician with no Six Birds
     background. Define every framework-native term on first use
     in plain mathematical language per
     `paper/notes/audience-translation.md`."
   - "Academic register: no internal verdict tokens, JSON paths,
     or Lean identifier strings in body prose; the formalization
     appendix carries that bookkeeping."
   - "Conditional structure must be stated explicitly wherever
     the headline result is referenced (per
     `paper/notes/scope-fence.md`); the outside-Six-Birds
     reading is the conditional theorem
     `Γ_{SDTC-Selberg} ⟹ RH`, not unconditional standard-ZFC RH."
3. Mandatory sources (codex reads before drafting):
   - `paper/rh/notes/contract.md`
   - `paper/rh/notes/section-outline.md` row for this section
   - `paper/notes/statements-of-record.yml` rows for every label
     this subsection touches
   - `paper/notes/prose-names.md` (Lean decl → paper-prose name
     map; body prose uses paper-prose names, never Lean
     identifier strings)
   - `paper/notes/mechanization-rebinding-policy.md` row for every
     label this subsection touches (canonical Lean-disclosure
     wording per row; cross-paper rebinding for `dcMasterApplied`)
   - `paper/notes/audience-translation.md` rows for framework
     terms used in this subsection
   - `paper/notes/scope-fence.md` (for `sec:intro`,
     `sec:scope_and_nonclaims`, `sec:discussion`, `sec:conclusion`)
   - `paper/notes/proof-presentation-policy.md` (4-mode wording
     table)
   - `paper/notes/anticipated-objections.md` (for
     `sec:scope_and_nonclaims`, `sec:discussion`; mitigation
     language already drafted)
   - `paper/notes/cross-paper-boundary.md` (canonical one-way
     dependency; verbatim-reproduction rule for the master theorem)
   - `paper/notation_and_terminology.md` +
     `paper/rh/includes/paper_macros.tex` (controlled macros)
   - The relevant `anti_loc/extracted_math/rh_construction.md`
     section
   - `paper/rh/notes/claim-revision-register.md` rows applicable
     to this subsection
   - `paper/rh/notes/artifact-plan.md` (canonical paths for any
     artifact cited; App D bookkeeping)
4. Deliverable: edit the target file in place; do not create new
   files; do not modify other sections. Return a short summary of
   choices made and any open questions for the manager.

## Mode-swap prompt (dispatch 0)

```
Mode swap: this session transitions from Lean mechanization to
paper drafting. The mechanization for the RH axis is complete (see
lean/manifests/rh_manifest.toml: 10 manifest entries; the conditional
landing chain rhConditional is the load-bearing entry). The drafting
workflow is governed by paper/writing-plan.md plus
paper/rh/notes/drafting-plan.md and the paper-writing memories
(~/.claude/projects/-home-repos-six-birds-duality-confinement/memory/).

In this drafting mode you (codex) are the WRITER and Claude is the
MANAGER + REVIEWER. You receive one subsection per dispatch and
write directly into the paper/rh/ scaffold via --full-auto. Claude
reviews the file you write and either accepts or sends a fix prompt
in this same session.

Read paper/rh/notes/contract.md,
paper/rh/notes/section-outline.md,
paper/rh/notes/drafting-plan.md,
paper/rh/notes/claim-revision-register.md,
paper/rh/notes/artifact-plan.md,
paper/rh/notes/notation.md,
paper/notes/audience-translation.md,
paper/notes/scope-fence.md,
paper/notes/anticipated-objections.md,
paper/notes/proof-presentation-policy.md,
paper/notes/mechanization-rebinding-policy.md,
paper/notes/cross-paper-boundary.md,
paper/notes/statements-of-record.yml,
paper/notes/prose-names.md,
paper/notation_and_terminology.md, and
paper/rh/includes/paper_macros.tex.

Confirm the citation restriction (only the three Tsiokos bibkeys —
TsiokosSDTC2026, TsiokosFoundationsII2026, TsiokosFoundationsIII2026 —
until the external-reference pipeline runs).

Confirm the conditional-structure discipline (every reference to
the headline result must state the conditional structure;
unconditional standard-ZFC RH is explicitly out of scope).

Confirm the cross-paper-citation discipline (master theorem
reproduced verbatim where invoked; cite `\cite{TsiokosSDTC2026}`
plus paper-prose pointer; no `\Cref` to Paper 1 internal labels).

Do not produce body prose in this turn. Acknowledge the mode swap,
list the locked section labels (per
paper/rh/notes/section-outline.md), and list any open questions
about the drafting context.
```

## Per-paper polish discipline (Phase I.G close)

- Run `make paper-preflight-rh` and verify clean: no
  Underfull/Overfull, no Float-too-large, no Cref-Cref artifacts,
  no undefined references or citations.
- End-to-end PDF read by the manager: scan for dangling references,
  double-word `\Cref`, table overflow, appendix-form departures
  from foundations-paper convention, and academic-register slips
  (per `feedback_pdf_review_discipline.md`).
- Defects routed back through codex via the same session; no
  silent edits by the manager (per
  `feedback_paper_writing_role_split.md`).
- After the polish pass: section labels are frozen. Update
  `paper/notes/statements-of-record.yml`'s `target_section_hint`
  fields only via a deliberate label-rename dispatch (none
  expected at this point given the Phase 3 section-label freeze).
- Verbatim-reproduction audit: cross-check that the master theorem
  statement reproduced in `sec:landing_chain` matches Paper 1's
  `sec:master_theorem` statement character-for-character (modulo
  RH-specialized parameter names). This is a Phase I.G close
  task; any drift routes back through a fix dispatch.

## Drafting log

The manager records each dispatch's outcome inline below as
drafting proceeds. One row per dispatch: dispatch id, file touched,
codex turn summary, manager review notes, status.

| Dispatch | File | Outcome | Notes |
| --- | --- | --- | --- |
| _(filled in as drafting proceeds; this paper's drafting begins only after Paper 1 reaches Phase I.G closure per `paper/writing-plan.md`)_ | | | |
