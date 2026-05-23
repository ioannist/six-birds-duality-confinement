# RH Framework Audit

Foundational integration document for the RH-track work in Steps 173-197.

Status: foundational-corpus candidate.

Audience: framework maintainers, future RH-track agents, and reviewers of the
typed-condition catalog.

This document consolidates the typed conditions, corollaries, carrier audits,
numerical experiments, no-go records, and next-route recommendations produced
in the Step 173-197 RH-track iteration.

It is not a proof of RH.

It is not a closure certificate for `Xi_BC`.

It is a structured audit of what the framework learned about RH-style carriers.

---

## 0. Executive Abstract

The Step 173-197 iteration changed the RH track from a single-carrier
Burnol/Sonine attack into a typed-carrier classification program.

The Burnol/Sonine cascade was pushed past its earlier kernel gap by deriving
an operational identity for `P_infty`.  That identity enabled a concrete
Branch C matrix-element computation.  The result was negative for the
full-carrier route: the terminal matrix element `L_{rho,k}(G)` is numerically
nonzero on a growing dataset.

The remaining Burnol/Sonine Branches A and B both reduce to the same missing
transport object

```text
kappa_{a,w}(tau) = T_a^* K_a^Gamma(.,w)(1/2+i tau).
```

Multiple attacks and a literature audit showed that this requires an explicit
projection formula for `P_{L_a^Gamma}`.  That formula is not inherited and was
not extracted from the Burnol 2006/2008 J_0 Fredholm material.

The iteration then generalized.  It formalized three nested foundational typed
conditions:

1. Carrier-Typed Matrix-Element Terminality (CTMT).
2. Classical-RH Carrier Foreclosure Taxonomy (CRCFT).
3. Framework RH-Carrier Dichotomy Theorem.

Together with the earlier Cascade Reduction Theorem for `Xi_BC`, these form
the current RH framework backbone.

The iteration also derived a Bridge Impossibility Corollary in partial form:
non-CRE native closures do not transport to Riemann RH without the bridge
itself becoming a CRE obstruction.

The carrier evidence now has the following shape:

- CRE carriers land in CRCFT foreclosure modes.
- Non-CRE carriers with complete native ledgers close natively.
- Statistical evidence carriers, such as RMT, are outside the dichotomy's
  closure-carrier scope.

This document integrates that structure for foundational-corpus review.

---

## 1. Scope and Nonclaims

This audit covers Steps 173-197.

It integrates:

- four foundational typed conditions;
- one corollary;
- row-level classifications for CRE, non-CRE, and out-of-scope carriers;
- two numerical experiments;
- ten retained framework no-gos;
- Path 1/2/3 strategic conclusions;
- corpus-inclusion recommendations;
- open questions.

This audit does not:

- prove RH;
- disprove RH;
- prove `Xi_BC` vanishes;
- prove any Burnol/Sonine branch closes;
- replace external classical theorems;
- claim that numerical evidence proves an asymptotic theorem;
- claim that all future carriers must fit the dichotomy.

The coverage claims remain typed framework claims and, where explicitly
called conjectures, conjectural.

---

## 2. Notation

The main RH residual on the Burnol/Sonine carrier is

```text
Xi_BC = B^* Pi_Y B.
```

The archimedean Sonin/prolate projection is denoted

```text
P_infty.
```

The Step 173 operational identity is the main projection tool:

```text
K_infty^op(s,s')
  = delta(tau-tau')
    - sin(lambda(tau-tau'))/(pi(tau-tau'))
    - sum_n Psi_n^lambda(s) Psi_n^lambda(s')^*.
```

The Branch C terminal matrix element is

```text
L_{rho,k}(G) = <M_zeta G, P_infty y_{rho,k}>.
```

The Branch A/B missing transport vector is

```text
kappa_{a,w}(tau) = T_a^* K_a^Gamma(.,w)(1/2+i tau).
```

