# References Selection

Status: Phase 5 produced 2026-05-23.

Purpose: audit log of bibliography selection per paper, with
rationale. Tsiokos-only entries are the in-scope citation pool for
the prep arc; external classical references are deferred to the
user's end-of-process external-reference pipeline.

Per the locked global decision in `paper/notes/prep-plan.md`:
**max 3 Tsiokos references per paper**. The shared
`paper/references.bib` holds all canonical bibkeys; each paper's
`main.tex` points at `references.bib` (symlinked from each paper's
directory).

## Per-paper picks

### Paper 1 — Duality Confinement

| Bibkey | Role | Body section(s) of first cite |
| --- | --- | --- |
| `TsiokosFoundationsII2026` | F2 (admissibility, FATCD, primitive roles) — used when the body invokes Foundations II vocabulary (e.g., closure formation per Foundations I; FATCD records as the audit substrate). First cite in `sec:framework`. | `sec:framework` |
| `TsiokosFoundationsIII2026` | F3 (BirdInt judgment, visibility tags, gate-status family, claim records) — used in App D when the formalization disclosure references the F3 alias surface (e.g., `F3VisibilityTag` aliases in `Terminology.lean`). | `sec:framework`, `app:formalization` |
| `TsiokosRHviaSDTC2026` | Sibling cross-reference; used ONLY in the two sanctioned forward-reference paragraphs in `sec:involutive_ledger` (RH worked example) and `sec:master_theorem` (Paper 2 as worked single-substrate validation). | `sec:involutive_ledger`, `sec:master_theorem` |

Paper 1 references count: 3 Tsiokos. **Limit not exceeded.**

### Paper 2 — RH closure

| Bibkey | Role | Body section(s) of first cite |
| --- | --- | --- |
| `TsiokosSDTC2026` | Sibling paper substantive citation: imports the master theorem, the SDTC structural-law framing, the V-Differential trace-state-only column condition for RH. First cite in `sec:framework` (V-Differential placement) and again in `sec:recognition_source` (SDTC framing) and `sec:landing_chain` (master theorem). | `sec:framework`, `sec:recognition_source`, `sec:landing_chain` |
| `TsiokosFoundationsII2026` | F2 — used when invoking the seven admissibility schemas that `Sel^!_{ζ,tr}` carries (proposal §4.2 admissibility claim) and the BirdInt-related vocabulary. | `sec:sat_sel_shell`, `sec:landing_chain` |
| `TsiokosFoundationsIII2026` | F3 — used in App D for the BirdInt judgment shape rendering the conditional theorem (proposal §2 final BirdInt judgment) and for the no-overreading-suppression theorem cited in the six-gates audit. | `sec:landing_chain` (BirdInt judgment form), `app:formalization` (six-gates audit detail) |

Paper 2 references count: 3 Tsiokos. **Limit not exceeded.**

## Deferred external classical references

The following external classical works WILL be cited in the final
papers but are deferred to the user's end-of-process external-
reference pipeline. The drafting arc treats these as paper-prose
mentions with deferred bibkeys (codex drafts the prose with
references to "the classical Douglas factorization", etc., without
inserting `\cite{}` for the deferred references).

### Paper 1 — Duality Confinement deferred externals

| Classical work | Where it would be cited |
| --- | --- |
| Douglas, R. G., "On majorization, factorization, and range inclusion of operators on Hilbert space" (1966) | `sec:domination` (Douglas factorization classical statement) |
| Standard trace-class operator theory references (e.g., Reed–Simon Vol. I; Simon "Trace Ideals and Their Applications") | `sec:anti_invariant_ledger` (trace functional + Loewner order classical statements); `sec:domination` (operator-theoretic Loewner dominance) |
| Standard operator inequality references (Bhatia "Matrix Analysis"; Horn–Johnson "Topics in Matrix Analysis") | `sec:direct_confinement` (Markov inequality classical form); `sec:exhaustive_squeeze_and_budgets` (AM-GM classical form) |

