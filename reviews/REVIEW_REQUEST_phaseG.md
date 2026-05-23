# Phase A-H Mechanization Review Request — six-birds-duality-confinement

You are reviewing the complete Lean-4 mechanization of two papers
(Duality Confinement + RH via SDTC-Selberg) at
`/home/repos/six-birds-duality-confinement`. Phases 0–H of
`PLAN_mechanization.md` are claimed complete. 22 manifest entries
across both axes were produced by codex per a strict per-subsection
protocol; Claude reviewed each turn.

Your task is to spot-check mathematical fidelity, substance, and
operational closure. You are **not** asked to extend mechanization,
dispatch codex, modify Lean modules, or rewrite the math artifacts.

## Context

- Two axes:
  - **Duality Confinement** (paper 1, 12 manifest entries).
    Anchor: `anti_loc/paper_proposal_self_dual_trace_confinement.md`.
  - **RH** (paper 2, 10 manifest entries).
    Anchor: `anti_loc/paper_proposal_rh_via_sdtc_selberg.md`.
- Math source (Phase A consolidation):
  - `anti_loc/extracted_math/dependency_map.md` — walks both
    proposals and cited cascade steps.
  - `anti_loc/extracted_math/duality_confinement_master.md` — DC
    axis consolidated math (sourced primarily from RH cascade step
    69, which is the self-contained RH-specialization of the
    upstream `needles.tex` §5 master theorem).
  - `anti_loc/extracted_math/rh_construction.md` — RH axis math
    (sourced from steps 69, 448, 449, 454 + proposal §§4–7).
  - `anti_loc/extracted_math/audit_summary.md` — Phase B verdict.
- Lean code:
  - `lean/SixBirdsDualityConfinement.lean` umbrella.
  - `lean/SixBirdsDualityConfinement/DualityConfinement/*.lean` —
    8 per-section modules (DC axis).
  - `lean/SixBirdsDualityConfinement/RH/*.lean` — 7 per-section
    modules (RH axis).
  - Alignment trio: `lean/SixBirdsDualityConfinement/{ImportedFoundations,FoundationsICompat,Terminology}.lean`.
  - Vendored foundations: `vendor/foundations/` (Lean 4.28.0,
    mathlib-free).
- Manifests:
  - `lean/manifests/duality_confinement_manifest.toml` (12 entries).
  - `lean/manifests/rh_manifest.toml` (10 entries).
- Inventory + queue + SoR:
  - `formalization/inventory/{duality_confinement,rh}_paper_inventory.toml`.
  - `formalization/traceability/queue_{duality_confinement,rh}.csv`.
  - `paper/notes/statements-of-record.yml`.
