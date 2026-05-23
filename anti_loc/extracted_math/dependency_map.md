# Dependency Map — Math sources for mechanization

Walks back from each paper proposal's mechanization targets through the
cited RH cascade steps and the foundations framework apparatus. Each
row lists a math item that the Lean mechanization needs and the
provenance step(s) where the item is stated.

Cited steps:
- Self-Dual Trace Confinement proposal (SDTC, paper 1): step 65, 67, 69, 71–84, 437–447, 448–454
- RH-via-SDTC-Selberg proposal (RH, paper 2): step 65, 67, 69, 71–84, 437–447, 448–454

Both proposals draw from the same RH cascade. Most cited steps are
provenance/support; only a small subset contribute distinct math
items the mechanization needs.

Framework apparatus (vendored from foundations-iii):
- `needles.tex` §5 (lines 1025–1505): Duality-Confinement Membrane
  Theorem — definitions, master theorem, exhaustive squeeze, defected
  obstruction budgets. **NOT** in our repo; not vendored. Step 69 is
  the self-contained RH-specialized presentation of the same content
  and is sufficient as the mathematical source.
- `adequacy.tex`: Schur-complement residual calculus, referenced by
  the defected-budget records. Not load-bearing for our mechanization
  scope (we mechanize at the master-theorem level, not the
  Schur-defect-budget level).

## Axis: duality_confinement

| Label | Math item | Source step(s) | Status |
|-------|-----------|----------------|--------|
| `def:involutive-object-ledger` | Involutive object ledger `(X, J, μ, ψ, Y, J_iso)` with equivariant readout `ψ(Jx) = J_iso ψ(x)`, projector `P_- = (I - J_iso)/2`, anti-invariant readout `ψ_-(x) = P_- ψ(x)` | step 69 §2 def 2.1 (Involutive object ledger) | mechanize_now |
| `def:anti-invariant-ledger` | `A_X := ∫_X ψ_-(x) ψ_-(x)* dμ(x)` (positive semidefinite, trace-class regime) | step 69 §2 def 2.1 (`A_X`) | mechanize_now |
| `def:separating-readout` | Separating: `ψ_-(x) = 0 ⟺ x ∈ Fix(J)` on visible support; quantitatively separating: ∀ε>0 ∃m(ε)>0 dist(x, Fix(J)) ≥ ε ⟹ ‖ψ_-(x)‖ ≥ m(ε) | step 69 §2 def 2.2 (Separating anti-invariant readout) | mechanize_now |
| `lem:trace-identity` | `tr A_X = ∫_X ‖ψ_-(x)‖² dμ(x)` and `A_X = 0 ⟺ ψ_-(x) = 0 μ-a.e.` | step 69 §3 lem 3.1 (Trace identity) | mechanize_now |
| `thm:separation-confinement` | Under separating readout: `A_X = 0 ⟹ μ(X ∖ Fix(J)) = 0` | step 69 §3 thm 3.2 (Separation implies fixed-locus confinement) | mechanize_now |
| `thm:quantitative-confinement` | Under quantitative separation: `μ{x: dist(x, Fix(J)) ≥ ε} ≤ tr A_X / m(ε)²` | step 69 §3 thm 3.3 (Quantitative confinement) | mechanize_now |
| `def:completed-domination-bridge` | Bridge record `A_X ⪯ K^- + E` with `E ⪰ 0` bridge defect; exact case `E = 0` iff exists contraction `T` with `V = TW` where `A_X = V*V`, `K^- = W*W` | step 69 §4 def 4.1 (Completed domination bridge) | mechanize_now |
| `thm:douglas-domination` | Douglas factorization: `A ⪯ K` iff exists contraction `T` with `V = TW` (where `A = V*V`, `K = W*W`) | step 69 §4 thm 4.2 (Douglas domination) | mechanize_now |
| `thm:duality-confinement-master` | **Master theorem.** Involutive object ledger with separating readout + completed domination records `A_X ⪯ B_n`, `B_n ⪰ 0`, `tr B_n → 0` ⟹ `μ(X ∖ Fix(J)) = 0` | step 69 §4 thm 4.3 (Duality-confinement membrane theorem) | mechanize_now |
| `def:exhaustive-moving-ledger` | Finite-window ledger `A_{X,n}` with inclusions `ι_n` and tails `T_n ⪰ 0` such that `A_X ⪯ ι_n A_{X,n} ι_n* + T_n`; vanishing-exhaustive under `A_{X,n} ⪯ B_n` if `tr(ι_n B_n ι_n*) + tr T_n → 0` | step 69 §5 def 5.1 (Exhaustive moving ledger) | mechanize_now |
| `thm:exhaustive-squeeze` | Exhaustive ledger squeeze: under hypotheses, `A_X = 0` | step 69 §5 thm 5.2 (Exhaustive ledger squeeze) | mechanize_now |
| `def:defected-budget` | Defected duality-confinement record `A_X ⪯ (1+t)(K^-_n + E_{src,n}) + (1+t^-1) E_{br,n}`; in collapse ladder with `K^-_n ⪯ Λ_n^-1 Θ_0^-`, `B_n(t) = (1+t)(Λ_n^-1 Θ_0^- + E_{src,n}) + (1+t^-1) E_{br,n}` | step 69 §6 def 6.1 (General obstruction budget) | support_only |
| `prop:optimized-trace-budget` | `inf_{t>0} tr B_n(t) = (√a_n + √b_n)²` where `a_n = tr(Λ_n^-1 Θ_0^- + E_{src,n})`, `b_n = tr E_{br,n}` | step 69 §6 prop 6.2 (Optimized scalar trace budget) | mechanize_now |
| `obl:sdtc-source` | `Γ_{SDTC}` — Self-Dual Trace Confinement structural law as recognition source. Under V-Differential trace-state-only column + lawful involutive duality, formed closure supplies the domination records hypothesis | proposal §2.4, sibling-of recognition source. NOT derivable per §11.2 hard rule. | out_of_scope_recognition_source |

