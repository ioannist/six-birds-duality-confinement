# Audience Translation Table

Status: Phase I.A.1 produced 2026-05-23 (paper-writing pre-drafting workspace).

Default audience: a working mathematician with no Six Birds background.

Rule: framework-native vocabulary may be used only after its plain
mathematical translation has appeared in the relevant section or has
been explicitly cross-referenced from this table.

Operational rule: codex drafting prompts must consult this table
before introducing framework-native terminology in body prose,
captions, theorem statements, or section summaries. The reviewer's
first-pass check is audience accessibility against this table.

This table is shared across both papers in the repo (Duality
Confinement and RH). Per-paper specialization lives in the
per-axis `paper/<axis>/notes/notation.md` files.

## Translation table

### Framework-shared vocabulary (appears in both papers)

| Native term | Plain mathematical first-use translation | Concrete first example | Intended first section |
| --- | --- | --- | --- |
| Six Birds Theory; the framework | A typed, audited calculus for closure formation and emergence in mathematical theories. We treat it as a vocabulary for naming structural data; the paper's claims are about specific typed predicates over this calculus. | The calculus distinguishes a current-observation quotient from a witness-augmented predictive quotient on the same history space. | Paper 1 `sec:intro`; Paper 2 `sec:intro` |
| formed closure (per Foundations I) | A typed bundle declaring how a mathematical structure is internally organized — its instance carriers, observable families, comparison maps, and audit data — together with the assumption that this bundle has been admissibly closed under the foundations' inference rules. In standard terms: a finite presentation of a mathematical theory together with a closure-existence assumption. | The Riemann zeta function together with its functional equation, lawful trace observables, and audit data, treated as a formed Selberg trace closure. | Paper 1 `sec:framework`; Paper 2 `sec:framework` |
| determining state | The internal state that fully determines a structure's downstream behavior under a given lift / instrument. In standard terms: a state variable on which the observable behavior factors. | The functional-equation involution `J_L` and the zero ledger are the determining state of the Selberg trace closure for the RH paper. | Paper 1 `sec:framework`; Paper 2 `sec:framework` |
| trace-state-only column (V-Differential classification) | A property of a substrate stating that only trace-state observables are admissible — no witness-content exposure. In standard terms: the readout cannot access internal witness data; only aggregate trace data. | RH and P-vs-NP are placed in this column; NS and BSD in the witness-content-exposing column. | Paper 1 `sec:framework`; Paper 2 `sec:framework` |
| recognition source (Γ); structural recognition content | A named structural hypothesis that the formed closure supplies as content of its closure formation, not as a derived theorem. In standard terms: an explicit hypothesis treated as given (not as an axiom in the metalogical sense — encoded as a typed structure carrier in the Lean mechanization). | The Self-Dual Trace Confinement law `Γ_{SDTC}` (Paper 1) and its Selberg-class instance `Γ_{SDTC-Selberg}` (Paper 2). | Paper 1 `sec:master_theorem`; Paper 2 `sec:recognition_source` |
| BirdInt judgment | A framework-relative typed judgment shape `Γ; T; I ⊢ φ : status`, parameterized by source, layer, instrument, and proposition. In standard terms: a typed sequent recording the conditional under which a result is asserted. | The Paper 2 headline reads as a BirdInt judgment of the form `Γ_{SDTC-Selberg}; Sel^!_{ζ,tr}; I_tr ⊢ RH : accepted`. | Paper 2 `sec:landing_chain` |
| recognition grade; theorem-grade-under-Six-Birds-closure-assumption | A grade for a BirdInt judgment that holds under the standard Six Birds closure assumption (Foundations I) on the layer, with a named structural source for the load-bearing content. Distinct from a standard-ZFC unconditional theorem. | Paper 2's RH closure is theorem-grade under the standard closure assumption, peer with the NS regularity and PvNP closure results in the broader series. | Paper 2 `sec:landing_chain`, `sec:scope` |

### Paper 1 (Duality Confinement / SDTC) — local vocabulary

