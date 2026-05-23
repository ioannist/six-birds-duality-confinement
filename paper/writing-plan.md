# Writing Plan — Duality Confinement + RH papers

Status: Phase 9 produced 2026-05-23 (paper-writing prep arc closed).

Manager-side runbook for the per-axis drafting arcs. Refines into
per-codex-dispatch units in
`paper/<axis>/notes/drafting-plan.md` for each axis.

Per-axis order (strict, no interleaving): Paper 1 (Duality
Confinement) is drafted to Phase I.G closure first, then Paper 2
(RH). The dependency Paper 2 → Paper 1 (one-way) is the operational
reason.

This file is the deliverable from Phase 9 of
`paper/notes/prep-plan.md`. It assumes Phases 0–8 are closed and
all prep artifacts are in place. The drafting arc consumes the
prep arc; it does not re-derive any of its inputs.

## Prep-arc inputs (must be present before drafting starts)

Every drafting dispatch references one or more of these. None are
re-derived during drafting.

| Artifact | Path | Phase produced |
| --- | --- | --- |
| Cross-paper asset audit | `paper/notes/phase0-asset-audit.md` | Phase 0 |
| Paper 1 contract | `paper/duality_confinement/notes/contract.md` | Phase 0 |
| Paper 2 contract | `paper/rh/notes/contract.md` | Phase 0 |
| Cross-paper boundary | `paper/notes/cross-paper-boundary.md` | Phase 0 |
| Out-of-scope ledger | `paper/notes/out-of-scope-ledger.md` | Phase 0 |
| Notation governance | `paper/notation_and_terminology.md` | Phase 1 |
| DC macros | `paper/duality_confinement/includes/paper_macros.tex` | Phase 1 |
| RH macros | `paper/rh/includes/paper_macros.tex` | Phase 1 |
| Macro audit | `paper/notes/macro-audit.md` | Phase 1 |
| Prose-name map | `paper/notes/prose-names.md` | Phase 1 |
| Statements of record (data) | `paper/notes/statements-of-record.yml` | Phase 2 |
| Statements of record (review) | `paper/notes/statements-of-record.md` | Phase 2 |
| DC section outline | `paper/duality_confinement/notes/section-outline.md` | Phase 3 |
| RH section outline | `paper/rh/notes/section-outline.md` | Phase 3 |
| DC figure/table plan | `paper/duality_confinement/notes/figure-table-plan.md` | Phase 4 |
| RH figure/table plan | `paper/rh/notes/figure-table-plan.md` | Phase 4 |
| References database | `paper/references.bib` | Phase 5 |
| References selection log | `paper/notes/references-selection.md` | Phase 5 |
| Audience translation | `paper/notes/audience-translation.md` | Phase 6 |
| Scope fence | `paper/notes/scope-fence.md` | Phase 6 |
| Anticipated objections | `paper/notes/anticipated-objections.md` | Phase 6 |
| Proof-presentation policy | `paper/notes/proof-presentation-policy.md` | Phase 6 |
| Mechanization rebinding policy | `paper/notes/mechanization-rebinding-policy.md` | Phase 7 |
| App D skeleton (DC) | `paper/duality_confinement/appendices/app_d_formalization.tex` | Phase 7 |
| App D skeleton (RH) | `paper/rh/appendices/app_d_formalization.tex` | Phase 7 |
| Preflight gate sign-off | `paper/notes/preflight-signoff.md` | Phase 8 |
| DC drafting plan | `paper/duality_confinement/notes/drafting-plan.md` | Phase 9 |
| RH drafting plan | `paper/rh/notes/drafting-plan.md` | Phase 9 |
| DC claim-revision register | `paper/duality_confinement/notes/claim-revision-register.md` | Phase 9 |
| RH claim-revision register | `paper/rh/notes/claim-revision-register.md` | Phase 9 |
| DC artifact plan | `paper/duality_confinement/notes/artifact-plan.md` | Phase 9 |
| RH artifact plan | `paper/rh/notes/artifact-plan.md` | Phase 9 |
| DC notation workspace | `paper/duality_confinement/notes/notation.md` | Phase 9 |
| RH notation workspace | `paper/rh/notes/notation.md` | Phase 9 |

## Governing memory files (loaded in paper-writing mode)

- `feedback_no_batching.md` — strict per-subsection protocol; one
  codex task per dispatch; section-level flow review is the only
  batching exception.
- `feedback_paper_writing_role_split.md` — manager/writer split:
  Claude is manager + reviewer; codex is writer (codex writes files
  directly via `--full-auto`).
- `feedback_general_audience_accessibility.md` — audience framing:
  working mathematician with no Six Birds background.
- `feedback_academic_register.md` — register discipline: no verdict
  tokens / JSON paths / Lean identifier strings in body prose.
- `feedback_anchor_to_six_birds_literature.md` — anchor conventions
  mirror the sibling hiddenness papers
  (`/home/repos/six-birds-hiddenness/paper/hiddenness/` and
  `/home/repos/six-birds-hiddenness/paper/pvnp/`).
