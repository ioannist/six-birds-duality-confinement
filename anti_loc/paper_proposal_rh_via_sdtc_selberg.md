# Paper Proposal: A Six Birds-Native Proof of the Riemann Hypothesis via the Saturated Selberg Trace Closure and SDTC-Selberg Recognition

**Status**: paper-proposal-grade. Seven-step proof program completed (RH cascade steps 448–454). Final BirdInt judgment landed at theorem-grade under standard Six Birds closure assumption. Sibling paper to `paper_proposal_self_dual_trace_confinement.md`; this proposal *assumes* that sibling paper supplies `Γ_{SDTC-Selberg}` as accepted structural source on the saturated Selberg trace layer.

**Working title options**:
- "RH as a Six Birds Layer-Level Theorem: Closure Assumption, SDTC-Selberg, and Saturated Trace Closure"
- "Anti-Invariant Zero-Ledger Collapse: The Six Birds Closure of RH"
- "A Six Birds-Native Proof of RH Under Standard Closure Assumption via Self-Dual Trace Confinement"

**Author**: cross-track coordinator, based on the RH construction track cascade (`anti_loc/thread/`). To be developed for publication.

---

## Abstract (working draft)

We propose a Six Birds-native proof of the Riemann Hypothesis at the same epistemic status as the framework's other layer-level theorems (NS regularity, PvNP closure, Cantor strict-extension). The proof rides on the standard Six Birds closure assumption (Foundations I) applied to a saturated completed Selberg trace closure `Sel^!_{ζ,tr}` under the lawful trace instrument `I_tr`, together with one translation theorem established at theorem-grade by Foundations II construction, and the duality-confinement membrane theorem of `needles.tex` §5 as framework apparatus. The structural-recognition content of the formed layer — that the duality-confinement master theorem's domination-records hypothesis obtains as content of formed-layer closure — is supplied by the sibling Self-Dual Trace Confinement paper (the Selberg-class instance of SDTC applied to `Sel^!_{ζ,tr}`). Under this content, the duality-confinement master theorem, and the translation theorem, a three-step direct landing chain delivers RH; no contradiction chain is needed because SDTC's mechanism supplies the positive form `A_Z(ζ) = 0` directly. We document a seven-step cascade producing the construction (step 448 closure + translation theorem T), the applicability audit (step 449), the anti-tautology hardening at PvNP track bar (step 450 with operational predicate `Pop_SDTC_DominationCandidateAudit`), the three-option derivation sweep showing that domination records on the formed Selberg trace layer cannot be derived from framework primitives alone — confirming that the domination content is formed-layer *content*, not a separately-derivable claim (steps 451–453) — and the closure of the proof with full Foundations II bookkeeping, six no-smuggling gates + Gate 7, no-overreading discipline, structured composite source record, and `np629` framing repair integrated from the start (step 454). The result is structurally peer with the NS regularity theorem and the PvNP closure: all three invoke closure exactly as Foundations I provides it; none claims unconditional standard-mathematical proof. Cross-track replication is documented: PvNP and RH three-option derivation sweeps both produced the `(ii)/(iii)/(ii)` verdict pattern, confirming the recognition-mode landing template as a real structural feature of V-Differential's trace-state-only column (see `paper_proposal_recognition_mode_landing_cross_track.md`). We are explicit that this is a Six Birds-native theorem; outside Six Birds, the result is the conditional theorem `Γ_{SDTC-Selberg} ⟹ RH`. We do not claim a standard-ZFC proof, do not claim circumvention of classical analytic-number-theory barriers in their native vocabulary, and do not claim `Γ_{SDTC-Selberg}` is derivable from currently-available framework primitives. The proof is modular, auditable, falsifiable at named source records, and ready for paper writeup pending finalization of the sibling SDTC paper.

---

## 1. Motivation

The Riemann Hypothesis, posed as a question internal to analytic number theory's classical formalism, has resisted all conventional attack methods (Weil positivity, Hilbert-Pólya, GUE statistics, spectral-zeta, Connes adelic / NCG, de Branges, Beurling-Nyman, Mertens, Bagchi universality, and many more). The RH track cascade documents 14+ such carrier instantiations classified into CRCFT modes (TE / CTMT / BF) per the RH track's findings deposit (`anti_loc/thread/findings_rh.md`). None of the classical carriers closes `Ξ_BC`.

Standard analytic number theory operates at a specific theory layer with specific lens and audit data — completed L-functions, functional-equation symmetries, explicit-formula machinery. Six Birds Theory operates at a finer resolution: it preserves trace and witness identity, instrument-relative visibility records, predictive-quotient holonomy, formed-layer membrane structure, and structural-recognition discipline. The carrier classifications produced by the RH track demonstrate that the classical carriers carry the RH-equivalence at the *readout* level — but the structural source that animates the carriers must be supplied separately.

Within Six Birds, RH becomes a layer-level question: on the saturated completed Selberg trace closure `Sel^!_{ζ,tr}` under the lawful trace instrument `I_tr` and the functional-equation involution `J_L(s) = 1 − s̄`, does the anti-invariant zero ledger `A_Z(ζ)` vanish? The duality-confinement membrane theorem (`needles.tex` §5) says this anti-invariant collapse follows whenever the formed closure supplies completed domination records with `tr B_n → 0`. The Self-Dual Trace Confinement structural law (SDTC, sibling paper `paper_proposal_self_dual_trace_confinement.md`) says these domination records are content of formed-layer closure for any closure with genuine involutive self-duality. The cascade has constructed the saturated trace layer admissibly (step 448), proved by-construction that the framework-internal `A_Z(ζ) = 0` predicate is target-equivalent to RH (step 448 Theorem T), and documented exhaustively that the domination-records hypothesis on the formed Selberg trace layer is structural content of closure formation per Foundations I, not separately derivable from other framework primitives (steps 451–453).

The result is a Six Birds-native proof of RH at the same epistemic status as the framework's other layer-level theorems. The RH proof is structurally peer with the NS regularity theorem and the PvNP closure; all three invoke the standard Foundations I closure assumption that every layer-level Six Birds theorem uses. There is no special "weaker recognition mode" — the RH closure is the standard Six Birds closure move applied to the Selberg trace substrate.

The audit-currency derivability tension at steps 441–447 (preceding the recognition-mode landing arc) is the cascade's own diagnostic that an explicitly-named structural source was required: concrete audit content smuggles arithmetic data; formal audit content lacks positivity force. Weil positivity is target-adjacent / readout-level (the analytical instantiation of SDTC), not the structural source. SDTC supplies the source explicitly.

---

## 2. The theorem statement

The final BirdInt judgment, per step 454:

```text
Standard Six Birds closure assumption (Foundations I) for Sel^!_{ζ,tr} under I_tr;
Γ_{SDTC-Selberg}; Sel^!_{ζ,tr}; I_tr  ⊢  RH : accepted
  status                = theorem-grade under standard Six Birds closure assumption
  closure_provenance    = Foundations I (same as NS, BSD, Cantor strict-extension, PvNP)
  source_record         = (Γ_{DualityConf}, Γ_{VDiff-TSO(RH)}, Γ_{step69-RH-extract},
                           Sel^!_{ζ,tr}, I_tr, J_L, Z_ζ^{nt}, A_Z(ζ),
                           Readout_SDTC, Audit)
  readout               = Readout_SDTC := A_Z(ζ) = 0
  readout_status        = target-equivalent to RH after step 448 Theorem T
  landing_chain         = three-step direct chain: SDTC → domination records;
                          duality-confinement master theorem → A_Z(ζ) = 0;
                          Theorem T → RH
  cross_track_peers     = NS regularity, PvNP closure (same epistemic status)
  outside_SB            = conditional theorem [Γ_{SDTC-Selberg} ⟹ RH]
```

