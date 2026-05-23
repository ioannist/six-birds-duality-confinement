
# Step 107 — Heap--Soundararajan operator-valued lift test

This step tests whether the Heap--Soundararajan dual mollifier mechanism can be promoted from scalar lower-moment strength to the operator-valued lower frame needed by the boundary-packet source route.

## Verdict

The scalar mechanism is a strong template, but it is not yet an operator lower frame.

A single positive mollifier direction can have large scalar strength while the associated source matrix is rank one. Therefore it cannot charge every recombination in the Burnol/Sonine boundary sector.

The accepted lift would require a matrix moment theorem:

```math
F_n=\sum_{\omega\in\mathcal X_n}\lambda_{\omega,n}Q_\omega^*\Theta_\omega^{-1}Q_\omega
\succeq \Lambda_n(\Theta_0^-)^{-1},\qquad \Lambda_n\to\infty .
```

The Heap--Soundararajan proof supplies the scalar prototype for the growth of `Lambda_n`; finite character orthogonality supplies the local tight-frame mechanism. The missing work is the uniform operator-valued lift on the completed boundary-packet carrier.

## Key no-go

A scalar lower bound on one chosen mollifier vector does not imply a lower frame. In finite dimensions,

```math
F=a a^*
```

has positive value on `a`, but zero minimum eigenvalue on every dimension greater than one.

## What would work

A family of mollifiers/source readouts whose coefficient vectors span the boundary model, with matrix moment asymptotics proving a uniform lower eigenvalue.

## Next target

Build a concrete finite Burnol/Sonine boundary dictionary and define the coefficient map `R_N` so that the operator-valued moment problem becomes explicit.
