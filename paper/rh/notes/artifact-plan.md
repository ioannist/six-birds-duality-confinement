# Artifact Plan: RH closure (Paper 2)

Status: Phase 9 produced 2026-05-23 (paper-writing prep arc closed).

Purpose: track the artifacts the paper references and the canonical
locations to cite. Body prose refers to artifacts by descriptive
role (per `feedback_academic_register.md`); this file gives the
machine-readable provenance that App D's coverage tables resolve.

## Math source artifacts

| Body role | Repo path | Notes |
| --- | --- | --- |
| Per-axis math artifact (Paper 2's source-of-record) | `anti_loc/extracted_math/rh_construction.md` | Phase A consolidation; 7 sections matching queue sections (Involution → RHConditional) |
| Phase B audit summary (representation choice §A3) | `anti_loc/extracted_math/audit_summary.md` | Cited in App D representation-notes table (real-part-type abstraction) |
| Cross-axis math dependency map | `anti_loc/extracted_math/dependency_map.md` | Cited in `sec:framework` for cross-axis context |
| Original proposal | `anti_loc/paper_proposal_rh_via_sdtc_selberg.md` | Cited in `sec:intro` framing; revised wording per `claim-revision-register.md` |
| Paper 1 math artifact (cross-paper) | `anti_loc/extracted_math/duality_confinement_master.md` | The master theorem source. Body prose cites it as `[1]` via the SDTC sibling bibkey, not by repo path |

## Lean source artifacts (cited in App D)

Per `paper/notes/statements-of-record.yml` filtered for
`target_paper = rh`. App D's coverage table renders the 11 rows
below. Long Lean decl strings ONLY appear in App D tables (per
`feedback_table_typesetting.md`).

| Paper label | Lean module path | Lean decl |
| --- | --- | --- |
| `def:rh:fe-involution` | `lean/SixBirdsDualityConfinement/RH/Involution.lean` | `SixBirdsDualityConfinement.RH.Involution.feInvolution` |
| `def:rh:psi-minus-rh` | (same file) | `SixBirdsDualityConfinement.RH.Involution.psiMinusRh` |
| `def:rh:nontrivial-zero-ledger` | `lean/SixBirdsDualityConfinement/RH/ZeroLedger.lean` | `SixBirdsDualityConfinement.RH.ZeroLedger.NontrivialZeroLedger` |
| `def:rh:anti-invariant-zero-ledger` | `lean/SixBirdsDualityConfinement/RH/AntiInvariantZeroLedger.lean` | `SixBirdsDualityConfinement.RH.AntiInvariantZeroLedger.AntiInvariantZeroLedger` |
| `def:rh:sat-sel-shell` | `lean/SixBirdsDualityConfinement/RH/SatSelShell.lean` | `SixBirdsDualityConfinement.RH.SatSelShell.SatSelShell` |
| `thm:rh:translation-T-forward` | `lean/SixBirdsDualityConfinement/RH/TranslationT.lean` | `SixBirdsDualityConfinement.RH.TranslationT.translationTForward` |
| `thm:rh:translation-T-reverse` | (same file) | `SixBirdsDualityConfinement.RH.TranslationT.translationTReverse` |
| `thm:rh:translation-T` | (same file) | `SixBirdsDualityConfinement.RH.TranslationT.translationT` |
| `obl:rh:gamma-sdtc-selberg` | `lean/SixBirdsDualityConfinement/RH/RHConditional.lean` | `SixBirdsDualityConfinement.RH.RHConditional.GammaSdtcSelberg` (typed structure carrier; inline placement per `lean/codex_kickoff.md` §12) |
| `thm:rh:dc-master-applied` | `lean/SixBirdsDualityConfinement/RH/DCMasterApplied.lean` | `SixBirdsDualityConfinement.RH.DCMasterApplied.dcMasterApplied` (imports `SixBirdsDualityConfinement.DualityConfinement.MasterTheorem.masterTheorem` from Paper 1) |
| `thm:rh:conditional` | `lean/SixBirdsDualityConfinement/RH/RHConditional.lean` | `SixBirdsDualityConfinement.RH.RHConditional.rhConditional` (takes `γ : GammaSdtcSelberg shell` as explicit hypothesis parameter) |

## Manifest / inventory / queue artifacts (machine-readable bookkeeping)

| Role | Path |
| --- | --- |
| Per-axis manifest | `lean/manifests/rh_manifest.toml` |
| Per-axis paper inventory | `formalization/inventory/rh_paper_inventory.toml` |
| Per-axis mechanization queue | `formalization/traceability/queue_rh.csv` |
| Foundations cross-walk | `formalization/inventory/imported_foundations.yml` |
| Trust base | `lean/manifests/trust_base.txt` |
| Statements-of-record (shared, but filtered for RH) | `paper/notes/statements-of-record.yml` |
| Section-module map | `lean/manifests/section_module_map.toml` (axis `rh`) |

## Cross-paper artifacts (Paper 1 imports)

Paper 2 imports the duality-confinement master theorem from Paper
1. The cross-paper rebinding is governed by
`paper/notes/mechanization-rebinding-policy.md`.

| Cross-paper artifact | Used by | Disclosure |
| --- | --- | --- |
| Paper 1's `masterTheorem` | `dcMasterApplied` (Lean import) | Body prose in `sec:landing_chain` reproduces the master theorem statement verbatim, with citation to Paper 1 [1] (`TsiokosSDTC2026`) and to Paper 1's §master_theorem |
| Paper 1's SDTC structural law (paper-prose only; no Lean entity in DC axis) | `sec:framework`, `sec:recognition_source` | Paper-prose citation `[1]`; the recognition source `Γ_{SDTC-Selberg}` in Paper 2 is the Selberg-class instance of this paper-prose claim |
| Paper 1's V-Differential trace-state-only column condition (paper-prose only) | `sec:framework` | Paper-prose citation `[1]` to Paper 1's §framework |
| Paper 1's three-option derivation sweep (paper-prose only) | `sec:recognition_source`, `sec:scope_and_nonclaims` | Paper-prose citation `[1]`; no `\Cref` to Paper 1 internal labels |

## Foundations dependencies (used by the RH Lean modules)

Per `formalization/inventory/imported_foundations.yml`, the RH axis
imports from:

- Foundations I (`ClosureLadder`) — closure operator / closure
  ladder / idempotent endomap / quotient packaging
- Foundations II (`SixBirds`) — channel status, FATCD, role,
  scoped exact six, typed non collapse; admissibility schemas
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
  `https://github.com/ioannist/six-birds-duality-confinement` (same
  repo as Paper 1)
- The math artifacts at `anti_loc/extracted_math/` are the
  source-of-record for paper claims
- The per-axis manifests at `lean/manifests/` enumerate the
  formally tracked entries
- The Phase H closure (full validator chain + axiom audit + Phase
  G/H REVISE fixes) was completed 2026-05-23
- The recognition source `Γ_{SDTC-Selberg}` is realized as a typed
  structure carrier (`GammaSdtcSelberg`) declared inline in
  `RHConditional.lean`; the mathlib-free, forbidden-tokens-rule
  encoding bans `axiom`/`opaque`/`constant`/`sorry`/`admit`

This is a SINGLE paragraph statement (per `feedback_academic_register.md`),
not a repeated artifact-path inventory.

## What does NOT belong in the paper body

Per `feedback_academic_register.md`:

- Internal verdict tokens (e.g. "verdict np604", "diagnosis-grade")
- JSON / TOML / YAML file paths
- Lean module path strings outside App D
- Cascade step identifiers (e.g. "step 451", "steps 441–447") —
  these appear only as paper-prose "the cascade's three-option
  derivation sweep documented in the development history" wording
  in `sec:recognition_source` and `sec:scope_and_nonclaims`. The
  cascade-step provenance lives in this artifact-plan file, not in
  body prose.
- Ticket IDs or branch identifiers
- Lean trust-base axiom names (mentioned once in App D, not in body)
- Cross-paper `\Cref` to Paper 1 internal labels (Paper 1's labels
  are not in Paper 2's `\Cref` namespace; cross-paper references
  use `\cite{TsiokosSDTC2026}` plus paper-prose pointer)
- Direct `axiom` / `opaque` / `constant` references for the
  recognition source (the forbidden-tokens rule bans these in the
  Lean source; body prose discloses via the typed-structure-carrier
  wording per `paper/notes/mechanization-rebinding-policy.md`)