Out-of-scope-for-Lean items in this axis:
- `Γ_{SDTC}` (the structural recognition source itself). Per SDTC
  proposal §2.4 and §8 it is the named source of the
  domination-records hypothesis on formed self-dual closures, not
  derivable from framework primitives. Encoded as a typed structure
  carrier in `RecognitionSource.lean` (RH axis side). The
  duality-confinement axis mechanizes only the master theorem and
  supporting infrastructure; it does NOT mechanize `Γ_{SDTC}`.

## Axis: rh

The RH axis mechanizes the Sel^!_{ζ,tr} construction, the translation
theorem T, and the conditional landing chain. It depends on the
duality-confinement axis (master theorem) and encodes
`Γ_{SDTC-Selberg}` as a typed structure carrier.

| Label | Math item | Source step(s) | Status |
|-------|-----------|----------------|--------|
| `def:completed-zeta` | `Λ_ζ(s) = π^{-s/2} Γ(s/2) ζ(s)` (completed Riemann zeta); the construction takes Λ as opaque entire data and uses only its zero ledger | step 448 audited-shell §1 (completed function form) | mechanize_now |
| `def:nontrivial-zero-ledger` | `Z_ζ^{nt}`: multiset of nontrivial zeros with multiplicities `m_ρ`, measure `μ_L({ρ}) = m_ρ` | step 448 Stage I.7 (zero ledger configuration); proposal §4.1 | mechanize_now |
| `def:fe-involution` | `J_L(s) = 1 - s̄` functional-equation involution; `Fix(J_L) = {Re(s) = 1/2}` | step 69 RH-specialization; step 448 Stage I.7 (involution) | mechanize_now |
| `def:psi-minus-rh` | `ψ_-(s) = Re(s) - 1/2` (separating anti-invariant readout for the RH involution) | step 69 §7 RH specialization | mechanize_now |
| `def:anti-invariant-zero-ledger` | `A_Z(ζ) := Σ_{ρ ∈ Z_ζ^{nt}} m_ρ · |Re(ρ) - 1/2|²` (anti-invariant zero ledger, positive semidefinite) | step 448 Stage I.8 (`A_Z`); proposal §4.1 | mechanize_now |
| `def:sat-sel-shell` | Saturated completed Selberg trace closure `Sel^!_{ζ,tr}` as a typed structure with carrier fields `H^!_L, I_tr, E^!_Q^tr, E^!_M^zero, Q^!_L, M^!_L, π^!_L, J_L, Λ_L, Z_ζ^{nt}, A_Z(ζ), Vis^!_L, Audit_L` | step 448 Stages I.1–I.10 + proposal §4.1 | mechanize_now |
| `def:domination-records` | Domination-records witness: `∃ B_n ⪰ 0` with `A_Z(ζ) ⪯ B_n` and `tr B_n → 0` | step 449 Hyp 3 named residual `Xi_SDTC_domination_records`; proposal §6.1 source clause | mechanize_now (as parameter to conditional theorem) |
| `thm:translation-T-forward` | **Theorem T forward**: `A_Z(ζ) = 0 ⟹ RH` (every term nonneg + `m_ρ > 0` + sum 0 ⟹ each `Re(ρ) = 1/2`) | step 448 Stage II forward direction; proposal §5.1 | mechanize_now |
| `thm:translation-T-reverse` | **Theorem T reverse**: `RH ⟹ A_Z(ζ) = 0` (each `Re(ρ) = 1/2` ⟹ `ψ_-(ρ) = 0` ⟹ sum vanishes) | step 448 Stage II reverse direction; proposal §5.2 | mechanize_now |
| `thm:translation-T` | **Theorem T**: `A_Z(ζ) = 0 ⟺ RH` (combination of forward + reverse) | step 448 Stage II; proposal §5; appendix A theorem T | mechanize_now |
| `thm:dc-master-applied` | Duality-confinement application: given the involutive ledger on `Z_ζ^{nt}` + separating readout `ψ_-` + domination records (hypothesis of master theorem), the master theorem yields `A_Z(ζ) = 0` | step 454 P2; proposal §7.1 step 2; appendix A "Duality-confinement application" | mechanize_now |
| `obl:gamma-sdtc-selberg` | `Γ_{SDTC-Selberg}`: structural recognition source asserting domination-records hypothesis obtains as content of formed-layer closure on `Sel^!_{ζ,tr}`. Composite source record (8 fields per proposal §6.2) | proposal §6 (out-of-scope-for-Lean per §11.4 explicit) | out_of_scope_recognition_source |
| `thm:rh-conditional` | **Conditional theorem**: assuming `Γ_{SDTC-Selberg}` supplies the domination records, the landing chain delivers RH. Encoded as: take an explicit `Γ_{SDTC-Selberg}` value as hypothesis parameter; conclude RH (in the form `Re(ρ) = 1/2` for all `ρ ∈ Z_ζ^{nt}`) | step 454 final proof statement; proposal §7.1; appendix A "Conditional theorem" | mechanize_now |

