# Step 44: Membrane Type Promotion Theorem

This step proves when a weaker membrane type can be promoted to an intrinsic membrane.

The core object is a response presentation

\[
J:Y\to Z
\]

from the native response space to a section stack, bundle response space, or protocol stack. The typed currency is

\[
K_Z=J K_Y J^*,
\qquad K_Y=LC^\dagger L^*.
\]

## Exact promotion theorem

If there is a reconstruction map

\[
R:Z\to Y,
\qquad RJ=I_Y,
\]

and the typed membrane satisfies

\[
K_Z\preceq \Theta_Z,
\]

then the intrinsic membrane satisfies

\[
K_Y\preceq R\Theta_ZR^*.
\]

So a sectioned, bundle, or protocol membrane promotes only through a faithful response bridge and a full block budget.

## Defective promotion theorem

If reconstruction has residual readout

\[
E=L-RJL,
\qquad K_E=EC^\dagger E^*,
\]

and

\[
K_E\preceq E_0,
\]

then for every \(t>0\),

\[
K_Y\preceq (1+t)R\Theta_ZR^*+(1+t^{-1})E_0.
\]

Thus bridge defects must be paid explicitly.

## Sectioned promotion

Section-local diagonal budgets do not promote. A sectioned membrane needs the full block currency

\[
K^{\mathrm{sec}}=[K^{ab}]_{a,b}
\]

and a faithful reconstruction of the native response from the section stack.

## Bundle promotion

Fiberwise finite budgets do not promote. A bundle/fiber membrane needs a uniform or direct-integral budget and a gluing/reconstruction map.

## Protocol promotion

Protocol-local route budgets do not promote. A protocol-indexed membrane needs the stacked protocol block matrix, mixed-route readout agreement, and a reconstruction/descent map.

## Status interpretation

A weaker membrane can have three outcomes:

1. `accepted_promotion`: faithful bridge + full block budget.
2. `defective_promotion`: residual is paid by explicit defect budget.
3. `local_only_or_nonclaim`: no faithful bridge or no block budget.

The last status is not failure of the weaker membrane; it is failure of the stronger intrinsic claim.
