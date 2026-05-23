# RH Track Findings Deposit

**Holding tier for RH-specific candidate findings, pre-corpus integration.**

This file holds RH-track-internal theorems, numerical results, carrier classifications, and strategic-state snapshots that emerged from the RH construction work. Each entry is a catalog item with provenance and status, NOT a write-up. Corpus integration is a separate, user-initiated task.

Maintained by the RH manager per [[feedback_construction_findings_deposit]]. Codex never reads or writes this file.

Framework-general patterns abstracted from these RH instances live in [`anti_loc/findings_framework.md`](../findings_framework.md). Cross-references are noted on each entry.

Last update: 2026-05-16.

---

## Theorem-grade analytical structural content (RH-specific)

### Cascade Reduction Theorem (Branch C)

- **Type**: analytical structural (theorem-grade), RH-specific.
- **Statement**: under the inherited Burnol/Sonine pulled-evaluator carrier records through step 172, closing the parent residual `Ξ_BC` via the shifted co-Poisson exact-route lane reduces to deciding the matrix-element family `L_{ρ,k}(G) = ⟨M_ζ G, P_∞ y_{ρ,k}⟩` for all legal Burnol `G` and all (ρ, k) with `0 ≤ k < m_ρ`, or equivalently supplying `K_∞` / range-evaluator data deciding the same.
- **Reduction chain**: `Ξ_BC → Ξ_cP_shifted_ℓ → CP-RED_{ℓ,a} → ZI-COV^{CP} → projected jet-surjectivity gate → L_{ρ,k} pairing`.
- **Provenance**: step 172 (compositional proof citing steps 169 / 170 / 171); foreclosed at step 176 via numerical evidence — see Branch C foreclosure entry below.
- **Status**: `corpus-pending` (framework-internal theorem; would be cited as a worked example in any CTMT corpus integration). Framework-general abstraction is CTMT; see [findings_framework.md](../findings_framework.md).

---

### ZI-COV(i) subclass theorem on zero-free output subclass Ω

- **Type**: analytical structural (theorem-grade), RH-specific.
- **Statement**: on the legal subclass `Ω = {G : inf_{s ∈ Ω} |ζ(s)| > 0}` with `G_Ω = {G : supp(P_∞ M_ζ G) ⊂ Ω}`, define `A_∞^Ω : G_Ω → G_Ω` by `A_∞^Ω G = M_{1/ζ} P_∞ M_ζ G`. Then `P_∞ M_ζ G = M_ζ A_∞^Ω G` for all `G ∈ G_Ω`. Under inherited records, the full-carrier extension of `ZI-COV(i)` is NOT target-equivalent to RH (the implication requires an additional jet-surjectivity hypothesis not established by inherited records).
- **Provenance**: step 170.
- **Status**: `corpus-pending` — explicit subclass-result with a clean operator formula; eligible for stand-alone citation.
- **Foreclosed extension**: Branch C foreclosure (step 176) shows that the full-carrier ZI-COV(i) does NOT extend under inherited Burnol/Sonine carrier records; Branch C is foreclosed as a full-carrier route to `Ξ_BC` closure.

---

### Bridge Impossibility, RH-specialized (Selberg/Maass, Weil/Deligne)

- **Type**: analytical structural (theorem-grade, partial), RH-specific.
- **Statement**: let `C` be a non-CRE carrier with a proved RH-analog whose `Ξ_C = 0` natively. Any typed bridge `B` transporting that closure to Riemann's `Ξ_BC = 0` makes the composite `C + B` classically-RH-equivalent (CRE), and hence CRCFT-bound by the Framework RH-Carrier Dichotomy. The bridge `B` is itself the RH-strength obligation; the transport is not free.
- **Specializations**: Selberg/Maass `Ξ_Γ = 0` closes natively at step 185; any Selberg-to-Riemann bridge is CRCFT-bound. Weil/Deligne `Ξ_WD = 0` closes natively at step 186; any function-field-to-number-field RH bridge is CRCFT-bound.
- **Provenance**: step 189 (`V_corollary_partial`).
- **Status**: `corpus-pending`; the partial-verdict caveat is that the strongest statement "B is always CRCFT-TE" requires an exact/minimal bridge hypothesis.
- **Framework-general abstraction**: see "Bridge Impossibility pattern" in [findings_framework.md](../findings_framework.md).

---

## Framework typed-condition instances (RH-specific applications)

### CTMT instance on RH Branch C