The framework carrier classes used below are:

- `CRE`: classically-RH-equivalent carrier.
- `not_CRE`: RH-analogous carrier whose native closure does not imply
  Riemann RH.
- `out_of_scope`: statistical or evidence carrier that is not a closure
  carrier.

---

## 3. Foundational Typed Condition I: Cascade Reduction Theorem

### 3.1 Formal Statement

The Step 172 theorem is the Shifted Co-Poisson Cascade Reduction for `Xi_BC`
on the Burnol/Sonine carrier.

Under inherited operator definitions:

- carrier `H`;
- projection `P_infty`;
- transport `T_a`;
- log-shift `tau_l`;
- Burnol generator class;
- Mellin-side variables;
- zero-evaluator atoms `y_{rho,k}`;

the shifted co-Poisson route reduces Branch C closure to deciding the matrix
elements

```text
L_{rho,k}(G) = <P_infty M_zeta G, y_{rho,k}>
             = <M_zeta G, P_infty y_{rho,k}>.
```

### 3.2 Reduction Chain

The theorem composes the following stages.

| Stage | Source | Content |
|---|---|---|
| a | Step 169 | Mellin-side computation for `u=Cg`: `M(B_{l,a} Cg)=T_a P_infty M_zeta(m_l G)-T_a P_infty M_{m_l}P_infty M_zeta G`. |
| b | Steps 169-170 | zeta factorization on the full `Cg` subclass is equivalent to ZI-COV conditions. |
| c | Step 170 | ZI-COV(i) holds on the zero-free output subclass via `A_infty^Omega=M_{1/zeta}P_infty M_zeta`; full-carrier target-equivalence is not inherited. |
| d | Step 171 | five structural routes reduce jet-surjectivity to `L_{rho,k}`. |
| e | Step 172 | closing `Xi_BC` via shifted co-Poisson exactness reduces to deciding the `L_{rho,k}` family. |

### 3.3 Consequence

The theorem localizes Branch C.  The relevant external content is not vague
"operator theory"; it is the typed family `L_{rho,k}(G)` or an equivalent
kernel/range-evaluator record for `P_infty`.

### 3.4 Later Status

Step 173 supplied `K_infty^op`.

Steps 175-176 and 196 evaluated nontrivial `L_{rho,k}(G)` values.

The full-carrier Branch C route is now numerically foreclosed under the
inherited normalization.

---

## 4. Foundational Typed Condition II: CTMT

### 4.1 Definition

Carrier-Typed Matrix-Element Terminality (CTMT) occurs when a residual closure
attempt on a typed carrier reduces to deciding a carrier-native matrix-element
family

```text
M(alpha,beta,gamma) = <a_alpha, P_beta b_gamma>,
```

where:

- `a_alpha` and `b_gamma` are carrier-native legal vectors;
- `P_beta` is a carrier-native projection or transport;
- inherited records do not compute the matrix element;
- the matrix-element decision is not already the target theorem under a
  different name.

### 4.2 Resolution Modes

CTMT instances resolve in three ways.

| Mode | Meaning | Framework output |
|---|---|---|
| CTMT-stuck | a missing classical kernel/transport theorem blocks evaluation | precise external-content interface |
| CTMT-foreclosed-numerical | a different operational path computes a nonzero value with error separation | route no-go |
| CTMT-bridge-failure | the matrix element is not defined across carriers because the bridge fails | comparison no-go |

### 4.3 CTMT Instances

| Instance | Carrier | Matrix element | Projection/transport | Resolution |
|---|---|---|---|---|
| Branch A | Burnol/Sonine | `<eta_i, C_l eta_j>` | `P_eta`, `P_infty`, `kappa` | CTMT-stuck at `kappa` |
| Branch B | Burnol/Sonine | `c_ij(l)=<e_i,C_l e_j>` | projected Sonine kernel | CTMT-stuck at `kappa` |
| Branch C | Burnol/Sonine | `L_{rho,k}(G)` | `K_infty^op` | CTMT-foreclosed-numerical |
| H6 | Hecke to Burnol/Sonine | cross-carrier comparison matrix | carrier bridge | CTMT bridge-failure / V-NC |

