# Anticipated Objections

Status: Phase 6 produced 2026-05-23.

Purpose: predicted reviewer objections with pre-drafted mitigation
language. The drafting arc consults this file when constructing
the relevant body sections; the wording is a STARTING POINT that
codex paraphrases, not a verbatim insertion.

The mitigations are organized per paper (Paper 1: DC; Paper 2: RH)
plus a shared section for cross-paper objections.

## Paper 1 — Duality Confinement objections

### Q1. "How is SDTC a 'law' when it's not derived from primitives?"

**Anticipated form**: "You call SDTC a 'structural law', but you
also say it isn't derivable from framework primitives. Isn't that
just an axiom you're naming? Why call it a 'law'?"

**Mitigation**:
- SDTC is **named as recognition source**, which is a specific
  Six Birds notion: structural content of formed-layer closure
  per Foundations I, supplied by the closure formation rather
  than derived from other framework primitives. This is the same
  epistemic status as the no-needles structural law (Navier–Stokes
  closure paper) and the CSL-SAT-hiddenness structural law (PvNP
  closure paper).
- The distinction from "axiom" is operational: an axiom in the
  metalogical sense is an unprovable assumption added to the
  formal system. A recognition source in the Six Birds sense is
  closure-content; it's what closure formation provides, not
  what's posited.
- The Lean encoding makes the distinction concrete: the
  recognition source is a typed structure carrier
  (`GammaSdtcSelberg` for the Selberg-class instance in Paper 2),
  not a `axiom` declaration. The forbidden-tokens rule bans
  `axiom`/`opaque`/`constant` everywhere in the source tree.
- The cascade's three-option derivation sweep (cited from Paper
  2's scope discussion) explicitly tested derivation from
  framework primitives and confirmed the recognition-source
  status. This is documented diligence, not a definitional
  hand-wave.

**Where to apply**: `sec:intro`, `sec:master_theorem`, `sec:scope`,
`sec:discussion`. The mitigation language is reinforced by
`paper/notes/scope-fence.md` canonical-nonclaim row 1.

### Q2. "Why is the master theorem 'mechanized at typed-cone level' rather than fully operator-theoretic?"

**Anticipated form**: "Your Lean mechanization of the master
theorem doesn't engage with classical trace-class operator theory.
Without operator-theoretic generality, isn't this just an
abstract toy?"

**Mitigation**:
- The typed positive cone is a mathlib-free abstraction over what
  the master theorem ACTUALLY USES: a partial order
  (Loewner-style), a trace functional, monotonicity of trace under
  the order, and the positivity axiom that a positive element with
  trace zero is the zero element. These are the same axioms that
  classical trace-class operator theory satisfies; the typed
  abstraction is faithful to the mathematical content.
- The operator-theoretic generality (extending the typed cone to a
  fully-realized typed model of trace-class positive operators on
  a Hilbert space) is acknowledged as an open extension. The
  current encoding is what enables the master theorem to be
  Lean-verified in a mathlib-free setting; relaxing the
  mathlib-free constraint would enable the operator-theoretic
  extension as straightforward future work.
- The Lean theorem statement is `lean_substantive` with `faithful`
  semantic alignment per `paper/notes/statements-of-record.yml`.
  The typed-cone abstraction is disclosed inline in the body
  (audit_summary §A1).

**Where to apply**: `sec:master_theorem`, `sec:domination` (typed-
cone encoding of Douglas), `sec:scope`, `app:formalization`. The
mitigation language is reinforced by `paper/notes/scope-fence.md`
canonical-nonclaim row 2.

### Q3. "The optimized-trace-budget proposition takes AM-GM as a hypothesis. Doesn't that make it trivial?"

**Anticipated form**: "Your `prop:duality_confinement:optimized-trace-budget`
takes AM-GM as `am_gm_optimization`. The 'optimization' isn't a
substantive Lean derivation — it's a hypothesis. Why include it as
a 'theorem' at all?"

**Mitigation**:
- The proposition is in the inventory as `lean_coverage = theorem`
  and `proof_presentation = lean_substantive`, but the body prose
  uses the "tracked by the formalization harness" wording (per
  `paper/notes/proof-presentation-policy.md` § §A2). The body does
  not claim "Lean derives AM-GM"; it claims "Lean tracks the
  optimized scalar trace budget under the typed-Scalar AM-GM
  hypothesis".
