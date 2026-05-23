# Scope Fence

Status: Phase I.A.1 produced 2026-05-23 (paper-writing pre-drafting workspace).

Purpose: records what the two papers must NOT claim. These are
drafting fences for the writer (codex) and review checkpoints for
the reviewer (Claude); they are NOT weakenings of the underlying
theorems.

Governing sources:

- `anti_loc/paper_proposal_self_dual_trace_confinement.md` (Paper 1 proposal)
- `anti_loc/paper_proposal_rh_via_sdtc_selberg.md` (Paper 2 proposal)
- `anti_loc/extracted_math/duality_confinement_master.md` (Paper 1 math source-of-truth)
- `anti_loc/extracted_math/rh_construction.md` (Paper 2 math source-of-truth)
- `anti_loc/extracted_math/audit_summary.md` (Phase B verdict + representation notes)
- `paper/notes/statements-of-record.yml` (24 rows, lean_coverage per row)
- `paper/notes/proof-presentation-policy.md` (Lean disclosure wording)
- `paper/<axis>/notes/claim-revision-register.md` (per-axis revisions of proposal-era claims)

## Canonical nonclaims

| Nonclaim | Required wording discipline | Where it belongs |
| --- | --- | --- |
| Paper 1 does not claim that SDTC is a derived theorem of framework primitives. | Say "Self-Dual Trace Confinement is named as recognition source — structural content supplied by formed-layer closure per Foundations I, not derived from framework primitives alone." Avoid "we prove SDTC" or "the SDTC theorem". | Paper 1 `sec:master_theorem`, `sec:scope_and_discussion`. |
| Paper 1 does not claim operator-theoretic generality for the master theorem mechanization. | Say "the master theorem is mechanized at the abstract positive-cone level with an explicit typed trace functional; operator-theoretic generality (trace class, Hilbert-Schmidt, Schatten norms) remains an open extension." Avoid "we mechanize the master theorem over trace-class operators" without the typed-cone qualifier. | Paper 1 `sec:master_theorem`, `app:formalization`. |
| Paper 1 does not claim the optimized-trace-budget proposition is substantively derived in Lean. | Say "the AM-GM step in `prop:duality_confinement:optimized-trace-budget` is tracked by the formalization harness as a typed-Scalar axiom; a substantive derivation requires introducing typed real-arithmetic structure." Avoid "Lean proves the optimized scalar trace budget". | Paper 1 `sec:exhaustive_squeeze_and_budgets`, `app:formalization`. |
| Paper 1 does not claim Section 5 cross-substrate generalizations (CPT, gauge invariance, Hermitian conjugation, particle-antiparticle, function-field RH) as established results. | Say "structural predictions that genuine involutive self-duality at the formed-layer level implies fixed-locus confinement; consistency with observed physical/mathematical symmetries; single-substrate validation (RH via Paper 2)." Avoid "we prove CPT invariance" or "we derive the self-adjointness postulate". | Paper 1 `sec:scope_and_discussion`. |
| Paper 1 does not claim novelty for classical operator-theoretic constructions (Douglas factorization, trace functionals, Loewner order, AM-GM). | Acknowledge classical constructions as standard operator theory; the contribution is the typed structural law (SDTC) and the duality-confinement master theorem packaging, not the underlying mathematics. Cite classical sources where appropriate. | Paper 1 `sec:domination`, `sec:exhaustive_squeeze_and_budgets`, `sec:scope_and_discussion`. |
| Paper 2 does not claim standard-ZFC unconditional RH. | Say "a Six Birds-native conditional theorem at theorem grade under the standard Six Birds closure assumption" or "the conditional theorem `Γ_{SDTC-Selberg} ⟹ RH`." Avoid "we prove RH" without the conditional or recognition-grade qualifier. | Paper 2 `sec:intro`, `sec:landing_chain`, `sec:scope_and_nonclaims`, `sec:discussion`, `sec:conclusion`. |
| Paper 2 does not claim that `Γ_{SDTC-Selberg}` is derivable from framework primitives. | Say "the recognition source is supplied by Paper 1's SDTC structural law applied to the Selberg trace closure; the cascade's three-option derivation sweep (steps 451–453) confirmed framework primitives do not suffice." Avoid "we derive" or "we prove the recognition source." | Paper 2 `sec:recognition_source`, `sec:scope_and_nonclaims`, `sec:discussion`. |
| Paper 2 does not claim the recognition source is a Lean axiom. | Say "the recognition source is encoded as a typed structure carrier `GammaSdtcSelberg` in `SixBirdsDualityConfinement.RH.RHConditional`; the project's forbidden-tokens rule bans `axiom`/`opaque`/`constant` declarations across the source tree." Avoid "we add an axiom" or "Lean axiom for the recognition source." | Paper 2 `sec:recognition_source`, `app:formalization`. |
| Paper 2 does not claim the Lean conclusion `∀ ρ ∈ shell.Z_nt, Re(ρ) = 1/2` equals the standard mathematical RH statement without the parameter-identification disclosure. | Say "the Lean theorem concludes the analogous statement about the typed-multiset parameter `shell.Z_nt`; the identification of `shell.Z_nt` with the actual nontrivial zeros of `ζ` is by construction-parameter assignment, not by a Lean-side derivation from analytic number theory." Avoid "Lean proves RH" without the parameter-identification disclosure. | Paper 2 `sec:involution_and_ledger`, `sec:translation_theorem`, `sec:landing_chain`, `app:formalization`. |
| Paper 2 does not claim circumvention of classical RH attack barriers (Weil positivity, Hilbert-Pólya, GUE statistics, Connes adelic / NCG, de Branges, Beurling-Nyman) in their native sense. | Say "the conditional theorem operates at the formed-layer closure level per Foundations I, not at the classical analytic-number-theory level; the audit-currency derivability tension at cascade steps 441–447 documents why Weil positivity is readout-level and structurally distinct from a source-level result." Avoid "we bypass Weil positivity" or "we circumvent the Connes barrier." | Paper 2 `sec:scope_and_nonclaims`, `sec:discussion`. |
| Paper 2 does not claim Generalized RH (GRH) for primitive Selberg-class L-functions. | Say "RH for `ζ` instantiated on `Sel^!_{ζ,tr}`; the Selberg-class generalization is structurally straightforward in principle but reserved for follow-up." Avoid "we prove GRH" or "the result extends to GRH" without the follow-up qualifier. | Paper 2 `sec:scope_and_nonclaims`, `sec:discussion`. |
| Paper 2 does not claim simple-zero conjecture or density-of-zeros results (Lindelöf, zero-density). | Say "the anti-invariant ledger accommodates multiplicities `m_ρ > 0`; closure does not force them to be 1; density-of-zeros results are RH-adjacent but distinct conjectures with their own structural status." Avoid mentions of multiplicity-1 or zero-density conclusions. | Paper 2 `sec:scope_and_nonclaims`. |
| Paper 2 does not claim novelty for classical zero-ledger constructions (completed zeta `Λ_ζ`, functional equation `J_L`, multiplicity bookkeeping). | Acknowledge classical constructions as standard analytic number theory; the contribution is the typed saturated trace closure, the typed translation theorem, and the recognition-grade conditional theorem packaging. | Paper 2 `sec:involution_and_ledger`, `sec:translation_theorem`, `sec:discussion`. |
| Neither paper claims Lean fully verifies every body theorem at the level of analytic number theory or operator theory. | Use the wording discipline from `paper/notes/proof-presentation-policy.md`: "Lean proves" only for `lean_coverage = theorem` rows with `faithful` semantic alignment; for narrowed/projection rows, use the disclosure phrasings; for `recognition_source` and `obligation` rows, use the typed-carrier wording. | Both papers `app:formalization`; any body formalization note. |
| Neither paper claims external classical bibliography has been curated in the prep arc. | Use the selected Tsiokos references plus the small set of classical references identified per axis (operator-theory for Paper 1; analytic-number-theory for Paper 2). External-source curation is the user's end-of-process pipeline. | Both papers `sec:intro`, technical sections, bibliography notes. |
| Neither paper treats `support_only`, `out_of_scope_meta`, or `out_of_scope_recognition_source` material as a preserved body claim. | Nonclaim rows and out-of-scope obligations are administrative metadata or recognition content. Do not cite them as theorem support, body claims, or examples; the recognition source enters the conditional theorem as a hypothesis parameter, not as a derived fact. | All sections across both papers. |