- Operating constraints (from
  `~/.claude/projects/-home-repos-six-birds-duality-confinement/memory/`):
  - Codex writes Lean, Claude reviews. One subsection per codex
    dispatch in document order.
  - Substance bar: at least one non-`rfl` mathematical step per
    theorem; reject projection-packaged tautologies.
  - Forbidden Lean tokens: `sorry`, `admit`, `axiom`, `opaque`,
    `constant` (in active source — comments are stripped before
    the validator scans).
  - Trust base: only `Classical.choice`, `propext`, `Quot.sound`,
    `choice`, `funext` are allowed in any theorem's `#print
    axioms` closure.

Plan history is in `PLAN_mechanization.md` Status block (covers
Phases 0–H).

## Exit criteria (claimed met)

Verify each independently:

1. `cd lean && lake build` — clean (~65 jobs).
2. `make validate` — full validator chain green
   (check_lean, check_manifests, check_statements_of_record,
   audit_foundations_dependencies, check_foundations_provenance,
   check_semantic_alignment).
3. `make test` — pytest 17/17 pass.
4. Per-theorem `#print axioms` audit — `python3
   scripts/check_manifests.py --check` (without `--skip-probe`) —
   all 22 entries' axiom closures within trust_base.
5. Forbidden-tokens grep clean:
   ```bash
   grep -rn -E '\b(sorry|admit|axiom|opaque|constant)\b' \
       lean/SixBirdsDualityConfinement/
   ```
   Expected: exactly 1 hit in
   `lean/SixBirdsDualityConfinement/RH.lean:22` — a doc-comment
   reference to the rule itself. Benign.
6. SoR consistency: 24 rows, manifest cross-check matches
   (`duality_confinement=12, rh=10`), inventory cross-check
   matches (`duality_confinement=13, rh=11`).

## Specific items to review

### A. Math extraction fidelity (Phase A)

Read both consolidated math artifacts end-to-end against the cited
cascade step content. Spot-check:

- **DC axis source step 69**:
  `anti_loc/thread_rh/steps/step69_duality_confinement_artifacts/duality_confinement_membrane_step69.tex`.
  Compare against `duality_confinement_master.md` §Involution
  through §DefectedBudget. Are all 8 definitions/lemmas/theorems
  preserved with the same hypotheses + conclusions? Any silent
  weakening or strengthening?
- **RH axis source step 448**:
  `anti_loc/thread_rh/steps/step448_sdtc_closure_construction_artifacts/step448_audited_shell_definition.md`
  and `step448_predictive_zero_family.md`. Compare against
  `rh_construction.md` §SatSelShell. Are all 13 typed shell fields
  represented?
- **RH axis source step 454**:
  `anti_loc/thread_rh/steps/step454_sdtc_recognition_closure_artifacts/step454_final_proof_statement.md`.
  Compare against `rh_construction.md` §RHConditional. Is the
  three-step landing chain (Γ → A_Z = 0 → RH) faithfully captured?

### B. Math audit substance (Phase B)

Read `anti_loc/extracted_math/audit_summary.md`. The auditor
(Claude) claims all 25 claims pass at the highest math-proof
standards. Spot-check the auditor's per-claim verdicts:

- The trace-identity lemma is encoded as a definitional unpacking
  (the typed cone bakes in `(A_X).trace = ∫ ‖ψ_-‖² dμ`). Is this
  encoding sound, or does it hide content?
- The Douglas factorization encoding (audit §A1) chose to bundle
  the equivalence into the typed `DouglasData` structure. Is this
  acceptable or projection-packaged?
- The master theorem's three non-`rfl` steps (trace monotonicity
  from `⪯`, real-sequence squeeze, trace-zero-positive ⟹ zero
  element) are listed as substantive. Confirm.

### C. Lean substance (Phase G)

For each theorem entry, check whether the proof clears the
non-`rfl` bar. The four headline proofs to audit:

1. **`SixBirdsDualityConfinement.DualityConfinement.MasterTheorem.masterTheorem`**
   ([lean/SixBirdsDualityConfinement/DualityConfinement/MasterTheorem.lean](lean/SixBirdsDualityConfinement/DualityConfinement/MasterTheorem.lean)).
   Load-bearing for DC axis. The proof composes
   `positive_trace_nonnegative` + `trace_mono` (typed-cone axiom) +
   `squeeze_trace_zero` (hypothesis) + `trace_zero_positive_zero`
   (hypothesis) + `DirectConfinement.separationConfinement`. Is the
   composition substantive, or does it pass through tautologically?

2. **`SixBirdsDualityConfinement.RH.TranslationT.translationT`**
   ([lean/SixBirdsDualityConfinement/RH/TranslationT.lean](lean/SixBirdsDualityConfinement/RH/TranslationT.lean)).
   The forward direction composes `A.sum_zero_imp_term_zero` and
   `A.term_zero_imp_on_line` (both fields of the typed
   `AntiInvariantZeroLedger` structure). Is the encoding strategy
   (push substance to typed-cone axioms; prove theorem by
   composition) acceptable per the audit_summary §A3 design?

3. **`SixBirdsDualityConfinement.RH.DCMasterApplied.dcMasterApplied`**
   ([lean/SixBirdsDualityConfinement/RH/DCMasterApplied.lean](lean/SixBirdsDualityConfinement/RH/DCMasterApplied.lean)).
   Bridges the DC master theorem to the RH-specific `A_Z = 0`
   statement via the `mu_zero_of_ae` hypothesis (which encodes the
   reverse-T direction). Is the bridge sound, or does it tautologize?

4. **`SixBirdsDualityConfinement.RH.RHConditional.rhConditional`**
   ([lean/SixBirdsDualityConfinement/RH/RHConditional.lean](lean/SixBirdsDualityConfinement/RH/RHConditional.lean)).
   Headline result. Takes `gamma : GammaSdtcSelberg shell` as
   explicit hypothesis, applies `dcMasterApplied` + `translationTForward`.
   Confirm:
   - `GammaSdtcSelberg` is a `structure` (not `axiom`).
   - The "conditional" is literal: `γ` is a Lean-level hypothesis.
   - The chain is `γ → dcMasterApplied → A_Z = 0 → translationTForward
     → every ρ ∈ Z_nt has Re(ρ) = 1/2`.

### D. Known weakness (documented; confirm scope)

`SixBirdsDualityConfinement.DualityConfinement.DefectedBudget.optimizedTraceBudget`
takes AM-GM as a hypothesis (`am_gm_optimization`) rather than
deriving it from `(x - y)² ≥ 0`. The audit_summary §A2 expected a
substantive derivation; the abstract-Scalar setting prevented it
without introducing typed real-arithmetic structure.

Confirm:
- This is off the critical mechanization path (the SDTC paper's
  §11.2 mechanization target is the master theorem, not the
  defected-budget proposition; per
  `paper_proposal_self_dual_trace_confinement.md` §8.5 +
  inventory's `support_only` flag on the def).
- The shortcoming is documented in `PLAN_mechanization.md` Phase G
  Status entry.
- Any fix would require either (a) introducing a typed
  `OrderedScalar` with `square_nonneg + sqrt_sq` axioms and
  deriving AM-GM, or (b) accepting the abstract-Scalar limitation.

### E. Encoding choices to spot-check

These are representation decisions that affect downstream
soundness:

- **`ψ_-` coherence**. The DC axis's `SeparatingReadout` and
  `AntiInvariantLedger` structures each carry their own
  `psi_minus` field rather than deriving `ψ_- = P_- ψ` from the
  involutive ledger's `J_iso` and `ψ`. Downstream coherence is
  enforced via `same_readout : ∀ x, A.psi_minus x = sep.psi_minus
  x` parameters on `separationConfinement` and `masterTheorem`.
  Is this acceptable, or does it allow vacuous instantiations?

- **`Sel^!_{ζ,tr}` admissibility**. The `SatSelShell` structure
  records `Audit_L` as an opaque field and uses `F2ChannelStatus`
  from the foundations alias surface. Phase Foundations II
  admissibility (per proposal §4.2) is encoded as the presence of
  this field; not derived. Confirm this is the intended encoding
  (admissibility is a Foundations-II-level fact, not a
  duality_confinement-axis derivation).

- **`GammaSdtcSelberg` placement**. The recognition source typed
  carrier was placed inline in
  `lean/SixBirdsDualityConfinement/RH/RHConditional.lean` rather
  than in a separate `RecognitionSource.lean` module. Both
  placements were sanctioned by `lean/codex_kickoff.md` §12;
  confirm this is documented in the SoR row's `notes` and the
  RH.lean umbrella's comment.

### F. Statements-of-record consistency

The SoR was synced in Phase H.4:
- 22 mechanized rows updated from `lean_coverage = not_mechanized`
  to `definition`/`theorem` with populated `lean_decl` and
  `semantic_alignment = faithful`.
- 1 `support_only` row (`def:duality_confinement:defected-budget`)
  stays `not_mechanized` (no manifest entry — codex did not write
  the def, only the proposition that uses its shape).
- 1 `recognition_source` row (`obl:rh:gamma-sdtc-selberg`) points
  at `SixBirdsDualityConfinement.RH.RHConditional.GammaSdtcSelberg`.

Spot-check that the SoR lean_decl values match what's actually
declared in the per-section .lean files.

### G. PLAN status block accuracy

`PLAN_mechanization.md` Status section claims Phases 0–H complete
with specific smoke-test results, codex thread UUIDs, dispatch
counts, and the known weakness. Cross-check the claims:

- DC thread UUID at `lean/.codex_thread_id_duality_confinement`
  matches the Status block.
- RH thread UUID at `lean/.codex_thread_id_rh` matches the Status
  block.
- Dispatch count (8 DC + 7 RH = 15) consistent with the
  per-section module count under
  `lean/SixBirdsDualityConfinement/{DualityConfinement,RH}/`.
- Manifest entry counts (12 DC + 10 RH = 22) match
  `lean/manifests/{duality_confinement,rh}_manifest.toml`.

### H. Hard prohibitions

You must NOT:

- Continue mechanization (no new manifest entries, no new per-section
  Lean modules).
- Dispatch codex (no `codex exec` calls).
- Modify the math artifacts under `anti_loc/extracted_math/`.
- Modify proposals or vendored foundations.
- Modify Lean modules under
  `lean/SixBirdsDualityConfinement/{DualityConfinement,RH}/*.lean`
  unless explicitly fixing a defect surfaced in your review
  (in which case patch with minimal scope and describe in your
  report).

You MAY:

- Read any file in the repo.
- Run `make validate`, `make test`, `make audit-check`.
- Run `cd lean && lake build`.
- Patch documentation typos in `PLAN_mechanization.md` or
  `audit_summary.md` (describe in your report).
- Suggest fixes for items A–F that are too substantial to apply
  yourself.

## Deliverable

A written report covering:

1. **Pass/fail for each exit criterion** (1–6 above).
2. **Per-item findings** for sections A–G (one short paragraph each,
   or "no issues found" if so).
3. **Substance verdict** on the four headline proofs in §C:
   genuine non-`rfl` content vs projection-packaged.
4. **Any other defects** spotted that aren't on the checklist
   (especially: silent ψ_- coherence violations, type-universe
   issues, manifest/inventory drift).
5. **Verdict**: ACCEPT (Phase H is genuine closure, work is
   release-ready for Phase I drafting) / REVISE (specific issues
   to fix first) / REJECT (substantive math or mechanization
   defect requires re-mechanization).

Limit the report to ~1500 words. Cite file paths and line numbers.
Distinguish between (a) load-bearing mechanization defects (fix
before any Phase I work), (b) documented limitations that are OK
to defer, and (c) matters of taste (note but don't block on).

## Background on the audit constraints

- The substance bar is per the
  `feedback_review_authority.md` memory: "Reject
  projection-packaged tautologies (taking conclusions as
  hypotheses; defining the LHS of an identity to equal its RHS so
  the proof becomes `rfl`; trivializing variational sup/inf into
  algebraic shortcuts). The Lean code must verify genuine
  mathematical content, not just record the paper's signature."
- The strict-protocol memory
  (`feedback_no_batching.md`) governs how codex was driven: one
  subsection per dispatch in document order, per-axis sessions,
  no Claude Code sub-agents. Any audit-surfaced reordering
  suggestion should be flagged but not unilaterally applied.
- The mathlib-free constraint is hard: this project is
  deliberately mathlib-free per `lean/README.md`. "Use mathlib's
  X" is not an acceptable fix recommendation; suggest local
  typed-structure additions instead.

## Pointers (quick navigation)

- Build/validate: `lean/`, `Makefile` (`paper-build`,
  `paper-preflight`, `audit-check`, `audit-regenerate`,
  `validate`, `test`).
- Per-axis Lean trees:
  `lean/SixBirdsDualityConfinement/DualityConfinement/`,
  `lean/SixBirdsDualityConfinement/RH/`.
- Per-axis manifests + section_module_map:
  `lean/manifests/`.
- Inventories + queues + SoR:
  `formalization/`, `paper/notes/statements-of-record.yml`.
- Math artifacts:
  `anti_loc/extracted_math/`.
- Cascade source (large, 431 step dirs): `anti_loc/thread_rh/`.
- Operating-constraint memories:
  `~/.claude/projects/-home-repos-six-birds-duality-confinement/memory/`.
- Phase 0 review (already accepted):
  `reviews/REVIEW_REQUEST_phase0.md`.
- This Phase A-H review:
  `reviews/REVIEW_REQUEST_phaseG.md` (this file).
