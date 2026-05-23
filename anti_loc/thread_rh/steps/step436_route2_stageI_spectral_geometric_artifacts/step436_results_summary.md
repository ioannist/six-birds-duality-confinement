# Step 436 Results Summary

## Attempt

Route 2 Stage I under `G_spectral_geometric_non_adelic`, the last of the four dispatch-named Route 2 grammars. Prior retracts:

- Step 433 `G_selberg_analog_non_arithmetic`: retracted at length-spectrum/log-prime mismatch and GUE naturality.
- Step 434 `G_quantum_semiclassical`: retracted at boundary-phase arithmetic smuggling and absent log-prime action structure.
- Step 435 `G_universal_forced_GUE`: retracted at distributional-not-pointwise spectrum matching.

## Candidate

The selected non-adelic NCG substrate is the circle spectral triple

```text
(C^infty(S^1), L^2(S^1, spinors), D_R = -i R^{-1} d/dtheta).
```

It is self-adjoint natively and avoids adèles.

## Main calculation

After removing the zero mode,

```text
zeta_D(s) = Tr |D_R|^{-s} = 2 R^s zeta(s).
```

This is the strongest positive result available inside the grammar: a non-adelic spectral triple whose spectral zeta is exactly a nonzero entire factor times the Riemann zeta function.

## Failure

The Route 2 target is not spectral-zeta equality. It requires a deterministic self-adjoint operator with

```text
Spec(H) = { gamma : zeta(1/2 + i gamma) = 0 }.
```

Here `Spec(D_R)=R^{-1}Z`, not the zero ordinates. The construction also has no natural prime-side explicit formula and no GUE mechanism.

## Verdict

Stage I retracts. New constraint distilled:

`C_spectral_zeta_not_spectrum`: matching zeta as a spectral zeta function is not Hilbert-Polya pointwise spectral realization.

This completes the fourth dispatch-named grammar attempt, but does not by itself declare Route 2 globally exhausted.
