# Paper-Writing Prep Arc Review Request — six-birds-duality-confinement

You are reviewing the paper-writing prep arc (Phases 0–9 of
`paper/notes/prep-plan.md`) at
`/home/repos/six-birds-duality-confinement`. The arc was claimed
closed 2026-05-23 and committed at `d7d0911`. It produced the
prep-workspace artifacts required before any body prose is drafted
for two papers (Duality Confinement / SDTC and RH closure via
SDTC-Selberg).

Your task is to spot-check the prep arc's deliverables for
**internal consistency**, **fidelity to the Lean mechanization
state and the math artifacts**, **scope discipline**, and
**readiness for sequential drafting**. You are **not** asked to
draft body prose, modify the Lean mechanization (which is closed
and out of scope for this review), or rewrite the math artifacts.

## Mode and what is NOT in scope

The repo is in **paper-writing mode**. The Lean mechanization arc
(Phases A–H of `PLAN_mechanization.md`) was closed 2026-05-23 and
reviewed externally (see `reviews/REVIEW_REQUEST_phaseG.md`); 22
manifest entries with full validator-chain green. **Do not** re-
review the Lean mechanization or the math extraction (Phases A–B).
Take the Lean state and math artifacts as inputs that the prep arc
consumes.

Specifically out of scope for this review:
- `lean/SixBirdsDualityConfinement/**` — Lean mechanization
- `anti_loc/extracted_math/**` — math source-of-record (audited
  separately)
- `lean/manifests/**` + `formalization/inventory/**` +
  `formalization/traceability/**` — mechanization bookkeeping
- `scripts/check_lean.py` + `scripts/check_manifests.py` +
  `scripts/audit_foundations_dependencies.py` +
  `scripts/check_foundations_provenance.py` +
  `scripts/check_semantic_alignment.py` — mechanization validators
- `vendor/foundations/**` — vendored upstream Foundations II/III

In scope for this review:
- `paper/notes/**` — cross-paper prep deliverables
- `paper/duality_confinement/notes/**` — DC-axis prep deliverables
- `paper/rh/notes/**` — RH-axis prep deliverables
- `paper/duality_confinement/sections/*.tex` +
  `paper/duality_confinement/appendices/*.tex` — TODO-only
  skeletons (verify they remain TODO-only)
- `paper/rh/sections/*.tex` + `paper/rh/appendices/*.tex` —
  TODO-only skeletons (verify they remain TODO-only)
- `paper/notation_and_terminology.md` — shared notation governance
- `paper/duality_confinement/includes/paper_macros.tex` +
  `paper/rh/includes/paper_macros.tex` — per-paper macros
- `paper/references.bib` — Tsiokos-only bibliography
- `paper/writing-plan.md` — manager runbook (Phase 9 deliverable)
- `paper/notes/prep-plan.md` — the runbook this arc executed
- `scripts/paper_lint.sh` + `scripts/check_statements_of_record.py`
  — paper-prep validators
- `Makefile` paper-* targets

## Context

The prep arc is modeled 1-to-1 on the sibling repo
`/home/repos/six-birds-hiddenness/paper/notes/prep-plan.md` (which
ran the same 10-phase shape successfully and produced two
companion papers `paper/hiddenness/` and `paper/pvnp/`). The
operator should compare structure where helpful but is not asked
to enforce strict mirroring.

Two papers are planned:
- **Paper 1 — Duality Confinement** (working title locked at
  Phase 0): *"Self-Dual Trace Confinement: A Six Birds Structural
  Law for Formed Closures Under Involutive Self-Duality"*. Headline:
  the duality-confinement membrane theorem. 13 inventory rows
  (12 mechanize_now + 1 support_only).
- **Paper 2 — Riemann Hypothesis (RH closure)** (working title
  locked at Phase 0): *"A Six Birds Closure of the Riemann
  Hypothesis via Self-Dual Trace Confinement on the Saturated
  Selberg Trace Layer"*. Headline: the conditional landing chain
  `Γ_{SDTC-Selberg} ⟹ RH`. 11 inventory rows (10 mechanize_now +
  1 recognition_source).

Total: 24 statements-of-record rows, all validated.

Cross-paper dependency: Paper 2 → Paper 1 (one-way). Paper 1 is
self-contained except for two sanctioned forward-reference
paragraphs (in `sec:involutive_ledger` and `sec:master_theorem`)
naming Paper 2 as "the worked single-substrate validation".