### Paper 2 — RH closure deferred externals

| Classical work | Where it would be cited |
| --- | --- |
| Standard analytic number theory references (Titchmarsh "The Theory of the Riemann Zeta-Function"; Edwards "Riemann's Zeta Function"; Iwaniec–Kowalski "Analytic Number Theory") | `sec:involution_and_ledger` (completed zeta, functional equation, nontrivial-zero ledger classical statements) |
| Selberg trace formula references (Selberg's original papers; Iwaniec "Spectral Methods of Automorphic Forms"; Bump "Automorphic Forms and Representations") | `sec:sat_sel_shell` (Selberg trace formula context for the saturated trace closure) |
| Weil positivity references (Weil's original "Sur les 'formules explicites' de la théorie des nombres"; Bombieri's expository papers) | `sec:scope_and_nonclaims` (Weil positivity as readout-level vs source-level discussion) |
| Hilbert–Pólya, Connes adelic / NCG, de Branges, Beurling–Nyman classical references | `sec:scope_and_nonclaims`, `sec:discussion` (classical RH attack barrier framing) |

## Decision log

| Date | Decision | Rationale |
| --- | --- | --- |
| 2026-05-23 | Shared `paper/references.bib` for both papers | Both papers share the same Foundations II/III references; symlinked from each paper's directory. Hiddenness uses the same convention. |
| 2026-05-23 | Tsiokos-only in the prep arc | Per locked global decision in prep-plan.md: external classical references deferred to user's end-of-process pipeline. Drafting arc prose may reference classical works descriptively ("the classical Douglas factorization") without inserting `\cite{}` for deferred bibkeys. |
| 2026-05-23 | Max 3 Tsiokos refs per paper | Same constraint as hiddenness, kept for parity. Both papers land at exactly 3. |
| 2026-05-23 | One-way sibling cross-citation | Paper 2 cites Paper 1 substantively (`TsiokosSDTC2026` in three body sections); Paper 1 cites Paper 2 only in two forward-reference paragraphs (`TsiokosRHviaSDTC2026`). Per `paper/notes/cross-paper-boundary.md`. |
| 2026-05-23 | No Foundations I bibkey | Foundations I (`ClosureLadder`) is referenced via Foundations II/III citations and via the framework apparatus citations in `sec:framework`. A standalone `TsiokosFoundationsI2026` bibkey is not in the per-paper picks above (it would consume one of the 3 Tsiokos slots without adding substantive citation content). If F1 becomes a load-bearing standalone citation during drafting, add as `TsiokosFoundationsI2026` and adjust the per-paper picks. |

## Validation against drafting needs

Cross-check against the per-axis section-outline:

- DC paper sections invoking citations:
  - `sec:framework`: F2, F3 (closure formation, FATCD, BirdInt context)
  - `sec:involutive_ledger`: F2 forward-reference to RH (Paper 2 worked example)
  - `sec:domination`: deferred external (Douglas 1966)
  - `sec:master_theorem`: forward-reference to Paper 2
  - `sec:exhaustive_squeeze_and_budgets`: deferred external (AM-GM standard)
  - `app:formalization`: F3 (BirdInt + visibility tags via Terminology aliases)

- RH paper sections invoking citations:
  - `sec:framework`: F2, F3, Paper 1 (V-Differential placement)
  - `sec:involution_and_ledger`: deferred external (standard analytic number theory)
  - `sec:sat_sel_shell`: F2 (admissibility schemas), deferred external (Selberg trace formula context)
  - `sec:recognition_source`: Paper 1 (SDTC framing)
  - `sec:landing_chain`: Paper 1 (master theorem), F3 (BirdInt judgment)
  - `sec:scope_and_nonclaims`: deferred external (classical RH barriers)
  - `sec:discussion`: deferred external (classical positioning)
  - `app:formalization`: F3 (no-overreading-suppression theorem)

No coverage gaps for the in-scope Tsiokos-only set. Deferred
external references are flagged consistently per paper.
