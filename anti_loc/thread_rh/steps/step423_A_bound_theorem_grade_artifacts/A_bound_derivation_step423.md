# Step 423 Analytic A(rho) Bound Derivation

## Target

Step 422 verified the exact dominance criterion on 46 cells:

```text
Re L''(rho) >= 0 iff B(rho)>0 and |B(rho)|>|A(rho)|.
```

This step attempts to replace the measured `|A(rho)|` with an analytic upper bound.

## Archimedean Bound

For conductor `q` and parity `a`, use

```text
|arch'(rho)| <= 0.5*|log(pi/q)| + 0.5*log(max(2,(T+a+2)/2))
```

with the zeta pole correction `+1/T+1/max(T,1)` for `zeta`. This is the explicit version of the digamma asymptotic `psi((rho+a)/2)=log(T/2)+O(1/T)`.

## Far-Zero Remainder Bound

Let

```text
Lambda = log(qT/(2*pi)).
```

The tested coarse Riemann-von-Mangoldt/Baez-Duarte envelope is

```text
|g'_rest(rho)| <= C_RvM*Lambda^2 + |Lambda| + C_BD,
C_RvM = 1, C_BD = 0.0462.
```

Step 405 anchor: `d_N^2 log(N) -> 0.0457` and `sum_rho 1/|rho|^2 approx 0.0462`.

## Combined Bound

Formally,

```text
|A(rho)| <= 2 |L'(rho)| ( |arch'(rho)| + |g'_rest(rho)| ).
```

Using the close-pair scale `|B| ~ 2|L'|/s_min` gives the structural sufficient condition

```text
s_min < 2/(K*log^2(qT/(2*pi))).
```

For the conservative audit constant `K=4`, the spacing condition is far too restrictive.

## Verbatim Step Anchors

- Step 422: `Re L''(rho) >= 0 iff B(rho) > 0 and |B(rho)| > |A(rho)|`.
- Step 381: `L''(rho) = 2L'(rho)*g'(rho)`.
- Step 405: `d_N^2*log(N) -> 0.0457` and `0.0462`.
