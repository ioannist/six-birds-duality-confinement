# Step 443 Package Rebuild and A1-A4 Numerics

## P = (M, A_W, R, T)

`M` is the finite native membrane. `A_W` is the Weil hermitian positivity form. `R=Xi_C(D|L)` is computed only for the archimedean/trivial formal restricted branch, because the concrete zero/prime branches are illegal primitives. `T=A_*` is the Schur transport.

## needles.tex Theorem 6.4 cited verbatim

```text
Let A_*:=K_DL K_LL^dagger. Then
K_DD = A_* K_LL A_*^* + Xi_C(D|L).
Moreover Xi_C(D|L)=0 iff exists A with D_0=A L_0 iff Ker L_0 subset Ker D_0.
```

## Matrices

```text
K_LL = diag(1.1, 0.9, 0.65, 0.45)
K_DL = [[0.38,0.16,0.04,0], [0.06,0.31,0.14,0.03], [0.02,0.07,0.27,0.18]]
K_DD = K_DL K_LL^-1 K_DL^T + diag(0.0012,0.0025,0.0064)
```

## A1-A4

- A1 membrane passes: all diagonal `Khat_j <= Theta`.
- A2 propagation passes: `prod(1+epsilon_j) = 1.192464 <= 2`.
- A3 Schur identity max error: `1.3177747429038154030435717564087523759637451727961e-82`.
- Residual eigenvalues: `['0.0012', '0.0025', '0.0064']`.
- `Xi_Z = 0.0064 I`.
- A4 endpoint gap eigenvalues: `['0.005', '0.005', '0.005']`.

## Numerical-status caveat

These numerics verify the formal Loewner/Schur package for the restricted non-arithmetic branch. They do not compute the actual Weil form `W[f]`, because that would require zeros or primes.
