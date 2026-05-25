# Consolidated math artifact — RH axis

Source paper proposal: `anti_loc/paper_proposal_rh_via_sdtc_selberg.md`.
Primary mathematical sources:
- RH cascade step 69 §7 (RH specialization)
  (`anti_loc/thread_rh/steps/step69_duality_confinement_artifacts/`).
- Step 448 (Sel^!_{ζ,tr} construction + Theorem T)
  (`anti_loc/thread_rh/steps/step448_sdtc_closure_construction_artifacts/`).
- Step 449 (master theorem applicability audit on Sel^!_{ζ,tr})
  (`anti_loc/thread_rh/steps/step449_sdtc_applicability_and_anti_tautology_strengthening_artifacts/`).
- Step 454 (recognition closure landing chain)
  (`anti_loc/thread_rh/steps/step454_sdtc_recognition_closure_artifacts/`).
- Proposal Appendix A (mechanization-ready theorem statements).

Labels are stable: `def:rh:<short-name>`, `thm:rh:<short-name>`,
`obl:rh:<short-name>`, etc. Top-level sections below correspond
1-to-1 with the per-axis Lean module sections in
`lean/manifests/section_module_map.toml` and the queue at
`formalization/traceability/queue_rh.csv`.

Mechanization scope: the RH axis mechanizes the saturated trace
closure typed objects, the translation theorem T, and the
conditional landing chain (Γ_{SDTC-Selberg} ⟹ RH). The structural
recognition source `Γ_{SDTC-Selberg}` is encoded as a typed structure
carrier — out of scope for derivation per proposal §11.4. The axis
depends on the duality-confinement axis for the master theorem.

---

## Involution

### def:rh:fe-involution

The **functional-equation involution** on the complex plane is
```
J_L(s) := 1 - s̄.
```
Its fixed locus is the critical line:
```
Fix(J_L) = {s ∈ ℂ | Re(s) = 1/2}.
```
`J_L` is involutive (`J_L ∘ J_L = id_ℂ`).

**Provenance**: step 69 §7 (RH specialization); step 448 Stage I.7.

**Mechanization note**: encoded as a function on a typed complex
number record (real part + imaginary part + complex conjugate). No
mathlib complex numbers; build a minimal `Complex` record locally in
this module (or in a small supporting helper that this section
introduces).

### def:rh:psi-minus-rh

The **separating anti-invariant readout** for `J_L` is
```
ψ_-(s) := Re(s) - 1/2.
```
This is anti-invariant under `J_L` (`ψ_-(J_L s) = -ψ_-(s)`) and
vanishes exactly on `Fix(J_L)`.

**Provenance**: step 69 §7.

---

## ZeroLedger

### def:rh:nontrivial-zero-ledger

The **nontrivial zero ledger** `Z_ζ^{nt}` is the typed multiset of
zeros of the completed Riemann zeta `Λ_ζ(s) := π^{-s/2} Γ(s/2) ζ(s)`
in the critical strip `0 < Re(s) < 1`. Each zero `ρ ∈ Z_ζ^{nt}`
carries a positive integer multiplicity `m_ρ > 0`.

The associated measure is `μ_L({ρ}) = m_ρ`.

**Provenance**: step 448 Stage I.7; proposal §4.1.

**Mechanization note**: `Z_ζ^{nt}` is encoded as a finite-multiset
record parameter (a function from zeros to multiplicities, with the
zeros and multiplicities both supplied externally). The
mechanization does NOT depend on a Lean construction of `Λ_ζ`; the
zero ledger is opaque input data. RH then states "every `ρ` in this
typed ledger has `Re(ρ) = 1/2`".

---

## AntiInvariantZeroLedger

### def:rh:anti-invariant-zero-ledger

The **anti-invariant zero ledger** is
```
A_Z(ζ) := Σ_{ρ ∈ Z_ζ^{nt}} m_ρ · |Re(ρ) - 1/2|².
```
By construction `A_Z(ζ) ≥ 0` as a real scalar.

**Provenance**: step 448 Stage I.8; proposal §4.1.

**Mechanization note**: encoded as a `Real`-valued (or
typed-ordered-field-valued) sum over the typed zero ledger. The sum
is finite at the type level (the ledger is supplied as a finite
multiset record). See `audit_summary.md` §A3 for the real-part type
representation note.

---

## SatSelShell

### def:rh:sat-sel-shell