## Exit criteria (claimed met)

Verify each independently:

1. `make paper-preflight` — green for both papers.
   - Per-paper LaTeX build via `latexmk` produces `paper/<axis>/build/main.pdf`.
   - `scripts/paper_lint.sh paper/<axis>` passes (prose discipline
     + label consistency + build-log layout checks).
   - `scripts/check_statements_of_record.py --check` passes
     (24 rows; manifest cross-check matches `duality_confinement=12,
     rh=10`; inventory cross-check matches
     `duality_confinement=13, rh=11`).
   - `scripts/check_manifests.py --check` passes.
   - `scripts/check_lean.py --skip-build` passes.

2. **No body prose** in either paper's `sections/*.tex` or
   `appendices/*.tex`. Each section file should contain only:
   - A header comment block (paper name, scaffold note, "rows
     resolved here: ..." pointer).
   - `\section{...}` + `\label{sec:...}`.
   - A `% TODO: drafting populates this section ...` comment.
   - **No live `\subsection`**, no body sentences, no live
     `\input{...}` calls inside section files.

3. **Phase log timestamps**: every phase in
   `paper/notes/prep-plan.md` carries a `*Closed YYYY-MM-DD.*`
   line (10 phases × 1 timestamp each).

4. **Cross-paper coherence (lightweight)**:
   - Both papers' `main.tex` use shared `paper/references.bib`.
   - Shared macros (`\Fix`, `\Pminus`, `\psim`, `\AX`, `\Kminus`,
     `\Jiso`, `\IOL`, `\GamSDTC`) render identically across
     `paper/duality_confinement/includes/paper_macros.tex` and
     `paper/rh/includes/paper_macros.tex`.

## Specific items to review

### A. Phase 0 — Asset audit + per-paper contracts

Files:
- `paper/notes/phase0-asset-audit.md`
- `paper/duality_confinement/notes/contract.md`
- `paper/rh/notes/contract.md`
- `paper/notes/cross-paper-boundary.md`
- `paper/notes/out-of-scope-ledger.md`

Spot-check:

1. Does the asset audit enumerate every labeled item in both math
   artifacts (`anti_loc/extracted_math/duality_confinement_master.md`
   and `anti_loc/extracted_math/rh_construction.md`)? Cross-reference
   the inventory counts: DC has 13 inventory rows; RH has 11. The
   asset audit should account for all of them with classifications.

2. Are the per-paper contracts (Paper 1 and Paper 2) faithful to
   the proposals? Paper 1's thesis paragraph should match the
   `paper_proposal_self_dual_trace_confinement.md` framing; Paper
   2's should match `paper_proposal_rh_via_sdtc_selberg.md`.

3. Does `cross-paper-boundary.md` correctly identify the two
   sanctioned forward-reference paragraphs in Paper 1 (in
   `sec:involutive_ledger` and `sec:master_theorem`)? Is the
   one-way dependency rule (no `\Cref` from Paper 1 to Paper 2
   labels; no `TsiokosRH*` bibkey in Paper 1) clearly stated?

4. Does `out-of-scope-ledger.md` cover the claimed nonclaims for
   both axes (DC: operator-theoretic generality, cross-substrate
   theorems; RH: unconditional ZFC RH, classical-barrier
   circumvention, framework-derivable Γ, GRH)? Are any obviously
   missing?

### B. Phase 1 — Notation, macros, prose names

Files:
- `paper/notation_and_terminology.md`
- `paper/duality_confinement/includes/paper_macros.tex`
- `paper/rh/includes/paper_macros.tex`
- `paper/notes/macro-audit.md`
- `paper/notes/prose-names.md`

Spot-check:

1. Cross-paper notation consistency: shared symbols (`J`, `ψ_-`,
   `A_X`, `⪯`, `tr`, `Fix(J)`, `Γ`) defined identically in both
   per-paper `paper_macros.tex`? The macros pulling in the
   isometric involution `\Jiso` and the readout `\psim`?

2. `prose-names.md` should map each of the 22 manifest entries
   plus 2 carriers (the SDTC paper-prose name; `GammaSdtcSelberg`)
   to a paper-prose name. Verify a 1-to-1 mapping (no Lean decl
   appears twice; no paper-prose name maps to two different Lean
   decls).

3. Verify body prose will never need to embed Lean identifier
   strings (per `feedback_academic_register.md` from the
   memories): every Lean-cited statement has a paper-prose name
   to use instead.

### C. Phase 2 — Statements of record

Files:
- `paper/notes/statements-of-record.yml`
- `paper/notes/statements-of-record.md`

Spot-check:

1. `scripts/check_statements_of_record.py --check` passes:
   ```
   rows=24, target_paper={duality_confinement:13, rh:11, dropped:0},
   mechanized=23, not_mechanized=1; manifest cross-check matches;
   inventory cross-check matches
   ```

2. Every row's `target_section_hint` corresponds to a real section
   label in the respective paper's `paper/<axis>/sections/`. The
   label-consistency check in `scripts/paper_lint.sh` enforces
   this; verify it passes.

3. The 1 `not_mechanized` row is
   `def:duality_confinement:defected-budget` (support_only).
   Confirm.

4. The 1 `recognition_source` row is
   `obl:rh:gamma-sdtc-selberg`. Confirm.

5. `statements-of-record.md` (review-friendly rendering) faithfully
   reflects the yml.

### D. Phase 3 — Section outlines + label freeze

Files:
- `paper/duality_confinement/notes/section-outline.md` (11 body
  sections + 1 appendix)
- `paper/rh/notes/section-outline.md` (10 body sections + 1
  appendix)
- `paper/duality_confinement/sections/*.tex` (11 TODO-only
  skeletons)
- `paper/rh/sections/*.tex` (10 TODO-only skeletons)

Spot-check:

1. Every section in each outline maps to exactly one `.tex` file
   in the corresponding `sections/` directory with a matching
   label. Section labels frozen per the outline's "Section label
   freeze" block.

2. Each `.tex` skeleton contains no body prose, no live
   `\subsection`, no live `\input{...}`. (Per
   `feedback_no_batching.md`; per the hiddenness `PREP_REVIEW_REPORT`
   REJECT-then-iterate lesson.)

3. The per-section purpose statements in the outline are
   plausible — do they distribute the inventory rows across
   sections coherently? Specifically:
   - DC's `sec:master_theorem` should host the headline (the
     duality-confinement membrane theorem) and reference back to
     direct-confinement and domination.
   - RH's `sec:landing_chain` should host the headline (the
     conditional theorem `Γ_{SDTC-Selberg} ⟹ RH`) and reference
     back to translation theorem T and the recognition source.

