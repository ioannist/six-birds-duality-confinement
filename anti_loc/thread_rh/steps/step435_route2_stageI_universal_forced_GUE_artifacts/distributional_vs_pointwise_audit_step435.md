# Step 435 Distributional vs Pointwise Audit

Hilbert-Polya requires a deterministic self-adjoint operator `H` such that

```text
Spec(H) = { gamma_n : zeta(1/2 + i gamma_n) = 0 }.
```

GUE universality supplies a different claim:

```text
local eigenvalue statistics of random matrices converge to the same limiting statistics observed/conjectured for zeta zeros.
```

This is distributional, not pointwise. The ensemble does not choose the actual zeta-zero sequence. Selecting a realization whose eigenvalues equal `{gamma_n}` has probability zero and, if imposed, is tautological. Altering the ensemble measure to concentrate on the zeta-zero realization would smuggle the arithmetic data into the measure.

Therefore the construction passes many operator-theoretic constraints but fails the central Route 2 target: pointwise spectrum equality.

## New constraint

```text
C_ensemble_distributional_not_pointwise:
Random matrix ensemble constructions may match zeta-zero statistics via universality, but Hilbert-Polya requires a deterministic operator with pointwise spectrum. Choosing or conditioning an ensemble realization to equal zeta zeros is tautological or arithmetic smuggling.
```