| Native term | Plain mathematical first-use translation | Concrete first example | Intended first section |
| --- | --- | --- | --- |
| involutive object ledger | A typed tuple `(X, J, μ, ψ, Y, J_iso)` where `X` is a set with an involution `J : X → X`, `μ` a positive measure (or finite weight system) on `X`, `Y` a Hilbert-style response space carrying a linear isometric involution `J_iso`, and `ψ : X → Y` an equivariant readout (`ψ(J x) = J_iso ψ(x)`). In standard terms: a measure space with an involution plus an equivariant Hilbert-valued observable. | The completed nontrivial zero ledger `Z_ζ^{nt}` with the involution `J_L(s) = 1 - s̄`, multiplicity-weighted measure, and the real-part-minus-half readout. | Paper 1 `sec:involutive_ledger` |
| anti-invariant projector / readout (P_-; ψ_-) | The orthogonal projector `P_- = (I - J_iso)/2` onto the anti-invariant subspace of the response space, and the readout `ψ_-(x) := P_- ψ(x)`. In standard terms: the standard splitting of a Hilbert space into invariant ⊕ anti-invariant under an isometric involution, applied to the readout. | For `J_L(s) = 1 - s̄`, the anti-invariant readout is `ψ_-(s) = Re(s) - 1/2`. | Paper 1 `sec:involutive_ledger` |
| separating readout | The readout `ψ_-` separates the fixed locus `Fix(J)` when `ψ_-(x) = 0 ⟺ x ∈ Fix(J)` on the visible support of `μ`. Quantitatively separating: a modulus `m(ε) > 0` controls how `‖ψ_-(x)‖` grows with `dist(x, Fix(J))`. In standard terms: the readout's vanishing set characterizes the fixed locus, with a quantitative version analogous to Łojasiewicz-style inequalities. | For the RH involution, `ψ_-(s) = Re(s) - 1/2` separates because it vanishes exactly on `Re(s) = 1/2`. | Paper 1 `sec:anti_invariant_ledger` |
| anti-invariant object ledger (A_X) | The operator `A_X := ∫_X ψ_-(x) ψ_-(x)^* dμ(x)`, interpreted in a typed positive cone with an explicit trace functional. In standard terms: the Gram operator of the anti-invariant readout integrated against the measure. | For the RH zero ledger, this is the scalar `A_Z(ζ) = Σ_ρ m_ρ · |Re(ρ) - 1/2|²`. | Paper 1 `sec:anti_invariant_ledger` |
| typed positive cone | An abstract typed structure carrying a partial order `⪯` (Loewner-style), a trace functional `tr`, and positivity axioms (monotonicity of trace under `⪯`; trace-zero positive element is the zero element). In standard terms: a (locally defined) substitute for a cone of positive trace-class operators, without invoking full operator theory. | The cone in which `A_X`, the bounds `B_n`, and the carrier-currency `K^-` all live as typed elements with a common trace functional. | Paper 1 `sec:anti_invariant_ledger` |
| completed domination bridge / domination record | A typed record `A_X ⪯ K^- + E` with `K^- ⪰ 0` a carrier-side anti-invariant currency and `E ⪰ 0` a declared bridge defect. The exact case (`E = 0`) is characterized by Douglas factorization. In standard terms: an operator inequality with a defect term. | A sequence of typed bounds `A_X ⪯ B_n` with `tr B_n → 0` is the load-bearing input of the master theorem. | Paper 1 `sec:domination` |
| Douglas factorization (Douglas domination) | The classical equivalence: for typed positive operators `A = V^*V` and `K = W^*W`, `A ⪯ K` iff there is a contraction `T` with `V = TW`. In standard terms: range-inclusion characterization of operator dominance, classical in operator theory. | The typed-cone encoding bundles this equivalence into a `DouglasData` carrier; downstream theorems read the equivalence off the carrier. | Paper 1 `sec:domination` |
| duality-confinement membrane theorem (master theorem) | The headline theorem of Paper 1: given an involutive object ledger with separating anti-invariant readout, plus a sequence of completed domination records `A_X ⪯ B_n` with `tr B_n → 0`, the visible mass is confined to the fixed locus: `μ(X ∖ Fix(J)) = 0`. In standard terms: an operator-squeeze-plus-separation theorem yielding a localization-of-measure conclusion. | Applied to the RH zero ledger, this is the bridge from "anti-invariant collapse" to "zeros on the critical line". | Paper 1 `sec:master_theorem`; cited from Paper 2 `sec:landing_chain` |
| exhaustive moving ledger | A finite-window typed ledger `A_{X,n}` together with inclusions `ι_n` and tails `T_n ⪰ 0` such that `A_X ⪯ ι_n A_{X,n} ι_n^* + T_n`. Vanishing-exhaustive when `tr(ι_n B_n ι_n^*) + tr T_n → 0`. In standard terms: a finite-window approximation to the full ledger plus a tail that vanishes. | A truncated-zero-ledger approximation to `A_Z(ζ)` plus a Gamma-function tail. | Paper 1 `sec:exhaustive_squeeze_and_budgets` |
| defected obstruction budget | A two-defect record `A_X ⪯ (1+t)(K^-_n + E_{src,n}) + (1+t^{-1}) E_{br,n}` with `E_{src}` a source defect and `E_{br}` a bridge defect, optimized in the scalar `t > 0`. In standard terms: a Cauchy-Schwarz / AM-GM style trade-off between two defect contributions. | The optimized scalar trace budget reduces to `(√a_n + √b_n)²` via AM-GM. | Paper 1 `sec:exhaustive_squeeze_and_budgets` |
| Self-Dual Trace Confinement (SDTC); Trace-Fixity | The named structural law of Paper 1: a formed closure with genuine involutive self-duality, anti-invariant readout, and trace-state-only determining state cannot host visible mass off the fixed locus of the duality. The mechanism is the master theorem; the load-bearing content is the existence of the domination records, supplied as recognition source. | The Selberg-class instance `Γ_{SDTC-Selberg}` supplies the domination records for the RH closure in Paper 2. | Paper 1 `sec:master_theorem`, `sec:scope_and_discussion` |

