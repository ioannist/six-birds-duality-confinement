# Notation and Terminology — Duality Confinement + RH Papers

Status: Phase I.A.4 populated 2026-05-23 (paper-writing pre-drafting).

This is the **single source of truth** for paper-facing names. Every
symbol used in either paper must be either:

1. Inherited from a vendored Foundations layer (F1/F2/F3) — listed
   in the "Inherited" section below with its canonical name and the
   alias used in the papers; or
2. Introduced locally in this repo — declared in the "Local" sections
   below with definition, role, and the Lean module it lives in.

No silent vocabulary. If a new term is added in either paper, it must
also be added here and in `Terminology.lean` in the same change.

## Governance

- `lean/SixBirdsDualityConfinement/Terminology.lean` declares the
  Lean side of the foundations alias surface.
- This file declares the paper side.
- Each paper `\input`s its own
  `paper/<axis>/includes/paper_macros.tex`, which defines the LaTeX
  commands rendering the symbols.
- Reserved-symbol policy: every reserved symbol below carries the
  meaning declared here. Local proofs MUST NOT repurpose a reserved
  symbol for a different role.

## Inherited from Foundations (alias surface)

| Concept | Canonical decl (foundations) | Paper-side alias | Foundation layer |
| --- | --- | --- | --- |
| Closure operator | `ClosureOp` | `F1ClosureOp` | Foundations I |
| Closure ladder strict extension | `ClosureLadder` | `F1ClosureLadder` | Foundations I |
| Idempotent endomap | `ClosureLadder.IdempotentEndo` | `F1IdempotentEndo` | Foundations I |
| Quotient packaging | `ClosureLadder.MetaPackaging.pack` | `F1PackagingPack` | Foundations I |
| Primitive roles (P1–P6) | `SixBirds.Role` | `F2Role` | Foundations II |
| FATCD host | `SixBirds.FATCD` | `F2FATCD` | Foundations II |
| Channel status | `SixBirds.ChannelStatus` | `F2ChannelStatus` | Foundations II |
| Scoped exact six | `SixBirds.scoped_exact_six` | `F2ScopedExactSix` | Foundations II |
| Typed non-collapse | `SixBirds.typed_non_collapse` | `F2TypedNonCollapse` | Foundations II |
| BirdInt audited finite calculus | `SixBirdsIII.BirdIntDomain` | `F3BirdIntDomain` | Foundations III |
| Primitive labels | `SixBirdsIII.Primitive` | `F3Primitive` | Foundations III |
| Promotion status family | `SixBirdsIII.PromotionStatus` | `F3PromotionStatus` | Foundations III |
| Claim status family | `SixBirdsIII.ClaimStatus` | `F3ClaimStatus` | Foundations III |
| Gate status family | `SixBirdsIII.GateStatus` | `F3GateStatus` | Foundations III |
| Strict gate status family | `SixBirdsIII.StrictGateStatus` | `F3StrictGateStatus` | Foundations III |
| Square status family | `SixBirdsIII.SqStatus` | `F3SqStatus` | Foundations III |
| Promotion bridge record | `SixBirdsIII.PromotionBridgeRecord` | `F3PromotionBridgeRecord` | Foundations III |
| Claim record | `SixBirdsIII.ClaimRecord` | `F3ClaimRecord` | Foundations III |
| Defect record | `SixBirdsIII.DefectRecord` | `F3DefectRecord` | Foundations III |
| Directed cell record | `SixBirdsIII.DirectedCellRecord` | `F3DirectedCellRecord` | Foundations III |
| Top-down channel record | `SixBirdsIII.TopDownChannelRecord` | `F3TopDownChannelRecord` | Foundations III |
| Visibility tag | `SixBirdsIII.VisibilityTag` | `F3VisibilityTag` | Foundations III |
| Threshold tag | `SixBirdsIII.ThresholdTag` | `F3ThresholdTag` | Foundations III |
| Level trichotomy | `SixBirdsIII.Level` | `F3Level` | Foundations III |
| Host taxonomy | `SixBirdsIII.Host` | `F3Host` | Foundations III |

Paper-side body prose typically refers to these concepts by plain
mathematical description (per `paper/notes/audience-translation.md`)
and only invokes the alias when the discussion is at the
foundations-vocabulary level (typically in App D or in `sec:framework`).

