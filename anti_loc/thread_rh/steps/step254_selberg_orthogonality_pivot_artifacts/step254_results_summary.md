# Step 254 Results Summary

## SOC Carrier Declaration

For distinct primitive Selberg-class L-functions `L1 != L2`, with prime
Dirichlet coefficients `a_p(L_i)`, Selberg orthogonality asks for

`(1/log log x) sum_{p<=x} a_p(L1) conjugate(a_p(L2))/p -> 0`.

The residual carrier is

`Xi_SOC = limsup_x |sum_{p<=x} a_p(L1) conjugate(a_p(L2))/p| / log log x`.

Closure means `Xi_SOC = 0` for every distinct primitive pair.

## SOC vs GRH

SOC is not Riemann-RH-equivalent.  It is a coefficient cross-correlation
statement across distinct primitive L-functions, not a zero-location statement
for `zeta(s)`.

It is also not the same as individual GRH for one Selberg-class L-function.
GRH-type assumptions plus Selberg-class structural/decomposition input are a
standard route to SOC, but the converse is not an audited equivalence.

## Classification

Under the Riemann-RH Dichotomy: outside scope.

Under the Selberg-Class Dichotomy Generalization from step 232: still outside
the single-L-function RH-analogue scope, because SOC is a cross-L-function
correlation condition.

SOC suggests a separate candidate extension:

`Selberg-class cross-correlation extension`: meta-carriers whose residuals
measure correlations between distinct primitive L-functions rather than the
RH-analogue of a single L-function.

## Literature Audit

- Selberg 1989/1992: original Selberg-class conjectural framework.
- Conrey-Ghosh 1993: Selberg class axioms and small-degree structure.
- Murty 1994: review of Selberg's conjectures and Artin L-functions.
- Kaczorowski-Perelli 1999/2011: Selberg-class surveys and structural program.

## Verdict

`V_selberg_orthogonality_outside_dichotomy`.

This is a 21st carrier classification, but not a new Riemann-RH CRE carrier.
It is a cross-correlation carrier outside both the Riemann Dichotomy and the
single-L Selberg-class extension.
