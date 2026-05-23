# Phase 0 — Cross-paper asset audit

Status: Phase 0 produced 2026-05-23.

Purpose: enumerate every labeled item in both math artifacts with
per-row classification, and cross-check against the per-axis
inventory and Phase H.4 statements-of-record.

## Source artifacts

| Artifact | Path | Labeled items |
| --- | --- | --- |
| DC math source | `anti_loc/extracted_math/duality_confinement_master.md` | 14 |
| RH math source | `anti_loc/extracted_math/rh_construction.md` | 11 |
| DC inventory | `formalization/inventory/duality_confinement_paper_inventory.toml` | 13 entries |
| RH inventory | `formalization/inventory/rh_paper_inventory.toml` | 11 entries |
| DC manifest | `lean/manifests/duality_confinement_manifest.toml` | 12 entries |
| RH manifest | `lean/manifests/rh_manifest.toml` | 10 entries |
| Statements of record (shared, post Phase H.4) | `paper/notes/statements-of-record.yml` | 24 rows |

**Total cross-paper math labels**: 25 (14 DC + 11 RH).
**Inventory total**: 24 entries (1 DC label intentionally dropped
from inventory; documented below).
**Manifest total**: 22 entries (1 DC inventory row is
`support_only` and has no manifest entry; 1 RH inventory row is
`recognition_source` and is a typed carrier rather than a manifest
theorem/definition).

## Duality Confinement axis — per-label classification

