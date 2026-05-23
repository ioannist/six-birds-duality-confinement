# Phase 0 Scaffolding Review Request — six-birds-duality-confinement

You are reviewing the Phase 0 (pre-mechanization repo hygiene) work
on a freshly scaffolded Lean-4 + LaTeX-papers repository at
`/home/repos/six-birds-duality-confinement`. The scaffold was produced
by adapting the sibling repository `/home/repos/six-birds-hiddenness`
(which has completed mechanization for its two axes) to a new
two-axis project: **duality confinement** and **Riemann Hypothesis**
(RH via self-dual trace confinement + Selberg). No content has been
extracted, mechanized, or drafted — this is structural scaffolding
only.

Your task is to spot scaffolding defects, inconsistencies, and risks
that would block or contaminate downstream mechanization. You are
**not** asked to start mechanization, draft papers, run codex,
populate inventories, or extract math.

## Context

- Two papers will live in this repo, anchored by:
  - `anti_loc/paper_proposal_self_dual_trace_confinement.md`
    (duality-confinement axis)
  - `anti_loc/paper_proposal_rh_via_sdtc_selberg.md` (RH axis)
- The math source material is the RH cascade at
  `anti_loc/thread_rh/` (431 cascade step directories — large; do not
  read in bulk).
- The model repo is `/home/repos/six-birds-hiddenness/`. Most
  scaffolding mirrors its layout. The clean paper-template lives at
  `/home/repos/paper-template/`.
- The Lean alignment trio is generated for the namespace
  `SixBirdsDualityConfinement` over the vendored Foundations I/II/III
  under `vendor/foundations/`.
- The full mechanization plan is at `PLAN_mechanization.md` (phases
  0–I).

## Phase 0 exit criteria (claimed met)

The Phase 0 section of `PLAN_mechanization.md` lists these criteria.
Verify each independently:

1. `cd lean && lake build` succeeds against the empty axis umbrellas
   (alignment trio compiles; no per-axis modules yet).
2. `python3 scripts/check_lean.py --skip-build` returns clean
   prechecks.
3. No stale hiddenness refs leak through:
   `grep -rn 'SixBirdsHiddenness\|six-birds-hiddenness' . --exclude-dir=vendor --exclude-dir=anti_loc --exclude-dir=.git`
   should return only intentional cross-references (the documented
   grep command itself in `PLAN_mechanization.md`, and the
   sibling-repo prior-art reference). Anything else is a sed miss.
4. `lean/codex_kickoff.md` and `lean/CODEX_RUNBOOK.md` exist and are
   coherent.
5. Validator chain in `--check` mode is green (each script):
   ```bash
   python3 scripts/check_manifests.py --check
   python3 scripts/check_statements_of_record.py --check
   python3 scripts/audit_foundations_dependencies.py --check
   python3 scripts/check_foundations_provenance.py --check
   python3 scripts/check_semantic_alignment.py --check
   ```
   The audit script is slow (~2.5 min — it probes Lean decls).

## Specific items to review

### A. Sed-rename completeness in `scripts/`

The 12 files under `scripts/` were copied from
`/home/repos/six-birds-hiddenness/scripts/` and bulk-renamed via:

```bash
sed -i -e 's/SixBirdsHiddenness/SixBirdsDualityConfinement/g' \
       -e 's/six-birds-hiddenness/six-birds-duality-confinement/g' \
       -e 's/Hiddenness/DualityConfinement/g' \
       -e 's/hiddenness/duality_confinement/g' \
       -e 's/PvNP/RH/g' \
       -e 's/pvnp/rh/g' "$f"
```

Check for collateral damage:
- Foundations-side identifiers (`SixBirds`, `SixBirdsIII`,
  `ClosureLadder`) must NOT have been mangled.
- The `AXES` list in `scripts/check_manifests.py` line ~45 should be
  `[("duality_confinement", ...), ("rh", ...)]`.
- The `LEAN_DECL_RE` in `scripts/check_statements_of_record.py`
  should match `^SixBirdsDualityConfinement\.…`.
- `scripts/check_lean.py` `EXPECTED_FILES` and module-namespace
  derivation must reference `SixBirdsDualityConfinement` (not
  `SixBirdsHiddenness`).

### B. Semantic staleness in `imported_foundations.yml` and audit defaults