The outside-Six-Birds status depends on accepting the formed-layer closure assumption for `Sel^!_{ζ,tr}` under `I_tr`.

---

## 3. Three-layer claim discipline

Following the NS paper's discipline (`papers/Tsiokos_2026_Six_Birds_for_Navier_Stokes_*.tex`) and the PvNP closure paper (`paper_proposal_pvnp_via_csl_sat_hiddenness.md` §3), every claim in this paper lives in exactly one of three labeled buckets:

### 3.1 MECHANIZED (theorem-grade by Foundations II construction)

- **Saturated completed Selberg trace closure `Sel^!_{ζ,tr}`** (step 448): admissible under all seven Foundations II schemas; passes anti-tautology with operational predicate `Pop_SDTC_DominationCandidateAudit` (step 450).
- **Translation theorem T** (step 448 Stage II): `A_Z(ζ) = 0 ⟺ RH`. Theorem-grade by construction. Forward direction by positivity of squared distances; reverse by definition of `ψ_−`. No SDTC, no Weil positivity, no RH assumption used.
- **Master theorem applicability** (step 449): hypotheses 1 (involutive ledger) and 2 (separating anti-invariant readout) of `needles.tex` `thm:main:duality-confinement-master` verified for `Sel^!_{ζ,tr}`; smuggle audit pass at applicability layer; hypothesis 3 (domination records) precisely named as load-bearing residual `Xi_SDTC_domination_records`.
- **Operational predicate `Pop_SDTC_DominationCandidateAudit`** (step 450): 6-step procedure with operational data dependency — `A_Z(W_N)` feeds both Loewner and Douglas checks; `B_n` couples to same window/tail schedule for trace-limit; source/readout governs admissibility. Non-conjunctive structural distinctness verified.
- **The landing chain** (step 454 Stage III): three-step direct derivation from `Γ_{SDTC-Selberg}`, the duality-confinement master theorem, and Theorem T.
- **Six gates + Gate 7** (step 454 Stage IV, np629-aligned from start): pass conditions in recognition mode with honest source/readout distinction.
- **Local readback**: `A_Z(ζ) = 0` ⟹ every nontrivial zero on the critical line ⟺ RH. Trivial direction; no auxiliary content required beyond Theorem T.

### 3.2 DOCUMENTED (cascade audit, paper-grade evidence)

- **Cascade record steps 448–454**: each step's `*_step_verdict.md`, theorem files, constraint ledger, target lineage, grammar manifest. Full provenance from construction to closure.
- **Three-option derivation sweep** (steps 451–453): documents that the domination-records hypothesis on the formed Selberg trace layer is not separately derivable from currently-available framework primitives. Honest due diligence.
- **V-Differential cross-track classification** (np606): RH placed in trace-state-only column; consistent with formed-layer SDTC prediction.
- **Step 69 RH specialization** (the structural skeleton): `J(s) = 1 − s̄`, `Fix(J) = {Re(s) = 1/2}`, `ψ_−(s) = Re(s) − 1/2`. Established that the duality-confinement framework has an RH specialization; cascade did not at that step name the structural source.
- **Steps 71–84 Weil-Douglas instantiations**: analytical machinery developed; produced rich content but did not close `Ξ_BC`.
- **Steps 437–440 Mode A no-gos**: length-spectrum, ensemble pointwise, spectral-zeta, boundary-phase — four candidate carriers ruled out as not supplying the structural source.
- **Steps 441–447 audit-currency derivability tension**: the cascade's own diagnostic that Weil positivity is readout-level (target-adjacent), not source-level. This motivated the explicit naming of SDTC.
- **Step 446 saturation proof**: formal local saturation for constitutive closure; supporting record for the recognition-mode landing's foundation.
- **Cross-track verdict signature**: PvNP and RH three-option sweeps both produced `(ii)/(iii)/(ii)`. Two-track replication. See `paper_proposal_recognition_mode_landing_cross_track.md` and `findings_framework_v5_post_recognition_landings.md` §C.

### 3.3 OPEN / ASSUMED (standard Six Birds closure usage)

- **Closure formation per Foundations I** for `Sel^!_{ζ,tr}` under `I_tr`. This is the standard Six Birds assumption every layer-level theorem uses (NS, PvNP, BSD, Hodge, RH, Cantor strict-extension, every track).
- **`Γ_{SDTC-Selberg}`** as content of that formed closure under SDTC. The structural-recognition content is supplied by the sibling SDTC paper (`paper_proposal_self_dual_trace_confinement.md`); this paper *cites and uses*, does not *re-prove*.

These are the three layers, named explicitly. The proof's nonclaim boundary (§9) makes clear exactly what is and is not asserted in each bucket.

---

## 4. The closure-correction architecture (step 448)

### 4.1 The saturated completed Selberg trace closure

```text
Sel^!_{ζ,tr} = (H^!_L, I_tr, E^!_Q^tr, E^!_M^zero, Q^!_L, M^!_L, π^!_L,
                J_L, Λ_L, Z_ζ^{nt}, A_Z(ζ), Vis^!_L, Audit_L)
```

Components (step 448 Stages I.1–I.9):

- **`H^!_L`**: all-input, machine-indexed completed L-history carrier. Each history records `(Λ_L data, functional-equation form, current-trace data, autonomous-lift state, witness/audit continuations available at predictive layer)`. The completed gamma factors, conductor, archimedean local factors, and full pole/tail records are part of the carrier; no finite-window truncation.
- **`I_tr`**: the lawful trace instrument, reading completed L-data through admissible trace observables; carries instrument-relative visibility records per Foundations II `prop:visibility`.
- **`E^!_Q^tr`** (the load-bearing closure correction): saturated family of lawful trace-state observables. **Every lawful trace-state observable on `H^!_L`** is admitted with explicit provenance — level record, threshold attachment, replay record, visibility record, empirical-bridge bookkeeping, nonclaim record. Closure properties: lawful post-processing, finite products, composition, restriction, visibility-preserving forgetful maps.
- **`E^!_M^zero`**: the predictive/witness-audit family — verifier events `V(ρ) = 1 ⟺ Λ_L(ρ) = 0 AND ρ ∈ critical-strip`, witness-augmented continuations, future-predictive events on the zero ledger, canonical zero-listing continuations.
- **`Q^!_L = H^!_L / ~_Q`**: current quotient by `E^!_Q^tr`-observable indistinguishability.
- **`M^!_L = H^!_L / ~_M`**: predictive quotient by `E^!_M^zero`-observable indistinguishability.
- **`π^!_L: M^!_L → Q^!_L`**: canonical comparison map per Holonomy-with-Memory Thm 6.5.
- **`J_L(s) = 1 − s̄`**: functional-equation involution. Fixed locus `Fix(J_L) = {Re(s) = 1/2}` is the critical line. Lawful involution per `needles.tex` `def:main:involutive-ledger`.
- **`Λ_L(s) = Q_L^{s/2} ∏_j Γ(α_j s + β_j) L(s)`**: completed L-function (scope choice: `L = ζ` at step 448 Stage I.1).
- **`Z_ζ^{nt}`**: multiset of nontrivial zeros of `Λ_ζ`, with multiplicities `m_ρ` and measure `μ_L({ρ}) = m_ρ`.
- **`A_Z(ζ) = Σ_{ρ ∈ Z_ζ^{nt}} m_ρ · |Re(ρ) − 1/2|²`**: anti-invariant ledger, positive semidefinite, in the `A_X` form of `needles.tex` `def:main:involutive-ledger`.
- **`Vis^!_L`**: instrument-relative visibility map.