| # | Math label | Section in math artifact | Inventory? | Manifest? | Classification | Target_destination | Notes |
| ---: | --- | --- | --- | :-: | --- | --- | --- |
| 1 | `def:duality_confinement:involutive-object-ledger` | §Involution | Y | Y (definition) | body | body | Spine — the central typed object |
| 2 | `def:duality_confinement:separating-readout` | §Separation | Y | Y (definition) | body | body | |
| 3 | `def:duality_confinement:anti-invariant-ledger` | §AntiInvariantLedger | Y | Y (definition) | body | body | |
| 4 | `lem:duality_confinement:trace-identity` | §AntiInvariantLedger | Y | Y (theorem) | body | body | Definitional unfolding in the typed-cone encoding |
| 5 | `thm:duality_confinement:separation-confinement` | §DirectConfinement | Y | Y (theorem) | body | body | |
| 6 | `thm:duality_confinement:quantitative-confinement` | §DirectConfinement | Y | Y (theorem) | body | body | |
| 7 | `def:duality_confinement:completed-domination-bridge` | §Domination | Y | Y (definition) | body | body | |
| 8 | `thm:duality_confinement:douglas-domination` | §Domination | Y | Y (theorem) | body | body | Typed-cone encoding (audit_summary §A1) |
| 9 | `thm:duality_confinement:master-theorem` | §MasterTheorem | Y | Y (theorem) | **body (headline)** | body | The load-bearing theorem of Paper 1 |
| 10 | `def:duality_confinement:exhaustive-moving-ledger` | §ExhaustiveSqueeze | Y | Y (definition) | body | body | |
| 11 | `thm:duality_confinement:exhaustive-squeeze` | §ExhaustiveSqueeze | Y | Y (theorem) | body | body | |
| 12 | `def:duality_confinement:defected-budget` | §DefectedBudget | Y | N (`support_only`) | **support_only** | appendix | Context for prop:optimized-trace-budget; no manifest entry |
| 13 | `prop:duality_confinement:optimized-trace-budget` | §DefectedBudget | Y | Y (theorem) | body | body | AM-GM as typed-Scalar axiom (audit_summary §A2) |
| 14 | `obl:duality_confinement:sdtc-source` | §Out-of-scope-for-Lean items | **N (dropped)** | N | **out_of_scope_recognition_source (paper-prose only)** | source_only | SDTC structural law itself, paper-prose claim (`sec:scope`, `sec:discussion`); not encoded as Lean entity in DC axis (the RH-specialized `Γ_{SDTC-Selberg}` carrier lives in Paper 2's `RHConditional.lean`) |

**DC counts**:
- 12 `mechanize_now` (rows 1–11 + 13) → all in manifest with
  `faithful` semantic alignment
- 1 `support_only` (row 12) → in inventory, NOT in manifest
- 1 paper-prose-only (row 14) → NOT in inventory, NOT in manifest

## RH axis — per-label classification

| # | Math label | Section in math artifact | Inventory? | Manifest? | Classification | Target_destination | Notes |
| ---: | --- | --- | --- | :-: | --- | --- | --- |
| 1 | `def:rh:fe-involution` | §Involution | Y | Y (definition) | body | body | |
| 2 | `def:rh:psi-minus-rh` | §Involution | Y | Y (definition) | body | body | |
| 3 | `def:rh:nontrivial-zero-ledger` | §ZeroLedger | Y | Y (definition) | body | body | Real-part-type abstraction (audit_summary §A3) |
| 4 | `def:rh:anti-invariant-zero-ledger` | §AntiInvariantZeroLedger | Y | Y (definition) | body | body | |
| 5 | `def:rh:sat-sel-shell` | §SatSelShell | Y | Y (definition) | body | body | Admissibility encoded as opaque `Audit_L` field |
| 6 | `thm:rh:translation-T-forward` | §TranslationT | Y | Y (theorem) | body | body | |
| 7 | `thm:rh:translation-T-reverse` | §TranslationT | Y | Y (theorem) | body | body | |
| 8 | `thm:rh:translation-T` | §TranslationT | Y | Y (theorem) | body | body | Headline equivalence `A_Z(ζ) = 0 ⟺ RH` |
| 9 | `obl:rh:gamma-sdtc-selberg` | §RecognitionSource | Y (`recognition_source`) | N (typed carrier) | **recognition_source** | body | Encoded as `GammaSdtcSelberg` typed structure carrier in `RHConditional.lean` (inline placement per `lean/codex_kickoff.md` §12); NOT a Lean axiom |
| 10 | `thm:rh:dc-master-applied` | §DCMasterApplied | Y | Y (theorem) | body | body | Bridges Paper 1's `masterTheorem` to Sel^!_{ζ,tr} |
| 11 | `thm:rh:conditional` | §RHConditional | Y | Y (theorem) | **body (headline)** | body | The load-bearing conditional theorem `Γ_{SDTC-Selberg} ⟹ RH` |

**RH counts**:
- 10 `mechanize_now` (rows 1–8 + 10–11) → all in manifest with
  `faithful` semantic alignment
- 1 `recognition_source` (row 9) → in inventory; typed carrier
  in Lean (not a manifest theorem/definition)

## Cross-paper boundary (preview; full version in cross-paper-boundary.md)

Paper 2 → Paper 1 (one-way):
- Paper 2 imports Paper 1's master theorem (DC row 9,
  `thm:duality_confinement:master-theorem`) — used by RH row 10
  `thm:rh:dc-master-applied`.
- Paper 2 imports Paper 1's SDTC structural-law framing (DC row 14,
  `obl:duality_confinement:sdtc-source`, paper-prose) as the source
  for the Selberg-class specialization (RH row 9,
  `obl:rh:gamma-sdtc-selberg`).
- Paper 2 imports Paper 1's V-Differential trace-state-only column
  condition (DC row context in `sec:framework`, not a labeled
  inventory item) as substrate classification for RH.

