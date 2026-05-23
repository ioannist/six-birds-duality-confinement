# Duality Confinement + RH paper-writing prep plan

Status: opened 2026-05-23; **closed 2026-05-23** (all 10 phases
0–9 closed; sequential drafting arc may begin per
`paper/writing-plan.md`).

Manager-side runbook for the pre-writing prep arc covering **both**
papers in this repo:

- **Paper 1 — Duality Confinement** (working title locked at Phase 0:
  *"Self-Dual Trace Confinement: A Six Birds Structural Law for
  Formed Closures Under Involutive Self-Duality"*). Math artifact:
  `anti_loc/extracted_math/duality_confinement_master.md`.
  Mechanization at `lean/SixBirdsDualityConfinement/DualityConfinement/`.
- **Paper 2 — Riemann Hypothesis (RH closure)** (working title locked
  at Phase 0: *"A Six Birds Closure of the Riemann Hypothesis via
  Self-Dual Trace Confinement on the Saturated Selberg Trace Layer"*).
  Math artifact: `anti_loc/extracted_math/rh_construction.md`.
  Mechanization at `lean/SixBirdsDualityConfinement/RH/`. **RH depends
  on Paper 1** for the master theorem and the SDTC recognition source
  (one-way dependency; Paper 1 does not cite Paper 2 results except
  for two sanctioned forward-reference paragraphs).

Locked decisions and per-phase tasks live in this file. Modeled
1-to-1 on the sibling repo's `paper/notes/prep-plan.md`
(`/home/repos/six-birds-hiddenness/paper/notes/prep-plan.md`) which
ran 10 phases (0–9) and produced the prep-arc deliverables before
any body prose was drafted.

**No `.tex` body prose is written under this plan.** This plan only
produces preparation artifacts. The Phase 9 deliverable
`paper/writing-plan.md` is itself a prep artifact (a runbook for a
future drafting arc), not body prose. Section / subsection / appendix
files end Phase 8 as TODO-only skeletons (file exists, has `\section`,
`\label`, and a TODO comment; no body prose; no live `\subsection`
structure; no live `\input{...}` calls).

The paper-writing discipline memories under
`~/.claude/projects/-home-repos-six-birds-duality-confinement/memory/`
(now in paper-writing-mode after the 2026-05-23 mode swap) govern
every dispatch.

---

## Paper theses (working — locked at Phase 0)

### Paper 1 — Duality Confinement

From `anti_loc/paper_proposal_self_dual_trace_confinement.md` and the
extracted math at `anti_loc/extracted_math/duality_confinement_master.md`:

> A formed Six Birds closure carrying genuine involutive self-duality
> on its visible object ledger cannot host visible mass off the fixed
> locus of the duality. The mechanism is the **duality-confinement
> membrane theorem**: an operator-style squeeze argument over a typed
> positive cone, given an involutive object ledger with separating
> anti-invariant readout plus a sequence of completed domination
> records `A_X ⪯ B_n` with `tr B_n → 0`. The named structural law
> articulating this closure-content fact is **Self-Dual Trace
> Confinement (SDTC)**; the load-bearing content (the existence of
> the domination records on the formed self-dual layer) is supplied
> as recognition source, structurally identified by the V-Differential
> trace-state-only column condition.

Plus the supporting apparatus: trace identity, direct confinement
consequences, completed domination bridge with Douglas factorization
(typed-cone encoding), exhaustive moving-ledger squeeze, optimized
scalar trace budget (AM-GM in abstract Scalar setting).

All 12 mechanize_now Lean theorems carry `faithful` semantic
alignment after Phase H.4 sync (Phase G/H of `PLAN_mechanization.md`).
Two encoding-disclosure notes (audit_summary §A1 Douglas, §A2 AM-GM)
must be carried into body prose.

Cross-substrate generalizations (CPT symmetry, gauge invariance,
quantum self-adjointness, particle-antiparticle, function-field RH)
are STRUCTURAL POINTERS, not established results.

### Paper 2 — Riemann Hypothesis (RH closure)

From `anti_loc/paper_proposal_rh_via_sdtc_selberg.md` and the
extracted math at `anti_loc/extracted_math/rh_construction.md`:

> Given the saturated completed Selberg trace closure
> `Sel^!_{ζ,tr}` under the lawful trace instrument `I_tr`,
> translation theorem T (theorem-grade by construction; mechanized)
> establishes that the anti-invariant zero ledger vanishes
> (`A_Z(ζ) = 0`) iff the Riemann hypothesis holds (every nontrivial
> zero of `ζ` has real part 1/2). Conditional on the recognition
> source `Γ_{SDTC-Selberg}` (supplied by Paper 1 as the
> Selberg-class instance of SDTC; encoded in Lean as a typed
> structure carrier, NOT a Lean axiom; not framework-derivable per
> the cascade's three-option sweep at steps 451–453), the
> duality-confinement master theorem (Paper 1) yields `A_Z(ζ) = 0`,
> and the conditional landing chain `Γ_{SDTC-Selberg} ⟹ RH`
> mechanized as `rhConditional` delivers RH on the typed zero ledger.

Out-of-Six-Birds reading: a conditional theorem
`Γ_{SDTC-Selberg} ⟹ RH`. NOT unconditional standard-ZFC RH.

All 10 mechanize_now Lean theorems carry `faithful` semantic
alignment. One representation-disclosure note (audit_summary §A3
real-part-type abstraction). The `obl:rh:gamma-sdtc-selberg`
recognition source is the typed structure carrier
`SixBirdsDualityConfinement.RH.RHConditional.GammaSdtcSelberg`
(inline placement sanctioned by `lean/codex_kickoff.md` §12).

---

## Locked global decisions

- **Source of record (Phase 0 input).** The math artifacts at
  `anti_loc/extracted_math/duality_confinement_master.md` and
  `anti_loc/extracted_math/rh_construction.md` are the canonical
  source for paper claims, NOT LaTeX. Phase 0 enumerates labeled
  items from these markdown artifacts. When paper `.tex` content
  is eventually drafted (under a separate post-prep drafting arc),
  the math artifacts remain the authoritative source.
- **Lean state as input.** Mechanization is complete (22 manifest
  entries; full validator chain green; per-theorem axiom audit
  within trust_base; Phase A–H all closed and REVISE-fixes applied
  per `PLAN_mechanization.md` Status block). Statements-of-record
  bind paper claims to the Lean realization state recorded at
  `lean/manifests/`.
- **Codex threads.** The prep arc is executed **Claude-only**. The
  two mechanization codex threads
  (`019e54ad-ec86-7560-9496-5afac11cb639` for duality_confinement;
  `019e54cc-8015-7570-a50e-582aca58ca74` for rh) are NOT dispatched
  under this prep arc. They are RESERVED for the future drafting
  arc, which begins with the mode-swap procedure documented in the
  Phase 9 deliverable `paper/writing-plan.md`.
- **Shared `paper/notes/`** for cross-paper artifacts. Per-paper
  `paper/<axis>/notes/` for paper-specific artifacts (contract,
  section outline, figure/table plan, notation workspace).
- **Bibliography.** Tsiokos / internal only. Max 3 references per
  paper. Shared `paper/references.bib`. External references handled
  by the user's end-of-process pipeline; deferred for now.
- **Build / CI.** Local-only `make paper-preflight-<axis>` per
  paper. No CI.
- **Out of scope for both papers.** For DC: standard-ZFC operator-
  theoretic full-generality master theorem; cross-substrate theorems
  (only structural pointers). For RH: standard-ZFC unconditional
  RH; circumvention of classical RH attack barriers in their native
  sense; GRH for primitive Selberg-class L-functions; framework-
  internal derivation of `Γ_{SDTC-Selberg}`. These are recorded as
  nonclaims in `paper/notes/scope-fence.md`.
- **Cross-paper dependency.** Paper 2 → Paper 1 (one-way). Paper 1
  does NOT cite Paper 2 results except in two sanctioned forward-
  reference paragraphs (in `sec:involutive_ledger` for the RH
  worked example and in `sec:master_theorem` for naming Paper 2 as
  the worked single-substrate validation). No `\Cref` to Paper-2
  labels from Paper 1; no `TsiokosRH*` bibkey in Paper 1's
  bibliography.
- **Phase ordering.** Phase 0 → ... → Phase 9 with forward
  dependency. Each phase closes when its deliverables exist and
  pass a Claude self-review against the math artifacts + Lean
  state. Phases run in order; no phase starts before the prior
  phase is closed. Phase log kept inline in this file (append a
  "Closed" timestamp under each phase heading after sign-off).
- **Sequential discipline.** Per memory `feedback_no_batching.md`:
  no parallel tool calls; one task at a time. The prep arc runs
  sequentially.

---

## Phase 0 — Asset audit & per-paper contracts

*Closed 2026-05-23.*

**Goal.** Enumerate every labeled item in the math artifacts, lock
each paper's contract, name the cross-paper boundary.

Tasks:

- [ ] **Cross-paper asset audit.** Enumerate every labeled item in
  `anti_loc/extracted_math/duality_confinement_master.md` and
  `anti_loc/extracted_math/rh_construction.md`. Classify each as
  `body` (mainline content), `appendix`, `evidence_pack_only`,
  `nonclaim`, `out_of_scope_recognition_source`, or `support_only`.
  Cross-check against
  `formalization/inventory/{duality_confinement,rh}_paper_inventory.toml`
  to confirm every inventory label has a target_destination and
  every math-artifact label has an inventory entry.
- [ ] **Paper 1 contract** (`paper/duality_confinement/notes/contract.md`):
  one-paragraph thesis (the SDTC structural law + duality-confinement
  master theorem, restated for a general mathematician audience);
  audience entry point; source-section mapping (which math-artifact
  §X feeds which target paper §Y); headline claim graph (which
  theorems are the spine). **NOTE**: a preliminary version was
  drafted out-of-order on 2026-05-23 before this prep plan existed;
  it will be reviewed against the asset-audit output and revised
  (or accepted as-is) during Phase 0 sign-off.
- [ ] **Paper 2 contract** (`paper/rh/notes/contract.md`): same
  shape. Headline contribution: the conditional landing chain
  `Γ_{SDTC-Selberg} ⟹ RH`. Relationship to Paper 1: RH imports the
  master theorem + recognition source. This file does NOT exist
  yet; produced during Phase 0.
- [ ] **Cross-paper boundary** (`paper/notes/cross-paper-boundary.md`):
  explicit list of what Paper 1 forwards to Paper 2 (the master
  theorem, the SDTC framing, the V-Differential trace-state-only
  column condition) and what Paper 2 imports from Paper 1
  (`Γ_{SDTC-Selberg}` as the Selberg-class instance of SDTC).
  Identifies the two sanctioned forward-reference paragraphs in
  Paper 1.
- [ ] **Out-of-scope ledger** (`paper/notes/out-of-scope-ledger.md`):
  explicit list of dropped material — DC: operator-theoretic full
  generality; cross-substrate theorems; RH: standard-ZFC RH;
  classical barrier circumvention; GRH; framework derivation of
  `Γ_{SDTC-Selberg}`.

Deliverables:

- `paper/notes/phase0-asset-audit.md` (shared) — cross-paper
  enumeration with per-row classification.
- `paper/duality_confinement/notes/contract.md` (revise / accept
  the preliminary draft)
- `paper/rh/notes/contract.md` (new)
- `paper/notes/cross-paper-boundary.md` (new)
- `paper/notes/out-of-scope-ledger.md` (new)

Dispatch: Claude-driven (reading math artifacts + inventories).
No codex dispatch.

---

## Phase 1 — Notation, macros, and terminology consolidation

*Closed 2026-05-23.*

**Goal.** Lock the symbol / macro / term vocabulary before any
prose is drafted.

Tasks:

- [ ] **Audit math-artifact notation.** Scan both math artifacts
  for every symbol introduced (`J`, `J_iso`, `ψ`, `ψ_-`, `P_-`,
  `A_X`, `K^-`, `B_n`, `E`, `T_n`, `ι_n`, `Fix(J)`, `Γ_{SDTC}`,
  `J_L`, `Λ_ζ`, `Z_ζ^nt`, `A_Z(ζ)`, `Sel^!_{ζ,tr}`, `I_tr`,
  `Γ_{SDTC-Selberg}`, etc.).
- [ ] **Confirm `paper/notation_and_terminology.md` coverage.** A
  preliminary DC-side population was drafted out-of-order on
  2026-05-23 before this prep plan existed; the RH side is a
  forward placeholder. Phase 1 finalizes both axes.
- [ ] **Populate `paper/duality_confinement/includes/paper_macros.tex`**
  with Paper 1 macros (`\Fix`, `\Pminus`, `\psim`, `\AX`, `\Jiso`,
  `\Kminus`, `\GamSDTC`, `\dist`, `\tr`, `\preceq`, `\IOL` for the
  ledger tuple shorthand, etc.).
- [ ] **Populate `paper/rh/includes/paper_macros.tex`** with Paper
  2 macros (the DC subset that Paper 2 reuses, plus
  RH-specific: `\JL`, `\psimRH`, `\AZ`, `\Sel`, `\Itr`, `\ZetaZL`,
  `\GamSDTCSelberg`, etc.).
- [ ] **Reserved-symbol verification.** Confirm naming conventions
  across math artifacts, Lean modules, and notation governance doc.
- [ ] **Prose names for mechanized objects.** Lock the English
  names. Lean uses `masterTheorem`, `traceIdentity`,
  `separationConfinement`, `douglasDomination`, `feInvolution`,
  `psiMinusRh`, `translationT`, `dcMasterApplied`, `rhConditional`,
  `GammaSdtcSelberg`, etc.; the paper's prose names need a 1-to-1
  mapping.

Deliverables:

- Populated `paper_macros.tex` per paper.
- `paper/notation_and_terminology.md` finalized for both axes.
- `paper/notes/macro-audit.md` (shared) — consolidated macro list
  with per-macro paper coverage.
- `paper/notes/prose-names.md` (shared) — Lean-decl-name → paper-
  prose-name mapping for all 22 manifest entries + 2 carriers
  (Γ_{SDTC} as paper-prose name; GammaSdtcSelberg).

Dispatch: Claude-only (macro audit + prose-names + notation
governance). The `paper_macros.tex` population is also Claude work
(short controlled artifacts).

---

## Phase 2 — Statements of record

*Closed 2026-05-23.*

**Goal.** Bind every paper claim to source label, target paper,
destination, proof-presentation mode, and Lean coverage.

Tasks:

- [ ] **Confirm `paper/notes/statements-of-record.yml`** (shared)
  is correct post-Phase-H.4. 24 rows: 13 DC + 11 RH. Per-row fields
  per `scripts/check_statements_of_record.py` schema (paper_label,
  env_kind, source_file, source_line, source_section, theorem_title,
  target_paper, target_destination, target_section_hint,
  proof_presentation, lean_coverage, lean_decl, semantic_alignment,
  notes). Pre-existing from Phase H.4; re-verify against the
  asset-audit (Phase 0) for any drift.
- [ ] **Generate `paper/notes/statements-of-record.md`** (shared,
  review-friendly rendering of the yml; sortable table per axis;
  per-row Lean coverage badges).
- [ ] **Adapt `scripts/check_statements_of_record.py`** for our
  axis labels — already done in Phase C scaffolding (Phase C.5 +
  Phase H.4 fix); re-verify and wire into the preflight gate.

Deliverables:

- `paper/notes/statements-of-record.yml` (confirmed)
- `paper/notes/statements-of-record.md` (new)
- Validator wired (confirmed)

Dispatch: Claude-driven (data assembly from inventory + math
artifacts + manifest).

---

## Phase 3 — Section outlines

*Closed 2026-05-23.*

**Goal.** Lock each paper's section / subsection structure with
page budgets, purposes, source mappings.

Tasks:

- [ ] **Paper 1 outline**
  (`paper/duality_confinement/notes/section-outline.md`) with
  per-section page budgets, purposes, primary sources from the math
  artifact, definitions introduced, key claims, dependencies. **NOTE**:
  a preliminary version was drafted out-of-order on 2026-05-23
  before this prep plan existed; it will be reviewed against the
  Phase 0/1/2 outputs and revised during Phase 3 sign-off.
- [ ] **Paper 2 outline** (`paper/rh/notes/section-outline.md`):
  same shape. New; produced during Phase 3.
- [ ] **Section labels lock.** Every section / subsection gets its
  eventual `\label{sec:...}` chosen at this stage.
- [ ] **Page budgets.** Planning numbers per section (not hard
  limits). Target body length per paper: 20–30 pages.
- [ ] **Empty section file skeletons** in each paper's `sections/`
  dir — replace the upstream template stubs with project-specific
  scaffolding (file exists, has `\section`, `\label`, and a TODO
  comment; **NO body prose; NO live `\subsection` structure; NO
  live `\input{...}` calls**). Per hiddenness `PREP_REVIEW_REPORT`
  REJECT-then-iterate cycle, the no-body-prose constraint extends
  to subsections and table inputs in section files.

Deliverables:

- `paper/duality_confinement/notes/section-outline.md` (revise /
  accept preliminary)
- `paper/rh/notes/section-outline.md` (new)
- Per-paper `sections/*.tex` skeletons.

Dispatch: Claude-driven (outline synthesis from contract +
asset-audit + math artifact). Each paper's section-skeleton file
list is a planning task.

---

## Phase 4 — Figure / table plans

*Closed 2026-05-23.*

**Goal.** Every floating object planned before drafting; placeholder
files in place.

Tasks:

- [ ] **Paper 1 figure/table plan** in
  `paper/duality_confinement/notes/figure-table-plan.md`. **NOTE**:
  a preliminary version was drafted out-of-order on 2026-05-23
  before this prep plan existed; revise during Phase 4 sign-off.
  Candidates: involutive-ledger schematic (RH worked example);
  involutive-ledger-examples table; master-theorem-proof-shape
  figure; representation-notes table (audit §A1, §A2); nonclaims
  table; Lean-coverage summary table (App D headline).
- [ ] **Paper 2 figure/table plan** in
  `paper/rh/notes/figure-table-plan.md`. New. Candidates:
  Sel^!_{ζ,tr} typed-shell schematic; landing-chain diagram
  (Γ_{SDTC-Selberg} → A_Z = 0 → RH); Six-Gates audit table; NC-1
  through NC-12 table; representation-notes table (audit §A3);
  Lean-coverage summary table.
- [ ] **Identify source vs. draw-from-scratch** for each figure.
  Most can be TikZ diagrams; the Lean-coverage tables are data from
  manifest + statements-of-record.
- [ ] **Placeholder `.tex` files** in `tables/` and `figures/` per
  paper with planning comments and target placement. Per the no-
  body-prose constraint, these are TODO-only stubs.

Deliverables:

- `paper/duality_confinement/notes/figure-table-plan.md` (revise /
  accept preliminary)
- `paper/rh/notes/figure-table-plan.md` (new)
- Placeholder `.tex` stubs per paper.

Dispatch: Claude-driven.

---

## Phase 5 — Bibliography (Tsiokos-only, max 3 per paper)

*Closed 2026-05-23.*

**Goal.** Every Tsiokos citation needed by either paper is in
`paper/references.bib`. External references are out of scope.

Tasks:

- [ ] **Audit math-artifact citations.** Which Tsiokos works are
  invoked? Both proposals reference Foundations II/III. The RH
  proposal references Holonomy with Memory and SDTC paper (which is
  Paper 1 itself). The DC proposal references needles.tex §5
  (framework apparatus, NOT vendored in our repo; the corresponding
  framework-apparatus path on disk is
  `/home/repos/six-birds-foundations-iii/anti_loc/framework_apparatus/needles.tex`),
  adequacy.tex, Holonomy with Memory, Non-Descending Objects.
- [ ] **Look up Tsiokos refs** from wherever they're staged
  (suggested staging area: `/home/repos/six-birds-papers/`; if not
  present, defer to inline `@misc` entries with the canonical
  bibkeys).
- [ ] **Decide per-paper picks.** Suggested initial set (≤3 per
  paper):
  - Paper 1 (DC): `TsiokosFoundationsII2026`,
    `TsiokosFoundationsIII2026`, and a third reference if available
    (the needles.tex framework apparatus paper or the
    Holonomy-with-Memory paper).
  - Paper 2 (RH): `TsiokosSDTC2026` (Paper 1 sibling cross-cite),
    `TsiokosFoundationsII2026`, `TsiokosFoundationsIII2026`.
- [ ] **Decide shared vs per-paper `.bib`.** Default to shared
  `paper/references.bib`. Each paper's `main.tex` already points at
  `references.bib` via the symlink.
- [ ] **`paper/notes/references-selection.md`** — audit log of
  picks + rationale; explicit note that external references are
  deferred to user's end-of-process pipeline.

Deliverables:

- Populated `paper/references.bib` (shared).
- `paper/notes/references-selection.md`.

Dispatch: Claude-driven.

---

## Phase 6 — Audience translation, scope fence, objections, proof-presentation policy

*Closed 2026-05-23.*

**Goal.** Prepare discipline artifacts so future drafting dispatches
can reference them.

Tasks:

- [ ] **`paper/notes/audience-translation.md`** (shared): table of
  framework-native terms → plain mathematical first-use
  translations + concrete first example + intended first section.
  **NOTE**: a preliminary version was drafted out-of-order on
  2026-05-23 before this prep plan existed; revise during Phase 6
  sign-off. Native terms covered: Six Birds framework; formed
  closure; determining state; trace-state-only column; recognition
  source; BirdInt judgment; involutive object ledger;
  anti-invariant readout; anti-invariant ledger; typed positive
  cone; completed domination bridge; Douglas factorization;
  duality-confinement membrane theorem; exhaustive moving ledger;
  defected obstruction budget; SDTC; functional-equation
  involution; nontrivial-zero ledger; anti-invariant zero ledger;
  saturated completed Selberg trace closure; lawful trace
  instrument; translation theorem T; Γ_{SDTC-Selberg};
  conditional landing chain; six no-smuggling gates + Gate 7;
  three-option derivation sweep.
- [ ] **`paper/notes/scope-fence.md`** (shared): what the two
  papers do NOT claim, with required wording discipline per
  nonclaim. **NOTE**: a preliminary version was drafted
  out-of-order on 2026-05-23; revise during Phase 6 sign-off.
- [ ] **`paper/notes/anticipated-objections.md`** (shared):
  predicted reviewer objections + pre-drafted mitigations. NEW
  (not drafted yet). Likely candidates: "How can the master
  theorem be claimed without operator-theoretic generality?";
  "Why is `Γ_{SDTC-Selberg}` not a Lean axiom?"; "What does
  'typed-cone level' commit you to?"; "Why call SDTC a 'law' when
  it is only validated single-substrate?"; "Doesn't Theorem T
  trivialize the result?"; "Is this just Weil positivity
  relabeled?"; "What about the classical barriers
  (Hilbert–Pólya, Connes, de Branges)?".
- [ ] **`paper/notes/proof-presentation-policy.md`** (shared):
  body / sketch / appendix / standard-reference policy, plus the
  Lean-disclosure wording table (from
  `~/.claude/projects/-home-repos-six-birds-duality-confinement/memory/feedback_lean_traceability_disclosure.md`).
  **NOTE**: a preliminary version was drafted out-of-order on
  2026-05-23; revise during Phase 6 sign-off.

Deliverables:

- Four shared `.md` files in `paper/notes/` (three already
  preliminary; anticipated-objections is new).

Dispatch: Claude-only (cross-paper discipline synthesis).

---

## Phase 7 — Formalization appendix planning + mechanization rebinding

*Closed 2026-05-23.*

**Goal.** Prepare the Lean-disclosure appendices for each paper
before any body prose is drafted.

Tasks:

- [ ] **`paper/notes/mechanization-rebinding-policy.md`** (shared):
  how the manifest's `(paper_label, lean_decl, status, notes)`
  tuples surface in each paper. Covers: which labels go in which
  paper (already settled in inventory); which appear with
  substantive Lean wording vs. projection wording (per the Lean
  coverage column); how the recognition source's typed-carrier
  encoding is disclosed (NOT as a Lean theorem; the inline
  carrier `GammaSdtcSelberg` in `RHConditional.lean`); which
  appear with the typed-cone encoding-disclosure note (the master
  theorem; Douglas factorization; AM-GM-as-axiom).
- [ ] **Draft Paper 1's Lean appendix skeleton**
  (`paper/duality_confinement/appendices/app_d_formalization.tex`)
  with the canonical wording-discipline table and a per-paper-label
  table of the 13 DC inventory rows. Per the no-body-prose
  constraint from hiddenness's `PREP_REVIEW_REPORT` REJECT-then-
  iterate cycle, this is a TODO-only appendix skeleton — file
  exists, has `\section`, `\label`, and a TODO comment; **NO live
  `\subsection` structure; NO live `\input{...}` table inclusions**.
  The wording-discipline table and per-row tables are themselves
  drafted as table-template `.tex` files referenced from a Phase
  9 dispatch table; not inlined into the appendix in Phase 7.
- [ ] **Draft Paper 2's Lean appendix skeleton**
  (`paper/rh/appendices/app_d_formalization.tex`) with the 10 RH
  manifest entries + the recognition-source carrier disclosure
  row. Same no-body-prose constraint.

Deliverables:

- `paper/notes/mechanization-rebinding-policy.md`.
- Skeletal `app_d_formalization.tex` per paper (TODO-only; no
  live structure).

Dispatch: Claude-only (cross-paper policy synthesis; skeletons are
small artifacts).

---

## Phase 8 — Build pipeline & preflight gate

*Closed 2026-05-23.*

**Goal.** `make paper-preflight-<paper>` per paper that lints,
builds, log-checks, and runs the statements-of-record validator.

Tasks:

- [ ] **Confirm top-level `Makefile`** has targets
  `paper-build-duality_confinement`, `paper-build-rh`,
  `paper-preflight-duality_confinement`, `paper-preflight-rh`, and
  the aggregate `paper-preflight`. Already in place from
  mechanization scaffolding; re-verify after section-skeleton
  insertion in Phase 3.
- [ ] **Adapt `scripts/paper_lint.sh`** for our prose rules: long
  Lean module identifiers in body prose, undefined `\Cref`
  references after build, double-word `\Cref` artifacts,
  table-overflow warnings, statements-of-record / manifest
  consistency. Mirrors the lint rules in hiddenness's
  `scripts/paper_lint.sh`.
- [ ] **Build target** invokes `latexmk` per paper using each
  paper's `latexmkrc`.
- [ ] **Log-check target** scans each paper's `.log` for
  `Underfull`, `Overfull`, `Float too large`.
- [ ] **Statements-of-record validator** (from Phase 2) wired into
  `paper-preflight`.
- [ ] **Verify paper-build smoke test**: the template defect in
  `app_a_definitions.tex` (empty `description` environment) needs
  to be either patched or worked around. Per Phase 7's TODO-only
  appendix skeleton constraint, the unused upstream-template
  appendices should be deleted (paper-template's `app_a`, `app_b`,
  `app_c`, `app_e` were always going to be dropped per hiddenness
  precedent which kept ONLY `app_d_formalization.tex`).
- [ ] **`paper/notes/preflight-signoff.md`** (shared) tracks
  pre-drafting gate state for both papers.

Deliverables:

- Updated `Makefile`, `scripts/paper_lint.sh`,
  `scripts/check_statements_of_record.py` integration.
- `paper/notes/preflight-signoff.md`.

Dispatch: Claude-only — script + Makefile tweaks.

---

## Phase 9 — Writing-plan runbook (deliverable only; no drafting)

*Closed 2026-05-23.*

**Goal.** Produce the per-subsection dispatch runbook for a future
drafting arc. **No body prose is written under this phase.** This
is the final prep artifact.

Tasks:

- [ ] **Write `paper/writing-plan.md`** — manager-side
  per-subsection dispatch runbook for both papers. Lists each
  subsection in document order with: target file, prerequisites
  (which prior sections must be drafted first), prep artifacts to
  reference in the prompt, expected page length, governing memory
  files. Includes the dispatch-prompt-construction conventions
  and the review cadence (per-dispatch, per-section flow review,
  per-paper polish, cross-paper review). **NOTE**: a preliminary
  version was drafted out-of-order on 2026-05-23; revise during
  Phase 9 sign-off.
- [ ] **Per-axis drafting-plan** (`paper/<axis>/notes/drafting-plan.md`)
  refining the writing-plan into per-codex-dispatch units for that
  axis. **NOTE**: a preliminary version was drafted out-of-order
  on 2026-05-23 for the DC axis; revise during Phase 9 sign-off.
  The RH version is produced during Phase 9 for the RH paper.
- [ ] **Per-axis claim-revision register**
  (`paper/<axis>/notes/claim-revision-register.md`) catalogs every
  claim from the proposal whose wording needs to be REVISED in the
  drafted paper because the mechanization narrowed / refined /
  made-concrete the original claim. **NOTE**: a preliminary version
  was drafted out-of-order on 2026-05-23 for the DC axis. The RH
  version is produced during Phase 9 for the RH paper. Drafting
  dispatches that touch a register row quote the revised wording.
- [ ] **Per-axis artifact-plan**
  (`paper/<axis>/notes/artifact-plan.md`) tracks the artifacts the
  paper references and the canonical locations to cite (math
  artifacts, Lean modules, manifests, inventory). **NOTE**: a
  preliminary version was drafted out-of-order on 2026-05-23 for
  the DC axis.
- [ ] **Per-axis notation workspace**
  (`paper/<axis>/notes/notation.md`) is the per-axis macro
  promotion staging area before symbols move into
  `paper/notation_and_terminology.md`. **NOTE**: a preliminary
  version was drafted out-of-order on 2026-05-23 for the DC axis.
- [ ] **Mode-swap procedure documented in writing-plan.md.** When
  future drafting begins, the operator sends each codex thread a
  "mode swap" message announcing the transition from mechanization
  to per-section drafting, with pointers to the prep artifacts
  produced under this plan. NOT done under this prep arc; this
  task only records the procedure in writing-plan.md.

Deliverables:

- `paper/writing-plan.md` (revise / accept preliminary)
- `paper/duality_confinement/notes/drafting-plan.md` (revise /
  accept preliminary)
- `paper/rh/notes/drafting-plan.md` (new)
- `paper/duality_confinement/notes/claim-revision-register.md`
  (revise / accept preliminary)
- `paper/rh/notes/claim-revision-register.md` (new)
- `paper/duality_confinement/notes/artifact-plan.md` (revise /
  accept preliminary)
- `paper/rh/notes/artifact-plan.md` (new)
- `paper/duality_confinement/notes/notation.md` (revise / accept
  preliminary)
- `paper/rh/notes/notation.md` (new)

Dispatch: Claude-only (synthesis of all prep artifacts into a
dispatch runbook).

---

## Phase exit criteria

Each phase closes when its deliverables exist and pass a Claude
self-review against the math artifacts + Lean state. Phases run in
order; no phase starts before the prior phase is closed. Phase log
kept inline in this file (append a "Closed" timestamp under each
phase heading after sign-off).

## Note on out-of-order pre-drafts

Several files were drafted on 2026-05-23 BEFORE this prep plan
existed (the manager started writing Phase 9-style deliverables
without first executing Phase 0–8). Those files are listed under the
"NOTE" markers above. The proper Phase ordering treats them as
**preliminary inputs to be reviewed during the corresponding Phase's
sign-off**, not as already-closed deliverables. If the asset audit
(Phase 0), notation finalization (Phase 1), or any subsequent Phase
reveals that the preliminary draft needs revision, the file is
revised; otherwise it is accepted as-is.

The premature `paper/writing-plan.md` and per-axis `drafting-plan.md`
files in particular WILL be revised at Phase 9 — they were drafted
without the benefit of Phase 0's asset audit, Phase 1's notation
finalization, Phase 5's bibliography selection, Phase 6's
anticipated-objections, Phase 7's mechanization-rebinding-policy, or
Phase 8's preflight signoff.

## Pointers

- Math artifacts: `anti_loc/extracted_math/{duality_confinement_master,rh_construction}.md`
- Dependency map: `anti_loc/extracted_math/dependency_map.md`
- Audit summary: `anti_loc/extracted_math/audit_summary.md`
- Inventory: `formalization/inventory/{duality_confinement,rh}_paper_inventory.toml`
- Manifest: `lean/manifests/{duality_confinement,rh}_manifest.toml`
- Section module map: `lean/manifests/section_module_map.toml`
- Mechanization plan: `PLAN_mechanization.md`
- Mechanization external reviews: `reviews/REVIEW_REQUEST_phase0.md`, `reviews/REVIEW_REQUEST_phaseG.md`
- Per-paper notes templates: `paper/{duality_confinement,rh}/notes/`
- Notation governance: `paper/notation_and_terminology.md`
- Memories: `~/.claude/projects/-home-repos-six-birds-duality-confinement/memory/`
- Sibling repo prep arc model: `/home/repos/six-birds-hiddenness/paper/notes/prep-plan.md`
- Sibling repo prep-arc external review: `/home/repos/six-birds-hiddenness/PREP_REVIEW_REPORT.md`