## Local to Duality Confinement (Paper 1) axis

### Reserved symbols

| Symbol | Meaning | LaTeX macro | Lean module |
| --- | --- | --- | --- |
| `X` | Visible object / root / defect space (carrier of the involutive ledger) | inline `X` | `DualityConfinement.Involution` (the `X` field of `InvolutiveObjectLedger`) |
| `J` | Involution on the object ledger; `J ∘ J = id_X` | inline `J` | `DualityConfinement.Involution` (`J` field) |
| `μ` | Positive object-ledger measure or finite weight system on `X` | inline `\mu` | `DualityConfinement.Involution` (`mu` field) |
| `Y` | Real Hilbert response space (typed carrier with inner product + norm) | inline `Y` | `DualityConfinement.Involution` (`Y` field) |
| `J_{\mathrm{iso}}` (`J_iso`) | Linear isometric involution on `Y` | `\Jiso` | `DualityConfinement.Involution` (`J_iso` field) |
| `ψ` | Equivariant readout `X → Y`; `ψ(J x) = J_iso ψ(x)` | inline `\psi` | `DualityConfinement.Involution` (`psi` field) |
| `P_-` | Anti-invariant projector `(I_Y - J_iso) / 2` | `\Pminus` | `DualityConfinement.AntiInvariantLedger` (implicit in `psi_minus` field) |
| `ψ_-` | Anti-invariant readout `P_- ψ` | `\psim` | `DualityConfinement.AntiInvariantLedger` (`psi_minus` field) |
| `\Fix(J)` | Fixed locus `{x ∈ X | J x = x}` | `\Fix(J)` | (paper-side only; the Lean encoding records membership through `J x = x` predicates) |
| `A_X` | Anti-invariant object ledger `∫_X ψ_- ψ_-^* dμ`, a typed positive cone element | `\AX` | `DualityConfinement.AntiInvariantLedger` (`A_X` field) |
| `\trace` | Trace functional on the typed positive cone; `A ⪯ B ⟹ tr A ≤ tr B` | `\trace` (declared in `paper_macros.tex` as `\DeclareMathOperator{\trace}{tr}` to avoid clobbering local `\tr` in pgf/tikz) | `DualityConfinement.AntiInvariantLedger` (`tr` field) |
| `⪯` | Loewner-style partial order on the typed positive cone | `\preceq` (standard) | `DualityConfinement.AntiInvariantLedger` (`preceq` field) |
| `\dist(x, \Fix(J))` | Distance from `x` to the fixed locus | `\dist` | (paper-side; abstract Scale in Lean) |
| `m(\varepsilon)` | Modulus function for quantitative separation | `m(\varepsilon)` inline | `DualityConfinement.Separation` (`modulus` field) |
| `K^-` | Carrier-side anti-invariant currency | `\Kminus` | `DualityConfinement.Domination` (used in `CompletedDominationBridge.K_minus`) |
| `B_n` | Domination-record sequence (`A_X ⪯ B_n`) | inline `B_n` | `DualityConfinement.MasterTheorem` (parameter of `masterTheorem`) |
| `E` | Bridge defect operator (`A_X ⪯ K^- + E` with `E ⪰ 0`) | inline `E` | `DualityConfinement.Domination` (`CompletedDominationBridge.E`) |
| `E_{\mathrm{br},n}`, `E_{\mathrm{src},n}` | Bridge / source defects in the defected-budget record | inline | `DualityConfinement.DefectedBudget` (implicit in the defected-budget statement) |
| `\iota_n`, `T_n` | Inclusion / transport and tail operator for the exhaustive moving ledger | inline `\iota_n`, `T_n` | `DualityConfinement.ExhaustiveSqueeze` (`iota_n`, `T_n` fields) |
| `\Gamma_{\mathrm{SDTC}}` | Self-Dual Trace Confinement recognition source (Paper 1's named structural law) | `\GamSDTC` | (paper-side only; the RH-specialized `\Gamma_{\mathrm{SDTC\text{-}Selberg}}` is encoded as a typed structure carrier in Paper 2's `RH.RHConditional.GammaSdtcSelberg`) |

### Named-concept terms (NOT symbols, but reserved)

- **Self-Dual Trace Confinement (SDTC)** — the named structural law
  of Paper 1. Body prose says "SDTC" or "Trace-Fixity"
  interchangeably; do not invent alternate names.
