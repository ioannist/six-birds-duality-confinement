# Figure and Table Plan: RH closure (Paper 2)

Status: Phase 4 produced 2026-05-23.

Purpose: plan the figures and tables ahead of drafting so the codex
dispatches building them have a definite spec. Each figure / table
is its own codex dispatch per `feedback_paper_writing_role_split.md`
(tables and figures count as separate subsection units).

## Tables

### tab:sat-sel-shell-fields (suggested for §4)

- **Purpose**: enumerate the 13 fields of `Sel^!_{ζ,tr}` with their
  paper-prose roles. Helps the reader navigate the typed shell.
- **Columns**: Field | Paper-prose name | Role in the construction.
- **Rows**: 13 rows for `H_L, I_tr, EQ_tr, EM_zero, Q_L, M_L, π_L,
  J_L, Λ_L, Z_nt, A_Z, Vis_L, Audit_L`.
- **Notes**: `tabularx` with raggedright prose columns; `booktabs`
  rules per `feedback_table_typesetting.md`. Short prose row
  labels, not Lean identifier strings.
- **Section anchor**: `\Cref{tab:sat-sel-shell-fields}` in
  `sec:sat_sel_shell`.

### tab:landing-chain (suggested for §7)

- **Purpose**: render the three-step conditional landing chain
  as a compact table for reader-orientation.
- **Columns**: Step | Premise | Conclusion | Lean realization.
- **Rows**: 3 rows for (i) extract domination records from
  `Γ_{SDTC-Selberg}`, (ii) apply `masterTheorem` from Paper 1
  [1] → `A_Z(ζ) = 0`, (iii) apply translation theorem T
  (forward) → `∀ρ, Re(ρ) = 1/2`.
- **Notes**: `tabularx`. Long Lean decl names go in App D, not
  this body table; the "Lean realization" column gives the
  paper-prose name + a short footnote referencing App D.
- **Section anchor**: `\Cref{tab:landing-chain}` in
  `sec:landing_chain`.

### tab:nonclaims (suggested in §8 `sec:scope_and_nonclaims`)

- **Purpose**: render the scope-fence canonical-nonclaims table
  from `paper/notes/scope-fence.md` in body-prose form for the RH
  axis only. Combines NC-1..NC-12 from the proposal with the
  shared / RH-specific scope-fence rows.
- **Columns**: Nonclaim | Required wording | Where the discipline
  applies.
- **Rows**: 8–10 rows from the RH half of
  `paper/notes/scope-fence.md` + NC-1..NC-12 condensed where
  needed.
- **Notes**: `tabularx` with three raggedright prose columns.
- **Section anchor**: `\Cref{tab:nonclaims}` in
  `sec:scope_and_nonclaims`.

### tab:six-gates (suggested in §8 or App D)

- **Purpose**: render the six no-smuggling gates + Gate 7 audit
  from proposal §B in compact body-prose form.
- **Columns**: Gate | What it checks | Verdict (PASS).
- **Rows**: 7 rows for Gate 1..Gate 7 with one-sentence
  descriptions and PASS verdicts.
- **Notes**: `tabularx`. Detail discussion in App D; body table
  is summary only.
- **Section anchor**: `\Cref{tab:six-gates}` in
  `sec:scope_and_nonclaims` with detail in `app:formalization`.

### tab:ns-pvnp-rh-parallel (suggested in §9 `sec:discussion`)

- **Purpose**: render the structural parallel between NS regularity,
  PvNP closure, and RH closure per proposal §8. Shows how all three
  Six Birds layer-level theorems use closure formation per
  Foundations I identically.
- **Columns**: Step | NS proof | PvNP closure | RH SDTC closure.
- **Rows**: ~6 rows for steps 1–6 of the proposal §8 table.
- **Notes**: `tabularx` with four raggedright prose columns;
  `\small` or `\footnotesize`. Short prose entries, not
  framework-internal vocabulary.
- **Section anchor**: `\Cref{tab:ns-pvnp-rh-parallel}` in
  `sec:discussion`.

### tab:formalization-coverage (App D headline table)

- **Purpose**: per-row coverage table for all 11 RH inventory rows
  (10 mechanize_now + 1 recognition_source). The headline artifact
  of App D.
