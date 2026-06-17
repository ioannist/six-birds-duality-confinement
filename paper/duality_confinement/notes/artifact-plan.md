# Artifact Plan: Duality Confinement (Paper 1)

Status: Phase 9 produced 2026-05-23 (paper-writing prep arc closed).

Purpose: track the artifacts the paper references and the canonical
locations to cite. Body prose refers to artifacts by descriptive
role (per `feedback_academic_register.md`); this file gives the
machine-readable provenance that App D's coverage tables resolve.

## Math source artifacts

| Body role | Repo path | Notes |
| --- | --- | --- |
| Per-axis math artifact (Paper 1's source-of-record) | `anti_loc/extracted_math/duality_confinement_master.md` | Phase A consolidation; 8 sections matching queue sections (Involution → DefectedBudget) |
| Phase B audit summary (representation choices §A1–A3) | `anti_loc/extracted_math/audit_summary.md` | Cited in App D representation-notes table |
| Cross-axis math dependency map | `anti_loc/extracted_math/dependency_map.md` | Cited in `sec:framework` for cascade-step provenance |
| Original proposal | `anti_loc/paper_proposal_self_dual_trace_confinement.md` | Cited in `sec:intro` framing; revised wording per `claim-revision-register.md` |

## Lean source artifacts (cited in App D)

Per `paper/notes/statements-of-record.yml` filtered for
`target_paper = duality_confinement`. App D's coverage table renders
the 13 rows below. Long Lean decl strings ONLY appear in App D
tables (per `feedback_table_typesetting.md`).

| Paper label | Lean module path | Lean decl |
| --- | --- | --- |
| `def:duality_confinement:involutive-object-ledger` | `lean/SixBirdsDualityConfinement/DualityConfinement/Involution.lean` | `SixBirdsDualityConfinement.DualityConfinement.Involution.InvolutiveObjectLedger` |
| `def:duality_confinement:separating-readout` | `lean/SixBirdsDualityConfinement/DualityConfinement/Separation.lean` | `SixBirdsDualityConfinement.DualityConfinement.Separation.SeparatingReadout` |
| `def:duality_confinement:anti-invariant-ledger` | `lean/SixBirdsDualityConfinement/DualityConfinement/AntiInvariantLedger.lean` | `SixBirdsDualityConfinement.DualityConfinement.AntiInvariantLedger.AntiInvariantLedger` |
| `lem:duality_confinement:trace-identity` | (same file) | `SixBirdsDualityConfinement.DualityConfinement.AntiInvariantLedger.traceIdentity` |
| `thm:duality_confinement:separation-confinement` | `lean/SixBirdsDualityConfinement/DualityConfinement/DirectConfinement.lean` | `SixBirdsDualityConfinement.DualityConfinement.DirectConfinement.separationConfinement` |
| `thm:duality_confinement:quantitative-confinement` | (same file) | `SixBirdsDualityConfinement.DualityConfinement.DirectConfinement.quantitativeConfinement` |
| `def:duality_confinement:completed-domination-bridge` | `lean/SixBirdsDualityConfinement/DualityConfinement/Domination.lean` | `SixBirdsDualityConfinement.DualityConfinement.Domination.CompletedDominationBridge` |
| `thm:duality_confinement:douglas-domination` | (same file) | `SixBirdsDualityConfinement.DualityConfinement.Domination.douglasDomination` |
| `thm:duality_confinement:master-theorem` | `lean/SixBirdsDualityConfinement/DualityConfinement/MasterTheorem.lean` | `SixBirdsDualityConfinement.DualityConfinement.MasterTheorem.masterTheorem` |
| `def:duality_confinement:exhaustive-moving-ledger` | `lean/SixBirdsDualityConfinement/DualityConfinement/ExhaustiveSqueeze.lean` | `SixBirdsDualityConfinement.DualityConfinement.ExhaustiveSqueeze.ExhaustiveMovingLedger` |
| `thm:duality_confinement:exhaustive-squeeze` | (same file) | `SixBirdsDualityConfinement.DualityConfinement.ExhaustiveSqueeze.exhaustiveSqueeze` |
| `def:duality_confinement:defected-budget` | `lean/SixBirdsDualityConfinement/DualityConfinement/DefectedBudget.lean` | (support_only; no manifest entry; no Lean decl cited in body) |
| `prop:duality_confinement:optimized-trace-budget` | (same file) | `SixBirdsDualityConfinement.DualityConfinement.DefectedBudget.optimizedTraceBudget` |

## Manifest / inventory / queue artifacts (machine-readable bookkeeping)

| Role | Path |
| --- | --- |
| Per-axis manifest | `lean/manifests/duality_confinement_manifest.toml` |
| Per-axis paper inventory | `formalization/inventory/duality_confinement_paper_inventory.toml` |
| Per-axis mechanization queue | `formalization/traceability/queue_duality_confinement.csv` |
| Foundations cross-walk | `formalization/inventory/imported_foundations.yml` |
| Trust base | `lean/manifests/trust_base.txt` |
| Statements-of-record (shared, but filtered for DC) | `paper/notes/statements-of-record.yml` |
| Section-module map | `lean/manifests/section_module_map.toml` (axis `duality_confinement`) |

## Foundations dependencies (used by the DC Lean modules)

Per `formalization/inventory/imported_foundations.yml`, the DC axis
imports from:
- Foundations I (`ClosureLadder`) — closure operator / closure
  ladder / idempotent endomap / quotient packaging
- Foundations II (`SixBirds`) — channel status, FATCD, role,
  scoped exact six, typed non collapse
- Foundations III (`SixBirdsIII`) — BirdInt domain, primitive
  labels, promotion / claim / gate status families, promotion
  bridge record, claim record, defect record, level trichotomy,
  host taxonomy, directed cell record, top-down channel record,
  threshold tag, visibility tag, strict gate status, square status

These appear in App D as the foundations-citation block. Body prose
does NOT inline the foundations-cross-walk identifiers per
`feedback_academic_register.md`.

## Reproducibility-statement note

A small "code and data availability" subsection in `sec:conclusion`
(or as the last paragraph of `sec:discussion`) states:
- The Lean mechanization is at the public repo
  `https://github.com/ioannist/six-birds-duality-confinement`
- The math artifacts at `anti_loc/extracted_math/` are the
  source-of-record for paper claims
- The per-axis manifests at `lean/manifests/` enumerate the
  formally tracked entries
- The Phase H closure (full validator chain + axiom audit + Phase
  G/H REVISE fixes) was completed 2026-05-23

This is a SINGLE paragraph statement (per `feedback_academic_register.md`),
not a repeated artifact-path inventory.

## What does NOT belong in the paper body

Per `feedback_academic_register.md`:
- Internal verdict tokens (e.g. "verdict np604", "diagnosis-grade")
- JSON / TOML / YAML file paths
- Lean module path strings outside App D
- Cascade step identifiers (e.g. "step 69", "steps 437–447") —
  these appear in `sec:scope` as part of the cascade documentation
  reference but with minimal use (single sentence). The
  cascade-step provenance lives in `paper/duality_confinement/notes/artifact-plan.md`
  (this file), not in body prose.
- Ticket IDs or branch identifiers
- Lean trust-base axiom names (mentioned once in App D, not in body)
