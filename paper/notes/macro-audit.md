# Macro Audit

Status: Phase 1 produced 2026-05-23.

Purpose: consolidated macro list with per-macro paper coverage.
Cross-checks that `paper/duality_confinement/includes/paper_macros.tex`
and `paper/rh/includes/paper_macros.tex` together cover every reserved
symbol declared in `paper/notation_and_terminology.md`, and that
shared macros render identically across both papers.

## Per-macro inventory

| Macro | DC paper | RH paper | Meaning | Reserved symbol? |
| --- | :-: | :-: | --- | :-: |
| `\Fix` | ✓ | ✓ | `\DeclareMathOperator{\Fix}{Fix}` — fixed locus of an involution | ✓ |
| `\Ran` | ✓ | ✓ | `\DeclareMathOperator{\Ran}{Ran}` — range of an operator | ✓ |
| `\dist` | ✓ | ✓ | `\DeclareMathOperator{\dist}{dist}` — distance function | ✓ |
| `\trace` | ✓ | ✓ | `\DeclareMathOperator{\trace}{tr}` — trace functional on the typed positive cone | ✓ |
| `\Real` | – | ✓ | `\DeclareMathOperator{\Real}{Re}` — real part (RH-specific use) | ✓ |
| `\Pminus` | ✓ | ✓ | Anti-invariant projector `P_- = (I_Y - J_{iso})/2` | ✓ |
| `\psim` | ✓ | ✓ | Anti-invariant readout `\psi_-` (RH-specific specialization in Paper 2) | ✓ |
| `\psimRH` | – | ✓ | Explicit RH-specialized anti-invariant readout `\psi_-(s) = Re(s) - 1/2` | ✓ |
| `\AX` | ✓ | ✓ | Anti-invariant object ledger `A_X = ∫ ψ_- ψ_-^* dμ` (generic, Paper 1; reused in Paper 2 when discussing the master theorem) | ✓ |
| `\AZ` | – | ✓ | Anti-invariant zero ledger `A_Z(ζ) = Σ_ρ m_ρ \cdot |Re(ρ) - 1/2|^2` (RH-specific instance of `A_X`) | ✓ |
| `\Kminus` | ✓ | ✓ | Carrier-side anti-invariant currency `K^-` | ✓ |
| `\Jiso` | ✓ | ✓ | Linear isometric involution on the response space `Y` | ✓ |
| `\IOL` | ✓ | ✓ | Involutive object ledger tuple shorthand `\hat{\mathfrak{X}}` (used sparingly) | – |
| `\GamSDTC` | ✓ | ✓ | Self-Dual Trace Confinement recognition source (Paper 1's named structural law); Paper 2 references it when describing the source of its specialized `Γ_{SDTC-Selberg}` | ✓ |
| `\GamSDTCSelberg` | – | ✓ | Recognition source `Γ_{SDTC-Selberg}` (RH-specialized Selberg-class instance) | ✓ |
| `\JL` | – | ✓ | Functional-equation involution `J_L(s) = 1 - \bar{s}` | ✓ |
| `\Lzeta` | – | ✓ | Completed Riemann zeta `Λ_ζ(s)` (opaque) | ✓ |
| `\Znt` | – | ✓ | Nontrivial zero ledger `Z_ζ^{nt}` | ✓ |
| `\Sel` | – | ✓ | Saturated completed Selberg trace closure `Sel^!_{ζ,tr}` | ✓ |
| `\Itr` | – | ✓ | Lawful trace instrument `I_{tr}` | ✓ |
| `\SiblingRH` | ✓ | – | Cross-paper reference to Paper 2 (used in the two sanctioned forward-reference paragraphs in DC) | – |
| `\SiblingDC` | – | ✓ | Cross-paper reference to Paper 1 (substantive citation in RH) | – |

**Counts**: DC paper_macros.tex defines 11 reserved-symbol macros +
3 utility / cross-reference macros = 14 total. RH paper_macros.tex
defines 18 reserved-symbol macros + 2 utility / cross-reference
macros = 20 total. Shared macros (defined identically in both) =
11.

## Cross-paper consistency check

The following macros are defined IDENTICALLY in both papers'
`paper_macros.tex` (verified by string-comparison of the
`\newcommand` / `\DeclareMathOperator` lines):

- `\Fix`, `\Ran`, `\dist`, `\trace`
- `\Pminus`, `\psim`, `\AX`, `\Kminus`, `\Jiso`, `\IOL`
- `\GamSDTC`

Per `paper/notes/cross-paper-boundary.md` § "Shared notation":
the Phase I.F cross-paper coherence pass (post-drafting) verifies
that these macros render IDENTICALLY in the two PDFs.

RH-only macros (`\JL`, `\psimRH`, `\Lzeta`, `\Znt`, `\AZ`, `\Sel`,
`\Itr`, `\GamSDTCSelberg`, `\Real`) are specializations introduced
in Paper 2; they are NOT redefined in Paper 1.

DC-only macros (`\SiblingRH`) are used only in the two sanctioned
forward-reference paragraphs in DC; they are NOT used in RH (which
uses `\SiblingDC` for the reverse direction).

## Coverage gap audit

Every reserved symbol declared in
`paper/notation_and_terminology.md` has a corresponding macro in at
least one of the two `paper_macros.tex` files. No gaps.

Per-axis coverage:

- Paper 1 (DC) symbols: all covered by
  `paper/duality_confinement/includes/paper_macros.tex` plus the
  inline-only items documented in
  `paper/duality_confinement/notes/notation.md` § "Macro promotion
  checklist" (the inline items are `m(\varepsilon)`, `B_n`, `E`,
  `\iota_n`, `T_n`, `E_{br,n}`, `E_{src,n}`, `\Lambda_n^{-1} \Theta_0^-`
  — short enough that a macro adds no clarity).
- Paper 2 (RH) symbols: all covered.

## Macro promotion convention

When a new symbol is introduced during the drafting arc:
1. Add to `paper/notation_and_terminology.md` under the appropriate
   per-axis section.
2. Add `\newcommand{\macroname}{...}` to the corresponding paper's
   `paper_macros.tex`.
3. Update this `macro-audit.md` with the new row.
4. If the symbol is shared across both papers, add the macro to
   BOTH `paper_macros.tex` files with identical definitions.

This convention is binding on every drafting dispatch that
introduces new notation; see
`paper/duality_confinement/notes/drafting-plan.md` and
`paper/rh/notes/drafting-plan.md` (Phase 9 deliverables) for the
per-dispatch prompt template that names this convention.