- **Duality-confinement membrane theorem** — the master theorem
  (Paper 1 `sec:master_theorem`). Body prose may also refer to it
  as "the master theorem" or "the duality-confinement master
  theorem"; do not call it "the SDTC theorem" (per
  `claim-revision-register.md` R1).
- **Typed positive cone** — the mathlib-free abstraction over
  trace-class positive operators used in the Lean encoding.
- **Trace identity** — the relation `tr A_X = ∫ ‖ψ_-‖² dμ`,
  encoded as a definitional unfolding in the typed cone.
- **Douglas factorization** — refer to as "the classical Douglas
  factorization" or "Douglas's theorem"; the typed-cone encoding
  bundles it into a typed `DouglasData` carrier (see
  `claim-revision-register.md` R2).

## Local to RH (Paper 2) axis

### Reserved symbols

| Symbol | Meaning | LaTeX macro | Lean module |
| --- | --- | --- | --- |
| `s` | Generic complex variable in the critical-strip context; typed `Complex R` over a typed coordinate model | inline `s` | `RH.Involution` (`Complex` record) |
| `\bar{s}` | Complex conjugate of `s` | `\bar{s}` (LaTeX standard) | `RH.Involution` (`Complex.conj`) |
| `J_L(s) = 1 - \bar{s}` | Functional-equation involution on `Complex R`; involutive (`J_L²(s) = s`); fixed locus `{s : Re(s) = 1/2}` | `\JL` | `RH.Involution` (`feInvolution`) |
| `\Fix(J_L) = \{s : \mathrm{Re}(s) = 1/2\}` | Critical line | `\Fix(\JL)` | (paper-side only; Lean records membership via `J_L s = s`) |
| `\psi_-(s) = \mathrm{Re}(s) - 1/2` | Separating anti-invariant readout for RH; `\psi_-(J_L s) = -\psi_-(s)`; `\psi_-(s) = 0 ⟺ s ∈ \Fix(J_L)` | `\psimRH` (or reuse `\psim` from DC with specialization in body prose) | `RH.Involution` (`psiMinusRh`) |
| `\Lambda_\zeta(s) = \pi^{-s/2} \Gamma(s/2) \zeta(s)` | Completed Riemann zeta (opaque; only its zero ledger is used in the mechanization) | inline `\Lambda_\zeta(s)` | `RH.ZeroLedger` (`Lambda_zeta` field) |
| `Z_\zeta^{\mathrm{nt}}` | Nontrivial zero ledger of `\Lambda_\zeta` in the critical strip; typed multiset with positive integer multiplicities `m_\rho > 0`; measure `\mu_L(\{\rho\}) = m_\rho` | `\Znt` | `RH.ZeroLedger` (`NontrivialZeroLedger`) |
| `\rho` | A nontrivial zero (element of `Z_\zeta^{\mathrm{nt}}`) | inline `\rho` | `RH.ZeroLedger` (`rho` field) |
| `m_\rho` | Multiplicity of `\rho` (positive integer) | inline `m_\rho` | `RH.ZeroLedger` (`m_rho` field) |
| `A_Z(\zeta) = \sum_{\rho \in Z_\zeta^{\mathrm{nt}}} m_\rho \cdot |\mathrm{Re}(\rho) - 1/2|^2` | Anti-invariant zero ledger; positive real scalar; `A_Z(\zeta) = 0 ⟺` RH on the typed ledger | `\AZ` | `RH.AntiInvariantZeroLedger` (`A_Z` field) |
| `\mathrm{Sel}^!_{\zeta,\mathrm{tr}}` | Saturated completed Selberg trace closure (typed shell record bundling 13 fields: `H_L, I_tr, EQ_tr, EM_zero, Q_L, M_L, π_L, J_L, Λ_L, Z_nt, A_Z, Vis_L, Audit_L`) | `\Sel` | `RH.SatSelShell` (`SatSelShell`) |
| `I_{\mathrm{tr}}` | Lawful trace instrument | `\Itr` | `RH.SatSelShell` (`I_tr` field) |
| `\Gamma_{\mathrm{SDTC\text{-}Selberg}}` | Recognition source: the Selberg-class instance of SDTC; structural content of formed-layer closure on `Sel^!_{ζ,tr}`; NOT a Lean axiom, encoded as typed structure carrier `GammaSdtcSelberg` declared inline in `RHConditional.lean` | `\GamSDTCSelberg` | `RH.RHConditional` (`GammaSdtcSelberg`) |

