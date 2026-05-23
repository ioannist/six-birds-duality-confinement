# Step 121 Results Summary

Step 121 constructs the regularized co-Poisson/Müntz Dirichlet shadow gate for the Burnol-to-Dirichlet readability problem.

The main correction is that ordinary critical-line partial sums of zeta are not lawful shadows. The shadow must be regularized by a declared Müntz/co-Poisson subtraction, by an approximate functional equation, or by another audited response-space construction.

For a Burnol/co-Poisson atom with right Mellin transform \(\widehat g(s)\), the native target is

\[
B g(s)=\zeta(s)\widehat g(s).
\]

A smooth Müntz shadow is

\[
Z_X^\omega(s)=\sum_{n\ge1}\omega(n/X)n^{-s}-X^{1-s}\Omega(1-s),
\]

where \(\Omega\) is the Mellin transform of the cutoff. The shadow target is

\[
B_X^{reg}g(s)=Z_X^\omega(s)\widehat g(s),
\]

plus a declared residual/tail.

The decisive defect is the angular gap

\[
\delta_{BD,N}^{reg}=
\|(I-P_{D,N}^{reg})B_NG_{B,N}^{-1/2}\|.
\]

Equivalently,

\[
\Xi_{BD,N}^{reg}=B_N^*(I-P_{D,N}^{reg})B_N.
\]

Thus regularized readability is an adequacy problem, not a scalar approximation problem.

The hybrid visibility bound is

\[
\epsilon_{hyb,N}
\le
\epsilon_{B,N}+\delta_{BD,N}^{reg}+\tau_{reg,N},
\]

hence

\[
c_{hyb,N}
\ge
1-(\epsilon_{B,N}+\delta_{BD,N}^{reg}+\tau_{reg,N})^2.
\]

The source route needs

\[
G_{\mathcal X,N}\succeq\gamma_NH_N,
\qquad
\gamma_Nc_{hyb,N}\to\infty,
\]

plus fixed/exhaustive tail promotion.

The step does not close the gate. It defines the gate and rejects the naive shadow.