### 4.4 Consequence Theorem

When CTMT is reached, the framework's product is the exact matrix-element
interface.  The framework does not replace the missing classical theorem.
It names it.

### 4.5 Corpus Relationship

CTMT should be integrated into `needles.tex` as a layer-dissolving terminality
condition and into `adequacy.tex` as a residual-closing external-interface
type.

---

## 5. Foundational Typed Condition III: CRCFT

### 5.1 Definition

The Classical-RH Carrier Foreclosure Taxonomy (CRCFT) classifies
classically-RH-equivalent carriers under the framework discipline.

A carrier is CRE when either:

- it is a named classical approach to Riemann RH; or
- closure of its residual is logically equivalent to Riemann RH.

CRCFT says that CRE carriers exhibit at least one typed foreclosure mode.

### 5.2 Modes

| Mode | Name | Obstruction level |
|---|---|---|
| CRCFT-CTMT | matrix-element terminality | post-reduction |
| CRCFT-TE | target-equivalence | pre-reduction circularity |
| CRCFT-BF | bridge-failure | carrier-comparison failure |

### 5.3 Consequence Theorem

For a CRE carrier in CRCFT mode `m`:

- if `m=CTMT`, the framework outputs the matrix-element family;
- if `m=TE`, the framework outputs the target-equivalence no-go;
- if `m=BF`, the framework outputs the failed comparison axis.

### 5.4 CRCFT Instances

| Carrier / branch | Mode | Obstruction | Step |
|---|---|---|---|
| Burnol/Sonine A | CTMT-stuck | `kappa` / projected Sonine kernel | 179 |
| Burnol/Sonine B | CTMT-stuck | `kappa` / projected Sonine kernel | 177-178 |
| Burnol/Sonine C | CTMT-foreclosed-numerical | nonzero `L_{rho,k}(G)` | 175-176, 196 |
| Hecke H6 | BF | ledger-relative non-comparability | 168 |
| de Branges | TE | de Branges RH program / Conrey-Li survival | 181 |
| HP/BK standard | BF | wrong spectrum | 182 |
| HP/BK modified | TE | boundary/cutoff data target-equivalent | 182 |
| Connes adelic | TE | full trace-formula closure equivalent to RH | 184 |
| Beurling-Nyman | TE | closure criterion equivalent to RH | 193-195 |
| Mertens weak criterion | TE | weak Mertens closure equivalent to RH | 197 |

### 5.5 Coverage Conjecture

Every CRE carrier exhibits CRCFT in at least one of the three modes.

Status: conjectural.

Supported in this iteration by all tested CRE carriers.

Refutable by a CRE carrier with a completed, non-target-equivalent,
non-CTMT, non-BF closure route.

### 5.6 Corpus Relationship

CRCFT extends CTMT.  It belongs in a carrier-taxonomy section of
`adequacy.tex` and should reference CTMT rather than duplicate it.

---

## 6. Foundational Typed Condition IV: Framework RH-Carrier Dichotomy

### 6.1 Statement

Let `C` be a typed primary carrier supporting a residual `Xi_C` aimed at an
RH-analogous statement about an L-function or zeta function `L_C`.

The framework dichotomy has two branches.

### 6.2 CRE Branch

If `C` is CRE, then `C` exhibits CRCFT in at least one of:

- CTMT;
- TE;
- BF.

The output is a typed obstruction.

### 6.3 Non-CRE Branch

If `C` is non-CRE and its RH analog has a complete native proof ledger, then
the framework yields native closure:

```text
Xi_C = 0.
```

### 6.4 Non-CRE Native Closures

