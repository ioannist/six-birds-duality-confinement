# Section Outline: Duality Confinement (Paper 1)

Status: Phase I.A.2 produced 2026-05-23.

Authoritative outline sources: this file,
`paper/duality_confinement/notes/contract.md`, and
`paper/notes/statements-of-record.yml`.

Section roster: 11 body sections + 1 appendix (formalization).

## Narrative spine

The paper opens with the structural question: when must an operator-
valued obstruction associated with an involutive system vanish?
Section 2 places the question in the Six Birds framework: typed
involutive object ledgers, the V-Differential trace-state-only column
condition, and the closure-content-as-structural-fact discipline.
Sections 3–8 build the apparatus: the involutive object ledger, the
anti-invariant ledger with its trace functional and separating
readout, direct confinement consequences, the domination-record
discipline with Douglas factorization, the headline master theorem,
and the exhaustive-squeeze plus optimized-trace-budget refinements.
Section 9 establishes the scope fence (SDTC as recognition source,
not derived theorem; typed-cone abstraction; AM-GM-as-axiom
limitation). Section 10 discusses cross-substrate generalization
predictions and positioning against classical operator-theoretic
results. Section 11 concludes.

## 1. Introduction

- File: `paper/duality_confinement/sections/sec_01_intro.tex`
- Section label: `sec:intro`
- Target length: 2–3 pages
- Purpose: opens from "when must an operator-valued obstruction
  associated with an involutive system vanish?" Frames the answer
  in plain mathematical terms first (anti-invariant readout +
  trace-class squeeze + separation), then names the framework's
  typed apparatus. States scope fence (SDTC is structural law /
  recognition source; master theorem mechanized at typed-cone
  abstraction; cross-substrate generalizations are pointers).
- Primary sources: contract thesis paragraph; math artifact
  preamble. Inventory rows: forward references only (definitions
  introduced in §3, master theorem in §7).
- Definitions introduced in plain prose (per
  `audience-translation.md`): involutive object ledger /
  anti-invariant readout / trace-class regime / formed closure /
  recognition source. Formal definitions appear later.
- Key claims: nonclaim rows from `sec:scope` (no derivation of
  SDTC; no operator-theoretic generality; no cross-substrate
  theorems).
- Dependencies: none.

## 2. Framework

- File: `paper/duality_confinement/sections/sec_02_framework.tex`
- Section label: `sec:framework`
- Target length: 2–3 pages
- Purpose: place the paper in the Six Birds framework context. Brief
  recap of: closure formation per Foundations I, the
  closure-content-as-structural-fact commitment, the V-Differential
  trace-state-only column condition, and the sibling structural
  laws (no-needles, CSL-SAT-hiddenness) that SDTC joins.
- Primary sources: proposal §1 motivation, §11 broader-program
  positioning. No inventory rows (background only).
- Definitions introduced: formed closure (plain-prose); the V-
  Differential classification (plain-prose). Foundations-canonical
  terms (FATCD, BirdInt, scoped exact six) mentioned only as
  citations to foundations II/III when they appear in body prose.
- Key claims: positioning only; no theorems.
- Dependencies: `sec:intro`.

## 3. Involutive object ledger

- File: `paper/duality_confinement/sections/sec_03_involutive_ledger.tex`
- Section label: `sec:involutive_ledger`
- Target length: 2–3 pages
- Purpose: define the central typed object — the involutive object
  ledger `(X, J, μ, ψ, Y, J_iso)`. Worked example: the RH
  specialization with `J_L(s) = 1 - s̄` and `Fix(J_L) = {Re(s) = 1/2}`
  (forward-references Paper 2; this is the concrete example a
  general mathematician can grasp). Contrast with a simpler toy
  example (e.g., complex conjugation on `ℂ` with the real line as
  fixed locus).
- Primary sources: math artifact §Involution. Inventory row:
  `def:duality_confinement:involutive-object-ledger`.
- Key claims: definition only.
- Dependencies: `sec:framework`.

## 4. Anti-invariant ledger and separation

