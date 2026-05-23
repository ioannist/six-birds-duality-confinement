# Writing Plan — Duality Confinement (Paper 1)

Status: Phase 9 deliverable produced 2026-05-23. Paper-1-focused
take-home runbook for the drafting arc.

Scope: this file is the **Paper-1-only** writing plan, modeled on
the hiddenness sibling's `paper/writing-plan.md` row format. It
consolidates the per-section dispatch table for Paper 1 (Duality
Confinement) into a single document with operational protocol, the
prep-arc artifact references per row, the mode-swap procedure, and
the review cadence.

Companions (do not duplicate):

- `paper/writing-plan.md` — the **cross-paper** manager runbook
  (Paper 1 + Paper 2 sequential discipline, cross-paper coherence
  pass, governing memories list).
- `paper/duality_confinement/notes/drafting-plan.md` — the
  **fine-granularity** subsection-level dispatch table (one row =
  one codex turn; splits this file's per-section rows into A/B
  passes + flow reviews per the per-subsection protocol of
  `feedback_no_batching.md`).
- `paper/notes/prep-plan.md` — the closed prep arc (Phases 0–9)
  whose deliverables this writing plan consumes.

## Paper identity

- **Working title** (locked at Phase 0): *"Self-Dual Trace
  Confinement: A Six Birds Structural Law for Formed Closures
  Under Involutive Self-Duality"*.
- **Headline result**: the duality-confinement membrane theorem
  (`thm:duality_confinement:master-theorem`); Lean realization
  `SixBirdsDualityConfinement.DualityConfinement.MasterTheorem.masterTheorem`.
- **Math source-of-record**:
  `anti_loc/extracted_math/duality_confinement_master.md` (Phase A
  consolidation; 8 sections matching mechanization queue).
- **Inventory**: 13 rows (12 mechanize_now + 1 support_only); see
  `formalization/inventory/duality_confinement_paper_inventory.toml`.
- **Manifest**: 12 entries; see
  `lean/manifests/duality_confinement_manifest.toml`.
- **Codex drafting thread UUID**:
  `019e54ad-ec86-7560-9496-5afac11cb639` (same UUID as the
  Duality Confinement mechanization thread; per
  `feedback_paper_writing_role_split.md`, reuse the mechanization
  thread for drafting). Save at
  `paper/duality_confinement/.codex_thread_id` after the mode-swap
  dispatch returns its acknowledgment.

## Paper-1 cross-paper rule

Paper 1 is **self-contained**. Paper 2 is mentioned only in two
**prose-only** sanctioned forward-reference paragraphs:
- in `sec:involutive_ledger` (the RH involution `J_L(s) = 1 - \bar{s}`
  as the worked example); and
