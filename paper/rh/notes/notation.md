# Notation Workspace: RH closure (Paper 2)

Status: Phase 9 produced 2026-05-23 (paper-writing prep arc closed).

Purpose: paper-local notation choices not yet promoted to the
shared governance file `paper/notation_and_terminology.md`. As
choices stabilize during drafting, they are promoted up.

This file is a workspace; the binding authority is
`paper/notation_and_terminology.md` + the per-paper
`paper/rh/includes/paper_macros.tex`. The macros in
`paper_macros.tex` were finalized during Phase 1 (notation and
macro consolidation); this workspace is the staging area for any
new symbol that emerges during drafting and may need promotion.

## Paper 2 notation roster (initial set; finalized in Phase 1)

| Symbol | Meaning | LaTeX macro (in paper_macros.tex) | First-use section |
| --- | --- | --- | --- |
| `J_L(s) = 1 - \bar{s}` | Functional-equation involution on `ℂ` | `\JL` | `sec:involution_and_ledger` |
| `Fix(J_L) = {Re(s) = 1/2}` | Critical line as fixed locus | `\Fix{\JL}` | `sec:involution_and_ledger` |
| `\psi_-(s) = Re(s) - 1/2` | Separating anti-invariant readout for RH | `\psimRH` | `sec:involution_and_ledger` |
| `\Lambda_\zeta(s)` | Completed `\zeta`-function | `\Lzeta` | `sec:involution_and_ledger`, `sec:sat_sel_shell` |
| `Z_\zeta^{nt}` | Typed multiset of nontrivial zeros of `\zeta` with multiplicities `m_\rho > 0` | `\Znt` | `sec:involution_and_ledger` |
| `A_Z(\zeta) = \sum_\rho m_\rho |Re(\rho) - 1/2|^2` | Anti-invariant zero ledger | `\AZ` | `sec:involution_and_ledger`, `sec:translation_theorem` |
| `Sel^!_{\zeta,tr}` | Saturated completed Selberg trace closure | `\Sel` | `sec:sat_sel_shell` and throughout |
| `I_tr` | Lawful trace instrument on `\Sel` | `\Itr` | `sec:sat_sel_shell` |
| `\Gamma_{SDTC-Selberg}` | Recognition source (Selberg-class instance of SDTC) | `\GamSDTCSelberg` | `sec:recognition_source`, `sec:landing_chain`, `sec:scope_and_nonclaims` |
| `[1]` | Bibtex pointer to Paper 1 (`TsiokosSDTC2026`) | `\SiblingDC` | throughout (every cross-paper citation to Paper 1) |
| `P_-`, `\psi_-`, `A_X`, `K^-`, `J_iso`, `\IOL`, `\Gamma_{SDTC}` | Cross-paper macros (Paper 1 vocabulary; available for verbatim master-theorem reproduction in `sec:landing_chain`) | `\Pminus`, `\psim`, `\AX`, `\Kminus`, `\Jiso`, `\IOL`, `\GamSDTC` | `sec:landing_chain` (verbatim master-theorem statement) |

## Reserved symbols (RH paper)

These symbols carry the meanings above and must NOT be repurposed
elsewhere in the paper:

- `J_L` (the functional-equation involution; not a general
  involution; never repurposed)
- `\psi_-` (anti-invariant readout; never repurposed; appears in
  two contexts — the RH-specific `psi_-(s) = Re(s) - 1/2` and the
  Paper-1 abstract `psi_-` — the macros `\psimRH` and `\psim`
  disambiguate)
- `Z_\zeta^{nt}` (typed multiset of nontrivial zeros; never
  repurposed)
- `A_Z(\zeta)` (anti-invariant zero ledger; the parenthesized
  `(\zeta)` is part of the symbol)
- `Sel^!_{\zeta,tr}` (typed shell; always with the full subscript
  modifier; never abbreviated to `Sel` in body prose)
- `I_tr` (lawful trace instrument; never repurposed for a different
  trace operator)
- `\Gamma_{SDTC-Selberg}` (recognition source; the `-Selberg`
  qualifier is part of the symbol; never abbreviated to
  `\Gamma_{SDTC}` in Paper 2 body prose — the un-qualified
  `\Gamma_{SDTC}` is Paper 1's vocabulary for the abstract
  structural law)
- `[1]` (Paper 1 citation; the bracketed numeric is the visible
  Tsiokos bibkey)

## Macro promotion checklist

When promoting a symbol from this workspace to
`paper/rh/includes/paper_macros.tex`:

1. Add `\newcommand{\macroname}{...}` to `paper_macros.tex`.
2. Add the symbol to `paper/notation_and_terminology.md` "Local to
   RH axis" section.
3. Mark this row as "promoted" in the table above.

All initial-set macros listed above are already promoted (Phase 1
closure 2026-05-23). New symbols that emerge during drafting are
added to this workspace first; promotion happens via a deliberate
notation-update dispatch.

## Cross-paper notation consistency notes

The following shared symbols must render identically in Paper 1
and Paper 2 (per the cross-paper coherence pass at Phase I.F of
the writing-plan):

| Shared symbol | DC paper macro | RH paper macro | Render |
| --- | --- | --- | --- |
| Fixed-locus operator | `\Fix` | `\Fix` | `Fix(J)` |
| Anti-invariant projector | `\Pminus` | `\Pminus` (cross-paper) | `P_-` |
| Anti-invariant readout (abstract) | `\psim` | `\psim` (cross-paper) | `\psi_-` |
| Anti-invariant readout (RH-specific) | (not used) | `\psimRH` | `\psi_-(s) = Re(s) - 1/2` |
| Anti-invariant ledger (abstract) | `\AX` | `\AX` (cross-paper) | `A_X` |
| Anti-invariant zero ledger (RH-specific) | (not used) | `\AZ` | `A_Z(\zeta)` |
| Loewner order | `\preceq` (standard) | `\preceq` (standard) | `\preceq` |
| Trace functional | `\trace` (declared in `paper_macros.tex`) | `\trace` (declared in `paper_macros.tex`) | `tr` |
| Carrier-side anti-invariant currency | `\Kminus` | `\Kminus` (cross-paper) | `K^-` |
| Isometric involution | `\Jiso` | `\Jiso` (cross-paper) | `J_{iso}` |
| Ledger tuple shorthand | `\IOL` | `\IOL` (cross-paper) | `\hat{\mathfrak{X}}` |
| SDTC recognition source (abstract) | `\GamSDTC` | `\GamSDTC` (cross-paper) | `\Gamma_{SDTC}` |
| SDTC recognition source (Selberg-class) | (not used; Paper 2 only) | `\GamSDTCSelberg` | `\Gamma_{SDTC-Selberg}` |

Drift in shared-symbol rendering is a Phase I.F defect; route the
fix through the affected paper's codex thread per
`paper/writing-plan.md`.