The **saturated completed Selberg trace closure** `Sel^!_{ζ,tr}` is
a typed record bundling the construction-time data:
```
Sel^!_{ζ,tr} := (
    H_L,        -- completed L-history carrier (typed; opaque internal structure)
    I_tr,       -- lawful trace instrument
    EQ_tr,      -- saturated trace observables
    EM_zero,    -- predictive verifier events
    Q_L,        -- current quotient H_L / ~_Q
    M_L,        -- predictive quotient H_L / ~_M
    pi_L,       -- comparison map M_L → Q_L
    J_L,        -- functional-equation involution (def:rh:fe-involution)
    Lambda_L,   -- completed L-function (opaque; only its zero ledger is used)
    Z_nt,       -- nontrivial zero ledger (def:rh:nontrivial-zero-ledger)
    A_Z,        -- anti-invariant zero ledger (def:rh:anti-invariant-zero-ledger)
    Vis_L,      -- instrument-relative visibility map
    Audit_L     -- audit provenance record
)
```

The construction passes all seven Foundations II schemas at step
448 Stage IV. The mechanization records the shell as a structure
type with the above fields, takes admissibility as a hypothesis
parameter (not Lean-derived; encoded in the `Audit_L` field), and
uses the fields downstream as needed.

**Provenance**: step 448 Stages I.1–I.10; proposal §4.

**Mechanization note**: the shell is essentially a parameter record
for downstream theorems. Most fields are typed opaque carriers; the
load-bearing fields for the mechanization chain are `J_L`,
`Z_nt`, and `A_Z`. The other fields appear as parameter types so
the conditional theorem's hypothesis names are visibly the same
objects the paper proves admissible.

---

## TranslationT

### thm:rh:translation-T-forward

**Forward direction**: `A_Z(ζ) = 0 ⟹ RH`. Formally, for any
nontrivial zero ledger `Z_ζ^{nt}` and any `ρ ∈ Z_ζ^{nt}`,
```
A_Z(ζ) = 0   ⟹   Re(ρ) = 1/2.
```

**Proof (step 448 Stage II forward)**:
```
A_Z(ζ) = Σ_{ρ} m_ρ · |Re(ρ) - 1/2|².
```
Each term is nonnegative (real square times positive integer). If
the sum is zero, every term is zero. Since `m_ρ > 0`, the factor
`|Re(ρ) - 1/2|²` must be zero, hence `Re(ρ) = 1/2`.

**Mechanization note**: substantive content is "finite sum of
nonneg terms = 0 ⟹ each term = 0" plus "real-square = 0 ⟹ real = 0".
Both are non-`rfl` at finite-type granularity.

### thm:rh:translation-T-reverse

**Reverse direction**: `RH ⟹ A_Z(ζ) = 0`. Formally, if
`Re(ρ) = 1/2` for every `ρ ∈ Z_ζ^{nt}`, then `A_Z(ζ) = 0`.

**Proof (step 448 Stage II reverse)**: each `|Re(ρ) - 1/2|² = 0`,
so each term in the sum is `m_ρ · 0 = 0`, hence the sum is `0`.

**Mechanization note**: this is a straightforward sum-of-zeros
computation. Non-`rfl` content is the substitution under the sum.

### thm:rh:translation-T

**Theorem T (translation)**: `A_Z(ζ) = 0 ⟺ RH`.

**Proof**: combine forward (`thm:rh:translation-T-forward`) and
reverse (`thm:rh:translation-T-reverse`).

**Provenance**: step 448 Stage II; proposal §5; appendix A
"Theorem T".

The proof uses only:
- The construction of `A_Z(ζ)` from `def:rh:anti-invariant-zero-ledger`.
- Positivity of squared distances (forward).
- The definition of `ψ_-` from `def:rh:psi-minus-rh` (reverse).

**No SDTC source used; no Weil positivity invoked; no RH assumed.**
Theorem-grade by construction.

---

## RecognitionSource (out of scope for Lean derivation)

### obl:rh:gamma-sdtc-selberg

`Γ_{SDTC-Selberg}` is the **structural recognition source** for the
RH closure. It asserts: on the saturated Sel^!_{ζ,tr} under `I_tr`
and `J_L`, the duality-confinement master theorem's
domination-records hypothesis obtains as content of formed-layer
closure:
```
∃ B_n ⪰ 0.  A_Z(ζ) ⪯ B_n   ∧   tr B_n → 0.
```

Per proposal §6.2, `Γ_{SDTC-Selberg}` is a structured Foundations II
audited recognition object with eight provenance fields:
duality-confinement structural law, V-Differential TSO placement,
step 69 RH extraction, the shell `Sel^!_{ζ,tr}`, instrument `I_tr`,
involution `J_L`, zero ledger `Z_ζ^{nt}`, anti-invariant ledger
`A_Z(ζ)`, readout `A_Z(ζ) = 0`, and audit provenance.

**Why out of scope (per proposal §11.4 and §10.4)**:
- "Mechanization of `Γ_{SDTC-Selberg}` is not pursued — recognition
  sources are not subject to Lean-style derivation."
