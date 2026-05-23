# Mechanization Plan — Duality Confinement + RH

Working plan for Lean-4 mechanization of the two papers in this repo.
Maintained as a stable reference document; safe to consult after
context compression.

## Cascade situation

The math for both axes traces back to cascade step files under
`anti_loc/thread_rh/steps/` (431 steps). It has **not been
consolidated** into a working math artifact. The anchor proposals are:

- **Duality confinement** —
  `anti_loc/paper_proposal_self_dual_trace_confinement.md`
- **RH (via SDTC + Selberg)** —
  `anti_loc/paper_proposal_rh_via_sdtc_selberg.md`

Each proposal cites specific cascade steps. The exact step ranges per
axis are unknown until Phase A.1 walks the proposals and produces the
dependency map.

This mirrors the situation in the sibling `six-birds-hiddenness` repo:
the cascade has produced step content but no consolidated math
artifact yet. (Contrast with the needles project, which inherited
consolidated manuscript files from its cascade.)

## Workflow (corrected order)

1. **Extract** math content from the relevant step files.
2. **Consolidate** per axis into a working math artifact in dependency
   order, every claim labeled.
3. **Confirm** the math (Claude review, gap audit).
4. **Mechanize** via codex per the strict protocol.
5. **Paper writing** (publication-grade exposition) is downstream of
   mechanization. Not a prerequisite. Out of scope for this plan
   until 4 completes.

## Mechanization targets

Per the proposals in `anti_loc/` (TBD — Phase A.1 produces the
authoritative target list per axis):

- **Duality-confinement axis**
  (`paper_proposal_self_dual_trace_confinement.md`): TBD.
- **RH axis** (`paper_proposal_rh_via_sdtc_selberg.md`): TBD.
- **Explicitly out of scope for Lean**: any structural recognition
  source identified during Phase A. Record in inventory with
  `intended_status = out_of_scope_recognition_source`; do not encode
  as Lean `axiom`.

## Operating constraints (from memory)

These are absolute. See
`~/.claude/projects/-home-repos-six-birds-duality-confinement/memory/`.

1. **Strict protocol** (`feedback_no_batching.md`): codex writes Lean,
   Claude orchestrates and reviews. One subsection per codex dispatch,
   one review pass per subsection, in document order. No batching, no
   Claude Code sub-agents. Per-axis codex sessions. Violation triggers
   delete-and-restart.
2. **Review authority** (`feedback_review_authority.md`): Claude
   unilaterally accepts/rejects/iterates. Bar = at least one non-`rfl`
   mathematical step per theorem; reject projection-packaged
   tautologies.
3. **Codex mechanics**
   (`reference_codex_cli.md`, `feedback_codex_bootstrap_stdin.md`):
   resume by UUID only; stdin redirection for the multi-KB kickoff
   bootstrap; argv fine on resumes.

## Role split

- **Codex** (OpenAI `codex` CLI) writes the Lean. Never Claude.
- **Codex may also assist with extraction/consolidation** (steps 1–2
  above) under a separate session — driven by Claude, not the
  mechanization session. The strict protocol governs the
  *mechanization* session; extraction can be more flexible. (See
  Phase A.4 below.)
- **Claude** does Phase 0 hygiene, drives extraction and consolidation,
  audits the consolidated math, builds inventories/queues, dispatches
  codex per-subsection during Phase G, runs validators, reviews
  substance, accepts or sends fix prompts.

## Per-axis codex sessions

- Duality-confinement mechanization session →
  `lean/.codex_thread_id_duality_confinement`
- RH mechanization session → `lean/.codex_thread_id_rh`

Never cross-resume between axes. Each rollout learns its paper's
vocabulary; mixing contaminates.

If a separate extraction session is used, store its UUID elsewhere
(e.g. `anti_loc/.codex_thread_id_extraction_<axis>`). Do not reuse the
mechanization thread UUID for extraction work.

---

## Phase 0 — Pre-mechanization repo hygiene

Goal: empty-but-rebranded skeleton `lake build`s clean;
manifests/inventory/queues stripped to schema headers; scripts adapted
to duality-confinement/rh vocabulary; root-level docs written.

Status: **complete** (2026-05-23). All Phase 0 exit criteria met
(see Status section below for the smoke-test results).

## Phase A — Math extraction & consolidation (Claude-driven, optional codex extraction subtasks)

