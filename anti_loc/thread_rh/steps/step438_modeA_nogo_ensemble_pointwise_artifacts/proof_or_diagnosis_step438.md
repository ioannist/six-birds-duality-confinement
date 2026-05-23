# Step 438 Proof

## 1. Universality is test-function convergence

Erdős-Schlein-Yau and Tao-Vu universality theorems identify the limiting integrals of compactly supported test functions against the normalized `k`-point correlation measures. The limiting object is the sine-kernel determinantal process. This is precisely a statement about local statistical measures.

The manager-provided anchor states the key structural property explicitly:

> Vague convergence is the most natural notion of convergence for discrete random matrix ensembles; for such ensembles, the correlation function is a discrete measure, and so one does not expect convergence to a continuous limit in any stronger sense than the vague sense.

Thus the theorem does not name, determine, or converge to a fixed deterministic eigenvalue sequence.

## 2. Correlation data do not determine pointwise spectra

If a deterministic sequence `{a_n}` has a given bulk pair-correlation limit, then the shifted sequence `{a_n + c}` has the same normalized pair-correlation limit. More generally, local correlation functions are invariant under global shifts and under many transformations that preserve normalized local spacing statistics. Hence the sine-kernel limit cannot distinguish `{gamma_n}` from `{gamma_n+1}`.

Montgomery's pair correlation conjecture says the normalized zeta-zero pair correlation matches the GUE pair-correlation function. Odlyzko verifies this numerically to high precision. These facts place zeta zeros in the GUE universality class statistically; they do not construct a deterministic operator with the zeta-zero ordinates as exact eigenvalues.

## 3. Ensemble realization selection is external data

A GUE matrix has random eigenvalues. To obtain exact zeta zeros as a realization one would need to condition the ensemble on the event `lambda_n = gamma_n` for all `n`, or define a deterministic selection rule using the zeta zeros. The first has probability zero in the continuous ensemble; the second imports the target sequence and is tautological.

## 4. Conclusion

Random matrix universality is a valid explanation for local statistics but cannot discharge the pointwise Hilbert-Polya target. Therefore `C_ensemble_distributional_not_pointwise` is promoted to theorem-grade structural impossibility for ensemble-only Route 2 constructions.
