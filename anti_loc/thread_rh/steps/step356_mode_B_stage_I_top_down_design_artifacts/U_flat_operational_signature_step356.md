# Step 356 U^flat Operational Signature

## Frozen Audit Target

Target `T` is frozen as an audit target, not a carrier axiom:

`T`: a kernel-preserving Hecke-to-Burnol/Sonine zeta transfer respecting
complex test-function pairings.

The carrier does not contain a primitive transfer `tau`, nor a primitive
predicate saying that such a transfer exists.

## Finite State Set

`Sigma = {a, b, c, d, e}`.

- `a`: Hecke evaluator atom.
- `b`: zeta residual atom.
- `c`: comparison atom carrying `(lambda_mag, lambda_phase)`.
- `d`: operator-compatibility audit atom.
- `e`: non-descending defect witness.

`e` is the promoted non-descending witness.

## Lens

The host lens `q` is partial:

- `q(a[data]) = complex Hecke evaluator pairing H_chi,k`.
- `q(b[data]) = complex zeta residual Z_rho,k`.
- `q(c[data]) = (lambda_mag, lambda_phase)`.
- `q(d[data]) = lambda_total = (lambda_mag, lambda_phase, lambda_operator_status)`.
- `q(e) = undefined / blocked`.

Thus the lens emits a residual ledger, not a target closure theorem.

## Equivalence

Two expressions are equivalent when:

1. they have the same state label,
2. they have identical bound indices `(chi,k,rho)` where applicable,
3. their emitted ledger entries agree under `q`,
4. they have the same admissibility status.

## Rewrite Rules

Finite rewrite/update rules:

- `R_H_load: a -> a[data_H]`.
- `R_Z_load: b -> b[data_Z]`.
- `R_compare: (a[data_H], b[data_Z]) -> c[lambda_mag, lambda_phase]`.
- `R_operator_audit: c -> d[lambda_mag, lambda_phase, operator_status]`.
- `R_block: d -> e` when any residual is nonzero or operator status is missing.
- `R_admit: d -> d_admissible` only when all residuals are zero and operator status is certified.

## Defect Ledger

`Lambda(U) = (lambda_mag, lambda_phase, lambda_operator_status)`.

The ledger is a diagnostic object.  `Lambda = 0` is not postulated; it must be
computed by rewrites and independently audited.

## Admissible Expressions

Admissible:

- `a[data_H]` for scoped Hecke evaluator reproduction.
- `b[data_Z]` for scoped zeta residual reproduction.
- `d[Lambda]` as a residual audit output.

Blocked:

- `e`.
- Any expression asking for `tau` directly.
- Any expression asserting `Lambda = 0` without a certified operator audit.

## Non-Descent Witness

`u_NC = e`.

The state `e` does not descend through `q`, and represents the finite
non-descending obstruction.

## Stage I Boundary

The signature is finite and operational.  It does not use categories, topoi,
type theory, model theory, operator algebras, algebraic geometry, or measure
spaces as the primary framing.
