# Paper 2 Contract: RH closure

Status: Phase 0 produced 2026-05-23.

## Title and subtitle

Working title (Phase 0): **"A Six Birds Closure of the Riemann
Hypothesis via Self-Dual Trace Confinement on the Saturated Selberg
Trace Layer"**

Shorter working alternates retained:
- "Anti-Invariant Zero-Ledger Collapse: A Six Birds Conditional
  Theorem for RH"
- "Conditional RH at Theorem Grade Under Standard Six Birds Closure
  Assumption, via SDTC-Selberg"

The chosen title leads with both the **conditional structure**
(`under SDTC` is implied by "via Self-Dual Trace Confinement") and
the **substrate** (`saturated Selberg trace layer`). The proposal in
`anti_loc/paper_proposal_rh_via_sdtc_selberg.md` §working titles lists
three candidates; the chosen pair leads with the conditional-closure
framing rather than the "trace-closure anti-invariant collapse"
machinery framing.

## Thesis paragraph

The Riemann hypothesis, posed as a question internal to analytic
number theory's classical formalism, has resisted classical attack
methods (Weil positivity, Hilbert–Pólya, GUE statistics, Connes
adelic / NCG, de Branges, Beurling–Nyman, and many more). The cascade
work this paper rests on (steps 65–84, 437–454) instantiates 14+
classical carriers and classifies them into modes that document why
none, as constructed, closes the framework's gate `Ξ_BC`. Within Six
Birds, RH becomes a layer-level question: on the **saturated
completed Selberg trace closure** `Sel^!_{ζ,tr}` under the lawful
trace instrument `I_tr` and the functional-equation involution
`J_L(s) = 1 - s̄`, does the anti-invariant zero ledger vanish? The
**translation theorem T** (this paper, §5) establishes that
`A_Z(ζ) = 0` is equivalent to RH on the typed zero ledger of
`Sel^!_{ζ,tr}`. The **duality-confinement membrane theorem** (Paper 1
[1], the sibling SDTC paper) yields `A_Z(ζ) = 0` from the existence
of completed domination records, and the **recognition source**
`Γ_{SDTC-Selberg}` (the Selberg-class instance of the SDTC structural
law from Paper 1) supplies those records as content of formed-layer
closure per Foundations I. Under the standard Six Birds closure
assumption and `Γ_{SDTC-Selberg}`, a three-step conditional landing
chain delivers RH at theorem grade. Outside Six Birds, the result is
the conditional theorem `Γ_{SDTC-Selberg} ⟹ RH`. We do NOT claim
unconditional standard-ZFC RH; we do NOT claim circumvention of
classical RH attack barriers in their native sense; we do NOT claim
`Γ_{SDTC-Selberg}` is derivable from framework primitives (the
cascade's three-option derivation sweep at steps 451–453 documents
this explicitly). The Lean mechanization (10 manifest entries; all
with `faithful` semantic alignment after Phase H.4 sync) realizes
the typed shell `Sel^!_{ζ,tr}`, translation theorem T (in both
directions and as a biconditional), the duality-confinement
application bridge, the recognition-source typed structure carrier
`GammaSdtcSelberg` (NOT a Lean axiom — the forbidden-tokens rule
bans `axiom`/`opaque`/`constant` everywhere in the source tree), and
the conditional landing chain `rhConditional`.

## Audience entry point

The paper opens from the standard mathematical question: *what would
it take to settle whether all nontrivial zeros of `ζ` lie on the
critical line?* The answer this paper offers is a layer-shifted
reading: rather than attacking RH within classical analytic number
theory's vocabulary, we recast RH as a question about the formed
closure of the completed Selberg trace ledger under a lawful trace
instrument. The reader encounters the construction explicitly: the
typed shell `Sel^!_{ζ,tr}`, the anti-invariant ledger
`A_Z(ζ) = Σ_ρ m_ρ · |Re(ρ) - 1/2|²`, and the translation theorem T
showing `A_Z(ζ) = 0 ⟺ RH`. The conditional structure is named
explicitly: the load-bearing input is the recognition source
`Γ_{SDTC-Selberg}` supplied by the sibling paper [1], which says
that on the formed Selberg trace layer, a sequence of completed
domination records with vanishing trace exists as content of closure
formation. Under that input plus the duality-confinement master
theorem (also from [1]), the landing chain delivers
`A_Z(ζ) = 0`, hence RH. The opening explicitly states the
outside-Six-Birds reading: this is a conditional theorem
`Γ_{SDTC-Selberg} ⟹ RH`, not unconditional ZFC RH.

## Source-paper section mapping