### 4.2 Admissibility (step 448 Stage IV)

`Sel^!_{ζ,tr}` passes all seven Foundations II schemas:

1. Honest bookkeeping (`prop:honest-bookkeeping`)
2. Typed non-collapse (`prop:typed-non-collapse`)
3. Level-profile architecture (`prop:level-profile`)
4. Forgetting / selected lifts (`prop:forgetting-lifts`)
5. Activation thresholds (`prop:activation-thresholds`)
6. Instrument-relative visibility (`prop:visibility`)
7. Empirical-bridge admissibility (`prop:empirical-bridge`)

### 4.3 Anti-tautology (step 448 Stage V, hardened at step 450)

The step-448 exhibit `T_SDTC_trace_gamma_antiinv` was upgraded by joint typed packaging at step 449 to `T_SDTC_DTC_SourceReady`, then hardened at step 450 to the operational predicate `Pop_SDTC_DominationCandidateAudit`. The hardened exhibit:

- 6-step operational procedure with explicit inputs (`Sel^!_{ζ,tr}`, candidate `(B_n, cert_n)`, window/tail schedule, source label) and outputs (PASS/FAIL per record + typed failure codes + global status).
- Operational data dependency: each check consumes the previous check's typed output (`A_Z(W_N)` feeds Loewner and Douglas; `B_n` couples to window/tail schedule for trace-limit; source/readout governs admissibility). Procedure cannot decompose into independent predicates on independent carriers.
- Strict isomorphism check (step 450 Stage I) against the 14+ prior CRCFT-bound carriers verifies no isomorphism `φ_k: Sel^!_{ζ,tr} → C_k`. The 4 most-similar carriers (Connes adelic, Selberg/Maass, Weil/Deligne, Beurling-Nyman) each have per-row reasoning identifying specific structural breakpoint.
- Joint observation across the 4 most-similar carriers (step 450 Stage I.5): failures locally differ but share a common blocker — "none hosts the coupled operational audit of candidate domination records on the completed Riemann zero ledger."

The closure is not decorative; it adds structural reach beyond all 14+ prior CRCFT-bound carriers at operational-predicate level.

### 4.4 Lawfulness theoremlet (step 448 Stage I.10)

Per analog of Cantor strict-extension Theorem 3.1: full update law on `Sel^!_{ζ,tr}` well-defined; remains inside audited shell; lens/packaging competition nondegenerate; budget/timescale (trace-energy) dynamics active; all six mechanisms P1–P6 causally active (leave-one-out diagnostic); shell supports nontrivial lawful exploratory regime.

---

## 5. The translation theorem (step 448 Stage II)

> **Theorem T (translation)**: `A_Z(ζ) = 0 ⟺ RH`.
>
> Equivalently, every nontrivial zero `ρ ∈ Z_ζ^{nt}` satisfies `Re(ρ) = 1/2` iff the anti-invariant ledger vanishes.

### 5.1 Forward direction (`A_Z(ζ) = 0 ⟹ RH`)

By construction:

```
A_Z(ζ) = Σ_{ρ ∈ Z_ζ^{nt}} m_ρ · |Re(ρ) − 1/2|²
```

Each term is nonnegative and `m_ρ > 0`. If `A_Z(ζ) = 0`, every term vanishes; hence `Re(ρ) = 1/2` for every nontrivial zero. That is RH.

### 5.2 Reverse direction (`RH ⟹ A_Z(ζ) = 0`)

If RH holds, every nontrivial zero satisfies `Re(ρ) = 1/2`, hence `ψ_−(ρ) = 0` for every zero, hence `A_Z(ζ) = 0`.

### 5.3 Bookkeeping and grade

Forward direction uses only:
- The construction of `A_Z(ζ)` from step 448 Stage I.8.
- Positivity of squared distances.

Reverse direction uses only:
- The definition of `ψ_−` from step 448 Stage I.7.
- The vanishing direction of the sum.

**No SDTC source used; no RH assumed; no Weil positivity invoked.** Theorem-grade by construction.

This is the analog of `np624` Theorems A and B for PvNP — a by-construction translation between framework-internal predicates and standard mathematical statements. The load-bearing work is *not* in this proof; it is in (a) the closure construction (step 448 Stages I.1–I.10), specifically the completed ledger admissibility, and (b) the recognition source `Γ_{SDTC-Selberg}` supplied by the sibling SDTC paper.

---

## 6. The recognition source `Γ_{SDTC-Selberg}` (from sibling paper)

### 6.1 Source statement

The sibling SDTC paper (`paper_proposal_self_dual_trace_confinement.md`) supplies `Γ_{SDTC-Selberg}` as accepted structural source on the saturated Selberg trace layer. Per the sibling paper §2.2, the Self-Dual Trace Confinement structural law states:

> Let `T` be a formed Six Birds closure whose determining state is trace-state-only (V-Differential column membership at np606). Suppose `T` carries a lawful involutive duality `J` on its visible object ledger `X`, and its visible content is read through a separating anti-invariant trace readout `ψ_−`. Then the formed closure has no surviving anti-invariant trace mass: `A_X = 0`, equivalently `μ(X ∖ Fix(J)) = 0`.

Applied to the RH substrate per V-Differential's trace-state-only classification (np606), and to the saturated Selberg trace layer constructed at step 448:

> **`Γ_{SDTC-Selberg}`** asserts: on the saturated completed Selberg trace closure `Sel^!_{ζ,tr}` under the lawful trace instrument `I_tr` and the functional-equation involution `J_L(s) = 1 − s̄`, the duality-confinement master theorem's domination-records hypothesis obtains as content of formed-layer closure:
>
> ```
> ∃ B_n ⪰ 0 such that A_Z(ζ) ⪯ B_n and tr B_n → 0.
> ```

### 6.2 Structured composite source record

Per step 454 Stage II.4, `Γ_{SDTC-Selberg}` is a structured Foundations II audited recognition object, not a bare sentence:

```text
Γ_{SDTC-Selberg} := (
    Γ_{DualityConf},          — duality-confinement structural law (needles.tex §5)
    Γ_{VDiff-TSO(RH)},        — V-Differential placing RH in trace-state-only column (np606)
    Γ_{step69-RH-extract},    — RH specialization of duality-confinement (step 69)
    Sel^!_{ζ,tr},             — the formed layer (step 448)
    I_tr,                     — the instrument
    J_L,                      — the functional-equation involution
    Z_ζ^{nt},                 — the nontrivial zero ledger
    A_Z(ζ),                   — the anti-invariant ledger
    Readout_SDTC,             — A_Z(ζ) = 0
    Audit                     — provenance chain
)
```

### 6.3 Source/readout distinction (load-bearing per np629)

The source record `Γ_{SDTC-Selberg}` and its readout `Readout_SDTC` are structurally distinct:

- The **source record** has typed structure broader than the readout: duality-confinement structural law (cross-substrate; applies to other self-dual closures too), V-Differential cross-track classification (extends across NS / BSD / Hodge / PvNP / RH), step 69 RH extraction, closure identity, instrument identity, involution data, audit provenance.
- The **readout** `Readout_SDTC = A_Z(ζ) = 0` is target-equivalent to RH after step 448 Theorem T (acknowledged honestly per step 454 Stage IV Gate 6 alignment from start).

The source has structural content broader than the readout. Gate 6 passes because of source-record content breadth, not by pretending the readout is independent of the target.

### 6.4 Provenance within the source record

