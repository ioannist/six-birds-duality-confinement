# Consolidated math artifact — Duality Confinement axis

Source paper proposal: `anti_loc/paper_proposal_self_dual_trace_confinement.md`.
Primary mathematical source: RH cascade step 69
(`anti_loc/thread_rh/steps/step69_duality_confinement_artifacts/duality_confinement_membrane_step69.tex`),
which is the RH-specialized presentation of the framework
duality-confinement membrane theorem (vendored `needles.tex` §5,
lines 1025–1505, not in our repo). Step 69 is self-contained at the
master-theorem level and is used as the source-of-record here. The
RH-specific specialization is presented separately in
`rh_construction.md` (the RH-axis artifact).

Labels are stable: `def:duality_confinement:<short-name>`,
`lem:duality_confinement:<short-name>`, etc. Top-level sections below
correspond 1-to-1 with the per-axis Lean module sections in
`lean/manifests/section_module_map.toml` and the queue at
`formalization/traceability/queue_duality_confinement.csv`.

Mechanization scope: the duality-confinement axis mechanizes the
abstract membrane apparatus (definitions, master theorem, exhaustive
squeeze, optimized scalar trace budget). The RH axis depends on this
axis. The structural recognition source `Γ_{SDTC}` and any axis-2
recognition source (`Γ_{SDTC-Selberg}`) live on the RH side as typed
structure carriers; this axis does not encode them.

---

## Involution

### def:duality_confinement:involutive-object-ledger

An **involutive object ledger** is a tuple
`X̂ = (X, J, μ, ψ, Y, J_iso)` consisting of:

- `X`: a visible object/root/defect space (carrier set);
- `J : X → X`: an involution (`J ∘ J = id_X`);
- `μ`: a positive object-ledger measure or finite positive weight
  system on `X`;
- `Y`: a real Hilbert response space (encoded abstractly as a typed
  carrier with inner product and norm);
- `J_iso : Y → Y`: a linear isometric involution;
- `ψ : X → Y`: an equivariant readout — `ψ(J x) = J_iso ψ(x)` for all
  `x ∈ X`.

The anti-invariant projector is `P_- := (I_Y - J_iso) / 2` and the
anti-invariant readout is `ψ_-(x) := P_- ψ(x)`.

**Provenance**: step 69 §2 def (Involutive object ledger).

**Mechanization note**: `X` and `Y` are taken as `Type u`; `J`,
`J_iso`, `ψ` as plain functions; `μ` as a typed weight function (finite
positive). This module hosts only the involutive object ledger
structure itself; the anti-invariant ledger `A_X` and the trace
functional are introduced in §AntiInvariantLedger.

---

## Separation

### def:duality_confinement:separating-readout

The anti-invariant readout `ψ_-` **separates the fixed locus** when
```
ψ_-(x) = 0   ⟺   x ∈ Fix(J)
```
holds on the visible support of `μ` (i.e. on the set
`{x ∈ X | μ({x}) > 0}` in the finite case, or `μ`-a.e. in the
measure-theoretic case).

It is **quantitatively separating** when there exists a modulus
`m : (0, ∞) → (0, ∞)` such that
```
∀ ε > 0, ∀ x ∈ X.  dist(x, Fix(J)) ≥ ε  ⟹  ‖ψ_-(x)‖ ≥ m(ε).
```

**Provenance**: step 69 §2 def (Separating anti-invariant readout).

**Mechanization note**: encode both the qualitative and quantitative
forms. The qualitative form is a `Prop` predicate; the quantitative
form bundles a modulus function with a proof obligation.

---

## AntiInvariantLedger

### def:duality_confinement:anti-invariant-ledger

The **anti-invariant object ledger** of an involutive object ledger
(`def:duality_confinement:involutive-object-ledger`) is
```
A_X := ∫_X ψ_-(x) ψ_-(x)* dμ(x),
```
interpreted abstractly as an element of a typed positive cone with a
distinguished `trace` operation (finite-rank, trace-class, or any
representation in which the trace identity below is well-defined).

**Provenance**: step 69 §2 def (`A_X` construction).

**Mechanization note**: encoded as a typed positive cone with a
typed `trace` field. The "trace-class" hypothesis from the TeX
presentation is replaced by the standing assumption that the positive
cone supports a monotone trace functional satisfying
`A ⪯ B ⟹ trace A ≤ trace B`. The cone's positivity axiom + the
trace functional + the order `⪯` form the algebraic substrate that
the master theorem uses.

### lem:duality_confinement:trace-identity

Assume `A_X` is in the trace-class regime where `tr A_X` is
well-defined. Then
```
tr A_X = ∫_X ‖ψ_-(x)‖² dμ(x).
```
Consequently `A_X = 0 ⟺ ψ_-(x) = 0` for `μ`-a.e. `x ∈ X`.

