# Step 117: Residual coefficient-map instantiation for \(\Xi^{\rm BC}\)

## Completed result

This step instantiates the finite residual-sector coefficient map

\[
R_N:Y_{R,N}\to \mathbb C^{I_N}
\]

for the boundary-to-co-Poisson residual

\[
\Xi^{\rm BC}_{\ell,a}=\mathfrak B_{\ell,a}^*\Pi_{Y_a}\mathfrak B_{\ell,a}.
\]

The key correction is now built in:

\[
\boxed{c_{R,N}\text{ is a spanning residual of a constructible family, not a column-norm bound.}}
\]

## Exact finite identity

Let

\[
M_{R,N}:Y_{R,N}\to H_N^{\rm resp}
\]

synthesize a finite residual-sector window, and let

\[
D_N:\mathbb C^{I_N}\to H_N^{\rm resp}
\]

synthesize the declared coefficient dictionary. Let \(P_N\) be the projection onto \(\operatorname{Ran}D_N\), and set

\[
R_N=D_N^\dagger M_{R,N},
\qquad
E_{{\rm coef},N}=(I-P_N)M_{R,N}.
\]

Then

\[
\boxed{
R_N^*H_NR_N
=G_{R,N}-E_{{\rm coef},N}^*E_{{\rm coef},N}.
}
\]

Therefore

\[
\boxed{
c_{R,N}=1-\left\|E_{{\rm coef},N}G_{R,N}^{-1/2}\right\|^2.
}
\]

This is the finite \(\Xi\)-style adequacy residual for translating the residual sector into coefficient language.

## Source-frame consequence

If

\[
G_{\mathcal X,N}\succeq \gamma_NH_N
\]

and

\[
R_N^*H_NR_N\succeq c_{R,N}G_{R,N},
\]

then

\[
\boxed{
R_N^*G_{\mathcal X,N}R_N
\succeq
\gamma_Nc_{R,N}G_{R,N}.
}
\]

So the effective residual source strength is

\[
\boxed{\Lambda_{R,N}=\gamma_Nc_{R,N}.}
\]

The route requires \(\gamma_Nc_{R,N}\to\infty\), plus completed tail/exhaustivity.

## Toy finite audit

The finite toy model is not RH evidence. It only checks the algebra of the residual visibility gate.

Representative results:

| case | atoms | \(c_{R,N}\) | mean visibility |
|---|---:|---:|---:|
| short Dirichlet | 127 | 0.0000 | 0.0535 |
| Burnol/co-Poisson-like | 96 | 0.00331 | 0.4131 |
| hybrid | 143 | 0.00827 | 0.5230 |

The main lesson is that average visibility can improve while worst-direction visibility remains weak. The gate is a true worst-direction adequacy condition.

## Interpretation

The source route has two independent burdens:

\[
\gamma_N=\text{arithmetic source strength},
\]

\[
c_{R,N}=\text{residual-sector coefficient visibility}.
\]

Heap--Soundararajan-style moment technology targets \(\gamma_N\). Burnol/co-Poisson density and coefficient construction target \(c_{R,N}\).

## Bottom line

Step 117 converts the residual-source route into the exact obligation

\[
\boxed{
G_{\mathcal X,N}\succeq\gamma_NH_N,
\qquad
R_N^*H_NR_N\succeq c_{R,N}G_{R,N},
\qquad
\gamma_Nc_{R,N}\to\infty.
}
\]

The next step is to replace the toy coefficient dictionary by a declared Burnol-to-Dirichlet hybrid atom family and prove or refute a genuine residual visibility theorem.