- The substantive AM-GM derivation requires introducing typed
  real-arithmetic structure (a typed `OrderedScalar` with
  `square_nonneg` and `sqrt_sq` axioms). The current abstract-
  Scalar encoding does not provide enough structure. The
  audit_summary §A2 documents the limitation and the path to a
  substantive lift.
- The proposition is off the critical mechanization path. The
  master theorem (Section 7) is the load-bearing claim of Paper 1;
  the optimized-trace-budget proposition is documented apparatus
  for cases where the domination record is naturally a defected
  two-defect budget. The honest disclosure is that this corner of
  the apparatus is partial in the current encoding.

**Where to apply**: `sec:exhaustive_squeeze_and_budgets`,
`sec:scope`, `app:formalization`. Per
`paper/notes/scope-fence.md` canonical-nonclaim row 3.

### Q4. "Don't your Section 5 cross-substrate generalizations (CPT, gauge, quantum self-adjointness) overclaim?"

**Anticipated form**: "Section 5 reads like you're predicting CPT
invariance, gauge invariance, self-adjointness, etc. as theorems.
You haven't proved any of them. Aren't these just hand-waves?"

**Mitigation**:
- Section 5 (Discussion: cross-substrate generalizations) explicitly
  frames the generalizations as **structural predictions** and
  **pointers**, not established results. The wording is "if a
  formed closure carries a genuine involutive self-duality, the
  master theorem's hypotheses would apply with the corresponding
  domination-record discipline" — conditional, not absolute.
- The only single-substrate validation is the RH-via-SDTC-Selberg
  closure of Paper 2. Other proposed substrates (CPT, gauge,
  quantum self-adjointness, particle-antiparticle, function-field
  RH) are listed as candidates for cross-substrate validation as
  future work.
- The mitigation wording in body prose: "structural predictions
  consistent with observed physical / mathematical symmetries;
  single-substrate validation via Paper 2; cross-substrate
  validation pending future work."
- Per `paper/notes/scope-fence.md` canonical-nonclaim row 4: no
  Section 5 generalization is asserted as an established result.

**Where to apply**: `sec:discussion`, `sec:scope`. Per scope-fence
row 4.

### Q5. "Is your Douglas factorization just classical Douglas relabeled?"

**Anticipated form**: "Your typed `DouglasData` carrier just bundles
the two directions of Douglas as fields. Isn't this circular — you
assume Douglas as data and call it a theorem?"

**Mitigation**:
- The typed encoding is an honest engineering choice: in our
  mathlib-free setting, the substantive Douglas content (range-
  inclusion characterization of operator dominance) is offloaded
  to the typed cone's `DouglasData` structure with `order_to_factor`
  and `factor_to_order` fields. The Lean theorem `douglasDomination`
  is the equivalence packaging.
- The body prose discloses this explicitly: "in our typed-cone
  encoding, the Douglas factorization is bundled into the
  `DouglasData` carrier; the substantive operator-theoretic
  content (Douglas 1966) is invoked at the Hilbert-space
  realization layer, not derived here." Per `audit_summary.md`
  §A1.
- The novelty claim is NOT for Douglas factorization itself
  (classical operator theory). The novelty is the typed structural
  law SDTC and the master theorem packaging; per `paper/notes/scope-fence.md`
  canonical-nonclaim row 5, Paper 1 acknowledges Douglas as
  classical and cites the standard source.

**Where to apply**: `sec:domination`, `sec:scope`,
`app:formalization`.

## Paper 2 — RH closure objections

### Q6. "How is this 'theorem-grade' RH when it's conditional on Γ_{SDTC-Selberg}?"

**Anticipated form**: "You call this a theorem-grade RH closure
under the standard Six Birds closure assumption. But the
recognition source is unconditional in the Lean statement — it's
just a parameter. Why is this theorem-grade?"

**Mitigation**:
- The qualification is explicit: "theorem-grade UNDER THE STANDARD
  SIX BIRDS CLOSURE ASSUMPTION" — not unconditional. Inside Six
  Birds, the conditional theorem is theorem-grade in the same
  sense the NS regularity theorem and the PvNP closure are
  theorem-grade (all three use the same Foundations I closure-
  assumption move).
- Outside Six Birds, the result reads as the conditional theorem
  `Γ_{SDTC-Selberg} ⟹ RH`. Body prose says this explicitly in
  `sec:intro`, `sec:landing_chain`, and `sec:scope_and_nonclaims`.
- The Lean encoding is faithful to this conditional structure:
  `rhConditional` takes `γ : GammaSdtcSelberg shell` as an
  explicit hypothesis parameter. There is no Lean-side claim
  that the recognition source holds; the conditional structure
  is the Lean structure.

