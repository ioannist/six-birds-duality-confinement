# Step 354 Results Summary

Mode C Stage IV applied the four-step refinement program.

## 1. Converse Probe

The step 353 weighted geometric transfer closes the in-sample magnitude OL
residual to near zero (`max lambda <= 2.71e-4`) but does not supply an
operator/kernel-preserving Hecke-to-zeta transfer and fails target hold-out.

Conclusion: magnitude-only OL closure is over-strong as an H6 translation.
The residual must include phase and operator-compatibility components.

## 2. Decomposition

Computed 35 representative complex cells (`7 chi x 5 k x rho_1`):

- mean magnitude residual: `1.4051`
- mean phase residual: `1.5006`
- phase-dominant cells: `18/35`
- magnitude-dominant cells: `17/35`
- per-k mean-magnitude variance: `0.1605`
- per-chi mean-magnitude variance: `0.0369`

Both magnitude and phase are material.  The k-direction contributes more
variance than the chi-direction on this representative slice.

## 3. Earning At Scale

Mode C provides intermediate content beyond the prior catalog verdict
`V-NC bridge-failure`: a finite residual, a blocking gate, transfer-search
objective, converse probe, and typed decomposition.

## 4. Equivalence Audit

Mode C OL is structurally distinct from Branch C foreclosure, elementary
bridge ansätze, H1-H5 framework lanes, and CRCFT-BF bridge-failure labeling.

## Verdict

`V_mode_C_stage_IV_passes_refined_residual_needs_phase_operator_terms`.

Proceed to Stage V with a refined residual:

`lambda_total = (lambda_mag, lambda_phase, lambda_operator)`.
