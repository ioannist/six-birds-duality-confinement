# Step 282 Results Summary

## Target

Audit Beale-Kato-Majda 1984 as a Navier-Stokes score-2 bridge candidate for the EXT2-4 BKM/BG time-gate in the NS 10-layer CTMT chain.

## BKM Statement Extract

The Springer/Duke article records the BKM result as:

> maximum norm of the vorticity controls the breakdown of smooth solutions

The continuation direction is:

> if the vorticity remains bounded, a smooth solution persists

In the standard BKM formulation, continuation is tied to:

> integral_0^T ||omega(t)||_{L^infty} dt < infinity

and breakdown to:

> integral_0^T* ||omega(t)||_{L^infty} dt = infinity

## Criterion vs Closure

The NS cascade needs global time-gate closure: either a proof that the relevant vorticity integral remains finite for all time, or a proof that it diverges in a target-class blowup construction.

BKM supplies a continuation/blowup criterion. It identifies the exact quantity that must be controlled, but it does not control it. Therefore BKM exposes the EXT2-4 terminal obligation rather than closing it.

## Derivation Attempt

The attempted derivation would need:

`BKM criterion + independent estimate -> global regularity / target closure`.

BKM supplies only the first factor. The independent estimate on
`int ||omega||_{L^infty} dt`
is not in BKM.

## Verdict

`V_BKM_NS_bridge_blocked`

BKM downgrades from score-2 to score-1 for the NS cascade. The empirical score-2 downgrade pattern is now 6-of-6 across RH, BSD, Hodge, and NS.