| Carrier | Native ledger | Closure | Step |
|---|---|---|---|
| Selberg/Maass | Selberg trace formula | `Xi_Gamma=0` | 185 |
| Weil-Deligne | Deligne purity + Grothendieck-Lefschetz | `Xi_WD=0` | 186 |
| Iwasawa main conjecture | Mazur-Wiles, Wiles, Skinner-Urban | `Xi_IW=0` | 190 |

### 6.5 Out-of-Scope Statistical Carrier

Random Matrix Theory was audited in Step 188.

It is not a closure carrier.  It is a statistical evidence and consistency
framework.  It therefore refines the dichotomy's domain but does not refute
the dichotomy.

### 6.6 Coverage Conjecture

Every RH-analogous typed closure carrier is classified by the dichotomy into
CRCFT foreclosure or native closure.

Status: conjectural.

Supported here by CRE and non-CRE tested carriers.

### 6.7 Corpus Relationship

The dichotomy contains CRCFT as its CRE branch.  It should be integrated as a
top-level RH-carrier theorem in the foundational corpus, with CTMT and CRCFT
as subordinate typed conditions.

---

## 7. Bridge Impossibility Corollary

### 7.1 Statement

Let `C` be a non-CRE RH-analogous carrier with native closure `Xi_C=0`.
Let `B` be a typed bridge such that closure of `B`, together with `Xi_C=0`,
derives Riemann RH or closes `Xi_BC`.

Then the composite carrier `C+B` is CRE.

By the dichotomy, the bridge/composite must fall into a CRCFT mode.

In the exact minimal bridge case, the bridge is CRCFT-TE: closing it is
logically equivalent to the missing Riemann RH step.

### 7.2 Proof Outline

1. `C` is non-CRE, so its native closure does not imply Riemann RH.
2. Add bridge data `B`.
3. If `Xi_C=0` plus `B` implies Riemann RH, the composite closure implies RH.
4. Therefore the composite is CRE by definition.
5. Apply the dichotomy to the composite.
6. The bridge is the new locus where Riemann information entered.
7. If no additional CTMT or BF obstruction intervenes, the bridge itself is
   target-equivalent.

### 7.3 Specializations

| Source carrier | Native closure | Bridge-to-Riemann status |
|---|---|---|
| Selberg/Maass | Selberg trace ledger closes `Xi_Gamma` | any exact bridge to Riemann becomes CRE/CRCFT |
| Weil-Deligne | Deligne purity closes `Xi_WD` | any number-field transport bridge becomes CRE/CRCFT |
| Iwasawa | Iwasawa main conjecture closes `Xi_IW` | p-adic to complex-RH transfer is not inherited and would be CRE/CRCFT |

### 7.4 Strategic Consequence

The corollary does not devalue native closures.

It says they do not transport to Riemann RH without the bridge becoming the
Riemann-hard object.

---

## 8. Carrier Classification Table

This table records row-level classifications.  Some carrier families produce
more than one row because standard and modified variants land in different
modes.

| # | Carrier / row | CRE status | Framework outcome | Mode / mechanism | Key step |
|---|---|---|---|---|---|
| 1 | Burnol/Sonine Branch A | CRE | foreclosed/stuck | CTMT-stuck at `kappa` | 179 |
| 2 | Burnol/Sonine Branch B | CRE | foreclosed/stuck | CTMT-stuck at `kappa` | 177-178 |
| 3 | Burnol/Sonine Branch C | CRE | foreclosed | CTMT-foreclosed-numerical | 175-176, 196 |
| 4 | Hecke H6 | CRE sibling bridge | foreclosed | BF / V-NC | 168 |
| 5 | de Branges `H(E_RH)` | CRE | foreclosed | TE | 181 |
| 6 | HP/BK standard `xp` | CRE candidate | foreclosed | BF / wrong spectrum | 182 |
| 7 | HP/BK modified | CRE | foreclosed | TE | 182 |
| 8 | Connes adelic / NCG | CRE | foreclosed | TE | 184 |
| 9 | Beurling-Nyman | CRE | foreclosed | TE with finite Gram subinterface | 193-195 |
| 10 | Mertens weak criterion | CRE | foreclosed | TE; strong form refuted separately | 197 |
| 11 | Selberg/Maass | not_CRE | native closure | Selberg trace ledger | 185 |
| 12 | Weil-Deligne function-field RH | not_CRE | native closure | Deligne purity | 186 |
| 13 | Iwasawa main conjecture | not_CRE | native closure | main conjecture ledger | 190 |
| 14 | RMT | outside scope | no closure classification | statistical evidence carrier | 188 |

