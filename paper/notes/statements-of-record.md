# Statements of Record (review-friendly rendering)

Status: Phase 2 produced 2026-05-23.

Purpose: human-readable rendering of `paper/notes/statements-of-record.yml`.
The yaml is the authoritative source; this markdown is the
review-facing summary table for sign-off.

Schema overview (per `scripts/check_statements_of_record.py`):
- `paper_label`: stable label like `def:duality_confinement:involutive-object-ledger`
- `env_kind`: definition / theorem / lemma / proposition / corollary / obligation
- `source_file`: `anti_loc/extracted_math/<axis>_*.md`
- `source_section`: e.g. `Involution`, `MasterTheorem` (math-artifact
  section header in `anti_loc/extracted_math/`)
- `theorem_title`: human-readable name
- `target_paper`: `duality_confinement` / `rh` / `dropped`
- `target_destination`: `body` / `appendix` / `source_only` / `evidence_pack_only`
- `target_section_hint`: paper-side section label, e.g.
  `sec:master_theorem`, `sec:landing_chain` (matches the frozen
  section labels in `paper/<axis>/notes/section-outline.md`)
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
| 1 | `def:duality_confinement:involutive-object-ledger` | definition | `sec:involutive_ledger` | definition_entry | definition | faithful | Phase G mechanize_now per inventory; central typed object |
| 2 | `def:duality_confinement:separating-readout` | definition | `sec:anti_invariant_ledger` | definition_entry | definition | faithful | Both qualitative and quantitative encoded; co-located with `def:anti-invariant-ledger` in the compressed section structure |
| 3 | `def:duality_confinement:anti-invariant-ledger` | definition | `sec:anti_invariant_ledger` | definition_entry | definition | faithful | Typed positive cone encoding with explicit trace functional (audit_summary §A1 representation note) |
| 4 | `lem:duality_confinement:trace-identity` | lemma | `sec:anti_invariant_ledger` | lean_substantive | theorem | faithful | Definitional unfolding in the typed-cone encoding |
| 5 | `thm:duality_confinement:separation-confinement` | theorem | `sec:direct_confinement` | lean_substantive | theorem | faithful | |
| 6 | `thm:duality_confinement:quantitative-confinement` | theorem | `sec:direct_confinement` | lean_substantive | theorem | faithful | Markov consequence of the trace identity |
| 7 | `def:duality_confinement:completed-domination-bridge` | definition | `sec:domination` | definition_entry | definition | faithful | |
| 8 | `thm:duality_confinement:douglas-domination` | theorem | `sec:domination` | lean_substantive | theorem | faithful | Typed-cone encoding via `DouglasData` carrier (audit_summary §A1) |
| 9 | `thm:duality_confinement:master-theorem` | theorem | `sec:master_theorem` | lean_substantive | theorem | faithful | **HEADLINE — load-bearing master theorem**; reused by RH axis as `thm:rh:dc-master-applied` |
| 10 | `def:duality_confinement:exhaustive-moving-ledger` | definition | `sec:exhaustive_squeeze_and_budgets` | definition_entry | definition | faithful | |
| 11 | `thm:duality_confinement:exhaustive-squeeze` | theorem | `sec:exhaustive_squeeze_and_budgets` | lean_substantive | theorem | faithful | |
| 12 | `def:duality_confinement:defected-budget` | definition | `sec:exhaustive_squeeze_and_budgets` | definition_entry | **not_mechanized** | not_applicable | `support_only` per inventory; no Lean decl; body prose introduces the shape as motivation for `prop:duality_confinement:optimized-trace-budget` |
| 13 | `prop:duality_confinement:optimized-trace-budget` | proposition | `sec:exhaustive_squeeze_and_budgets` | lean_substantive | theorem | faithful | AM-GM step taken as typed-Scalar axiom (audit_summary §A2); disclosure wording "tracked by the formalization harness" |

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
| 14 | `def:rh:fe-involution` | definition | `sec:involution_and_ledger` | definition_entry | definition | faithful | `J_L(s) = 1 - \bar{s}`; involutive + critical-line fixed locus + RH involution disclosures (audit_summary §A3 real-part-type abstraction) |
| 15 | `def:rh:psi-minus-rh` | definition | `sec:involution_and_ledger` | definition_entry | definition | faithful | Anti-invariant readout `\psi_-(s) = Re(s) - 1/2` |
| 16 | `def:rh:nontrivial-zero-ledger` | definition | `sec:involution_and_ledger` | definition_entry | definition | faithful | Typed multiset with `m_\rho > 0` multiplicities; `Λ_ζ` opaque |
| 17 | `def:rh:anti-invariant-zero-ledger` | definition | `sec:involution_and_ledger` | definition_entry | definition | faithful | `A_Z(ζ) = Σ_ρ m_ρ |Re(ρ) - 1/2|²` |
| 18 | `def:rh:sat-sel-shell` | definition | `sec:sat_sel_shell` | definition_entry | definition | faithful | 13-field typed shell; admissibility encoded as opaque `Audit_L` field |
| 19 | `thm:rh:translation-T-forward` | theorem | `sec:translation_theorem` | lean_substantive | theorem | faithful | `A_Z(ζ) = 0 ⟹ ∀ρ, Re(ρ) = 1/2` |
| 20 | `thm:rh:translation-T-reverse` | theorem | `sec:translation_theorem` | lean_substantive | theorem | faithful | `∀ρ, Re(ρ) = 1/2 ⟹ A_Z(ζ) = 0` |
| 21 | `thm:rh:translation-T` | theorem | `sec:translation_theorem` | lean_substantive | theorem | faithful | Biconditional combining 19 + 20; the construction-grade headline |
| 22 | `obl:rh:gamma-sdtc-selberg` | obligation | `sec:recognition_source` | appendix_only | **recognition_source** | not_applicable | Typed structure carrier `GammaSdtcSelberg` declared inline in `RHConditional.lean` (per kickoff §12 sanctioned inline placement); NOT a Lean axiom |
| 23 | `thm:rh:dc-master-applied` | theorem | `sec:landing_chain` | lean_substantive | theorem | faithful | Bridges Paper 1's `masterTheorem` to `Sel^!_{ζ,tr}` via `mu_zero_of_ae` parameter |
| 24 | `thm:rh:conditional` | theorem | `sec:landing_chain` | lean_substantive | theorem | faithful | **HEADLINE — conditional landing chain**; takes `γ : GammaSdtcSelberg shell` as explicit hypothesis |

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
unit. The mapping (post Phase 9 closure):

