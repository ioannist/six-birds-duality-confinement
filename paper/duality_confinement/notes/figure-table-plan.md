# Figure and Table Plan: Duality Confinement (Paper 1)

Status: Phase I.A.2 produced 2026-05-23.

Purpose: plan the figures and tables ahead of drafting so the codex
dispatches building them have a definite spec. Each figure / table
is its own codex dispatch per `feedback_paper_writing_role_split.md`
(tables and figures count as separate subsection units).

## Tables

### tab:involutive-ledger-examples (suggested for §3 or §10)

- **Purpose**: ground the abstract involutive-object-ledger definition
  with concrete instances a working mathematician can recognize.
- **Columns**: Instance name | Carrier `X` | Involution `J` | Fixed locus | Anti-invariant readout `ψ_-`.
- **Rows**: (i) complex conjugation on ℂ (Fix = ℝ); (ii) the RH
  specialization with `J_L(s) = 1 - s̄` (Fix = critical line); (iii)
  a toy Hilbert-space example (involutive isometry on ℂ² with
  anti-invariant projector).
- **Notes**: tabularx with raggedright prose columns; `booktabs`
  rules per `feedback_table_typesetting.md`. Keep row labels short
  prose, not Lean identifiers.
- **Section anchor**: `\Cref{tab:involutive-ledger-examples}` in
  `sec:involutive_ledger`.

### tab:formalization-coverage (App D headline table)

- **Purpose**: per-row coverage table for all 13 DC inventory rows
  (12 mechanize_now + 1 support_only). The headline artifact of App D.
- **Columns**: Paper label | Paper-prose name | Lean module | Lean
  decl | Coverage mode | Disclosure wording.
- **Rows**: 13 rows mirroring
  `paper/notes/statements-of-record.yml` filtered for
  `target_paper = duality_confinement`.
- **Notes**: this is the long-identifier-tolerant table per
  `feedback_table_typesetting.md`; long Lean decl names live HERE
  rather than in any body-section table. `booktabs` rules; `tabularx`
  with two prose columns (Paper-prose name + Disclosure wording) and
  monospaced `\texttt{}` for the Lean decl column. Use `\small` or
  `\footnotesize`.
- **Section anchor**: `\Cref{tab:formalization-coverage}` in
  `app:formalization` (it is also referenced in
  `sec:scope` via `\Cref{app:formalization}` for the project-wide
  coverage summary).

### tab:representation-notes (App D companion)

- **Purpose**: document the three representation choices from
  `anti_loc/extracted_math/audit_summary.md` (§A1 Douglas encoding;
  §A2 AM-GM-as-axiom; §A3 real-part-type abstraction for RH).
- **Columns**: Representation note | Affected Lean entry | Encoding
  choice | Limitation | Path to substantive lift.
- **Rows**: 2 rows for DC paper (§A1 Douglas; §A2 AM-GM); §A3 is
  RH-paper content (cross-referenced only).
- **Notes**: `tabularx` with raggedright prose columns. Short prose
  labels, not Lean decl strings.
- **Section anchor**: `\Cref{tab:representation-notes}` in
  `app:formalization`.

### tab:nonclaims (suggested in §9 `sec:scope`)

- **Purpose**: render the scope-fence canonical-nonclaims table from
  `paper/notes/scope-fence.md` in body-prose form for the DC axis
  only.
- **Columns**: Nonclaim | Required wording | Where the discipline
  applies.
- **Rows**: 6–8 rows from the DC half of
  `paper/notes/scope-fence.md`.
- **Notes**: `tabularx` with three raggedright prose columns.
- **Section anchor**: `\Cref{tab:nonclaims}` in `sec:scope`.

## Figures

### fig:involutive-ledger-schematic (suggested for §3)

- **Purpose**: visual schematic of the involutive-object-ledger
  structure: the carrier `X`, the involution `J` as an arrow,
  the fixed locus highlighted, the readout `ψ` to the response
  space `Y` with the anti-invariant projection `P_-`.
- **Style**: TikZ commutative diagram OR an `\fbox`-style placeholder
  per the template's `figures/fig_01_template.tex` shape, drafted by
  codex during Phase I.D.
- **Section anchor**: `\Cref{fig:involutive-ledger-schematic}` in
  `sec:involutive_ledger`.

### fig:master-theorem-proof-shape (suggested for §7)

- **Purpose**: a small diagram showing the proof shape of the master
  theorem: monotonicity (`A_X ⪯ B_n`) → trace inequality
  (`tr A_X ≤ tr B_n`) → squeeze (`tr B_n → 0` ⟹ `tr A_X = 0`) →
  positivity (`A_X = 0`) → separation (`μ(X∖Fix(J)) = 0`).
- **Style**: simple flow diagram (TikZ or equivalent).
- **Section anchor**: `\Cref{fig:master-theorem-proof-shape}` in
  `sec:master_theorem`.

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
   exists; if it doesn't yet, the build will warn (not error) — the
   subsequent figure/table dispatch resolves it.

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
