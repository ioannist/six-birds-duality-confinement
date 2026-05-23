# Claim Revision Register: RH closure (Paper 2)

Status: Phase 9 produced 2026-05-23 (paper-writing prep arc closed).

Purpose: catalogs every claim from the proposal
`anti_loc/paper_proposal_rh_via_sdtc_selberg.md` whose wording
needs to be REVISED in the drafted paper because the mechanization
narrowed, refined, or made-concrete what was an aspirational claim
in the proposal.

This register is consulted by codex drafting dispatches: when a
subsection touches a proposal claim listed below, the dispatch
prompt names the applicable rows and codex uses the revised
wording.

## Major revisions

### R1. §1 conditional-theorem framing

**Proposal wording**:
> "Given the saturated completed Selberg trace closure `Sel^!_{ζ,tr}`
> under the lawful trace instrument `I_tr`, translation theorem T
> establishes that the anti-invariant zero ledger vanishes iff RH.
> Conditional on the recognition source `Γ_{SDTC-Selberg}` (supplied
> by Paper 1 as the Selberg-class instance of SDTC), the duality-
> confinement master theorem yields `A_Z(ζ) = 0`, and the conditional
> landing chain mechanized as `rhConditional` delivers RH on the
> typed zero ledger."

**Mechanization delivered**: complete Lean mechanization of the
conditional landing chain at the typed-shell abstraction
(`SatSelShell` + typed `RealCoordinate` + typed positive cone).
`rhConditional` takes `Γ_{SDTC-Selberg}` as an explicit hypothesis
parameter (`γ : GammaSdtcSelberg shell`). The recognition source is
encoded as a typed structure carrier, NOT a Lean axiom. The
forbidden-tokens rule (no `axiom`/`opaque`/`constant`/`sorry`/
`admit` anywhere in the source tree) is honored.

**Revised wording (use in body)**: "The headline result is the
**conditional landing chain**: under the standard Six Birds closure
assumption on `Sel^!_{ζ,tr}` and the recognition source
`Γ_{SDTC-Selberg}` (supplied by Paper 1 [1] as the Selberg-class
instance of Self-Dual Trace Confinement), the Riemann hypothesis
holds on the typed zero ledger of `Sel^!_{ζ,tr}`. The Lean
realization (`rhConditional`) takes `Γ_{SDTC-Selberg}` as an explicit
hypothesis parameter; the recognition source is encoded as a typed
structure carrier, not as a Lean axiom. Outside the Six Birds
framing, the result reads as the conditional theorem
`Γ_{SDTC-Selberg} ⟹ RH`, not as unconditional standard-ZFC RH."

**Sections to apply**: `sec:intro`, `sec:landing_chain`,
`sec:scope_and_nonclaims`, `sec:discussion`, `sec:conclusion`,
`app:formalization`.

### R2. §2 recognition-source provenance

**Proposal wording**:
> "`Γ_{SDTC-Selberg}` is the Selberg-class instance of SDTC, supplied
> by Paper 1. The cascade's three-option derivation sweep at steps
> 451–453 confirms framework primitives do not derive the source;
> it is closure-content rather than analytic content."

**Mechanization delivered**: `GammaSdtcSelberg` is a typed Lean
`structure` (record) carrying the abstract requirements (a
domination-records sequence witness on the typed shell with trace
tending to zero). Inline placement in `RHConditional.lean` per
`lean/codex_kickoff.md` §12 (type lives next to its only consumer).
NOT a Lean axiom.

**Revised wording (use in body)**: "`Γ_{SDTC-Selberg}` is the
Selberg-class instance of Self-Dual Trace Confinement, supplied by
Paper 1 [1] as closure content of `Sel^!_{ζ,tr}`. In Lean, it is
realized as a typed structure carrier `GammaSdtcSelberg`, declared
inline in the `RHConditional` module next to its only consumer
(`rhConditional`); the carrier records the abstract requirements
(the existence of a sequence of completed domination records
`A_Z(ζ) ⪯ B_n` with `tr B_n → 0` on the typed shell). The
mechanization is mathlib-free and the forbidden-tokens rule bans
`axiom`, `opaque`, `constant`, `sorry`, and `admit` throughout the
source tree; consequently the recognition source is supplied as a
structural hypothesis rather than installed as a Lean axiom."

