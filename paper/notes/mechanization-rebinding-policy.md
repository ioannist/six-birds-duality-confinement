# Mechanization Rebinding Policy

Status: Phase 7 produced 2026-05-23.

Purpose: how the manifest's `(paper_label, lean_decl, status, notes)`
tuples surface in each paper. This file binds the Lean-side
mechanization state (manifests + inventory + statements-of-record)
to the paper-side prose disclosure discipline (per
`paper/notes/proof-presentation-policy.md`).

The mechanization state is fixed (Phase A–H of `PLAN_mechanization.md`
closed 2026-05-23 with 22 manifest entries, all 22 carrying
`faithful` semantic alignment after Phase H.4 sync, plus 1
support_only and 1 recognition_source in the inventory). This file
specifies how that state is rebound for paper-side disclosure.

## Per-label rebinding (summary; details in
`paper/notes/proof-presentation-policy.md`)

### Duality Confinement axis

| Paper label | Inventory class | Manifest status | Paper disclosure mode | Paper-side wording (canonical) |
| --- | --- | --- | --- | --- |
| `def:duality_confinement:involutive-object-ledger` | `mechanize_now` | `definition` | `definition_entry` | "realized in Lean as `InvolutiveObjectLedger`" |
| `def:duality_confinement:separating-readout` | `mechanize_now` | `definition` | `definition_entry` | "realized in Lean as `SeparatingReadout`" |
| `def:duality_confinement:anti-invariant-ledger` | `mechanize_now` | `definition` | `definition_entry` | "realized in Lean as `AntiInvariantLedger` over the typed positive cone" |
| `lem:duality_confinement:trace-identity` | `mechanize_now` | `theorem` (definitional unfolding in typed-cone encoding) | `lean_substantive` | "Lean verifies the trace identity as `traceIdentity`" |
| `thm:duality_confinement:separation-confinement` | `mechanize_now` | `theorem` | `lean_substantive` | "Lean proves the separation–confinement theorem as `separationConfinement`" |
| `thm:duality_confinement:quantitative-confinement` | `mechanize_now` | `theorem` | `lean_substantive` | "Lean proves the quantitative-confinement bound as `quantitativeConfinement`" |
| `def:duality_confinement:completed-domination-bridge` | `mechanize_now` | `definition` | `definition_entry` | "realized in Lean as `CompletedDominationBridge`" |
| `thm:duality_confinement:douglas-domination` | `mechanize_now` | `theorem` (typed-cone encoding per `audit_summary.md` §A1) | `lean_substantive` | "Lean derives Douglas factorization at the typed-cone level as `douglasDomination` (per the typed-cone encoding choice; the classical Douglas factorization (Douglas 1966) is the underlying operator-theoretic content)" |
| `thm:duality_confinement:master-theorem` | `mechanize_now` | `theorem` | `lean_substantive` | "Lean proves the duality-confinement master theorem as `masterTheorem`; the typed-cone abstraction is disclosed inline" |
| `def:duality_confinement:exhaustive-moving-ledger` | `mechanize_now` | `definition` | `definition_entry` | "realized in Lean as `ExhaustiveMovingLedger`" |
| `thm:duality_confinement:exhaustive-squeeze` | `mechanize_now` | `theorem` | `lean_substantive` | "Lean proves the exhaustive squeeze as `exhaustiveSqueeze`" |
| `def:duality_confinement:defected-budget` | `support_only` | (no manifest entry) | `definition_entry` | NO Lean citation. Body prose introduces the defected-budget shape as motivation for the optimized scalar trace budget, without claiming Lean coverage |
| `prop:duality_confinement:optimized-trace-budget` | `mechanize_now` | `theorem` (AM-GM as typed-Scalar axiom per `audit_summary.md` §A2) | `lean_substantive` | "the optimized scalar trace budget is **tracked by the formalization harness** as `optimizedTraceBudget`; the AM-GM step is taken as typed-Scalar axiom (a substantive derivation requires typed real-arithmetic structure)" |