4. Page budget plausibility: DC body ~21–25 pages; RH body ~21–28
   pages; per-paper App D ~4–6 pages.

### E. Phase 4 — Figure / table plans

Files:
- `paper/duality_confinement/notes/figure-table-plan.md`
- `paper/rh/notes/figure-table-plan.md`

Spot-check:

1. Every figure / table candidate has a clear purpose and target
   section. Per `feedback_table_typesetting.md`: long Lean
   identifiers should NOT appear in body-table row labels (they
   belong in the formalization appendix).

2. Per-paper `tables/` and `figures/` directories — confirm any
   placeholder `.tex` files are TODO-only and do not embed body
   prose.

### F. Phase 5 — Bibliography (Tsiokos-only, max 3 per paper)

Files:
- `paper/references.bib`
- `paper/notes/references-selection.md`

Spot-check:

1. Four Tsiokos entries: `TsiokosFoundationsII2026`,
   `TsiokosFoundationsIII2026`, `TsiokosSDTC2026` (sibling key for
   Paper 1, cited from Paper 2), `TsiokosRHviaSDTC2026` (sibling
   key for Paper 2, cited from Paper 1 only in sanctioned forward
   references if at all).

2. Per-paper picks documented:
   - DC (Paper 1): `TsiokosFoundationsII2026`,
     `TsiokosFoundationsIII2026`.
   - RH (Paper 2): `TsiokosSDTC2026`, `TsiokosFoundationsII2026`,
     `TsiokosFoundationsIII2026`.

3. External references explicitly deferred to the user's
   end-of-process pipeline (not pre-loaded into `references.bib`).

### G. Phase 6 — Audience translation, scope fence, objections, proof-presentation

Files:
- `paper/notes/audience-translation.md`
- `paper/notes/scope-fence.md`
- `paper/notes/anticipated-objections.md`
- `paper/notes/proof-presentation-policy.md`