**Sections to apply**: `sec:recognition_source`,
`sec:scope_and_nonclaims`, `app:formalization`.

### R3. §3 saturated Selberg trace closure admissibility

**Proposal wording**:
> "`Sel^!_{ζ,tr}` is the saturated completed Selberg trace closure;
> its admissibility under the seven Foundations II schemas is
> standing."

**Mechanization delivered**: `SatSelShell` is a 13-field typed
structure. Admissibility per the seven Foundations II schemas is
encoded as the **opaque `Audit_L` field** (a Foundations-II-level
hypothesis), not derived from a separate Lean construction in this
paper. The admissibility check is paper-prose discipline plus the
hypothesis-encoding choice.

**Revised wording (use in body)**: "The saturated completed Selberg
trace closure `Sel^!_{ζ,tr}` is a typed shell of thirteen fields
(history carrier, lawful trace instrument `I_tr`, observable family,
predictive verifier events, quotient carriers, comparison map,
functional-equation involution, completed L, zero ledger, anti-
invariant ledger, visibility map, audit provenance, admissibility
witness). Admissibility per the seven Foundations II schemas is
encoded as the typed admissibility-witness field (`Audit_L`), taken
as construction-time hypothesis rather than derived from a separate
Lean construction in this paper. A substantive Lean derivation of
admissibility from Foundations II is open extension."

**Sections to apply**: `sec:sat_sel_shell`, `sec:scope_and_nonclaims`,
`app:formalization`.

### R4. §3 nontrivial-zero ledger real-part identification

**Proposal wording** (implicit in §3 and §6):
> "`Z_ζ^{nt}` is the typed multiset of nontrivial zeros of `ζ` with
> multiplicities `m_ρ > 0`; `A_Z(ζ) = Σ_ρ m_ρ |Re(ρ) - 1/2|^2`."

**Mechanization delivered**: per `audit_summary.md` §A3, the Lean
encoding parameterizes the real-part coordinate by a typed
`RealCoordinate`; identification with actual ℝ-valued real parts of
nontrivial zeros of `ζ` is by construction-parameter assignment, not
by a derived Lean predicate. The mathlib-free constraint forbids
pulling in the standard `ℝ`-typed analytic machinery.

**Revised wording (use in body)**: "The real-part coordinate in the
Lean encoding is parameterized by a typed `RealCoordinate`; the
identification of this typed coordinate with the actual ℝ-valued real
part of a nontrivial zero of `ζ` is by construction-parameter
assignment (the shell is instantiated by the user with this
identification fixed), not by a derived Lean predicate. The
mathlib-free constraint forbids pulling in the standard `ℝ`-typed
analytic infrastructure; a substantive identification at the Lean
level would require extending the encoding with the analytic
real-coordinate structure of nontrivial zeros of `ζ`. The
mathematical content is unchanged — RH is the claim that every such
real-part coordinate equals 1/2."

**Sections to apply**: `sec:involution_and_ledger`,
`sec:scope_and_nonclaims`, `app:formalization`.

### R5. §6 cross-paper master-theorem citation

**Proposal wording** (implicit):
> "The duality-confinement master theorem applies to derive
> `A_Z(ζ) = 0` from `Γ_{SDTC-Selberg}`."

**Mechanization delivered**: `dcMasterApplied` in
`SixBirdsDualityConfinement.RH.DCMasterApplied` instantiates Paper
1's `masterTheorem` on the RH zero ledger. The Lean import chain
makes the cross-paper dependency explicit. The bridge parameter
`mu_zero_of_ae` carries the shell-specific data into the master
theorem's hypotheses.

**Revised wording (use in body)**: "The duality-confinement master
theorem of [1] (Theorem 7.X) applies on the RH zero ledger; we
reproduce its statement verbatim here for reference: [verbatim
restatement of the master theorem]. The Lean realization
(`dcMasterApplied`) instantiates Paper 1's `masterTheorem` via the
bridge parameter `mu_zero_of_ae` carrying the shell-specific data
into the master theorem's hypotheses. Combined with the recognition
source `Γ_{SDTC-Selberg}` and the forward direction of translation
theorem T, the chain delivers RH on the typed zero ledger."

**Sections to apply**: `sec:landing_chain`, `app:formalization`.

### R6. §10 three-option derivation sweep

