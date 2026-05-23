# Step 433 Results Summary

## Substrate

`M_0` is a genus-2 compact hyperbolic surface specified by non-arithmetic Fenchel-Nielsen/Bers data. The cuff `ell_1=2` gives trace `2cosh(1)=e+e^{-1}`, transcendental, excluding arithmetic Fuchsian origin.

## Operator

```text
H_space = L^2(M_0,dmu_M),
H = Delta_M = -div grad.
```

`H` is self-adjoint natively because `M_0` is compact and boundaryless.

## Critical Test

Selberg's trace formula is available and natural, but the geometric side is primitive closed-geodesic lengths `ell(gamma)`, not `log p`. The short length sample in `length_spectrum_step433.csv` does not match `log` rational primes structurally or numerically.

## Constraint Result

Passes: `C_arithmetic_independence`, `C_self_adjoint_native`, `C_no_adelic_substrate`, `C_no_tautology`.

Fails / partial-fails: `C_trace_formula_compatibility`, `C_explicit_formula_natural`, `C_GUE_natural`; Gate 5 fails because there is no small-spectrum match.

## Verdict

Stage I retracts. New active failure-shape constraint proposed:

```text
C_length_spectrum_arithmetic_mismatch:
A non-arithmetic Selberg-analog substrate must explain why its primitive closed-geodesic length spectrum equals or canonically transforms to log rational primes; otherwise the Selberg trace formula is only formally analogous to Weil's explicit formula.
```

## Required Citations

- Route 2 dispatch 2026-05-19: Route 1 parked; Route 2 operator-theoretic non-descending active.
- Active basis cited verbatim: `C_arithmetic_independence`, `C_self_adjoint_native`, `C_no_adelic_substrate`, `C_no_tautology`, `C_explicit_formula_natural`, `C_GUE_natural`, `C_trace_formula_compatibility`.
- References: Selberg trace formula (Selberg 1956), Bers/Maskit/Fenchel-Nielsen construction of Teichmuller space, Hejhal/Sarnak quantum chaos context for hyperbolic surfaces.