**Proof (TeX, step 69 §3)**: the identity is the definition of trace
for rank-one positive operators integrated against a positive
measure. Since the integrand is nonnegative, vanishing of the
integral is equivalent to vanishing almost everywhere. A positive
trace-class operator has trace zero iff it is the zero operator.

**Mechanization note**: encode the identity as the *defining*
relation between the typed anti-invariant ledger and the integral of
the squared norm — i.e. `(A_X).trace = ∫ ‖ψ_-‖² dμ` is built into
the constructor of `A_X` rather than derived. The equivalence
`A_X = 0 ⟺ ψ_- = 0 μ-a.e.` follows from positivity (a positive
element of the typed cone with trace zero is the zero element).
This is a non-`rfl` step: it requires the typed cone's positivity
axiom + nonneg integrand vanishing iff integral vanishes.

---

## DirectConfinement

### thm:duality_confinement:separation-confinement

Assume the anti-invariant readout separates the fixed locus
(`def:duality_confinement:separating-readout`). If `A_X = 0`, then
```
μ(X ∖ Fix(J)) = 0.
```
In the finite weighted case, every visible object with positive
weight lies in `Fix(J)`.

**Proof (TeX, step 69 §3 thm)**: by the trace identity, `ψ_-(x) = 0`
for `μ`-a.e. `x`. Separation identifies that zero set with `Fix(J)`
on the visible support.

### thm:duality_confinement:quantitative-confinement

Assume quantitative separation. Then for every `ε > 0`,
```
μ({x ∈ X | dist(x, Fix(J)) ≥ ε}) ≤ tr(A_X) / m(ε)².
```

**Proof (TeX, step 69 §3 thm)**: on `{dist(x, Fix(J)) ≥ ε}`,
`‖ψ_-(x)‖² ≥ m(ε)²`. Apply Markov's inequality to the trace identity.

---

## Domination

### def:duality_confinement:completed-domination-bridge

A **completed domination bridge** from the object ledger to a
positive carrier-side currency `K^- ⪰ 0` is a record
```
A_X ⪯ K^- + E
```
with `E ⪰ 0` a declared bridge defect. In the **exact case** `E = 0`,
writing `A_X = V*V`, `K^- = W*W`, the bridge is exact iff there
exists a contraction `T` such that
```
V = T W.
```

**Provenance**: step 69 §4 def 4.1.

### thm:duality_confinement:douglas-domination

**Douglas factorization.** Let `A = V*V` and `K = W*W` be bounded
positive operators on the same response space. Then
```
A ⪯ K   ⟺   ∃ contraction T.  V = T W.
```

**Proof (TeX, step 69 §4 thm)**: this is the Douglas factorization
lemma applied to `V*` and `W*`, equivalently to the range inclusion
and norm inequality induced by `V*V ⪯ W*W`.

**Mechanization note** (per `audit_summary.md` §A1): encode this as a
packaged equivalence between two typed witnesses (`Domination` and
`ContractiveFactor`), not as an external mathlib invocation. The
substantive content is the forward direction (`⪯ ⟹ factor`) which
packages the range inclusion induced by the ordering. Reverse
direction is computational.

---

## MasterTheorem

### thm:duality_confinement:master-theorem

**Duality-confinement membrane theorem** (the master theorem).

Let `X̂ = (X, J, μ, ψ, Y, J_iso)` be an involutive object ledger
(`def:duality_confinement:involutive-object-ledger`) with separating
anti-invariant readout (`def:duality_confinement:separating-readout`).
Suppose there exists a sequence of completed domination records
```
A_X ⪯ B_n   (n = 1, 2, ...)
```
with `B_n ⪰ 0` and
```
tr B_n → 0   as n → ∞.
```
Then
```
μ(X ∖ Fix(J)) = 0.
```

**Proof (TeX, step 69 §4 thm)**: for every `n`,
`0 ⪯ A_X ⪯ B_n`, hence `0 ≤ tr A_X ≤ tr B_n`. Taking `n → ∞` gives
`tr A_X = 0`, hence `A_X = 0` (positivity). Apply the separation
theorem (`thm:duality_confinement:separation-confinement`).

**Mechanization note**: this is the load-bearing master theorem and
the principal mechanization target for this axis. The proof has
three non-`rfl` steps: (1) trace monotonicity from `⪯`, (2) the
squeeze `0 ≤ tr A_X ≤ tr B_n` with `tr B_n → 0` ⟹ `tr A_X = 0`,
(3) trace-zero positive ⟹ zero element, then the separation theorem.

---

## ExhaustiveSqueeze

### def:duality_confinement:exhaustive-moving-ledger

