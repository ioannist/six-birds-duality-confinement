# Step 405: BN <-> Branch C Structural Cross-Link

## Inputs Used

- Step 193/195/196 inherited BN/Branch-C context used in substance: Beurling-Nyman approximation error and Branch C Burnol/Sonine matrix-element foreclosure belong to different cascade branches.
- Step 199 used verbatim from the prompt: `d_N^2*log(N) -> 0.0457`.
- Step 366 used verbatim from the prompt: `gamma_zeta ~= pi/(T*log(T/(2pi)))`.

## Báez-Duarte Sum

For zeros `rho_j = 1/2+iT_j`,

```text
1/|rho_j|^2 = 1/(1/4 + T_j^2).
```

The closed-form Báez-Duarte constant is

```text
A = sum_rho 1/|rho|^2 = 2 + gamma_E - log(4*pi)
  = 0.046191417932242067628620495812990583...
```

The first 100 positive zeros contribute

```text
sum_{j=1}^{100} 1/|rho_j|^2
 = 0.019984852403923805300300450226026915...
```

This is only `43.2653%` of the full closed-form value, so the BN constant is
not a low-zero phenomenon.

The cascade empirical value from Step199,

```text
d_N^2 log N ~= 0.0457,
```

differs from the closed form by about `1.06%`.

## Branch-C-Informed Contribution Test

The Branch C structural law

```text
gamma_zeta(T) ~= pi/(T*log(T/(2*pi)))
```

is an inverse local-density scale: the Riemann-von Mangoldt local zero density
is

```text
dN/dT ~= log(T/(2*pi))/(2*pi).
```

Thus `gamma_zeta` contains the reciprocal of the same logarithmic density
factor that governs zero statistics.  This is a real structural overlap.

However, the Báez-Duarte per-zero residue weight is already fixed as

```text
residue_BN(rho) / |rho|^2,
```

and in the closed-form constant the visible height dependence is

```text
1/(1/4+T^2).
```

The Branch C `gamma_zeta(T)` is a decay rate for Burnol/Sonine matrix elements,
not the BN residue.  Without an additional theorem identifying
`residue_BN(rho)` with a Branch-C matrix-element expression, `gamma_zeta` does
not modify the Báez-Duarte constant.

## Tail Comparison

Using density alone, the BN tail has the shape

```text
integral_X^infty [log(T/(2*pi))/(2*pi)] * T^{-2} dT,
```

while the Branch C rate has shape

```text
pi/(T*log(T/(2*pi))).
```

These are reciprocal-density-related but not the same contribution law.

## Verdict

Weak structural cross-link only.

The BN `1/log(N)` scale and Branch C `1/log(T)` factor both reflect the same
Riemann-von Mangoldt local zero-density logarithm.  But Branch C imposes no new
constraint on `d_N^2` beyond the known Báez-Duarte constant unless an additional
bridge theorem identifies BN residues with Branch-C matrix elements.
