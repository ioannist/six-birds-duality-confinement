# Step 119: Explicit Burnol-to-Dirichlet Shadow Map

This step derives the actual finite shadow map from declared Burnol/co-Poisson atoms to Dirichlet/Hecke-readable coefficients.

The Burnol response image is

\[
B_Nc(s)=\zeta(s)\sum_{j\in J_N}c_j\widehat g_j(s),
\]

where \(\widehat g_j(s)=\int_0^\infty g_j(t)t^{-s}\,dt\) and the co-Poisson identity gives \(M(\mathcal Cg_j)(s)=\zeta(s)\widehat g_j(s)\).

The Dirichlet synthesis is

\[
D_Na(s)=\sum_{n\in\mathcal N_N}a_n n^{-s}.
\]

The optimal Burnol-to-Dirichlet shadow map is

\[
\boxed{A_N=(D_N^*W_ND_N)^\dagger D_N^*W_NB_N.}
\]

It is the least-squares projection of the Burnol/co-Poisson response image onto the source-readable Dirichlet coefficient range.

The exact shadow defect is

\[
\boxed{\delta_{BD,N}=\|(I-P_{D_N})B_NG_{B,N}^{-1/2}\|,}
\]

and the visibility constant is

\[
\boxed{c_{BD,N}=1-\delta_{BD,N}^2.}
\]

So the active adequacy residual is

\[
\boxed{\Xi_{BD,N}=B_N^*W_N(I-P_{D_N})B_N.}
\]

This measures what the Burnol/co-Poisson response sees that Dirichlet/Hecke source coefficients cannot read.

The convolution shadow formula is:

\[
\widehat g_j(s)\approx\sum_{r\in\mathcal R_N}b_j(r)r^{-s},
\qquad
Z_X(s)=\sum_{m\le X}m^{-s},
\]

then

\[
Z_X(s)\widehat g_j(s)
\approx
\sum_{n}\left(\sum_{mr=n}b_j(r)\right)n^{-s}.
\]

Thus

\[
\boxed{(A_N^{\rm conv})_{n,j}=\sum_{mr=n}b_j(r).}
\]

The defect splits into three gates:

1. generator-readability defect;
2. zeta-tail defect;
3. multiplicative support-tail defect.

Step 119 does **not** prove \(\delta_{BD,N}\to0\). It gives the exact map, the exact residual, and the next mathematical obligation.

The finite plots are projection sanity checks only, not RH evidence.
