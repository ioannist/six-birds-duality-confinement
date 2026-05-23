# Step 275 Results Summary — QUE Classification

## Carrier Declaration

Quantum Unique Ergodicity (QUE) for arithmetic Hecke-Maass cusp forms is represented by the mass-equidistribution residual
\[
\Xi_{\mathrm{QUE}}(j;f)=\left|\int_{\Gamma\backslash\mathbb H} f(z)|\phi_j(z)|^2\,d\mathrm{vol}(z)
-\frac{1}{\mathrm{vol}(\Gamma\backslash\mathbb H)}\int_{\Gamma\backslash\mathbb H}f(z)\,d\mathrm{vol}(z)\right|.
\]
Closure is \(\Xi_{\mathrm{QUE}}(j;f)\to 0\) for every continuous test function \(f\) as \(t_j\to\infty\).

## Classification

Verdict: `V_que_in_subconvexity`.

Primary classification: **Selberg-Class Subconvexity Extension, Type alpha**.  Watson's triple-product bridge converts quantitative QUE periods / matrix coefficients such as \(\int \phi_j^2\psi\) into central triple-product \(L\)-values, equivalently central values of the shape \(L(1/2,\operatorname{sym}^2\phi_j\times\psi)\) up to local factors and normalization.  Thus the arithmetic route from QUE to effective estimates is a central-\(L\)-value size problem, not a new framework family.

Secondary classification: **Cross-Correlation Extension, Type Ia correlation shadow**.  The residual itself is a correlation between the mass \(|\phi_j|^2\) and a test observable \(f\), but the decisive arithmetic bridge is subconvexity.

Excluded: SCDG.  QUE is not a per-\(L\)-function RH-analog or zero-location residual.  No 11th candidate framework finding is needed.

## Literature Audit

- Rudnick-Sarnak 1994: `The behaviour of eigenstates of arithmetic hyperbolic manifolds`.
- Watson 2002: `Rankin Triple Products and Quantum Chaos`; triple-product formulas relate periods to central \(L\)-values.
- Lindenstrauss 2006: `Invariant measures and arithmetic quantum unique ergodicity`.
- Soundararajan 2010: `Quantum unique ergodicity for SL2(Z)\H`; eliminates escape of mass for Hecke-Maass forms on the modular surface.
- Holowinsky-Soundararajan 2010: `Mass equidistribution for Hecke eigenforms`.

## Status Update

`anti_loc/findings_framework.md` was updated to add QUE as a Type alpha subconvexity-bridge instance and as a secondary Cross-Correlation Type Ia note.  Arithmetic QUE in the cited Hecke settings is proved, but general non-arithmetic QUE remains open; no RH/GRH consequence is claimed.

## Artifacts

Artifacts are deposited at:
`/home/repos/six-birds-foundations-iii/anti_loc/thread/steps/step275_QUE_classification_artifacts/`.
