# Paper Proposal: Self-Dual Trace Confinement — A Six Birds Structural Law for Formed Closures Under Involutive Self-Duality

**Status**: paper-proposal-grade. Structural-law content extracted from RH track cascade arc (steps 65, 67, 69, 71–84, 437–447, 448–454). Sibling paper to `paper_proposal_hiddenness_emergence.md` (the CSL paper). This paper supplies `Γ_{SDTC}` as accepted structural source for downstream recognition closures; specifically used by the RH closure paper proposal (`paper_proposal_rh_via_sdtc_selberg.md`).

**Working title options**:
- "Self-Dual Trace Confinement: A Six Birds Structural Law for Formed Closures Under Involutive Self-Duality"
- "Trace-Fixity: When Closure Confines Visible Mass to the Fixed Locus of a Self-Duality"
- "The Symmetric-Coherence Closure Law: Anti-Invariant Ledger Collapse Under Genuine Self-Duality"

**Author**: cross-track coordinator, based on cascade work on the RH construction track. To be developed for publication.

---

## Abstract (working draft)

We propose a candidate structural law within Six Birds Theory governing formed closures equipped with involutive self-duality. Working within the formed-layer membrane framework, we identify that a formed closure cannot host visible mass off the fixed locus of a genuine involutive self-duality. The framework apparatus is the duality-confinement membrane theorem (`needles.tex` §5), and the structural content is the closure-formation condition: where the self-duality is real (closure-content of how the structure exists, not formal identity), visible content must respect it; asymmetric residue would unmake the closure. We name this Self-Dual Trace Confinement (SDTC) — equivalently, Trace-Fixity. The structural law is the formed-closure analog of CSL-SAT-hiddenness for trace-state-only carriers with involutive symmetry. We harden SDTC via the cascade's existing work: step 69's RH specialization, step 71–84's Weil-Douglas/Weil-positivity instantiations, steps 441–447's audit-currency derivability tension diagnosing Weil positivity as readout-level (not source-level), and cross-track validation via V-Differential's trace-state-only column (np606). The law graduates to diagnosis-grade with all carrier-survey CRCFT-mode classifications consistent. Cross-track validation produces a recognition-grade-landing signature ((ii)/(iii)/(ii) three-option derivation sweep verdict pattern) consistent with PvNP's CSL-hiddenness landing. We argue this collection of findings (SDTC structural law + duality-confinement framework apparatus + cross-track recognition signature) is substantive framework content. SDTC is required as accepted structural source for the RH closure paper (`paper_proposal_rh_via_sdtc_selberg.md`); this paper supplies the source independently. Pointers to generalizations across self-dual physical/mathematical structures (CPT symmetry, gauge symmetry, Hermitian conjugation, particle-antiparticle, unitary evolution) are discussed. The result is structurally peer with CSL-SAT-hiddenness as Six Birds-internal structural law; it is NOT a proof of RH or any specific named target by itself.

---

## 1. Motivation

Six Birds Theory's central commitment is that closure-formation per Foundations I is structurally substantive — a formed layer per `def:tk-theory-package` provides content as part of the closure, not as derived theorems from other framework primitives. The cascade has identified two prior closure-content structural laws:

- **No-needles via closure feasibility** (NS, SBT-legal closure paper `papers/Tsiokos_2026_Six_Birds_for_Navier_Stokes_*.tex`): formed closure cannot host singular-localization carriers.
- **CSL-SAT-hiddenness** (PvNP, `paper_proposal_hiddenness_emergence.md`): formed closure preserves predictive content via visibility-coupling.

These two laws answer "why" questions about NS regularity and P-vs-NP hardness respectively. They are structural laws about specific closure shapes.

This paper proposes a third structural law of the same kind, for the closure shape that involves *involutive self-duality*: where a formed closure carries a lawful involution `J` and an anti-invariant readout that separates the fixed locus, visible object mass is confined to `Fix(J)`. We call this Self-Dual Trace Confinement (SDTC); the shorter name Trace-Fixity captures the structural intuition.