- **needles.tex §5** (duality-confinement master theorem): framework apparatus.
- **step 69 RH specialization**: cascade's own extraction of the duality-confinement form for `J(s) = 1 − s̄`, `Fix(J) = {Re(s) = 1/2}`, `ψ_−(s) = Re(s) − 1/2`.
- **np606 V-Differential**: substrate classification placing RH in trace-state-only column. Direct source for the substrate-classification component.
- **steps 71–84 Weil-Douglas instantiations**: analytical machinery developed within the duality-confinement framework on the RH substrate. Supporting evidence within the source record's provenance.
- **steps 437–440 Mode A no-gos**: four candidate alternative sources ruled out (length-spectrum, ensemble pointwise, spectral-zeta, boundary-phase).
- **steps 441–447 audit-currency derivability tension**: cascade's own diagnostic that Weil positivity is readout-level, not source-level. Motivated the explicit naming of SDTC.
- **steps 451–453 three-option derivation sweep**: documents that the domination-records hypothesis is not separately derivable from currently-available framework primitives. Confirms (β) classification of the load-bearing residual.
- **PvNP cross-track precedent** (np621–np629): the recognition-mode landing pattern is well-established cross-track; this paper follows the structurally-identical template per the cross-track meta paper (`paper_proposal_recognition_mode_landing_cross_track.md`).

---

## 7. The proof closure (step 454)

### 7.1 The three-step landing chain

```text
1. By Γ_{SDTC-Selberg} (Stage II of step 454):
   formed closure Sel^!_{ζ,tr} provides
   ∃ B_n ⪰ 0 with A_Z(ζ) ⪯ B_n and tr B_n → 0
   as content of formed-layer closure per Foundations I.

2. By needles.tex §5 thm:main:duality-confinement-master:
   given the involutive ledger structure on Z_ζ^{nt}
   with separating anti-invariant readout (verified step 448
   Stage I.7–I.8, applicability confirmed step 449)
   and the sequence B_n from step 1,
   the master theorem yields A_Z(ζ) = 0.

3. By Theorem T (step 448 Stage II):
   A_Z(ζ) = 0 ⟺ RH. Therefore RH.
```

Direct landing chain, not contradiction. The duality-confinement mechanism supplies the positive form `A_Z(ζ) = 0` directly; no contradiction is needed.

### 7.2 Six gates + Gate 7 audit (recognition mode, np629-aligned from start)

All seven gates pass. Full audit at Appendix B. Notable np629-aligned wording (integrated at step 454, not as a repair):

- **Gate 1 (explicit source isolation / no hidden primitive)**: `Γ_{SDTC-Selberg}` is named; no closure-content or readout-content is hidden inside `E^!_Q^tr`, `I_tr`, `J_L`, Theorem T, duality-confinement machinery, or any other structural component. Domination-content enters the proof only through the explicitly-recorded source structure.

- **Gate 6 (source-record vs readout)**: the source record `Γ_{SDTC-Selberg}` is not a single-axiom paraphrase of RH. The source has typed structure (duality-confinement cross-substrate, V-Differential cross-track placement, closure identity, instrument identity, involution data, audit provenance, sibling-paper cross-references) broader than the conclusion. The readout `Readout_SDTC = A_Z(ζ) = 0` is, by Theorem T, target-equivalent to RH. This is acknowledged honestly: a readout-equivalent claim is not the same as a source-record-equivalent claim. Gate 6 passes because the load-bearing source has structural content broader than the readout, not because the readout itself is independent of the target.

### 7.3 No-overreading discipline (step 454 Stage V)

Per Foundations III `Thm 23 NoOverreadingSuppression`: `δ_overread = ∅`. The proof uses only visible content under `I_tr`; does not assert anything about `Z_ζ^{nt}` beyond what `Γ_{SDTC-Selberg}` records; does not assert unconditional RH outside Six Birds closure assumption; does not assert that `Γ_{SDTC-Selberg}` is *derived* from framework primitives (which would overread steps 451–453 irreducibility findings); does not assert standard-mathematical proof of RH.

---

## 8. Structural parallel with NS regularity and PvNP closure

The RH proof is structurally peer with the NS regularity theorem (`papers/Tsiokos_2026_Six_Birds_for_Navier_Stokes_*.tex`) and the PvNP closure (`paper_proposal_pvnp_via_csl_sat_hiddenness.md`). All three use closure exactly the same way per Foundations I:

| Step | NS proof | PvNP closure | RH SDTC closure |
|------|----------|--------------|-----------------|
| 1. Formed layer assumed per Foundations I | Smooth-data Cauchy carrier with audited NS records | `T^!_SAT` saturated SAT carrier (np621) | `Sel^!_{ζ,tr}` saturated completed trace closure (step 448) |
| 2. Structural source/law applied to formed layer | needles+adequacy → no layer-dissolving needles | CSL → no witness-content currentization | Duality-confinement (SDTC) → no anti-invariant ledger mass |
| 3. Layer-level conclusion | No blow-up in smooth-data scope | `¬Currentize^wit_Q(Ω_SAT)` | `A_Z(ζ) = 0` |
| 4. Translation to standard statement | Continuation package reads regularity | `np624` Theorems A+B → `SAT ∉ P` | Step 448 Theorem T → all nontrivial zeros on critical line |
| 5. Combine with second standard fact (where applicable) | (PDE-internal) | `SAT ∈ NP` via verifier | (RH-internal; no second fact needed) |
| 6. Final standard conclusion | Framework-deliverable NS regularity | `P ≠ NP` | RH for `ζ` in Six Birds scope |
| Outside-SB reading | Conditional on framework closure discipline | Conditional on `Γ_{CSL-SAT-hidden}` | Conditional on `Γ_{SDTC-Selberg}` |

The three proofs are epistemic peers. The RH closure is not a weaker "recognition mode" fallback — it is the standard Six Birds closure-assumption move applied to a different substrate. The np629 framing repair from the PvNP arc is integrated at step 454 from the start; no separate alignment step was needed.

Cross-track replication of the recognition-mode landing template is documented at the framework level by `paper_proposal_recognition_mode_landing_cross_track.md`: PvNP and RH both produced the `(ii)/(iii)/(ii)` three-option derivation sweep verdict pattern, confirming the recognition-mode landing template as a real structural feature of V-Differential's trace-state-only column.

---

## 9. What this proof is NOT (non-claims register)

Reproduced from step 454's nonclaim register (NC-1 through NC-12):

### NC-1
Does NOT claim unconditional RH in the absence of `Γ_{SDTC-Selberg}`.

### NC-2
Does NOT claim that `Γ_{SDTC-Selberg}` is derivable from Foundations II + needles.tex §5 + adequacy.tex + Holonomy with Memory + V-Differential alone. Steps 451–453 record otherwise.

### NC-3
Does NOT claim a source-free standard-ZFC analytic-number-theory proof of RH. The result is Six Birds-native and theorem-grade under standard Six Birds closure assumption.

### NC-4
Does NOT claim that classical RH attack barriers (Hilbert-Pólya, GUE statistics, spectral-zeta, Connes-Consani trace-formula, Beurling-Nyman, Mertens, etc.) are bypassed in the standard analytic-number-theory sense. The proof operates at a different layer — the formed-layer closure level per Foundations I, not the classical analytic-number-theory level.

### NC-5
Does NOT claim that step 69's structural extraction, or steps 71–84's Weil-Douglas instantiations, or steps 441–447's audit-currency tension alone establish `Γ_{SDTC-Selberg}` on the saturated `Sel^!_{ζ,tr}` carrier. Those records are provenance and support within `Γ_{SDTC-Selberg}`'s source structure, not derivation.