- The three-option derivation sweep (steps 451–453) failed to
  derive the domination-records hypothesis from framework
  primitives; the cascade's own diagnostic is that the domination
  content is part of what closure formation per Foundations I
  structurally provides, not separately derivable.

**Mechanization encoding (as landed)**: `Γ_{SDTC-Selberg}` is
realized as a typed `structure` carrier named `GammaSdtcSelberg`,
declared **inline** in
`lean/SixBirdsDualityConfinement/RH/RHConditional.lean` (its only
consumer; placement convention from kickoff §12 — a type lives next
to its only consumer). It is not a standalone `RecognitionSource.lean`
module. The forbidden-tokens rule
bans `axiom`/`opaque`/`constant`/`sorry`/`admit` anywhere in
`lean/SixBirdsDualityConfinement/*`; the recognition source is NOT
declared with `axiom`. Inventory `intended_status` is
`out_of_scope_recognition_source`.

**Bridge-carrier shape (as landed)**: the carrier supplies, in one
record, the full duality-confinement apparatus needed by
`DCMasterApplied.dcMasterApplied` **together with** the bridge
propositions that link the apparatus to the shell's `A_Z` ledger.
The shape is (approximately):
```
structure GammaSdtcSelberg
    {R : Involution.RealCoordinate}
    (shell : SatSelShell R) where
  ledger : DualityConfinement.Involution.InvolutiveObjectLedger
  sep    : DualityConfinement.Separation.SeparatingReadout ledger
  A      : DualityConfinement.AntiInvariantLedger.AntiInvariantLedger ledger
  -- Bridge propositions to the shell:
  same_readout       : ∀ x, A.psi_minus x = sep.psi_minus x
  mu_zero_of_ae      : A.psi_minus_ae_zero → shell.A_Z.A_Z = shell.A_Z.zero
  visible_zero_of_ae : A.psi_minus_ae_zero →
                         ∀ x, x ∈ ledger.mu_support →
                           A.psi_minus x = sep.zero_Y
  -- Domination records and typed-cone scaffolding:
  B_n                  : Nat → A.Cone
  domination_records   : ∀ n, A.preceq A.A_X (B_n n)
  B_n_positive         : ∀ n, A.Positive (B_n n)
  tr_B_n_tends_zero    : Prop
  h_tr_B_n_tends_zero  : tr_B_n_tends_zero
  TraceNonnegative     : A.TraceValue → Prop
  positive_trace_nonnegative : ∀ C, A.Positive C → TraceNonnegative (A.tr C)
  TraceZero            : A.TraceValue
  squeeze_trace_zero   : (TraceNonnegative (A.tr A.A_X)) →
                           (∀ n, A.TraceLE (A.tr A.A_X) (A.tr (B_n n))) →
                             (∀ n, A.Positive (B_n n)) →
                               tr_B_n_tends_zero →
                                 A.tr A.A_X = TraceZero
  trace_zero_positive_zero : A.tr A.A_X = TraceZero → A.A_X = A.zero
```

The bridge propositions (`same_readout`, `mu_zero_of_ae`,
`visible_zero_of_ae`) are typed hypotheses, not derivations: the
DC apparatus data is supplied together with the assertion that it
coheres with the shell, not constructed from the shell.

Downstream, `rhConditional` takes `(γ : GammaSdtcSelberg shell)` as
explicit parameter; the proof feeds `γ.sep`, `γ.A`, and the bridge
fields to `dcMasterApplied`, yielding `shell.A_Z.A_Z = shell.A_Z.zero`,
and then applies `translationTForward`.

**Note on module placement**: no separate
`RecognitionSource.lean` module exists or appears in
`section_module_map.toml`. The carrier is declared inline in
`RHConditional.lean` per the placement convention above.

---

## DCMasterApplied

### thm:rh:dc-master-applied

**Duality-confinement application.** Given:
- The involutive ledger structure on `Z_ζ^{nt}` with `J_L(s) = 1 - s̄`
  (which fixes Re(s) = 1/2);
- The separating anti-invariant readout `ψ_-(s) = Re(s) - 1/2`;
- A sequence of completed domination records `A_Z(ζ) ⪯ B_n` with
  `B_n ⪰ 0` and `tr B_n → 0`,

the master theorem (`thm:duality_confinement:master-theorem` from
the duality-confinement axis) yields `A_Z(ζ) = 0`.