- **Columns**: Paper label | Paper-prose name | Lean module | Lean
  decl | Coverage mode | Disclosure wording.
- **Rows**: 11 rows mirroring
  `paper/notes/statements-of-record.yml` filtered for
  `target_paper = rh`.
- **Notes**: this is the long-identifier-tolerant table per
  `feedback_table_typesetting.md`; long Lean decl names live HERE
  rather than in any body-section table. `booktabs` rules;
  `tabularx` with two prose columns (Paper-prose name + Disclosure
  wording) and monospaced `\texttt{}` for the Lean decl column.
  Use `\small` or `\footnotesize`.
- **Section anchor**: `\Cref{tab:formalization-coverage}` in
  `app:formalization`.

### tab:representation-notes (App D companion)

- **Purpose**: document the representation choice from
  `anti_loc/extracted_math/audit_summary.md` §A3 (real-part-type
  abstraction for RH). The §A1 and §A2 notes are Paper-1
  responsibility; Paper 2 cross-references Paper 1's App D.
- **Columns**: Representation note | Affected Lean entry | Encoding
  choice | Limitation | Path to substantive lift.
- **Rows**: 1 row for §A3 (real-part-type abstraction for the RH
  zero ledger) + 1 row noting the `GammaSdtcSelberg` typed-carrier
  encoding choice.
- **Notes**: `tabularx` with raggedright prose columns.
- **Section anchor**: `\Cref{tab:representation-notes}` in
  `app:formalization`.

## Figures

### fig:landing-chain-diagram (suggested for §7)

- **Purpose**: visual flow diagram of the conditional landing
  chain: `Γ_{SDTC-Selberg}` (typed carrier) → extract domination
  records → master theorem [1] → `A_Z(ζ) = 0` → translation T
  forward → `∀ρ ∈ Z_ζ^{nt}, Re(ρ) = 1/2` (RH on the typed zero
  ledger).
- **Style**: simple TikZ flow diagram (5 boxes with arrows).
- **Section anchor**: `\Cref{fig:landing-chain-diagram}` in
  `sec:landing_chain`.

### fig:sat-sel-shell-schematic (suggested for §4)

- **Purpose**: visual schematic of `Sel^!_{ζ,tr}`'s 13-field
  structure. Groups the fields by role (history layer; instrument
  + observable family; quotients + comparison map; involution +
  completed L + zero ledger + anti-invariant ledger; visibility +
  audit).
- **Style**: TikZ box diagram OR an `\fbox`-style placeholder per
  the template's `figures/fig_NN_template.tex` shape.
- **Section anchor**: `\Cref{fig:sat-sel-shell-schematic}` in
  `sec:sat_sel_shell`.

## Per-figure / per-table dispatch convention

Per `feedback_paper_writing_role_split.md`, each figure and each
table is its OWN codex dispatch (not bundled with body prose).

When drafting a section that includes a figure or table, the
sequence is:
1. Dispatch body prose for the section (one dispatch per subsection).
2. Dispatch the figure / table as a SEPARATE dispatch (using the
   `figures/fig_NN_*.tex` or `tables/tab_NN_*.tex` template files).
3. The body prose dispatch may include `\input{figures/fig_NN_*}` or
   `\input{tables/tab_NN_*}` calls assuming the figure/table file
   exists; if it doesn't yet, the build will warn (not error) —
   the subsequent figure/table dispatch resolves it.

Manager order: typically body-prose first (so the codex turn that
writes the body knows where the figure / table is referenced); then
the figure / table dispatch (which can use the body context for
caption alignment).

## Convention reminders

- `booktabs` rules only (`\toprule` / `\midrule` / `\bottomrule`); no
  vertical rules per `feedback_table_typesetting.md`.
- `tabularx` with `>{\raggedright\arraybackslash}` for prose columns.
- `\small` or `\footnotesize` for dense tables.
- Long Lean decl strings ONLY in `app:formalization` tables; never
  in body-section table row labels.
- Captions: short, descriptive; the in-body referent must use
  `\Cref{tab:...}` or `\Cref{fig:...}`.
