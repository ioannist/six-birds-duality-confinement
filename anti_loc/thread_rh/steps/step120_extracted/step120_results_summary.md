
# Step 120: Burnol-to-Dirichlet Shadow Asymptotic Criterion

## Result
The Burnol-to-Dirichlet readability problem is now an angular-gap problem. For a Burnol/co-Poisson synthesis map

\[
B_N:Y_{B,N}\to H_N
\]

and a declared Dirichlet-readable synthesis map

\[
D_N:\mathbb C^{I_N}\to H_N,
\]

with \(P_{D,N}\) the projection onto \(\operatorname{Ran}D_N\), the shadow defect is

\[
\delta_{BD,N}=\|(I-P_{D,N})B_NG_{B,N}^{-1/2}\|.
\]

Equivalently,

\[
\Xi_{BD,N}=B_N^*(I-P_{D,N})B_N
\]

is the Burnol-to-Dirichlet adequacy residual.

## Criterion
The shadow defect tends to zero precisely when the declared Dirichlet-readable subspaces approximate the Burnol target ranges uniformly on normalized growing windows:

\[
\sup_{0\ne y\in Y_{B,N}}
\frac{\operatorname{dist}(B_Ny,\operatorname{Ran}D_N)}{\|B_Ny\|}\to0.
\]

Strong convergence on each fixed atom is not enough because the Burnol windows grow.

## If the criterion fails
The limiting missed shadow is

\[
\Xi_{BD}=B^*(I-P_D)B.
\]

If this is nonzero, the hybrid dictionary has a readability blind spot. That blind spot must be absorbed by a separate source frame, shown compact/tail, or declared as a scoped nonclaim.

## Regularization warning
Burnol/co-Poisson gives the target

\[
M(\mathcal Cg)(s)=\zeta(s)\widehat g(s),
\]

but naive partial sums of \(\zeta(s)\) are not lawful shadows on the critical line. The Dirichlet shadow must be regularized by a declared co-Poisson/Müntz, approximate-functional-equation, smoothed Euler, or equivalent audited construction.

## Source consequence
If

\[
\epsilon_{B,N}=\text{Burnol geometric exhaustion defect},
\]

and

\[
\delta_{BD,N}=\text{Dirichlet readability defect},
\]

then

\[
c_{\mathrm{hyb},N}\ge 1-(\epsilon_{B,N}+\delta_{BD,N})^2.
\]

With a source lower frame

\[
G_{\mathcal X,N}\succeq\gamma_NH_N,
\]

the effective residual source strength is

\[
\Lambda_{R,N}=\gamma_Nc_{\mathrm{hyb},N}.
\]

The route needs

\[
\gamma_Nc_{\mathrm{hyb},N}\to\infty
\]

after fixed/exhaustive tail promotion.

## Next step
Step 121 should construct the actual regularized co-Poisson/Müntz Dirichlet shadow family and determine whether it gives \(\delta_{BD,N}\to0\), a positive visibility floor, or a nonzero missed shadow sector.