**Proof**: direct application of the master theorem to the involutive
object ledger `(Z_ζ^{nt}, J_L|_{Z_ζ^{nt}}, μ_L, ψ_-, ℝ, -Id_ℝ)`.
The linear isometric involution on the 1-D real response space is
`J_iso = -Id` (because `ψ_-` is real-valued and anti-invariant under
`J_L`); the anti-invariant projector becomes
`P_- = (Id - (-Id))/2 = Id`, so `ψ_-` is its own anti-invariant
projection. Equivariance `ψ_-(J_L ρ) = -ψ_-(ρ) = J_iso ψ_-(ρ)` is the
content of `def:rh:psi-minus-rh`.

**Provenance**: step 454 P2; proposal §7.1 step 2; appendix A
"Duality-confinement application".

**Mechanization note (as landed)**: this is the load-bearing
application of the duality-confinement axis's master theorem to the
RH-specific setup. The Lean module does **not** instantiate the
abstract involutive object ledger of the DC axis directly on
`Sel^!_{ζ,tr}`. Instead, `DCMasterApplied.dcMasterApplied` composes
`thm:duality_confinement:master-theorem` through a typed-bridge
interface: the DC apparatus (involutive object ledger, separating
readout, anti-invariant ledger) is taken as input, and three bridge
fields (`same_readout`, `mu_zero_of_ae`, `visible_zero_of_ae`)
connect that apparatus to the shell's `A_Z` ledger. The body-level
role assignment `(Sel ↔ IOL, A_Z ↔ A_X, J_L ↔ J, ψ_-^RH ↔ ψ_-)` is
the mathematical interpretation of the bridge interface, not a Lean
derivation of the role assignment. The DC apparatus together with
the bridge fields is supplied by `obl:rh:gamma-sdtc-selberg` at the
next step (`thm:rh:conditional`).

---

## RHConditional

### thm:rh:conditional

**Conditional theorem (the RH closure)**. Let `shell : Sel^!_{ζ,tr}`
be a saturated trace closure (`def:rh:sat-sel-shell`) and suppose
`γ : GammaSdtcSelberg shell` (`obl:rh:gamma-sdtc-selberg`). Then RH
holds in the form: for every `ρ ∈ shell.Z_nt`, `Re(ρ) = 1/2`.

**Proof (step 454 final proof statement; proposal §7.1)**:

1. From `γ`, extract the domination-records witness:
   `∃ B_n ⪰ 0` with `shell.A_Z ⪯ B_n` and `tr B_n → 0`.
2. Apply `thm:rh:dc-master-applied` (which in turn invokes the
   duality-confinement axis's `thm:duality_confinement:master-theorem`)
   to obtain `shell.A_Z = 0`.
3. Apply `thm:rh:translation-T` (specifically the forward
   direction `thm:rh:translation-T-forward`) to obtain `RH`.

The chain is direct (not by contradiction); the duality-confinement
mechanism supplies the positive form `A_Z(ζ) = 0` directly via the
explicit `γ`.

**Provenance**: step 454 final proof statement
(`step454_final_proof_statement.md`); proposal §7.1, appendix A
"Conditional theorem".

**Mechanization note**: this is the headline theorem of the RH
axis. It explicitly takes the recognition source `γ` as a
hypothesis parameter — the conditional in "conditional theorem" is
literal: `γ` is a Lean-level hypothesis, not a Lean-level proven
fact. Outside Six Birds, the result is the conditional implication
`γ ⟹ RH(shell)`; inside Six Birds, `γ` is supplied as recognition
content per `obl:rh:gamma-sdtc-selberg`.

---

## Bookkeeping items (recorded but not Lean-derived)

The proposal's §B (Six Gates + Gate 7 audit), §9 (NC-1 through
NC-12), and §10 (three-option derivation sweep verdicts) are
metamathematical audit constraints. They are not Lean-mechanizable
theorems; they belong in the paper prose with provenance to the
cascade step files.

---

## Dependency order

Suggested mechanization order matches the queue at
`formalization/traceability/queue_rh.csv`:

1. Involution (`def:fe-involution`, `def:psi-minus-rh`)
2. ZeroLedger (`def:nontrivial-zero-ledger`)
3. AntiInvariantZeroLedger (`def:anti-invariant-zero-ledger`)
4. SatSelShell (`def:sat-sel-shell`)
5. TranslationT (`thm:translation-T-forward`, `thm:translation-T-reverse`, `thm:translation-T`)
6. RecognitionSource (`obl:rh:gamma-sdtc-selberg`; typed structure carrier; not in queue)
7. DCMasterApplied (`thm:dc-master-applied`)
8. RHConditional (`thm:rh:conditional`)

Sections 1–5 are construction-grade and theorem-grade by construction.
Section 6 is a typed-structure carrier (no proof; introduced by the
`RHConditional` dispatch when needed). Section 7 re-uses the
duality-confinement axis. Section 8 is the headline result.
