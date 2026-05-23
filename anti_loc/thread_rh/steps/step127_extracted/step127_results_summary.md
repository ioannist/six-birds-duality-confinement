# Step 127: Source-weighted matrix lower-frame import

## Verdict
The finite unweighted character frame is settled. The remaining analytic import is a coefficient-uniform weighted quadratic-form theorem.

The required theorem has the form

\[
\sum_{\chi\in\mathcal X_q} w_\chi\left|\sum_{n\in\mathcal N_N}a_n\chi(n)\right|^2
\ge
\gamma_{q,w}\|a\|_{H_N}^2
\]

for every residual coefficient vector \(a\), not just for one selected mollifier.

## Imported literature platforms

- CIS / asymptotic large sieve: baseline platform for coefficient-uniform primitive-character bilinear forms.
- Pratt--Robles: t-aspect perturbed-moment model with a general Dirichlet polynomial; useful for import grammar.
- Bui--Pratt--Robles--Zaharescu: q-aspect twisted second moment with arbitrary polynomial; closest to the required \(|L|^2|A|^2\) weighted Gram.
- Tang--Wu 2025: current hybrid mixed-moment platform over primitive characters.
- Gao--Wu--Zhao 2025: mollified q-aspect fourth moment; gives concrete shortness constraints.

## Framework contribution
The framework contribution is not the AFE, large sieve, or mollifier-length mechanics. It is the operator-valued lower-frame demand and the \(\Xi\)-adequacy bookkeeping:

\[
R_N^*G_{q,w}R_N\succeq \gamma_{q,w}c_{\rm hyb,N}G_{R,N}.
\]

## Active gap
Existing scalar/literature results must be audited for coefficient-uniformity:

\[
\operatorname{Main}(a)\ge c\|a\|^2,
\qquad
|\operatorname{Err}(a)|\le \varepsilon c\|a\|^2
\quad\forall a.
\]

Without this uniform statement, the source-weighted lower-frame gate remains unclosed.
