# Claim Revision Register: Duality Confinement (Paper 1)

Status: Phase 9 produced 2026-05-23 (paper-writing prep arc closed).

Purpose: catalogs every claim from the proposal
`anti_loc/paper_proposal_self_dual_trace_confinement.md` whose
wording needs to be REVISED in the drafted paper because the
mechanization narrowed, refined, or made-concrete what was an
aspirational claim in the proposal.

This register is consulted by codex drafting dispatches: when a
subsection touches a proposal claim listed below, the dispatch
prompt names the applicable rows and codex uses the revised
wording.

## Major revisions

### R1. §8.5 Mechanized lemma anchor

**Proposal wording**:
> "The duality-confinement master theorem (`needles.tex` §5 Thm
> `thm:main:duality-confinement-master`) has partial Lean
> mechanization. Strengthening to operator-theoretic generality
> with the trace identity and Douglas domination is mechanization-
> eligible work that would anchor SDTC's framework apparatus."

**Mechanization delivered**: complete Lean mechanization at the
**typed positive-cone abstraction level** (mathlib-free). Operator-
theoretic generality (trace-class operators, Hilbert–Schmidt,
Schatten ideals) remains an open extension.

**Revised wording (use in body)**: "The duality-confinement master
theorem is mechanized in Lean at the typed positive-cone level
(`MasterTheorem.masterTheorem` in
`SixBirdsDualityConfinement.DualityConfinement.MasterTheorem`).
Operator-theoretic generality — extending the proof to trace-class
operators on a Hilbert space with the full trace-norm topology —
remains an open extension. The mechanization composes typed-cone
monotonicity, the squeeze argument, and the positivity-to-zero
implication with the separation–confinement theorem (mechanized
separately as `separationConfinement`)."

**Sections to apply**: `sec:master_theorem`, `sec:scope`,
`sec:discussion` (future work), `app:formalization`.

### R2. §2.4 mechanism / operator-theoretic-generality framing

**Proposal wording**:
> "SDTC operationalizes via `needles.tex` §5 Theorem
> `thm:main:duality-confinement-master`: Given an involutive object
> ledger `(X, J, μ, ψ)` with separating anti-invariant readout `ψ_-`,
> and a sequence of completed domination records `A_X ⪯ B_n` with
> `tr B_n → 0`, the master theorem yields `A_X = 0` and hence
> `μ(X ∖ Fix(J)) = 0`."

**Mechanization delivered**: the master theorem mechanization
encodes `⪯` and `tr` as typed-cone primitives with monotonicity
and squeeze taken as typed-cone axioms / explicit hypotheses
(rather than derived from operator-theoretic infrastructure).
Faithful to the statement; abstract in encoding.

**Revised wording (use in body)**: "The mechanism is operationally
captured by an operator-style squeeze argument over a typed positive
cone. The cone abstracts what is needed of trace-class positive
operators: a partial order `⪯` corresponding to Loewner dominance,
a trace functional `tr` with `A ⪯ B ⟹ tr A ≤ tr B`, and the
positivity axiom that a positive element with `tr A = 0` equals
zero. The master theorem (Section 7) takes these as primitives and
yields `A_X = 0` from the sequence of completed domination records,
hence `μ(X ∖ Fix(J)) = 0`."

**Sections to apply**: `sec:intro`, `sec:framework`,
`sec:anti_invariant_ledger`, `sec:master_theorem`, `sec:scope`.

### R3. Appendix A "aspirational" theorem statements

**Proposal wording** (§Appendix A):
> "**Theorem 1 (SDTC core)**: ... **Theorem 2 (SDTC apparatus
> equivalence)**: ... **Theorem 3 (SDTC cross-substrate)**: ...
> These theorem statements are aspirational; their proofs require
> the pending work in Section 8."

