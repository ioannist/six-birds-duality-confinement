# Statements of Record (review-friendly rendering)

Status: Phase 2 produced 2026-05-23.

Purpose: human-readable rendering of `paper/notes/statements-of-record.yml`.
The yaml is the authoritative source; this markdown is the
review-facing summary table for sign-off.

Schema overview (per `scripts/check_statements_of_record.py`):
- `paper_label`: stable label like `def:duality_confinement:involutive-object-ledger`
- `env_kind`: definition / theorem / lemma / proposition / corollary / obligation
- `source_file`: `anti_loc/extracted_math/<axis>_*.md`
- `source_section`: e.g. `Involution`, `MasterTheorem`
- `theorem_title`: human-readable name
- `target_paper`: `duality_confinement` / `rh` / `dropped`
- `target_destination`: `body` / `appendix` / `source_only` / `evidence_pack_only`
- `target_section_hint`: e.g. `Involution`, `RHConditional`
- `proof_presentation`: `body_full` / `body_sketch` / `appendix_only` /
  `lean_substantive` / `lean_traceability_only` / `standard_reference` /
  `definition_entry`
- `lean_coverage`: `definition` / `theorem` / `partial` / `not_mechanized` /
  `recognition_source` / `obligation`
- `lean_decl`: fully-qualified Lean declaration name
- `semantic_alignment`: `faithful` / `narrowed_surrogate` /
  `weakened_genericized` / `needs_strengthening` / `projection_packaged` /
  `not_applicable`
- `notes`: drafting hints / disclosure flags

Validator status (post Phase H.4 sync):
- rows=24, target_paper={duality_confinement:13, rh:11, dropped:0}
- mechanized=23, not_mechanized=1
- manifest cross-check: duality_confinement=12, rh=10 (matches)
- inventory cross-check: duality_confinement=13, rh=11 (matches)

## Duality Confinement axis — 13 rows

| # | paper_label | env_kind | target_section_hint | proof_presentation | lean_coverage | semantic_alignment | notes |
| --: | --- | --- | --- | --- | --- | --- | --- |
| 1 | `def:duality_confinement:involutive-object-ledger` | definition | Involution | definition_entry | definition | faithful | Phase G mechanize_now per inventory; central typed object |
| 2 | `def:duality_confinement:separating-readout` | definition | Separation | definition_entry | definition | faithful | Both qualitative and quantitative encoded |
| 3 | `def:duality_confinement:anti-invariant-ledger` | definition | AntiInvariantLedger | definition_entry | definition | faithful | Typed positive cone encoding with explicit trace functional (audit_summary §A1 representation note) |
| 4 | `lem:duality_confinement:trace-identity` | lemma | AntiInvariantLedger | lean_substantive | theorem | faithful | Definitional unfolding in the typed-cone encoding |
| 5 | `thm:duality_confinement:separation-confinement` | theorem | DirectConfinement | lean_substantive | theorem | faithful | |
| 6 | `thm:duality_confinement:quantitative-confinement` | theorem | DirectConfinement | lean_substantive | theorem | faithful | Markov consequence of the trace identity |
| 7 | `def:duality_confinement:completed-domination-bridge` | definition | Domination | definition_entry | definition | faithful | |
| 8 | `thm:duality_confinement:douglas-domination` | theorem | Domination | lean_substantive | theorem | faithful | Typed-cone encoding via `DouglasData` carrier (audit_summary §A1) |
| 9 | `thm:duality_confinement:master-theorem` | theorem | MasterTheorem | lean_substantive | theorem | faithful | **HEADLINE — load-bearing master theorem**; reused by RH axis as `thm:rh:dc-master-applied` |
| 10 | `def:duality_confinement:exhaustive-moving-ledger` | definition | ExhaustiveSqueeze | definition_entry | definition | faithful | |
| 11 | `thm:duality_confinement:exhaustive-squeeze` | theorem | ExhaustiveSqueeze | lean_substantive | theorem | faithful | |
| 12 | `def:duality_confinement:defected-budget` | definition | DefectedBudget | definition_entry | **not_mechanized** | not_applicable | `support_only` per inventory; no Lean decl; body prose introduces the shape as motivation for `prop:duality_confinement:optimized-trace-budget` |
| 13 | `prop:duality_confinement:optimized-trace-budget` | proposition | DefectedBudget | lean_substantive | theorem | faithful | AM-GM step taken as typed-Scalar axiom (audit_summary §A2); disclosure wording "tracked by the formalization harness" |