The requested carrier-instance grouping counts Burnol/Sonine as one carrier
family, HP/BK as one family, and RMT as out of scope.  The row-level table is
more explicit and is the operational form used in this audit.

---

## 9. Numerical Experiment I: Branch C Foreclosure

### 9.1 Method

Steps 173-174 supplied the operational and symbolic formulas.

Steps 175-176 computed the first nontrivial values.

Step 196 extended the dataset.

Numerical convention:

- `lambda=1`;
- `U=200`;
- grid spacing `h=0.05`;
- `mpmath` zeta at 50 decimal digits;
- Gauss-Legendre quadrature for legal bump generators;
- PSWF terms from sinc-kernel diagonalization on `[-1,1]`;
- Step 196 included finite-difference diagnostics for `k=1`.

### 9.2 Step 175-176 Data

| Triple | Value / magnitude |
|---|---|
| `L_{rho_1,0}(G_star)` | `0.12147 - 0.08986 i`, `|L| >= 0.15089` |
| `L_{rho_2,0}(G_star)` | `|L| approx 0.1664` |
| `L_{rho_3,0}(G_star)` | `|L| approx 0.1113` |
| `L_{rho_1,0}(G_prime)` | `|L| approx 0.2170` |

### 9.3 Step 196 Extended Data

Step 196 computed 18 triples.

Coverage:

- zeros `rho_1` through `rho_6`;
- `k=0`;
- three `k=1` finite-difference diagnostics;
- five legal Burnol generators.

All 18 values were separated from zero by the stated error budget.

The smallest certified lower bound was

```text
min(|L|-error) = 3.4126458948014055e-02.
```

### 9.4 Interpretation

The data support robust nonvanishing of the Branch C terminal matrix element.

This forecloses the full-carrier ZI-COV(i) route under the inherited
normalization.

It does not prove any universal theorem over all legal `G`.

It does not disturb Step 170's zero-free output subclass theorem.

---

## 10. Numerical Experiment II: Beurling-Nyman Gram Chain

### 10.1 Carrier

The Beurling-Nyman carrier is `L^2[0,1]` with atoms

```text
rho_a(t) = {a/t} - a {1/t}.
```

The residual is the distance from the constant function `1` to the closed
span of the atoms.

### 10.2 Finite Defect

For a finite set `A={a_1,...,a_N}`,

```text
delta_A^2 = 1 - b_A^* G_A^dagger b_A.
```

Here:

- `G_A(i,j)=<rho_{a_i},rho_{a_j}>`;
- `b_A(i)=<1,rho_{a_i}>`;
- the harmonic chain is `A_N={1/k:1<=k<=N}`.

### 10.3 Step 194 Numerical Pattern

Step 194 computed several finite chains using direct deterministic summation.

For the harmonic chain:

| N | delta_A^2 |
|---|---|
| 5 | `0.0363` |
| 10 | `0.0238` |
| 20 | `0.0165` |
| 40 | `0.0127` |
| 80 | `0.0110` |

The observed product `delta_A^2 log N` stabilized near `0.05` for moderate
`N`.

### 10.4 Step 195 Arithmetic Refinement

Step 195 implemented the arithmetic Gram refinement and extended the
harmonic chain to larger `N`.