- File: `paper/duality_confinement/sections/sec_04_anti_invariant_ledger.tex`
- Section label: `sec:anti_invariant_ledger`
- Target length: 3–4 pages
- Purpose: define the anti-invariant projector `P_-`, the
  anti-invariant readout `ψ_- = P_- ψ`, the anti-invariant ledger
  `A_X := ∫ ψ_- ψ_-^* dμ` in a typed positive cone with explicit
  trace functional. Prove (or definitionally encode) the trace
  identity `tr A_X = ∫ ‖ψ_-‖² dμ`. Define the separating-readout
  condition (qualitative + quantitative).
- Primary sources: math artifact §Separation + §AntiInvariantLedger.
  Inventory rows: `def:duality_confinement:separating-readout`,
  `def:duality_confinement:anti-invariant-ledger`,
  `lem:duality_confinement:trace-identity`.
- Key claims: trace identity lemma (Lean-substantive, but
  definitional-unfolding in the typed-cone encoding).
- Dependencies: `sec:involutive_ledger`.
- Lean disclosure: trace identity is `lean_substantive` with
  `faithful` alignment but encoded as a constructor field of the
  typed cone. Per `proof-presentation-policy.md`, body prose says
  "Lean verifies the trace identity as `traceIdentity`" with a
  one-sentence note that the identity is built into the typed-cone
  constructor rather than derived from measure theory.

## 5. Direct confinement

- File: `paper/duality_confinement/sections/sec_05_direct_confinement.tex`
- Section label: `sec:direct_confinement`
- Target length: 1–2 pages
- Purpose: prove the two direct consequences of the trace identity
  plus separation: (1) `A_X = 0 ⟹ μ(X ∖ Fix(J)) = 0`; (2)
  quantitative `μ{x : dist(x, Fix(J)) ≥ ε} ≤ tr(A_X) / m(ε)²`.
  These are the "warm-up" results before the master theorem.
- Primary sources: math artifact §DirectConfinement. Inventory rows:
  `thm:duality_confinement:separation-confinement`,
  `thm:duality_confinement:quantitative-confinement`.
- Key claims: both theorems Lean-substantive with faithful
  alignment.
- Dependencies: `sec:anti_invariant_ledger`.

## 6. Domination and Douglas factorization

- File: `paper/duality_confinement/sections/sec_06_domination.tex`
- Section label: `sec:domination`
- Target length: 2–3 pages
- Purpose: define the completed-domination-bridge record
  `A_X ⪯ K^- + E`; state Douglas factorization in the typed-cone
  encoding (the `DouglasData` carrier per `audit_summary.md` §A1);
  note the classical operator-theoretic origin (cite Douglas 1966)
  and the typed-encoding choice; explain why downstream theorems
  use this carrier.
- Primary sources: math artifact §Domination. Inventory rows:
  `def:duality_confinement:completed-domination-bridge`,
  `thm:duality_confinement:douglas-domination`.
- Key claims: domination bridge definition; Douglas factorization
  theorem (Lean-substantive with faithful alignment, typed-cone
  encoding disclosed).
- Dependencies: `sec:anti_invariant_ledger`.

## 7. The duality-confinement membrane theorem

- File: `paper/duality_confinement/sections/sec_07_master_theorem.tex`
- Section label: `sec:master_theorem`
- Target length: 3–4 pages
- Purpose: state and prove the headline master theorem. Layout: (a)
  statement; (b) proof sketch in body (trace monotonicity from `⪯`;
  squeeze from `tr B_n → 0`; positivity-to-zero; separation
  consequence); (c) Lean-disclosure note that the proof composes
  four typed-cone axioms / hypotheses with the separation theorem
  from §5; (d) consequence statement (SDTC named); (e) forward
  reference to RH instantiation (Paper 2 `sec:landing_chain`).
- Primary sources: math artifact §MasterTheorem. Inventory row:
  `thm:duality_confinement:master-theorem`.
- Key claims: the master theorem (Lean-substantive with faithful
  alignment; the typed-cone abstraction is disclosed).
- Dependencies: `sec:direct_confinement`, `sec:domination`.

## 8. Exhaustive squeeze and defected budgets

- File: `paper/duality_confinement/sections/sec_08_exhaustive_squeeze_and_budgets.tex`
- Section label: `sec:exhaustive_squeeze_and_budgets`
- Target length: 2–3 pages
- Purpose: refinements of the master theorem for cases where the
  domination record is naturally finite-window-plus-tail (exhaustive
  moving ledger) or defected (two-defect budget with scalar
  optimization). State and prove the exhaustive-squeeze theorem;
  state the defected-budget shape and the optimized scalar trace
  budget. Disclose the AM-GM-as-typed-Scalar-hypothesis limitation
  per `audit_summary.md` §A2.
