# Step 436: Arithmetic Independence Audit

## Prompt and ledger context

The prompt lists 11 active Route 2 constraints and notes a counting ambiguity. The repository ledger at attempt time contains 10 active Route 2 rows:

1. `C_arithmetic_independence`
2. `C_self_adjoint_native`
3. `C_no_adelic_substrate`
4. `C_no_tautology`
5. `C_explicit_formula_natural`
6. `C_GUE_natural`
7. `C_trace_formula_compatibility`
8. `C_length_spectrum_arithmetic_mismatch`
9. `C_boundary_phase_arithmetic_smuggling`
10. `C_ensemble_distributional_not_pointwise`

This attempt audits those 10 ledger-active constraints and adds the Step 436 failure-shape constraint `C_spectral_zeta_not_spectrum` as the eleventh row in `constraints_and_gates_check_step436.csv`.

## Arithmetic independence result

The selected substrate `C^infty(S^1), L^2(S^1), D_R` does not use adèles, idèles, class field theory, modular forms, Hecke operators, primes, or zeta zeros in its primitives. In that narrow construction sense, it passes arithmetic-independence and non-adelic-substrate checks.

## Why the attempt still retracts

The positive identity

```text
zeta_D(s) = 2 R^s zeta(s)
```

is not the Hilbert-Polya target. It realizes the Riemann zeta function as a spectral zeta of the integer-lattice Dirac spectrum, not the zero ordinates as the operator spectrum. The operator has a completely integrable, arithmetic-free, time-reversal-symmetric, picket-fence spectrum. It gives neither GUE statistics nor a natural primes-side explicit formula.

## New constraint distilled

`C_spectral_zeta_not_spectrum`: Matching the Riemann zeta function as `Tr |D|^{-s}` or matching the zeros of a spectral zeta function does not satisfy the Route 2 target unless the operator spectrum itself is the zeta-zero ordinate set. Spectral-zeta equality is a different object from pointwise Hilbert-Polya spectral realization.

This constraint is distinct from step 435's `C_ensemble_distributional_not_pointwise`: step 435 failed by being statistical rather than pointwise; step 436 fails by matching the wrong spectral object.
