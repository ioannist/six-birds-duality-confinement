# Out-of-Scope Ledger

Status: Phase 0 produced 2026-05-23.

Purpose: explicit list of dropped material per paper. These are
NOT weakenings of the underlying theorems; they are honest
delineations of what each paper's body claims do not assert,
together with the reasons why and the pointers to where the
discipline is enforced in body prose.

This ledger complements `paper/notes/scope-fence.md` (the
canonical-nonclaim wording table) and feeds into each paper's
`sec:scope` (Paper 1) / `sec:scope_and_nonclaims` (Paper 2).

## Paper 1 — Duality Confinement out-of-scope

### Operator-theoretic full generality

- **Dropped**: a master theorem proof at the full
  operator-theoretic level (trace-class operators, Hilbert–Schmidt,
  Schatten ideals, full trace-norm topology, classical Douglas
  factorization on bounded Hilbert operators).
- **Why**: the mechanization runs at the typed-positive-cone level
  (mathlib-free). The cone abstracts what is needed (Loewner
  order; trace functional with monotonicity; positivity axiom),
  but the operator-theoretic generality is a separate extension.
  Per `audit_summary.md` §A1 and the contract honesty caveat R1.
- **Where the discipline applies**: body prose around
  `sec:master_theorem`, `sec:domination`, `sec:scope`,
  `sec:discussion`. App D documents the typed-cone abstraction
  explicitly.
- **Future-work pointer**: extending the typed cone to a
  fully-realized typed model of trace-class positive operators on
  a Hilbert space is open extension.

### Substantive AM-GM derivation in optimized-trace-budget

- **Dropped**: a Lean-side derivation of the AM-GM step
  `ta + b/t ≥ 2√(ab)` (with equality at `t = √(b/a)`) for the
  optimized scalar trace budget proposition.
- **Why**: the abstract-Scalar encoding does not provide enough
  arithmetic structure to derive AM-GM substantively; the
  proposition takes AM-GM as a typed-Scalar hypothesis. Per
  `audit_summary.md` §A2 and the contract honesty caveat R4.
- **Where the discipline applies**: body prose around
  `sec:exhaustive_squeeze_and_budgets`, `sec:scope`,
  `app:formalization`. App D documents the limitation explicitly.
- **Future-work pointer**: introducing a typed `OrderedScalar`
  structure with `square_nonneg + sqrt_sq` axioms and deriving
  AM-GM is open extension.

### Cross-substrate theorems (CPT, gauge, Hermitian conjugation, etc.)

- **Dropped**: theorems applying the SDTC structural law to
  quantum self-adjointness, CPT symmetry, gauge invariance,
  particle-antiparticle (C-symmetry), function-field RH, or any
  non-RH substrate.
- **Why**: Paper 1 names cross-substrate generalizations as
  **structural pointers** (per proposal §5). The only mechanized
  validation is the RH instance via Paper 2. Per the contract
  honesty caveat R7 and scope-fence canonical-nonclaim row 5.
- **Where the discipline applies**: body prose around
  `sec:discussion`. Wording: "structural predictions that genuine
  involutive self-duality at the formed-layer level implies
  fixed-locus confinement; consistency with observed
  physical/mathematical symmetries; single-substrate validation
  (RH via Paper 2)."
- **Future-work pointer**: extending the mechanization to other
  single-substrate validations (function-field RH first; then
  quantum self-adjointness; etc.) is open extension.

### Derivation of `Γ_{SDTC}` from framework primitives

- **Dropped**: any claim that the SDTC structural law is derivable
  from framework primitives (Foundations I/II/III + needles
  framework + adequacy + Holonomy with Memory).
- **Why**: SDTC is a named structural law (recognition source).
  The cascade's three-option derivation sweep (in the RH paper's
  context, steps 451–453) documents the analogous result for the
  Selberg-class specialization. Per contract honesty caveat R1
  and scope-fence canonical-nonclaim row 1.