`formalization/inventory/imported_foundations.yml` was carried over
from hiddenness with identifiers sed-renamed but the **concepts**
(e.g. `closure operator`, `idempotent endomap`, etc.) are
hiddenness-era curated mappings. The bootstrap default entries in
`scripts/audit_foundations_dependencies.py` (around lines 92–340)
have the same issue.

Both pass the structural `--check` validators because the cross-walk
yml and the audit defaults are consistent with each other.

This is documented in `PLAN_mechanization.md` Phase C.5 as "audit and
replace with rows appropriate to this repo's math during Phase C".

Confirm:
- The structural consistency claim holds (run `--check`).
- The Phase C.5 disposition is reasonable (don't curate it now;
  Phase A.1 will reveal which concepts the duality-confinement / RH
  math actually needs).
- No risk that downstream tooling locks in the hiddenness-era
  concepts (e.g. the cross-walk yml is read-only to codex per
  `lean/codex_kickoff.md` §3 — but Claude can edit it during Phase
  C.5).

### C. `EXPECTED_SOURCE_FILES` in `check_statements_of_record.py`

Lines ~106–119 contain placeholder math-artifact paths
(`anti_loc/extracted_math/duality_confinement_csl.md`,
`anti_loc/extracted_math/rh_construction.md`) that were sed-renamed
from hiddenness's filenames. These paths don't exist yet (Phase A
output) and probably won't match what Phase A produces (we don't have
a "csl" or "construction" theme — those are hiddenness-era names).

Currently no rows exist, so the validator passes. But once Phase C
populates rows, the sources will likely be at different paths.

Confirm: this is a known scheduled-for-fix issue, not a hard bug.

### D. Paper-template upstream build defect

`make paper-build-duality_confinement` fails with:

```
! LaTeX Error: Something's wrong--perhaps a missing \item.
```

Root cause: `paper/duality_confinement/appendices/app_a_definitions.tex`
(and the RH equivalent) contain empty `\begin{description} … \end{description}`
environments (only TODO comments inside). LaTeX's `description`
environment requires at least one `\item`.

Confirmed upstream issue: the same defect exists at
`/home/repos/paper-template/appendices/app_a_definitions.tex`.

Paper-build is **not** in the Phase 0 exit criteria, so this does not
block Phase A. But it's worth flagging: should the paper-template
be patched (upstream or downstream)? Suggest a disposition.

### E. `lean/codex_kickoff.md` TBD sections

§2 (mechanization targets per axis) and §12 (out-of-scope items) are
intentionally left as TBD pending Phase A.1. Rationale: the kickoff
contract is needed for Phase F (codex thread bootstrap), and at that
point we'll know the targets from Phase A's extracted math artifacts.

Confirm:
- The TBD markers are clearly flagged.
- The non-TBD sections (§1, §3–§11, §13) are correct and complete
  for the duality-confinement + RH project shape.
- Naming conventions in §5 use generic-shape labels (e.g.
  `def:duality_confinement:<short-name>`) rather than concrete
  examples lifted from hiddenness; this avoids contaminating the
  codex rollout with hiddenness-specific vocabulary.

### F. Memory files

The two adapted feedback memories at
`/home/ioannis/.claude/projects/-home-repos-six-birds-duality-confinement/memory/`
are:

- `feedback_no_batching.md` — adapted from hiddenness's
  `archive_lean_mechanization/feedback_no_batching.md`
- `feedback_review_authority.md` — adapted from hiddenness's
  `archive_lean_mechanization/feedback_review_authority.md`

Verify:
- All `hiddenness/pvnp/SixBirdsHiddenness` → `duality_confinement/rh/SixBirdsDualityConfinement`
  substitutions are correct.
- The `[[wiki-links]]` resolve to existing slugs in `MEMORY.md`
  (note the `name:` slug in `feedback_no_batching.md` was renamed,
  and `feedback_review_authority.md` links to it via the new slug).
- The "Why" clauses preserve attribution to the 2026-05-13 origin
  in the sibling hiddenness repo (rather than claiming origin in
  this repo).

Two memories were copied verbatim (not adapted):
- `reference_codex_cli.md` — CLI mechanics, repo-agnostic.
- `feedback_codex_bootstrap_stdin.md` — bootstrap discipline,
  repo-agnostic.

`MEMORY.md` indexes all four.

