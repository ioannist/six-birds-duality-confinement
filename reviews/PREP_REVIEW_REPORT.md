# Prep Review Report — six-birds-duality-confinement

## Verdict

REVISE

## Summary

The paper-prep arc is close: `make paper-preflight` is green; both
PDFs build to two-page scaffold PDFs; the section and App D appendix
files are TODO-only; the statements-of-record YAML validates at 24
rows; and the high-level contracts, scope fences, recognition-source
disclosures, and drafting-order discipline are mostly coherent.

I do not see evidence of body-prose drift in
`paper/duality_confinement/sections/*.tex`,
`paper/rh/sections/*.tex`, or the two App D files. The Lean/math state
is consumed as closed input and was not re-reviewed.

The prep arc should not start drafting yet. Several documents that
codex is instructed to read directly still contain stale or conflicting
instructions. These are not mechanization defects, but they can cause
undefined LaTeX macros, wrong citation behavior, wrong section routing,
or reuse of template tables with stale labels.

## Exit Criteria

1. **`make paper-preflight`: PASS.** It built both papers, ran
   `paper_lint.sh` on both, and passed
   `check_statements_of_record.py --check`,
   `check_manifests.py --check`, and `check_lean.py --skip-build`.
   The SoR validator reported 24 rows, manifest cross-check
   `duality_confinement=12, rh=10`, and inventory cross-check
   `duality_confinement=13, rh=11`.
2. **No body prose in section/App D skeletons: PASS.** The section
   files contain only comments, `\section`, `\label`, and TODO
   comments. App D files are likewise section-plus-TODO only; see
   `paper/duality_confinement/appendices/app_d_formalization.tex:14-19`
   and `paper/rh/appendices/app_d_formalization.tex:14-18`.
3. **Phase timestamps: PASS.** `paper/notes/prep-plan.md` has one
   `*Closed 2026-05-23.*` line for each of Phases 0-9
   (`paper/notes/prep-plan.md:166-592`).
4. **Lightweight cross-paper coherence: MIXED.** Both `main.tex`
   files use the shared `references.bib`, and the listed shared macros
   (`\Fix`, `\Pminus`, `\psim`, `\AX`, `\Kminus`, `\Jiso`, `\IOL`,
   `\GamSDTC`) render identically in the two macro files. The notation
   governance and drafting docs still disagree with those macro files;
   see Blocking Defect 1.

## Blocking Defects

1. **Notation docs instruct codex to use undefined or wrong macros.**

   Files:
   - `paper/duality_confinement/notes/notation.md:23-25`
   - `paper/duality_confinement/notes/notation.md:60-64`
   - `paper/rh/notes/notation.md:88-90`
   - `paper/notation_and_terminology.md:80`
   - `paper/duality_confinement/includes/paper_macros.tex:13-21`
   - `paper/rh/includes/paper_macros.tex:13,40-42`

   What is wrong: the actual macro files define `\psim` and `\trace`,
   but the DC notation workspace tells codex to use `\psiminus` and
   `\tr`, and its promotion list mentions nonexistent `\preceqDC` and
   `\trDC`. The shared notation file also lists `\tr` as the LaTeX
   macro for trace, while the macro audit and macro files use
   `\trace`.

   Fix: choose one trace macro convention before drafting. The least
   disruptive fix is to update all prep docs to say `\psim` and
   `\trace`, and delete `\preceqDC` / `\trDC` from the promotion list;
   alternatively define `\tr`, `\preceqDC`, and `\trDC` in both macro
   files and update the macro audit.

2. **`statements-of-record.md` is stale relative to the authoritative YAML.**

   Files:
   - `paper/notes/statements-of-record.yml:34-365`
   - `paper/notes/statements-of-record.md:37-79`

   What is wrong: the YAML uses final frozen section labels such as
   `sec:involutive_ledger`, `sec:master_theorem`, and
   `sec:landing_chain`. The review-friendly markdown still renders old
   module-style hints like `Involution`, `MasterTheorem`,
   `RecognitionSource`, `DCMasterApplied`, and `RHConditional`. This
   violates the Phase 2 claim that the markdown faithfully reflects the
   YAML and can misroute drafting review.

   Fix: regenerate or manually update `statements-of-record.md` from
   the YAML after Phase 8 label rewrites, preserving the 24-row counts
   and the support-only / recognition-source notes.

