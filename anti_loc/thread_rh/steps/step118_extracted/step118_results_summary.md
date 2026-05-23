
# Step 118 summary: Burnol-to-Dirichlet hybrid dictionary theorem

Step 118 defines a source-readable hybrid dictionary for the residual sector
\[
\Xi^{BC}.
\]

The key correction is that \(c_N\) is a spanning/exhaustivity residual, not a column-norm estimate.

The hybrid dictionary has two parts:

\[
D_N^{hyb}=D_N^{Dir}+D_N^{B\to Dir}.
\]

The first part is the ordinary short Dirichlet coefficient dictionary used by the Heap--Soundararajan source mechanism.

The second part is a Burnol/co-Poisson-native family, transported into Dirichlet coefficient space through a declared shadow map.

The central theorem is:

If Burnol atoms exhaust the residual sector with residual \(\epsilon_{B,N}\), and their Dirichlet shadows have normalized defect \(\delta_{BD,N}\), then

\[
\epsilon_{hyb,N}\le \epsilon_{B,N}+\delta_{BD,N},
\]

and therefore

\[
c_{hyb,N}\ge 1-(\epsilon_{B,N}+\delta_{BD,N})^2.
\]

If the character/source Gram satisfies

\[
G_{\mathcal X,N}\succeq \gamma_NH_N,
\]

then

\[
R_N^*G_{\mathcal X,N}R_N
\succeq
\gamma_N c_{hyb,N}G_{R,N}.
\]

Thus the effective residual source strength is

\[
\Lambda_N=\gamma_Nc_{hyb,N}.
\]

The route requires

\[
\gamma_Nc_{hyb,N}\to\infty
\]

after fixed/exhaustive residual-tail promotion.

The new obstruction is the Burnol-to-Dirichlet shadow defect:
\[
\delta_{BD,N}.
\]

If the Burnol atoms see the residual sector but cannot be represented by source-readable Dirichlet coefficients, then they improve geometric visibility but do not produce a lawful Hecke/Dirichlet source frame.

The next step is to define the shadow map explicitly from co-Poisson/Mellin data and estimate \(\delta_{BD,N}\).