- Primary sources: math artifact §ExhaustiveSqueeze + §DefectedBudget.
  Inventory rows:
  `def:duality_confinement:exhaustive-moving-ledger`,
  `thm:duality_confinement:exhaustive-squeeze`,
  `def:duality_confinement:defected-budget` (support_only, no Lean
  citation),
  `prop:duality_confinement:optimized-trace-budget`.
- Key claims: exhaustive-squeeze theorem; optimized-trace-budget
  proposition (with AM-GM-as-axiom disclosure).
- Dependencies: `sec:master_theorem`.

## 9. Scope and non-claims

- File: `paper/duality_confinement/sections/sec_09_scope.tex`
- Section label: `sec:scope`
- Target length: 1–2 pages
- Purpose: explicitly state the paper's nonclaims with required
  wording (per `paper/notes/scope-fence.md`). Distinguishes the
  named structural law SDTC from a derivation; the typed-cone
  encoding from operator-theoretic generality; the AM-GM
  hypothesis from a substantive AM-GM derivation; structural
  predictions from cross-substrate theorems.
- Primary sources: contract honesty caveats; scope-fence canonical
  nonclaims. No inventory rows beyond cross-references.
- Key claims: nonclaim discipline only.
- Dependencies: `sec:master_theorem`,
  `sec:exhaustive_squeeze_and_budgets`.

## 10. Discussion

- File: `paper/duality_confinement/sections/sec_10_discussion.tex`
- Section label: `sec:discussion`
- Target length: 2–3 pages
- Purpose: cross-substrate generalization pointers (quantum
  self-adjointness, CPT, gauge invariance, particle-antiparticle,
  function-field RH) per proposal §5 — as structural predictions
  with explicit "structural pointer, not theorem" qualifier.
  Positioning against classical operator-theoretic results: the
  master theorem is partial-spirit-aligned with but
  structurally-distinct-from classical operator squeeze theorems.
  Future work: operator-theoretic generalization of the master
  theorem; substantive AM-GM derivation requiring typed
  real-arithmetic; additional single-substrate validations.
- Primary sources: proposal §5 (generalizations), §10
  (philosophical claim), §11 (broader program).
- Key claims: no new theorems.
- Dependencies: all preceding body sections.

## 11. Conclusion

- File: `paper/duality_confinement/sections/sec_11_conclusion.tex`
- Section label: `sec:conclusion`
- Target length: 1 page
- Purpose: restate the headline (SDTC structural law + master
  theorem apparatus); list pending mechanization directions
  (operator-theoretic generality; AM-GM substantive derivation);
  forward to Paper 2 as the worked single-substrate validation.
- Primary sources: contract thesis paragraph.
- Key claims: none.
- Dependencies: `sec:discussion`.

## Appendix — Formalization

- File: `paper/duality_confinement/appendices/app_d_formalization.tex`
- Section label: `app:formalization`
- Target length: 4–6 pages
- Purpose: per-row table of all 13 Duality Confinement inventory
  rows (12 mechanize_now + 1 support_only) with paper label →
  paper-prose name → Lean decl name → coverage notes. Includes the
  Lean-disclosure wording-discipline table per
  `paper/notes/proof-presentation-policy.md`. Documents the three
  representation choices from `audit_summary.md` §A1 (Douglas
  factorization typed-cone encoding), §A2 (AM-GM as typed-Scalar
  axiom), and (forward-referencing Paper 2) §A3 (real-part type
  abstraction for RH).
- Primary sources: `lean/manifests/duality_confinement_manifest.toml`,
  `paper/notes/statements-of-record.yml`,
  `anti_loc/extracted_math/audit_summary.md`.

## Section label freeze

Locked labels (do not change without updating
`paper/notes/statements-of-record.yml`'s `target_section_hint`
fields):

`sec:intro`, `sec:framework`, `sec:involutive_ledger`,
`sec:anti_invariant_ledger`, `sec:direct_confinement`, `sec:domination`,
`sec:master_theorem`, `sec:exhaustive_squeeze_and_budgets`, `sec:scope`,
`sec:discussion`, `sec:conclusion`, `app:formalization`.
