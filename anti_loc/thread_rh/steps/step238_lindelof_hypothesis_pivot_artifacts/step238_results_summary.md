# Step 238 Results Summary

## Carrier Declaration

The Lindelof carrier is the growth residual of the Riemann zeta function on the critical line:

```text
Xi_Lindelof = limsup_{t -> infinity} log |zeta(1/2 + i t)| / log t.
```

Closure is `Xi_Lindelof = 0`, equivalently `|zeta(1/2 + it)| = O_epsilon(t^epsilon)` for every `epsilon > 0`.

## Relation To RH

RH implies Lindelof by the standard convexity / Phragmen-Lindelof consequences of zero control, but the reverse implication is not an accepted theorem. Lindelof is therefore treated in this cascade as a strictly weaker sub-target: its closure is not an RH closure.

## Current Analytic Status

Lindelof remains open. The strongest pointwise subconvexity exponent found in this audit is Bourgain's

```text
zeta(1/2 + it) <<_epsilon t^(13/84 + epsilon).
```

This improves the classical Weyl/Hardy-Littlewood style exponents but is still far from exponent `0`.

## Density / Zero-Count Form

Backlund's short-interval zero-count condition is recorded as Lindelof-equivalent: for every `sigma > 1/2`, zeros in `T <= Im(s) <= T+1`, `sigma <= Re(s) <= 1`, grow slower than `log T`.

The broader density hypothesis belongs to the same Lindelof-family of zero-density statements and is Lindelof-implied in the audited sources. This step does not use it as an unqualified RH-equivalent bridge.

## Classification

- Under the Riemann-RH Dichotomy: outside scope, because Lindelof is not RH-equivalent.
- Under the generalized "zeta sub-conjecture" Dichotomy: generalized CRCFT-TE within the Lindelof family, because closing the residual is exactly the Lindelof hypothesis.

## Verdict

`V_lindelof_outside_dichotomy_sub_conjecture`

The carrier is substantively distinct from RH-equivalent carriers: it is weaker than RH, open, and target-equivalent only to its own Lindelof sub-target.
