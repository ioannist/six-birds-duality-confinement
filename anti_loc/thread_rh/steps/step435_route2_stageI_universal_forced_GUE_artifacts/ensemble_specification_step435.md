# Step 435 Ensemble Specification

## Canonical GUE

For each `N`, define

```text
H_N = H_N^*
```

on `H_space_N = C^N`, with diagonal entries real Gaussian and off-diagonal entries complex Gaussian satisfying Hermitian symmetry. With the usual `1/sqrt(N)` scaling, the empirical eigenvalue distribution converges to the Wigner semicircle law in the bulk.

## Operator status

Each finite `H_N` is self-adjoint by Hermiticity. The large-`N` object is an ensemble limit, not a single deterministic operator unless a specific realization or deterministic limit operator is additionally specified.

## TRS / GUE

The canonical GUE is complex Hermitian and not invariant under the real time-reversal symmetry appropriate to GOE. Thus the refined TRS-breaking part of `C_GUE_natural` is structurally satisfied.

## Primitive vocabulary

The ensemble specification uses finite-dimensional complex Hilbert spaces, Gaussian measures, and Hermitian matrices. It contains no zeta zeros, primes, modular forms, adeles, ideles, or boundary-condition phases.