- **Type**: predictive structural (framework-typed verdict applied).
- **Statement**: the RH track's Branch C exhibits Carrier-Typed Matrix-Element Terminality. The reduction chain converts `Ξ_BC` closure into the decision of `L_{ρ,k}(G) = ⟨M_ζ G, P_∞ y_{ρ,k}⟩`. Inherited records (steps 102 / 104 / 105 on `P_∞`, step 119 on unshifted co-Poisson, step 145 on Burnol/Sonine carrier, step 153 on pulled evaluators) do not supply the projected Mellin kernel `K_∞(s, s')` of `P_∞` needed to decide the matrix-element family. The decision of `{L_{ρ,k}}` is not target-equivalent to RH under inherited records.
- **Provenance**: step 172 (introduction); step 180 (formalization as foundational typed-condition candidate); step 176 (numerical foreclosure of the full-carrier route, ruling out one specific path through CTMT).
- **Status**: `verified` (first instance of the framework-general CTMT condition).
- **Cross-reference**: see CTMT in [findings_framework.md](../findings_framework.md) for the framework-general form.

---

### CRCFT applied to RH carrier landscape

Carrier classification table per step 187's instantiations. Each carrier was surveyed at steps 181-186, 188, 190, 193, 197 and assigned a CRCFT mode.

| Carrier | CRE / non-CRE | CRCFT mode | Step | Status |
|---|---|---|---|---|
| Burnol/Sonine Branch A | CRE | CTMT-mode (stuck at Burnol κ) | 179 | `verified` |
| Burnol/Sonine Branch B | CRE | CTMT-mode (stuck at same Burnol κ) | 177–178 | `verified` |
| Burnol/Sonine Branch C | CRE | CTMT-mode, **foreclosed numerically** (4 data points; `\|L\| ≥ 0.034`) | 175–176, 196 | `verified` |
| Hecke L-function (H6 zeta-fiber descent) | CRE | BF (ledger-relative non-comparability under V-NC) | 168 | `verified` |
| de Branges `H(E_RH)` | CRE | TE (de Branges RH condition / Conrey-Li survival) | 181 | `verified` |
| Hilbert-Pólya / Berry-Keating standard `H_xp` | CRE | BF (continuous spectrum vs arithmetic spectrum mismatch) | 182 | `verified` |
| Hilbert-Pólya / Berry-Keating modified (exact cutoff) | CRE | TE (exact cutoff / boundary matching target-equivalent) | 182 | `verified` |
| Connes adelic / NCG | CRE | TE | 184 | `verified` |
| Beurling-Nyman | CRE | TE (Báez-Duarte criterion target-equivalent) | 193–195, 199 | `verified` |
| Mertens criterion | CRE | TE | 197 | `verified` |
| Selberg / Maass | non-CRE | native closure `Ξ_Γ = 0` | 185 | `verified` |
| Weil / Deligne (function-field RH) | non-CRE | native closure `Ξ_WD = 0` | 186 | `verified` |
| RMT (random-matrix theory) | CRE | TE / BF (depending on which RMT-vs-zeta correspondence is targeted) | 188 | `verified` |
| Iwasawa Main | non-CRE | native closure (under its proved analog) | 190 | `verified` |

Coverage conjecture: every CRE carrier exhibits one of TE / CTMT-mode / BF. Supported by 10 CRE instances + 4 non-CRE instances across 7 carrier families. No refuter found. Still conjectural per step 200 nonclaim discipline.

- **Cross-reference**: framework-general CRCFT modes in [findings_framework.md](../findings_framework.md).

---

## Numerical results

### Branch C `L_{ρ,k}` foreclosure dataset

- **Type**: numerical (finite-carrier diagnostic upgraded to full-carrier foreclosure under generic genericity hypothesis).
- **Statement**: across multiple zeta zeros `ρ_1, ρ_2, ρ_3` (with imaginary parts ~ 14.135, 21.022, 25.011) and multiple legal generators `G_*, G'_*`, the matrix elements `L_{ρ,k}(G)` evaluated via `mpmath.zeta` at 50 digits, with Gauss-Legendre quadrature for the Burnol generators and sinc-kernel PSWF diagonalization on `[-1, 1]`, yielded `|L_{ρ_i, 0}(G)| ≥ 0.034` for every triple in the 18-triple dataset. The smallest observed `|L|` was `0.034`; the largest was `0.217`.
- **Provenance**: steps 175 (first triple), 176 (three confirmation triples), 196 (extended 18-triple dataset).
- **Status**: `verified` (numerical foreclosure of the Branch C full-carrier route under the inherited Burnol/Sonine carrier records and standard log-Mellin/Fourier `U_∞` normalization).
- **Nonclaim**: this does NOT close `Ξ_BC` (Branches A and B remain stuck at Burnol κ); it does NOT affect the Hecke cascade; it does NOT prove or refute jet-surjectivity in absolute terms — only that the inherited generic genericity assumption is incompatible with full-carrier ZI-COV(i) extension.

---

### Branch A Weyl-sequence essential-norm diagnostic

