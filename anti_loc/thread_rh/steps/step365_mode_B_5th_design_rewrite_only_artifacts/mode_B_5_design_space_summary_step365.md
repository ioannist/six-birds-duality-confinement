# Mode B Five-Design Space Summary

1. U^flat: 5-state carrier; training 1.22, holdout 1.63.
2. U^flat-prime: 8-state carrier; training 0.27, holdout 1.97.
3. U^flat-double-prime: 4-state rich rewrite carrier; training 0.16, holdout 1.97.
4. U^flat_G: graph/path-predicate carrier; training 1.76, holdout 2.12.
5. U^flat_R: rewrite-system-only term algebra; training 1.727684439025268, holdout rho_2 2.212545328283977, holdout rho_3 2.374234560617829.

## Reach-Boundary Status

The fifth attempt removes explicit states and graph nodes entirely.  Its primitives are terms and rewrite normal forms.

It also retracts at Stage III.  The accumulated evidence now spans:

- state-based carriers;
- graph/path-predicate carriers;
- rewrite-system-only carriers.

This strongly supports the diagnosis that the H6 obstruction is not an artifact of explicit state structure.  It is still empirical design-space evidence, not a theorem over all Mode B carriers.
