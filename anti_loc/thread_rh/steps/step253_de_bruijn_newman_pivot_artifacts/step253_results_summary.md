# Step 253 Results Summary

## Carrier Declaration

For real `t`, define the heat-flow deformation

`H_t(z) = integral_0^infty exp(t u^2) Phi(u) cos(z u) du`,

where

`Phi(u) = sum_{n>=1} (2*pi^2*n^4*exp(9u) - 3*pi*n^2*exp(5u)) exp(-pi*n^2 exp(4u))`.

The de Bruijn-Newman constant is

`Lambda = inf{t in R : H_t has only real zeros}`.

Equivalently, in the older normalization, this is the heat-flow deformation of
Riemann's xi function on the critical line.

## CRE Audit

de Bruijn's 1950 work supplies the heat-flow real-zero persistence structure.
Newman's 1976 work supplies the finite threshold constant and the conjecture
`Lambda >= 0`.

The Riemann Hypothesis is equivalent to `Lambda <= 0`.  Rodgers-Tao 2018
proved `Lambda >= 0`; therefore the remaining closure is exactly
`Lambda = 0`, target-equivalent to RH.

CRE status: `CRE`.

## CRCFT Mode

Mode: `CRCFT-TE`.

Reason: closing the carrier residual is precisely the target-equivalent
assertion `Lambda <= 0`, now equivalently `Lambda = 0` after Rodgers-Tao.
The heat-flow carrier is structurally distinct from Burnol/Sonine, but no
bridge is required for classification because the target-equivalence is direct.

## Bound Status

- de Bruijn 1950: real-zero heat-flow persistence.
- Newman 1976: finite threshold `Lambda` and conjecture `Lambda >= 0`.
- Rodgers-Tao 2018: `Lambda >= 0`.
- Polymath15 2019: unconditional `Lambda <= 0.22`.

## Verdict

`V_de_Bruijn_Newman_CRCFT_TE`.

The de Bruijn-Newman constant is a new CRE carrier in TE mode and a 20th
carrier classification in the running Dichotomy survey.  No RH closure is
claimed.