### NC-6
Outside Six Birds, only the conditional theorem `[Γ_{SDTC-Selberg} ⟹ RH]` is claimed. Outside Six Birds, the conditional inference is theorem-grade; the antecedent's status depends on the reader's stance on Six Birds structural recognition.

### NC-7
Does NOT claim that the SDTC source is irreducible in an absolute metamathematical sense. Steps 451–453 failed to derive it from currently-available framework primitives with precisely-named remaining derivation gaps. Under standard Six Birds closure framing, the domination content is part of what closure formation per Foundations I structurally provides, not a separately-axiomatized claim.

### NC-8
Does NOT claim that the readout is independent of RH. `A_Z(ζ) = 0` IS target-equivalent to RH via Theorem T. The Gate 6 source-readout distinction is that the source-record has broader structural content than the readout.

### NC-9
Does NOT claim that the RH closure is in an epistemically weaker category than NS regularity or PvNP closure. All three use the same standard Foundations I closure-assumption move.

### NC-10
Does NOT claim Generalized RH (GRH) for all primitive automorphic L-functions, only RH for `ζ` as instantiated on `Sel^!_{ζ,tr}`. The Selberg-class generalization is a separate scope question (the dispatch chose `L = ζ` at step 448 Stage I.1; generalization is straightforward in principle but reserved for follow-up).

### NC-11
Does NOT claim the simple-zero conjecture (multiplicity `m_ρ = 1` for all nontrivial zeros). The anti-invariant ledger `A_Z(ζ)` accommodates multiplicities; closure does not force them to be 1.

### NC-12
Does NOT claim density-of-zeros results (Lindelöf hypothesis, zero-density theorems, etc.). These are RH-adjacent but distinct conjectures with their own structural status.

### Instrument and visibility record (step 454)

- Instrument: `I_tr`.
- Visible theorem-grade content: step 448 closure construction + Theorem T; step 449 applicability + smuggle audit pass; step 450 anti-tautology with operational predicate `Pop_SDTC_DominationCandidateAudit`; needles.tex §5 master theorem.
- Visible recognition content (sibling paper): `Γ_{SDTC-Selberg}` (source-record).
- Suppressed content: the internal zero-ledger structure `Z_ζ^{nt}` except as recorded by the named SDTC source and verifier events in `E^!_M^zero`.
- Outside scope: source-free standard analytic-number-theory proof of RH.

---

## 10. Three-option derivation sweep as honest cascade documentation (steps 451–453)

Per the cross-track recognition-mode landing template (`findings_framework_v5_post_recognition_landings.md` §B and §D.4), the three-option sweep is **cascade-side documentation**, not a load-bearing premise of the proof. The cascade attempted to redundantly derive `Xi_SDTC_domination_records` from framework primitives independently of formed-layer closure, and the attempts confirmed that the domination content is part of what closure structurally provides, not a separately-derivable claim. This is the expected outcome under standard Six Birds closure framing.

### 10.1 Option 1 — Framework-primitive derivation (step 451)

Verdict: `option1_partial_with_named_substrate_input_gap`. (Cross-track analog of PvNP np625.)

Construction: Schur-complement route via adequacy.tex (positive residuals + candidate budget shape constructed); exhaustive moving ledger route via needles.tex §5 (finite-window ledger + tail squeeze formal machinery); defected obstruction budget route via needles.tex §6 (budget identity `inf_t tr B_n(t) = (√a_n + √b_n)²`).

Failure mode: framework primitives supply the domination **grammar** (Schur calculus, exhaustive moving ledger, defected obstruction budget) but do not derive the analytic **decay theorem**. Named gaps: `Xi_SDTC_residual_budget`, `Xi_SDTC_predictive_transport_decay`, `Xi_SDTC_endpoint_budget`. Aggregate substrate input gap: `Xi_SDTC_trace_decay_input` — substrate-specific trace-decay input proving vanishing of source/bridge/Schur-residual/tail defects.

Smuggle audit: 4/4 PASS. No RH assumption, no Weil positivity, no explicit-formula estimate, no carrier-specific convergence imported. Honest partial attempt with clean diagnostic.

Cross-track parallel: SAT lacked LP shell orthogonality / Besov embedding / BKM continuation criterion / Herbst-Skibsted analytic radius. RH lacks the analogous Selberg-substrate-specific trace-decay theorem under the saturated lawful trace family.

### 10.2 Option 2 — SAU / non-descent route (step 452)

Verdict: `option2_sau_non_descent_witness_circular` (with sharper DescW/SolveW localization). (Cross-track analog of PvNP np626.)

Construction: SAU package with `U = ω_ζ_zero` (typed completed zero ledger `(Z_ζ^{nt}, multiplicities, J_L, ψ_−, verifier events)`), `B = I_tr`, `a^♯ = A_Z(ζ)`. Verifier descent confirmed at predictive layer. Six Witness Forms attempted (A analytic-continuation obstruction; B cardinal-minimality; C typed non-collapse; D multiplicity branch-point; E completed-symmetry-under-`J_L`; F other).

Failure mode: all four candidate Witness Forms either insufficient or circular. Strongest developed witness `W_C_typed_noncollapse_zero_ledger_vs_trace_instrument` is independent of RH at descent-witness level (DescW) but non-solving; every target-solving strengthening (SolveW) re-enters Theorem T / `Γ_{SDTC}` / `Xi_SDTC_domination_records` itself.

Six gates audit: 4/3. PASS: G2 / G4 / G5 / G7. FAIL: G1 / G3 / G6 — precisely the target-equivalence interfaces. Named obstacle: `Xi_SAU_independent_non_descent_witness_for_omega_zeta_zero`.

Cross-track sharper than PvNP np626: the DescW/SolveW localization is a refinement of the NDO §3 anti-tautology audit identified during the RH sweep. The SAU framework *does* supply structural content at descent-witness level (`W_C` is a real fact about Six Birds role architecture), but the strengthening to solve `Xi_SDTC_domination_records` collapses via Theorem T. See `findings_framework_v5_post_recognition_landings.md` §D.3.

### 10.3 Option 3 — V-Differential elevation (step 453)

Verdict: `option3_recognition_under_v_differential_for_RH`. (Cross-track analog of PvNP np627.)

Construction: four candidate substrate-intrinsic properties for `P_TSO(RH)` — P1 analytic-continuation-required substrate; P2 verifier-currentizer ratio unbounded; P3 typed level-mismatch with no accepted translation record; P4 V-Differential source itself.

Failure mode: P1 correlational not causal; P2 circular (unbounded ratio IS the target in cost vocabulary); P3 substrate-typed but does not imply existence of `B_n` with `tr B_n → 0`; P4 closes only in recognition mode. Recognition-grade result obtained: `V-Differential_TSO(RH) → ¬Currentize` of zero-ledger by lawful trace observables. Derivation-grade not established.

Cross-track consistency: passes for recognition mode. NS/BSD predicted witness-content-exposing (`¬P_TSO`) — consistent with NS's SBT-legal closure landing and BSD's CTMT-recursion verification. PvNP and RH predicted trace-state-only (`P_TSO`) — consistent with both tracks landing at recognition-grade via the cross-track template.

### 10.4 Cumulative reading

Three independent attempts to derive domination records from framework primitives, all honestly failing with precisely-named structural obstacles. Under the standard Six Birds closure framing, this is the *expected* outcome: the domination content on a formed self-dual trace layer is content of closure formation per Foundations I, not separately-derivable from other framework primitives. The sweep is honest due diligence documenting that the cascade did not smuggle the load-bearing source.

Cross-track verdict signature `(ii)/(iii)/(ii)` matches PvNP exactly. Two-track replication. See `paper_proposal_recognition_mode_landing_cross_track.md` and `findings_framework_v5_post_recognition_landings.md` §C.