DC counts:
- definition_entry: 6 (rows 1, 2, 3, 7, 10, 12)
- lean_substantive: 7 (rows 4, 5, 6, 8, 9, 11, 13)
- appendix_only: 0
- definition: 5 (rows 1, 2, 3, 7, 10)
- theorem: 7 (rows 4, 5, 6, 8, 9, 11, 13)
- not_mechanized: 1 (row 12)
- faithful: 12
- not_applicable: 1
- target_destination = body: 12
- target_destination = appendix: 1 (row 12, defected-budget context)

## RH axis — 11 rows

| # | paper_label | env_kind | target_section_hint | proof_presentation | lean_coverage | semantic_alignment | notes |
| --: | --- | --- | --- | --- | --- | --- | --- |
| 14 | `def:rh:fe-involution` | definition | Involution | definition_entry | definition | faithful | `J_L(s) = 1 - \bar{s}`; involutive + critical-line fixed locus + RH involution disclosures (audit_summary §A3 real-part-type abstraction) |
| 15 | `def:rh:psi-minus-rh` | definition | Involution | definition_entry | definition | faithful | Anti-invariant readout `\psi_-(s) = Re(s) - 1/2` |
| 16 | `def:rh:nontrivial-zero-ledger` | definition | ZeroLedger | definition_entry | definition | faithful | Typed multiset with `m_\rho > 0` multiplicities; `Λ_ζ` opaque |
| 17 | `def:rh:anti-invariant-zero-ledger` | definition | AntiInvariantZeroLedger | definition_entry | definition | faithful | `A_Z(ζ) = Σ_ρ m_ρ |Re(ρ) - 1/2|²` |
| 18 | `def:rh:sat-sel-shell` | definition | SatSelShell | definition_entry | definition | faithful | 13-field typed shell; admissibility encoded as opaque `Audit_L` field |
| 19 | `thm:rh:translation-T-forward` | theorem | TranslationT | lean_substantive | theorem | faithful | `A_Z(ζ) = 0 ⟹ ∀ρ, Re(ρ) = 1/2` |
| 20 | `thm:rh:translation-T-reverse` | theorem | TranslationT | lean_substantive | theorem | faithful | `∀ρ, Re(ρ) = 1/2 ⟹ A_Z(ζ) = 0` |
| 21 | `thm:rh:translation-T` | theorem | TranslationT | lean_substantive | theorem | faithful | Biconditional combining 19 + 20; the construction-grade headline |
| 22 | `obl:rh:gamma-sdtc-selberg` | obligation | RecognitionSource | appendix_only | **recognition_source** | not_applicable | Typed structure carrier `GammaSdtcSelberg` declared inline in `RHConditional.lean` (per kickoff §12 sanctioned inline placement); NOT a Lean axiom |
| 23 | `thm:rh:dc-master-applied` | theorem | DCMasterApplied | lean_substantive | theorem | faithful | Bridges Paper 1's `masterTheorem` to `Sel^!_{ζ,tr}` via `mu_zero_of_ae` parameter |
| 24 | `thm:rh:conditional` | theorem | RHConditional | lean_substantive | theorem | faithful | **HEADLINE — conditional landing chain**; takes `γ : GammaSdtcSelberg shell` as explicit hypothesis |

