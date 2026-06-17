# RH closure — figures/

Status: empty at prep-arc close (2026-05-23).

The Phase 4 plan in `paper/rh/notes/figure-table-plan.md`
enumerates the figures this paper will need (e.g.
`fig:landing-chain-diagram`,
`fig:sat-sel-shell-schematic`). Concrete figure `.tex` files are
created during the drafting arc, one per dispatch, per
`paper/rh/notes/drafting-plan.md`. The `generated/` subdirectory
will host any TikZ-rendered output if the build pipeline ever
caches them.

This README is the placeholder so the directory survives git and
`scripts/paper_lint.sh` (which requires `figures/` to exist) passes.