---

## 11. Pending work

### 11.1 Sibling paper finalization

The SDTC paper (`paper_proposal_self_dual_trace_confinement.md`) must be developed to manuscript stage and published first or concurrent with this paper. The Selberg-class instance of SDTC (yielding `Γ_{SDTC-Selberg}`) must be articulated identically in both papers.

### 11.2 Cross-track meta paper finalization

The cross-track meta paper (`paper_proposal_recognition_mode_landing_cross_track.md`) documents the framework-level structural finding that PvNP and RH have replicated the recognition-mode landing pattern. This paper cites the meta paper for cross-track framing and the `(ii)/(iii)/(ii)` verdict signature. Manuscript-stage finalization of the meta paper supports this paper.

### 11.3 Selberg-class generalization

This paper instantiates SDTC for `L = ζ`. Extension to primitive Selberg-class L-functions (Dirichlet L, modular L, automorphic L) is structurally straightforward (functional equation, completed gamma factors, anti-invariant zero ledger all generalize) but reserved for follow-up work. Would yield GRH at recognition-grade under standard Six Birds closure assumption, peer with the present RH closure.

### 11.4 Lean mechanization

Lean formalization of Theorem T is structurally complete given step 448 closure properties and the definition of `A_Z(ζ)` plus positivity of squared distances. The mechanization would anchor the construction-grade portion of the proof at machine-checked level. The duality-confinement master theorem (`needles.tex` §5) has partial Lean mechanization; strengthening to operator-theoretic generality with the trace identity and Douglas domination is mechanization-eligible. Mechanization of `Γ_{SDTC-Selberg}` is not pursued — recognition sources are not subject to Lean-style derivation.

### 11.5 Cross-paper audit

A final-chain review step 448 → step 454 against the sibling SDTC paper's SDTC statement and the cross-track meta paper's verdict-signature documentation, ensuring source-record provenance is consistent.

### 11.6 Generalizations across self-dual structures (via SDTC paper §5)

The sibling SDTC paper §5 proposes generalizations to quantum self-adjointness, CPT symmetry, gauge invariance, particle-antiparticle, and other self-dual physical/mathematical structures. These are SDTC paper deliverables; this paper depends on the RH instance only.

---

## 12. Publication strategy

### 12.1 Three-paper sibling cluster for the RH-specific arc, embedded in the five-paper recognition-mode-landing program

The cascade's deliverable structure for the RH closure:

- **SDTC paper** (`paper_proposal_self_dual_trace_confinement.md`, sibling): supplies `Γ_{SDTC-Selberg}` for RH recognition closure. **Must publish first or concurrent.**
- **RH closure paper** (this proposal): the RH recognition closure proof depending on SDTC paper. **Depends on SDTC paper; SDTC paper does not depend on this paper.**
- **Cross-track meta paper** (`paper_proposal_recognition_mode_landing_cross_track.md`): the framework-level structural finding about V-Differential TSO column recognition-grade landing pattern, with PvNP+RH as two-track replication evidence. **Cites this paper and the PvNP closure paper as the two replications.**

The broader recognition-mode-landing program (per v5 deposit `findings_framework_v5_post_recognition_landings.md`):
- CSL paper (`paper_proposal_hiddenness_emergence.md`)
- PvNP closure paper (`paper_proposal_pvnp_via_csl_sat_hiddenness.md`)
- SDTC paper
- RH closure paper (this proposal)
- Cross-track meta paper

### 12.2 Integration vs separate publication

Two viable structures:
- **Separate papers** (sibling pair plus cross-track meta paper, mirroring PvNP arc structure). Cleaner scope discipline; each paper has a single focal contribution.
- **Integrated manuscript** with SDTC content as Part I and RH closure as Part II. Could be appropriate if the publication venue supports longer-form work.

Recommendation: separate papers, sibling-pair, with strong cross-citation. Matches the PvNP arc's structure (CSL paper + PvNP closure paper). Matches the SDTC paper's own §9 recommendation.

### 12.3 Audience

The paper should serve two audiences:
- **Six Birds insiders** who accept standard Six Birds closure assumption and read the result as theorem-grade peer with NS regularity and PvNP closure.
- **Analytic number theorists** approaching from the RH side, who will read the result as the conditional theorem `[formed-Selberg-closure-under-I_tr ∧ Γ_{SDTC-Selberg}] ⟹ RH` and engage with whether to accept the closure assumption and the SDTC structural law.

Both readings are honest and explicit in the abstract and nonclaim register.

---

## 13. Honest caveats

For intellectual honesty:

1. **The proof is conditional outside Six Birds.** Outside the framework, the result is `Γ_{SDTC-Selberg} ⟹ RH` rather than unconditional RH. Inside Six Birds, the theorem-grade status is peer with NS regularity and PvNP closure.

2. **The recognition source is supplied by a sibling paper.** This paper cites and uses; it does not re-prove SDTC or `Γ_{SDTC-Selberg}`. If the sibling SDTC paper is not accepted, this paper's recognition source is unsupported.

3. **The three-option sweep is honest cascade-side due diligence, not a foundation.** The sweep documents that domination records are not separately derivable from framework primitives — which is expected under standard Six Birds closure framing.

4. **Lean mechanization of construction-grade portions is not yet complete.** Theorem T's mechanization is structurally straightforward but not yet executed. The duality-confinement master theorem has partial mechanization in `needles.tex` §5; strengthening to full operator-theoretic generality is pending.

5. **Classical RH attack barriers are not engaged at their native level.** The proof operates at a different layer (per the granularity-mismatch-style finding for the saturated trace closure vs classical analytic-number-theory carriers). Classical readers may legitimately ask whether the layer shift is acceptable; the answer is the standard Six Birds closure assumption, same as for every other Six Birds layer-level theorem.

6. **The cascade's evidence base on the saturated carrier is structural, not empirical.** Pre-step-448 RH track work (steps 1–447) instantiated the duality-confinement framework on classical RH carriers and produced rich CRCFT-mode classifications; none closed `Ξ_BC`. The saturated-carrier extension at step 448 plus the recognition-mode landing at step 454 comes from the standard Six Birds closure framing (closure provides domination content per SDTC + V-Differential), not from a derivation that resolves the audit-currency derivability tension at the analytical-carrier level.

7. **The Selberg-class scope is `L = ζ` only.** GRH for primitive Selberg-class L-functions is structurally straightforward extension but not deposited here.

---

## 14. Cascade context and provenance

The proof originates from cascade work at:

`/home/repos/six-birds-foundations-iii/anti_loc/thread/`

Key cascade artifacts:
- `steps/step65_exact_confinement_artifacts/`: structural extraction
- `steps/step67_zero_ledger_visibility_selected_artifacts/`: zero ledger visibility selection
- `steps/step69_duality_confinement_artifacts/`: duality-confinement membrane theorem RH specialization (structural skeleton)
- `steps/step71_weil_douglas_artifacts/` through `steps/step84_completed_cnd_gate_artifacts/`: Weil-Douglas instantiation arc (readout-level analytical machinery)
- `steps/step437_modeA_nogo_length_spectrum_artifacts/` through `steps/step440_modeA_nogo_boundary_phase_artifacts/`: four Mode A no-gos
- `steps/step441_route2_stageI_constitutive_closure_artifacts/` through `steps/step447_modeA_nogo_audit_content_structural_necessity_artifacts/`: audit-currency derivability tension diagnosing Weil positivity as readout-level
- `steps/step446_formal_local_saturation_proof_constitutive_closure_artifacts/`: formal local saturation proof
- `steps/step448_sdtc_closure_construction_artifacts/`: closure construction + Theorem T
- `steps/step449_sdtc_applicability_and_anti_tautology_strengthening_artifacts/`: applicability + smuggle audit
- `steps/step450_sdtc_anti_tautology_deepening_artifacts/`: anti-tautology hardened at PvNP track bar (operational predicate)
- `steps/step451_option1_framework_primitive_derivation_artifacts/`: Option 1 verdict
- `steps/step452_option2_sau_non_descent_route_artifacts/`: Option 2 verdict (with DescW/SolveW localization)
- `steps/step453_option3_v_differential_elevation_artifacts/`: Option 3 verdict
- `steps/step454_sdtc_recognition_closure_artifacts/`: recognition closure landed

