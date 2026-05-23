# Step 151 — Direct residual-exclusion / adequacy theorem for `H_R`

## Verdict

The positive source-frame / positive fixed-ledger trace squeeze has become diagnostic rather than proof-producing. Step 151 therefore pivots to the direct Burnol residual-exclusion route.

The desired direct theorem is

\[
H_R=0,
\qquad\text{equivalently}\qquad
\Pi_{Y_a}\mathfrak B_{\ell,a}=0
\]

for every finite-place log-shift mode \(\ell\).

Step 151 does **not** prove this direct exclusion. It gives the exact criteria, the strongest lawful certificate, and the residual if the criterion fails.

---

## Main objects

\[
\mathfrak B_{\ell,a}=J_aP_\infty\tau_\ell(I-P_\infty)
\]

is the shifted Sonin/prolate boundary block transported into Burnol's \(L_a\)-carrier.

\[
Y_a=\overline{\operatorname{span}\{Y^a_{\rho,k}\}}
\]

is Burnol's nontrivial-zero evaluator span.

\[
P_a=Y_a^\perp
\]

is Burnol's co-Poisson subspace for \(a<1\).

The completed residual carrier is

\[
H_R=\overline{\operatorname{span}\{\operatorname{Ran}\Pi_{Y_a}\mathfrak B_{\ell,a}\}}.
\]

---

## Direct exclusion criteria

For each \(\ell\), the following are equivalent:

\[
\Pi_{Y_a}\mathfrak B_{\ell,a}=0,
\]

\[
\operatorname{Ran}\mathfrak B_{\ell,a}\subseteq P_a,
\]

\[
M(\mathfrak B_{\ell,a}u)^{(k)}(\rho)=0
\quad\forall u,\rho,0\le k<m_\rho,
\]

\[
\mathfrak B_{\ell,a}^{*}Y^a_{\rho,k}=0
\quad\forall \rho,k.
\]

Assuming \(P_\infty=P_\infty^*\) and \(\tau_\ell^*=\tau_{-\ell}\), the adjoint formula is

\[
\boxed{
\mathfrak B_{\ell,a}^{*}Y^a_{\rho,k}
=(I-P_\infty)\tau_{-\ell}P_\infty J_a^*Y^a_{\rho,k}.
}
\]

So the direct route reduces to this exact transported zero-evaluator test.

---

## Co-Poisson certificate

A sufficient certificate is

\[
M(\mathfrak B_{\ell,a}u)(s)=\zeta(s)\alpha_{\ell,u}(s),
\]

with lawful Burnol support, pole, endpoint, and Sonine records.

If this holds, every nontrivial zero evaluator annihilates the boundary packet, and

\[
\operatorname{Ran}\mathfrak B_{\ell,a}\subseteq P_a.
\]

---

## Obstruction

A raw log-shift does not create a \(\zeta\)-factor. In Mellin variables, a shift/scaling operation contributes a nonvanishing exponential or power multiplier.

Therefore the implication

\[
\text{shifted Sonin/prolate packet}
\Rightarrow
\zeta(s)\text{-divisible Mellin transform}
\]

is not automatic.

Any zeta-factorization must come from a genuine co-Poisson synthesis, a deeper projection cancellation, or an additional declared source/quotient record.

---

## Active residual

If direct exclusion is not proved, the residual is

\[
\boxed{
\Xi^{\rm BC}_{\ell,a}
=
\mathfrak B_{\ell,a}^{*}\Pi_{Y_a}\mathfrak B_{\ell,a}.
}
\]

It satisfies

\[
\langle u,\Xi^{\rm BC}_{\ell,a}u\rangle
=
\|\Pi_{Y_a}\mathfrak B_{\ell,a}u\|^2.
\]

So \(\Xi^{\rm BC}\) is exactly what the shifted boundary packet sees outside the Burnol/co-Poisson complement.

---

## Step 151 bottom line

The direct residual-exclusion route is the right pivot after the source-budget obstruction, but it is not closed by the current construction.

The next analytic object is

\[
\boxed{
(I-P_\infty)\tau_{-\ell}P_\infty J_a^*Y^a_{\rho,k}.
}
\]

If this vanishes for all zero evaluators, then \(H_R=0\). If it does not, its squared norm is the first direct measurement of \(\Xi^{\rm BC}\).

## Next step

**Step 152: adjoint zero-evaluator transport formula.**

Target: compute or estimate

\[
(I-P_\infty)\tau_{-\ell}P_\infty J_a^*Y^a_{\rho,k}
\]

for a single shift \(\ell=\log p\), and decide whether the direct exclusion route has a real cancellation mechanism or whether \(\Xi^{\rm BC}\) remains nonzero.