**Where to apply**: `sec:intro`, `sec:landing_chain`,
`sec:scope_and_nonclaims`, `sec:discussion`,
`sec:conclusion`. Per `paper/notes/scope-fence.md`
canonical-nonclaim row 6.

### Q7. "If Γ_{SDTC-Selberg} isn't framework-derivable, isn't this just an axiom in disguise?"

**Anticipated form**: "The recognition source is supplied as
hypothesis. The cascade tested three options for deriving it from
framework primitives and all failed. How is this different from
adding an axiom `RH-on-formed-Selberg-closure-holds`?"

**Mitigation**:
- The Lean encoding distinguishes the recognition source from a
  metalogical axiom: it is a typed `structure` carrier
  (`GammaSdtcSelberg`) with named fields (the domination-records
  existence claim being the load-bearing one), declared inline in
  `RHConditional.lean`. The forbidden-tokens rule bans
  `axiom`/`opaque`/`constant` everywhere in the source tree. The
  recognition source has typed structure broader than the readout
  (per proposal §6.3 source/readout distinction).
- The cascade's three-option derivation sweep (steps 451–453) is
  cited as cascade-side due diligence, NOT a load-bearing premise.
  Under standard Six Birds closure framing, the domination content
  is part of what closure formation per Foundations I structurally
  provides — not a separately-axiomatized claim.
- The recognition-source provenance is multi-component: the source
  record `Γ_{SDTC-Selberg}` carries 8 provenance fields per proposal
  §6.2 (duality-confinement structural law, V-Differential
  TSO placement, step 69 RH extraction, closure identity,
  instrument identity, involution data, audit provenance,
  sibling-paper cross-references). This is structurally distinct
  from a one-line axiom.

**Where to apply**: `sec:recognition_source`,
`sec:scope_and_nonclaims`, `sec:discussion`. Per
`paper/notes/scope-fence.md` canonical-nonclaim rows 7 and 8.

### Q8. "What does 'RH on the typed zero ledger' mean if shell.Z_nt isn't the actual ζ-zeros?"

**Anticipated form**: "Your Lean theorem concludes
`∀ ρ ∈ shell.Z_nt, Re(ρ) = 1/2` where `shell.Z_nt` is a typed
multiset parameter. How does this connect to the actual
nontrivial zeros of ζ?"

**Mitigation**:
- The identification of `shell.Z_nt` with the actual nontrivial
  zeros of `ζ` is by **construction-parameter assignment**, not by
  a Lean-side derivation from analytic number theory. The
  `SatSelShell` structure is parameterized by the zero ledger;
  when applied to the canonical `Sel^!_{ζ,tr}` built from the
  classical completed `Λ_ζ`, the parameter `Z_nt` is the
  classical nontrivial-zero set with its multiplicities.
- The body prose discloses this explicitly in
  `sec:involution_and_ledger` and `sec:landing_chain`. The
  identification step is itself classical analytic number theory
  (the structure of nontrivial zeros of `Λ_ζ`), not framework-
  internal.
- The audit_summary §A3 representation note documents the real-
  part-type abstraction: the Lean encoding parameterizes the real-
  part coordinate by a typed `RealCoordinate`. The classical
  ℝ-valued real-part identification is by construction-parameter
  assignment when the `RealCoordinate` is instantiated as the
  standard real line.

**Where to apply**: `sec:involution_and_ledger`,
`sec:translation_theorem`, `sec:landing_chain`,
`sec:scope_and_nonclaims`, `app:formalization`. Per
`paper/notes/scope-fence.md` canonical-nonclaim row 9 and
`paper/notes/proof-presentation-policy.md` §"Project-specific
representation notes" §A3.

### Q9. "Doesn't translation theorem T trivialize the result?"

**Anticipated form**: "Theorem T says `A_Z(ζ) = 0 ⟺ RH`. The
forward direction is 'a sum of nonnegative terms is zero iff each
term is zero'. The reverse is a substitution. Doesn't this make
the whole paper about a trivial reformulation?"

**Mitigation**:
- Theorem T is **construction-grade** by design: it is what the
  framework calls a translation, packaging the framework-internal
  predicate `A_Z(ζ) = 0` as equivalent to the standard
  mathematical statement RH (on the typed zero ledger). The proof
  IS short; the load-bearing work is NOT in Theorem T but in
  (a) the saturated trace closure construction (`sec:sat_sel_shell`,
  proposal §4), which establishes that `Sel^!_{ζ,tr}` is the
  formed layer on which the closure-content discipline applies;
  and (b) the recognition source `Γ_{SDTC-Selberg}`
  (`sec:recognition_source`), which supplies the domination
  records as content of formed-layer closure.