- `feedback_pdf_review_discipline.md` — rebuild + PDF readback per
  drafting turn.
- `feedback_table_typesetting.md` — wide-table discipline; long
  Lean identifiers belong in App D, not body tables.
- `feedback_lean_traceability_disclosure.md` — Lean coverage
  wording; consult `paper/notes/proof-presentation-policy.md` per
  subsection.

Plus the always-live: `reference_codex_cli.md`,
`feedback_codex_bootstrap_stdin.md`.

## Protocol

- **One codex task per dispatch.** Never two subsections; never one
  subsection plus one operational artifact. Tables and figures are
  each separate dispatches. Section-level flow review after a
  section is fully drafted subsection-by-subsection is the ONLY
  batching exception.
- **Resume by UUID.** The mechanization codex threads are reused
  for drafting:
  - Paper 1: `lean/.codex_thread_id_duality_confinement` =
    `019e54ad-ec86-7560-9496-5afac11cb639`
  - Paper 2: `lean/.codex_thread_id_rh` =
    `019e54cc-8015-7570-a50e-582aca58ca74`

  Resume by UUID always (per `reference_codex_cli.md`); a typo'd
  resume silently spawns a fresh thread.
- **Mode-swap first.** See the **Mode-swap procedure** section
  below. The mode-swap message is itself a codex dispatch and
  counts as the first turn of the drafting arc. It does NOT produce
  body prose — it acknowledges the transition from mechanization
  to drafting context. After the mode-swap, save
  `paper/<axis>/.codex_thread_id` pointing at the same UUID
  (drafting-context flag, distinct file from the mechanization
  thread file).
- **Codex writes files directly** via `--full-auto`; the manager
  reviews the files, not returned text.
- **Build after every dispatch.** Run
  `make paper-preflight-<axis>` after every codex turn that touches
  paper sources. If it fails, route the fix back through codex via
  the same session.
- **Read the PDF** after every turn that materially changes drafted
  content (per `feedback_pdf_review_discipline.md`).
- **Review checklist** applies to every codex output in this order
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
     `paper/<axis>/includes/paper_macros.tex`;
  7. scaffold conformance (file path, label, no off-scaffold
     dependencies);
  8. citations (canonical bibtex keys only).
- **Lean disclosure discipline** per
  `paper/notes/proof-presentation-policy.md` and the
  `feedback_lean_traceability_disclosure.md` memory: `lean_substantive`
  rows with `faithful` alignment may say "Lean proves";
  projection-shaped rows must use the "tracked by the formalization
  harness" wording; recognition-source-shaped rows use the
  typed-structure-carrier wording.
- **Mechanization rebinding** per
  `paper/notes/mechanization-rebinding-policy.md`. Every dispatch
  that touches a Lean-cited row uses the canonical paper-side
  wording in the rebinding table.
- **Academic register** per `feedback_academic_register.md`. No
  internal verdict tokens, JSON paths, Lean identifier strings in
  body prose; appendices carry that bookkeeping.
- **Claim revisions** per
  `paper/<axis>/notes/claim-revision-register.md`. Codex dispatch
  prompts that touch a row listed in the register quote the
  revised wording verbatim.
- **Audience translation** per
  `paper/notes/audience-translation.md`. Native Six Birds terms
  introduced via plain-prose first use plus the canonical first
  example.

## Mode-swap procedure

Before any drafting dispatch on a given axis, send the codex thread
a single mode-swap message. The mode-swap message announces the
transition from mechanization to per-section drafting, points at
the prep-arc artifacts, and asks codex to acknowledge.

Template (substitute `<AXIS>` and `<PAPER>`; UUID per axis above):

```
codex exec resume --json --full-auto <UUID> <<'EOF'
Mode swap: this thread now operates in paper-drafting mode for the
<PAPER> paper. Mechanization is closed (Phase H of
PLAN_mechanization.md closed 2026-05-23; 22 manifest entries with
faithful semantic alignment).

Authoritative inputs for drafting:
- Contract: paper/<AXIS>/notes/contract.md
- Section outline (labels frozen): paper/<AXIS>/notes/section-outline.md
- Figure/table plan: paper/<AXIS>/notes/figure-table-plan.md
- Claim-revision register: paper/<AXIS>/notes/claim-revision-register.md
- Artifact plan: paper/<AXIS>/notes/artifact-plan.md
- Notation workspace: paper/<AXIS>/notes/notation.md
- Drafting plan (this thread's dispatch table): paper/<AXIS>/notes/drafting-plan.md

Cross-axis inputs:
- Notation governance: paper/notation_and_terminology.md
- Prose-name map: paper/notes/prose-names.md
- Statements of record: paper/notes/statements-of-record.yml,
  paper/notes/statements-of-record.md
- Audience translation: paper/notes/audience-translation.md
- Scope fence: paper/notes/scope-fence.md
- Anticipated objections: paper/notes/anticipated-objections.md
- Proof-presentation policy: paper/notes/proof-presentation-policy.md
- Mechanization rebinding: paper/notes/mechanization-rebinding-policy.md
- Cross-paper boundary: paper/notes/cross-paper-boundary.md
- Out-of-scope ledger: paper/notes/out-of-scope-ledger.md
- Preflight gate: paper/notes/preflight-signoff.md
- References: paper/references.bib, paper/notes/references-selection.md

Discipline:
- Codex writes files directly via --full-auto; one section /
  subsection per dispatch (see drafting-plan.md).
- Body prose uses paper-prose names (prose-names.md); Lean
  identifiers appear ONLY in app:formalization tables.
- Wording per proof-presentation-policy.md (4 modes); never
  silently paraphrase a mechanized statement.
- Build + lint after every dispatch via `make paper-preflight-<AXIS>`.

Acknowledge by listing the locked section labels for this axis (no
body prose in this response). Subsequent dispatches will issue
per-subsection drafting tasks per drafting-plan.md.
EOF
```

