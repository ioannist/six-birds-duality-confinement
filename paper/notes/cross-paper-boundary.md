# Cross-Paper Boundary

Status: Phase 0 produced 2026-05-23.

Purpose: explicit list of what Paper 1 forwards to Paper 2 and what
Paper 2 imports from Paper 1. The dependency is **one-way**: Paper 2
→ Paper 1. Paper 1 is self-contained.

## The dependency

```
                  ┌──────────────────────────────────────┐
                  │   Paper 1 (Duality Confinement)      │
                  │                                       │
                  │   • SDTC structural law (named        │
                  │     recognition source)               │
                  │   • Duality-confinement membrane      │
                  │     theorem (master theorem)          │
                  │   • V-Differential trace-state-only   │
                  │     column condition                  │
                  └─────────────────┬─────────────────────┘
                                    │
                                    │  forwards (one-way)
                                    ▼
                  ┌──────────────────────────────────────┐
                  │   Paper 2 (RH closure)                │
                  │                                       │
                  │   • Imports master theorem            │
                  │   • Specializes SDTC to Γ_{SDTC-     │
                  │     Selberg} on Sel^!_{ζ,tr}          │
                  │   • Imports V-Differential placement  │
                  │     of RH as substrate condition      │
                  │   • Headline: rhConditional           │
                  └──────────────────────────────────────┘
```

## What Paper 1 forwards to Paper 2

1. **The duality-confinement master theorem** (`thm:duality_confinement:master-theorem`).
   - Lean realization: `SixBirdsDualityConfinement.DualityConfinement.MasterTheorem.masterTheorem`.
   - Paper-prose statement: given an involutive object ledger with
     separating anti-invariant readout and a sequence of completed
     domination records `A_X ⪯ B_n` with `tr B_n → 0`, visible
     object mass is confined to `Fix(J)` (i.e. `μ(X ∖ Fix(J)) = 0`).
   - Paper 2 invokes the master theorem in `thm:rh:dc-master-applied`
     to derive `A_Z(ζ) = 0` from the recognition source.