- The trivial-seeming nature of Theorem T is intentional: it
  separates the construction-grade content (the typed encoding of
  RH as `A_Z(ζ) = 0`) from the recognition-source content (the
  load-bearing structural hypothesis). Body prose makes this
  separation explicit.
- Analog in the sibling PvNP closure paper: Translation Theorems A
  and B (PvNP) also have short proofs; they are the
  construction-grade bridge from framework-internal predicates to
  standard mathematical statements. The substantive content lives
  in the recognition source.

**Where to apply**: `sec:translation_theorem`,
`sec:landing_chain`, `sec:scope_and_nonclaims`.

### Q10. "Is this just Weil positivity relabeled?"

**Anticipated form**: "Your conditional landing chain looks
suspiciously similar to invoking Weil's explicit-formula positivity.
Is this just a rebranding?"

**Mitigation**:
- The audit-currency derivability tension at cascade steps 441–447
  (cited in `sec:scope_and_nonclaims` and `sec:discussion`)
  explicitly documents why Weil positivity is **readout-level**
  (target-adjacent), not **source-level**. Concrete audit content
  smuggles arithmetic data; formal audit content lacks positivity
  force; Weil positivity is the analytical instantiation of the
  structural shape, NOT the source-level recognition content.
- The recognition source `Γ_{SDTC-Selberg}` is structurally
  distinct from Weil positivity: it asserts the existence of the
  completed domination records as closure-content per Foundations
  I, where Weil positivity is a specific analytical condition on
  a specific carrier. The cascade's three-option derivation sweep
  (steps 451–453) tested whether the source content could be
  derived from analytical primitives (including Weil-style
  positivity instantiations) and confirmed it could not be — that's
  what motivated naming SDTC as recognition source rather than
  deriving it from Weil-style content.
- Body prose: "partial-spirit-aligned with but structurally
  distinct from Weil positivity" — never "we use Weil positivity"
  or "we extend Weil positivity". Per `paper/notes/scope-fence.md`
  canonical-nonclaim row 10.

**Where to apply**: `sec:scope_and_nonclaims`, `sec:discussion`.

### Q11. "What about the other classical barriers (Hilbert–Pólya, Connes, de Branges, Beurling–Nyman)?"

**Anticipated form**: "Classical RH attack programs have decades of
work. How does your conditional closure relate?"

**Mitigation**:
- The conditional theorem operates at a **different layer**: the
  formed-layer closure level per Foundations I, not the classical
  analytic-number-theory layer. The classical programs (Hilbert–
  Pólya, Connes adelic / NCG, de Branges, Beurling–Nyman, etc.)
  work at the analytic-number-theory layer with classical carriers
  (operator-theoretic, NCG-theoretic, etc.) that don't close `Ξ_BC`
  per the cascade's CRCFT-mode classifications.
- The conditional theorem does NOT circumvent classical barriers
  in their native sense. Body prose: "partial-spirit-aligned with
  but structurally distinct from Hilbert–Pólya, Connes,
  de Branges, Beurling–Nyman" — never "we bypass". Per
  `paper/notes/scope-fence.md` canonical-nonclaim row 10.
- The layer-shift question (whether to accept the formed-layer
  closure assumption per Foundations I as the right level for RH)
  is what an outside-Six-Birds reader is being asked to engage
  with. The paper makes this explicit in the introduction and
  scope sections.

**Where to apply**: `sec:scope_and_nonclaims`, `sec:discussion`.

### Q12. "What about GRH? Simple zeros? Density results?"

**Anticipated form**: "Does the framework extend to GRH for primitive
Selberg-class L-functions? Does it imply simple zeros (multiplicity
1)? Does it imply density bounds (Lindelöf)?"

**Mitigation**:
- GRH for primitive Selberg-class L-functions: structurally
  straightforward extension (functional equation, completed gamma
  factors, anti-invariant zero ledger all generalize), but
  reserved for follow-up. Body prose: "RH for ζ instantiated on
  Sel^!_{ζ,tr}; the Selberg-class generalization is structurally
  straightforward in principle but reserved for follow-up." Per
  `paper/notes/scope-fence.md` canonical-nonclaim row 11.
- Simple-zero conjecture (multiplicity-1): NOT claimed. The
  anti-invariant ledger accommodates `m_ρ > 0` multiplicities;
  closure does not force them to be 1. Per scope-fence row 12.
