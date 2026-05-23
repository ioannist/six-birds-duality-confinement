# Step 281 Results Summary

## Target

Audit Cattani-Deligne-Kaplan 1995 as a Hodge score-2 bridge candidate for the seven-layer Hodge CTMT chain.

## CDK Theorem Extract

CDK's main theorem is a Hodge-locus algebraicity theorem:

> S(K) is an algebraic variety, finite over S.

Its local consequence is:

> The germ of analytic subvariety of S where u remains of type (0, 0), is algebraic.

Its global consequence is:

> The set of points in S where some determination of u is of type (0, 0), is an algebraic subvariety of S.

Charles-Schnell summarize the same theorem type as algebraicity of Hodge loci:

> the locus of Hodge classes and the Hodge locus ... are countable unions of closed algebraic subsets

## Locus vs Class Distinction

The Hodge cascade needs codimension-2 cycle realization and cycle-class-map closure: a relevant Hodge class must be represented by an algebraic cycle on the fiber.

CDK proves that the parameter locus where a class remains Hodge is algebraic. It does not prove that the class itself is the class of an algebraic cycle. This is the wrong typed object for the cascade closure.

Voisin's target formulation keeps the distinction sharp:

> The Hodge conjecture asserts that any rational Hodge class is a combination with rational coefficients of such classes.

## Derivation Attempt

Starting from CDK's locus theorem, the missing inference would be:

`algebraic Hodge locus -> algebraic cycle realizing the Hodge class on the target fiber`.

No such inference is supplied by CDK. Under the Hodge track source-to-status discipline, this cannot promote to `known_zero` without a source-stated cycle-span theorem.

## Verdict

`V_CDK_Hodge_bridge_blocked`

The CDK bridge candidate downgrades from score-2 to score-1. The empirical score-2 downgrade pattern becomes 5-of-5 across RH, BSD, and Hodge.