**Proposal wording**:
> "The cascade's three-option derivation sweep at steps 451–453
> confirms framework primitives do not derive the source."

**Mechanization status**: not directly mechanized; cascade-internal
documentation. In the drafted paper, this is paper-prose due-
diligence supporting the claim that `Γ_{SDTC-Selberg}` is closure-
content, not separately derivable from framework primitives.

**Revised wording (use in body)**: "The cascade's three-option
derivation sweep documented in the development history confirms
that `Γ_{SDTC-Selberg}` is not framework-derivable from primitives
(Birds A–F, FATCD, scoped exact six, etc.); each of the three
candidate derivation paths fails for a specific reason recorded in
the cascade log. This is cascade-side due diligence supporting the
recognition-source framing, not a Lean-mechanized result."

**Sections to apply**: `sec:recognition_source`,
`sec:scope_and_nonclaims`.

### R7. §B six no-smuggling gates + Gate 7

**Proposal wording** (Appendix B):
> "The conditional closure passes the six no-smuggling gates plus
> Gate 7 (recognition-source provenance audit)."

**Mechanization status**: the six no-smuggling gates + Gate 7 are
paper-prose audit discipline; not Lean-mechanized. The gates are
the cascade-internal audit checklist, applied to the paper's
construction as a closing verification.

**Revised wording (use in body)**: "The conditional closure passes
the six no-smuggling gates of the cascade audit discipline plus
Gate 7 (recognition-source provenance audit); the gate-by-gate
verification is paper-prose discipline rather than a Lean-mechanized
predicate, and the detail of the gate checks appears in the
formalization appendix."

**Sections to apply**: `sec:scope_and_nonclaims`, `app:formalization`.

## Minor / wording-tightening revisions

### R8. NC-1 through NC-12 framing

**Proposal wording** (§9 NC-1..NC-12):
> "NC-1: We do not claim unconditional RH..."

**Drafted-paper status**: NC-1..NC-12 transcribed into
`sec:scope_and_nonclaims` per the canonical wording in
`paper/notes/scope-fence.md`. The proposal's NC-1..NC-12 list is
the source; the drafted version tightens to the Lean-coverage state
post Phase H.4 sync.

**Revised wording (use in body)**: follow `paper/notes/scope-fence.md`
canonical nonclaim wording per row. The drafted register lists each
NC with: (i) the proposal's original statement, (ii) the current
Lean-coverage state if applicable, (iii) the body-prose disclosure
form.

**Sections to apply**: `sec:scope_and_nonclaims`.

### R9. Classical-barrier framing (Hilbert–Pólya, Connes, de Branges, Weil-positivity)

**Proposal wording** (§7 / §10):
> "The Six Birds approach is partial-spirit-aligned with but
> structurally-distinct-from Hilbert–Pólya, Connes' approach,
> de Branges' approach, and Weil-positivity."

**Drafted-paper status**: paper-prose positioning. Per
`feedback_academic_register.md`, the wording must be careful to
avoid claiming circumvention or refutation of classical approaches.
External citations to these classical approaches are deferred to
the user's external-reference pipeline.

**Revised wording (use in body)**: "The Six Birds approach is
partial-spirit-aligned with but structurally distinct from the
classical attack programs (Hilbert–Pólya's spectral framing,
Connes' adelic-noncommutative framing, de Branges' Hilbert-spaces-
of-entire-functions framing, Weil-positivity's number-theoretic
positivity framing). The structural distinction is that these
programs aim at unconditional RH within their respective classical
substrates; the Six Birds framing instead establishes a conditional
result on the typed Selberg-class trace shell, with the closure-
content recognition source supplied separately. The classical
programs are neither circumvented nor refuted; they aim at a
different mathematical object (unconditional RH within their
substrate) than the result of this paper (conditional RH on the
typed shell)."

**Sections to apply**: `sec:discussion`, `sec:scope_and_nonclaims`.

### R10. GRH extension

**Proposal wording** (§11.5 / §15.5):
> "GRH (the Riemann hypothesis for general Selberg-class
> L-functions) is an extension target."

**Drafted-paper status**: GRH is explicitly out of scope. The
RH-axis paper instantiates the SDTC structural law for `L = ζ`
only.