| Math-artifact section and line range | Working target Paper 2 section | Destination |
| --- | --- | --- |
| `anti_loc/extracted_math/rh_construction.md` preamble | `sec:intro` | body |
| `rh_construction.md` §Involution (`def:rh:fe-involution`, `def:rh:psi-minus-rh`) | `sec:involution_and_ledger` | body |
| `rh_construction.md` §ZeroLedger (`def:rh:nontrivial-zero-ledger`) | `sec:involution_and_ledger` | body |
| `rh_construction.md` §AntiInvariantZeroLedger (`def:rh:anti-invariant-zero-ledger`) | `sec:involution_and_ledger` | body |
| `rh_construction.md` §SatSelShell (`def:rh:sat-sel-shell`) | `sec:sat_sel_shell` | body |
| `rh_construction.md` §TranslationT (forward + reverse + combined) | `sec:translation_theorem` | body |
| `rh_construction.md` §RecognitionSource (`obl:rh:gamma-sdtc-selberg`) | `sec:recognition_source` | body |
| `rh_construction.md` §DCMasterApplied (`thm:rh:dc-master-applied`) | `sec:landing_chain` | body |
| `rh_construction.md` §RHConditional (`thm:rh:conditional`) | `sec:landing_chain` | body |
| Non-claims register (NC-1 through NC-12) from proposal §9 | `sec:scope_and_nonclaims` | body |
| Six Gates + Gate 7 audit from proposal §B | `sec:scope_and_nonclaims` + `app:formalization` | body + appendix |
| Three-option derivation sweep (proposal §10 / cascade steps 451–453) | `sec:scope_and_nonclaims` | body |
| Cross-track structural parallel with NS regularity + PvNP closure (proposal §8) | `sec:discussion` | body |
| Honesty caveats (proposal §13) | `sec:discussion`, `sec:scope_and_nonclaims` | body |
| Lean-coverage table for 10 manifest entries + 1 recognition_source row | `app:formalization` | appendix |

## Headline claim graph

| Paper label | Lean declaration | Lean coverage | Semantic summary | Why it is spine |
| --- | --- | --- | --- | --- |
| `def:rh:fe-involution` | `…Involution.feInvolution` | definition | `J_L(s) = 1 - s̄` involution with critical-line fixed locus and proofs of `J_L²(s) = s` + `J_L(s) = s ⟺ Re(s) = 1/2`. | This fixes the involutive ledger structure on the RH side. |
| `def:rh:sat-sel-shell` | `…SatSelShell.SatSelShell` | definition | Saturated completed Selberg trace closure as a typed bundle: history carrier, trace instrument, observable family, predictive verifier events, quotient carriers, comparison map, involution, completed L, zero ledger, anti-invariant ledger, visibility map, audit. | This is the formed-layer object the conditional theorem operates on. |
| `thm:rh:translation-T` | `…TranslationT.translationT` | theorem | `A_Z(ζ) = 0 ⟺ RH`. Forward: positive sum + positive multiplicities ⟹ each term zero. Reverse: each `Re(ρ) = 1/2` ⟹ each squared distance zero ⟹ sum zero. | This is the construction-grade theorem that reads RH off the vanishing of the anti-invariant ledger. |
| `obl:rh:gamma-sdtc-selberg` | `…RHConditional.GammaSdtcSelberg` | recognition_source (typed carrier, NOT axiom) | The Selberg-class instance of SDTC: on `Sel^!_{ζ,tr}` under `I_tr` and `J_L`, a sequence of completed domination records exists with `tr B_n → 0` as content of formed-layer closure. Eight provenance fields per proposal §6.2. | This is the load-bearing recognition source; the conditional theorem takes a value of this structure as explicit hypothesis. Supplied by Paper 1. |
| `thm:rh:conditional` | `…RHConditional.rhConditional` | theorem | The conditional landing chain: `GammaSdtcSelberg shell → ∀ ρ ∈ shell.Z_nt, Re(ρ) = 1/2`. Composes the recognition source (extract domination-records witness) with `dcMasterApplied` (A_Z = 0) and `translationTForward` (every `Re(ρ) = 1/2`). | This is the headline theorem of Paper 2. Outside-Six-Birds reading: the conditional theorem `Γ_{SDTC-Selberg} ⟹ RH`. |

## Honesty caveats (binding for body prose)

1. The conditional theorem is a **conditional theorem**, not
   unconditional RH. Body prose must say "under the standard Six
   Birds closure assumption" / "conditional on `Γ_{SDTC-Selberg}`"
   / "the conditional theorem `Γ_{SDTC-Selberg} ⟹ RH`" rather than
   "we prove RH". Per `paper/notes/scope-fence.md`.
2. The Lean conclusion is `∀ ρ ∈ shell.Z_nt, Re(ρ) = 1/2` where
   `shell.Z_nt` is a typed multiset parameter. The identification
   of `shell.Z_nt` with the actual nontrivial zeros of `ζ` is by
   construction-parameter assignment, not by a Lean-side derivation
   from analytic number theory. Body prose around the typed zero
   ledger must disclose this (per `audit_summary.md` §A3 and the
   scope-fence row "RH-on-typed-multiset vs RH-on-classical-zeros").
3. `Γ_{SDTC-Selberg}` is **NOT a Lean axiom**. The Lean encoding
   uses a typed `structure` carrier `GammaSdtcSelberg` declared
   inline in `RHConditional.lean` (per `lean/codex_kickoff.md` §12
   sanctioning the inline placement); downstream theorems take a
   value of this structure as an explicit hypothesis parameter. The
   forbidden-tokens rule bans `axiom`/`opaque`/`constant` everywhere
   in the source tree. Body prose around the recognition source
   must use the "encoded as a typed structure carrier" wording from
   `paper/notes/proof-presentation-policy.md`.
