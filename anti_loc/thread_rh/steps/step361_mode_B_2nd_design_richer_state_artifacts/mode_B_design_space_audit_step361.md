# Mode B Design Space Audit: U^flat vs U^flat-prime

## Baseline U^flat (Steps 356-359)

State set: {a,b,c,d,e}.

Stage III outcome:

- tau_character_scalar training RMSE: 1.2174; holdout rho_2: 1.6258; holdout rho_3: 2.5367.
- tau_character_affine_log training RMSE: 1.3486; holdout rho_2: 1.2269; holdout rho_3: 3.0039.

Failure pattern: under-fit already at training, plus missing operator certificate.

## Richer U^flat-prime (Step 361)

State set: {a,b,c,d,e,f,g,h}.

Added states:

- f: operator-realization atom.
- g: phase-bound atom.
- h: transfer-witness atom.

Stage III candidate: character-indexed affine-log magnitude plus linear phase correction.

Summary:

- rho_1 training lambda_total RMSE: 0.2657549597854174.
- rho_2 holdout lambda_total RMSE: 1.982740773308652.
- rho_3 holdout lambda_total RMSE: 2.534982204826251.

## Audit Conclusion

U^flat-prime is genuinely different from U^flat because it separates phase-bound and operator-realization atoms and expands the transfer family from scalar/affine forms to a 28-parameter state-indexed magnitude/phase rule.

It improves the baseline under-fit but does not close Stage III.  The richer design shifts the failure pattern toward over-parameterized in-sample improvement with holdout failure and still lacks an external operator-compatibility certificate.