### RH axis

| Paper label | Inventory class | Manifest status | Paper disclosure mode | Paper-side wording (canonical) |
| --- | --- | --- | --- | --- |
| `def:rh:fe-involution` | `mechanize_now` | `definition` | `definition_entry` | "realized in Lean as `feInvolution`" |
| `def:rh:psi-minus-rh` | `mechanize_now` | `definition` | `definition_entry` | "realized in Lean as `psiMinusRh`" |
| `def:rh:nontrivial-zero-ledger` | `mechanize_now` | `definition` | `definition_entry` | "realized in Lean as `NontrivialZeroLedger` over a typed `RealCoordinate` (per `audit_summary.md` §A3: the real-part coordinate is parameterized; identification with actual ℝ-valued real parts of nontrivial zeros of ζ is by construction-parameter assignment)" |
| `def:rh:anti-invariant-zero-ledger` | `mechanize_now` | `definition` | `definition_entry` | "realized in Lean as `AntiInvariantZeroLedger`" |
| `def:rh:sat-sel-shell` | `mechanize_now` | `definition` | `definition_entry` | "realized in Lean as `SatSelShell`; admissibility per the seven Foundations II schemas is encoded as the opaque `Audit_L` field, not derived in this paper" |
| `thm:rh:translation-T-forward` | `mechanize_now` | `theorem` | `lean_substantive` | "Lean proves the forward direction of Theorem T as `translationTForward`" |
| `thm:rh:translation-T-reverse` | `mechanize_now` | `theorem` | `lean_substantive` | "Lean proves the reverse direction of Theorem T as `translationTReverse`" |
| `thm:rh:translation-T` | `mechanize_now` | `theorem` | `lean_substantive` | "Lean proves the translation theorem T as `translationT` (combining forward and reverse)" |
| `obl:rh:gamma-sdtc-selberg` | `out_of_scope_recognition_source` | (no manifest entry; typed structure carrier) | `appendix_only` | "the recognition source `Γ_{SDTC-Selberg}` is supplied by Paper 1's SDTC structural law applied to the Selberg-class instance; encoded in Lean as a typed structure carrier `GammaSdtcSelberg` declared inline in `RHConditional.lean` (per `lean/codex_kickoff.md` §12 — type lives next to its only consumer). NOT a Lean axiom; the forbidden-tokens rule bans `axiom`/`opaque`/`constant`/`sorry`/`admit` everywhere in the source tree" |
| `thm:rh:dc-master-applied` | `mechanize_now` | `theorem` | `lean_substantive` | "Lean derives the RH-specific application of the master theorem as `dcMasterApplied`, instantiating Paper 1 [1]'s `masterTheorem` on the RH zero ledger via the bridge parameter `mu_zero_of_ae`" |
| `thm:rh:conditional` | `mechanize_now` | `theorem` | `lean_substantive` | "Lean proves the conditional landing chain `Γ_{SDTC-Selberg} ⟹ RH` as `rhConditional`, with the recognition source supplied as an explicit hypothesis parameter `γ : GammaSdtcSelberg shell`" |

## Cross-paper rebinding for the DC master theorem

Paper 2 imports `thm:duality_confinement:master-theorem` from
Paper 1. The rebinding for the cross-paper citation:

- In Paper 1's `app:formalization`: the master theorem appears as
  a row with the full Lean decl
  `SixBirdsDualityConfinement.DualityConfinement.MasterTheorem.masterTheorem`.
- In Paper 2's `sec:landing_chain`: the master theorem statement
  is reproduced verbatim (not paraphrased) with a citation to
  Paper 1 [1] § master-theorem section.