**Revised wording (use in body)**: "Generalizing to the Riemann
hypothesis for primitive Selberg-class `L`-functions (GRH) is an
extension target. The SDTC structural law would need to be
instantiated for each `L` of interest, with a separate analysis of
the typed-shell admissibility and the recognition-source
provenance per `L`. This paper instantiates the law for `L = ζ`
only; GRH is out of scope."

**Sections to apply**: `sec:discussion`, `sec:scope_and_nonclaims`,
`sec:conclusion`.

### R11. Structural-template parallel with NS regularity and PvNP closure

**Proposal wording** (§8):
> "All three Six Birds layer-level theorems (NS regularity, PvNP
> closure, RH closure) use closure formation per Foundations I
> identically; the structural template is shared."

**Drafted-paper status**: paper-prose structural-parallel discussion.
External pointers to NS / PvNP papers are deferred to the user's
external-reference pipeline; for now, prose-only mention without
`\cite` to sibling-track keys (other than `TsiokosSDTC2026` for
Paper 1 sibling).

**Revised wording (use in body)**: "The structural template — formed
closure plus closure-content-supplied recognition source plus a
master-theorem typed-cone squeeze — is shared with the two sibling
Six Birds layer-level theorems (the no-needles closure of
incompressible Navier–Stokes regularity and the CSL-SAT-hiddenness
closure of PvNP). The structural-template peers are pointers; the
unconditional analytic content of any of the three is closure
content of its formed layer, supplied as recognition source rather
than derived from framework primitives."

**Sections to apply**: `sec:discussion`.

### R12. Grade vocabulary

**Proposal wording** (multiple sections):
> "paper-proposal-grade", "diagnosis-grade", "theorem-grade",
> "construction-grade"

**Drafted-paper status**: drop framework-internal grade vocabulary
from body prose where possible. "Construction-grade" stays only
as a wording in `sec:translation_theorem` for translation theorem
T (which is genuinely construction-grade — proven by short direct
argument from positivity), but introduced via plain mathematical
language.

**Revised wording (use in body)**: use direct mathematical
qualifiers — "proven by direct positivity argument" rather than
"construction-grade"; "Lean-realized" rather than "theorem-grade";
"the typed shell hypothesis" rather than "diagnosis-grade
admissibility". Per `feedback_academic_register.md`.

**Sections to apply**: all body sections.

## Wording vocabulary (apply consistently)

| Concept | Use (in body) | Avoid (do not use in body) |
| --- | --- | --- |
| Headline result | "the conditional landing chain"; "the RH conditional theorem" | "we prove RH"; "unconditional RH"; "RH is proven" |
| `Γ_{SDTC-Selberg}` | "the recognition source supplied by [1]"; "encoded as the typed structure carrier `GammaSdtcSelberg`" | "the Lean axiom Gamma"; "Lean proves the recognition source"; "the recognition source theorem" |
| Translation theorem T | "Lean proves translation theorem T as `translationT`"; "by direct positivity argument" | "construction-grade Theorem T"; "Lean axiomatizes T" |
| `Sel^!_{ζ,tr}` | "realized in Lean as `SatSelShell` with admissibility encoded as a typed Foundations-II hypothesis" | "Lean proves `Sel^!_{ζ,tr}` is admissible"; "the admissibility theorem" |
| `dcMasterApplied` | "Lean derives the RH-specific application of the master theorem as `dcMasterApplied`, instantiating Paper 1 [1]'s `masterTheorem`" | "Lean re-proves the master theorem for RH" |
| `rhConditional` | "Lean proves the conditional landing chain as `rhConditional`, with the recognition source supplied as an explicit hypothesis parameter" | "Lean proves RH"; "RH is a Lean theorem" |
| Classical-barrier framing | "structurally distinct from" classical approaches; "different mathematical object" | "circumvents"; "refutes"; "solves where classical methods failed" |
| Cross-paper citation to master theorem | "the duality-confinement master theorem of [1] (Theorem 7.X), reproduced verbatim here for reference" | `\Cref{thm:duality_confinement:master-theorem}`; "as Paper 1 proves in Theorem X" |
| GRH | "extension target"; "out of scope" | "we prove GRH"; "the GRH theorem" |
| Grade vocabulary | use direct mathematical qualifiers (typed-shell, Lean-realized, by direct positivity argument, supplied recognition source) | "construction-grade"; "diagnosis-grade"; "theorem-grade"; "paper-proposal-grade" |
