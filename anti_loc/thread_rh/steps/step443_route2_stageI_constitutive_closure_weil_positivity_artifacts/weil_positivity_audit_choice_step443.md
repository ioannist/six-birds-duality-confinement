# Step 443 Weil-Positivity Audit Choice

## Chosen mechanism

This third `G_constitutive_closure` carrier attempt chooses Weil's explicit-formula positivity as the audit currency.

Primary anchor: Weil 1952, "Sur les formules explicites de la théorie des nombres premiers".

Verbatim criterion used in this step's typed form:

```text
RH iff for every admissible autocorrelation test function f = g * g*,
W[f] := sum_rho fhat(gamma_rho) >= 0.
```

The explicit formula decomposes this same form into zero side, archimedean side, prime side, and trivial-zero correction.

## Why this is structurally distinct

- Step 441 used a zero-height audit currency and failed by height smuggling.
- Step 442 used de Branges kernel positivity and failed by kernel-positivity derivability.
- Step 443 uses Weil explicit-formula positivity, where the audit object is a hermitian quadratic form on test functions.

## Expected tension

Concrete evaluation of `W[f]` requires either zero heights or the prime/von Mangoldt side. A purely formal symbol `W` avoids that arithmetic input but does not yield a numerical residual or derived positivity.