**Mechanization delivered**: Theorem 1 is named-as-recognition-source
(supplied by the formed closure's content), not a Lean-derived
theorem. Theorem 2 (apparatus equivalence between the SDTC structural
claim and the existence of the domination-record sequence) is
mechanized in spirit — the master theorem encodes the forward
direction (records ⟹ collapse); the reverse direction (collapse ⟹
records would obtain) is not formally bidirectionalized. Theorem 3
(cross-substrate applicability) is NOT mechanized — only the
single-substrate RH instance is validated (in Paper 2).

**Revised wording (use in body)**:
- Theorem 1: presented as the named structural law (recognition
  source), not a Lean-derived theorem. Wording: "Self-Dual Trace
  Confinement is named as the structural law: where a formed
  closure carries genuine involutive self-duality, the load-bearing
  content (the existence of the domination records) is supplied as
  closure content per Foundations I, not derived from framework
  primitives."
- Theorem 2: scoped to the forward direction (mechanized) with an
  explicit note about the reverse. Wording: "The master theorem
  (Theorem 7.1) realizes the forward apparatus implication; a
  bidirectional equivalence between the SDTC structural claim and
  the existence of the domination records is not formally
  established in this paper."
- Theorem 3: marked as future work. Wording: "Whether the master
  theorem's structural form applies cross-substrate (across closures
  with genuine involutive self-duality beyond the RH instance) is an
  open question; the only mechanized validation is the
  RH-via-SDTC-Selberg closure of the companion paper [Paper 2]."

**Sections to apply**: `sec:scope`, `sec:discussion` (future work),
`app:formalization`.

### R4. Optimized-trace-budget proposition

**Proposal wording** (§6.4 implicit):
> "**Proposition (Optimized scalar trace budget)**: `inf_{t>0} tr B_n(t) = (√a_n + √b_n)²` ... **Proof**: minimize `(1+t) a_n + (1+t^{-1}) b_n` over `t > 0`."

**Mechanization delivered**: `optimizedTraceBudget` in
`DefectedBudget.lean` takes AM-GM as a typed-Scalar hypothesis
(`am_gm_optimization`) rather than deriving it from
`(x - y)² ≥ 0`. The abstract-Scalar encoding does not provide enough
arithmetic structure to derive AM-GM substantively.

**Revised wording (use in body)**:
"In our typed-Scalar encoding, the AM-GM step in the proof of the
optimized scalar trace budget is taken as a typed-Scalar hypothesis
rather than derived from a quadratic-non-negativity axiom on a
typed real-arithmetic structure. The optimized scalar trace budget
is thus **tracked by the formalization harness** as a typed
projection over the AM-GM hypothesis; a substantive Lean derivation
would require extending the abstract-Scalar encoding with sufficient
arithmetic to express the inequality `(√a - √b)² ≥ 0`."

**Sections to apply**: `sec:exhaustive_squeeze_and_budgets`,
`sec:scope`, `app:formalization`.

## Minor / wording-tightening revisions

### R5. §2.3 structural variables framing

**Proposal wording**:
> "The law identifies a single structural variable controlling
> fixed-locus confinement: the genuineness of involutive
> self-duality at the formed layer."

**Mechanization status**: the mechanization does NOT encode
"genuineness" as a Lean-side predicate; it takes the typed
involutive ledger as input and asks no question about whether the
involution is "genuine" in any framework-theoretic sense. The
genuineness check is a paper-prose qualifier on when the master
theorem applies.

**Revised wording (use in body)**: "The structural variable is the
existence of the typed involutive object ledger with a separating
anti-invariant readout. Whether the involution is 'genuine' at the
formed-layer level — i.e., whether the ledger is closure-content
rather than a formal annotation — is a framework-discipline
question, not a Lean-side predicate."

**Sections to apply**: `sec:involutive_ledger`, `sec:scope`.

### R6. §3.3 audit-currency derivability tension framing

**Proposal wording**:
> "Steps 441–447 explicitly diagnosed the obstacle: concrete audit
> content smuggles arithmetic data; formal audit content lacks
> positivity force. Weil positivity is therefore readout-level
> (target-adjacent), not source-level."

**Mechanization status**: not directly mechanized; this is cascade-
internal documentation of why the recognition source must be named
explicitly rather than derived analytically.

**Revised wording (use in body)**: The Weil-positivity discussion is
RH-paper material (Paper 2 `sec:discussion`). In Paper 1 (DC), the
cascade's derivability-tension argument is referenced briefly as
"the cascade's own diagnostic that the duality-confinement
structural content must be named as recognition source rather than
sought as a derivation from analytical instantiations" — without
naming Weil positivity (an RH-specific carrier) in detail.

**Sections to apply**: `sec:scope`, `sec:discussion`.

### R7. §5 generalizations framing

