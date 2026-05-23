# Mode B Four-Design Space Summary

## U^flat: 5-state design

- Framing: state/rewrite carrier.
- Stage III: under-fit at training.
- Training RMSE: 1.22; holdout rho_2: 1.63.

## U^flat-prime: 8-state design

- Framing: richer state carrier with operator and phase atoms.
- Stage III: improved training but holdout failure.
- Training RMSE: 0.27; holdout rho_2: 1.97.

## U^flat-double-prime: 4-state rich-rewrite design

- Framing: fewer states, richer per-state rewrites.
- Stage III: best in-sample among state designs; holdout failure.
- Training RMSE: 0.16; holdout rho_2: 1.97.

## U^flat_G: graph-based design

- Framing: finite labeled graph, path predicates, edge-label weights.
- Stage III training RMSE(lambda_total): 1.764253290788628.
- Holdout rho_2 RMSE(lambda_total): 2.122900424929048.
- Holdout rho_3 RMSE(lambda_total): 2.347972116925062.

## Reach-Boundary Evidence

Four structurally distinct Mode B attempts now fail Stage III:

1. state-count medium, simple rewrites;
2. state-count high, dedicated operator/phase atoms;
3. state-count low, rich rewrites;
4. graph/path-predicate framing.

This is strong empirical reach-boundary evidence across the declared finite design span, not a theorem of impossibility.