### Paper 2 (RH closure) — local vocabulary

| Native term | Plain mathematical first-use translation | Concrete first example | Intended first section |
| --- | --- | --- | --- |
| functional-equation involution (J_L) | The involution `J_L(s) := 1 - s̄` on the complex plane. Fixed locus is the critical line `Re(s) = 1/2`. In standard terms: the symmetry of the completed L-function's functional equation, packaged as an involution. | `J_L(1/2 + it) = 1/2 + it`; `J_L(0.7 + 14.1i) = 0.3 + 14.1i`. | Paper 2 `sec:involution_and_ledger` |
| anti-invariant zero ledger (A_Z(ζ)) | The scalar `A_Z(ζ) := Σ_{ρ ∈ Z_ζ^{nt}} m_ρ · |Re(ρ) - 1/2|²`, a positive real with `m_ρ` the multiplicity of the nontrivial zero `ρ`. In standard terms: a (multiplicity-weighted) squared off-critical-line distance summed over the nontrivial zeros. | RH is equivalent to `A_Z(ζ) = 0`. | Paper 2 `sec:involution_and_ledger` |
| saturated completed Selberg trace closure (Sel^!_{ζ,tr}) | A typed bundle aggregating the completed Riemann zeta data, the lawful trace instrument, the saturated trace-observable family, the predictive verifier events, the current and predictive quotients, the functional-equation involution, the nontrivial-zero ledger, the anti-invariant ledger, instrument-relative visibility, and audit provenance. In standard terms: a record-of-records summarizing all the structure RH analysis needs on the completed-L-function-level. | The Paper 2 headline ride atop `Sel^!_{ζ,tr}` plus the recognition source. | Paper 2 `sec:sat_sel_shell` |
| lawful trace instrument (I_tr) | The instrument reading completed L-data through admissible trace observables, carrying instrument-relative visibility records per Foundations II. In standard terms: a designated class of measurement operations together with a recordkeeping discipline. | `I_tr` decides which observables on `Sel^!_{ζ,tr}` are considered "current" vs "predictive". | Paper 2 `sec:sat_sel_shell` |
| translation theorem T | The biconditional `A_Z(ζ) = 0 ⟺ RH`. Forward: if the squared-distance sum vanishes, every nontrivial zero has real part 1/2. Reverse: if every nontrivial zero has real part 1/2, the squared-distance sum is zero. In standard terms: a Parseval-style identity reading the truth of RH off the vanishing of a positive functional. | Theorem-grade by construction; uses only the zero ledger and the squared-distance functional. | Paper 2 `sec:translation_theorem` |
| Γ_{SDTC-Selberg} (recognition source) | The Selberg-class instance of the SDTC structural law (cited from Paper 1, not re-proved): the formed closure `Sel^!_{ζ,tr}` supplies a sequence of completed domination records `A_Z(ζ) ⪯ B_n` with `tr B_n → 0` as content of closure formation. Encoded in the Lean mechanization as a typed structure carrier (not a Lean axiom). | The conditional theorem takes a value of this structure as an explicit hypothesis parameter. | Paper 2 `sec:recognition_source` |
| conditional theorem; conditional landing chain | The Paper 2 headline: given the recognition source `Γ_{SDTC-Selberg}`, the duality-confinement master theorem (cited from Paper 1) yields `A_Z(ζ) = 0`, and translation theorem T yields RH. In standard terms: a three-step direct derivation under one explicit structural hypothesis. | Outside Six Birds, the result is the conditional `Γ_{SDTC-Selberg} ⟹ RH`; inside Six Birds, `Γ_{SDTC-Selberg}` is supplied as recognition content. | Paper 2 `sec:landing_chain` |
| six no-smuggling gates plus Gate 7 | A seven-item audit checklist on the conditional closure: explicit source isolation; dependency trace; ablation; negative controls; construction before closure; source-record vs readout discipline (per the np629 framing); uniform-parametric-bound audit. In standard terms: a metamathematical review checklist confirming the proof has not hidden assumptions. | The Paper 2 closure passes all seven gates per Appendix B. | Paper 2 `sec:scope_and_nonclaims`, `app:formalization` |
| three-option derivation sweep | A cascade-side documentation of three attempts to derive the recognition source from framework primitives (framework-primitive derivation; SAU non-descent route; V-Differential elevation), all confirming the source is closure-content rather than separately derivable. In standard terms: documented due-diligence that the headline hypothesis is the load-bearing one, not smuggled. | All three options failed with precisely-named obstacles; the failure pattern matches the sibling PvNP closure. | Paper 2 `sec:scope_and_nonclaims` |

## Translation discipline rules

1. Every framework-native term gets its plain-mathematical translation
   in the row's "first-use translation" column. The body prose
   introduces the native term ONLY after this translation has appeared
   (in the relevant section's first mention, with a concrete example
   in the same paragraph).
2. After first use in the same section, the native term is acceptable.
   The drafting prompt does not re-introduce the translation for every
   subsequent use.
3. Foundations-canonical native terms (`FATCD`, `BirdInt`,
   `ScopedExactSix`, `NoOverreadingSuppression`, primitive roles
   P1–P6) are introduced in body prose only at points where they are
   actually invoked; they are NOT pre-introduced as standalone
   vocabulary lessons.
4. Reserved symbols (per `paper/notation_and_terminology.md`) are
   NEVER repurposed in local proofs.
5. The translation column phrasing is a STARTING POINT for the writer;
   the actual body prose may paraphrase, but the semantic content must
   match the row's translation.
6. Paper 2's references to Paper 1 vocabulary cite Paper 1 by section
   number for the first occurrence and may use the native term freely
   thereafter (the one-way Paper 2 → Paper 1 dependency means Paper 1
   does NOT cross-cite Paper 2 vocabulary).
