# Duality Confinement Drafting Plan

Status: Phase 9 produced 2026-05-23 (paper-writing prep arc closed).

This plan is the manager-side runbook for drafting Paper 1
(Duality Confinement). It refines `paper/writing-plan.md`'s
per-section table into per-codex-dispatch units. Each row below is
exactly one codex turn (the no-batching protocol per
`feedback_no_batching.md`).

Assumes Phases 0–8 of `paper/notes/prep-plan.md` are closed and
all prep artifacts are in place:

- Contract, section outline, figure/table plan, notation workspace,
  artifact plan, claim-revision register (per-axis)
- Statements of record, mechanization rebinding policy,
  proof-presentation policy, scope fence, audience translation,
  anticipated objections, prose-name map (cross-paper)
- Preflight gate sign-off, references selection, macro audit
  (cross-paper)

The drafting arc consumes these inputs; it does not re-derive any
of them. Drift caught during drafting (e.g., a Lean entry's
encoding choice that did not surface during Phase 2) is routed
back to the relevant prep-arc artifact via a deliberate revision
dispatch, then the drafting dispatch proceeds.

## Hard constraints (every dispatch)

- **One codex task per dispatch.** Never two subsections.
  Section-level flow review is the only batching exception.
- **Resume by UUID only.** Drafting thread is the same UUID as the
  Duality Confinement mechanization thread:
  `019e54ad-ec86-7560-9496-5afac11cb639`. Saved at
  `paper/duality_confinement/.codex_thread_id` for drafting-mode
  operational tooling.
- **Codex writes files directly** via `--full-auto`. The manager
  reviews the resulting `.tex`, never the returned text alone.
- **Build + PDF read after every drafting dispatch.** Run
  `make paper-preflight-duality_confinement`; read the affected pages
  of `paper/duality_confinement/build/main.pdf`.
- **Citations: Tsiokos-only, per `paper/references.bib`.** Allowed
  bibtex keys for Paper 1 (set in Phase I.A.6):
  `TsiokosFoundationsII2026`, `TsiokosFoundationsIII2026`. External
  classical operator-theory references (Douglas 1966, standard
  trace-class references) added in the post-prep external-reference
  pipeline, NOT in this drafting arc. Codex prompts must state this
  restriction.
- **Cross-paper boundary.** Paper 1 is self-contained; no mention of
  Paper 2 (RH) by name beyond a single forward-reference paragraph in
  `sec:involutive_ledger` (the RH involution as worked example) and
  in `sec:master_theorem` (mention the RH instantiation as Paper 2's
  contribution). No `\Cref` to Paper-2 labels, no `TsiokosRH*`
  bibkey. The one-way dependency Paper 2 → Paper 1 means Paper 1
  cites Paper 2 only as forward reference for "the worked
  single-substrate validation".
