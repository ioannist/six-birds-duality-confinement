/-!
Umbrella module for the RH paper axis (Paper 2).

Per-section modules are added under `SixBirdsDualityConfinement/RH/`
as paper sections are mechanized from the queue at
`formalization/traceability/queue_rh.csv`. Imports below are kept in
document order; codex appends a new line per accepted subsection.

Out-of-scope-for-Lean items (e.g. structural recognition sources that
are not Lean-derivable per the proposal) are encoded as typed structure
carriers in dedicated modules; downstream theorems take values of those
structures as explicit hypothesis parameters. The forbidden-tokens rule
bans `axiom`/`opaque`/`constant`/`sorry`/`admit` anywhere in the source
tree.
-/

-- Per-section imports go here as Phase G dispatches accept them.
