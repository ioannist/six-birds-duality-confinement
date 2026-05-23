# Step 153: Pulled Zero-Evaluator Kernel Formula

## Purpose

Step 152 reduced direct residual exclusion to

\[
r_{\ell,\rho,k}=(I-P_\infty)[\tau_{-\ell},P_\infty]J_a^*Y^a_{\rho,k}.
\]

Step 153 computes the pulled evaluator

\[
\eta^a_{\rho,k}=J_a^*Y^a_{\rho,k}
\]

as a projected Burnol/Sonin reproducing kernel and rewrites the direct-exclusion problem as a commutator-vanishing theorem.

## Main formula

Let

\[
M(f)(s)=\pi^{-s/2}\Gamma(s/2)\widehat f(s)
\]

be the completed right Mellin transform. Let \(K_a^\Gamma(s,w)\) be the reproducing kernel of the completed Mellin image of Burnol's augmented Sonine space \(L_a\). Then

\[
\mathcal M_\Gamma(Y^a_{w,k})(s)=\partial_{\bar w}^{k}K_a^\Gamma(s,w)
\]

under the Hilbert convention, with \(\partial_w^k\) replacing \(\partial_{\bar w}^k\) under Burnol's analytic bilinear convention.

If

\[
T_a=\mathcal M_\Gamma J_a\mathcal U_\infty^{-1},
\]

then the pulled evaluator is

\[
\boxed{
\mathcal U_\infty(J_a^*Y^a_{w,k})
=
T_a^*\partial_{\bar w}^{k}K_a^\Gamma(\cdot,w).
}
\]

## Ambient Hardy shadow

The exact kernel is a Sonine projection of an ambient Hardy kernel:

\[
K_a^\Gamma(\cdot,w)=P_{\mathcal L_a^\Gamma}K_a^{\Gamma,\mathrm{amb}}(\cdot,w),
\]

where

\[
K^{\Gamma,\mathrm{amb}}_a(s,w)
=
A_\infty(s)\overline{A_\infty(w)}
\frac{s}{s-1}\overline{\frac{w}{w-1}}
\frac{a^{s+\bar w-1}}{s+\bar w-1}.
\]

The projection \(P_{\mathcal L_a^\Gamma}\) is load-bearing. Dropping it gives only a Hardy-shadow formula, not the Burnol/Sonin evaluator.

## Commutator residual

The normalized log shift obeys

\[
\widehat{\tau_\ell f}(s)=e^{\ell(1/2-s)}\widehat f(s).
\]

Thus \(\tau_{-\ell}\) is multiplication by

\[
m_\ell(s)=e^{-\ell(1/2-s)}.
\]

The direct-exclusion residual is

\[
\boxed{
\widehat r_{\ell,w,k}
=
(I-\mathsf P_\infty)M_{m_\ell}\mathsf P_\infty
T_a^*\partial_{\bar w}^{k}K_a^\Gamma(\cdot,w).
}
\]

Equivalently,

\[
\boxed{
\widehat r_{\ell,w,k}
=
(I-\mathsf P_\infty)[M_{m_\ell},\mathsf P_\infty]
T_a^*\partial_{\bar w}^{k}K_a^\Gamma(\cdot,w).
}
\]

Therefore

\[
H_R=0
\iff
r_{\ell,\rho,k}=0
\quad\forall \ell,\rho,k.
\]

## Verdict

Raw log-shift transport does not create a \(\zeta(s)\)-factor. It only multiplies the Mellin transform by a nonvanishing factor and triangularly mixes derivative evaluators at the same zero.

So direct exclusion is not automatic. It requires one of:

1. genuine Burnol/co-Poisson factorization;
2. projection reduction of the pulled evaluator family under the shifted Sonin projection;
3. carrying \(\Xi^{\rm BC}\) as an explicit adequacy residual.

Status:

\[
\boxed{\texttt{direct\_exclusion\_not\_earned}.}
\]

## Next step

Step 154 should audit whether

\[
(I-\mathsf P_\infty)M_{m_\ell}\mathsf P_\infty
T_a^*\partial_{\bar\rho}^{k}K_a^\Gamma(\cdot,\rho)
\]

vanishes for the actual projected Sonine kernel, or whether \(\Xi^{\rm BC}\) remains nonzero.
