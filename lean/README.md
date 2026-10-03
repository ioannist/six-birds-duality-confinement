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

## Mathlib and classical zeros

The RH repair uses mathlib at the revision pinned in `lakefile.toml`.
`RH.ClassicalZeroLedger` defines all completed Riemann zeta zeros in
the open critical strip and proves the positive-sum translation
theorem over actual complex and real numbers.
`RH.ClassicalZeroCountable` proves those zeros form a countable subtype
by applying isolated zeros to an entire numerator of completed zeta.
This supplies exhaustive finite zero windows without an encodability
assumption from outside the repository. The generic DC modules
retain their typed positive-cone interface. The separate
`ClassicalZeroIdentification` input in `RHConditional` states the
shell-to-classical-zero bridge explicitly. `RH.ClassicalBareShell`
constructs that bridge for an exact completed-zeta zero carrier. Its
trace and audit fields are placeholders; no Selberg gamma source is
constructed there.
`RH.BareSourceConverse` checks the converse boundary: assuming RH, a
one-object zero-energy DC model inhabits the generic gamma record on
the bare shell. Together with the gamma-to-RH theorem, generic record
inhabitation on that shell is RH-equivalent. The constructed record is
not an independent Selberg trace source.

## Updated AOR and XI dependency

The `SixBirdsNeedles` Lake dependency resolves AOR and XI declarations from
the separately prepared `../../six-birds-needles/lean/` source tree.
This dependency is not vendored here. The required source snapshot contains
82 Lean files, identified by
`../formalization/inventory/needles_dependency.sha256`. The sibling's
base commit is recorded in that manifest, but 74 required files are
untracked there at the time of this snapshot. Cloning the base commit
alone does not provide the required dependency. Obtain the recorded
sources separately before building; from this repository's root, verify
their bytes with:

```bash
cd ../six-birds-needles/lean
sha256sum --check ../../six-birds-duality-confinement/formalization/inventory/needles_dependency.sha256
```

The sibling project must also provide its declared Foundations dependencies
and use the same Lean and mathlib pins. The checksums identify the imported
Needles sources; they do not distribute them or pin the sibling's full
repository. Update the manifest deliberately when changing this dependency.

`RH.UpdatedAORXiInterfaces` applies those declarations. Its AOR
accounting theorem certifies proof payloads already held by a gamma
parameter. Its XI interface gives a conditional route from finite
dimensional null-legal residual vanishing through actual critical-strip
RH to Mathlib's full `RiemannHypothesis`. The response and zero-residual
premises remain explicit; the interface constructs neither a Selberg
gamma nor a zeta-derived XI probe.
`RH.AORReplayNoGo` uses the extended AOR complete-charge calculus with
the exact singleton XI currency. It proves that a finite budget for all
raw repeated zero-check operations is equivalent to critical-strip RH.
It is a calibration of any proposed source-stock law, not a payment
construction.
`RH.AORFreshNoGo` shows the complementary boundary: charging only the
first check admits a finite budget for every individual actual zero,
while coverage of the original repeated XI cost is equivalent to that
zero lying on the critical line.

`RH.FiniteZeroWindows` builds finite windows of actual completed-zeta
zeros and a reflection-invariant native probe. It proves that the
original-energy XI residual, evaluated on the actual displacement vector,
equals the positive window ledger. Exhaustive windows with a vanishing
budget imply critical-strip RH. Its complete currency operator identity
delegates to the shared
`XiCore.audit_currency_decomposition`; Needles NS uses that same theorem
for its physical point readout.
The module also proves that the residual quadratic vanishes on the actual
state in all exhaustive windows exactly
when RH holds; the missing analytic budget
must therefore be supplied independently of this representation. Its
Loewner-budget theorem uses the same operator-residual payment shape as
the Navier physical membrane and leaves the actual-state charge as an
explicit, RH-strength hypothesis.

`RH.RealPartWindowDC` quotients a reflected finite zero window by real
part. The resulting finite DC ledger has positive fiber weights, an
involution whose fixed locus is exactly the critical-line coordinate,
and a proved separating readout. Its `A_X` is exactly the finite RH
positive ledger and the fixed-target XI residual quadratic. A typed XI
operator payment becomes a DC domination record, and the imported DC
master theorem is applied to this concrete ledger under an explicit
vanishing payment sequence. No such analytic payment is constructed here.

`RH.GaussianCenterIntegralBlindness` proves that integrating the
unweighted linear complex Gaussian reading over every real center
erases horizontal displacement on actual completed-zeta zero windows.
Its finite-window value depends only on total multiplicity. This is a
scoped obstruction; the center-local nonlinear log-modulus reading in
`RH.ComplexGaussianObservation` still detects the RH XI charge.

The maintained cross-repository observation and return theorems are in
`../../six-birds-meta-math/lean/SixBirdsMetaMath/RHNavier/`. The Navier-only
complex Gaussian observation lemmas are owned by
`../../six-birds-needles/lean/SixBirdsNeedles/NSCore/ComplexGaussianObservations.lean`.
Those cross-repository results require separately prepared Needles and
metatheory projects and are outside this repository's build target.
Their RH and Navier
conditional endpoints state different premises. The RH zero-excess
premise is proved RH-equivalent; the Navier residual closure remains a
separate dynamical assumption.

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
python3 scripts/check_lean.py
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