### Named-concept terms (NOT symbols, but reserved)

- **Translation theorem T** — the central construction-grade
  theorem `A_Z(ζ) = 0 ⟺ RH`. Body prose refers to it as
  "Theorem T" or "the translation theorem".
- **Conditional landing chain** — the three-step direct chain
  `Γ_{SDTC-Selberg} → A_Z(ζ) = 0 → RH` realized by the
  `rhConditional` theorem.
- **Recognition source** — the named structural hypothesis
  `Γ_{SDTC-Selberg}`. Body prose says "recognition source" or
  "structural recognition content"; do not say "axiom".
- **Saturated trace closure** — the typed shell
  `\mathrm{Sel}^!_{\zeta,\mathrm{tr}}`. Body prose may say "the
  saturated Selberg trace closure" or "the saturated trace shell".
- **BirdInt judgment** — the Foundations-III typed sequent shape
  `Γ; T; I ⊢ φ : status`. Used in `sec:landing_chain` to render
  the conditional theorem in framework vocabulary; introduced via
  `paper/notes/audience-translation.md` on first use.
- **Six no-smuggling gates + Gate 7** — the seven-gate audit
  discipline. Body prose says "the six no-smuggling gates plus
  Gate 7" or "the seven-gate audit". Detail in `app:formalization`.
- **Three-option derivation sweep** — the cascade's documented
  attempt to derive `Γ_{SDTC-Selberg}` from framework primitives
  (three options: framework-primitive, SAU non-descent,
  V-Differential elevation), all confirming the recognition-source
  status. Body prose says "the three-option derivation sweep" with
  cascade-step citation to steps 451–453.

### RH paper - specific encoding-disclosure notes (carry into body)

These notes from `anti_loc/extracted_math/audit_summary.md` apply
specifically to Paper 2:

- **§A3 real-part type abstraction**: the real-part coordinate is
  parameterized by a typed ordered-field carrier (`RealCoordinate`)
  with `half`, `oneMinus`, `sub`, `neg` operations and axioms
  `oneMinus_involutive`, `oneMinus_fixed_iff`,
  `sub_half_eq_zero_iff`, `sub_oneMinus_half`. Body prose around
  `def:rh:fe-involution` and `def:rh:nontrivial-zero-ledger` must
  disclose that the Lean statement abstracts the real-part type;
  the identification with actual ℝ-valued real parts of nontrivial
  zeros of `ζ` is by construction-parameter assignment.
- **Inline `GammaSdtcSelberg` placement**: per
  `lean/codex_kickoff.md` §12, the recognition-source carrier was
  declared inline in `RHConditional.lean` (the conditional theorem
  is its only consumer; the type lives next to its only consumer).
  Body prose around `sec:recognition_source` and
  `app:formalization` must use this canonical placement (no
  separate `RecognitionSource.lean` module exists).

## Cross-paper notation consistency

The following symbols carry IDENTICAL meaning in both papers and
must render identically across the two PDFs (per Phase I.F
cross-paper coherence pass):

- `J` (involution; in Paper 2 specialized to `J_L`)
- `\Fix(J)` (fixed locus)
- `ψ`, `ψ_-` (readouts; in Paper 2 specialized to `ψ_-(s) = Re(s) - 1/2`)
- `A_X` (Paper 1 generic) / `A_Z(\zeta)` (Paper 2 specialized)
- `⪯`, `tr` (typed-cone primitives)
- `B_n`, `E`, `\iota_n`, `T_n` (apparatus operators)
- `\Gamma` (recognition source; Paper 1 `\Gamma_{\mathrm{SDTC}}`,
  Paper 2 `\Gamma_{\mathrm{SDTC\text{-}Selberg}}`)

The macro definitions in
`paper/duality_confinement/includes/paper_macros.tex` and
`paper/rh/includes/paper_macros.tex` MUST agree on the rendering of
these shared symbols. Per-axis differences are limited to the
specialization names (e.g. `\GamSDTC` in Paper 1, `\GamSDTCSelberg`
in Paper 2).
