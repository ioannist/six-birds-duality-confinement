# Step 108 Summary — Finite Burnol/Sonine Boundary Dictionary and Coefficient Map

## Completed step

Step 108 defines the finite boundary-packet model needed for the Hecke/Dirichlet source-coercivity route.

The new finite objects are:

\[
Y_{\mathcal B,N},
\qquad
R_N:Y_{\mathcal B,N}\to\mathbb C^{\mathcal N_N},
\qquad
F_{\mathcal B,N}=R_N^*G_{\mathcal X,N}R_N.
\]

Here:

- \(Y_{\mathcal B,N}\) is a finite Burnol/Sonine boundary-packet dictionary;
- \(R_N\) maps a boundary-packet recombination to short Dirichlet-polynomial coefficients;
- \(G_{\mathcal X,N}\) is the finite character Gram/source matrix;
- \(F_{\mathcal B,N}\) is the induced boundary source frame.

## Main theorem

If

\[
R_N^*G_{\mathcal X,N}R_N
\succeq
\Lambda_NG_{\mathcal B,N}
-
E_{\mathrm{coef},N}
-
E_{\mathrm{win},N},
\]

then every finite boundary-packet recombination is charged by the source family.

If this holds with

\[
\Lambda_N\to\infty
\]

and the finite boundary dictionaries exhaust the completed Burnol/Sonine boundary sector with vanishing tail, then the completed boundary-packet obstruction is source-absorbed.

## Key rank obstruction

If \(R_N\) is not injective on \(Y_{\mathcal B,N}\), then no character family can produce a strict lower frame on the finite boundary dictionary.

That is the operator-valued upgrade of the warning from Step 107:

\[
\text{a scalar mollifier lower bound does not imply a matrix lower frame.}
\]

## Numerical toy check

The finite model used:

- a discrete Sonin projection built from time and Fourier cutoff kernels;
- shifted boundary blocks \(S\tau_m(I-S)\);
- top singular vectors as a finite boundary dictionary;
- a short Dirichlet dictionary \(n^{-1/2-it}\);
- finite character Gram matrices.

Sanity data:

- boundary dictionary dimension: 16
- Dirichlet support size: 51
- mean coefficient residual: 0.2171
- max coefficient residual: 0.7595
- full-character boundary min eigenvalue in stable toy: 0.1249

The numerics are only algebra checks, not RH evidence.

## Strategic conclusion

\[
\boxed{
\text{prove a matrix lower-frame bound for }R_N^*G_{\mathcal X,N}R_N
\text{ on Burnol/Sonine boundary dictionaries.}
}
\]

This is where Burnol's Sonine completeness, Heap--Soundararajan's dual-mollifier strength, and finite/Hecke character orthogonality must be composed.
