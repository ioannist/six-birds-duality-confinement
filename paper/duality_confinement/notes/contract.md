# Paper 1 Contract: Duality Confinement

Status: Phase I.A.2 produced 2026-05-23.

## Title and subtitle

Working title (Phase I.A.2): **"Self-Dual Trace Confinement"**

Working subtitle: **"A Six Birds Structural Law for Formed Closures Under Involutive Self-Duality"**

The proposal in `anti_loc/paper_proposal_self_dual_trace_confinement.md`
§options lists three candidates; the chosen pair leads with the
**central claim** (SDTC as named structural law) rather than the
apparatus (duality-confinement membrane theorem). Alternates retained
in case the cover-page decision needs revisiting:

- "Trace-Fixity: When Closure Confines Visible Mass to the Fixed Locus of a Self-Duality"
- "The Symmetric-Coherence Closure Law: Anti-Invariant Ledger Collapse Under Genuine Self-Duality"

## Thesis paragraph

Six Birds Theory's commitment to closure-content-as-structural-fact —
that closure formation per Foundations I is structurally substantive,
not derivative — has previously been articulated through two named
structural laws: no-needles via closure feasibility (for Navier–Stokes
substrates) and CSL-SAT-hiddenness (for the trace-state-only column
without explicit self-duality). This paper proposes a third structural
law for the closure shape with **involutive self-duality**: a formed
closure with genuine involutive self-duality cannot host visible mass
off the duality's fixed locus. We name this **Self-Dual Trace
Confinement (SDTC)**, equivalently **Trace-Fixity**. The mechanism is
the **duality-confinement membrane theorem**, an operator-style
squeeze argument over a typed positive cone: given an involutive object
ledger with separating anti-invariant readout, plus a sequence of
completed domination records `A_X ⪯ B_n` with `tr B_n → 0`, visible
object mass is confined to `Fix(J)`. We mechanize the master theorem
in Lean at the abstract positive-cone level (mathlib-free). The
load-bearing content of SDTC — the existence of the domination
records on the formed self-dual layer — is supplied as recognition
source, structurally identified by the V-Differential trace-state-only
column condition. We document the typed-cone encoding choices, the
projection-disclosure discipline, and the scope fence: SDTC is a
framework-internal structural law, not a derivation from external
primitives; cross-substrate generalizations (CPT symmetry, gauge
invariance, Hermitian conjugation, quantum self-adjointness, function-
field RH) are structural pointers, not established results.

## Audience entry point

The paper opens from the mathematical question: *when must an
operator-valued obstruction vanish?* The answer the framework offers
is that when a structure carries a genuine involutive self-duality and
its visible content is read through an anti-invariant trace functional,
the obstruction is bounded above by a sequence whose trace tends to
zero — and consequently must itself be zero, confining visible mass to
the fixed locus of the duality. The reader encounters concrete
examples (the Riemann-zero ledger under the functional-equation
involution; toy involutive systems in Hilbert space) and sees that the
genuineness of the self-duality at the formed layer — not the
analytic strength of any particular readout — is what controls the
collapse. The opening explicitly distinguishes the paper's
framework-internal claim from a standard operator-theoretic theorem:
the paper is naming a structural law about formed self-dual closures,
not proving a theorem about all involutive Hilbert operators.

## Source-paper section mapping

| Math-artifact section and line range | Working target Paper 1 section | Destination |
| --- | --- | --- |
| `anti_loc/extracted_math/duality_confinement_master.md` preamble | `sec:intro` | body |
| `duality_confinement_master.md` §Involution (lines ~25–60) | `sec:involutive_ledger` | body |
| `duality_confinement_master.md` §Separation + §AntiInvariantLedger (~62–135) | `sec:anti_invariant_ledger` | body |
| `duality_confinement_master.md` §DirectConfinement (~137–165) | `sec:direct_confinement` | body |
| `duality_confinement_master.md` §Domination (~167–210) | `sec:domination` | body |
| `duality_confinement_master.md` §MasterTheorem (~212–250) | `sec:master_theorem` | body |
| `duality_confinement_master.md` §ExhaustiveSqueeze + §DefectedBudget (~252–340) | `sec:exhaustive_squeeze_and_budgets` | body |
| Out-of-scope-for-Lean items (Γ_{SDTC}) + scope-fence | `sec:scope` | body |
| Cross-substrate generalizations + structural-law sibling positioning | `sec:discussion` | body |
| Honesty caveats throughout the artifact | `sec:discussion`, `sec:scope` | body |
| Lean-coverage table for the 12 manifest entries + 1 support_only def | `app:formalization` | appendix |

## Headline claim graph