The reported pattern was:

```text
delta_A^2 log N approx 0.047.
```

This is consistent with slow logarithmic decay in the Baez-Duarte
Beurling-Nyman setting.

### 10.5 Interpretation

The Beurling-Nyman numerics support the RH-consistent direction but do not
prove the weak closure.

The carrier remains CRCFT-TE because the infinite closure is exactly the
target-equivalent step.

---

## 11. Retained Framework No-Gos

The iteration retains the following ten no-gos.

| # | No-go | What it forecloses |
|---|---|---|
| 1 | Public-shadow non-promotion | Hardy or hard-support shadows cannot decide the completed Calkin object without an accepted bridge. |
| 2 | Finite-window Calkin blindness | finite singular-value evidence cannot certify completed compactness or positive essential norm. |
| 3 | Auxiliary-GRH smuggling | assuming GRH on the Hecke side imports the target. |
| 4 | Incomplete character spectrum support-only | partial character coverage is not completed Hecke closure. |
| 5 | Scalar identity not carrier identity | `L_Q(s,1)=zeta(s)` does not identify carriers, probes, audits, or residuals. |
| 6 | Hecke V-NC bridge no-go | Hecke zeta fiber is non-comparable to Burnol/Sonine under inherited ledgers. |
| 7 | Branch C full-carrier ZI-COV(i) foreclosure | nonzero `L_{rho,k}(G)` blocks full-carrier Branch C. |
| 8 | de Branges target-equivalence | de Branges closure is the classical RH-equivalent program. |
| 9 | HP/BK standard BF and modified TE | standard `xp` has wrong spectrum; modified versions are target-equivalent. |
| 10 | Connes trace-formula target-equivalence | full Connes trace closure is RH-equivalent without independent inherited ledger. |

These no-gos are not claims that RH is false.

They are route-foreclosure records.

---

## 12. Path 1/2/3 Strategic Conclusion

The current strategy space reduces to three paths.

### Path 1: Resolve a CRCFT-Stuck Classical Record

The only live non-foreclosed Riemann route inside the explored Burnol/Sonine
tree is the `kappa` record:

```text
kappa_{a,w}(tau)=T_a^*K_a^Gamma(.,w)(1/2+i tau).
```

This requires the projected Sonine kernel

```text
K_a^Gamma = P_{L_a^Gamma} K_a^{Gamma,amb}.
```

Steps 191-192 refined the source of the gap:

- Burnol literature contains related Sonine/Hankel/Fredholm material.
- Burnol 2006/2008 J_0 resolvent material does not directly specialize to
  Step 153's Fourier-cosine/zeta-completed Sonine carrier.
- A separate projection theorem or carrier-equivalence theorem is needed.

### Path 2: Transport Non-CRE Native Closure to Riemann

The Bridge Impossibility Corollary forecloses this as a cheap route.

Selberg, Weil-Deligne, and Iwasawa native closures remain important, but a
bridge from them to Riemann RH becomes the CRE-hard object.

### Path 3: Find a Dichotomy Coverage Refuter

RMT was tested as a plausible refuter and classified out of scope because it
is statistical, not a closure carrier.

Beurling-Nyman and Mertens were tested as fresh CRE carriers and landed in
CRCFT-TE.

No coverage refuter was found.

---

## 13. Classical References Used Across the Audit

The following external classical references are cited by the integrated
records.

### Burnol / Sonine / Hankel

- Jean-Francois Burnol, papers on Sonine spaces, co-Poisson, Fourier and
  zeta, 1990s-2000s.
- Burnol, `Scattering, determinants, hyperfunctions in relation to
  Gamma(1-s)/Gamma(s)`, arXiv:math/0602425, 2006/2008.
- Classical Sonine, Bessel, and Hankel transform literature.
- Slepian-Pollak prolate spheroidal wave function theory.

### de Branges

