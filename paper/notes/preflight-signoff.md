# Preflight Sign-off — Pre-Drafting Gate

Status: Phase 8 produced 2026-05-23.

Purpose: record the pre-drafting `make paper-preflight` gate state
for both papers. This sign-off marks the transition from
prep-phase (Phases 0–8) into the writing-plan runbook (Phase 9).

The preflight gate is the canonical check that the per-paper
infrastructure (build, lint, validators, label consistency) is
sound BEFORE any body prose is drafted. Re-run after every
drafting dispatch; failures route back through the per-axis codex
thread per `paper/writing-plan.md` and the per-axis drafting-plan.

## Gate definition

`make paper-preflight` runs (in order):

1. `make paper-build-duality_confinement` — `latexmk` builds Paper
   1's `main.tex` into `paper/duality_confinement/build/main.pdf`.
2. `scripts/paper_lint.sh paper/duality_confinement` — runs prose
   discipline checks (forbidden Lean-module identifiers in body
   prose; forbidden JSON-path mentions outside `\path{...}`;
   forbidden ticket-ID strings; forbidden all-caps verdict tokens),
   build-log layout checks (undefined references / citations;
   overfull hbox; float-too-large; double-word cleveref artifacts),
   and label consistency (every `\label{sec:...}` in a section file
   must either be a `target_section_hint` value in
   `paper/notes/statements-of-record.yml` OR the file must carry
   the magic phrase "statements-of-record rows resolved here:
   none").
3. Build-log scan in the Makefile recipe for `Underfull`, `Overfull`,
   `Float too large`, undefined-reference / undefined-citation
   warnings, and double-`\Cref` artifacts.
4. Same three steps for Paper 2 (RH) via
   `make paper-preflight-rh`.
5. `python3 scripts/check_statements_of_record.py --check` —
   schema + cross-check against per-axis manifest and per-axis
   inventory.
6. `python3 scripts/check_manifests.py --check` — per-axis manifest
   entry counts; trust-base axiom count; section_module_map coverage.
7. `python3 scripts/check_lean.py --skip-build` — Lean prechecks
   (without re-running `lake build`; the Lean build is governed by
   the mechanization arc, not the prep arc).

## Sign-off — 2026-05-23

| Step | Status |
| --- | --- |
| `paper-build-duality_confinement` | PASS — `paper/duality_confinement/build/main.pdf` (2 pages, 133654 bytes) |
| `paper_lint.sh paper/duality_confinement` | PASS |
| DC build-log scan | PASS — no Underfull/Overfull/Float-too-large/undefined-ref/undefined-cit/double-Cref artifacts |
| `paper-build-rh` | PASS — `paper/rh/build/main.pdf` builds clean |
| `paper_lint.sh paper/rh` | PASS |
| RH build-log scan | PASS |
| `check_statements_of_record.py --check` | PASS — `rows=24, target_paper={duality_confinement:13, rh:11, dropped:0}, mechanized=23, not_mechanized=1; manifest cross-check matches; inventory cross-check matches` |
| `check_manifests.py --check` | PASS — `duality_confinement=12 entries, rh=10 entries, trust_base=5 axioms, section_module_map covers every queued section` |
| `check_lean.py --skip-build` | PASS — `duality_confinement Lean prechecks passed` |

Aggregate `make paper-preflight`: **PASS**.

## Caveats

These notes record adjustments made to clear the gate; they are
not failures of the prep arc.

1. **Label consistency adjustment.** The pre-Phase-8 section-label
   restructuring (Phase 3) renamed section labels from CamelCase
   Lean-module values (e.g. `MasterTheorem`) to snake-case section
   labels (e.g. `sec:master_theorem`); Phase 8 updated all 24
   `target_section_hint` values in `paper/notes/statements-of-record.yml`
   to match the new section labels.
2. **Non-hosting section files.** The five framing / discussion
   / conclusion section files per paper (intro, framework, scope /
   scope_and_nonclaims, discussion, conclusion) carry the magic
   phrase "statements-of-record rows resolved here: none" in the
   header comment, signalling the label-consistency check that
   these labels do not appear as `target_section_hint` values and
   should not fail the check.
3. **`Underfull \hbox` warnings.** The lint script issues these as
   `WARN`, not as failures. As of 2026-05-23 sign-off, no Underfull
   hits appear in either paper's build log; the rule will become
   relevant once body prose is drafted.
4. **bibliography warnings.** `latexmk` emits "Empty
   'thebibliography' environment" because no `\cite` exists yet in
   either paper (sections are TODO-only). This is benign in the
   prep arc and disappears once body prose with citations is
   drafted.
5. **`Unused \captionsetup` warnings.** The `caption` package
   warns about unused captionsetup directives for `table` /
   `figure` / `algorithm` because no tables / figures / algorithms
   appear in the current TODO-only build. Benign; disappears once
   floats appear during drafting.
6. **Lean prechecks scope.** `check_lean.py --skip-build` runs the
   Lean-side precheck logic without re-running `lake build`; the
   full Lean build closure was established at Phase H of
   `PLAN_mechanization.md` (closed 2026-05-23). Re-running the
   build is out of scope for the paper-prep arc.

## What this sign-off does NOT certify

- That body prose exists. It does not; sections are TODO-only
  skeletons per the no-body-prose constraint of the prep arc.
- That the PDF is reviewer-ready. It is not; the current PDFs are
  build smoke-tests confirming the scaffolding compiles.
- That cross-paper coherence has been audited. Cross-paper coherence
  is a Phase-I.F task in `paper/writing-plan.md`; it runs only
  after both papers have completed their drafting closure.
- That figures / tables are populated. The figure-table-plan
  artifacts (`paper/<axis>/notes/figure-table-plan.md`) catalogue
  what is needed; the per-paper `tables/` and `figures/`
  directories are empty (each carries a README.md placeholder
  pointing at the plan). Concrete table / figure `.tex` files are
  created during the drafting arc, one per dispatch.

## Re-running the gate

The gate is idempotent. To re-run:

```
make paper-preflight
```

To re-run only one paper:

```
make paper-preflight-duality_confinement
make paper-preflight-rh
```

To re-run only the cross-paper validators (skip rebuild):

```
python3 scripts/check_statements_of_record.py --check
python3 scripts/check_manifests.py --check
python3 scripts/check_lean.py --skip-build
```

After every drafting dispatch (under the future writing arc),
re-run `make paper-preflight-<axis>` for the affected paper. Any
new failures must be routed back through the per-axis codex thread
per `paper/writing-plan.md`.

## Pointers

- Top-level target driver: `Makefile`
- Prose lint script: `scripts/paper_lint.sh`
- Statements-of-record validator: `scripts/check_statements_of_record.py`
- Manifest validator: `scripts/check_manifests.py`
- Lean precheck driver: `scripts/check_lean.py`
- Per-paper build directory: `paper/<axis>/build/`
- Statements-of-record (data): `paper/notes/statements-of-record.yml`
- Per-paper section outlines (label freezes):
  `paper/duality_confinement/notes/section-outline.md`,
  `paper/rh/notes/section-outline.md`