Out-of-scope-for-Lean items in this axis:
- `Γ_{SDTC-Selberg}` (composite recognition source, paper 2's
  analog of hiddenness's `Γ_{CSL-SAT-hidden}`). Encoded as a typed
  structure carrier (`recognitionSource` record with one `Prop` field
  that the conditional theorem takes as an explicit hypothesis
  parameter). The forbidden-tokens rule bans `axiom`/`opaque`/`constant`
  anywhere in `lean/SixBirdsDualityConfinement/*`.
- Six gates + Gate 7 bookkeeping (proposal §B): these are
  metamathematical audit constraints on the proof's source-record
  vs readout discipline. Not Lean-derivable. Recorded in inventory
  with `intended_status = out_of_scope_meta` (alternatively as
  prose-only sections in the paper); no Lean carrier.

## Notes on extraction scope

- **No mathlib.** Per the alignment trio and codex_kickoff.md §4, this
  project is mathlib-free. The "positivity of squared distances" used
  in Theorem T forward is straightforward `Nat`/`Real`-level
  arithmetic; the trace-class machinery from `def:anti-invariant-ledger`
  through `lem:trace-identity` is encoded as a typed structure with
  the trace and norm as fields rather than via mathlib's
  operator-theoretic machinery. Decisions on representation level
  (operator-theoretic vs finite-rank vs purely typed) are made per
  subsection in Phase C; the math artifact records the abstract
  statement, the Lean module records the chosen representation.
- **The master theorem's "trace-class" hypothesis** is treated
  abstractly: the Lean encoding takes `A_X` and `B_n` to be elements
  of an abstract typed-positive cone with a `trace` operation that
  satisfies the monotonicity needed (`A ⪯ B ⟹ tr A ≤ tr B`). This
  avoids depending on full bounded-operator theory.
- **The RH axis's `Z_ζ^{nt}` and `Λ_ζ`** are NOT mechanized as
  actual analytic objects — they appear in the conditional theorem
  as opaque parameters of the right type. The mechanization is the
  forward/reverse direction of Theorem T (which is finite arithmetic
  given a typed `Z_ζ^{nt}` with multiplicities and real parts) and
  the conditional landing chain. The conditional theorem's stated
  conclusion is "every `ρ` in the typed zero ledger has real-part-1/2",
  which is what RH means within this framework.
