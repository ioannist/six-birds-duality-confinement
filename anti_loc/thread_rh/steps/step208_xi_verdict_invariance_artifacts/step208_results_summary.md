# Step 208 Results Summary

## Verdict

`V_xi_invariant_partial`.

The verdict-invariance tactic was executed under both sampled candidate
transport formulas from Step 207:

- CAND1: Burnol 2002 boundary-kernel sample.
- CAND2: Burnol 2004 [19] zeta-dual single-term sample.

The finite-grid Step 173 operator used
\[
P f = f - \operatorname{sinc}*f-\sum_{n<N}\Psi_n\langle \Psi_n,f\rangle,
\qquad
C f=(I-P)e^{i\ell\tau}Pf,
\quad \ell=\log 2.
\]

## Commutator Matrices

Main run: 200 tau nodes, 24 PSWF terms.

CAND1 produced small entries:
\[
\max |c_{ij}^{(1)}| = 9.03975455\cdot 10^{-11}, \qquad
\|c^{(1)}\|_F = 9.03980135\cdot 10^{-11}.
\]

CAND2 produced very large entries:
\[
\max |c_{ij}^{(2)}| = 2.20220836\cdot 10^{16}, \qquad
\|c^{(2)}\|_F = 2.20332330\cdot 10^{16}.
\]

## Compressed-HS Residual

Using the inherited unnormalized formula
\[
\Xi_{\rm matrix\_source}=\operatorname{tr}(G^{-1}c^\dagger G^{-1}c),
\]
with the Step 204/207 Gram matrix:

| Candidate | Xi value | |Xi| | error bound | candidate verdict |
|---|---:|---:|---:|---|
| CAND1 | 0.0287707490 - 4.5574e-6 i | 2.8771e-2 | 1.4685e14 | inconclusive |
| CAND2 | 8.1516e65 + 9.8051e61 i | 8.1516e65 | 2.6239e66 | inconclusive |

The error bound is dominated by applying the very ill-conditioned inherited
`G^{-1}` to finite-grid c-matrix variation. The calculation therefore cannot
certify closure, nonzero obstruction, or candidate-dependence.

## Robustness

PSWF terms `{12,24,36}`, a 100-node subsample, and ell values
`log 2`, `log 3`, and `1.0` were tested. The candidate scale difference is
stable: CAND1 stays near `1e-10` in `max|c|`; CAND2 stays near `1e16`.

## Consequence

The closure verdict is not invariant in a certified sense. The diagnostic
exposes the same downstream issue as Steps 204-207: the inherited Gram matrix
and transport normalization must be sharpened before `Xi_matrix_source` can be
decided numerically.