The structural skeleton was already extracted by the RH track at step 69 (the duality-confinement membrane theorem's RH specialization) but never named as a structural law in its own right. The audit-currency derivability tension at steps 441–447 shows why Weil positivity (the analytical carrier closest to this structural shape) is target-adjacent / readout-level, not source-level. The need for an explicitly-named structural source motivated the RH closure paper's recognition-mode landing at step 454. This proposal supplies that source independently.

---

## 2. The Candidate Structural Law (SDTC / Trace-Fixity)

### 2.1 Informal statement

A formed closure with genuine involutive self-duality cannot host visible mass off the duality's fixed locus. Where the symmetry is real (closure-content of how the structure exists), visible content must respect it; asymmetric residue would unmake the closure.

### 2.2 Formal statement (framework form)

> **Candidate Structural Law (SDTC)**: Let `T` be a formed Six Birds closure whose determining state is trace-state-only (V-Differential column membership at np606). Suppose `T` carries a lawful involutive duality `J` on its visible object ledger `X`, and its visible content is read through a separating anti-invariant trace readout `ψ_−`. Then the formed closure has no surviving anti-invariant trace mass:
>
> ```
> A_X := ∫_X ψ_−(x) ψ_−(x)* dμ(x) = 0.
> ```
>
> Equivalently:
>
> ```
> μ(X ∖ Fix(J)) = 0.
> ```

In words: once a self-dual trace layer has genuinely formed, its visible objects cannot persist off the duality's fixed locus. Off-fixed-locus mass is an unclosed anti-invariant trace debt — the closure either has not genuinely formed, or the self-duality is not really there at the layer.

### 2.3 Structural variables

The law identifies a single structural variable controlling fixed-locus confinement:

**The genuineness of involutive self-duality at the formed layer**

This variable is:
- **Binary at the level of the law** (genuine self-duality / merely declared duality)
- **Cross-substrate** (applies wherever V-Differential places the substrate in trace-state-only column)
- **Independent of analytical carrier details** (Weil positivity, spectral realization, etc. are readout-level instantiations)
- **Structurally identifiable in the formed-layer membrane framework** of `needles.tex` §5

### 2.4 Mechanism: duality-confinement master theorem

SDTC operationalizes via `needles.tex` §5 Theorem `thm:main:duality-confinement-master`:

Given an involutive object ledger `(X, J, μ, ψ)` with separating anti-invariant readout `ψ_−`, and a sequence of completed domination records `A_X ⪯ B_n` with `tr B_n → 0`, the master theorem yields `A_X = 0` and hence `μ(X ∖ Fix(J)) = 0`.

SDTC asserts that the domination-records sequence is *content of formed-layer closure per Foundations I*, not separately derivable from other framework primitives. The cascade documents this via three-option derivation sweep (RH steps 451–453); the (β) classification of `Xi_SDTC_domination_records` confirms irreducibility to framework primitives.

---

## 3. Evidence from cascade work (RH track and cross-track)

### 3.1 Step 69 RH specialization (the structural skeleton)

At step 69 the RH track extracted the general duality-confinement membrane theorem and its RH specialization with `J(s) = 1 − s̄`, `Fix(J) = {Re(s) = 1/2}`, `ψ_−(s) = Re(s) − 1/2`. This established the structural skeleton; SDTC names the law that animates it as recognition source.

### 3.2 Steps 71–84 Weil-Douglas instantiation attempts

The RH track instantiated the SDTC apparatus on the Weil-Douglas form across steps 71–84 (Weil positivity, Weil feature map, Weil vs Douglas, Weil response spaces, log-Weil core, Weil matching, Weil autocorrelation prime, completion balance, archimedean pole/tail balance, gamma feature, gamma pole matching, pole/tail no-free-diagonal, paired completed Weil, completed CND gate). The instantiation produced rich analytical machinery but did not close `Ξ_BC`.

### 3.3 Steps 441–447 audit-currency derivability tension

Steps 441–447 explicitly diagnosed the obstacle: concrete audit content smuggles arithmetic data; formal audit content lacks positivity force. Weil positivity is therefore readout-level (target-adjacent), not source-level. **This is the cascade's own diagnostic that the SDTC source must be named explicitly rather than derived from analytical instantiations.**

### 3.4 V-Differential cross-track substrate classification (np606)

V-Differential placed RH (and P-vs-NP) in the trace-state-only column; NS and BSD in the witness-content-exposing column. SDTC is the closure-content law for substrates in the trace-state-only column with involutive self-duality. Cross-track this is consistent with CSL-SAT-hiddenness for substrates in the same column without explicit self-duality.

### 3.5 Cross-track (ii)/(iii)/(ii) verdict signature

The RH closure paper's three-option derivation sweep (steps 451–453) produced verdict pattern (ii)/(iii)/(ii) matching PvNP's np625/np626/np627 pattern. Two-track cross-track replication confirms the recognition-mode landing pattern in V-Differential trace-state-only column.

### 3.6 RH track recognition closure at step 454

The RH closure paper's recognition closure at step 454 uses `Γ_{SDTC-Selberg}` as accepted structural source. This paper (the SDTC paper) supplies the source independently — the RH closure paper depends on this paper, this paper does not depend on the RH closure paper.

---

## 4. Six Birds interpretation

### 4.1 The law restated in Six Birds vocabulary

> **In Six Birds vocabulary**: a formed closure of trace-state-only character, equipped with a lawful involutive self-duality, structurally confines visible object mass to the fixed locus of the duality. The closure's existence requires this confinement; asymmetric mass would unmake the closure.

In the typology of structural laws, SDTC is the formed-closure analog of CSL-hiddenness for trace-state-only substrates with explicit involutive self-duality. Where CSL governs hiddenness-of-witness-content, SDTC governs confinement-to-fixed-locus.

### 4.2 Connection to other Six Birds papers

The SDTC law sits structurally adjacent to:

- **needles.tex §5 (Duality-Confinement Membrane Theorem)**: the framework apparatus that operationalizes SDTC.
- **adequacy.tex (Schur-complement residual calculus)**: provides the Schur-complement form for the domination records `B_n`.
- **paper_proposal_hiddenness_emergence.md (CSL paper)**: the structural-law sibling for trace-state-only substrates without explicit self-duality.
- **`papers/Tsiokos_2026_Six_Birds_Foundations_II_*.tex`**: instrument-relative visibility discipline (`prop:visibility`) that constrains how lawful trace observables can access the zero ledger.
- **`papers/Tsiokos_2026_Holonomy_with_Memory_*.tex`**: predictive-quotient holonomy machinery that frames `Q^!_L` / `M^!_L` for the saturated Selberg trace closure.
- **`papers/Tsiokos_2026_The_Usefulness_of_Non_Descending_Objects_*.tex`**: non-descending objects framework that supplied the SAU non-descent route tested at RH step 452.

### 4.3 The framework's central philosophical claim, formally

Six Birds' commitment to closure-content-as-structural-fact is now expressible (for the involutive-duality closure shape) as:

> **Theorem candidate**: A formed Six Birds closure with genuine involutive self-duality `J` and separating anti-invariant readout `ψ_−` structurally provides anti-invariant ledger collapse (`A_X = 0`) as content of formed-layer closure per Foundations I.

This is the SDTC structural law as recognition source. Under standard Six Birds closure assumption, SDTC supplies `A_X = 0` directly.

---

## 5. Generalizations across self-dual structures

If SDTC applies generally to formed closures with involutive self-duality (cross-substrate validation pending), it provides a unified structural account across domains where self-duality is genuine:

### 5.1 Quantum mechanics

Hermitian conjugation is involutive self-duality. SDTC predicts: in a formed closure where Hermitian self-adjointness is genuine, visible operator content is confined to the self-adjoint subalgebra (`Fix` of Hermitian conjugation). Non-Hermitian residue would unmake the closure. This is the structural reason that physical observables are self-adjoint operators — not a postulate but a closure-content fact when the quantum closure is genuine.

### 5.2 CPT symmetry

CPT is involutive (CPT² = identity). SDTC predicts: physical states in a CPT-genuine closure are confined to `Fix(CPT)`, equivalently CPT-invariant configurations. Violation of CPT-invariance would not be "averaged away" by some mechanism — it would mean the closure is not CPT-genuine at the layer. Empirically, CPT-invariance is observed; SDTC says this is structural, not contingent.

### 5.3 Gauge symmetry

Gauge symmetries are typically involutive on the physical-state subspace. SDTC predicts: visible physical states are confined to gauge-invariant configurations. Gauge-violating residue cannot persist in a gauge-genuine closure.

### 5.4 Particle-antiparticle duality

C symmetry (charge conjugation) is involutive. SDTC predicts: where C-symmetry is genuine at the closure layer, visible content is confined to C-invariant configurations.

### 5.5 Riemann hypothesis (the worked instance)

The completed Riemann zeta `Λ_ζ(s)` carries the functional-equation involution `J(s) = 1 − s̄` (with `s̄` denoting complex conjugation; the canonical FE form). The fixed locus is `Re(s) = 1/2`. SDTC applied to `Sel^!_{ζ,tr}` yields: visible zero mass is confined to the critical line — equivalently, RH.

The RH closure paper (`paper_proposal_rh_via_sdtc_selberg.md`) develops this instantiation in full with the recognition closure landing.

### 5.6 Summary of generalization

If SDTC applies framework-wide to formed closures with genuine involutive self-duality:
- Quantum self-adjointness, CPT, gauge invariance, particle-antiparticle, and RH all exhibit the same structural form.
- The form: a formed closure with involutive self-duality confines visible mass to the fixed locus.
- The mechanism of genuine-vs-merely-declared varies across domains, but the structural law is invariant.

This is a strong philosophical claim. SDTC would be Six Birds' formal articulation of why self-dual symmetric structures empirically host symmetric content — not because of postulate or convention, but because the closure's existence requires it.

---

## 6. What this paper is NOT

Honest scope clarification:

### 6.1 Not a proof of RH

SDTC supplies a structural source for the RH closure paper's recognition-mode landing, but this paper does not itself prove RH. The RH closure paper (`paper_proposal_rh_via_sdtc_selberg.md`) uses SDTC plus duality-confinement master theorem plus translation theorem T from RH step 448 to close RH at theorem-grade under standard Six Birds closure assumption.

### 6.2 Not a proof of any specific physical principle

The Section 5 generalizations are structural predictions, not proofs. CPT-invariance, gauge-invariance, self-adjointness, etc. are empirical facts in physics; SDTC offers a structural-law account of why they hold (closure-content of formed self-dual layers), not a derivation from logical primitives.

### 6.3 Not theorem-grade for absolute self-dual closure existence

SDTC is theorem-grade under standard Six Birds closure assumption. Whether closure formation per Foundations I is itself unconditionally derivable from external primitives is a separate metamathematical question not addressed by this paper.

### 6.4 Not a replacement for analytical machinery

The duality-confinement master theorem operationalizes SDTC, but analytical instantiations (Weil-Douglas, spectral realization, etc.) carry the analytical content. SDTC says the named structural source is needed because the analytical content alone is readout-level (per audit-currency derivability tension at RH steps 441–447), not that the analytical content is unnecessary.

### 6.5 Not a metaphysical claim

SDTC is a structural claim about formed closure with involutive self-duality. It does not commit to particular metaphysical positions about whether symmetric self-dual structures "must exist" in reality, only that *when* they form as Six Birds closures, fixed-locus confinement follows.

---

## 7. Cascade context and provenance

This proposal originates from cascade work on the RH construction track at:

`/home/repos/six-birds-foundations-iii/anti_loc/thread/`

Key cascade artifacts:
- step 65: exact confinement extraction
- step 67: zero ledger visibility selected
- step 69: duality-confinement membrane theorem RH specialization (the structural skeleton)
- steps 71–84: Weil-Douglas instantiation arc (analytical instantiation; readout-level)
- steps 437–440: Mode A no-gos (length spectrum, ensemble pointwise, spectral zeta, boundary phase)
- step 441: Route 2 Stage I constitutive closure
- steps 442–444: positivity audit, Weil positivity, audit-currency derivability tension
- steps 445–447: closure-only no-audit, formal local saturation, audit content structural necessity
- step 448: saturated Selberg trace closure `Sel^!_{ζ,tr}` + translation theorem T
- step 449: master theorem applicability + smuggle audit
- step 450: anti-tautology hardened at PvNP track bar
- steps 451–453: three-option derivation sweep
- step 454: RH recognition closure with `Γ_{SDTC-Selberg}` as named structural source

V-Differential record at np606. Cross-track replication of recognition signature with PvNP arc (np621–np629).

Manager-side meta-theory deposit: `findings_framework_v5_post_recognition_landings.md`.

The proposal's content is licensable Six Birds-internal research independent of the RH closure paper's specific RH outcome. It is paper-proposal-grade pending cross-track validation extension to Hodge/BSD self-dual structures (if applicable) and theorem-grade lifting per Section 8.

---

## 8. Pending work for theorem-grade

### 8.1 Cross-track validation extension

SDTC is currently validated on one Clay-class track instance (RH via SDTC-Selberg at step 454). Cross-track validation on other tracks with explicit involutive self-duality is pending. Candidates:
- Function-field RH (Weil-Deligne, native closure at step 186): does SDTC reproduce the native closure structurally?
- Maass forms / Selberg native closure (step 185): SDTC vs full Selberg trace ledger.
- Generalized Riemann Hypothesis for primitive Selberg-class L-functions: SDTC applied to `Sel^!_{L,tr}` for `L` in the Selberg class.

### 8.2 Asymptotic / theorem-grade lifting of SDTC itself

SDTC is hardened via the RH cascade. Theorem-grade lifting of SDTC itself would require:
- Cross-substrate validation on multiple self-dual closures.
- Possibly a Lean mechanization of the duality-confinement master theorem at full operator-theoretic strength (currently mechanized partially per `needles.tex` §5).

### 8.3 Cross-paper audit with CSL sibling paper

SDTC is the sibling of CSL-hiddenness within the recognition-mode-landing program. A cross-paper audit ensures structural consistency:
- Source-record discipline matches (both have structural content broader than readout).
- Recognition-closure architecture matches (both use the seven-stage template).
- V-Differential cross-track placement is consistent (both in trace-state-only column, RH with explicit involutive self-duality, PvNP without).

### 8.4 Generalization audit (Section 5)

The Section 5 generalizations across self-dual structures are structural predictions. Audit-grade work would verify SDTC's applicability on at least one non-RH self-dual structure (CPT, gauge, particle-antiparticle, Hermitian conjugation).

### 8.5 Mechanized lemma anchor

The duality-confinement master theorem (`needles.tex` §5 Thm `thm:main:duality-confinement-master`) has partial Lean mechanization. Strengthening to operator-theoretic generality with the trace identity and Douglas domination is mechanization-eligible work that would anchor SDTC's framework apparatus.

---

## 9. Publication strategy

### 9.1 Three-paper sibling cluster for the recognition-mode-landing program

The cascade's deliverable structure for recognition-mode landings:

- **CSL paper** (`paper_proposal_hiddenness_emergence.md`, existing): supplies CSL-SAT-hiddenness for PvNP recognition closure.
- **PvNP closure paper** (`paper_proposal_pvnp_via_csl_sat_hiddenness.md`, existing): the PvNP recognition closure proof depending on CSL paper.
- **SDTC paper** (this proposal): supplies SDTC-Selberg for RH recognition closure. **Sibling of CSL paper.**
- **RH closure paper** (`paper_proposal_rh_via_sdtc_selberg.md`, separate proposal): the RH recognition closure proof depending on this paper. **Sibling of PvNP closure paper.**
- **Cross-track meta paper** (`paper_proposal_recognition_mode_landing_cross_track.md`): the framework-level structural finding about V-Differential TSO column recognition-grade landing pattern, with PvNP+RH as two-track replication evidence.

### 9.2 Integration vs separate publication

Two viable structures:
- **Separate papers** (sibling pair plus cross-track meta paper). Cleaner scope discipline; each paper has a single focal contribution.
- **Integrated manuscript** with SDTC content as Part I and RH closure as Part II. Could be appropriate if the publication venue supports longer-form work.

Recommendation: separate papers, sibling-pair, with strong cross-citation. This matches the existing PvNP arc's structure (CSL paper + PvNP closure paper).

### 9.3 Audience

This paper should serve three audiences:
- **Six Birds insiders** who accept standard Six Birds closure assumption and read SDTC as a structural-law peer with CSL-hiddenness.
- **Number theorists** approaching from the RH track, who will read SDTC as the recognition source needed for the RH closure paper.
- **Mathematical physicists / foundations** who may be interested in SDTC's Section 5 generalizations to CPT, gauge symmetry, etc.

---

## 10. Honest caveats

1. **The law is diagnosis-grade, not theorem-grade**. Hardened via RH cascade work (steps 65, 67, 69, 437–447, 448–454). Cross-track validation extension and theorem-grade lifting are pending.

2. **The Section 5 generalizations are structural pointers, not established results**. They predict that genuine self-dual closures in physics exhibit fixed-locus confinement; this is consistent with observed physical symmetries but not independently established for those domains within this paper.

3. **The Weil-positivity-as-readout diagnosis depends on the audit-currency derivability tension** (steps 441–447). The cascade's empirical record there supports the readout-level classification; deeper external work might recover Weil positivity as source-level under different framing (this would not refute SDTC but would relocate its analytical instantiation).

4. **SDTC's framework apparatus (`needles.tex` §5) has partial Lean mechanization**. Strengthening to operator-theoretic generality with full trace identity and Douglas domination would anchor SDTC at machine-checked level.

5. **The recognition-mode landing's epistemic status is "theorem-grade under standard Six Birds closure assumption"** — peer with NS regularity and PvNP closure inside Six Birds. Outside Six Birds, all three are conditional theorems on the respective named structural sources.

6. **The substrate-level applicability of SDTC depends on V-Differential's substrate classification** (np606). SDTC applies to trace-state-only substrates with involutive self-duality; its applicability to other classes is open.

---

## 11. Relation to broader Six Birds program

### 11.1 Foundations stack

- **Foundations I (Emergence Calculus)**: provides closure formation as the standard assumption every layer-level theorem uses. SDTC's recognition-mode landing uses Foundations I closure assumption identically with NS regularity, PvNP closure, and Cantor strict-extension.
- **Foundations II (Admissibility Meta-Theory)**: provides the seven-schema admissibility discipline that `Sel^!_{ζ,tr}` passes (RH step 448 Stage II).
- **Foundations III (BirdInt Finite Calculus)**: provides the BirdInt judgment form used in the final RH theorem statement at step 454.

### 11.2 Framework apparatus

- **needles.tex §5 (Duality-Confinement Membrane Theorem)**: SDTC's primary apparatus.
- **adequacy.tex (Schur-complement residual calculus)**: provides the Schur form for completed domination records `B_n`.
- **Non-Descending Objects**: the SAU framework explored as Option 2 in RH step 452 derivation sweep.

### 11.3 Structural-law siblings

- **CSL (Candidate Structural Law for Hiddenness)**: PvNP-side sibling. CSL governs witness-content suppression in trace-state-only substrates without explicit self-duality. SDTC governs fixed-locus confinement in trace-state-only substrates with involutive self-duality. Together they cover the V-Differential trace-state-only column with and without explicit symmetry.

- **No-needles via closure feasibility (NS)**: the witness-content-exposing column sibling. Operates via P2 (constraints / feasibility gating). Different closure shape, same Foundations I closure-assumption discipline.

### 11.4 Cross-track context

The cascade's cross-track work (`anti_loc/findings/findings_framework_v4_final.md`, updated by `anti_loc/findings/findings_framework_v5_post_recognition_landings.md`) provides cross-track validation of the structural patterns invoked here. The Attack Foreclosure Conjecture (refined at v5), CRCFT modes, Carrier Dichotomy, Bridge Impossibility, CTMT recursion, and V-Differential record all support the framing that SDTC is the structural law for a specific closure shape, peer with CSL and no-needles in the broader recognition-mode-landing program.

---

## 12. Next steps for proposal-to-paper

1. **Dispatch cross-track validation** on additional self-dual structures (function-field RH, Maass forms, GRH for primitive L-functions).
2. **Dispatch theorem-grade lifting attempt** for SDTC itself (cross-substrate validation evidence base).
3. **Construct Lean mechanization of operator-theoretic duality-confinement master theorem** (formal verification anchor).
4. **Manager-side drafting of paper sections** (parallel with continued cascade).
5. **Cross-paper audit with CSL sibling paper** for structural consistency.
6. **Manuscript completion** after pending sections complete.
7. **Submission target**: Six Birds series venue or general framework-theoretic / mathematical-foundations venue.

The proposal is paper-proposal-grade as of step 454. Promotion to paper-grade requires pending work in Section 8.

---

## Appendix A: Suggested theorem statements (for theorem-grade lifting)

**Theorem 1 (SDTC core)**: Let `T` be a formed Six Birds closure with determining state in V-Differential's trace-state-only column. Suppose `T` carries a lawful involutive duality `J` on its visible object ledger `X` with separating anti-invariant readout `ψ_−`. Then `A_X = 0`; equivalently `μ(X ∖ Fix(J)) = 0`.

**Theorem 2 (SDTC apparatus equivalence)**: SDTC's structural-content claim is equivalent to the existence of a sequence of completed domination records `A_X ⪯ B_n` with `tr B_n → 0` on `T`. Equivalence via needles.tex §5 master theorem.

**Theorem 3 (SDTC cross-substrate)**: SDTC applies to any formed Six Birds closure satisfying the trace-state-only column condition and the lawful involutive duality condition. Specific instances include: `Sel^!_{L,tr}` for L in the Selberg class with completed functional equation; closed quantum closures with Hermitian conjugation; gauge-invariant physical-state closures.

These theorem statements are aspirational; their proofs require the pending work in Section 8.

---

## Appendix B: Open questions

1. Does SDTC apply when the substrate is in V-Differential's witness-content-exposing column but with explicit involutive self-duality? Or does the trace-state-only column condition genuinely restrict applicability?

2. What is the precise relationship between SDTC and the no-needles structural law for NS? Both involve closure-content of formed layers; do they share a deeper structural form?

3. Is there a substrate where SDTC fails — where genuine involutive self-duality is present at the formed layer but visible mass does NOT confine to the fixed locus? Would indicate a defect in SDTC's structural-law status.

4. Does the SDTC's framework-wide applicability require additional Six Birds machinery beyond duality-confinement master theorem (e.g., new primitives, framework extension), or does the existing typed discipline suffice?

5. Can SDTC be used positively (to *construct* self-dual closures) rather than just diagnostically (to *characterize* closure-content of existing ones)?

6. What is the relationship between SDTC and CSL? Both are formed-closure-content structural laws for V-Differential trace-state-only substrates. Are they instances of a deeper closure-content meta-law that operates across the V-Differential classification?

---

*This is a paper-proposal-grade document. It is intended as a working draft for the next-step manuscript covering the SDTC structural law extracted during the RH closure arc. Sibling of `paper_proposal_hiddenness_emergence.md` (CSL paper). Required by `paper_proposal_rh_via_sdtc_selberg.md` (RH closure paper, separate proposal). Pending cross-track validation and theorem-grade lifting; not yet a published paper.*