- In Paper 2's `app:formalization` row for `thm:rh:dc-master-applied`:
  the Lean decl
  `SixBirdsDualityConfinement.RH.DCMasterApplied.dcMasterApplied`
  is documented as importing
  `SixBirdsDualityConfinement.DualityConfinement.MasterTheorem.masterTheorem`
  from Paper 1.

## Discipline rules

1. **No silent paraphrase of mechanized statements.** Body prose
   reproduces the Lean statement's content (in standard
   mathematical language per `paper/notes/audience-translation.md`)
   without weakening or strengthening. If the body prose says
   something different from what Lean proves, it must say so
   explicitly (e.g., "Lean proves X under typed-cone abstraction;
   the operator-theoretic generalization Y is open extension").
2. **No Lean identifier strings in body prose.** Per
   `feedback_academic_register.md`: Lean decl names appear in
   `app:formalization` tables only. Body prose uses paper-prose
   names from `paper/notes/prose-names.md`.
3. **Wording discipline per `paper/notes/proof-presentation-policy.md`.**
   Body and App D both apply the wording table; the table is the
   single canonical source for "Lean proves" vs "tracked by the
   formalization harness" vs "realized in Lean as ..." vs
   "encoded as a typed structure carrier" vs no-Lean-mention.
4. **Representation notes from `audit_summary.md` carry into body.**
   - §A1 Douglas factorization typed-cone encoding (Paper 1
     `sec:domination`)
   - §A2 AM-GM as typed-Scalar axiom (Paper 1
     `sec:exhaustive_squeeze_and_budgets`)
   - §A3 real-part-type abstraction (Paper 2
     `sec:involution_and_ledger`)
   Body prose discloses each note when the relevant Lean entry is
   first cited; App D documents the notes in full.
5. **Recognition source rebinding.** `obl:rh:gamma-sdtc-selberg`
   uses the typed-structure-carrier wording (NOT "Lean axiom",
   NOT "Lean proves"). The carrier placement is canonically inline
   in `RHConditional.lean` (per `lean/codex_kickoff.md` §12); the
   paper-side App D row documents this placement.

## Boundary: out-of-scope-for-this-rebinding

This rebinding policy covers ONLY the 22 manifest entries + 1
support_only + 1 recognition_source. It does NOT cover:
- Foundations II / III declarations cited in App D (e.g., F3
  visibility tags via `F3VisibilityTag` aliases in
  `Terminology.lean`). Those are vendored foundations references;
  the paper-side citation is to the Foundations II/III bibkeys.
- The DC paper's out-of-scope claim `obl:duality_confinement:sdtc-source`
  (the SDTC structural law itself as paper-prose claim). This is
  NOT in the DC inventory and NOT in any manifest; it is body-prose
  recognition content in Paper 1's `sec:master_theorem`,
  `sec:scope`, and `sec:discussion`. The rebinding for this claim
  is purely paper-prose (no Lean citation at all).
- Future-work mechanization extensions (operator-theoretic
  generality, substantive AM-GM derivation, cross-substrate
  validations, GRH, Sel admissibility derivation, parameter-
  identification work). These are flagged in `sec:scope` /
  `sec:scope_and_nonclaims` and `sec:discussion` per paper; no
  Lean entries exist for them and no rebinding applies.

## Validation

The rebinding policy is consistent with:
- `paper/notes/statements-of-record.yml` (Phase H.4 sync;
  authoritative SoR state)
- `lean/manifests/duality_confinement_manifest.toml` (12 entries)
- `lean/manifests/rh_manifest.toml` (10 entries)
- `formalization/inventory/duality_confinement_paper_inventory.toml`
  (13 entries)
- `formalization/inventory/rh_paper_inventory.toml` (11 entries)
- `paper/notes/proof-presentation-policy.md` (4-mode wording table)
- `anti_loc/extracted_math/audit_summary.md` (3 representation
  notes A1–A3)

Cross-validation per `paper/notes/phase0-asset-audit.md` confirms
no asymmetries beyond the documented intentional ones.
