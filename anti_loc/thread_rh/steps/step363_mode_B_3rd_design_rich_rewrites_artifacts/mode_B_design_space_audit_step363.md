# Mode B Design Space Audit: Three Attempts

## Attempt 1: U^flat, Step 356/358

- States: 5 (`a,b,c,d,e`).
- Transfer class: scalar and affine-log character forms.
- Stage III: under-fit at training.
- Training RMSE: 1.2174 for scalar, 1.3486 for affine-log.

## Attempt 2: U^flat-prime, Step 361

- States: 8 (`a,b,c,d,e,f,g,h`).
- Transfer class: character-indexed affine-log magnitude and linear phase.
- Training RMSE(lambda_total): 0.2658.
- Holdout RMSE: rho_2 = 1.9827, rho_3 = 2.5350.

## Attempt 3: U^flat-double-prime, Step 363

- States: 4 (`alpha,beta,gamma,delta`).
- Transfer class: rich per-character polynomial rewrites on magnitude and phase.
- Training RMSE(lambda_total): 0.1558010988527524.
- Holdout RMSE: rho_2 = 1.973439189878534, rho_3 = 2.525160108522078.

## Design-Space Evidence

The three attempts vary different axes:

- state count low/medium/high: 4, 5, 8;
- state granularity: separate atoms vs composite atoms;
- rewrite expressivity: scalar, affine-log, affine-log plus phase, polynomial magnitude/phase.

All retract at Stage III.  The third design shows that adding rewrite expressivity improves in-sample fit but does not create cross-rho robustness or an operator certificate.