| Paper label | Lean declaration | Lean coverage | Semantic summary | Why it is spine |
| --- | --- | --- | --- | --- |
| `def:duality_confinement:involutive-object-ledger` | `…Involution.InvolutiveObjectLedger` | definition | A typed tuple `(X, J, μ, ψ, Y, J_iso)` with involution `J`, positive weight `μ`, isometric involution `J_iso` on response space `Y`, and equivariant readout `ψ`. | This is the load-bearing structural object that the entire paper operates on. |
| `def:duality_confinement:anti-invariant-ledger` | `…AntiInvariantLedger.AntiInvariantLedger` | definition | The anti-invariant ledger `A_X := ∫ ψ_- ψ_-^* dμ` encoded as an element of a typed positive cone with trace functional. | This is the obstruction whose vanishing yields fixed-locus confinement. |
| `thm:duality_confinement:master-theorem` | `…MasterTheorem.masterTheorem` | theorem | Master theorem: separating readout + domination records `A_X ⪯ B_n` with `tr B_n → 0` ⟹ `μ(X ∖ Fix(J)) = 0`. | This is the central theorem of the paper. Every later result is either its proof apparatus, its mechanism analysis, or its consumer. |
| `thm:duality_confinement:douglas-domination` | `…Domination.douglasDomination` | theorem | Douglas factorization in the typed-cone encoding: `A ⪯ K ⟺ ∃ contraction T. V = TW`. | This is the operator-theoretic backbone of the domination-record discipline. |
| `prop:duality_confinement:optimized-trace-budget` | `…DefectedBudget.optimizedTraceBudget` | theorem (AM-GM as typed-Scalar hypothesis) | Optimized scalar trace budget: `inf_t tr B_n(t) = (√a_n + √b_n)²`. | This is the scalar-side reduction that makes the master theorem operationally checkable on candidate budget sequences. The AM-GM step is taken as typed-Scalar axiom; substantive derivation requires typed real-arithmetic. |

## Honesty caveats (binding for body prose)

1. SDTC is the **named structural law / recognition source**, not a
   derived theorem of framework primitives. Body prose must say
   "supplied as recognition source" or "named as structural law";
   never "we prove SDTC" or "the SDTC theorem".
2. The master theorem is mechanized in Lean at the **typed positive-cone**
   level (mathlib-free). Operator-theoretic generality (trace-class
   operators, Hilbert–Schmidt, Schatten ideals) is an open extension,
   not a Lean-side claim. Body prose around the master theorem must
   acknowledge the typed-cone formulation.
3. The Douglas factorization encoding (`audit_summary.md` §A1) bundles
   the equivalence into a typed `DouglasData` carrier; downstream
   theorems read the equivalence off the carrier. Body prose around
   `thm:duality_confinement:douglas-domination` must note this is the
   typed-cone formulation of the classical Douglas factorization, not
   a re-proof of the full operator-theoretic result.
4. The optimized-trace-budget proposition takes the AM-GM inequality
   as a typed-Scalar hypothesis (`audit_summary.md` §A2). The body
   must use "tracked by the formalization harness" wording; a
   substantive derivation requires introducing typed real-arithmetic
   structure (open extension).
5. Cross-substrate generalizations (Paper proposal §5: CPT symmetry,
   gauge invariance, Hermitian conjugation, quantum self-adjointness,
   particle-antiparticle, function-field RH) are **structural pointers**,
   not established results. The only single-substrate validation is via
   the RH closure (Paper 2). Body prose must not claim cross-substrate
   theorems.
6. The Lean mechanization does not include the recognition source
   `Γ_{SDTC}` as a Lean entity. The DC paper's mechanization is
   purely the apparatus (definitions through master theorem). The
   RH-specialized `Γ_{SDTC-Selberg}` is encoded as a typed structure
   carrier in Paper 2's `RHConditional.lean`; the DC paper does not
   re-encode it.

## Page-budget planning (initial estimate; refines during drafting)

Body: ~22–32 pages. Distribution:
- Intro: 2–3
- Framework (Six Birds context + V-Differential placement): 2–3
- Involutive object ledger: 2–3
- Anti-invariant ledger (with trace identity, separating readout): 3–4
- Direct confinement (separation-confinement + quantitative): 1–2
- Domination (bridge + Douglas factorization): 2–3
- Master theorem (the headline): 3–4
- Exhaustive squeeze + defected budgets: 2–3
- Scope (nonclaims): 1–2
- Discussion (cross-substrate generalizations, classical comparison): 2–3
- Conclusion: 1

Appendix: formalization appendix ~4–6 pages.

Total: ~26–38 pages. The master theorem section is the load-bearing
one. The formalization appendix's coverage table for the 12+1
inventory rows is a fixed cost.

## Cross-paper boundary

- **Paper 1 forwards to Paper 2**: the duality-confinement master
  theorem (as the apparatus Paper 2 invokes), the SDTC structural law
  framing (which Paper 2 specializes as `Γ_{SDTC-Selberg}`), and the
  V-Differential trace-state-only column condition (which Paper 2
  imports as substrate classification for RH).
- **Paper 1 does NOT depend on Paper 2 for anything.** Paper 1 is
  self-contained. The DC paper's claim is the structural law and its
  apparatus; the RH specialization is Paper 2's contribution.
- **Paper 2 cites Paper 1** for the master theorem, the SDTC framing,
  and the V-Differential placement of RH. The dependency is one-way.