Goal: produce per-axis working math artifacts at
`anti_loc/extracted_math/duality_confinement_*.md` and
`anti_loc/extracted_math/rh_*.md`. Each contains every definition,
hypothesis, lemma, theorem, and proof obligation in dependency order,
with stable labels.

- **A.1** Map the dependency closure. Starting from each proposal's
  targets, walk back through cited step files to identify every step
  that contributes math content the mechanization needs. Output:
  `anti_loc/extracted_math/dependency_map.md` listing each step and
  the math item(s) it contributes, with the per-axis grouping made
  explicit (a step may feed one axis or both).
- **A.2** Per axis, pull math content out of each step file. For each
  item:
  - the LaTeX/markdown of the statement,
  - the labeled hypotheses,
  - the proof or proof obligation,
  - the bookkeeping (forward/reverse direction, grade, dependencies),
  - the cascade-internal name and the step it came from.
- **A.3** Order by dependency and merge into one math artifact per
  axis. Resolve duplicate names; assign stable labels of the form
  `def:duality_confinement:<short-name>`, `lem:duality_confinement:<short-name>`,
  `thm:rh:<short-name>`, etc.
- **A.4** Codex extraction sessions (optional). For tedious extraction
  passes (pulling math out of many step files into clean tex/markdown),
  a separate codex session can be used. This is NOT the mechanization
  session. The extraction session is bounded in scope to text
  consolidation. Save its thread ID under
  `anti_loc/.codex_thread_id_extraction_<axis>`. Strict protocol does
  not govern this session, but Claude still reviews each output.
- **A.5** Exit criterion: each math artifact reads as a coherent math
  document; every claim has hypotheses, a statement, and either a
  proof or a tagged proof obligation; no step-file references in the
  body (only in the provenance footnote per item).

## Phase B — Math confirmation (Claude only, no codex)

Goal: Claude exercises math judgment on the consolidated artifacts
(per `feedback_review_authority.md`).

- **B.1** Read each math artifact end-to-end as math, not as cascade
  output.
- **B.2** For each claim, audit:
  - Are hypotheses sufficient for the conclusion?
  - Does the proof actually derive the conclusion from the
    hypotheses?
  - Are there silent assumptions (e.g. classical logic, axiom of
    choice, finite-dimensionality, RH-adjacent prerequisites)?
  - Is the statement faithful to what the cascade actually
    established, or is it overreaching?
- **B.3** Flag gaps. For each gap:
  - state the gap precisely,
  - propose a fix path (run another cascade step? cite a standard
    reference? weaken the claim?),
  - surface to user for direction if the fix is non-trivial.
- **B.4** Resolve gaps with user input where required. Cascade steps
  to fill gaps are run outside this plan.
- **B.5** Exit criterion: every claim in each math artifact passes
  Claude's audit at the highest math-proof standards, or is tagged as
  an explicit proof obligation with a justified path.

## Phase C — Mechanization prep (Claude only, no codex)

Goal: populate inventories, manifests, queues from the confirmed math
artifacts.

- **C.1** Build per-axis statements-of-record from the math artifact
  → `paper/notes/statements-of-record.yml` (or per-axis equivalent
  under `formalization/`). For each label:
  `label`, `section_in_artifact`, `intended_status` (`mechanize_now` /
  `obligation` / `out_of_scope_recognition_source` /
  `out_of_scope_meta` / `support_only` / `nonclaim`),
  `lean_coverage` placeholder.
- **C.2** Populate per-axis inventory TOMLs from §C.1 →
  `formalization/inventory/{duality_confinement,rh}_paper_inventory.toml`.
- **C.3** Populate per-axis dispatch queues from `mechanize_now` rows
  in document order →
  `formalization/traceability/queue_{duality_confinement,rh}.csv`.
- **C.4** Update `lean/manifests/section_module_map.toml` mapping
  artifact sections → target Lean module paths.
- **C.5** Update `formalization/inventory/imported_foundations.yml`
  with any new Foundations cross-walk entries the confirmed math
  requires (visibility tag uses, FATCD records, audited records, etc.).
  **Note**: the file currently contains hiddenness-era bootstrap
  rows (sed-renamed during Phase 0); audit and replace with rows
  appropriate to this repo's math during this step.
- **C.6** Run the pre-mechanization validator chain:
  `python3 scripts/audit_foundations_dependencies.py --check --skip-validation`,
  `python3 scripts/check_foundations_provenance.py --check`,
  `python3 scripts/check_manifests.py --check`. All must pass before
  Phase D.

## Phase D — Lean scaffold sanity (mostly done in Phase 0)

