# Prose Names — Lean decl → paper-prose name

Status: Phase 1 produced 2026-05-23.

Purpose: 1-to-1 mapping from Lean declaration names to paper-prose
names. Body prose uses the paper-prose name (not the Lean
identifier; per `feedback_academic_register.md`). Lean identifier
strings appear ONLY in `app:formalization` tables.

The mapping is canonical: every drafting dispatch that touches a
Lean-cited theorem or definition uses the paper-prose name from
this table.

## Duality Confinement axis (13 inventory rows)

| Lean decl | Paper-prose name | Inventory paper_label | Notes |
| --- | --- | --- | --- |
| `SixBirdsDualityConfinement.DualityConfinement.Involution.InvolutiveObjectLedger` | "involutive object ledger" | `def:duality_confinement:involutive-object-ledger` | Sometimes "the involutive object ledger `\IOL = (X, J, μ, ψ, Y, J_iso)`" on first use |
| `SixBirdsDualityConfinement.DualityConfinement.Separation.SeparatingReadout` | "separating anti-invariant readout" (qualitative); "quantitatively separating readout" (quantitative form) | `def:duality_confinement:separating-readout` | Both forms encoded in one Lean structure |
| `SixBirdsDualityConfinement.DualityConfinement.AntiInvariantLedger.AntiInvariantLedger` | "anti-invariant object ledger" or "the anti-invariant ledger `\AX`" | `def:duality_confinement:anti-invariant-ledger` | |
| `SixBirdsDualityConfinement.DualityConfinement.AntiInvariantLedger.traceIdentity` | "trace identity" (the relation `tr A_X = ∫ ‖ψ_-‖² dμ`) | `lem:duality_confinement:trace-identity` | Body prose says "trace identity" (Lemma 4.X) |
| `SixBirdsDualityConfinement.DualityConfinement.DirectConfinement.separationConfinement` | "separation–confinement theorem" or "Theorem 5.1 (separation-confinement)" | `thm:duality_confinement:separation-confinement` | |
| `SixBirdsDualityConfinement.DualityConfinement.DirectConfinement.quantitativeConfinement` | "quantitative confinement bound" or "Theorem 5.2 (quantitative confinement)" | `thm:duality_confinement:quantitative-confinement` | |
| `SixBirdsDualityConfinement.DualityConfinement.Domination.CompletedDominationBridge` | "completed domination bridge" | `def:duality_confinement:completed-domination-bridge` | |
| `SixBirdsDualityConfinement.DualityConfinement.Domination.douglasDomination` | "Douglas factorization" (or "Douglas domination" in framework-vocabulary contexts) | `thm:duality_confinement:douglas-domination` | Body prose: "the classical Douglas factorization (Douglas 1966)" on first use; the typed-cone encoding choice is disclosed inline |
| `SixBirdsDualityConfinement.DualityConfinement.MasterTheorem.masterTheorem` | "the duality-confinement membrane theorem" or "the master theorem" | `thm:duality_confinement:master-theorem` | The HEADLINE theorem of Paper 1 |
| `SixBirdsDualityConfinement.DualityConfinement.ExhaustiveSqueeze.ExhaustiveMovingLedger` | "exhaustive moving ledger" | `def:duality_confinement:exhaustive-moving-ledger` | |
| `SixBirdsDualityConfinement.DualityConfinement.ExhaustiveSqueeze.exhaustiveSqueeze` | "exhaustive ledger squeeze" | `thm:duality_confinement:exhaustive-squeeze` | |
| (no Lean decl) | "defected obstruction budget" | `def:duality_confinement:defected-budget` | `support_only`; no manifest entry; body prose introduces the shape as motivation for the optimized trace budget |
| `SixBirdsDualityConfinement.DualityConfinement.DefectedBudget.optimizedTraceBudget` | "optimized scalar trace budget" | `prop:duality_confinement:optimized-trace-budget` | Body prose discloses the AM-GM-as-typed-Scalar-axiom limitation |

Paper-prose-only (no Lean decl, no inventory row):

| Paper-prose name | Body location | Notes |
| --- | --- | --- |
| "Self-Dual Trace Confinement" / "SDTC" / "Trace-Fixity" | `sec:master_theorem`, `sec:scope`, `sec:discussion`, `sec:conclusion` | The named structural law of Paper 1; recognition source for the master theorem hypothesis. Encoded paper-prose only (no Lean entity in DC axis); the RH-specialized version is encoded as `GammaSdtcSelberg` in Paper 2 |

