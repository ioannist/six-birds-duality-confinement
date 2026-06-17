# Duality Confinement + RH — Lean Project

This directory holds the Lean 4 mechanization for the
six-birds-duality-confinement project. Two paper axes are tracked
under `SixBirdsDualityConfinement/DualityConfinement/` and
`SixBirdsDualityConfinement/RH/`. The alignment trio
(`ImportedFoundations`, `FoundationsICompat`, `Terminology`) sits at
the top of the namespace and pulls in the vendored Foundations I/II/III.

## Toolchain

Pinned to `leanprover/lean4:v4.28.0` in `lean-toolchain`. Matches the
three vendored foundations under `../vendor/foundations/`. No version
drift across the project.

## No mathlib

This Lean project is deliberately mathlib-free, matching the
foundations and the sibling projects in the series. Any
finite-dimensional linear algebra or analytic number-theory machinery
used by either axis is defined locally as mechanization proceeds.
See `../paper/notation_and_terminology.md` for the governance contract.

## Build

```bash
cd lean
lake build
```

This builds the umbrella `SixBirdsDualityConfinement`, which
transitively builds the alignment trio and the two per-axis umbrellas
(`DualityConfinement.lean`, `RH.lean`) together with the per-section
modules imported by those umbrellas.

## Full check

From the repo root:

```bash
python scripts/check_lean.py
```

Runs the structural prechecks (required files, forbidden tokens,
external-ref grep), the Phase A python validator chain, and
`lake build`. Use `--skip-build` if the Lean toolchain is not
available, or `--skip-prechecks` to run only the lake build.

## Forbidden Lean tokens

The validator rejects any occurrence of `sorry`, `admit`, `axiom`,
`opaque`, or `constant` in `SixBirdsDualityConfinement/*`. Out-of-scope
obligations (e.g. structural recognition sources that are not
Lean-derivable) live in the per-axis inventories under
`../formalization/inventory/` with `intended_status = out_of_scope_*`;
they do not appear in Lean as axioms.

## Pointers

- Cross-walk to canonical Foundations names:
  `../formalization/inventory/imported_foundations.yml`
- Generated drift canary:
  `SixBirdsDualityConfinement/ImportedFoundations.lean`
  (regenerate with `scripts/generate_imported_foundations.py`)
- Notation/terminology governance: `../paper/notation_and_terminology.md`
- Per-axis mechanization queues:
  `../formalization/traceability/queue_{duality_confinement,rh}.csv`
