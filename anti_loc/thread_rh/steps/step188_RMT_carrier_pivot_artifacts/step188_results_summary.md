# Step 188: RMT Carrier Pivot

Verdict:

`RMT_verdict = V_RMT_outside_dichotomy_scope`.

Carrier declaration:

The RMT typed context is a statistical comparison carrier:

```tex
C_RMT(N,T) = (U_N or H_N, {gamma_j: 0 < gamma_j <= T})
```

where `U_N` is Haar-random CUE or `H_N` is GUE, and `{gamma_j}` denotes
Riemann-zero ordinates, typically after assuming RH so all zeros are on
`Re(s)=1/2` and local scaling is well-defined.

Native probes:

- pair correlation `R_2`;
- n-level correlations `R_n`;
- nearest-neighbor spacing statistics;
- characteristic-polynomial moments.

Dissolving probes:

- computed zero ordinates;
- empirical spacing/correlation/moment data.

Residual:

`Xi_RMT` is a statistical distance between RMT predictions and zero data, for
example an `L^2` pair-correlation distance, a Kolmogorov-Smirnov distance for
spacing distributions, or moment-difference metrics.

CRE audit:

RMT is not a closure carrier for RH. Exact agreement of `Xi_RMT=0` would be a
statistical GUE/CUE conjecture about zeros after RH has already supplied the
critical-line ordering. It is not equivalent to RH, and it does not imply RH
without a separate zero-line theorem.

Dichotomy audit:

The step-187 dichotomy classifies typed carriers aimed at closing an
RH-analogous statement. RMT is a statistical evidence/consistency-checking
carrier, not a closure carrier. Therefore it is outside the dichotomy's
strict domain, not a counterexample.

Coverage status:

`dichotomy_coverage_conjecture_status = unchanged_domain_refined`.

The domain refinement is: statistical evidence carriers are separate from
RH-analogous closure carriers.