2. **The SDTC structural-law framing** (paper-prose body claim in
   Paper 1's `sec:master_theorem`, `sec:scope`, `sec:discussion`).
   - Concept: a formed Six Birds closure with genuine involutive
     self-duality cannot host visible mass off the fixed locus; the
     load-bearing content (existence of the domination records) is
     supplied as recognition source per Foundations I.
   - Paper 2 specializes this to the Selberg-class instance
     `Γ_{SDTC-Selberg}`, encoded as the typed `GammaSdtcSelberg`
     structure carrier in `RHConditional.lean`.

3. **The V-Differential trace-state-only column condition**
   (paper-prose body claim in Paper 1's `sec:framework`).
   - Concept: substrates whose visible content is read through
     trace-state observables (no witness-content exposure) are in
     the V-Differential trace-state-only column.
   - Paper 2 cites Paper 1 to establish that RH (specifically the
     completed Selberg trace closure) is in this column.

4. **Supporting apparatus**: the trace identity, direct confinement,
   completed domination bridge, Douglas factorization, exhaustive
   moving-ledger squeeze, optimized scalar trace budget — all in
   Paper 1's body sections. Paper 2 references these implicitly
   when constructing or auditing the conditional landing chain
   (e.g. the `dcMasterApplied` proof composes the master theorem
   with the typed-cone monotonicity).

## What Paper 2 does NOT import from Paper 1

- Paper 1's cross-substrate generalizations (Section 5 of Paper 1:
  CPT symmetry, gauge invariance, quantum self-adjointness,
  particle-antiparticle, function-field RH). Paper 2 is the worked
  RH-specific instance; the other generalizations are structural
  pointers (Paper 1's `sec:discussion`) not invoked by Paper 2.
- Paper 1's classical operator-theory positioning (Paper 1's
  `sec:discussion` against classical operator-theoretic squeeze
  results). Paper 2 positions against classical RH attack barriers
  (Weil positivity, Hilbert–Pólya, etc.) in its own `sec:discussion`,
  which is RH-specific.

## What Paper 1 imports from Paper 2

**Nothing.** Paper 1 is self-contained.

Exceptions: two **forward-reference paragraphs** in Paper 1 mention
Paper 2 by name as the worked single-substrate validation:

1. **In `sec:involutive_ledger`** (Paper 1 §3): the RH involution
   `J_L(s) = 1 - s̄` and its critical-line fixed locus appear as a
   worked example of the involutive-object-ledger definition. Body
   prose may say "as the worked example in the sibling paper [2]
   develops in detail" or analogous wording. This is a forward
   reference for the reader's intuition, not a content import.

2. **In `sec:master_theorem`** (Paper 1 §7): the master theorem's
   conclusion `μ(X ∖ Fix(J)) = 0` is illustrated by naming Paper 2
   as the single-substrate validation: "the application to the
   Riemann-zero ledger of the completed Selberg trace closure is
   developed in the sibling paper [2]". This is a one-sentence
   forward reference, NOT a citation of Paper 2 results.

No `\Cref` to Paper-2 labels from Paper 1. No `TsiokosRH*` bibkey
is used by Paper 1; the two forward-reference paragraphs are
**prose-only** ("the sibling paper on the worked single-substrate
RH validation"). The `TsiokosRHviaSDTC2026` entry remains in the
shared `paper/references.bib` for Paper 2's use only; Paper 1
does not cite it. This is the asymmetric form of the one-way
dependency (Paper 2 cites Paper 1 substantively; Paper 1 does not
cite Paper 2). The rule is mirrored in `paper/writing-plan.md`,
`paper/duality_confinement/notes/drafting-plan.md`,
`paper/duality_confinement/notes/claim-revision-register.md`, and
`paper/notes/references-selection.md`.

## Citation conventions across the boundary

| From | To | Citation form |
| --- | --- | --- |
| Paper 1 → Paper 2 | Forward reference (in `sec:involutive_ledger` or `sec:master_theorem`) | **prose-only**: "the sibling paper" / "the worked single-substrate validation"; no `\cite{}`; no `\Cref` to Paper 2 labels |
| Paper 2 → Paper 1 (master theorem) | Substantive import | Section number + bibkey `[1]` (`TsiokosSDTC2026`); reproduce master theorem statement verbatim where invoked |
| Paper 2 → Paper 1 (SDTC framing) | Substantive import | Section number + bibkey `[1]`; paraphrase the SDTC structural law statement as appropriate for the RH-specific specialization |
| Paper 2 → Paper 1 (V-Differential) | Substantive import | Section number + bibkey `[1]`; one-sentence summary of the trace-state-only column condition |

## Shared notation (must render identically across both PDFs)

Per `paper/notation_and_terminology.md` § "Cross-paper notation
consistency". Phase I.F (cross-paper coherence pass; runs after both
papers complete drafting) verifies identical rendering:

- `J` (involution; Paper 2 specialized to `J_L`)
- `Fix(J)` (fixed locus)
- `ψ`, `ψ_-` (readouts; Paper 2 specialized to
  `ψ_-(s) = Re(s) - 1/2`)
- `A_X` (Paper 1 generic) / `A_Z(ζ)` (Paper 2 specialized; same
  conceptual object, instantiated to the RH zero ledger)
- `⪯`, `tr` (typed-cone primitives; identical macros in both
  papers' `paper_macros.tex`)
- `B_n`, `E`, `ι_n`, `T_n` (apparatus operators)
- `Γ` (recognition source; Paper 1 `Γ_{SDTC}` paper-prose,
  Paper 2 `Γ_{SDTC-Selberg}` paper-prose + typed carrier)

## Shared scope-fence rows (applicable to BOTH papers)

Per `paper/notes/scope-fence.md`:

- Neither paper claims Lean fully verifies every body theorem at
  the level of analytic number theory or operator theory.
- Neither paper claims external classical bibliography has been
  curated in the prep arc.
- Neither paper treats `support_only` / `out_of_scope_meta` /
  `out_of_scope_recognition_source` material as a preserved body
  claim.

## Sequential execution

Per `feedback_no_batching.md` + manager directive: Paper 1 is
drafted to its full Phase I.G closure (mechanization → math
extraction → contracts → notation → all 11 body sections → App D
→ submission deliverables) before Paper 2's drafting arc begins.
No interleaving.

After both papers complete drafting (their respective Phase I.G),
the cross-paper coherence pass (Phase I.F in the full plan) runs:
- Notation consistency across both PDFs
- Paper 2's master-theorem citation reproduces Paper 1's statement
  verbatim
- Bibliography consistency
- Defects routed per-axis to the corresponding paper's codex thread
