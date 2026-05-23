# Step 104: Shifted Sonin/prolate off-diagonal compactness test

## Main result

The raw archimedean Sonin off-diagonal block

\[
B_a=S_\lambda\tau_a(I-S_\lambda)
\]

is **not compact** for any nonzero shift \(a\).

The witness is a sequence of high-frequency packets supported near the edge of the cutoff interval. Before shifting, the packets lie in the non-Sonin sector. After a nonzero shift, their support exits the spatial cutoff and their Fourier mass exits the low-frequency cutoff. Thus their shifted images become nearly Sonin, with norm bounded away from zero, while the original packets converge weakly to zero. A compact operator cannot do that.

## Consequence

The compactness shortcut for the semilocal cross-term cannot come from raw transported Sonin geometry alone. A single finite-place log-shift already creates a noncompact off-diagonal block.

So the compactness route survives only if the actual semilocal prolate projection supplies extra cancellation beyond the raw archimedean Sonin projection. Otherwise the finite-place cross-term has a genuine noncompact sector and must be handled by Hecke/Dirichlet source absorption.

## Route implication

The active fork is now:

1. prove a semilocal prolate correction cancels the boundary-packet sector; or
2. accept that the compactness shortcut fails and build the source-coercivity lower frame for the noncompact sector.

## Nonclaim

This does not prove that the full Connes--Consani--Moscovici semilocal prolate residual is noncompact. It proves that the raw shifted Sonin block is noncompact. The actual semilocal prolate operator could still repair this, but that repair must be proved.