## RH axis (11 inventory rows)

| Lean decl | Paper-prose name | Inventory paper_label | Notes |
| --- | --- | --- | --- |
| `SixBirdsDualityConfinement.RH.Involution.feInvolution` | "functional-equation involution" `J_L(s) = 1 - \bar{s}` or "Definition 3.X (J_L)" | `def:rh:fe-involution` | |
| `SixBirdsDualityConfinement.RH.Involution.psiMinusRh` | "anti-invariant readout for RH" `\psi_-(s) = Re(s) - 1/2` | `def:rh:psi-minus-rh` | |
| `SixBirdsDualityConfinement.RH.ZeroLedger.NontrivialZeroLedger` | "nontrivial zero ledger" `Z_ζ^{nt}` | `def:rh:nontrivial-zero-ledger` | The real-part-type abstraction disclosure goes here (audit_summary §A3) |
| `SixBirdsDualityConfinement.RH.AntiInvariantZeroLedger.AntiInvariantZeroLedger` | "anti-invariant zero ledger" `A_Z(\zeta)` | `def:rh:anti-invariant-zero-ledger` | |
| `SixBirdsDualityConfinement.RH.SatSelShell.SatSelShell` | "saturated completed Selberg trace closure" or "the saturated trace shell `Sel^!_{ζ,tr}`" | `def:rh:sat-sel-shell` | Body prose discloses admissibility-as-hypothesis encoding |
| `SixBirdsDualityConfinement.RH.TranslationT.translationTForward` | "Theorem T (forward direction)" or "the forward direction of Theorem T" | `thm:rh:translation-T-forward` | |
| `SixBirdsDualityConfinement.RH.TranslationT.translationTReverse` | "Theorem T (reverse direction)" or "the reverse direction of Theorem T" | `thm:rh:translation-T-reverse` | |
| `SixBirdsDualityConfinement.RH.TranslationT.translationT` | "translation theorem T" or "Theorem T" (`A_Z(\zeta) = 0 \iff` RH) | `thm:rh:translation-T` | The biconditional combining forward and reverse |
| `SixBirdsDualityConfinement.RH.RHConditional.GammaSdtcSelberg` | "the recognition source `\GamSDTCSelberg`" or "`\GamSDTCSelberg`" | `obl:rh:gamma-sdtc-selberg` | Typed structure carrier (NOT Lean axiom); declared inline in `RHConditional.lean` |
| `SixBirdsDualityConfinement.RH.DCMasterApplied.dcMasterApplied` | "the duality-confinement master theorem applied to `Sel^!_{ζ,tr}`" or "application of the master theorem" | `thm:rh:dc-master-applied` | Cites Paper 1's master theorem (`\SiblingDC`); body prose reproduces the master theorem statement verbatim |
| `SixBirdsDualityConfinement.RH.RHConditional.rhConditional` | "the conditional landing chain" or "the RH conditional theorem" or "Theorem 7.X (conditional RH)" | `thm:rh:conditional` | The HEADLINE theorem of Paper 2 |

## Conventions

- **First-use in body**: paper-prose name + symbol if applicable
  (e.g. "the anti-invariant object ledger `\AX`"). After first use
  in the same section, the symbol alone may be used freely.
- **Lean identifiers in body**: NEVER. Per
  `feedback_academic_register.md`, Lean identifier strings appear
  only in `app:formalization` tables (and the per-row coverage
  table in App D references the prose name from this file).
- **Cross-paper citations**: Paper 2 cites Paper 1's
  `SixBirdsDualityConfinement.DualityConfinement.MasterTheorem.masterTheorem`
  as "the duality-confinement master theorem of [1] (Theorem 7.X)";
  the Lean identifier appears only in Paper 2's App D coverage row
  for `thm:rh:dc-master-applied`.
- **The "Lean proves" wording** per
  `paper/notes/proof-presentation-policy.md` is applied to the
  paper-prose name + a parenthetical Lean identifier on the row's
  first body mention if helpful (e.g. "Lean proves the
  separation–confinement theorem (`separationConfinement`)"; after
  first mention, the prose name alone suffices).

## When the prose name shifts

If during drafting a paper-prose name shifts (e.g. "Theorem T"
becomes "translation theorem (Theorem 5.1)" once section numbering
stabilizes), update this table in the same drafting turn. The
binding constraint is the Lean decl → prose name mapping; the
exact prose wording may evolve as the body firms up.

The drafting dispatch prompts (per-axis `drafting-plan.md`) name
this file as a mandatory source.
