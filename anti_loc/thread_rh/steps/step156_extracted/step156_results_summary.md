# Step 156: Xi^BC residual-kernel Schatten/tail audit

## Object

The active residual is

\[
\Xi^{\rm BC}_{\ell,a}
=
\mathfrak B_{\ell,a}^{*}\Pi_{Y_a}\mathfrak B_{\ell,a}\succeq0.
\]

Using the pulled zero-evaluator family

\[
\eta^a_{ho,k}=J_a^*Y^a_{ho,k},
\]

and the projected commutator block

\[
C_\ell=(I-P_\infty)M_{m_\ell}P_\infty,
\]

the residual kernel is

\[
\mathcal R_\ell((w,k),(z,j))
=
\langle C_\ell\eta^a_{w,k}, C_\ell\eta^a_{z,j}\rangle.
\]

Equivalently, with residual synthesis map

\[
E_{\ell,a}e_z=C_\ell\eta_z,
\]

we have

\[
\mathcal R_\ell=E_{\ell,a}^{*}E_{\ell,a}.
\]

---

## Main theorem

For any bounded residual synthesis map \(E\), with \(R=E^*E\):

\[
R\text{ compact}\iff E\text{ compact},
\]

\[
R\in \mathcal S_p\iff E\in \mathcal S_{2p},
\]

and

\[
R\in\mathcal S_1\iff E\in\mathcal S_2.
\]

Thus

\[
\boxed{
\mathcal R_\ell\in\mathcal S_1
\iff
E_{\ell,a}\text{ is Hilbert--Schmidt}.
}
\]

This is the exact Schatten/tail criterion for \(\Xi^{\rm BC}\).

---

## Tail promotion

If \(Q_N\uparrow I\) strongly on the zero-evaluator coordinate space, then:

- compact \(\mathcal R_\ell\) gives operator-norm tail payment;
- trace-class \(\mathcal R_\ell\) gives trace-tail payment:

\[
\operatorname{tr}((I-Q_N)\mathcal R_\ell(I-Q_N))\to0.
\]

So compactness or Schatten control would be enough to reopen the completed-tail route.

---

## Essential test

Let

\[
\mathcal E_a=
\overline{\operatorname{span}\{\eta^a_{\rho,k}\}}.
\]

The compactness question is now exactly:

\[
\boxed{
\pi(C_\ell|_{\mathcal E_a})\stackrel{?}{=}0
}
\]

in the Calkin algebra.

If the restricted Calkin class is nonzero and the pulled zero-evaluator system is cofinal in that essential sector, then \(\Xi^{\rm BC}\) is not compact.

---

## Verdict

\[
\boxed{
\Xi^{\rm BC}\text{ is not classified as compact/tail-payable yet.}
}
\]

The residual is still active. Compactness is not inherited from Burnol, CCM, or the source-frame construction. It has to be proved on the pulled zero-evaluator closure.

---

## Current status

| route | status |
|---|---|
| exact exclusion | open |
| compact/tail payment | reduced to restricted Calkin test |
| trace-class payment | reduced to Hilbert--Schmidt residual synthesis |
| positive source-frame absorption | blocked as closure shortcut |
| scoped residual | active |

---

## Next step

Step 157 should perform the essential-support test:

\[
\pi(C_\ell|_{\mathcal E_a})\stackrel{?}{=}0.
\]

If yes, the compact/tail route reopens. If no, \(\Xi^{\rm BC}\) is a genuine noncompact adequacy residual.