## Shared nonclaims

The Lean mechanization boundary applies to both papers. Paper 1 (DC)
has 13 inventory rows (12 mechanize_now + 1 support_only); Paper 2
(RH) has 11 (10 mechanize_now + 1 recognition_source). All 22
mechanize_now rows carry `faithful` semantic alignment after Phase
H.4 sync. The canonical wording source per row is
`paper/notes/statements-of-record.yml`.

The external-reference boundary applies to both papers. Paper 1
will cite classical operator theory (Douglas 1966; standard
trace-class / Loewner-order references) and the Six Birds
foundations papers (II, III). Paper 2 will cite classical analytic
number theory at appropriate points (completed zeta, Selberg trace
machinery as standard references); Tsiokos-only references inherit
the shared `paper/references.bib`.

The recognition-source boundary applies to Paper 2. Paper 2 cites
Paper 1 for `Γ_{SDTC-Selberg}` but does NOT derive it. The
recognition source is structural content of closure formation per
Foundations I, not framework-derivable per cascade steps 451–453.
**The dependency is one-way**: Paper 1 does NOT cross-cite Paper 2.

## Positive claim boundary

What the papers DO claim, stated affirmatively:

**Paper 1 (Duality Confinement / SDTC):**

1. A typed Self-Dual Trace Confinement structural law (SDTC) over
   formed closures with genuine involutive self-duality: visible
   object mass is confined to the fixed locus of the duality. The
   law is named as recognition source; the mechanism is the
   duality-confinement master theorem.