- Density results (Lindelöf, zero-density theorems): NOT claimed.
  These are RH-adjacent but distinct conjectures with their own
  structural status. Per scope-fence row 12.

**Where to apply**: `sec:scope_and_nonclaims`, `sec:discussion`.

## Shared (both papers) objections

### Q13. "Why mechanize in Lean if you're going to take so much as hypothesis?"

**Anticipated form**: "Your master theorem takes squeeze /
trace-mono / positivity-to-zero as hypotheses. Your translation
theorem T takes the typed-cone arithmetic axioms. Your conditional
theorem takes the recognition source as a parameter. What does the
Lean mechanization actually verify?"

**Mitigation**:
- The Lean mechanization verifies the **composition**: given the
  named hypotheses, the conclusions follow. The substance is in
  WHAT THE HYPOTHESES ARE (the typed cone's positivity axioms;
  the Selberg-class instance of SDTC) and HOW THEY COMPOSE (the
  three-step landing chain). The composition is mechanically
  checked; the hypotheses are explicit.
- This is honest: a mechanization that hides the hypotheses inside
  more abstract `axiom` declarations would be less transparent.
  The forbidden-tokens rule (no `axiom`/`opaque`/`constant`) is
  the discipline that forces the hypotheses to be explicit
  parameters rather than hidden axioms.
- App D (formalization appendix) per paper documents the full
  hypothesis-vs-derivation split: which Lean entries are
  `lean_substantive` with `faithful` alignment (genuine proofs);
  which are `recognition_source` (typed carriers);
  which are `not_mechanized` (no Lean entity). Per
  `paper/notes/proof-presentation-policy.md` § 4-mode wording
  table.

**Where to apply**: `app:formalization` in both papers;
`sec:scope` (DC) / `sec:scope_and_nonclaims` (RH);
`sec:discussion` in both papers.

### Q14. "Why no external citations to classical work?"

**Anticipated form**: "Your bibliography has only three Tsiokos
references and no external classical citations. How can readers
trust the classical claims you invoke?"

**Mitigation**:
- The prep-arc bibliography is Tsiokos-only by deliberate scope
  decision. External classical references are deferred to the
  user's end-of-process external-reference pipeline (per
  `paper/notes/references-selection.md`); they will be added in a
  later pass.
- Drafting prose nevertheless names the classical works
  descriptively where invoked ("the classical Douglas factorization
  (Douglas 1966)", "standard Selberg trace machinery", etc.). The
  bibkeys are placeholders that the end-of-process pipeline fills
  in.
- This is a prep-arc artifact, not a final-paper limitation. The
  final published versions WILL include the external classical
  references.

**Where to apply**: any section that invokes classical results;
the prep-arc bibkey policy is documented in
`paper/notes/references-selection.md`.

### Q15. "How does this compare to the sibling NS / PvNP closures?"

**Anticipated form**: "You frame the RH closure as a structural
peer with the NS regularity theorem and the PvNP closure. How are
these comparable epistemically?"

**Mitigation**:
- All three Six Birds layer-level closures use the standard
  Foundations I closure-assumption move identically. The body
  prose of Paper 2 (`sec:discussion`) renders the structural
  parallel as a comparison table (proposal §8): formed layer →
  structural source applied → layer-level conclusion → translation
  → standard statement. NS, PvNP, RH each fill in the rows
  identically in structure, differently in content.
- The epistemic peer claim is internal to Six Birds: all three are
  theorem-grade under the standard closure assumption. Outside
  Six Birds, each is the corresponding conditional theorem on its
  named structural source (recognition source for PvNP and RH;
  no-needles for NS).
- The body discussion (proposal §8 in both Paper 2 prose and the
  cross-track meta paper if available) cites this parallel as
  evidence that the recognition-mode landing template is a real
  structural feature of the framework, not an isolated RH-specific
  hack.

**Where to apply**: Paper 2 `sec:discussion`; Paper 1
`sec:discussion` (briefer cross-reference).

## How this file is used during drafting

The codex dispatch prompts that touch a section addressed above
quote the relevant Q-row's mitigation language as a STARTING
POINT. Codex paraphrases (does not paste); the body prose may
condense the mitigation into a sentence or two within the larger
section, or expand it into a short defense paragraph depending on
the section's flow.

The drafting reviewer's check applies the mitigation as a discipline:
if codex's drafted prose admits the objection without addressing
it, the dispatch is sent back with the mitigation language quoted.
