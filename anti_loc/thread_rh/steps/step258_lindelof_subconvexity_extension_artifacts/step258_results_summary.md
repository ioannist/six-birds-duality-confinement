# Step 258 Results Summary

## Lindelof Carrier

For zeta, define

`mu(1/2)=limsup_{T->infty} log|zeta(1/2+iT)|/log T`.

The Lindelof residual is

`Xi_Lindelof(T)=sup_{T'<=T} log|zeta(1/2+iT')|/log T'`.

Closure is `mu(1/2)=0`, equivalently
`zeta(1/2+iT)=O_epsilon(T^epsilon)`.

RH implies Lindelof; the converse is open.

## Subconvexity Family

For `L(s,pi)` with analytic conductor `C(pi)`, convexity gives

`L(1/2,pi) << C(pi)^(1/4+epsilon)`.

Subconvexity means breaking the `1/4` exponent.  Lindelof is the limiting
exponent `0`.

## Classification

Lindelof/subconvexity is not a cross-correlation residual and is not a
zero-location RH analogue.  It is a single-L or automorphic-family
growth-rate residual.  Therefore it is parallel to, not inside, both:

- the Selberg-Class Dichotomy Generalization;
- the Selberg-Class Cross-Correlation Extension.

## Candidate Finding

`Selberg-Class Subconvexity Extension`.

Critical-line growth-rate residuals form a separate typed-condition family:
convexity baseline, subconvexity partial closure, Lindelof exponent-zero
target.

## Evidence

1. Zeta Lindelof / Bourgain 2017: `|zeta(1/2+it)| << t^(13/84+epsilon)`.
2. Burgess Dirichlet subconvexity: `L(1/2,chi) << q^(3/16+epsilon)`.
3. Michel-Venkatesh GL(2): subconvexity for GL1/GL2 automorphic L-functions
   over fixed number fields, uniformly in aspects.

Status: `candidate (verified-on-3-subconvexity-instances) corpus-pending`.

Deposited in `anti_loc/findings_framework.md`.

## Verdict

`V_lindelof_subconvexity_extension`.
