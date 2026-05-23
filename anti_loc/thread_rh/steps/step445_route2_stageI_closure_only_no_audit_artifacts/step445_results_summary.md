# Step 445 Results Summary

## Scope and package

Finite scope: first 10 nontrivial zeros plus `-2,-4,-6,-8`. Package `P'=(K^L,Xi,[K^D+S])` has no separate audit currency.

## Numerics

A1-A4 pass formally. Schur identity error: `1.3177747429e-82`. `Xi_Z=0.0036 I`. Target capacity gap eigenvalues: `['0.004', '0.004', '0.004']`. Off-critical control gap has negative eigenvalue(s): `['-0.021392', '-0.013672', '-0.005216']`.

## Gates and absence

6 gates: 4 pass, 1 partial, 1 fail. Five Mode A absence checks: 4 pass, 1 fail (Step 444 audit tension reappears as implicit capacity semantics). Three audit-specific absence checks pass.

## Verdict

Stage I retracts. New constraint: `C_capacity_bound_semantic_audit_smuggling`. The formal capacity bound survives, but interpreting it as zero-localization requires an external audit or RH-equivalent `Theta^D` semantics.