Paper 1 does NOT import any RH-axis label. Paper 1 mentions Paper 2
in two sanctioned forward-reference paragraphs (in
`sec:involutive_ledger` for the RH worked example, and in
`sec:master_theorem` for naming Paper 2 as "the worked
single-substrate validation") with no `\Cref` to Paper-2 labels and
no `TsiokosRH*` bibkey.

## Audit consistency checks

1. **Math labels ↔ inventory**: every inventory label has a math
   artifact origin row (cross-checked above). The single
   intentional asymmetry: `obl:duality_confinement:sdtc-source`
   appears in the DC math artifact but is intentionally NOT in the
   DC inventory (it is a paper-prose-only claim, not a
   mechanization target). Documented in `duality_confinement_master.md`
   §"Out-of-scope-for-Lean items" and inventory header.
2. **Inventory ↔ manifest**: every inventory `mechanize_now` row
   has a manifest entry. The `support_only` row
   (`def:duality_confinement:defected-budget`) is intentionally in
   inventory but not in manifest. The `recognition_source` row
   (`obl:rh:gamma-sdtc-selberg`) is intentionally a typed carrier
   (not a manifest theorem/definition entry).
3. **Statements-of-record cross-check**: post Phase H.4 sync, all
   24 inventory rows have an SoR row; all 22 mechanize_now rows
   have `lean_coverage ∈ {definition, theorem}` and faithful
   semantic alignment; 1 support_only row has `lean_coverage =
   not_mechanized`; 1 recognition_source row has `lean_coverage =
   recognition_source`. Verified by
   `python3 scripts/check_statements_of_record.py --check`
   ("statements-of-record.yml check passed: rows=24, ...,
   manifest cross-check matches, inventory cross-check matches").

No asymmetries beyond those documented above.

## Target-paper distribution

| Target paper | Inventory rows | Headline labels |
| --- | ---: | --- |
| Duality Confinement (Paper 1) | 13 (12 mechanize_now + 1 support_only) | `thm:duality_confinement:master-theorem` |
| RH (Paper 2) | 11 (10 mechanize_now + 1 recognition_source) | `thm:rh:conditional` (and `thm:rh:translation-T` as the construction-grade headline) |
| Dropped (paper-prose only) | 1 (DC row 14, `obl:duality_confinement:sdtc-source`) | n/a (paper-prose section, not a labeled inventory row) |
| **Total** | 25 math labels → 24 inventory rows → 22 manifest entries | |

## Target-destination distribution

| Destination | DC | RH | Total |
| --- | ---: | ---: | ---: |
| body | 12 | 11 | 23 |
| appendix | 1 (defected-budget support_only) | 0 | 1 |
| source_only | 0 | 0 | 0 |
| evidence_pack_only | 0 | 0 | 0 |
| **Total** | 13 | 11 | 24 |

The DC paper-prose-only row 14 (`obl:duality_confinement:sdtc-source`)
is NOT counted in the destination distribution because it is not an
inventory row; it is a body claim of Paper 1's `sec:master_theorem` /
`sec:scope` / `sec:discussion` sections (the SDTC structural law as
named recognition source).

## Findings / decisions

1. The asset audit confirms the SoR is consistent with the math
   artifacts and manifests.
2. The single intentional inventory omission
   (`obl:duality_confinement:sdtc-source`) is documented and
   defensible: the SDTC structural law is body-prose recognition
   content, not a mechanization target on the DC axis.
3. The three encoding-disclosure notes from audit_summary
   (§A1 Douglas factorization typed-cone encoding; §A2 AM-GM as
   typed-Scalar axiom; §A3 real-part-type abstraction for RH) must
   be carried into body prose during the drafting arc; they are
   tagged in the SoR `notes` field and will be reinforced via
   `paper/notes/proof-presentation-policy.md` during Phase 6.
4. **No further per-axis inventory adjustments needed.** The Phase
   H.4 SoR sync is the authoritative state.

## Phase 0 deliverables checklist

- [x] `paper/notes/phase0-asset-audit.md` (this file)
- [ ] `paper/duality_confinement/notes/contract.md` (preliminary
  draft exists; review at Phase 0 sign-off)
- [ ] `paper/rh/notes/contract.md` (new; produce during Phase 0)
- [ ] `paper/notes/cross-paper-boundary.md` (new; produce during
  Phase 0)
- [ ] `paper/notes/out-of-scope-ledger.md` (new; produce during
  Phase 0)

## Phase 0 close

Pending production of the four remaining deliverables.
