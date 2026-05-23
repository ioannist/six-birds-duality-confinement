# Step 152: Adjoint zero-evaluator transport formula

## Main object

The shifted residual block is

\[
\mathfrak B_{\ell,a}=J_aP_\infty\tau_\ell(I-P_\infty).
\]

The direct Burnol/co-Poisson exclusion target is

\[
\Pi_{Y_a}\mathfrak B_{\ell,a}=0.
\]

Equivalently, for every zero evaluator,

\[
\mathfrak B_{\ell,a}^*Y^a_{\rho,k}=0.
\]

## Adjoint transport formula

Assuming \(P_\infty=P_\infty^*\) and \(\tau_\ell^*=\tau_{-\ell}\),

\[
\boxed{
\mathfrak B_{\ell,a}^*Y^a_{\rho,k}
=
(I-P_\infty)\tau_{-\ell}P_\infty J_a^*Y^a_{\rho,k}.
}
\]

Equivalently,

\[
\boxed{
\mathfrak B_{\ell,a}^*Y^a_{\rho,k}
=
(I-P_\infty)[\tau_{-\ell},P_\infty]J_a^*Y^a_{\rho,k}.
}
\]

So direct residual exclusion is a commutator-vanishing theorem.

## Mellin shift formula

Under the right-Mellin convention

\[
\widehat f(s)=\int_0^\infty f(t)t^{-s}\,dt,
\]

the unitary log-shift \(\tau_\ell\) acts as

\[
\widehat{\tau_\ell f}(s)=e^{\ell(1/2-s)}\widehat f(s).
\]

Therefore raw shifts act on zero-evaluator derivatives by triangular same-zero mixing:

\[
(\tau_\ell^*Y_{\rho,k})(f)
=
 e^{\ell(1/2-\rho)}
\sum_{r=0}^k {k\choose r}(-\ell)^{k-r}Y_{\rho,r}(f).
\]

This preserves the zero-evaluator span, but it does not annihilate it.

## Verdict

A raw log-shift does not create a \(\zeta\)-factor and does not force

\[
\Pi_{Y_a}\mathfrak B_{\ell,a}=0.
\]

The obstruction is exactly the Sonin/prolate projection commutator

\[
(I-P_\infty)[\tau_{-\ell},P_\infty]J_a^*Y^a_{\rho,k}.
\]

Thus \(H_R=0\) is not earned. The active residual remains

\[
\Xi^{\rm BC}_{\ell,a}
=\mathfrak B_{\ell,a}^*\Pi_{Y_a}\mathfrak B_{\ell,a}.
\]
