# Step 122 — Regularized co-Poisson/Müntz Shadow Angular-Gap Estimate

## Status
Completed as a conditional construction theorem and obstruction audit.

Step 122 chooses the smooth Müntz/co-Poisson shadow as the first lawful Burnol-to-Dirichlet regularization and derives the exact angular-gap criterion that would make Burnol/co-Poisson visibility readable by Dirichlet/Hecke source frames.

This step does **not** prove RH and does **not** prove that the angular gap tends to zero. It identifies the three estimates that would be sufficient.

---

## Chosen regularization

Choose a smooth cutoff \(\omega\) with \(\omega(x)=1\) near zero and rapid decay or compact support. Let

\[
\Omega(w)=\int_0^\infty \omega(x)x^{w-1}\,dx.
\]

Define the regularized Müntz shadow

\[
Z_X^\omega(s)
=
\sum_{n\ge1}\omega(n/X)n^{-s}
-
X^{1-s}\Omega(1-s).
\]

The correction term

\[
X^{1-s}\Omega(1-s)
\]

is mandatory. It is the Müntz/pole channel.

---

## Contour residual

For \(0<\Re(s)<1\), Mellin inversion gives

\[
Z_X^\omega(s)=\zeta(s)+\mathcal E_X^\omega(s),
\]

where

\[
\mathcal E_X^\omega(s)
=
\frac{1}{2\pi i}
\int_{(-\eta)}X^w\Omega(w)\zeta(s+w)\,dw.
\]

On a finite vertical window \(|\Im(s)|\le T\), this gives a bound of the schematic form

\[
\sup_{|\Im(s)|\le T}|\\mathcal E_X^\omega(s)|
\le
C_{\omega,\eta,A}(1+T)^A X^{-\eta}.
\]

So the regularized shadow can approximate \(\zeta(s)\), but only through a lawful contour/tail record.

---

## Burnol-to-Dirichlet shadow defect

For a Burnol/co-Poisson atom \(g\), the exact target is

\[
B g(s)=\zeta(s)\widehat g(s).
\]

The regularized shadow is

\[
B_X^{\rm reg}g(s)=Z_X^\omega(s)\widehat g(s).
\]

The residual is

\[
T_X^\omega g(s)=B g(s)-B_X^{\rm reg}g(s)
=-\mathcal E_X^\omega(s)\widehat g(s).
\]

For finite Burnol windows \(Y_{B,N}\), the normalized angular-gap defect is

\[
\delta_{BD,N}^{\rm reg}
=
\|(I-P_N^{\rm reg})B_NG_{B,N}^{-1/2}\|.
\]

Equivalently,

\[
\Xi_{BD,N}^{\rm reg}
=
B_N^*(I-P_N^{\rm reg})B_N.
\]

This is the exact \(\Xi\)-style adequacy residual for what the regularized Dirichlet-readable shadow misses.

---

## Main conditional theorem

If the declared regularized shadow has three controlled defects:

\[
\epsilon_{\rm Mell,N}
=
\text{Mellin/Dirichlet model error},
\]

\[
\tau_{\rm M,N}
=
\text{Müntz contour residual},
\]

\[
\kappa_{\rm tail,N}
=
\text{coefficient/support/tail defect},
\]

then

\[
\boxed{
\delta_{BD,N}^{\rm reg}
\le
\epsilon_{\rm Mell,N}+\tau_{\rm M,N}+\kappa_{\rm tail,N}.
}
\]

Therefore

\[
\boxed{
 c_{BD,N}^{\rm reg}
 \ge
 1-(\epsilon_{\rm Mell,N}+\tau_{\rm M,N}+\kappa_{\rm tail,N})^2.
}
\]

So the regularized shadow is accepted if the sum of these three errors tends to zero. A positive visibility floor may still be enough if the character/source strength grows fast enough.

---

## The new obstruction

The regularized route has a length-balancing problem.

The Müntz residual wants

\[
X_N^\eta \gg A_N(1+T_N)^A.
\]

But Heap–Soundararajan style moment technology wants the Dirichlet polynomial to remain short relative to the family/conductor parameter.

So the active compatibility gate is:

\[
\boxed{
\text{large enough for Müntz accuracy, short enough for moment estimates.}
}
\]

This is the new quantitative obstruction.

---

## Route consequence

The source route now requires

\[
\gamma_Nc_{\rm hyb,N}\to\infty,
\]

where

\[
c_{\rm hyb,N}
\ge
1-(\epsilon_{B,N}+\n\epsilon_{\rm Mell,N}+\tau_{\rm M,N}+\kappa_{\rm tail,N})^2.
\]

Here:

- \(\epsilon_{B,N}\) is Burnol geometric exhaustion;
- \(\epsilon_{\rm Mell,N}\) is Mellin/Dirichlet modeling error;
- \(\tau_{\rm M,N}\) is the smooth Müntz contour error;
- \(\kappa_{\rm tail,N}\) is the coefficient/support/tail defect;
- \(\gamma_N\) is Hecke/Dirichlet source strength.

---

## Bottom line

Step 122 makes the smooth Müntz/co-Poisson shadow lawful and converts the readability question into a quantitative angular-gap estimate.

The active obstruction is now:

\[
\boxed{
\epsilon_{\rm Mell,N}+\tau_{\rm M,N}+\kappa_{\rm tail,N}
}
\]

and the active compatibility target is:

\[
\boxed{
\gamma_N\left(1-(\epsilon_{B,N}+\epsilon_{\rm Mell,N}+\tau_{\rm M,N}+\kappa_{\rm tail,N})^2\right)	o\infty.
}
\]

## Next step

Step 123 should attack the balanced-length theorem: choose growth regimes for \(X_N,T_N\), Burnol atom complexity, and source family/conductor size, then determine whether the three shadow errors can be made small while Heap–Soundararajan style source strength still grows.