RH counts:
- definition_entry: 5 (rows 14, 15, 16, 17, 18)
- lean_substantive: 5 (rows 19, 20, 21, 23, 24)
- appendix_only: 1 (row 22)
- definition: 5 (rows 14, 15, 16, 17, 18)
- theorem: 5 (rows 19, 20, 21, 23, 24)
- recognition_source: 1 (row 22)
- faithful: 10
- not_applicable: 1
- target_destination = body: 11

## Aggregate counts

| Field | DC | RH | Total |
| --- | ---: | ---: | ---: |
| Rows | 13 | 11 | 24 |
| `lean_coverage = theorem` | 7 | 5 | 12 |
| `lean_coverage = definition` | 5 | 5 | 10 |
| `lean_coverage = recognition_source` | 0 | 1 | 1 |
| `lean_coverage = not_mechanized` | 1 | 0 | 1 |
| `semantic_alignment = faithful` | 12 | 10 | 22 |
| `semantic_alignment = not_applicable` | 1 | 1 | 2 |
| `target_destination = body` | 12 | 11 | 23 |
| `target_destination = appendix` | 1 | 0 | 1 |
| `proof_presentation = lean_substantive` | 7 | 5 | 12 |
| `proof_presentation = definition_entry` | 6 | 5 | 11 |
| `proof_presentation = appendix_only` | 0 | 1 | 1 |
| **Headline theorems** | `thm:duality_confinement:master-theorem` | `thm:rh:conditional` (+ `thm:rh:translation-T` construction-grade) | — |

## Per-row drafting disposition (cross-reference to drafting-plan)

The Phase 9 deliverable `paper/<axis>/notes/drafting-plan.md`
refines each row's `target_section_hint` into a specific dispatch
unit. The mapping is:

- DC dispatch 3: row 1 (Involution section)
- DC dispatch 4: row 2 (Separation section, drafted as part of
  AntiInvariantLedger flow in the compressed 11-section structure)
- DC dispatch 5A: row 3 (AntiInvariantLedger section, definition pass)
- DC dispatch 5B: row 4 (AntiInvariantLedger section, trace-identity pass)
- DC dispatch 6: rows 5+6 (DirectConfinement section, both theorems together)
- DC dispatch 7A: row 7 (Domination section, bridge definition)
- DC dispatch 7B: row 8 (Domination section, Douglas factorization)
- DC dispatch 8A+8B: row 9 (MasterTheorem section, statement + proof
  sketch + headline framing)
- DC dispatch 9A: rows 10+11 (ExhaustiveSqueeze section)
- DC dispatch 9B: rows 12+13 (DefectedBudget section, defected shape
  + optimized scalar trace budget with AM-GM disclosure)
- RH dispatch 3: rows 14+15 (Involution section, J_L + ψ_-)
- RH dispatch 4: row 16 (ZeroLedger section)
- RH dispatch 5: row 17 (AntiInvariantZeroLedger section)
- RH dispatch 6: row 18 (SatSelShell section)
- RH dispatch 7A+7B+7C: rows 19, 20, 21 (TranslationT section, three
  theorems)
- RH dispatch 8: row 22 (RecognitionSource section, typed-carrier
  disclosure)
- RH dispatch 9: row 23 (DCMasterApplied section)
- RH dispatch 10: row 24 (RHConditional section, headline)

(Each dispatch is one codex turn per `feedback_no_batching.md`; the
above grouping is the working draft of the dispatch table; Phase 9
finalizes per-axis `drafting-plan.md` for both axes.)

## Validator wiring

`scripts/check_statements_of_record.py` is wired into
`make validate` (Makefile target `validate` runs both
`check_statements_of_record.py --check` and the manifest
cross-check). The pre-flight gate `make paper-preflight-<axis>`
also runs the validator chain.

Validator command:

```bash
python3 scripts/check_statements_of_record.py --check
```

Post Phase H.4 sync (2026-05-23): passes.
