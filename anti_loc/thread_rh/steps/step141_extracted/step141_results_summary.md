
# Step 141: Omega-Compatible Density Audit on Burnol/Sonine Residual Windows

## Main result

This step audits the new density defect introduced by the Omega-compatible dictionary route:

\[
\epsilon_{B\to\Omega,N}
=
\|(I-P_{\Omega,N})M_{R,N}G_{R,N}^{-1/2}\|.
\]

This is a spanning/adequacy residual, not a column-norm bound.

## Verdict

The finite algebra is closed, but the density theorem is not earned:

\[
\epsilon_{B\to\Omega,N}\to0
\]

is not implied by Burnol completeness alone, because Burnol/co-Poisson density does not automatically preserve Heap--Soundararajan-style Omega block cutoffs.

A positive floor may be enough:

\[
\epsilon_{B\to\Omega,N}\le \epsilon<1.
\]

If this fails, the missed sector

\[
\Xi_{B\to\Omega,N}
=
M_{R,N}^{*}(I-P_{\Omega,N})M_{R,N}
\]

is a genuine residual.

## Bicriteria source condition

The restricted BPRZ source route now needs two independent floors:

\[
1-\epsilon_{B\to\Omega,N}^{2}
\]

and

\[
1-\delta_{R,K,N}^{2}.
\]

The effective source strength is

\[
\Lambda_N^{\Omega}
\gtrsim
\gamma_q
(1-\epsilon_{B\to\Omega,N}^{2})
(1-\delta_{R,K,N}^{2}).
\]

So the route is viable if both defects stay below one and the source strength diverges, subject to fixed/exhaustive tail promotion.

## Nonclaim

Step 141 does not prove RH. It does not prove Omega-compatible density. It gives the exact density gate and the residual if the gate fails.
