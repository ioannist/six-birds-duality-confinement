# Step 421 Foreclosure Consistency

## Direct Saddle-Point Evaluation

For j=1..15, the saddle was taken in the `real_plus_fixed_Im_sigma_ge_1_2` direction:

```text
z_star(rho_j) = (1/2 + pi/log(T_j/(2*pi))) + i*T_j.
```

This direction keeps `sigma >= 1/2`, matching the side of the strip needed by the Simonic conditional bound.

The direct dps80 product range is:

```text
min |zeta(z*) M(G_star)(z*)| = 0.003285685891524279829666586
max |zeta(z*) M(G_star)(z*)| = 0.02500697854606009602912918
threshold 0.034 comparison: 0/15 products are >= 0.034
```

## Conditional Bound Status

Step 420 inherited Simonic 2024 Theorem 1 / eq (8):

```text
log|zeta(s)| <= 8.45*log(2T)/log log(2T) for sigma >= 1/2, T >= 14694.
```

All first 15 zeta zeros have `T <= 65.12`, so the explicit high-T condition is not met. The table records the formal expression but does not use it as a valid bound in this regime. Direct mpmath evaluation is therefore the operative cross-check.

## Foreclosure Comparison

The cascade foreclosure value `|L_k| >= 0.034` from Step 380 is a lower-bound statement about the projected/raw Branch C evaluator cells. The Simonic inequality is an upper bound for `|zeta|`, and the evaluated saddle product is not a lower bound for `|L_k|`. Since every evaluated product is below `0.034`, this route cannot conditionally complete Stage V foreclosure.

## Verdict

The calculation is consistent as a scale diagnostic, but it does not prove or conditionally complete the foreclosure threshold. The empirical cascade foreclosure remains stronger/different from what the Simonic + Mellin saddle product supplies at j=1..15.

## Verbatim Step Anchors

- Step 196: `G_star` is the `Step 174/175 base generator`.
- Step 220: `Phi_max = 0.4904766190 at (sigma, ell) = (0.35, 2.0)`.
- Step 292: `delta_Dk(rho, G) = (zeta * M(G))^(k)(rho)`.
- Step 366: `gamma_zeta approx pi/(T*log(T/(2pi)))`.
- Step 380: `|L_k| >= 0.034`.
- Step 420: `log|zeta(s)| <= 8.45*log(2T)/log log(2T)`.
