# Notation Workspace: Duality Confinement (Paper 1)

Status: Phase 9 produced 2026-05-23 (paper-writing prep arc closed).

Purpose: paper-local notation choices not yet promoted to the shared
governance file `paper/notation_and_terminology.md`. As choices
stabilize during drafting, they are promoted up.

This file is a workspace; the binding authority is
`paper/notation_and_terminology.md` + the per-paper
`paper/duality_confinement/includes/paper_macros.tex`. The macros
in `paper_macros.tex` were finalized during Phase 1 (notation and
macro consolidation); this workspace is the staging area for any
new symbol that emerges during drafting and may need promotion.

## Paper 1 notation roster (initial set; finalized in Phase 1)

| Symbol | Meaning | LaTeX macro (to define in paper_macros.tex) | First-use section |
| --- | --- | --- | --- |
| `(X, J, μ, ψ, Y, J_iso)` | Involutive object ledger tuple | `\IOL` for the tuple shorthand; individual letters used inline | `sec:involutive_ledger` |
| `Fix(J)` | Fixed locus of `J` | `\Fix` | `sec:involutive_ledger` |
| `P_-` | Anti-invariant projector `(I - J_iso) / 2` | `\Pminus` | `sec:anti_invariant_ledger` |
| `ψ_-` | Anti-invariant readout `P_- ψ` | `\psiminus` | `sec:anti_invariant_ledger` |
| `A_X` | Anti-invariant object ledger `∫ ψ_- ψ_-^* dμ` | `\AX` | `sec:anti_invariant_ledger` |
| `tr` | Trace functional on the typed positive cone | `\tr` (already standard) | `sec:anti_invariant_ledger` |
| `⪯` | Loewner-style order on the typed positive cone | `\preceq` (already standard) | `sec:anti_invariant_ledger` |
| `dist(x, Fix(J))` | Distance from `x` to the fixed locus | `\dist` | `sec:anti_invariant_ledger`, `sec:direct_confinement` |
| `m(ε)` | Modulus function for quantitative separation | `m(\varepsilon)` inline (no macro) | `sec:anti_invariant_ledger`, `sec:direct_confinement` |
| `K^-` | Carrier-side anti-invariant currency | `\Kminus` | `sec:domination` |
| `E_{br,n}`, `E_{src,n}` | Bridge / source defects | inline (no macro) | `sec:exhaustive_squeeze_and_budgets` |
| `B_n` | Domination-record sequence | inline (no macro) | `sec:domination`, `sec:master_theorem`, `sec:exhaustive_squeeze_and_budgets` |
| `ι_n` | Inclusion / transport for exhaustive moving ledger | `\iota` (already standard) | `sec:exhaustive_squeeze_and_budgets` |
| `T_n` | Tail operator | `T_n` inline | `sec:exhaustive_squeeze_and_budgets` |
| `Λ_n^{-1} Θ_0^-` | Collapse-ladder normalization | inline | `sec:exhaustive_squeeze_and_budgets` |
| `Γ_{SDTC}` | Self-Dual Trace Confinement recognition source | `\GamSDTC` | `sec:master_theorem`, `sec:scope`, `sec:discussion` |
| SDTC; Trace-Fixity | Named structural law | (no macro; spelled out) | `sec:intro`, `sec:master_theorem`, `sec:scope`, `sec:discussion`, `sec:conclusion` |

## Reserved symbols (DC paper)

These symbols carry the meanings above and must NOT be repurposed
elsewhere in the paper:
- `J` (the ledger involution; not the imaginary unit)
- `J_iso` (the isometric involution on the response space)
- `ψ`, `ψ_-` (readouts; never repurposed for psi-functions in number
  theory)
- `A_X` (anti-invariant ledger; never repurposed for any other "A")
- `Fix(J)` (fixed locus)
- `tr`, `⪯` (typed-cone primitives; never repurposed for other trace
  or order notions in informal asides)

## Macro promotion checklist

When promoting a symbol from this workspace to
`paper/duality_confinement/includes/paper_macros.tex`:
1. Add `\newcommand{\macroname}{...}` to paper_macros.tex.
2. Add the symbol to `paper/notation_and_terminology.md` "Local to
   DC axis" section.
3. Mark this row as "promoted" in the table above.

Initial Phase 1 promotion set (already in
`paper/duality_confinement/includes/paper_macros.tex`): `\Fix`,
`\Pminus`, `\psim`, `\AX`, `\Jiso`, `\Kminus`, `\IOL`, `\GamSDTC`,
plus the cross-paper macros `\SiblingRH` (Paper 2 forward-reference
placeholder), `\preceqDC`, `\trDC`. The others remain inline.

New symbols that emerge during drafting are added to this workspace
first; promotion to `paper_macros.tex` (and to
`paper/notation_and_terminology.md`'s local-to-DC table) happens via
a deliberate notation-update dispatch.