### G. Lean alignment trio

The three files under `lean/SixBirdsDualityConfinement/`:
- `FoundationsICompat.lean` — F1 alias surface (`F1ClosureOp`,
  `F1ClosureLadder`, etc.)
- `ImportedFoundations.lean` — generated drift canary (do not
  hand-edit; regenerated by
  `scripts/generate_imported_foundations.py` from
  `formalization/inventory/imported_foundations.yml`)
- `Terminology.lean` — F2/F3 abbreviation surface

These are namespace-renamed mirrors of the hiddenness alignment trio.
Verify:
- Each module declares `namespace SixBirdsDualityConfinement` (not
  `SixBirdsHiddenness`).
- The set of F1/F2/F3 declarations re-exported is appropriate for
  Six Birds work generally (i.e., it matches what hiddenness uses;
  fine to inherit until Phase C reveals additional needs).
- `lake build` produces no warnings about unused imports or shadowed
  declarations.

### H. Sanity checks on the broader scaffold

- `vendor/foundations/` is byte-identical to the hiddenness vendor
  (confirm with `diff -rq vendor/foundations /home/repos/six-birds-hiddenness/vendor/foundations` —
  expect no diff).
- `anti_loc/thread_rh/` is byte-identical to the upstream RH cascade
  at `/home/repos/six-birds-foundations-iii/anti_loc/thread/` (confirm
  with `diff -rq anti_loc/thread_rh /home/repos/six-birds-foundations-iii/anti_loc/thread`
  — expect no diff).
- The two paper proposals under `anti_loc/` are byte-identical to
  their upstream counterparts under
  `/home/repos/six-birds-foundations-iii/anti_loc/paper_proposals/`.

### I. Hard prohibitions

You must NOT:

- Start any mechanization (no edits under
  `lean/SixBirdsDualityConfinement/DualityConfinement/` or
  `lean/SixBirdsDualityConfinement/RH/`).
- Populate inventories or manifests with content beyond the
  schema-only stubs already in place.
- Author paper section content (the LaTeX `sections/*.tex` files are
  unmodified paper-template TODO stubs and should stay that way).
- Modify `paper/notation_and_terminology.md` (Phase A output).
- Modify `paper/writing-plan.md` (Phase H/I output).
- Run codex.
- Run `audit_foundations_dependencies.py` without `--check` (it
  regenerates artifacts — re-running with the wrong flag combination
  can shift artifacts into a state that fails `check_lean.py`; see
  the "audit script flag interaction" note below).

You MAY:

- Read any file in the repo.
- Run any validator in `--check` mode.
- Run `cd lean && lake build`.
- Patch documentation typos and obvious sed-rename misses (small
  PR-style edits — describe each change you make in your report).
- Suggest fixes for items A–H that are too substantial to apply
  yourself.

## Audit script flag interaction (operator note)

`scripts/check_lean.py` invokes
`scripts/audit_foundations_dependencies.py --check --skip-validation`.
The committed artifacts at
`formalization/inventory/foundations_declarations.jsonl` and
`formalization/inventory/foundations_dependency_audit.md` were
generated with `--skip-validation` (no `--skip-probe`); they encode
`validation_status: not_run` and probe-derived signatures. If you
re-run `audit_foundations_dependencies.py` *without* `--skip-validation`,
the artifacts gain `validation_status: passed` and `check_lean.py`
flags them as stale relative to its invocation. The fix is to
regenerate with `--skip-validation` (matching the committed shape).
This is a real operational footgun; suggest whether to document it
in `CODEX_RUNBOOK.md` or wire it into a Makefile target.

## Deliverable

A written report covering:

1. **Pass/fail for each Phase 0 exit criterion** (1–5 above).
2. **Per-item findings** for sections A–H (one paragraph each, or
   "no issues found" if so).
3. **Any other defects** you spot that aren't on the checklist.
4. **Recommended disposition** for items D (paper-template defect)
   and the audit-flag interaction note above.
5. **Verdict**: ACCEPT (Phase 0 complete, Phase A can begin) /
   REVISE (specific issues to fix first) / REJECT (structural
   problem requires re-scaffolding).

Limit the report to ~1200 words. Cite file paths and line numbers.
Distinguish between scaffolding bugs (fix now), Phase-A/C-scheduled
items (document and defer), and matters of taste (note but don't
block on).