- Louis de Branges, `Hilbert Spaces of Entire Functions`, 1968.
- de Branges RH program papers, 1980s.
- Conrey-Li, 2000, survival obstruction for de Branges RH program.

### Hilbert-Polya / Berry-Keating / Connes

- Polya, Hilbert-Polya conjectural spectral framing.
- Berry, 1986, quantum chaos and Riemann zeros.
- Berry-Keating, 1999, `H=xp`.
- Connes, 1999, trace formula in noncommutative geometry and zeros of zeta.
- Meyer and Deninger work around adelic/cohomological programs.

### Selberg / Automorphic

- Selberg, 1956, trace formula and Selberg zeta.
- Standard Maass form and Eisenstein spectral decomposition references.

### Weil / Deligne / Grothendieck

- Weil, 1948/1949, curves and finite-field zeta functions.
- Grothendieck, l-adic cohomology and Lefschetz trace formula.
- Deligne, `La conjecture de Weil. I`, 1973.
- Deligne, `La conjecture de Weil. II`, 1980.

### Iwasawa

- Iwasawa, 1959 onward, cyclotomic theory.
- Kubota-Leopoldt, 1964, p-adic L-functions.
- Mazur-Wiles, 1984, cyclotomic Iwasawa main conjecture.
- Wiles, 1990, totally real fields.
- Skinner-Urban, 2014, GL2 main conjectures.

### Beurling-Nyman

- Nyman, 1950, Uppsala thesis.
- Beurling, 1955, closure problem related to zeta.
- Baez-Duarte, 2003, strengthened Nyman-Beurling criterion.
- Baez-Duarte, 2005, invariant unitary operators.
- Bercovici-Foias, 1984, generalizations.

### Mertens

- Stieltjes, 1885 historical claims around Mobius summatory bounds.
- Mertens, 1897, strong square-root conjecture.
- Littlewood, 1912, weak Mertens criterion equivalent to RH.
- Odlyzko and te Riele, 1985, disproof of the Mertens conjecture.

### Random Matrix Theory

- Montgomery, 1973, pair correlation.
- Odlyzko numerical computations of high zeta zeros.
- Diaconis-Shahshahani, 1994, random unitary statistics.
- Keating-Snaith, 2000, characteristic polynomial moment conjectures.

---

## 14. Corpus-Inclusion Recommendations

### 14.1 `adequacy.tex`

Recommended additions:

- Framework RH-Carrier Dichotomy Theorem.
- CRCFT as a CRE-carrier foreclosure taxonomy.
- Cascade Reduction Theorem as a case-study theorem.
- Bridge Impossibility Corollary in a bridge/admissibility section.

Rationale:

`adequacy.tex` governs residual closure, carrier adequacy, and legal promotion.
The dichotomy and CRCFT are adequacy-level results.

### 14.2 `needles.tex`

Recommended additions:

- CTMT as a terminal layer-dissolving condition.
- The matrix-element interface template:

```text
M(alpha,beta,gamma)=<a_alpha,P_beta b_gamma>.
```

Rationale:

`needles.tex` tracks how probes dissolve residuals or terminate at missing
interfaces.  CTMT is exactly a terminal-interface classification.

### 14.3 `paper/sections/`

Recommended new section:

```text
RH carrier audit and typed foreclosure taxonomy
```

Suggested subsection order:

1. Burnol/Sonine reduction and Branch C numerical foreclosure.
2. CTMT.
3. CRCFT.
4. Dichotomy.
5. Non-CRE native closures.
6. Bridge Impossibility.
7. Open external content.

### 14.4 Standalone Corpus Files

Recommended files:

- `anti_loc/CTMT.md`;
- `anti_loc/CRCFT.md`;
- `anti_loc/RH_carrier_dichotomy.md`;
- `anti_loc/RH_framework_audit.md`.

This document supplies the fourth item.

---

## 15. Open Questions

### 15.1 Burnol `kappa`