The empty-but-rebranded skeleton already builds (Phase 0 outstanding
items confirm this). Re-confirm before Phase F kickoff:

- **D.1** `cd lean && lake build` — clean.
- **D.2** `python3 scripts/check_lean.py --skip-build` — pass.
- **D.3** No stale hiddenness refs (the grep excludes its own
  documentation hits in `PLAN_mechanization.md` and `REVIEW_REQUEST*.md`
  where the search command appears verbatim; the only allowed remaining
  hit is the sibling-repo cross-reference in this plan):
  ```bash
  grep -rn 'SixBirdsHiddenness\|six-birds-hiddenness' . \
      --exclude-dir=vendor --exclude-dir=anti_loc --exclude-dir=.git \
      --exclude-dir=memory --exclude=PLAN_mechanization.md \
      --exclude='REVIEW_REQUEST*.md'
  ```

## Phase E — Audit infrastructure (already in place from Phase 0)

The validators copied from hiddenness are scaffolded and rebranded.
Sanity-confirm:

- **E.1** Every validator runs on the empty skeleton without
  crashing (empty data is expected pre-Phase C). Use the
  authoritative invocations — `audit_foundations_dependencies.py`
  in particular requires `--skip-validation` (see "Audit flag
  interaction" below):
  ```bash
  python3 scripts/check_lean.py --skip-build
  python3 scripts/check_manifests.py --check
  python3 scripts/check_statements_of_record.py --check
  python3 scripts/audit_foundations_dependencies.py --check --skip-validation
  python3 scripts/check_foundations_provenance.py --check
  python3 scripts/check_semantic_alignment.py --check
  python3 -m pytest scripts/test_check_manifests.py
  ```
- **E.2** `lean/manifests/trust_base.txt` reviewed; no additions
  needed yet (`Classical.choice`, `propext`, `Quot.sound`, `choice`,
  `funext`).

### Audit flag interaction (operator footgun)

`scripts/check_lean.py` invokes
`scripts/audit_foundations_dependencies.py --check --skip-validation`
([scripts/check_lean.py:248](scripts/check_lean.py)). The committed
artifacts at `formalization/inventory/foundations_declarations.jsonl`
and `formalization/inventory/foundations_dependency_audit.md` must be
generated with `--skip-validation` (matching that mode). Convenience
Makefile targets (see [Makefile](Makefile)):

- `make audit-check` — `--check --skip-validation` (matches
  check_lean.py's invocation; the safe verification command).
- `make audit-regenerate` — `--skip-validation` (regenerates artifacts
  in the same mode the committed shape uses).

Running `audit_foundations_dependencies.py` without `--skip-validation`
(or `make audit-regenerate-full`) writes `validation_status: passed`
artifacts, which then cause `check_lean.py` to flag them as stale.
Default to the `--skip-validation` mode unless you specifically need
the upstream-validator side effects.

## Phase F — Codex thread bootstrap (one per axis)

For each axis (duality_confinement first, then rh — or whichever order
matches the cascade dependency closure that Phase A.1 reveals), once
Phase C is complete for that axis:

- **F.1** Build kickoff prompt at `/tmp/bootstrap_<axis>.txt` from
  `lean/codex_kickoff.md` plus the first per-subsection prompt.
- **F.2** Bootstrap via stdin (required — argv hangs for multi-KB
  bootstraps; see `feedback_codex_bootstrap_stdin.md`):
  ```bash
  codex exec --json --skip-git-repo-check --full-auto \
      -c model_reasoning_effort='"high"' \
      < /tmp/bootstrap_<axis>.txt \
      2>/tmp/bootstrap_<axis>.stderr \
      > /tmp/bootstrap_<axis>.jsonl
  head -1 /tmp/bootstrap_<axis>.jsonl | jq -r .thread_id \
      > lean/.codex_thread_id_<axis>
  ```
- **F.3** Inspect the kickoff turn output. The bootstrap prompt is
  `kickoff + first per-subsection dispatch`, so the turn IS expected
  to produce Lean code for the first subsection. Apply the same
  per-subsection review criteria (G.3 + G.4) as for any other
  dispatch.

## Phase G — Per-subsection mechanization loop (strict protocol)

For each row in the axis queue, in document order:

- **G.1** Build dispatch prompt via `scripts/build_codex_prompt.py`.
- **G.2** Dispatch via `codex exec resume` (argv on resume is fine):
  ```bash
  codex exec resume --json --full-auto \
      -c model_reasoning_effort='"high"' \
      "$(cat lean/.codex_thread_id_<axis>)" \
      "$(cat /tmp/dispatch.txt)" \
      2>/tmp/dispatch.stderr > /tmp/dispatch.jsonl
  ```
- **G.3** Validator chain: `check_lean.py`, `check_manifests.py`,
  `check_statements_of_record.py`.
- **G.4** Substance review (Claude's call): statement fidelity ≥
  non-`rfl` step ≥ idiomatic style.
- **G.5** Iterate (same-session fix prompt) or accept (advance queue,
  append manifest entry).
- **G.6** Section-level coherence review only after every subsection
  in a section is accepted (single permitted batching exception).

Hard rules: never combine two subsections in one dispatch; never start
a fresh codex thread to "retry"; never invoke Claude Code sub-agents.

## Phase H — Closure

- **H.1** Full validator chain green across both axes:
  `python3 scripts/check_lean.py`,
  `python3 scripts/check_manifests.py --check`,
  `python3 scripts/check_statements_of_record.py --check`,
  `python3 scripts/audit_foundations_dependencies.py --check --skip-validation`,
  `python3 scripts/check_foundations_provenance.py --check`,
  `python3 scripts/check_semantic_alignment.py --check`.
- **H.2** Per-theorem axiom audit (`#print axioms`) confirms each
  theorem's deps are within `lean/manifests/trust_base.txt`.
- **H.3** No forbidden tokens (`sorry`, `admit`, `axiom`, `opaque`,
  `constant`) outside doc-comments anywhere under
  `lean/SixBirdsDualityConfinement/*`.
- **H.4** Lean-traceability disclosure pass — re-promote the
  disclosure-discipline memory (`feedback_lean_traceability_disclosure.md`
  in the sibling hiddenness archive) before drafting any paper-side
  prose that cites the Lean work.

## Phase I — Paper writing (deferred)

After Phase H, papers can be written as publication-grade exposition
of the confirmed mechanized math. This is a separate workflow with its
own memories (paper-writing role split, register, audience, PDF
review, etc.) not currently loaded in this repo. Re-promote the
relevant paper-writing memories from the sibling hiddenness archive
before starting Phase I.

---

## Status

- Phase 0: **complete** (2026-05-23, revised after external review;
  see [reviews/REVIEW_REQUEST_phase0.md](reviews/REVIEW_REQUEST_phase0.md)
  for the request the reviewer responded to). Scaffold copied from
  hiddenness model, vocabulary adapted, memories ported,
  codex_kickoff.md + CODEX_RUNBOOK.md authored, sed-rename misses
  cleaned up post-review. Smoke tests green:
  - `cd lean && lake build` → 50/50 jobs clean against the empty axis
    umbrellas and the alignment trio.
  - `python3 scripts/check_lean.py --skip-build` → `duality_confinement
    Lean prechecks passed`.
  - `make validate` (full validator chain) →
    `check_lean --skip-build`, `check_manifests --check` (0+0 entries),
    `check_statements_of_record --check` (0 rows),
    `audit_foundations_dependencies --check --skip-validation`
    (148 declarations, 25 import mappings),
    `check_foundations_provenance --check` (3 vendored tracks, 25
    import-use entries), `check_semantic_alignment --check` — all pass.
  - `make test` (`pytest scripts/test_check_manifests.py`) → 17/17 pass.
  - `python3 scripts/build_paper_inventories.py --check` →
    `paper inventories and queues are current`.
  - Residual-rename grep clean (exclude-aware form; see D.3).
  - Bootstrapped generated artifacts: `foundations_declarations.jsonl`
    (148 decls), `foundations_dependency_audit.md`,
    `foundations_provenance_summary.md`, regenerated
    `lean/SixBirdsDualityConfinement/ImportedFoundations.lean`.
  - Stub added: `paper/notes/statements-of-record.yml` (rows=0,
    schema-conformant, validates clean).
  - Post-review cleanups: `build_paper_inventories.py`
    (`HIDDENNESS_/PVNP_` → `DC_/RH_`; "main"/"xi" labels →
    `duality_confinement`/`rh`; render_toml schema header expanded
    with the full per-entry schema and corrected `intended_status`
    enumeration); `check_manifests.py` docstring; stale
    `main/xi` axis references in `test_check_manifests.py` and the
    failing `test_parse_section_module_map_real_file` spot-check
    that hardcoded hiddenness-era entries; `check_semantic_alignment.py`
    `needles_items.jsonl` → `source_items.jsonl`;
    `audit_foundations_dependencies.py` 17-entry `DEFAULT_IMPORTED_FOUNDATIONS`
    bootstrap deleted, `write_imported_foundations_if_missing` →
    `require_imported_foundations` (cross-walk yml is curated; restore
    from git rather than auto-regenerating from stale defaults);
    inventory TOML stubs' `[[items]]` → `[[entry]]` schema doc;
    codex_kickoff.md §11 validator list reconciled with what
    `check_lean.py` actually invokes; `Makefile` gained
    `audit-check`/`audit-regenerate`/`audit-regenerate-full`/`validate`/`test`
    targets; CODEX_RUNBOOK.md gained the audit-flag interaction note.
  - Deferred to later phases (documented; not blocking):
    `scripts/build_codex_prompt.py` has hiddenness-shaped hardcoded
    paths + notation cues (rewrite in Phase F prep);
    `scripts/check_statements_of_record.py` `EXPECTED_SOURCE_FILES`
    has placeholder math-artifact paths (rewrite in Phase C as the
    actual extracted_math filenames stabilize); paper-template
    upstream `description`-environment defect breaks `make
    paper-build` (independent decision — patch upstream then resync,
    or downstream-patch with placeholder `\item` rows).
- Phase A: **complete** (2026-05-23). Math extraction & consolidation
  per axis:
  - [anti_loc/extracted_math/dependency_map.md](anti_loc/extracted_math/dependency_map.md)
    walks both proposals, identifies cited cascade steps, lists
    per-item math content needed for mechanization.
  - [anti_loc/extracted_math/duality_confinement_master.md](anti_loc/extracted_math/duality_confinement_master.md)
    — duality-confinement axis consolidated math (8 top-level sections
    matching queue sections; 13 items, 12 mechanize_now + 1
    support_only + 1 out_of_scope_recognition_source on RH side).
  - [anti_loc/extracted_math/rh_construction.md](anti_loc/extracted_math/rh_construction.md)
    — RH axis consolidated math (8 top-level sections matching queue
    sections; 11 items, 10 mechanize_now + 1 recognition_source).
  - Primary mathematical sources: RH cascade step 69 (master theorem
    statement and proof, self-contained as RH-specialization of
    needles.tex §5), step 448 (Sel^!_{ζ,tr} construction + Theorem T),
    step 449 (master theorem applicability audit), step 454
    (recognition closure landing chain). The framework
    `needles.tex` (§5) is the upstream apparatus but is not vendored;
    step 69 is the self-contained presentation.
- Phase B: **complete** (2026-05-23). Math-substance audit at the
  highest math-proof standards
  ([anti_loc/extracted_math/audit_summary.md](anti_loc/extracted_math/audit_summary.md)).
  All 25 claims pass; 3 mechanization-representation notes (Douglas
  factorization encoding choice, AM-GM in abstract Scalar setting,
  real-part type for the RH zero ledger) flagged to be carried into
  per-subsection dispatch prompts. No mathematical gaps surfaced to
  user.
- Phase C: **complete** (2026-05-23). Populated per-axis inventories
  (13 DC + 11 RH = 24 entries), queue CSVs (12 DC + 10 RH = 22
  mechanize_now items in document order), the
  [section_module_map.toml](lean/manifests/section_module_map.toml)
  (8 DC + 7 RH sections), and the
  [statements-of-record.yml](paper/notes/statements-of-record.yml)
  (24 rows). The
  [imported_foundations.yml](formalization/inventory/imported_foundations.yml)
  cross-walk was audited; the existing 25 entries enumerate
  foundation primitives codex may consume, consumer fields populate
  during Phase G as actual use materializes. C.5 verdict: file is
  structurally sound; no curation changes needed pre-mechanization.
- Phase D: **complete** (2026-05-23). `cd lean && lake build` clean
  against the empty per-axis-section stubs (24 modules: 8 DC + 7 RH
  + alignment trio + foundations + 2 axis umbrellas).
- Phase E: **complete** (2026-05-23). Full validator chain green
  pre-mechanization (`make validate`).
- Phase F: **complete** (2026-05-23). Two codex threads bootstrapped
  via stdin:
  - Duality Confinement axis: `019e54ad-ec86-7560-9496-5afac11cb639`
    at [lean/.codex_thread_id_duality_confinement](lean/.codex_thread_id_duality_confinement).
    Bootstrap turn included the first per-subsection dispatch and
    produced the first Involution module.
  - RH axis: `019e54cc-8015-7570-a50e-582aca58ca74` at
    [lean/.codex_thread_id_rh](lean/.codex_thread_id_rh). Bootstrap
    turn included the first per-subsection dispatch and produced the
    first Involution module (RealCoordinate + Complex record +
    feInvolution + psiMinusRh with substantive proofs of involutivity,
    fixed_locus, anti_invariance).
- Phase G: **complete** (2026-05-23). All 22 mechanize_now queue items
  accepted as 22 manifest entries across 15 per-section modules:
  - **Duality Confinement axis** (8 dispatches → 12 manifest entries):
    Involution → Separation → AntiInvariantLedger → DirectConfinement
    → Domination → MasterTheorem → ExhaustiveSqueeze → DefectedBudget.
    Load-bearing master theorem
    (`SixBirdsDualityConfinement.DualityConfinement.MasterTheorem.masterTheorem`)
    composes typed-cone monotonicity + squeeze + positivity-to-zero +
    separation theorem (4 non-`rfl` steps).
  - **RH axis** (7 dispatches → 10 manifest entries):
    Involution → ZeroLedger → AntiInvariantZeroLedger → SatSelShell →
    TranslationT → DCMasterApplied → RHConditional.
    Headline conditional theorem
    (`SixBirdsDualityConfinement.RH.RHConditional.rhConditional`)
    chains `GammaSdtcSelberg γ → dcMasterApplied → A_Z = 0 →
    translationTForward → RH (every ρ has Re(ρ) = 1/2)`.
    `GammaSdtcSelberg` is a typed `structure` carrier (not a Lean
    `axiom`) placed inline in RHConditional.lean.
  - Known weakness: `prop:duality_confinement:optimized-trace-budget`
    has AM-GM taken as hypothesis (projection-packaged at the
    abstract-Scalar level — see audit_summary §A2). Off the critical
    path; would require introducing typed real-arithmetic structure to
    derive substantively.
- Phase H: **complete** (2026-05-23):
  - **H.1** Full validator chain green across both axes (`make
    validate`).
  - **H.2** Per-theorem `#print axioms` audit (full `check_manifests
    --check` without `--skip-probe`): all 12+10 manifest entries pass;
    every theorem's axiom closure lies within
    `lean/manifests/trust_base.txt` (`Classical.choice`, `propext`,
    `Quot.sound`, `choice`, `funext`).
  - **H.3** No forbidden tokens (`sorry`, `admit`, `axiom`, `opaque`,
    `constant`) in active source under
    `lean/SixBirdsDualityConfinement/*`. Single grep hit is a
    documentation reference in
    [lean/SixBirdsDualityConfinement/RH.lean](lean/SixBirdsDualityConfinement/RH.lean):22
    (doc-comment naming the rule; benign — comments are stripped
    before the validator scans).
  - **H.4** SoR sync: all 22 mechanized SoR rows updated from
    `lean_coverage = not_mechanized` to `definition`/`theorem` with
    populated `lean_decl` and `semantic_alignment = faithful`. The
    1 `support_only` def (defected-budget) stays `not_mechanized`;
    the 1 recognition_source (`obl:rh:gamma-sdtc-selberg`) at
    `recognition_source` with `lean_decl` pointing at the inline
    typed carrier
    `SixBirdsDualityConfinement.RH.RHConditional.GammaSdtcSelberg`.
- Phase I: **deferred** (paper writing — not a prerequisite for
  mechanization, governed by separate workflow + memories).

## Pointers

- Memories: `~/.claude/projects/-home-repos-six-birds-duality-confinement/memory/`
- Sibling-repo model (for prior-art reference): `../six-birds-hiddenness/`
- Proposals: `anti_loc/paper_proposal_self_dual_trace_confinement.md`,
  `anti_loc/paper_proposal_rh_via_sdtc_selberg.md`
- Cascade steps: `anti_loc/thread_rh/steps/` (431 steps)
- Cascade findings: `anti_loc/thread_rh/findings_rh.md`,
  `anti_loc/thread_rh/cascade_map_rh.md`,
  `anti_loc/thread_rh/manager_log.md`
- Lean entry: `lean/SixBirdsDualityConfinement.lean`
- Lakefile: `lean/lakefile.toml`
- Vendored foundations: `vendor/foundations/`
- Vendor provenance: `vendor/foundations/vendor_provenance.yml`
