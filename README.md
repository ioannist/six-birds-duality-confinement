# Six Birds Duality Confinement

This repository contains the public support surface for two papers in
the Six Birds series: modular LaTeX sources, tracked flattened
manuscript sources, Lean 4 mechanization, formalization inventories,
validation manifests, scripts, and vendored Foundations dependencies.

## Papers

- **Self-Dual Trace Confinement: A Six Birds Structural Law for Formed
  Closures Under Involutive Self-Duality**
  DOI: [10.5281/zenodo.20713517](https://doi.org/10.5281/zenodo.20713517)
- **Riemann Hypothesis via Self-Dual Trace Confinement: A Conditional
  Closure**
  DOI: [10.5281/zenodo.20713535](https://doi.org/10.5281/zenodo.20713535)

## What This Repository Provides

- Modular LaTeX sources for the Duality Confinement and RH papers under
  `paper/duality_confinement/` and `paper/rh/`.
- Tracked flattened manuscript sources at the repository root for
  submission and archive workflows.
- Shared bibliography, notation, and paper-support records under
  `paper/`.
- Lean 4 mechanization under `lean/`, with separate Duality
  Confinement and RH axes.
- Formalization inventories and traceability queues under
  `formalization/`.
- Validation and build-support scripts under `scripts/`.
- Vendored Six Birds Foundations dependencies under
  `vendor/foundations/`.

Internal research archives, local process notes, and draft-preparation
artifacts are ignored locally and are not part of the intended public
support surface.

## Build

Build both paper PDFs:

```bash
make paper-build
```

Run the full paper preflight gate:

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

- `paper/duality_confinement/` - modular source for the Self-Dual Trace
  Confinement paper.
- `paper/rh/` - modular source for the conditional RH paper.
- `paper/references.bib` - shared bibliography.
- `paper/notation_and_terminology.md` - shared notation and terminology
  support.
- `lean/` - Lean 4 project and validation manifests.
- `formalization/inventory/` - paper inventories, boundaries, and
  imported-foundations cross-walks.
- `formalization/traceability/` - per-axis statement queues.
- `scripts/` - deterministic validators and build-support scripts.
- `vendor/foundations/` - vendored upstream Foundations tracks required
  by the local Lake project.

## Notes

- The LaTeX toolchain requires `latexmk` and a TeX distribution with the
  packages used by the manuscripts.
- The Lean toolchain is pinned in `lean/lean-toolchain`.
- Vendored third-party or upstream project files retain their upstream
  license terms.
