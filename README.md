# Six Birds Duality Confinement

This repository contains the public support surface for two papers in
the Six Birds series: modular LaTeX sources, tracked flattened
manuscripts, Lean 4 mechanization, inventories, manifests, validators,
and vendored Foundations dependencies.

## Papers

- **Self-Dual Trace Confinement: A Six Birds Structural Law for Formed
  Closures Under Involutive Self-Duality**:
  DOI: [10.5281/zenodo.20713517](https://doi.org/10.5281/zenodo.20713517)
- **Riemann Hypothesis via Self-Dual Trace Confinement: A Conditional
  Closure**:
  DOI: [10.5281/zenodo.20713535](https://doi.org/10.5281/zenodo.20713535)

## What This Repository Provides

- Modular LaTeX paper sources under
  `paper/duality_confinement/` and `paper/rh/`.
- Tracked flattened manuscript sources at the repository root.
- Shared bibliography, notation, and paper-support records under
  `paper/`.
- Lean 4 mechanization under `lean/`, with separate Duality
  Confinement and RH axes.
- Paper inventories, traceability queues, and validation manifests under
  `formalization/` and `lean/manifests/`.
- Deterministic validation and build-support scripts under `scripts/`.
- Vendored Six Birds Foundations dependencies under
  `vendor/foundations/`.

Internal research archives, local process notes, and draft-preparation
artifacts are ignored locally and are not part of this public
support surface.

## Build

Build both modular paper PDFs:

```bash
make paper-build
```

Run the paper preflight gate:

```bash
make paper-preflight
```

Build the Lean project:

```bash
cd lean
lake build
```

Run the Lean and inventory validators without rebuilding Lean:

```bash
python3 scripts/check_lean.py --skip-build
```

## Repository Layout

- `paper/duality_confinement/` and `paper/rh/` - modular manuscript
  sources used to build the two paper PDFs.
- Repository-root `Tsiokos_2026_*.tex` files - tracked flattened
  manuscript sources.
- `paper/references.bib` and `paper/notation_and_terminology.md` -
  shared bibliography and notation support.
- `lean/` - Lean 4 project and validation manifests.
- `formalization/inventory/` - paper inventories, boundaries, and
  imported-foundations cross-walks.
- `formalization/traceability/` - per-axis statement queues.
- `scripts/` - deterministic validation and build-support scripts.
- `vendor/foundations/` - vendored upstream foundations required by the
  local Lake project.

## Notes

- The LaTeX toolchain requires `latexmk` and a TeX distribution with the
  packages used by the manuscripts.
- The Lean toolchain is pinned in `lean/lean-toolchain`.
- Third-party vendored code remains under its upstream license terms.