2. The duality-confinement membrane theorem (the master theorem):
   given an involutive object ledger with separating anti-invariant
   readout and a sequence of completed domination records
   `A_X ⪯ B_n` with `tr B_n → 0`, visible mass is confined to
   `Fix(J)`. Mechanized in Lean at the typed positive-cone level.
3. Supporting apparatus: trace identity, direct confinement,
   quantitative confinement via Markov, Douglas factorization in
   typed-cone encoding, exhaustive ledger squeeze, optimized scalar
   trace budget (AM-GM in abstract Scalar setting).
4. Cross-substrate generalization predictions (structural pointers
   only, not derivations).

**Paper 2 (RH closure):**

1. A Six Birds-native conditional theorem at theorem grade under
   the standard Foundations I closure assumption, conditional on
   the recognition source `Γ_{SDTC-Selberg}` from Paper 1:
   every nontrivial zero of `ζ` (typed in the shell's zero ledger)
   has real part 1/2.
2. Translation theorem T: `A_Z(ζ) = 0 ⟺ RH` (theorem grade by
   construction, mechanized in Lean).
3. Construction-grade machinery: the saturated completed Selberg
   trace closure `Sel^!_{ζ,tr}` as a typed bundle; the
   functional-equation involution `J_L` with its critical-line
   fixed locus; the anti-invariant zero ledger `A_Z(ζ)`.
4. The three-step conditional landing chain mechanized as
   `rhConditional` in Lean.
5. Outside-Six-Birds reading: the conditional theorem
   `Γ_{SDTC-Selberg} ⟹ RH`.

## Disambiguation rules (apply across both papers)

- Whenever the body uses "RH", indicate whether the reference is to
  the standard mathematical statement (every nontrivial zero of `ζ`
  has real part 1/2) or to the framework-internal conditional
  reading `Γ_{SDTC-Selberg} ⟹ RH`. The relationship between the two
  is via construction-parameter identification of `shell.Z_nt`.
- Whenever the body mentions the "conditional theorem" reading, use
  that phrase exactly; do not paraphrase to "approximate RH" or
  "weak RH".
- Whenever a Lean theorem is cited, use the wording allowed by the
  row's `lean_coverage` × `semantic_alignment` cell (per
  `paper/notes/proof-presentation-policy.md`); do not invent
  shortcuts.
- Cross-paper citations: Paper 2 → Paper 1 by section number on
  first reference, native term thereafter. Paper 1 does NOT
  cross-cite Paper 2 (one-way dependency).