A finite-window or moving object ledger `A_{X,n}` is **exhaustive**
for a completed ledger `A_X` if there exist inclusions/transports
`ι_n` and tail operators `T_n ⪰ 0` such that
```
A_X ⪯ ι_n A_{X,n} ι_n* + T_n.
```
It is **vanishing-exhaustive** under bounds `A_{X,n} ⪯ B_n` if
```
tr(ι_n B_n ι_n*) + tr T_n → 0.
```

**Provenance**: step 69 §5 def 5.1.

### thm:duality_confinement:exhaustive-squeeze

**Exhaustive ledger squeeze.** If `A_{X,n} ⪯ B_n` and the moving
ledger is vanishing-exhaustive for `A_X`, then `A_X = 0`. Under
readout separation, visible object mass is confined to `Fix(J)`.

**Proof (TeX, step 69 §5 thm)**:
```
0 ⪯ A_X ⪯ ι_n B_n ι_n* + T_n.
```
Taking traces and passing to the limit yields `tr A_X = 0`.

---

## DefectedBudget

### def:duality_confinement:defected-budget

A **defected duality-confinement record** has the form
```
A_X ⪯ (1+t)(K^-_n + E_{src,n}) + (1+t^{-1}) E_{br,n}
```
for `t > 0`, with `E_{br,n}` a bridge/domination defect and
`E_{src,n}` a source/membrane defect. In a collapse ladder one often
has `K^-_n ⪯ Λ_n^{-1} Θ_0^-`, giving
```
B_n(t) = (1+t)(Λ_n^{-1} Θ_0^- + E_{src,n}) + (1+t^{-1}) E_{br,n}.
```

**Status**: `support_only`. Not part of the master mechanization
chain; recorded for completeness because the optimized scalar trace
budget below references the shape.

### prop:duality_confinement:optimized-trace-budget

Let
```
a_n = tr(Λ_n^{-1} Θ_0^- + E_{src,n}),
b_n = tr E_{br,n}.
```
Then
```
inf_{t>0} tr B_n(t) = (√a_n + √b_n)².
```
Sufficient scalar condition for exact confinement by fixed-ledger
squeeze: `a_n → 0` and `b_n → 0`.

**Proof (TeX, step 69 §6 prop)**: minimize `(1+t) a_n + (1+t^{-1}) b_n`
over `t > 0`. The minimizer is `t = √(b_n / a_n)` when `a_n, b_n > 0`,
with the stated value. Degenerate cases follow by continuity.

**Mechanization note** (per `audit_summary.md` §A2): non-`rfl`
content is the optimization in `t`. Expand
`(1+t)a + (1+t^{-1})b = a + b + ta + b/t`. By AM-GM,
`ta + b/t ≥ 2√(ab)`, with equality at `t = √(b/a)`. Hence
`inf ≥ a + b + 2√(ab) = (√a + √b)²`. The infimum is attained, so
equality.

---

## Out-of-scope-for-Lean items

### obl:duality_confinement:sdtc-source

`Γ_{SDTC}`: Self-Dual Trace Confinement structural law as
recognition source. Statement (per proposal §2.2): for a formed Six
Birds closure with determining state in V-Differential's
trace-state-only column, lawful involutive duality `J` on visible
object ledger `X`, and separating anti-invariant readout `ψ_-`, the
formed closure has no surviving anti-invariant trace mass —
equivalently, `A_X = 0`.

**Why out of scope**: this is a *structural law*, not a derivation.
The proposal's §2.4 and §8 explicitly identify it as recognition
content. The duality-confinement axis does NOT mechanize `Γ_{SDTC}`;
the RH axis encodes the RH-specialized version `Γ_{SDTC-Selberg}` as
a typed structure carrier (`obl:rh:gamma-sdtc-selberg`).

The duality-confinement axis stays purely at the master-theorem
level: given the domination-records hypothesis (no matter how
supplied), `μ(X ∖ Fix(J)) = 0` follows.

---

## Dependency order

Suggested mechanization order matches the queue at
`formalization/traceability/queue_duality_confinement.csv`:

1. Involution (`def:involutive-object-ledger`)
2. Separation (`def:separating-readout`)
3. AntiInvariantLedger (`def:anti-invariant-ledger`, `lem:trace-identity`)
4. DirectConfinement (`thm:separation-confinement`, `thm:quantitative-confinement`)
5. Domination (`def:completed-domination-bridge`, `thm:douglas-domination`)
6. MasterTheorem (`thm:duality-confinement-master`)
7. ExhaustiveSqueeze (`def:exhaustive-moving-ledger`, `thm:exhaustive-squeeze`)
8. DefectedBudget (`def:defected-budget` as support_only, `prop:optimized-trace-budget`)

Sections 1–6 are load-bearing. Section 7 is a strengthening the RH
axis does not currently use. Section 8 is included for completeness
(`prop:optimized-trace-budget` per proposal §11.4).