- **Where the discipline applies**: body prose throughout; the
  scope-fence row 1 wording governs every appearance of "SDTC" in
  Paper 1 prose.

### Bidirectional apparatus equivalence (proposal Appendix A Theorem 2)

- **Dropped**: a formal bidirectional equivalence between the
  SDTC structural claim and the existence of the domination
  records (proposal §Appendix A Theorem 2 "SDTC apparatus
  equivalence").
- **Why**: the mechanization realizes the forward direction
  (records ⟹ collapse) via the master theorem; the reverse
  direction (collapse ⟹ records would obtain) is not formally
  bidirectionalized in this paper. Per contract honesty caveat R3.
- **Where the discipline applies**: body prose around
  `sec:master_theorem`, `sec:scope`. Wording: "The master theorem
  realizes the forward apparatus implication; a bidirectional
  equivalence is not formally established in this paper."

### Classical operator-theory novelty claims

- **Dropped**: any claim of novelty for classical operator-theoretic
  constructions (Douglas factorization, trace functionals, Loewner
  order, AM-GM inequality, Markov's inequality).
- **Why**: the paper's contribution is the typed structural law
  (SDTC) and the duality-confinement master theorem packaging, not
  the underlying classical operator-theoretic mathematics. Per
  scope-fence canonical-nonclaim row 5.
- **Where the discipline applies**: body prose around
  `sec:domination`, `sec:direct_confinement`,
  `sec:exhaustive_squeeze_and_budgets`,
  `sec:discussion`. Cite classical sources (Douglas 1966; standard
  operator-theory references) when invoking the classical content,
  even where the citation lookups are deferred to the user's
  external-reference pipeline.

## Paper 2 — RH closure out-of-scope

### Unconditional standard-ZFC RH

- **Dropped**: a standard-ZFC unconditional proof of RH (every
  nontrivial zero of `ζ` has real part 1/2 in the standard
  analytic-number-theory sense).
- **Why**: the paper proves a conditional theorem
  `Γ_{SDTC-Selberg} ⟹ RH` at theorem grade under the standard Six
  Birds closure assumption. Outside Six Birds, only the conditional
  inference is theorem-grade. Per contract honesty caveat 1 and
  scope-fence canonical-nonclaim row 6.
- **Where the discipline applies**: body prose throughout; the
  scope-fence row 6 wording governs every appearance of "RH" in
  Paper 2 prose. `sec:intro`, `sec:landing_chain`,
  `sec:scope_and_nonclaims`, `sec:discussion`, `sec:conclusion`
  must use "conditional theorem" / "under the standard Six Birds
  closure assumption" wording.

### Standard-mathematical RH on the actual ζ-zeros

- **Dropped**: an identification of the Lean theorem's conclusion
  `∀ ρ ∈ shell.Z_nt, Re(ρ) = 1/2` with the standard mathematical
  RH statement (every nontrivial zero of `ζ` has real part 1/2)
  without disclosing the parameter-identification.
- **Why**: `shell.Z_nt` is a typed multiset parameter in the Lean
  encoding; the identification with the actual nontrivial zeros of
  `ζ` is by construction-parameter assignment, not by a Lean-side
  derivation from analytic number theory. Per contract honesty
  caveat 2 and `audit_summary.md` §A3.
- **Where the discipline applies**: body prose around
  `sec:involution_and_ledger`, `sec:translation_theorem`,
  `sec:landing_chain`, `app:formalization`. The disclosure wording
  is in `paper/notes/proof-presentation-policy.md` §"Project-
  specific representation notes".

### Derivation of `Γ_{SDTC-Selberg}` from framework primitives

- **Dropped**: any claim that the Selberg-class instance of SDTC is
  derivable from framework primitives (Foundations I/II/III +
  needles framework + adequacy + Holonomy with Memory).
- **Why**: the recognition source is supplied by Paper 1's SDTC
  structural law applied to the Selberg trace closure. The
  cascade's three-option derivation sweep (steps 451–453) confirms
  that framework primitives do not derive the domination-records
  hypothesis on the formed Selberg trace layer. Per contract
  honesty caveat 4 and scope-fence canonical-nonclaim row 7.
- **Where the discipline applies**: body prose around
  `sec:recognition_source`, `sec:scope_and_nonclaims`,
  `sec:discussion`.

### `Γ_{SDTC-Selberg}` as Lean axiom

- **Dropped**: any framing of the recognition source as a Lean
  axiom.
- **Why**: the Lean encoding uses a typed `structure` carrier
  (`GammaSdtcSelberg`) declared inline in `RHConditional.lean`
  (per `lean/codex_kickoff.md` §12 sanctioning the inline
  placement); downstream theorems take a value of this structure
  as an explicit hypothesis parameter. The forbidden-tokens rule
  bans `axiom`/`opaque`/`constant`/`sorry`/`admit` everywhere in
  the source tree. Per contract honesty caveat 3 and scope-fence
  canonical-nonclaim row 8.
- **Where the discipline applies**: body prose around
  `sec:recognition_source`, `app:formalization`. The disclosure
  wording is in `paper/notes/proof-presentation-policy.md` §
  Lean-disclosure for `recognition_source`.

### Classical RH attack barrier circumvention

- **Dropped**: any claim that the conditional theorem circumvents
  classical RH attack barriers (Weil positivity, Hilbert–Pólya,
  GUE statistics, Connes adelic / NCG, de Branges, Beurling–Nyman,
  Mertens, Bagchi, etc.) in their native sense.
- **Why**: the conditional theorem operates at the formed-layer
  closure level per Foundations I, not at the classical
  analytic-number-theory level. The audit-currency derivability
  tension at cascade steps 441–447 documents why classical
  carriers are readout-level and structurally distinct from the
  source-level recognition content. Per contract honesty caveat 5
  and scope-fence canonical-nonclaim row 10.
- **Where the discipline applies**: body prose around
  `sec:scope_and_nonclaims`, `sec:discussion`. Wording:
  "partial-spirit-aligned with but structurally distinct from
  classical barriers" — never "we bypass" or "we circumvent".

### Generalized Riemann Hypothesis (GRH)

- **Dropped**: GRH for primitive Selberg-class L-functions
  (Dirichlet L, modular L, automorphic L).
- **Why**: the paper instantiates SDTC for `L = ζ` only; the
  Selberg-class generalization is structurally straightforward in
  principle but reserved for follow-up. Per contract honesty
  caveat 6 and scope-fence canonical-nonclaim row 11.
- **Where the discipline applies**: body prose around
  `sec:scope_and_nonclaims`, `sec:discussion`. Wording: "RH for ζ
  instantiated on `Sel^!_{ζ,tr}`; the Selberg-class
  generalization is structurally straightforward in principle but
  reserved for follow-up."

### Simple-zero conjecture / density results

- **Dropped**: any claim about multiplicity 1 for all nontrivial
  zeros (simple-zero conjecture), Lindelöf hypothesis, or
  zero-density results.
- **Why**: the anti-invariant ledger accommodates `m_ρ > 0`
  multiplicities; closure does not force them to be 1. These are
  RH-adjacent but distinct conjectures. Per contract honesty
  caveat 7 and scope-fence canonical-nonclaim row 12.
- **Where the discipline applies**: body prose around
  `sec:scope_and_nonclaims`. Wording: do not mention multiplicity-1
  or zero-density conclusions.

### Sel^!_{ζ,tr} admissibility derivation

- **Dropped**: a Lean-side or paper-side derivation that
  `Sel^!_{ζ,tr}` passes all seven Foundations II admissibility
  schemas.
- **Why**: admissibility is encoded as a Foundations-II-level
  hypothesis in the `SatSelShell` structure (the opaque `Audit_L`
  field). Per the proposal §4.2 paper-side claim, admissibility
  is established at construction time; the Lean encoding takes it
  as construction-time hypothesis, not as a derived fact in the
  DC axis or RH axis. Per contract honesty caveat 8.
- **Where the discipline applies**: body prose around
  `sec:sat_sel_shell`, `app:formalization`. Wording: "the
  saturated trace shell carries an audit record of its
  admissibility per Foundations II [cited]; the Lean encoding
  takes this as construction-time data."

### Classical analytic-number-theory novelty claims

- **Dropped**: any claim of novelty for classical analytic
  number theory constructions (completed zeta `Λ_ζ`, functional
  equation `J_L`, multiplicity bookkeeping, Selberg trace
  machinery).
- **Why**: the contribution is the typed saturated trace closure,
  the typed translation theorem, and the recognition-grade
  conditional theorem packaging. Per scope-fence
  canonical-nonclaim row 13.
- **Where the discipline applies**: body prose around
  `sec:involution_and_ledger`, `sec:translation_theorem`,
  `sec:discussion`. Cite classical analytic-number-theory sources
  when invoking classical content.

## Shared out-of-scope (both papers)

### Full Lean verification at the level of analytic number theory / operator theory

- **Dropped**: claims that Lean verifies every body theorem at
  the full level of classical analytic number theory or operator
  theory.
- **Why**: the project is mathlib-free. The Lean encoding is at
  typed-abstraction level with explicit representation notes
  (audit_summary §A1 Douglas; §A2 AM-GM; §A3 real-part type).
  Per scope-fence canonical-nonclaim row 14.
- **Where the discipline applies**: `app:formalization` per
  paper; any body Lean citation. Wording per
  `paper/notes/proof-presentation-policy.md` 4-mode table.

### External classical bibliography curation

- **Dropped**: a full external classical bibliography in the prep
  arc.
- **Why**: external references are deferred to the user's
  end-of-process pipeline. The prep arc curates Tsiokos-only
  references (max 3 per paper) plus a small set of classical
  references identified per axis (Douglas 1966 for Paper 1;
  standard analytic-number-theory references for Paper 2) as
  paper-prose placeholders. Per scope-fence canonical-nonclaim
  row 15.
- **Where the discipline applies**: `paper/references.bib`;
  `paper/notes/references-selection.md` (produced at Phase 5).

### Support-only / out-of-scope material as preserved body claims

- **Dropped**: treating `support_only` definitions
  (`def:duality_confinement:defected-budget`),
  `out_of_scope_meta` rows (none in current inventory), or
  `out_of_scope_recognition_source` rows
  (`obl:rh:gamma-sdtc-selberg`) as preserved body claims.
- **Why**: these are administrative metadata or recognition
  content; the recognition source enters the conditional theorem
  as a hypothesis parameter, not as a derived fact. Per
  scope-fence canonical-nonclaim row 16.
- **Where the discipline applies**: all sections across both
  papers.

## Out-of-scope-but-future-work pointers

Items dropped here that are reasonable future-work targets:

1. **Operator-theoretic generality of the master theorem**
   (Paper 1) — extend the typed cone to a fully-realized typed
   model of trace-class positive operators on a Hilbert space.
2. **Substantive AM-GM derivation in `optimizedTraceBudget`**
   (Paper 1) — introduce a typed `OrderedScalar` with
   `square_nonneg + sqrt_sq` axioms.
3. **Cross-substrate single-substrate validations** (Paper 1) —
   function-field RH; quantum self-adjointness; CPT, etc.
4. **GRH for primitive Selberg-class L-functions** (Paper 2) —
   instantiate SDTC for general `L`.
5. **Identification of `shell.Z_nt` with the actual nontrivial
   zeros of `ζ`** (Paper 2) — substantively connect the typed
   multiset parameter to analytic number theory.
6. **Sel^!_{ζ,tr} admissibility derivation** (Paper 2) —
   formalize the seven Foundations II admissibility schemas in
   Lean and derive `Audit_L`.
7. **Bidirectional apparatus equivalence** (Paper 1) — formal
   bidirectional equivalence between SDTC structural claim and
   the existence of the domination records.

The `sec:discussion` of each paper enumerates these as future
work without overclaiming progress on them.
