# Step 84: CND Audit of the Paired Completed Weil Candidate

This step audits the paired-feature strategy that replaced separated diagonal accounting after the no-free-diagonal obstruction.

## Main conclusion

The finite prime slot and normalized gamma slot each pass the paired shift-feature gate. Their sum is continuous negative definite (CND), hence admits a positive paired shift-difference feature representation.

But this does **not** prove the RH Douglas bridge. It only says the candidate prime-plus-gamma paired carrier is a lawful positive feature. The remaining analytic task is proving that the actual completed Weil form is equal to or dominated by this paired carrier plus lawful pole/tail records.

## Key theorem

A translation-invariant paired shift feature

\[
q_\mu[f]=\int \|\tau_a f-f\|_2^2\,d\mu(a)
\]

has Fourier symbol

\[
\Psi_\mu(\xi)=2\int(1-\cos(a\xi))\,d\mu(a).
\]

Thus a symbol is representable by positive paired shift features exactly when it has the symmetric Levy-Khinchine / CND form

\[
\Psi(\xi)=c\xi^2+2\int(1-\cos(a\xi))\,d\mu(a),\quad c\ge0,\ \mu\ge0.
\]

## Prime slot

For finite prime cutoff,

\[
\Psi_{\rm pr,L}(\xi)=2\sum_n w_{n,L}(1-\cos(\xi\log n)),\quad w_{n,L}\ge0.
\]

This is CND by construction.

## Gamma slot

The normalized zeta gamma symbol is

\[
\Psi_\Gamma(\xi)=\frac12\int_0^\infty \frac{e^{-t/4}}{1-e^{-t}}\left(1-\cos\frac{\xi t}{2}\right)dt\ge0.
\]

It is CND as a paired singular difference form.

## Warning

Pointwise nonnegative is not enough. The symbol \(\xi^4\) is nonnegative but not CND. With points \([-1,0,1]\) and coefficients \([1,-2,1]\), the CND quadratic is positive:

\[
\sum_{i,j}c_ic_j(x_i-x_j)^4=24>0.
\]

So a generic positive spectral symbol is not automatically a lawful paired shift feature.

## Status

Accepted as candidate feature:

\[
\Psi_{\rm pr,L}+\Psi_\Gamma.
\]

Still open:

\[
q_Z\le q_{\rm pr+\Gamma}+q_{\rm pole}+q_{\rm tail}+e_L
\]

on the completed anti-invariant core, with tail and core-to-full records.

## Layman interpretation

The prime and gamma pieces can be written as honest positive “compare a function to its shifted copy” accounts. That is good.

But we have not shown that this account is the actual completed Weil account. We have only shown that one candidate account is mathematically lawful.

The remaining RH work is to prove that the real zeta explicit formula pays every off-critical displacement through this paired account, plus pole and tail records, without hidden signed debt.