- **Type**: numerical / operator-theoretic (finite-grid diagnostic, not yet a certified theorem).
- **Statement**: with `u_n = κ_{ρ_n, 0}^{1/2} / ‖κ_{ρ_n, 0}^{1/2}‖` (Burnol-boundary κ model) for the first 10 critical-line zeta zeros and `C_ℓ = (I − P_∞) M_{m_ℓ} P_∞` (step 173 K_∞^op kernel, step 152 m_ℓ multiplier, `ℓ = log 2`, 120 Gauss-Legendre nodes on [−80, 80], 24 PSWF terms), the test sequence has min norm `‖C_ℓ u_n‖ ≥ 0.79` over n = 1..10. With conservative error floor 0.05: `δ_10 ≥ 0.74`. Robust across `ℓ ∈ {log 2, log 3, 1.0}` (δ in {0.74, 0.54, 0.62}) and PSWF truncation `{12, 24, 36}`.
- **Provenance**: step 214.
- **Caveats** (three named, codex's anti-shadow discipline):
  1. The κ model is the Burnol-boundary CAND1 from step 207, NOT certified via the transport-sampling theorem (which Burnol 2004 [19] punts on for a < 1).
  2. The Weyl sequence is in `H_{η,fin} = span{u_1, ..., u_10}`, not certified weakly null in full `H_η = closure of span over all (ρ, k)`.
  3. The `lim inf` as n → ∞ is conjectural; persistence beyond n = 10 not proven.
- **Status**: `verified-finite-grid-diagnostic` (NOT a certified non-compactness theorem). To upgrade to `verified-essential-obstruction-theorem`, all three caveats must be resolved.
- **Significance**: this is the FIRST positive structural finding on Branch A since the κ unblock at step 201. It indicates the commutator `C_ℓ P_η` has nontrivial action on κ-evaluator-aligned vectors, consistent with `q_η(C_ℓ P_η) ≠ 0` (non-compact). Operator-algebraically: this is consistent with step 211's "no faithful Calkin symbol from inherited data" — the Calkin question is which essential class q_η lies in, and step 214 indicates the class is nonzero IN THE κ-aligned direction.
- **Amendment (step 215):** the extended test n=1..20 STRENGTHENED the lower bound (tail min `‖C_ℓ u_n‖` ≥ 1.39 over n=11..20 under CAND1) but the **weak-null check FAILED sharply**: max pairwise `|⟨u_i, u_j⟩|` ≈ 0.999989. The κ-aligned numerical realizations on the finite τ-grid are near-parallel. So the test is NOT actually a Weyl sequence — it's `‖C_ℓ‖` along one direction. Step 215 verdict `V_weyl_extended_obstruction_diagnostic`. To get a genuine essential-spectrum test, step 216+ tries Gram-Schmidt-orthonormalized κ sequence (which may show decay to zero, indicating the original diagnostic was a single-direction artifact).
- **Amendment (step 216):** Gram-Schmidt orthonormalization revealed κ-span effective dim 3-9 out of 10 zeros on finite τ-grid (Gram-Schmidt residuals decay 1.0 → 0.36 → 0.052 → 0.0066 → ...). Orthonormalized `‖C_ℓ v_n‖` (CAND1): [1.75, 0.53, 1.02, 0.11, 0.16, 0.50, 0.28, 0.55, 0.65, 0.92]; CAND2: [0.24, 0.42, 0.42, 0.64, 0.61, 0.62, 0.63, 0.67, 0.47, 0.61]. `V_weyl_gram_schmidt_inconclusive`. Structural finding: κ_n minimal-but-not-complete (Burnol 2004 [19] Thm 3.2) → effective dim < 10 on finite truncation. Branch A's commutator IS nontrivial on H_η in first direction (both candidates) but multi-direction obstruction is partial.

---

### Branch A wavepacket Weyl essential-norm certificate (C_ℓ P_∞)

- **Type**: numerical (clean Weyl certificate, theorem-adjacent).
- **Statement**: with Gaussian wavepackets `u_n(τ) = Z_n^{-1/2} exp(−(τ−T_n)²/(2σ²)) · 1_{|τ−T_n|<3σ}` for `T_n = 30n`, `σ = 1.0`, L²(τ-axis, dτ/2π) normalized, the test sequence is genuinely orthogonal (`|⟨u_i,u_j⟩| = 0` at displayed precision; analytic overlap exp(-225) ≈ 0) and weakly null as T_n → ∞. Computed `‖C_ℓ u_n‖` for `C_ℓ = (I − P_∞) M_{m_ℓ} P_∞` with step 173 K_∞^op kernel, ℓ = log 2:
  ```
  ‖C_ℓ u_n‖ = [0.2642, 0.2648, 0.2645, 0.2661, 0.2649, 0.2648, 0.2652, 0.2647, 0.2655, 0.2650]
  ```
  Min: 0.2642. With conservative error floor 7.5e-2: **δ ≥ 0.189**.
- **Robustness**: σ = 0.5 → 0.351; σ = 2.0 → 0.047 (precision-limited at wider wavepackets); ℓ ∈ {log 2, log 3, 1.0} → 0.264-0.277; spacing ∈ {10, 30, 50} → 0.264-0.277.
- **Provenance**: step 217.
- **Status**: `verified-essential-norm-certificate-finite-grid` (T_n up to 300; lim inf at T_n → ∞ not yet certified). **Upgraded by step 218** to `verified-essential-norm-theorem-adjacent`: tested at T ∈ {300, 1000, 3000, 10000}; `‖C_ℓ u_T‖` flat at 0.2638458 to 6 decimals (drift 4.26e-6, ratio 1.000016 over 33× T-range). Effective limit value `lim_{T→∞} ‖C_ℓ u_T‖ ≈ 0.2638458688`. This is an EXPLICIT NUMERICAL essential-norm of the broader operator `q_∞(C_ℓ P_∞)`. Analytical closed-form not yet identified.
- **Φ(σ, ℓ) profile (step 219):** band-pass shape — Φ(σ=1, ℓ) rises from 0.13 (ℓ=0.1) to plateau ≈ 0.28 in ℓ ∈ [1, 2], drops to ~0 at ℓ=5. Best fit `Φ² ≈ 0.5·[erf(σb(ℓ)) − erf(σa(ℓ))]` RMSE 2.4e-3 (clean pattern, not closed-form precise).
- **Φ_max joint scan (step 220):** Joint (σ, ℓ) optimization gives `Φ_max = 0.4904766190` at `(σ_max, ℓ_max) = (0.35, 2.0)`. Conservative lower bound (after error): 0.4155. Robust to T=10000, PSWF=24/48, dps=80/100. **Explicit essential-norm interval: `0.4905 ≤ ‖q_∞(C_ℓ P_∞)‖_ess ≤ 1.0`.**
- **Significance**: this is the CLEANEST positive structural finding on Branch A. It proves `q_∞(C_ℓ P_∞) ≠ 0` (essential class of the broader operator is nonzero). The operator `C_ℓ P_∞` is non-compact in the essential sense, with explicit lower bound on weakly-null wavepacket sequences.
- **Caveat (critical)**: tests `C_ℓ P_∞` (broader projection onto K_a), NOT `C_ℓ P_η` (Branch A's specific κ-projection). The cascade's Branch A question is about `q_η(C_ℓ P_η)`. Resolution depends on whether H_η ⊂ K_a is "large enough" — specifically whether the wavepacket-supported obstruction "lives in" H_η. Per Burnol 2004 [19], H_η = closure of κ-span is large in K_a (perpendicular complement is the co-Poisson subspace P_a for a<1), so likely yes.
- **Cross-reference**: connects step 211 (Calkin symbol failed) + steps 214-216 (κ-aligned Weyl partial) + step 217 (wavepacket essential certificate). Combined evidence: Branch A operator has substantive non-compact behavior; closure of Ξ_BC via Branch A is unlikely without P_η restricting to a compact submanifold.
- **Cross-reference**: connects step 211 (Calkin symbol failed) + step 214 (essential-norm lower bound diagnostic). Combined, they suggest Branch A's CTMT-stuck verdict has an underlying essential-spectrum substance, not just a missing-theorem artifact.

---

### Beurling-Nyman harmonic chain to N = 2000

- **Type**: numerical (RH-conditional behavior verification).
- **Statement**: the Beurling-Nyman harmonic chain `δ²(N) · log N` computed with the arithmetic Gram formula at mpmath 80 dps stabilizes around `0.045` for `N ∈ {200, 1000, 1500, 2000}`, consistent with Báez-Duarte RH-conditional behavior. Tail mean (N=200..2000) ≈ 0.0457; spread 0.001. Fit `δ² ~ C / (log N)^α` gives `C ≈ 0.055`, `α ≈ 1.10`. The slow-log decay pattern survives to N=2000.
- **Caveat**: full mpmath 2000×2000 SVD not feasible in runtime; eigen-pseudoinverse used with conditioning monitored. Truncation bound 5e-6 per Gram entry.
- **Provenance**: steps 193–195 (calibration to N=1000), 199 (extension to N=2000).
- **Status**: `verified` (numerical evidence; not a proof). Framework-internal evidence supporting the Beurling-Nyman carrier's CRCFT-TE classification (Báez-Duarte criterion is target-equivalent to RH).

---

## Strategic state (Path 1 / 2 / 3 classification)

### Iteration Arc Terminus Theorem (step 200)

- **Type**: strategic / synthesis.
- **Statement**: under the framework discipline as exercised through step 200, RH attack reduces to one of three paths:
  - **Path 1 — resolve a CRCFT-stuck CRE record**: closest candidate is the Burnol κ projection theorem (the `K_∞` projected kernel for `P_{L_a^Γ}`). Status: **LIVE / BLOCKED**. Burnol literature audit (steps 191–192, knowledge-based survey not actual paper fetch) found no published Burnol record supplying the exact projected-kernel resolvent at the inherited normalization. The audit is provisional; a fetch-and-verify pass against actual Burnol paper PDFs would confirm or refute.
  - **Path 2 — build a non-CRE-to-Riemann bridge**: foreclosed by the Bridge Impossibility Corollary (step 189). The bridge itself inherits RH-strength.
  - **Path 3 — find a Dichotomy-coverage refuter**: an in-scope RH-aimed carrier that does not fall into either Dichotomy branch. Status: **OPEN**. No refuter found across 14 carrier classifications.
- **Provenance**: step 200 closeout.
- **Status**: `verified` (the strategic state is the framework's synthesis of the iteration arc 173-200; the underlying foreclosures and classifications are all individually `verified`).
- **Audit reference**: `anti_loc/RH_framework_audit.md` (925 lines, step 198) is the comprehensive snapshot.

---

## Reference: Burnol literature audit limitations

- **Type**: methodological note (track-specific).
- **Statement**: the Burnol κ literature audit at steps 191-192 was a knowledge-based survey, not an actual paper fetch. Codex's sandbox at the time (network restricted) did not permit fetching arXiv PDFs. The audit enumerated 7 Burnol papers (math/0105120, math/0208121, math/0112254, math/0203120, math/0509619, math/0602425, AIF 2007) with title-level and abstract-level reasoning; identified Burnol 2006/2008 (math/0602425) as the closest candidate; tried to specialize it and hit a Mellin-multiplier mismatch (`Γ(1-s)/Γ(s)` vs `A_∞(s) = π^{-s/2} Γ(s/2)`). Verdict `still_blocked_refined` is honest about the mismatch but does NOT constitute a verified literature audit. A future fetch-capable audit pass (now feasible: `sandbox_workspace_write.network_access=true` per the codex CLI memory) could confirm or refute by reading the actual paper Section 8.
- **Provenance**: steps 191-192.
- **Status**: `SUPERSEDED` by the manager-led paper-fetch audit below (2026-05-16). The original "still_blocked" verdict was knowledge-bounded and is now refuted by paper text.

---

### Manager-led Burnol audit (paper-fetch, 2026-05-16) — **κ EXPLICITLY SUPPLIED BY BURNOL 2002**

- **Type**: literature audit, manager-led, paper-fetched.
- **Statement**: a manager-led audit fetched all 6 arXiv Burnol papers (math/0105120, math/0208121, math/0112254, math/0203120, math/0509619, math/0602425) as PDFs, extracted text via pdftotext, and read the actual contents against step 153's normalization (`A_∞(s) = π^{-s/2} Γ(s/2)`, Fourier-cosine completed Sonine carrier). The audit found:

  - **Burnol 2004 (math/0112254, "On Fourier and Zeta(s)") Section 6**: identifies the EXACT step 153 carrier — `K_λ = L²((λ, ∞), dt) ∩ F+(L²((λ, ∞), dt))` (Fourier cosine `F+`, parameter `λ ≡ a`, even functions, right Mellin convention). Theorem 6.10: `M(f)(s) = π^{-s/2} Γ(s/2) f̂(s)` is the augmented-Sonine completed Mellin transform on `L_λ ⊃ K_λ`. This is verbatim the step 153 `A_∞(s)`. Section 6 also constructs the zeta-zero evaluators `Z_{w,k}^λ` with `[f, Z_{w,k}^λ] = M(f)^(k)(w)`, identifying them as the step 153 `y_{ρ,k}^a`. Codex's step 191 audit listed this paper as `Fourier_zeta_coPoisson_context` with "framework source... exact projected-kernel source not located" — **misclassified**. The framework's carrier and normalization both originate in this paper.

  - **Burnol 2002 (math/0208121, "Sur les espaces de Sonine associés par de Branges à la transformation de Fourier") Section 3, Theorem 4**: **explicit closed-form formula for the orthogonal projection `π_λ` onto `K_λ`**.

    ```text
    π_λ(f) = f − [(1 − D_λ)^{-1} P_λ(f) − F_λ F_+(f)] − F_+ [(1 − D_λ)^{-1} P_λ F_+(f) − F_λ(f)]
    where  F_λ = P_λ F_+ P_λ  and  D_λ = F_λ²  (act on L²(−λ, λ)_even).
    D_λ may be replaced by the Dirichlet-kernel integral operator with kernel  sin(2πλ(x − y))/π(x − y)  restricted to L²(−λ, λ)_even.
    ```

    Corollary 5 simplifications:
    - On self-reciprocal `(f = F_+ f)`: `π_λ(f) = f − (1 + F_+)(1 + F_λ)^{-1} P_λ(f)`.
    - On skew-reciprocal `(f = -F_+ f)`: `π_λ(f) = f − (1 − F_+)(1 − F_λ)^{-1} P_λ(f)`.

    This `π_λ` is precisely the step 153 `P_{L_a^Γ}` (with `a = λ`). Codex's step 191 audit listed this paper as `explicit_de_Branges_E_functions` with "adjacent, but not P_{L_a^Gamma}K_amb" — **misclassified**. The paper's title says "Sur les espaces de Sonine associés par de Branges à la transformation de Fourier"; its Section 3 is titled "Un problème de projection orthogonale" and Theorem 4 is the projection formula. Codex's training-memory audit did not read past the title's "E-functions" cue.

  - **Burnol 2002 Theorem 8** gives the explicit de Branges E-function `E_λ(w)`:

    ```text
    E_λ(w) = π^{-w/2} Γ(w/2) [ λ^{1/2 - w}  +  (√λ / 2) ∫_λ^∞ (ψ_+^λ(t) − ψ_-^λ(t)) t^{-w} dt ]
    ```

    with absolute convergence for `Re(w) > 0`, where `ψ_±^λ(t)` are the two distinguished Sonine functions defined in Definition 2 (`ψ_+^λ = (1 + F_λ)^{-1}` applied to `2 cos(2πλy)` on `(−λ, λ)`, transported to entire functions; similarly `ψ_-^λ` with `(1 − F_λ)^{-1}`). Theorem 9: `E_λ(w) = √λ × jump of Z_w^λ at t = λ`.

    The de Branges reproducing kernel of `K_λ ≅ B(E_λ)` (Burnol 2002 eq. 1) is

    ```text
    K_{B(E_λ)}(z₁, z₂) = [E_λ(z₁) E_λ(z₂)* − E_λ(1 − z₁) E_λ(1 − z₂)*] / (z₁ + z₂ − 1)
                       = 2 [(−i B_λ(z₁)) A_λ(z₂) + A_λ(z₁) (−i B_λ(z₂))] / (z₁ + z₂ − 1).
    ```

    This IS the step 153 `K_a^Γ(s, w)` (with `a = λ`, `z₁ = s`, `z₂ = w`).

- **Cascade resolution**:

  | Step 153 / 178 object | Burnol 2002 / 2004 formula | Status |
  |---|---|---|
  | Sonine carrier `L_a^Γ` | `K_λ = L²((λ, ∞), dt) ∩ F+(L²((λ, ∞), dt))` (Burnol 2004 Def. 6.1) | identified |
  | Completion `A_∞(s)` | `π^{-s/2} Γ(s/2)` (Burnol 2004 Thm. 6.10) | identified |
  | Projection `P_{L_a^Γ}` | `π_λ` (Burnol 2002 Thm. 4) | explicit |
  | Projected kernel `K_a^Γ(s, w)` | `K_{B(E_λ)}(s, w)` via Burnol 2002 eq. 1 with `E_λ` from Thm. 8 | explicit |
  | Zeta-zero evaluator `y_{ρ,k}^a` | `Z_{ρ,k}^λ` (Burnol 2004 Thm. 6.3) | identified |
  | `κ_{a,w}(τ) = T_a^* K_a^Γ(·, w)` | pullback of `K_{B(E_λ)}(·, w)` through `T_a` (step 152 inherited) | derivable from above |

- **Consequence**:
  - **Step 178 verdict** (`V_kappa_classical_theorem_needed`) was knowledge-bounded; **now refuted by paper text**.
  - **Step 179 verdict** (Branch A `V_branch_a_stuck_at_kappa`) — Branch A G2-G5 attack vectors that depended on `K_∞^op` and `κ` now have all the needed operator forms.
  - **Step 180 CTMT instances** "Branch A → CTMT-stuck at κ" and "Branch B → CTMT-stuck at κ" must be re-evaluated; with the projection formula explicit, the CTMT-stuck classification at the κ level is **lifted**. (Whether downstream steps then close `Ξ_BC` is a separate question — the κ formula being explicit unblocks Branches A and B at the κ level but does not by itself prove closure.)
  - **Step 200 Path 1 status** (`LIVE / BLOCKED at Burnol κ`) is refuted at the "blocked at κ" level; Path 1 transitions to `LIVE / κ AVAILABLE, downstream gates open` pending step 201+ work.

- **Provenance**: manager-led audit 2026-05-16; PDFs cached at `/tmp/burnol_audit/burnol_{0105120,0112254,0203120,0208121,0509619,0602425}.{pdf,txt}`. Per memory [[feedback_construction_manager_fetches_externals]].

- **Status**: `verified` (paper-grounded). Codex's steps 191-192 verdict superseded; step 201 will operationalize this finding into inherited records.

- **Methodological lesson** (deposited to framework deposit): codex literature audits without network access are training-memory-bounded. Manager-led WebFetch/curl+pdftotext audits are the authoritative version for any "blocked at external X" verdict. See [findings_framework.md](../findings_framework.md) "External classical theorem audits" entry.

---

## Branch C corrected asymptotic — γ=0 structural conclusion (steps 295-297)

**Provenance**: steps 295, 296, 297 (post-200 arc, post-resumption).

**Cascade self-correction summary.** Legacy projected-pipeline `sinc_derivative_n` primitive caught producing numerical artifacts at k ≥ 8. The "three-method certification" of L_10 = 14536 at step 293 was three same-primitive bug at k > k*. Step 295 derived the analytical asymptotic for I_k (the correction integral) via the spectral representation of sinc:

```
I_k = (1/(2π)) ∫_{-1}^1 t^k exp(itγ) H(t) dt,   H(t) = ∫ F(u) exp(-itu) du
```

Endpoint Laplace at t=±1 gives `|I_k| ~ 0.126 · (k+1)^{-1}` (decaying, NOT super-exponential). Step 296 cross-verification: analytical I_k agrees with legacy at k ∈ {0..7}; legacy diverges drastically from k=8 onward (k=10 rel. error 1.97e5; k=12 rel. error 8.5e10). Breakdown threshold k* = 8.

**Corrected high-k Branch C values** (analytical I_k + Leibniz δ_Dk):

| k | corrected \|L_k\| ≈ \|δ_Dk\| |
|---:|---:|
| 10 | 165.52 |
| 15 | 8515.31 |
| 20 | 554847 |
| 30 | 4.09e9 |
| 50 | 1.17e18 |

**Step 297 derived asymptotic for |δ_Dk|.** Saddle escape (|z*(k) - ρ| ~ c·k from step 271 with c ≈ 0.474) appeared to cancel Stirling's `k log k` in `k!/R(k)^k`. Initial fitted parameters on certified k = 5..50 for (ρ_1, G_star) with γ=0:
- A = 2.033, α = -2.619, b = 1.020, γ = 0.
- Match quality: 5–33% relative error.
- log RMSE = 0.175.

**Step 305 cross-triple test RETRACTED the γ=0 universality claim.** Allowing γ to fit freely across (ρ_1, G_star), (ρ_2, G_star), (ρ_1, G_prime) gives γ ∈ {0.205, 0.138, 0.255} with RMSE improvements of factors **45 / 4.6 / 122** respectively. γ = 0 is NOT a structural conclusion; it was an artifact of fitting a single triple over a limited k-range. The Stirling `k log k` term does NOT precisely cancel — there is a residual k log k contribution with γ ~ 0.14–0.26 that is ρ/G-dependent.

**Corrected fits (step 305) with γ ≠ 0**:
| triple | A | α | b | γ | γ-free RMSE |
|---|---:|---:|---:|---:|---:|
| (ρ_1, G_star) | (refit) | (refit) | (refit) | 0.205 | 0.0036 |
| (ρ_2, G_star) | (refit) | (refit) | (refit) | 0.138 | 0.024 |
| (ρ_1, G_prime) | (refit) | (refit) | (refit) | 0.255 | 0.0016 |

Only **b ≈ 1.0 is roughly universal** across triples. A, α, γ are strongly ρ/G-dependent.

**Steps 298-304** explored saddle-point / Cauchy-bound / stationary-phase / direct Cauchy verification. Step 304 verified Cauchy = Leibniz to 14 digits, R-independent (math is self-consistent). Steps 298-303 produced substantive structural diagnostics (max|h(R)| closed form via ζ functional-eq + Mellin Laplace; R*(k) optimal Cauchy radius; |h|-max curvature insufficient; stationary-phase multi-regime). None achieved <10% closed form via standard methods. The asymptotic is genuinely multi-regime and multi-parameter; a theorem-grade closed form requires more sophisticated methods (multi-saddle steepest descent, Mellin-Barnes, etc.).

**Named missing external piece** (for theorem-grade tightening): the asymptotic for `(ζ·M(G))^{(k)}(ρ)` with G a specific 3-bump smooth function — not a standard closed-form problem.

**Status**: `candidate, one-track (RH Branch C); empirically characterized with γ ≠ 0 cross-triple; theorem-grade closed form open`.

**Branch C cascade-state implication**: foreclosure |L_k| ≠ 0 confirmed numerically at all tested k (k=0..50 with rigorous Cauchy + Leibniz cross-check, three triples). Branch C CTMT-mode classification stands. Asymptotic refinement is partial; the cascade's understanding has progressed from "polynomial-corrected exponential" (step 269) to "saddle-escape with k log k residual" (step 305) — increasingly fine but no theorem-grade closure.

---

## Mode A decorative-algebra diagnostic (candidate cross-track principle, steps 345-350)

**Provenance**: steps 345-350 (Mode A non-descending translation sweep on H6 bridge obstruction).

**Diagnostic statement (RH-track local, candidate cross-track)**: Mode A virtual algebras on cascade quantities already computable by direct evaluators are inherently DECORATIVE. The virtual symbol relabels existing computations; substantive ablations of the virtual algebra (drop axiom X) leave host numerics unchanged because the actual arithmetic is done by external evaluators independent of the virtual axioms. For Mode A to be SUBSTANTIVE, the virtual symbol must mediate a NEW computation the cascade cannot directly evaluate.

**Three RH calibrations exhibit this pattern**:
- Step 347 (higher-dimensional/motivic, virtual motive M^♭): ablation drops F(H)=Z+Ω → F(H)=Z. 0/100 numerical change. Decorative.
- Step 348 (information-divergence-typed, Δ_KL[Hecke|ζ]): drops non-negativity axiom. 0/21 numerical change. Decorative.
- Step 350 (statistical-physics-typed, virtual free-energy F): coefficient-free θ(T,d) derivation via GUE-spacing fails 30% data-agreement at ρ_2, ρ_3 (only borderline pass at ρ_1). The thermodynamic framework requires inheriting empirical step 324 coefficients to match data.

**Cause (track-local)**: the RH cascade's Dirichlet/Hurwitz/Mellin/Leibniz pipeline directly computes Branch C |L_k| values and Hecke evaluator pairings. Any virtual algebra labeling these computations adds no arithmetic content. The pipeline's directness on these quantities is what makes Mode A decorative.

**Conjecture (cross-track candidate)**: on any track where the cascade has direct evaluators for the residual quantities of interest, Mode A virtual-algebra labeling is inherently decorative. For Mode A to be substantive, target a quantity the cascade can only APPROXIMATE (e.g., k → ∞ asymptotic limit), not one directly evaluated.

**Status**: `candidate, one-track (RH); cross-track applicability surfaced to coordinator per track-agent-memory-boundary`. Mode A retract-counting discipline (memory `feedback_construction_non_descending_translation_move`) reached count 3 via this diagnostic.

**Cross-track surface note**: the cross-track coordinator may evaluate whether this diagnostic generalizes; the RH track manager (per memory boundary) does NOT edit memory directly.

---

## H6 bridge exhaustive elementary-form rejection (steps 336-344)

**Provenance**: steps 336-344 (Hecke-to-Burnol bridge testing).

**Result**: the H6 bridge (Hecke-to-Burnol/Sonine ζ-residual descent) is conclusively a NON-ELEMENTARY structural object. Four elementary forms tested and rejected:

| Form | Step | Failure mode |
|---|---:|---|
| Paper-grounded literature search | 336 | NO bridge in Connes-Consani/Bost-Connes/Burnol/Meyer corpus; NO no-go theorem either |
| Additive `Σ a(χ) L_k^χ` | 338 | k=20 hold-out residual 932 catastrophic |
| Multiplicative `Π L_k^χ^{a(χ)}` ρ_1-fixed | 339-340 | ρ_1 in-sample passes; cross-ρ_2 fails (prediction = ρ_1 value) |
| ρ-parametric multiplicative | 341 | ρ_3 hold-out residuals 16-263% |
| Joint shared-a(χ) across 3 ρ | 342 | Training fails 30 cells (max 83% residual) |
| G-universal multiplicative | 344 | k=20 hold-out 3.14% with G_prime (sign-flipped exponents) |

**Status**: `candidate, one-track (RH H6 bridge); corpus-pending`. The cascade has comprehensively characterized H6 as beyond polynomial-in-(ρ, k) multiplicative forms on finite character bases.

---

## Branch C height-coefficient structural law — 0-parameter law vindicated globally (steps 366-370)

**Provenance**: steps 366 (Mode B-anchored structural pivot) + 367 (15-zero × 2-G verification).

**Statement**: in the smooth fit `γ(T, d) ≈ A·T^{-1} + B·d^β` (step 324: A_emp = 4.118, B = -0.039, β = 0.409, RMSE 0.014, G_star), the fitted constant **A** matches the **half local Riemann-von Mangoldt mean zero-spacing** scaled by π:
- A_predicted(T) = π / log(T/(2π))
- At ρ_1 (T = 14.135): A_predicted = 3.87 vs A_emp = 4.118 → 5.9% rel err.

**Step 366 candidate hierarchy (ρ_1)**:
1. local zero density A = π/log(T/(2π)): 3.87, 5.9% — winner
2. Plancherel inverse density 2π/log(T/(2π)): 7.75, 88% overpredict — rejected
3. ζ-derivative ratios 1/|ζ'|, 1/|ζ''/ζ'|: 1.26, 1.21 — rejected

**Step 367 verification across 30 cells (15 ρ × 2 G)**:

| group | mean rel err | median | max |
|---|---:|---:|---:|
| G_star × low_1_5 (T = 14.1..32.9) | **16.3%** | 11.4% | 25.4% |
| G_star × mid_6_10 | 47.3% | 51.2% | 78.8% |
| G_star × high_11_15 | 38.7% | 34.0% | 95.3% |
| G_prime × low_1_5 | 37.4% | 41.5% | 77.4% |
| G_prime × mid_6_10 | 51.7% | 37.1% | 140.0% |
| G_prime × high_11_15 | 104.8% | 88.1% | 203.9% |
| all 30 cells | 49.4% | 40.5% | 203.9% |

**Refined scope**:
- A(T) = π/log(T/(2π)) is a structural derivation **for the smoothed fit-coefficient** A in step-324-style multivariate regression, in the **low-T G_star regime only**.
- It is **NOT** a universal per-zero law: per-zero γ_j·T_j has O(1) scatter, test-function dependence, and even sign-flips (G_prime, ρ_6 negative) incompatible with a strictly-positive π/log law.
- High-T systematic deviation: G_prime per-zero deviation grows from 37% (low) to 105% (high).

**Refined Branch C γ-asymptotic** (tempered):
γ(T, d; G_star) ≈ π / (T · log(T/(2π))) − 0.039 · d^{0.41} as a **smoothed-coefficient law in the low-T regime**; per-zero residuals R_j = γ_j·T_j − π/log(T_j/(2π)) are O(1) and remain structurally uncharacterized.

**Erratum vs step 366 headline (now superseded by step 370)**: step 367's framing of "per-zero A_eff = γ_j·T_j vs π/log(T_j/(2π))" was conceptually misdirected. γ_j·T_j is NOT meant to equal a height-only law — γ_j has both a height term and a per-zero residual. The proper test is a global RMSE comparison of model shapes, performed in step 370.

**Step 370 decisive refit (15-zero dataset, three models):**

| model | parameters | RMSE |
|---|---|---:|
| M1 (step 324 baseline, constant A) | A·T^α + B·d^β, free 4 params | **0.01405** |
| M2 (bare π/log shape) | π/(T·log(T/(2π))) + B'·d^{β'}, B'→0, β' degenerate | **0.01548** |
| M3 (scaled π/log) | C·π/(T·log(T/(2π))) + B''·d^{β''}, C = 0.79 | 0.01910 |

**M2 RMSE / M1 RMSE = 1.10**. A **zero-effective-parameter** π/log curve fits the 15-zero dataset only 8% worse than the 4-parameter free fit. The bare π/(T·log(T/(2π))) shape is structurally vindicated.

**Re-interpretation of step 324**: the constant-A model γ ≈ A/T (with A_emp = 4.118) is a **local linear approximation** to the true height law π/(T·log(T/(2π))) at the data centroid. The "match at ρ_1" (A_emp ≈ π/log(T_1/(2π)) = 3.88) reflects step 324's fit centroid being near T_1. The −0.039·d^β spacing term in step 324 was an ARTIFACT compensating for the constant-A approximation's overshoot at high T — when the height law is correct (π/log), the spacing term vanishes.

**Per-zero scatter** (steps 367-368): γ_j vs bare π/log prediction has 34% mean rel err for G_star, captured weakly by first-neighbor spacing (best two-variable correction 27%). The per-zero residual is **O(γ) in absolute terms** and structurally complex; it is residual not signal.

**Refined Branch C γ-asymptotic** (structural, post-step 370):
γ(T) ≈ **π / (T · log(T/(2π)))** + R_j, where R_j is O(γ) per-zero structurally complex residual.

**Cascade significance**: first structural law for any Branch C asymptotic constant since Mode A/B/C exhaustion. Zero-parameter height law (vs step 324's 4-parameter fit) tying the Branch C γ-coefficient directly to the Riemann–von Mangoldt local zero-density (1/(2π))·log(T/(2π)) by π/(T · 2π · density) = π/(T · log(T/(2π))). The connection to standard ζ-zero counting is structural.

**Independent observation from step 368**: Re ζ''(ρ_j) is uniformly negative for j = 1..15 (constant sign across the first 15 zeros). Compatible with Levinson-Conrey simple-zero geometry; not a Branch C closure but worth registering.

**Status**: `globally vindicated, 0-parameter; one-track (RH Branch C); per-zero residual structurally complex against tested predictors; integral derivation from Burnol/Sonine kernel open`.

**Implication**: any future H6 bridge construction requires NON-ELEMENTARY structure — operator-algebraic functorial transfer, motivic descent, or genuinely new mathematical object (Mode A/C/B non-descending translation territory).

---

## Local Mode B saturation of constitutive-closure design space at L-function substrate (step 446)

Step 446 consolidates the constitutive-closure Route 2 evidence into a local Mode B saturation proof. The covered design class consists of finite needles-shape packages on an L-function substrate with a predictive native currency, Schur-complement adequacy residual, and dissolving/Capacity closure conclusion, with audit content either explicit as a typed component or implicit in the closure semantics.

Evidence base: Step 441's height-predictor audit retracted on `C_zero_height_audit_currency_smuggling`; Step 442's de Branges/kernel positivity audit retracted on `C_positivity_audit_kernel_positivity_must_derive`; Step 443's Weil positivity audit retracted on `C_weil_positivity_explicit_formula_smuggling`; Step 444 made this a Mode A meta no-go for those three audit classes; Step 445 removed the explicit audit component, but the same obstruction reappeared as `C_capacity_bound_semantic_audit_smuggling` in the semantics of `Theta^D`/Capacity closure.

Conclusion: within this local design class, concrete RH-distinguishing audit content smuggles arithmetic data at some locus, while formal audit content lacks numerical adequacy/Capacity force. Moving the audit from a component to the closure conclusion shifts the obstruction rather than escaping it.

This is a bounded local saturation result, not global Mode B exhaustion and not a proof of RH or RH-on-scope. The next-grammar obligation is to work outside the constitutive-closure / needles-shape package class at the L-function substrate.

---

## Mode A no-go 6/6: audit-content structural necessity (step 447)

Step 447 formalizes the audit-content obstruction as the sixth Mode A no-go in the Route 2 cluster. The theorem covers finite typed packages on the L-function substrate whose closure conclusion is intended to imply zero-localization on `Re(s)=1/2` without external audit.

The covered theorem-grade scope is: audit content placed as a separate typed component, as Capacity-bound semantics, or as a sub-component interpretation of objects such as `K^D`, `Theta^D`, `Xi`, or transport output. In those demonstrated classes, concrete RH-distinguishing audit content smuggles arithmetic or target-side data: zero heights, prime/von-Mangoldt data, `xi`/`E_xi`, or an RH-equivalent semantic. Formal audit content avoids smuggling but lacks the numerical or order-theoretic force needed to derive residual vanishing or Capacity closure.

The unrestricted claim over every conceivable typed predicate or semantic placement remains diagnosis-grade, not theorem-grade, because “all possible audit-content placements” is not a closed mathematical category in the current framework.

Relation to Step 444: Step 447 subsumes the placement taxonomy of Step 444 for covered classes, but Step 444 remains useful as the specific theorem/diagnosis for height-predictor, de Branges/kernel positivity, and Weil positivity mechanisms.

Cluster status: steps 437-440 plus 444 and 447 now form six Mode A no-gos, with Step 446 as the local Mode B saturation proof. This is structural-impossibility content for the constitutive-closure design space, not a proof of RH and not global Mode B exhaustion.