- DC dispatch 3: row 1 (`sec:involutive_ledger`)
- DC dispatch 4A: rows 2 + 3 (`sec:anti_invariant_ledger`,
  separating-readout + anti-invariant-ledger pass)
- DC dispatch 4B: row 4 (`sec:anti_invariant_ledger`, trace-identity
  pass)
- DC dispatch 5: rows 5 + 6 (`sec:direct_confinement`, both theorems
  together)
- DC dispatch 6A: row 7 (`sec:domination`, bridge definition)
- DC dispatch 6B: row 8 (`sec:domination`, Douglas factorization)
- DC dispatch 7A: row 9 (`sec:master_theorem`, statement)
- DC dispatch 7B: row 9 (`sec:master_theorem`, proof sketch +
  headline framing)
- DC dispatch 8A: rows 10 + 11
  (`sec:exhaustive_squeeze_and_budgets`, exhaustive squeeze)
- DC dispatch 8B: rows 12 + 13
  (`sec:exhaustive_squeeze_and_budgets`, defected shape +
  optimized scalar trace budget with AM-GM disclosure)
- RH dispatch 3A: rows 14 + 15 (`sec:involution_and_ledger`, `J_L`
  + `\psi_-`)
- RH dispatch 3B: rows 16 + 17 (`sec:involution_and_ledger`,
  nontrivial-zero ledger + anti-invariant zero ledger; A3
  disclosure)
- RH dispatch 4: row 18 (`sec:sat_sel_shell`)
- RH dispatch 5A: row 21 (`sec:translation_theorem`, biconditional
  statement)
- RH dispatch 5B: rows 19 + 20 (`sec:translation_theorem`, forward
  + reverse directions)
- RH dispatch 6: row 22 (`sec:recognition_source`, typed-carrier
  disclosure)
- RH dispatch 7A: row 23 (`sec:landing_chain`, master-theorem
  application)
- RH dispatch 7B: row 24 (`sec:landing_chain`, conditional landing
  chain — headline)

(Each dispatch is one codex turn per `feedback_no_batching.md`.
The per-axis `drafting-plan.md` files are the authoritative
dispatch tables; this list is the row-to-dispatch cross-reference
for review convenience.)

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