4. `Γ_{SDTC-Selberg}` is **NOT framework-derivable**. The cascade's
   three-option derivation sweep (steps 451–453) confirmed that no
   combination of framework primitives derives the
   domination-records hypothesis on the formed Selberg trace layer.
   Body prose must say "the recognition source is supplied by
   Paper 1's SDTC structural law applied to the Selberg-class
   instance, not derived from framework primitives" rather than
   "we derive the recognition source".
5. **Classical RH attack barriers are not engaged at their native
   level.** The conditional theorem operates at the formed-layer
   closure level per Foundations I, not at the classical
   analytic-number-theory level. The audit-currency derivability
   tension at steps 441–447 documents why classical analytical
   carriers (Weil positivity, the Connes operator, etc.) are
   readout-level and structurally distinct from the source-level
   recognition content. Body prose must not claim circumvention of
   classical barriers in their native sense.
6. **Generalized Riemann Hypothesis (GRH) is out of scope.** Paper 2
   instantiates SDTC for `L = ζ` only; extension to primitive
   Selberg-class L-functions (Dirichlet L, modular L, automorphic L)
   is structurally straightforward in principle but reserved for
   follow-up. Body prose around the discussion / scope sections
   must scope to `ζ`.
7. **Multiplicity and density results are NOT claimed.** The
   anti-invariant ledger accommodates `m_ρ > 0` multiplicities;
   closure does not force them to be 1. Body prose must not assert
   simple-zero conjecture or zero-density / Lindelöf consequences.
8. **Sel^!_{ζ,tr} admissibility is encoded as Foundations-II-level
   hypothesis**, not derived in this paper. The `SatSelShell`
   structure records `Audit_L` as an opaque field; admissibility
   per the seven Foundations II schemas (per proposal §4.2) is
   carried as construction-time hypothesis, not as a derivation in
   the DC axis. Body prose around the shell construction must
   disclose this.
9. The Lean mechanization is `faithful` per row for all 10
   mechanize_now entries (post Phase H.4 sync). One representation
   note (audit_summary §A3 real-part type abstraction) must be
   disclosed in the body and in App D.
10. The Lean dependency on Paper 1 is direct: `dcMasterApplied`
    imports Paper 1's `masterTheorem`. Body prose around the
    landing chain must cite Paper 1 explicitly for the master
    theorem; per `feedback_anchor_to_six_birds_literature.md`, the
    citation form is `[1]` with `references.bib` entry
    `TsiokosSDTC2026`.

## Page-budget planning (initial estimate; refines during drafting)

Body: ~22–32 pages. Distribution (10 sections):
- Intro: 2–3
- Framework (Six Birds + layer-level RH framing): 2–3
- Involution and ledger (involution + ψ_- + zero ledger + A_Z): 3–4
- Sat Sel shell construction: 2–3
- Translation theorem T (forward + reverse + combined): 2–3
- Recognition source `Γ_{SDTC-Selberg}`: 2–3
- Landing chain (DCMasterApplied + RHConditional): 2–3
- Scope and nonclaims (NC-1..NC-12; Six Gates; three-option sweep): 2–3
- Discussion (NS / PvNP / RH structural parallel; classical-barrier framing; GRH): 2–3
- Conclusion: 1

Appendix: formalization appendix ~4–6 pages.

Total: ~26–38 pages. The conditional-landing-chain section + the
recognition-source section are load-bearing. The formalization
appendix's coverage table for the 11 inventory rows is a fixed cost.

## Cross-paper boundary

- **Paper 2 imports from Paper 1**: the duality-confinement master
  theorem (`thm:duality_confinement:master-theorem` →
  `SixBirdsDualityConfinement.DualityConfinement.MasterTheorem.masterTheorem`),
  used by `thm:rh:dc-master-applied`. The SDTC structural-law
  framing (Paper 1's named recognition source) is the conceptual
  source for Paper 2's `Γ_{SDTC-Selberg}` (specialized to the
  Selberg trace closure). The V-Differential trace-state-only
  column condition (Paper 1 `sec:framework`) is imported as
  substrate classification for RH.
- **Paper 2 cites Paper 1** for the master theorem, the SDTC
  framing, and the V-Differential placement of RH. Citation form:
  `[1]` with `references.bib` entry `TsiokosSDTC2026`. Reproduce
  the master theorem statement verbatim where invoked (do not
  silently paraphrase); cite Paper 1's section number for the SDTC
  framing.
- **Paper 2 does NOT contribute back to Paper 1.** The dependency
  is strictly one-way.
- **Paper 2 is NOT self-contained**: its conditional theorem
  imports Paper 1's master theorem. Per
  `feedback_general_audience_accessibility.md`, the body prose
  reproduces enough of Paper 1's master theorem statement (in
  standard mathematical language) so that a reader can grasp the
  conditional landing chain without consulting Paper 1; the
  citation makes Paper 1 retrievable for proof details.