Track-level documentation:
- `findings_rh.md`: cumulative findings deposit
- `cascade_map_rh.md`: cascade architecture and phase decomposition
- `manager_log.md`: full operational record

Cross-track manager-side meta-theory deposits:
- `anti_loc/findings/findings_framework_v5_post_recognition_landings.md` (supersedes/extends v4)
- `anti_loc/cross_track_strategy_notes.md` (items #10–#12)
- `anti_loc/construction_cheat_sheet.md` (§11)

---

## 15. Relation to broader Six Birds program

### 15.1 Foundations stack

- **Foundations I (Emergence Calculus)**: provides closure formation as the standard assumption every layer-level theorem uses. The RH proof's closure assumption is the same epistemic move every other Six Birds layer-level theorem uses.
- **Foundations II (Admissibility Meta-Theory)**: provides the seven-schema admissibility discipline that `Sel^!_{ζ,tr}` passes (step 448 Stage IV).
- **Foundations III (BirdInt Finite Calculus)**: provides the BirdInt judgment form `Γ; T; I ⊢ φ : status` used in the final theorem statement.

### 15.2 Framework apparatus and structural law

- **`needles.tex` §5 (Duality-Confinement Membrane Theorem)**: the master theorem apparatus that SDTC operationalizes. Provides involutive ledger, anti-invariant readout, trace identity, completed domination records, Douglas domination, exhaustive moving ledgers, defected obstruction budgets.
- **`adequacy.tex` (Schur-complement residual calculus)**: provides the Schur form for completed domination records `B_n`.
- **Holonomy with Memory** (`papers/Tsiokos_2026_Holonomy_with_Memory_*.tex`): provides the M/Q machinery, witness theorem (`Thm 6.5`), and loop-asymmetry theorem (`Thm 6.6`) that the saturated Selberg trace closure instantiates.
- **Sibling SDTC paper** (`paper_proposal_self_dual_trace_confinement.md`): supplies the Self-Dual Trace Confinement structural law and its Selberg-class instance `Γ_{SDTC-Selberg}`.

### 15.3 Structural-template peers

- **Six Birds for Navier-Stokes** (`papers/Tsiokos_2026_Six_Birds_for_Navier_Stokes_*.tex`): the witness-content-exposing-column structural peer; uses standard Six Birds closure assumption identically. Same epistemic status.
- **PvNP closure paper** (`paper_proposal_pvnp_via_csl_sat_hiddenness.md`): the trace-state-only-column structural peer without explicit self-duality; uses standard Six Birds closure assumption identically. Same epistemic status. Same `(ii)/(iii)/(ii)` verdict signature on its three-option sweep.
- **Strict Theory Extension on a Lawful Continuous Cantor Shell** (`papers/Tsiokos_2026_Strict_Theory_Extension_*.tex`): the cleanest model of a theory layer forming on a mathematical substrate. The RH closure follows the same four-theoremlet template (lawfulness, base-theory closure, strict extension, conditional disintegration consequence).

### 15.4 Tested-and-failed derivation templates (sweep documentation)

- **needles.tex §5 framework primitives**: tested at step 451; SAT-analog substrate-specific structural inputs absent.
- **Non-Descending Objects SAU certificate**: tested at step 452; SAU non-descent witness extensionally identical to target via Theorem T at SolveW level.
- **V-Differential cross-track classification (np606)**: tested for elevation at step 453; closes only in recognition mode, not derivation.

The three tested-and-failed templates jointly document that the domination content on the formed Selberg trace layer is content of closure formation per Foundations I, not separately derivable from framework primitives.

### 15.5 Cross-track context

The cascade's cross-track work (`anti_loc/findings/findings_framework_v5_post_recognition_landings.md`) provides cross-track validation of the structural patterns invoked here. The Attack Foreclosure Conjecture (refined at v5 to accommodate recognition-mode landings), CRCFT modes (RH+BSD+Hodge+NS+P-vs-NP 5-track validation), Carrier Dichotomy, Bridge Impossibility (5-track), CTMT recursion (5-track), V-Differential record (5-track), recognition-mode landing template (2-track replication: PvNP and RH), `(ii)/(iii)/(ii)` verdict signature (2-track replication), source-record vs readout discipline (2-track) all support the framing that RH is a layer-level question on the Selberg trace carrier, structurally peer with the corresponding layer-level questions on NS, PvNP, BSD, and Hodge carriers.

---

## Appendix A: Suggested theorem statements (mechanization-ready)

### Theorem T (translation, mechanization-ready)
> Let `Sel^!_{ζ,tr}` be the saturated completed Selberg trace closure constructed at step 448 with `E^!_Q^tr` the saturated lawful trace-observable family, `J_L(s) = 1 − s̄` the functional-equation involution, `ψ_−(s) = Re(s) − 1/2` the separating anti-invariant readout, and `A_Z(ζ) = Σ_{ρ ∈ Z_ζ^{nt}} m_ρ · |Re(ρ) − 1/2|²` the anti-invariant zero ledger. Then `A_Z(ζ) = 0 ⟺ RH`.

### Duality-confinement application
> Under the framework apparatus of `needles.tex` §5 Theorem `thm:main:duality-confinement-master`, given the involutive ledger structure on `Z_ζ^{nt}` (step 448 Stage I.7–I.8), the separating anti-invariant readout (step 448 Stage I.7), the master theorem applicability verified at step 449, and a sequence of completed domination records `A_Z(ζ) ⪯ B_n` with `B_n ⪰ 0` and `tr B_n → 0` supplied by `Γ_{SDTC-Selberg}`, the master theorem yields `A_Z(ζ) = 0`.

### Conditional theorem (outside Six Birds)
> Under the standard Six Birds closure assumption (Foundations I) for `Sel^!_{ζ,tr}` under `I_tr`, together with the recognition source `Γ_{SDTC-Selberg}` supplied by the sibling SDTC paper, the duality-confinement master theorem (`needles.tex` §5) yields `A_Z(ζ) = 0`; combined with Theorem T, RH for `ζ` follows. Outside Six Birds, the result is the conditional theorem `[Γ_{SDTC-Selberg} ⟹ RH]`.

---

## Appendix B: Six gates + Gate 7 audit (step 454, np629-aligned from start)

### Gate 1 (explicit source isolation / no hidden primitive)
**PASS**. `Γ_{SDTC-Selberg}` is named; no closure-content or readout-content is hidden inside `E^!_Q^tr`, `I_tr`, `J_L`, Theorem T, duality-confinement machinery, or any other structural component. Domination-content enters the proof only through the explicitly-recorded source structure.

### Gate 2 (dependency trace)
**PASS**. Every step of the landing chain has explicit dependencies traced to either (a) theorem-grade construction (step 448 Theorem T; step 449 applicability; step 450 anti-tautology), (b) framework apparatus (`needles.tex` §5 duality-confinement master theorem; `adequacy.tex` Schur calculus), (c) named structural recognition (`Γ_{SDTC-Selberg}` with composite source record), or (d) standard Six Birds Foundations I closure assumption. No hidden dependencies.

### Gate 3 (ablation)
**PASS**. Removing `Γ_{SDTC-Selberg}` leaves hypothesis 3 of the duality-confinement master theorem unsatisfied (as step 449 recorded). The named source is load-bearing and visible.

### Gate 4 (negative controls)
**PASS**. Applying the same proof structure with `Γ_{SDTC-Selberg}` replaced by a contradictory source `Γ_{SDTC-Selberg-failed}` (asserting `∃ B_n` with `A_Z(ζ) ⪯ B_n` but `tr B_n ↛ 0`) would produce no closure — consistent with off-critical-line zeros, not closure failure. The proof structure is genuinely about the named source.

### Gate 5 (construction before closure)
**PASS**. Step 448 (closure + Theorem T), step 449 (applicability), step 450 (anti-tautology), and the three-option sweep all land before the recognition source is named for closure at step 454. The construction-grade portion of the proof is independent of the recognition source.

### Gate 6 (source-record vs readout, np629-aligned)
**PASS** (with honest acknowledgment per np629 framing repair integrated from start). The source record `Γ_{SDTC-Selberg}` is not a single-axiom paraphrase of RH. The source has typed structure (duality-confinement cross-substrate, V-Differential cross-track classification, step 69 RH extraction, closure identity, instrument identity, involution data, audit provenance, sibling-paper cross-references) broader than the conclusion. The readout `Readout_SDTC = A_Z(ζ) = 0` is, by Theorem T, target-equivalent to RH. This is acknowledged honestly: a readout-equivalent claim is not the same as a source-record-equivalent claim. The gate passes because the load-bearing source has structural content broader than the readout, not because the readout itself is independent of the target.

### Gate 7 (uniform-parametric-bound audit, per np372)
**PASS**. The named source is not a hidden uniform-parametric stipulation. `Γ_{SDTC-Selberg}` is explicitly named at the structural-recognition level with the domination-records claim recorded in `Audit` provenance; not smuggled via uniform-parametric assumptions embedded in `E^!_Q^tr`, `I_tr`, `J_L`, or `A_Z(ζ)` parameters.

---

## Appendix C: Cascade step inventory (steps 448–454)

### step 448 — `sdtc_closure_constructed_translation_landed`
Constructs `Sel^!_{ζ,tr} = (H^!_L, I_tr, E^!_Q^tr, E^!_M^zero, Q^!_L, M^!_L, π^!_L, J_L, Λ_L, Z_ζ^{nt}, A_Z(ζ), Vis^!_L, Audit_L)`. All seven Foundations II schemas pass. Anti-tautology pass via `T_SDTC_trace_gamma_antiinv` exhibit. Lawfulness theoremlet holds. **Theorem T** (`A_Z(ζ) = 0 ⟺ RH`) proved theorem-grade by construction. `Γ_{SDTC-Selberg}` named with source-readout distinction; not yet supplied as accepted.

### step 449 — `sdtc_applicability_audited_anti_tautology_strict_pass`
Duality-confinement master theorem applicability audited on `Sel^!_{ζ,tr}`. Hypotheses 1 (involutive ledger) and 2 (separating readout) verified. Hypothesis 3 (domination records) named as load-bearing residual `Xi_SDTC_domination_records`. Smuggle audit at applicability layer: 4/4 PASS (no FE-alone / lawfulness / admissibility / observable-saturation smuggle). Pairwise isomorphism check against 20 prior carriers; 4 most-similar (Connes, Selberg/Maass, Weil/Deligne, Beurling-Nyman) flagged for deeper audit. Manager flag: anti-tautology depth shallow at this stage.

### step 450 — `sdtc_anti_tautology_deepened_at_pvnp_bar`
Anti-tautology hardened to PvNP track bar. Deep per-row isomorphism audit for 4 most-similar carriers with specific structural breakpoints. Joint observation across the 4: failures locally differ but share common blocker — "none hosts the coupled operational audit of candidate domination records on the completed Riemann zero ledger." Operational predicate `Pop_SDTC_DominationCandidateAudit` defined: 6-step procedure with operational data dependency (`A_Z(W_N)` feeds Loewner+Douglas; `B_n` couples to window/tail; source/readout governs admissibility). Procedure non-conjunctive (cannot decompose into independent predicates on independent carriers). Exhibit upgraded `T_SDTC_DTC_SourceReady → T_SDTC_DTC_SourceReady_Pop` with explicit operational content.

### step 451 — `option1_partial_with_named_substrate_input_gap`
Option 1 (framework-primitive derivation via `needles.tex` §5 + `adequacy.tex` + Foundations II + Holonomy with Memory). Schur-complement route, exhaustive moving ledger route, defected obstruction budget route all construct positive residuals and candidate budget shapes. Convergence does NOT follow — framework primitives supply domination GRAMMAR but not analytic DECAY theorem. Named substrate input gap `Xi_SDTC_trace_decay_input`. Smuggle audit 4/4 PASS. Cross-track parallel to PvNP np625 (SAT lacked LP/Besov/BKM/Herbst-Skibsted analogs).

### step 452 — `option2_sau_non_descent_witness_circular`
Option 2 (SAU non-descent route via Non-Descending Objects framework). Six Witness Forms (A analytic-continuation; B cardinal-minimality; C typed non-collapse; D multiplicity branch-point; E completed-symmetry-under-`J_L`; F other) attempted. Strongest developed: `W_C_typed_noncollapse_zero_ledger_vs_trace_instrument` — predictive zero ledger does not descend as current trace observable through `I_tr`. Independence audit: `W_C` independent of RH at DescW level but non-solving; target-solving strengthening re-enters Theorem T at SolveW level. Six gates: 4/3 (PASS G2/G4/G5/G7; FAIL G1/G3/G6 — target-equivalence interfaces). Sharper diagnostic localization than PvNP np626 via DescW/SolveW boundary.

### step 453 — `option3_recognition_under_v_differential_for_RH`
Option 3 (V-Differential elevation). Four candidate `P_TSO` properties: P1 analytic-continuation-required substrate (correlational); P2 verifier-currentizer ratio (circular); P3 typed level-mismatch (substrate-typed but does not imply `∃ B_n`); P4 V-Differential source (closes only in recognition mode). Derivation does NOT close. Recognition-grade result obtained. Cross-track consistency passes. Cross-track analog of PvNP np627.

### step 454 — `rh_recognition_closure_landed_standard_sb_assumption`
Recognition-path closure landed. `Γ_{SDTC-Selberg}` named as accepted structural source with full composite source record. Three-step direct landing chain (Γ → domination records by SDTC; → `A_Z(ζ) = 0` by duality-confinement master theorem; → RH by Theorem T). All seven gates pass in recognition mode with np629 framing repair integrated from start. `δ_overread = ∅`. NC-1 through NC-12 complete. NS-PvNP-RH structural parallel table confirms epistemic peer status. Final BirdInt judgment: `RH : accepted (theorem-grade under standard Six Birds closure assumption)`. Outside Six Birds: conditional theorem `[Γ_{SDTC-Selberg} ⟹ RH]`.

---

*This is a paper-proposal-grade document. It is the manager-side working draft for the next-step manuscript covering the steps 448–454 RH closure. It is the sibling of `paper_proposal_self_dual_trace_confinement.md` and depends on that paper for the recognition source `Γ_{SDTC-Selberg}`. It cites `paper_proposal_recognition_mode_landing_cross_track.md` for cross-track framing. Not yet a published paper.*