After codex responds with the acknowledgment, save the file
`paper/<AXIS>/.codex_thread_id` containing the same UUID. This file
is a drafting-context flag distinct from the mechanization-context
flag at `lean/.codex_thread_id_<axis>`.

## Per-axis dispatch tables

The authoritative dispatch tables are in:

- `paper/duality_confinement/notes/drafting-plan.md` (Paper 1)
- `paper/rh/notes/drafting-plan.md` (Paper 2)

Each per-axis drafting plan lists every subsection in document
order with: target file, prerequisites (which prior subsections
must be drafted first), prep artifacts to reference in the prompt,
expected page length, and governing memory files.

## Cross-paper dependency (one-way)

Paper 2 → Paper 1. Paper 1 is self-contained and does not cite
Paper 2 results, except in two sanctioned forward-reference
paragraphs (in `sec:involutive_ledger` and `sec:master_theorem`)
naming Paper 2 as "the worked single-substrate validation". No
`\Cref` to Paper 2 labels from Paper 1; no `TsiokosRH*` bibkey in
Paper 1's bibliography.

Paper 2 cites Paper 1 for the master theorem, the SDTC framing,
and the V-Differential placement of RH. Paper 2's bibliography
contains `TsiokosSDTC2026` (the canonical sibling cross-citation
key).

## Sequential discipline (no interleaving)

Per directives: drafting is strictly sequential.

- Paper 1 (DC) is drafted to Phase I.G closure (full validator
  chain green; submission/ deliverables populated; committed +
  pushed) BEFORE Paper 2 (RH) begins its Phase I.A.
- Within each paper, Phase I.A → I.B → I.C → I.D → I.E → I.G is
  sequential. Phase I.F (cross-paper coherence) runs only after
  both papers have completed Phase I.E.
- Per `feedback_no_batching.md`: no parallel tool calls, no
  parallel codex dispatches, no parallel Phase work.

## Per-paper polish discipline (Phase I.G close)

- Run `make paper-preflight-<axis>` and verify clean: no
  Underfull/Overfull, no Float-too-large, no Cref-Cref artifacts,
  no undefined references or citations.
- End-to-end PDF read by the manager: scan for dangling references,
  double-word `\Cref`, table overflow, appendix-form departures
  from foundations-paper convention, and academic-register slips.
- Defects routed back through codex via the same session; no
  silent edits by the manager.
- After polish: section labels are frozen (already locked at Phase
  3 of the prep arc, but polish re-confirms no drift).
- Submission/ deliverables (metadata.json, manifest.json,
  citation-audit.md, claim-audit.md, presentation-audit.md,
  submission-checklist.md) populated per the per-axis drafting-plan.

## Cross-paper coherence pass (Phase I.F)

Runs only after both papers reach Phase I.G closure.

- Notation consistency across both PDFs: every shared symbol
  (`J`, `ψ_-`, `A_X`, `⪯`, `tr`, `Fix(J)`, `Γ`) renders identically.
- Paper 2's citations of Paper 1: master theorem statement quoted
  verbatim where reproduced; not silently paraphrased.
- Bibliography consistency: shared `paper/references.bib` entries
  used identically in both papers; sibling cross-cite in the
  Paper 2 → Paper 1 direction only.
- Any defects → per-axis fix dispatch via the corresponding paper's
  codex thread (each paper has its own thread; cross-paper fixes
  are routed per the affected paper, not as a combined dispatch).

## Pointers

- Prep plan (Phases 0–9): `paper/notes/prep-plan.md`
- Math artifacts:
  `anti_loc/extracted_math/duality_confinement_master.md`,
  `anti_loc/extracted_math/rh_construction.md`
- Audit summary: `anti_loc/extracted_math/audit_summary.md`
- Sibling hiddenness papers (mirror conventions):
  `/home/repos/six-birds-hiddenness/paper/hiddenness/`,
  `/home/repos/six-birds-hiddenness/paper/pvnp/`
- Memories:
  `~/.claude/projects/-home-repos-six-birds-duality-confinement/memory/`
