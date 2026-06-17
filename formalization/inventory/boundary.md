# Formalization Boundary

This inventory defines the source contract for the
duality-confinement + RH Lean 4 mechanization. The authoritative target
corpus is the set of theorem-like environments in:

- `paper/duality_confinement/sections/*.tex` (duality-confinement axis;
  targets defined in
  `anti_loc/paper_proposal_self_dual_trace_confinement.md`)
- `paper/rh/sections/*.tex` (RH axis; targets defined in
  `anti_loc/paper_proposal_rh_via_sdtc_selberg.md`)

There are no external dependency papers in this repository.
Foundations I/II/III declarations are not source items; they are tracked
separately via `imported_foundations.yml` and the vendored trees under
`vendor/foundations/`.

Out-of-scope-for-Lean items (e.g. any structural recognition sources
identified in the proposals) are recorded in the per-axis inventories
with `intended_status = out_of_scope_recognition_source`; they do not
appear in Lean.