3. **Paper 1 cross-paper citation policy is internally contradictory.**

   Files:
   - `paper/notes/references-selection.md:18-26`
   - `paper/notes/cross-paper-boundary.md:108-118`
   - `paper/writing-plan.md:230-237`
   - `paper/duality_confinement/notes/drafting-plan.md:42-56`
   - `paper/duality_confinement/notes/claim-revision-register.md:261`
   - `paper/references.bib:37-41`

   What is wrong: `references-selection.md` lists
   `TsiokosRHviaSDTC2026` as a Paper 1 pick and counts Paper 1 at three
   Tsiokos references. `cross-paper-boundary.md` says the same key is
   the citation form for the two sanctioned forward references. But the
   writing plan, DC drafting plan, and claim-revision register all say
   Paper 1 must not use a `TsiokosRH*` bibkey. The review request's
   expected per-paper picks also list Paper 1 as Foundations II and
   Foundations III only.

   Fix: decide the rule. Recommended: keep `TsiokosRHviaSDTC2026` in
   the shared bibliography as an available sibling key, but remove it
   from Paper 1's active picks and update cross-boundary wording to say
   the two Paper 1 forward references are prose-only unless the manager
   explicitly enables the optional sibling citation. If the key should
   be cited, then update `writing-plan.md`, `drafting-plan.md`, and the
   claim-revision register to allow exactly those two exceptions.

4. **Figure/table template files are live stale templates, not
   TODO-only axis-specific placeholders.**

   Files:
   - `paper/duality_confinement/tables/tab_01_template.tex:1-19`
   - `paper/rh/tables/tab_01_template.tex:1-19`
   - same pattern in `tab_02_template.tex` through `tab_05_template.tex`
   - `paper/duality_confinement/figures/fig_01_template.tex:1-8`
   - `paper/rh/figures/fig_01_template.tex:1-8`

   What is wrong: the table templates contain live `table`
   environments, generic `TODO row` content, and stale series labels
   such as `subsec:inherited-state-table`,
   `subsec:constructed-object-table`, `subsec:closed-domain-summary`,
   `subsec:accepted-families-table`, and
   `subsec:final-claim-boundary`. The figure templates contain live
   figure environments with `Template figure caption.`. These files are
   not currently input by the papers, so preflight passes, but they are
   not the TODO-only, axis-specific placeholders requested by Phase 4.

   Fix: replace them with comment-only TODO stubs, or rename/rewrite
   them to the concrete planned artifacts in
   `figure-table-plan.md` (`tab:involutive-ledger-examples`,
   `tab:sat-sel-shell-fields`, `fig:landing-chain-diagram`, etc.) with
   no stale `subsec:*` labels.

5. **Some prep docs still point at nonexistent section labels.**

   Files:
   - `paper/notes/audience-translation.md:48`
   - `paper/notes/scope-fence.md:25-29`

   What is wrong: these rows route DC material to
   `sec:scope_and_discussion`, but the frozen DC labels are
   `sec:scope` and `sec:discussion` separately
   (`paper/duality_confinement/notes/section-outline.md:264-267`).

   Fix: split those destinations into `sec:scope` and/or
   `sec:discussion` consistently with the DC section outline.

## Non-Blocking Polish

- `scripts/check_statements_of_record.py:88-89` still uses the
  hiddenness-era comment example `Γ_{CSL-SAT-hidden}` for the
  `recognition_source` coverage mode. It does not affect validation,
  but should be renamed to the local `Γ_{SDTC-Selberg}` example.
- `paper/notes/preflight-signoff.md:109-112` says the actual table and
  figure `.tex` files are TODO-only. That is only true in the sense
  that they are not input yet; the files themselves contain live
  template floats. Update this after fixing Blocking Defect 4.

## Per-Phase Notes

- **Phase 0:** Asset audit accounts for 13 DC inventory rows, 11 RH
  rows, and the intentional dropped DC paper-prose row. Contracts are
  faithful to the conditional and typed-cone framing. Cross-paper
  boundary is structurally right but citation wording needs the fix
  above.
- **Phase 1:** Macro files themselves are consistent for the explicitly
  shared macros. The governance/workspace docs are not.
- **Phase 2:** YAML is valid and internally consistent; markdown
  rendering is stale.
- **Phase 3:** Section outlines and section skeleton labels line up;
  no body prose found.
- **Phase 4:** Figure/table plans are sensible and avoid long Lean
  identifiers in body tables. Template files need cleanup.
- **Phase 5:** `references.bib` contains only the four Tsiokos entries
  and no deferred classical bibkeys. The per-paper selection log needs
  citation-policy reconciliation.
- **Phase 6:** Audience translation, scope fence, objections, and proof
  policy cover the expected reviewer objections, including conditional
  RH, Weil-positivity relabeling, classical barriers, non-derivable
  `Γ`, and GRH. Section-label drift remains.
- **Phase 7:** Mechanization rebinding policy correctly distinguishes
  Lean-substantive rows, tracked-by-harness AM-GM, typed-cone Douglas,
  support-only defected budget, and typed-structure `GammaSdtcSelberg`.
  App D skeletons are TODO-only.
- **Phase 8:** Preflight wiring works as claimed.
- **Phase 9:** Sequential drafting discipline is clearly stated, and
  the per-axis drafting plans are detailed enough for codex dispatches
  once the blocking inconsistencies above are removed.