**Proposal wording**: Section 5 describes generalizations across
self-dual structures: quantum self-adjointness, CPT, gauge,
particle-antiparticle, function-field RH.

**Mechanization status**: NOT mechanized for any of these. The only
single-substrate validation is RH-via-SDTC-Selberg (Paper 2).

**Revised wording (use in body)**: keep proposal §5 framing
("structural predictions") with strengthened disclaimer that these
are pointers and not established results. Per scope-fence canonical
nonclaim. Wording: "These cross-substrate generalizations are
structural predictions of the SDTC framing: if a formed closure
carries a genuine involutive self-duality on its visible ledger,
the master theorem's hypotheses would apply with the corresponding
domination-record discipline. They are not established results of
this paper; the single-substrate validation is the
RH-via-SDTC-Selberg closure in [Paper 2]."

**Sections to apply**: `sec:discussion`.

### R8. Paper-paper-grade vs theorem-grade vocabulary

**Proposal wording** (multiple sections):
> "paper-proposal-grade", "diagnosis-grade", "theorem-grade"

**Drafted-paper status**: drop the framework-internal grade
vocabulary from body prose where possible. The contract is the
binding statement of what the paper claims; grades belong to the
cascade-internal process not the published paper.

**Revised wording (use in body)**: use direct mathematical
qualifiers — "supplied as recognition source" rather than
"recognition-grade"; "mechanized at typed-cone level" rather than
"diagnosis-grade"; "theorem in the typed-cone encoding" rather than
"theorem-grade under the encoding assumption". Per
`feedback_academic_register.md`.

**Sections to apply**: all body sections.

### R9. Outside-Six-Birds reading

**Proposal §6.3 wording** (analog from RH proposal):
> "Outside Six Birds, all three are conditional theorems on the
> respective named structural sources."

**Drafted-paper status**: the DC paper is the structural-law paper;
the conditional outside-Six-Birds reading applies most directly to
the RH paper (Paper 2). For the DC paper, the outside-Six-Birds
reading is: "the master theorem is a typed-cone squeeze theorem
that, in the operator-theoretic setting where the cone is a positive
trace-class cone, recovers the classical fact that
`0 ⪯ A ⪯ B_n ∧ tr B_n → 0 ⟹ A = 0`."

**Revised wording (use in body)**: "Outside the Six Birds framing,
the master theorem reads as a typed abstraction of a classical
operator-theoretic fact: a positive operator dominated by a sequence
of positive operators whose traces tend to zero must itself vanish.
The structural-law content of SDTC — that this trace-vanishing
sequence exists as content of formed self-dual closures — is the
named recognition source, supplied here rather than derived."

**Sections to apply**: `sec:scope`, `sec:discussion`.

## Wording vocabulary (apply consistently)

| Concept | Use (in body) | Avoid (do not use in body) |
| --- | --- | --- |
| SDTC | "named structural law"; "supplied as recognition source"; "the SDTC structural law" | "we prove SDTC"; "the SDTC theorem"; "we derive SDTC" |
| Master theorem mechanization | "mechanized at the typed positive-cone level"; "verified in Lean as `masterTheorem`" | "operator-theoretic Lean proof"; "Lean derives the trace-class result" |
| Douglas factorization | "encoded in Lean as the typed `DouglasData` carrier"; "the typed-cone formulation of the classical Douglas factorization (Douglas 1966)" | "Lean proves Douglas's theorem in full generality"; "the classical operator theorem is verified" |
| Optimized scalar trace budget | "tracked by the formalization harness"; "the AM-GM step is taken as typed-Scalar axiom" | "Lean proves the optimized trace budget"; "a Lean derivation establishes AM-GM" |
| Cross-substrate generalizations | "structural predictions"; "pointers for cross-substrate applicability" | "we prove the CPT theorem"; "we derive the gauge-invariance principle" |
| Forward reference to Paper 2 | "the worked single-substrate validation [Paper 2]"; "the RH closure of [Paper 2]" | `\Cref{thm:rh:conditional}`; `\cite{TsiokosRH*}`; "as Paper 2 proves in Theorem X" |
| Grade vocabulary | use direct mathematical qualifiers (typed-cone level; named structural law; supplied recognition source) | "diagnosis-grade"; "recognition-grade"; "paper-proposal-grade" |
