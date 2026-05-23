# Step 291 Results Summary — Branch A Burnol Corpus Audit

## Scope

Network audit queried arXiv for `au:"Burnol"`, returning 40 entries. I fetched/text-extracted 28 zeta/Sonine/Fourier/Hankel/operator papers and marked 12 recent Kempner/missing-digit or otherwise Branch-A-unrelated entries as out of scope. Web search also checked Burnol's University of Lille publication page and external index pages.

Corrected inherited bibliography detail: `math/0203120` is **Two complete and minimal systems associated with the zeros of the Riemann zeta function**; `math/0112254` is **On Fourier and Zeta(s)**.

## Branch A Need

Branch A closure would require one of:

1. a faithful Calkin symbol for the `[M_zeta, P_lambda]` Sonine projection class;
2. a closed form for the essential norm `Phi_max = 0.4904766200...`;
3. a structural identity relating that constant to Burnol/Sonine/de Branges data.

## Audit Result

No fetched Burnol text contains the required terminology or statement. Corpus keyword search over PDF and source text gave zero hits for `Calkin`, `essential norm`, `norme essentielle`, `0.490476`, `M_zeta`, and `M_ζ`.

The closest matches are adjacent, not resolving:

- `math/0208121`: Theorem 4 gives the orthogonal Sonine projection; Theorem 8 gives `E_lambda` and the de Branges realization.
- `math/0203120`: Theorems 3.1 and 3.2 give complete/minimal systems associated with zeta zeros.
- `math/0112254`: Section 6 introduces `HP_lambda`, `Z_rho_k^lambda`, and evaluator identities.
- `math/9812012` / `math/9902080`: local commutator operators are bounded, but they are `i[log|p|, log|q|]`, not `[M_zeta, P_lambda]`; `math/9902080` explicitly leaves the exact archimedean commutator norm as an open-interest item.

## Top Verbatim Evidence

- Burnol `math/0208121`, Section 4, p.5: “Sa projection orthogonale sur l’espace de Sonine `K_lambda` est donnée par la formule ...”
- Burnol `math/0208121`, Section 5, p.6: “La fonction `E_lambda(w)` est une fonction entière satisfaisant la condition de de Branges.”
- Burnol `math/0203120`, Section 3, p.6: “The vectors `Y_rho_k^a` ... are a minimal system ... if and only if `a <= 1`.”
- Burnol `math/0112254`, Section 6.3, p.35: “the linear forms `f -> M(f)^(k)(w)` are continuous and correspond to (unique) vectors `Z_w_k^lambda`.”
- Burnol `math/9812012`, p.9: “Theorem: The commutator operator is bounded.”
- Burnol `math/9902080`, Notes, p.27: “It would also be interesting to know the exact operator norm of the commutator operator at the archimedean places.”

## Disposition

Burnol's corpus contains the Branch A background machinery, but not the cascade-needed Calkin/essential-norm lemma. Branch A's score-1 classification is now paper-grounded against the fetched Burnol corpus. Extended literature remains possible, but Burnol is not the source of the missing lemma.

Final verdict: `V_branch_A_burnol_audit_confirms_no_lemma`.
