# Notation and Terminology — Duality Confinement + RH Papers

Stub. Populate during Phase A (math extraction & consolidation), keep
in sync with the alignment trio in `lean/SixBirdsDualityConfinement/`
(`ImportedFoundations.lean`, `FoundationsICompat.lean`,
`Terminology.lean`).

This is the **single source of truth** for paper-facing names. Every
symbol used in either paper must be either:

1. Inherited from a vendored Foundations layer (F1/F2/F3) — listed in
   the "Inherited" section below with its canonical name and the
   alias used in the papers, or
2. Introduced locally in this repo — declared in the "Local" section
   below with definition, role, and the Lean module it lives in.

No silent vocabulary. If a new term is added in either paper, it must
also be added here and in `Terminology.lean` in the same change.

## Governance

- `Terminology.lean` declares the Lean side of the surface.
- This file declares the paper side.
- Both papers `\input` `paper/<axis>/includes/paper_macros.tex`, which
  defines the LaTeX commands rendering the symbols.

## Inherited from Foundations

TODO: cross-walk table — Foundations layer | canonical decl | paper alias | first use.

## Local to this repo

### Duality-confinement axis

TODO.

### RH axis

TODO.