- **Review checklist** applies to every dispatch in this order (per
  `feedback_paper_writing_role_split.md`):
  1. audience accessibility for a working mathematician with no Six
     Birds background;
  2. correctness against the math artifact + statements-of-record;
  3. grounding (no fabricated counts, labels, or Lean identifiers
     that don't exist in the registry);
  4. flow within the section and into the next;
  5. readability;
  6. notation/macro compliance per
     `paper/notation_and_terminology.md` +
     `paper/duality_confinement/includes/paper_macros.tex`;
  7. scaffold conformance (file path, label, no off-scaffold
     dependencies);
  8. citations (only the canonical Tsiokos keys above).
- **Lean disclosure discipline** per
  `paper/notes/proof-presentation-policy.md`: `lean_substantive`
  rows with `faithful` alignment may say "Lean proves"; the
  Douglas-domination row must disclose the typed-cone encoding (per
  `audit_summary.md` §A1); the optimized-trace-budget row must use
  "tracked by the formalization harness" wording and disclose the
  AM-GM-as-typed-Scalar-axiom limitation (per `audit_summary.md`
  §A2); the defected-budget row carries no Lean citation
  (support_only).
- **Academic register** per `feedback_academic_register.md`. No
  internal verdict tokens, no JSON paths, no Lean identifier strings
  in body prose; the formalization appendix carries that bookkeeping.

## Subsection granularity (dispatch units)

Document-order subsection list. Each row is one codex dispatch.
Mode-swap is dispatch 0. After each section completes its
subsection dispatches, a section-level flow review dispatch closes
the section (manager judgment on whether the flow review is needed
for single-subsection sections).

| # | Dispatch | Target | Notes |
| ---: | --- | --- | --- |
| 0 | mode-swap | (no file write) | Codex acknowledges transition from mechanization to drafting; lists open questions |
| 1 | sec:intro | `sections/sec_01_intro.tex` | 2–3 pages; opens with "when must an operator-valued obstruction associated with an involutive system vanish?"; plain math first, framework idiom after; scope fence in last paragraph (SDTC as named structural law; typed-cone abstraction; cross-substrate predictions). Forward-references definitions defined in §3+. |
| 1F | sec:intro flow | (review) | Section flow check before advancing |
| 2 | sec:framework | `sections/sec_02_framework.tex` | 2–3 pages; Six Birds framework context: closure formation per Foundations I; closure-content-as-structural-fact commitment; V-Differential trace-state-only column condition; sibling structural laws (no-needles, CSL). No inventory rows (background only). |
| 2F | sec:framework flow | (review) | |
| 3 | sec:involutive_ledger | `sections/sec_03_involutive_ledger.tex` | 2–3 pages; define involutive object ledger `(X, J, μ, ψ, Y, J_iso)`; worked example 1: complex conjugation on ℂ; worked example 2: forward-reference to the RH specialization with `J_L(s) = 1 - s̄`. Row `def:duality_confinement:involutive-object-ledger`. Lean disclosure: "realized in Lean as `InvolutiveObjectLedger`". |
| 3F | sec:involutive_ledger flow | (review) | Manager judgment whether needed |
| 4A | sec:anti_invariant_ledger-A | `sections/sec_04_anti_invariant_ledger.tex` | First pass: anti-invariant projector `P_- = (I - J_iso)/2`, anti-invariant readout `ψ_- = P_- ψ`, separating-readout definitions (qualitative + quantitative); the anti-invariant ledger `A_X := ∫ ψ_- ψ_-^* dμ` introduced abstractly in the typed positive cone with explicit trace functional. Rows `def:duality_confinement:separating-readout`, `def:duality_confinement:anti-invariant-ledger`. Lean disclosure: both as "realized in Lean as ...". |
| 4B | sec:anti_invariant_ledger-B | `sections/sec_04_anti_invariant_ledger.tex` | Append: trace identity `tr A_X = ∫ ‖ψ_-‖² dμ` with one-sentence note that the identity is built into the typed-cone constructor (definitional unfolding in the encoding). Row `lem:duality_confinement:trace-identity`. Lean disclosure (typed-interface composition): "Lean records the trace identity as a constructor unfolding from the `AntiInvariantLedger` field `trace_identity`". |
| 4F | sec:anti_invariant_ledger flow | (review) | |
| 5 | sec:direct_confinement | `sections/sec_05_direct_confinement.tex` | 1–2 pages (single dispatch since the two theorems are tightly coupled and short). Statement + proof of both: separation-confinement (`A_X = 0 ⟹ μ(X∖Fix(J)) = 0`) and quantitative-confinement (Markov consequence). Rows `thm:duality_confinement:separation-confinement`, `thm:duality_confinement:quantitative-confinement`. Lean disclosure (typed-interface composition): "Lean checks `separationConfinement` composing the trace identity and separation with the measure-reading bridges `mu_zero_of_ae` and `visible_zero_of_ae` supplied as typed hypotheses; Lean checks `quantitativeConfinement` composing the trace identity with the typed `markov_bound` hypothesis". |
| 5F | sec:direct_confinement flow | (review) | |
| 6A | sec:domination-A | `sections/sec_06_domination.tex` | First pass: completed-domination-bridge definition `A_X ⪯ K^- + E` with `E ⪰ 0` defect; the exact case and its characterization. Row `def:duality_confinement:completed-domination-bridge`. Lean disclosure: "realized in Lean as `CompletedDominationBridge`". |
| 6B | sec:domination-B | `sections/sec_06_domination.tex` | Append: Douglas factorization theorem (`A ⪯ K ⟺ ∃ contraction T. V = TW`) with the typed-cone encoding disclosure (per `audit_summary.md` §A1: `DouglasData` carrier bundling the equivalence). Cite Douglas 1966 (NOTE: this external reference is deferred to user's post-prep pipeline; for now, describe as "the classical Douglas factorization"). Row `thm:duality_confinement:douglas-domination`. |
| 6F | sec:domination flow | (review) | |
| 7A | sec:master_theorem-A | `sections/sec_07_master_theorem.tex` | First pass: statement of the master theorem (involutive object ledger + separating readout + domination records `A_X ⪯ B_n` with `tr B_n → 0` ⟹ `μ(X ∖ Fix(J)) = 0`); typed-cone abstraction disclosure; named-structural-law framing of SDTC. Row `thm:duality_confinement:master-theorem`. |
| 7B | sec:master_theorem-B | `sections/sec_07_master_theorem.tex` | Append: proof sketch (trace monotonicity from `⪯`; squeeze from `tr B_n → 0`; positivity-to-zero; separation consequence chained through §5). Lean disclosure: "Lean proves the master theorem as `masterTheorem`". Forward-reference to Paper 2's RH instantiation (without `\Cref` to PvNP labels — prose-only "the worked single-substrate validation"). |
| 7F | sec:master_theorem flow | (review) | |
| 8A | sec:exhaustive_squeeze_and_budgets-A | `sections/sec_08_exhaustive_squeeze_and_budgets.tex` | First pass: exhaustive-moving-ledger definition + exhaustive-squeeze theorem. Rows `def:duality_confinement:exhaustive-moving-ledger`, `thm:duality_confinement:exhaustive-squeeze`. Lean disclosure (typed-interface composition): "Lean checks the exhaustive squeeze as `exhaustiveSqueeze`, consuming the ambient bound supplied as the moving-ledger's `exhaustive_bound` field (the reduction from moving bound to ambient bound is an interface assumption, not derived from monotonicity-of-transport primitives)". |
| 8B | sec:exhaustive_squeeze_and_budgets-B | `sections/sec_08_exhaustive_squeeze_and_budgets.tex` | Append: defected-budget shape (`def:duality_confinement:defected-budget`, support_only — no Lean citation, just paper-prose introduction) + optimized scalar trace budget proposition with AM-GM-as-typed-Scalar-axiom disclosure (per `audit_summary.md` §A2). Row `prop:duality_confinement:optimized-trace-budget`. Lean disclosure: "tracked by the formalization harness as `optimizedTraceBudget`; the AM-GM step is taken as typed-Scalar hypothesis; substantive derivation is open extension". |
| 8F | sec:exhaustive_squeeze_and_budgets flow | (review) | |
| 9 | sec:scope | `sections/sec_09_scope.tex` | 1–2 pages; nonclaims with required wording per `paper/notes/scope-fence.md`. Articulate (i) SDTC as recognition source not derived theorem; (ii) typed-cone abstraction vs operator-theoretic generality; (iii) AM-GM-as-axiom vs substantive derivation; (iv) cross-substrate predictions vs theorems; (v) no novelty for classical operator-theoretic constructions. |
| 9F | sec:scope flow | (review) | |
| 10 | sec:discussion | `sections/sec_10_discussion.tex` | 2–3 pages; cross-substrate generalization predictions (quantum self-adjointness, CPT, gauge invariance, particle-antiparticle, function-field RH) per proposal §5 — as STRUCTURAL POINTERS, not theorems. Positioning against classical operator-theoretic squeeze results. Future work: operator-theoretic generalization; substantive AM-GM; additional single-substrate validations. |
| 10F | sec:discussion flow | (review) | |
| 11 | sec:conclusion | `sections/sec_11_conclusion.tex` | 1 page; restate the SDTC structural law + master theorem; list pending mechanization directions; forward to Paper 2 as worked single-substrate validation. |
| 11F | sec:conclusion flow | (review) | |
| 12 | title/abstract/keywords | `main.tex` | Set `\title{Self-Dual Trace Confinement}`, `\subtitle` (if supported) or extend title; set `pdftitle`; write abstract per contract thesis paragraph in 200-300 words; set keywords (suggested: "duality confinement; involutive self-duality; trace confinement; closure formation; Six Birds Theory; structural law"); remove the four TODO placeholders in main.tex. |
| 13A | app:formalization-A | `appendices/app_d_formalization.tex` | Wording-discipline summary (mirror `paper/notes/proof-presentation-policy.md`'s wording table); structural overview of the typed-cone encoding; representation notes (audit_summary §A1 Douglas factorization, §A2 AM-GM as axiom). |
| 13B | app:formalization-B | `appendices/app_d_formalization.tex` | Append: per-row coverage table for the 13 Duality Confinement inventory rows (12 mechanize_now + 1 support_only) with paper label → paper-prose name → Lean decl name → coverage notes. Long Lean identifiers belong in THIS appendix per `feedback_table_typesetting.md` (not in body-table row labels). |
| 14 | end-to-end polish | (all touched files) | Section-level flow + cross-section consistency + cross-reference audit + caption sanity. Codex reviews the whole paper as a unit and proposes adjustments. |
| 15 | final PDF read | (no file write — Claude action) | Manager-side end-to-end PDF read; defects routed back via additional codex dispatches if needed |

## Per-dispatch prompt template

Each dispatch prompt (resumed by UUID) carries:

1. Paper identity: "Paper 1 (Duality Confinement), file
   `paper/duality_confinement/sections/sec_NN_<slug>.tex`, label
   `sec:<slug>`. One subsection only."
2. Hard restriction lines:
   - "Cite only `TsiokosFoundationsII2026`,
     `TsiokosFoundationsIII2026`. No external bibtex keys; the user
     adds external references (Douglas 1966 etc.) in a later
     pipeline. Do not invent keys."
   - "Paper 1 is self-contained. Mention Paper 2 (RH) ONLY in the
     two sanctioned forward-references (`sec:involutive_ledger` and
     `sec:master_theorem`); do not cite Paper 2 results, do not
     `\Cref` Paper 2 labels, do not use a `TsiokosRH*` bibkey."
   - "Audience: a working mathematician with no Six Birds
     background. Define every framework-native term on first use in
     plain mathematical language per
     `paper/notes/audience-translation.md`."
   - "Academic register: no internal verdict tokens, JSON paths,
     or Lean identifier strings in body prose; the formalization
     appendix carries that bookkeeping."
3. Mandatory sources (codex reads before drafting):
   - `paper/duality_confinement/notes/contract.md`
   - `paper/duality_confinement/notes/section-outline.md` row for
     this section
   - `paper/notes/statements-of-record.yml` rows for every label
     this subsection touches
   - `paper/notes/prose-names.md` (Lean decl → paper-prose name
     map; body prose uses paper-prose names, never Lean
     identifier strings)
   - `paper/notes/mechanization-rebinding-policy.md` row for every
     label this subsection touches (canonical Lean-disclosure
     wording per row)
   - `paper/notes/audience-translation.md` rows for framework terms
     used in this subsection
   - `paper/notes/scope-fence.md` (for `sec:intro`, `sec:scope`,
     `sec:discussion`, `sec:conclusion`)
   - `paper/notes/proof-presentation-policy.md` (for sections that
     cite Lean coverage; 4-mode wording table)
   - `paper/notes/anticipated-objections.md` (for `sec:scope`,
     `sec:discussion`; mitigation language already drafted)
   - `paper/notation_and_terminology.md` +
     `paper/duality_confinement/includes/paper_macros.tex`
     (controlled macros)
   - The relevant `anti_loc/extracted_math/duality_confinement_master.md`
     section
   - `paper/duality_confinement/notes/claim-revision-register.md`
     rows applicable to this subsection (for revised wording where
     proposal claims have shifted post-mechanization)
   - `paper/duality_confinement/notes/artifact-plan.md` (canonical
     paths for any artifact cited; App D bookkeeping)
4. Deliverable: edit the target file in place; do not create new
   files; do not modify other sections. Return a short summary of
   choices made and any open questions for the manager.

## Mode-swap prompt (dispatch 0)

```
Mode swap: this session transitions from Lean mechanization to paper
drafting. The mechanization for the Duality Confinement axis is
complete (see lean/manifests/duality_confinement_manifest.toml:
12 manifest entries; the master theorem masterTheorem is the
load-bearing entry). The drafting workflow is governed by
paper/writing-plan.md plus
paper/duality_confinement/notes/drafting-plan.md and the
paper-writing memories
(~/.claude/projects/-home-repos-six-birds-duality-confinement/memory/).

In this drafting mode you (codex) are the WRITER and Claude is the
MANAGER + REVIEWER. You receive one subsection per dispatch and
write directly into the paper/duality_confinement/ scaffold via
--full-auto. Claude reviews the file you write and either accepts
or sends a fix prompt in this same session.

Read paper/duality_confinement/notes/contract.md,
paper/duality_confinement/notes/section-outline.md,
paper/duality_confinement/notes/drafting-plan.md,
paper/duality_confinement/notes/claim-revision-register.md,
paper/notes/audience-translation.md,
paper/notes/scope-fence.md,
paper/notes/proof-presentation-policy.md,
paper/notes/statements-of-record.yml,
paper/notation_and_terminology.md, and
paper/duality_confinement/includes/paper_macros.tex.

Confirm the citation restriction (only the two Tsiokos bibkeys —
TsiokosFoundationsII2026, TsiokosFoundationsIII2026 — until the
external-reference pipeline runs).

Confirm the self-contained-Paper-1 discipline (Paper 2 mentioned
only in the two sanctioned forward-references in sec:involutive_ledger
and sec:master_theorem).

Do not produce body prose in this turn. Acknowledge the mode swap
and list any open questions about the drafting context.
```

## Per-paper polish discipline (Phase I.D close)

- Run `make paper-preflight-duality_confinement` and verify clean:
  no Underfull/Overfull, no Float-too-large, no Cref-Cref artifacts,
  no undefined references or citations.
- End-to-end PDF read by the manager: scan for dangling references,
  double-word `\Cref`, table overflow, appendix-form departures
  from foundations-paper convention, and academic-register slips
  (per `feedback_pdf_review_discipline.md`).
- Defects routed back through codex via the same session; no silent
  edits by the manager (per `feedback_paper_writing_role_split.md`).
- After the polish pass: section labels are frozen. Update
  `paper/notes/statements-of-record.yml`'s `target_section_hint`
  fields only via a deliberate label-rename dispatch (none expected
  at this point given the Phase I.A.2 section-label freeze).

## Drafting log

The manager records each dispatch's outcome inline below as drafting
proceeds. One row per dispatch: dispatch id, file touched, codex
turn summary, manager review notes, status.

| Dispatch | File | Outcome | Notes |
| --- | --- | --- | --- |
| _(filled in as drafting proceeds)_ | | | |