- in `sec:master_theorem` (Paper 2 named as "the worked single-
  substrate validation").

**No `\Cref` to Paper 2 labels. No `TsiokosRH*` bibkey in Paper 1's
bibliography.** The asymmetric one-way dependency rule is asserted
in `paper/notes/cross-paper-boundary.md`, `paper/writing-plan.md`,
this file, `paper/duality_confinement/notes/drafting-plan.md`, and
`paper/duality_confinement/notes/claim-revision-register.md`.

## Citation restriction (Paper 1)

Allowed bibtex keys (from `paper/references.bib`):

- `TsiokosFoundationsII2026` — Foundations II (admissibility,
  FATCD, primitive roles)
- `TsiokosFoundationsIII2026` — Foundations III (BirdInt judgment,
  visibility tags, gate-status family, claim records)

No external bibtex keys in this drafting arc. Classical references
(Douglas 1966, Reed–Simon, Bhatia, Horn–Johnson, etc.) are deferred
to the user's post-prep external-reference pipeline; drafting
prose treats them as descriptive ("the classical Douglas
factorization") without `\cite{}` for deferred bibkeys.

## Governing memory files (currently active in paper-writing mode)

- `feedback_no_batching.md` — strict per-subsection protocol; one
  codex task per dispatch; section-level flow review is the only
  batching exception.
- `feedback_paper_writing_role_split.md` — Claude is manager +
  reviewer; codex is writer; codex writes files directly via
  `--full-auto`; resume codex by UUID.
- `feedback_general_audience_accessibility.md` — audience framing:
  working mathematician with no Six Birds background; tiered
  rigor; standard math vocabulary preferred; framework-native terms
  defined on first use.
- `feedback_academic_register.md` — register discipline: no
  internal verdict tokens, JSON paths, ticket IDs, or Lean
  identifier strings in body prose; appendices carry that
  bookkeeping.
- `feedback_anchor_to_six_birds_literature.md` — anchor conventions
  mirror the sibling hiddenness papers
  (`/home/repos/six-birds-hiddenness/paper/hiddenness/` and
  `/home/repos/six-birds-hiddenness/paper/pvnp/`).
- `feedback_pdf_review_discipline.md` — rebuild + PDF readback per
  drafting turn that touches body content.
- `feedback_table_typesetting.md` — wide-table discipline;
  redesign overflowing tables rather than landscape them; long
  Lean identifiers belong in App D, not body tables.
- `feedback_lean_traceability_disclosure.md` — Lean coverage
  wording per the 4-mode table in
  `paper/notes/proof-presentation-policy.md`.

Plus the always-live: `reference_codex_cli.md`,
`feedback_codex_bootstrap_stdin.md`.

## Protocol

- **One codex task per dispatch.** Never two subsections; never one
  subsection plus one operational artifact. Tables and figures are
  each separate tasks. Section-level flow review after a section is
  fully drafted subsection-by-subsection is the ONLY batching
  exception. Protocol violation triggers a delete-and-restart
  order per `feedback_no_batching.md`.
- **Resume by UUID.** Always read from
  `paper/duality_confinement/.codex_thread_id` (created at mode-
  swap); a typo'd UUID silently spawns a fresh thread per
  `reference_codex_cli.md`.
- **No sub-agents.** No `Agent` tool calls during paper-1 drafting.
  All work happens in the main conversation with codex as the only
  delegated executor.
- **No parallel tool calls during paper work.** Sequential dispatch
  and sequential tool calls only.
- **Codex writes files directly** via `--full-auto`. Claude reviews
  the resulting `.tex`, never the returned text alone.
- **Build + PDF read after every drafting dispatch.** Run
  `make paper-preflight-duality_confinement` after every codex turn
  that touches paper sources; read the affected pages of
  `paper/duality_confinement/build/main.pdf` per
  `feedback_pdf_review_discipline.md`.
- **Defects route back through codex via the same session.** No
  silent edits by the manager (per
  `feedback_paper_writing_role_split.md`).
- **Review checklist** applies to every codex output in this order:
  (0) audience accessibility (FIRST PASS, before everything else);
  (1) correctness against the math artifact + statements-of-record;
  (2) grounding in repo state (no fabricated counts, labels, or
  Lean identifiers); (3) flow within the section and into the
  next; (4) readability; (5) notation/macro compliance per
  `paper/notation_and_terminology.md` +
  `paper/duality_confinement/includes/paper_macros.tex`; (6)
  scaffold conformance (file path, label, no off-scaffold
  dependencies); (7) citations (only the canonical Tsiokos keys
  above).
- **Lean disclosure wording** per
  `paper/notes/proof-presentation-policy.md` and
  `paper/notes/mechanization-rebinding-policy.md`; the rebinding
  policy gives the canonical paper-side wording per
  inventory row.

## Mode swap (one-time, before first drafting dispatch)

Before any drafting dispatch, send the codex thread a single
mode-swap message. Template (substitute UUID from above):

```
codex exec resume --json --full-auto 019e54ad-ec86-7560-9496-5afac11cb639 <<'EOF'
Mode swap: this thread now operates in paper-drafting mode for
Paper 1 (Duality Confinement). Mechanization is closed (Phase H of
PLAN_mechanization.md closed 2026-05-23; 22 manifest entries with
faithful semantic alignment).

Authoritative inputs for drafting:
- Contract: paper/duality_confinement/notes/contract.md
- Section outline (labels frozen): paper/duality_confinement/notes/section-outline.md
- Figure/table plan: paper/duality_confinement/notes/figure-table-plan.md
- Claim-revision register: paper/duality_confinement/notes/claim-revision-register.md
- Artifact plan: paper/duality_confinement/notes/artifact-plan.md
- Notation workspace: paper/duality_confinement/notes/notation.md
- Paper-1 writing plan (this thread's dispatch table): paper/duality_confinement/writing-plan.md
- Per-subsection dispatch detail: paper/duality_confinement/notes/drafting-plan.md

Cross-paper inputs:
- Cross-paper writing plan: paper/writing-plan.md
- Notation governance: paper/notation_and_terminology.md
- Prose-name map: paper/notes/prose-names.md
- Statements of record: paper/notes/statements-of-record.yml,
  paper/notes/statements-of-record.md
- Audience translation: paper/notes/audience-translation.md
- Scope fence: paper/notes/scope-fence.md
- Anticipated objections: paper/notes/anticipated-objections.md
- Proof-presentation policy: paper/notes/proof-presentation-policy.md
- Mechanization rebinding policy: paper/notes/mechanization-rebinding-policy.md
- Cross-paper boundary: paper/notes/cross-paper-boundary.md
- Out-of-scope ledger: paper/notes/out-of-scope-ledger.md
- Preflight gate: paper/notes/preflight-signoff.md
- References: paper/references.bib,
  paper/notes/references-selection.md

Discipline:
- Codex writes files directly via --full-auto; one section /
  subsection per dispatch (see drafting-plan.md for subsection
  granularity).
- Body prose uses paper-prose names (prose-names.md); Lean
  identifiers appear ONLY in app:formalization tables.
- Wording per proof-presentation-policy.md (4 modes); never
  silently paraphrase a mechanized statement.
- Paper 1 is self-contained: no \\Cref to Paper 2 labels; no
  TsiokosRH* bibkey; the two sanctioned Paper 2 forward references
  in sec:involutive_ledger and sec:master_theorem are
  prose-only.
- Cite only TsiokosFoundationsII2026 and TsiokosFoundationsIII2026.
  Classical references (Douglas 1966 etc.) deferred to the user's
  post-prep pipeline; drafting prose treats them descriptively
  without \\cite.
- Build + lint after every dispatch via
  `make paper-preflight-duality_confinement`.

Acknowledge by listing the locked section labels for Paper 1 (no
body prose in this response). Subsequent dispatches will issue
per-subsection drafting tasks per drafting-plan.md.
EOF
```

After codex acknowledges, save the file
`paper/duality_confinement/.codex_thread_id` containing the same
UUID. This file is the drafting-context flag, distinct from the
mechanization-context flag at
`lean/.codex_thread_id_duality_confinement`.

## Per-section dispatch table

Section granularity starts here: 11 body sections + 1 appendix.
During drafting, this file's per-section rows are split into A/B
subsection passes + flow-review dispatches per
`paper/duality_confinement/notes/drafting-plan.md` (the per-codex-
dispatch table). The mode-swap is dispatch 0; this file's row 1
becomes dispatches 1 + 1F (flow); row 4 becomes dispatches 4A +
4B + 4F; and so on.

| Subsection id | Target file | Prerequisites | Prep artifacts to reference in prompt | Expected length |
| --- | --- | --- | --- | --- |
| `sec:intro` | `paper/duality_confinement/sections/sec_01_intro.tex` | Mode-swap | contract.md (thesis paragraph); section-outline.md (sec:intro row); audience-translation.md rows for `involutive object ledger`, `anti-invariant readout`, `trace-class regime`, `formed closure`, `recognition source`, `Self-Dual Trace Confinement (SDTC)`, `duality-confinement membrane theorem`; scope-fence.md (Paper 1 nonclaim rows: SDTC-as-named-not-derived, typed-cone abstraction, AM-GM-as-axiom, cross-substrate predictions); anticipated-objections.md (Paper 1 obj 1–4); cross-paper-boundary.md (forward-reference rule) | 2–3 pages |
| `sec:framework` | `paper/duality_confinement/sections/sec_02_framework.tex` | `sec:intro` | section-outline.md (sec:framework row); audience-translation.md rows for `Six Birds framework`, `closure formation per Foundations I`, `closure-content-as-structural-fact`, `V-Differential trace-state-only column condition`, `sibling structural laws`; references-selection.md (cite TsiokosFoundationsII2026, TsiokosFoundationsIII2026 here on first use); no inventory rows resolved here (background only) | 2–3 pages |
| `sec:involutive_ledger` | `paper/duality_confinement/sections/sec_03_involutive_ledger.tex` | `sec:framework` | statements-of-record.yml row `def:duality_confinement:involutive-object-ledger`; prose-names.md row "involutive object ledger"; mechanization-rebinding-policy.md row 1 (DC table); proof-presentation-policy.md (`definition_entry` mode); math-artifact §Involution; notation.md (DC) symbols `J`, `J_iso`, `\IOL`, `\Fix`; figure-table-plan.md `fig:involutive-ledger-schematic` plan; cross-paper-boundary.md (sanctioned forward reference 1 of 2 — RH `J_L(s) = 1 - \bar{s}` as worked example, prose-only) | 2–3 pages |
| `sec:anti_invariant_ledger` | `paper/duality_confinement/sections/sec_04_anti_invariant_ledger.tex` | `sec:involutive_ledger` | statements-of-record.yml rows `def:duality_confinement:separating-readout`, `def:duality_confinement:anti-invariant-ledger`, `lem:duality_confinement:trace-identity`; prose-names.md rows for each; mechanization-rebinding-policy.md DC rows 2, 3, 4; audit_summary.md §A1 representation note (typed-cone encoding for trace identity); proof-presentation-policy.md (`definition_entry` for definitions; `lean_substantive` for the trace identity with the typed-cone definitional-unfolding caveat); math-artifact §Separation + §AntiInvariantLedger; notation.md (DC) symbols `\Pminus`, `\psim`, `\AX`, `\trace`, `\preceq` | 3–4 pages |
| `sec:direct_confinement` | `paper/duality_confinement/sections/sec_05_direct_confinement.tex` | `sec:anti_invariant_ledger` | statements-of-record.yml rows `thm:duality_confinement:separation-confinement`, `thm:duality_confinement:quantitative-confinement`; prose-names.md rows for both; mechanization-rebinding-policy.md DC rows 5, 6 (both `lean_substantive`/`faithful`); proof-presentation-policy.md (`lean_substantive` wording "Lean proves"); math-artifact §DirectConfinement | 1–2 pages |
| `sec:domination` | `paper/duality_confinement/sections/sec_06_domination.tex` | `sec:anti_invariant_ledger` | statements-of-record.yml rows `def:duality_confinement:completed-domination-bridge`, `thm:duality_confinement:douglas-domination`; prose-names.md rows; mechanization-rebinding-policy.md DC rows 7, 8 (Douglas requires typed-cone encoding disclosure per audit §A1); audit_summary.md §A1 (Douglas `DouglasData` carrier representation note); proof-presentation-policy.md (`definition_entry` for the bridge; `lean_substantive` with typed-cone encoding caveat for Douglas); claim-revision-register.md R2 (Douglas wording); math-artifact §Domination; references-selection.md (descriptive prose for Douglas 1966; no `\cite{}` — deferred) | 2–3 pages |
| `sec:master_theorem` | `paper/duality_confinement/sections/sec_07_master_theorem.tex` | `sec:direct_confinement`, `sec:domination` | statements-of-record.yml row `thm:duality_confinement:master-theorem` (**HEADLINE**); prose-names.md row "duality-confinement membrane theorem"; mechanization-rebinding-policy.md DC row 9; proof-presentation-policy.md (`lean_substantive` wording "Lean proves the duality-confinement master theorem as `masterTheorem`; the typed-cone abstraction is disclosed inline"); claim-revision-register.md R1 (master-theorem mechanization at typed-cone level; operator-theoretic generality is open extension); R2 (typed-cone abstraction framing); math-artifact §MasterTheorem; cross-paper-boundary.md (sanctioned forward reference 2 of 2 — Paper 2 named as "the worked single-substrate validation", prose-only); figure-table-plan.md `fig:master-theorem-proof-shape` plan | 3–4 pages |
| `sec:exhaustive_squeeze_and_budgets` | `paper/duality_confinement/sections/sec_08_exhaustive_squeeze_and_budgets.tex` | `sec:master_theorem` | statements-of-record.yml rows `def:duality_confinement:exhaustive-moving-ledger`, `thm:duality_confinement:exhaustive-squeeze`, `def:duality_confinement:defected-budget` (support_only — no Lean citation), `prop:duality_confinement:optimized-trace-budget`; prose-names.md rows; mechanization-rebinding-policy.md DC rows 10, 11, 12, 13 (defected-budget carries no Lean citation; optimized-trace-budget uses "tracked by the formalization harness" wording with AM-GM disclosure); audit_summary.md §A2 (AM-GM as typed-Scalar axiom); proof-presentation-policy.md (3 distinct modes appear in this section: `lean_substantive` for exhaustive-squeeze; `definition_entry` no-Lean for defected-budget; "tracked by the harness" with AM-GM disclosure for optimized-trace-budget); claim-revision-register.md R4 (optimized-trace-budget AM-GM-as-axiom wording); math-artifact §ExhaustiveSqueeze + §DefectedBudget | 2–3 pages |
| `sec:scope` | `paper/duality_confinement/sections/sec_09_scope.tex` | `sec:master_theorem`, `sec:exhaustive_squeeze_and_budgets` | scope-fence.md (Paper 1 nonclaim rows: SDTC-as-named-not-derived; typed-cone abstraction vs operator-theoretic generality; AM-GM-as-axiom vs substantive derivation; cross-substrate predictions vs theorems; no novelty for classical constructions); claim-revision-register.md R1, R3, R5, R7 (all touching scope wording); anticipated-objections.md (Paper 1 objections requiring nonclaim discipline); out-of-scope-ledger.md (Paper 1 dropped material); no inventory rows resolved here (cross-references only) | 1–2 pages |
| `sec:discussion` | `paper/duality_confinement/sections/sec_10_discussion.tex` | `sec:scope` | anticipated-objections.md (Paper 1 objections — full set, prepared mitigation language); claim-revision-register.md R3, R6, R7, R8 (cross-substrate; Weil-positivity (Paper 2 material, omit here); cross-substrate predictions framing); cross-paper-boundary.md (forward to Paper 2 as worked single-substrate validation; PROSE-ONLY); references-selection.md (descriptive prose for classical operator-theoretic positioning — Reed–Simon, Bhatia, Horn–Johnson — no `\cite{}`); no inventory rows | 2–3 pages |
| `sec:conclusion` | `paper/duality_confinement/sections/sec_11_conclusion.tex` | `sec:discussion` | contract.md (thesis paragraph for restatement); out-of-scope-ledger.md (pending mechanization directions: operator-theoretic generality; substantive AM-GM); claim-revision-register.md R1, R4 (future-work framing); artifact-plan.md (reproducibility-statement note); cross-paper-boundary.md (final mention of Paper 2 as worked single-substrate validation; prose-only) | 1 page |
| `app:formalization` | `paper/duality_confinement/appendices/app_d_formalization.tex` | all body sections accepted | mechanization-rebinding-policy.md (canonical paper-side wording table to mirror as appendix wording-discipline summary); proof-presentation-policy.md (4-mode wording table — reproduce here as the canonical reference); statements-of-record.yml (all 13 DC rows for the per-row coverage table); statements-of-record.md (review-friendly rendering); prose-names.md (DC section — Lean decl ↔ paper-prose name); artifact-plan.md (Lean module path per row); audit_summary.md §A1 + §A2 (representation notes to document in the appendix); manifest `lean/manifests/duality_confinement_manifest.toml` (entries list); inventory `formalization/inventory/duality_confinement_paper_inventory.toml` (cross-reference); trust base `lean/manifests/trust_base.txt`; figure-table-plan.md `tab:formalization-coverage` plan | 4–6 pages |

## Float dispatches

Each float (figure or table) is its own dispatch. Schedule each
after the body section that depends on it but before the section-
level flow review of that section. Per
`feedback_table_typesetting.md`: redesign tables that overflow
rather than landscape them; long Lean identifiers in App D's
appendix mapping, not in body-table row labels.

Float candidates (per `paper/duality_confinement/notes/figure-table-plan.md`):

- `fig:involutive-ledger-schematic` — schematic of `(X, J, \mu, \psi, Y, J_{iso})` and `Fix(J)` (TikZ; after `sec:involutive_ledger`)
- `tab:involutive-ledger-examples` — examples table (after `sec:involutive_ledger`)
- `fig:master-theorem-proof-shape` — squeeze diagram (after `sec:master_theorem`)
- `tab:representation-notes` — audit §A1 + §A2 disclosures (in `sec:master_theorem` and `sec:exhaustive_squeeze_and_budgets`)
- `tab:nonclaims-grid` — nonclaims with required wording (in `sec:scope`)
- `tab:formalization-coverage` — 13-row coverage table (in `app:formalization`)

Each float dispatch consumes the planned artifact under
`paper/duality_confinement/{figures,tables}/`. As of prep-arc
close, those directories are empty (each has a README.md
placeholder pointing at the figure-table-plan); the actual
`.tex` files are created by codex during the float dispatches.

## Review cadence

- **Per-dispatch review** happens immediately after codex returns.
  Manager runs `make paper-preflight-duality_confinement`, reads
  the changed source, reads the resulting PDF for material prose
  change, applies the 8-criterion checklist
  (`feedback_paper_writing_role_split.md`).
- **Per-section flow review** happens after the last subsection of
  a section is drafted and accepted. May be a single codex task
  focused only on flow, transitions, internal consistency, and
  unresolved TODOs. It does NOT draft the next section. This is
  the ONE batching exception per `feedback_no_batching.md`.
- **Per-paper polish review** happens after the last body section
  and the appendix are drafted and accepted. Manager runs an
  end-to-end PDF read and dispatches one codex polish pass scoped
  to consistency, cross-references, theorem/proof presentation,
  and table/figure placement. Defects route back through codex via
  the same session (`feedback_paper_writing_role_split.md`).
- **Cross-paper review** is not in scope for this Paper-1 writing
  plan; it runs after Paper 2 also completes drafting per
  `paper/writing-plan.md` (cross-paper coherence pass).

## Per-paper polish discipline (Paper 1 close)

- Run `make paper-preflight-duality_confinement` and verify clean:
  no Underfull/Overfull, no Float-too-large, no Cref-Cref
  artifacts, no undefined references or citations.
- End-to-end PDF read by the manager: scan for dangling
  references, double-word `\Cref`, table overflow, appendix-form
  departures from foundations-paper convention, and academic-
  register slips (per `feedback_pdf_review_discipline.md`).
- Defects routed back through codex via the same session; no
  silent edits by the manager.
- After the polish pass: section labels are frozen (already locked
  at Phase 3 of the prep arc; polish re-confirms no drift).
- Reproducibility statement (single paragraph) populated in
  `sec:conclusion` or as the last paragraph of `sec:discussion`
  per `paper/duality_confinement/notes/artifact-plan.md`.

## Drafting order (Paper 1)

Per `paper/writing-plan.md` § "Sequential discipline (no
interleaving)":

1. Mode-swap dispatch (no body prose; codex acknowledges
   transition + lists locked section labels).
2. Body sections in document order: `sec:intro` →
   `sec:framework` → `sec:involutive_ledger` →
   `sec:anti_invariant_ledger` → `sec:direct_confinement` →
   `sec:domination` → `sec:master_theorem` →
   `sec:exhaustive_squeeze_and_budgets` → `sec:scope` →
   `sec:discussion` → `sec:conclusion`. Per-section flow review
   after each section's subsection dispatches close.
3. Title + abstract + keywords dispatch on `main.tex` (after all
   body sections accepted; per
   `paper/duality_confinement/notes/drafting-plan.md` dispatch 12).
4. Appendix `app:formalization` dispatches (A: wording-discipline
   summary + representation notes; B: per-row coverage table for
   13 inventory rows).
5. End-to-end polish dispatch (whole-paper consistency).
6. Final manager-side PDF read; defects route back via additional
   codex dispatches if needed.
7. Paper 1 closure: committed + pushed; `make
   paper-preflight-duality_confinement` clean; section labels
   frozen; submission/ deliverables populated per the per-axis
   drafting-plan.

After step 7 (Paper 1 reaches "Phase I.G closure" in the
cross-paper writing-plan's vocabulary), Paper 2 (RH) begins its
own mode-swap + drafting arc per
`paper/rh/notes/drafting-plan.md`. The two papers' drafting arcs
do NOT interleave.

## Status

This writing plan is the Phase 9 deliverable for Paper 1. Drafting
begins when the operator signals readiness. The mode-swap dispatch
to the codex thread is the first action of the drafting arc; this
file's per-section table is the take-home runbook for that arc.

## Pointers

- Cross-paper writing plan: `paper/writing-plan.md`
- Per-subsection drafting plan: `paper/duality_confinement/notes/drafting-plan.md`
- Section outline (label freeze):
  `paper/duality_confinement/notes/section-outline.md`
- Contract (thesis): `paper/duality_confinement/notes/contract.md`
- Claim-revision register:
  `paper/duality_confinement/notes/claim-revision-register.md`
- Artifact plan:
  `paper/duality_confinement/notes/artifact-plan.md`
- Notation workspace:
  `paper/duality_confinement/notes/notation.md`
- Figure/table plan:
  `paper/duality_confinement/notes/figure-table-plan.md`
- Math source-of-record:
  `anti_loc/extracted_math/duality_confinement_master.md`
- Audit summary (representation notes):
  `anti_loc/extracted_math/audit_summary.md`
- Sibling hiddenness writing plan (model):
  `/home/repos/six-birds-hiddenness/paper/writing-plan.md`
- Paper-writing memories:
  `~/.claude/projects/-home-repos-six-birds-duality-confinement/memory/`