Spot-check:

1. `audience-translation.md` covers every framework-native term
   that will appear in body prose. The reader-target is a working
   mathematician with no Six Birds background. Are translations
   plain enough? Concrete first examples present?

2. `scope-fence.md` matches `out-of-scope-ledger.md` (no drift).

3. `anticipated-objections.md` covers the predictable reviewer
   pushback for both papers. The conditional-theorem framing for
   RH ("isn't this just relabeled Weil positivity?",
   "classical-barrier circumvention?", "why isn't `Γ_{SDTC-Selberg}`
   derived?") should be addressed.

4. `proof-presentation-policy.md` defines the 4-mode wording
   table that body prose uses (per
   `feedback_lean_traceability_disclosure.md` memory):
   `lean_substantive` / `tracked by harness` / `typed-structure
   carrier` / no-mention. The policy should be self-contained.

### H. Phase 7 — Mechanization rebinding + App D skeletons

Files:
- `paper/notes/mechanization-rebinding-policy.md`
- `paper/duality_confinement/appendices/app_d_formalization.tex`
- `paper/rh/appendices/app_d_formalization.tex`

Spot-check:

1. The rebinding policy maps each of the 22 manifest entries +
   1 support_only + 1 recognition_source to a canonical paper-side
   wording mode. Critically:
   - The 12 DC theorems / definitions use `lean_substantive` or
     `definition_entry`.
   - The optimized-trace-budget row uses the "tracked by the
     formalization harness" wording with the AM-GM-as-typed-Scalar-
     axiom disclosure (audit_summary §A2).
   - The Douglas factorization row uses the typed-cone encoding
     disclosure (audit_summary §A1).
   - The `obl:rh:gamma-sdtc-selberg` row uses the typed-structure-
     carrier wording (NOT "Lean axiom" or "Lean proves"), with
     inline placement in `RHConditional.lean` noted per
     `lean/codex_kickoff.md` §12.
   - The `def:duality_confinement:defected-budget` row is
     support_only — body prose introduces it as motivation without
     claiming Lean coverage.

2. App D skeletons are TODO-only. No live tables; no body prose
   on the appendix beyond a `\section` + `\label` + TODO comment.

### I. Phase 8 — Build pipeline & preflight gate

Files:
- `Makefile` (paper-* targets)
- `scripts/paper_lint.sh`
- `scripts/check_statements_of_record.py`
- `paper/notes/preflight-signoff.md`

Spot-check:

1. `make paper-preflight` is wired correctly (the aggregate target
   runs both per-paper preflights plus the cross-paper validators).

2. `scripts/paper_lint.sh` enforces:
   - Forbidden body-prose tokens (Lean module identifier strings;
     JSON paths outside `\path{...}`; ticket-ID strings; all-caps
     verdict tokens).
   - Build-log layout checks (Overfull / Underfull / Float too
     large / undefined ref/cit / double-`\Cref` artifacts).
   - Label consistency (every `\label{sec:...}` either appears as
     a `target_section_hint` value in
     `paper/notes/statements-of-record.yml` OR the file has the
     magic phrase "statements-of-record rows resolved here: none").

3. The preflight-signoff.md tracks both papers' gate state with
   per-step PASS markers and explicit caveats (benign warnings).

### J. Phase 9 — Writing-plan runbook

Files:
- `paper/writing-plan.md`
- `paper/duality_confinement/notes/drafting-plan.md`
- `paper/rh/notes/drafting-plan.md`
- `paper/duality_confinement/notes/claim-revision-register.md`
- `paper/rh/notes/claim-revision-register.md`
- `paper/duality_confinement/notes/artifact-plan.md`
- `paper/rh/notes/artifact-plan.md`
- `paper/duality_confinement/notes/notation.md`
- `paper/rh/notes/notation.md`

Spot-check:

1. `writing-plan.md` enumerates every prep-arc input in the
   "Prep-arc inputs" table. Sequential discipline (Paper 1 first
   to Phase I.G closure, then Paper 2) is clearly stated. The
   mode-swap procedure (per axis) is fully scripted.

2. Per-axis `drafting-plan.md` files: subsection-granular dispatch
   tables for ~15 dispatches per paper (one codex turn each,
   per `feedback_no_batching.md`). Hard constraints per dispatch
   (cite restrictions, audience, register, Lean disclosure) are
   stated; the per-dispatch prompt template enumerates mandatory
   sources for codex to read.

3. Per-axis `claim-revision-register.md` files: every proposal
   claim whose wording was narrowed / refined / made-concrete by
   the mechanization is listed, with a "revised wording" the
   drafting dispatch quotes. Most-load-bearing revisions to check:
   - DC R1: master-theorem mechanization at typed positive-cone
     level (operator-theoretic generality is open extension).
   - DC R4: optimized-scalar-trace-budget AM-GM-as-axiom
     disclosure.
   - RH R1: conditional-theorem framing (the headline is
     conditional, not unconditional).
   - RH R2: `Γ_{SDTC-Selberg}` typed-structure-carrier encoding.
   - RH R4: real-part-type abstraction (audit §A3).

4. Per-axis `artifact-plan.md` files: every artifact body prose
   may need to cite has a canonical path. Long Lean identifiers
   live only in App D coverage tables, not body prose.

5. Per-axis `notation.md` workspaces: cross-paper consistency
   table (RH side) flags shared symbols that must render
   identically across both papers.

### K. Operational concerns

1. **No body prose drift.** Confirm no `.tex` file in
   `paper/<axis>/sections/` or `paper/<axis>/appendices/` has
   slipped body prose into it. Both PDFs build to ~2 pages each
   (just title/abstract scaffold + section headers).

2. **Phase-log timestamps.** Every phase in
   `paper/notes/prep-plan.md` carries a `*Closed YYYY-MM-DD.*`
   line. Verify all 10 phases (0–9) are timestamped.

3. **References hygiene.** `paper/references.bib` should not
   contain placeholder or fabricated bibkeys (e.g.,
   `RIEMANN1859` or `DOUGLAS1966` are explicitly deferred).

4. **Hidden coupling.** Are there any prep-arc artifacts that
   silently reference one another in a way that would make
   drafting brittle? (E.g., a claim-revision register row that
   refers to a section the outline doesn't have; or a
   rebinding-policy row that names a Lean decl not in the
   manifest.)

5. **Sequential drafting feasibility.** Could a working
   mathematician (the target reader, who is also the model for
   what codex needs to produce) draft Paper 1's intro from the
   prep-arc artifacts alone? Specifically: contract + section
   outline + audience translation + scope fence + claim revision
   register + drafting plan + writing plan + memory files. If
   any obvious input is missing, name it.

## Verdict format

Please produce a `reviews/PREP_REVIEW_REPORT.md` file at the repo
root with one of:

- **ACCEPT** — the prep arc is ready for sequential drafting.
  Cite the items you verified end-to-end and any minor cosmetic
  notes that do not block drafting.

- **REVISE** — the prep arc is mostly ready but has specific
  defects that should be fixed before drafting begins. List the
  defects as numbered items with: file path + line range, what's
  wrong, how to fix. Prefer concrete suggestions over
  open-ended critiques. Distinguish blocking defects (which
  prevent drafting from starting) from non-blocking polish.

- **REJECT** — the prep arc is unsound at the structural level.
  Explain the unsoundness; suggest which phases need to be re-run.

If you find issues that span multiple phases, group them under a
"Cross-phase concerns" heading.

Out-of-scope-for-this-review items (mechanization, math extraction,
foundations vendoring) should be ignored even if you notice
inconsistencies — flag them as informational notes only, not as
defects against the prep arc.

## Pointers

- Prep-plan runbook: `paper/notes/prep-plan.md`
- Writing-plan runbook (Phase 9 output): `paper/writing-plan.md`
- Prior external reviews (for tone/format reference):
  `reviews/REVIEW_REQUEST_phase0.md`,
  `reviews/REVIEW_REQUEST_phaseG.md`
- Sibling repo prep-arc model:
  `/home/repos/six-birds-hiddenness/paper/notes/prep-plan.md`
- Sibling repo prep-arc external review (for verdict-format
  reference): `/home/repos/six-birds-hiddenness/PREP_REVIEW_REPORT.md`
- Paper-writing memories (operational discipline):
  `~/.claude/projects/-home-repos-six-birds-duality-confinement/memory/`
- Commit at prep-arc close: `d7d0911` (`git show d7d0911 --stat`)