The main external mathematical target is:

```text
explicit P_{L_a^Gamma} projection formula
```

or an equivalent formula for

```text
kappa_{a,w}(tau).
```

Open subquestions:

- Is the projection formula already present in Burnol's Sonine papers under a
  different normalization?
- Can the J_0 Hankel resolvent be transported to the Fourier-cosine/zeta
  completed Sonine carrier?
- Is there a de Branges subspace formula giving `P_{L_a^Gamma}` directly?
- Can Branch A or B be decided without `kappa` by a new structural route?

### 15.2 Branch C Universality

Step 196 gives an extended numerical dataset.

Open subquestions:

- Can the nonzero `L_{rho,k}(G)` pattern be proved analytically for an open
  set of legal `G`?
- Can the finite-difference `k=1` diagnostics be replaced by analytic
  derivative formulas?
- Does normalized `|L|/||G||` obey a structural law?

### 15.3 Beurling-Nyman Finite Interfaces

The Beurling-Nyman Gram chain shows slow logarithmic decay.

Open subquestions:

- Can the arithmetic Gram computation be made stable for much larger `N`?
- Can finite Gram condition numbers be related to CRCFT-TE finite-data
  limitations?
- Can the Baez-Duarte asymptotic be expressed as a typed residual promotion
  theorem?

### 15.4 Mertens Finite Data

Mertens finite data are computable but not promotable.

Open subquestions:

- Can Mertens finite-window obstruction be compared formally with
  finite-window Calkin blindness?
- Can the strong-Mertens refutation be encoded as a typed sidecar no-go?
- Can weak-Mertens promotion be related to Beurling-Nyman Gram promotion?

### 15.5 Dichotomy Coverage

Open subquestions:

- Are there CRE carriers outside CTMT, TE, and BF?
- Are there non-CRE closure carriers without complete native ledgers that form
  a third branch?
- Are statistical carriers like RMT better captured by a separate evidence
  taxonomy?

---

## 16. Current State Summary

The RH framework currently supplies:

- a complete Branch C reduction theorem;
- a Branch C full-carrier numerical foreclosure record;
- a precise Branch A/B `kappa` external interface;
- CTMT;
- CRCFT;
- the RH-Carrier Dichotomy;
- the Bridge Impossibility Corollary in partial form;
- native closure certificates for Selberg, Weil-Deligne, and Iwasawa;
- finite numerical evidence for Beurling-Nyman;
- CRE target-equivalence classifications for Beurling-Nyman and Mertens.

What remains external:

- the Burnol projected Sonine kernel theorem;
- any coverage-conjecture refuter;
- any non-circular bridge from non-CRE native closure to Riemann RH;
- any direct proof of Riemann RH.

The practical next route is Path 1:

```text
resolve kappa or prove it unnecessary.
```

The strategic next route is Path 3:

```text
find an in-scope carrier that refutes the dichotomy coverage conjecture.
```

No such refuter was found in this iteration.

---

## 17. Artifact Provenance

Primary step artifacts:

- Step 172: cascade reduction theorem.
- Step 180: CTMT.
- Step 183: CRCFT.
- Step 187: Dichotomy.
- Step 189: Bridge Impossibility Corollary.
- Steps 175-176 and 196: Branch C numerical foreclosure.
- Steps 194-195: Beurling-Nyman numerical refinement.
- Steps 185, 186, 190: non-CRE native closures.
- Steps 193 and 197: fresh CRE criteria, Beurling-Nyman and Mertens.

This audit document is Step 198's foundational-corpus integration deliverable.

---

## 18. Final Audit Verdict

```text
V_audit_integrated
```

All requested components are consolidated:

- foundational typed conditions;
- corollary;
- carrier classifications;
- numerical experiments;
- retained no-gos;
- Path 1/2/3 strategic conclusion;
- corpus recommendations;
- open questions.

The document is intentionally a framework audit, not a proof document.

