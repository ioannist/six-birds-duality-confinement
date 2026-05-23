# Step 442 Package Rebuild and A1-A4 Numerics

## P = (M, A_pos, R, T)

`M` remains a finite predictive native membrane, but `A` is replaced by `A_pos`, a de Branges-style positivity-form audit object.

## Needles theorem cited

From `needles.tex` Theorem 6.4 / adequacy interface:

```text
Let A_*:=K_DL K_LL^dagger. Then
K_DD = A_* K_LL A_*^* + Xi_C(D|L).
Moreover Xi_C(D|L)=0 iff exists A with D_0=A L_0 iff Ker L_0 subset Ker D_0.
```

## Matrices

```text
K_LL = diag(1.2, 1.0, 0.7, 0.5)
K_DL = [[0.42,0.18,0.05,0], [0.05,0.36,0.16,0.04], [0,0.08,0.30,0.22]]
K_DD = K_DL K_LL^-1 K_DL^T + diag(0.0009,0.0016,0.0049)
```

`T=A_*=K_DL K_LL^dagger`.

## A1 membrane

`Khat_j <= Theta` for `j=0..4`; the smallest final diagonal gap is `0.022`.

## A2 propagation

`epsilon = ['0.06', '0.05', '0.04', '0.04']` and `prod(1+epsilon_j) = 1.2038208 <= 2`.

`D_infty` diagonal is `['0.01617', '0.01364', '0.01486']`.

## A3 adequacy interface

Schur identity max absolute error:

```text
1.4824965857667923284240182259598464229592133193956e-82
```

Residual eigenvalues:

```text
['0.0009', '0.0016', '0.0049']
```

Thus `Xi_Z = 0.0049 I`.

## A4 endpoint

With `S=I`, `Theta^Y=K_LL+0.05I`, `Xi^Z=Xi_Z`, and `Theta^D=A_*Theta^Y A_*^*+Xi^Z+0.006I`, the endpoint gap eigenvalues are:

```text
['0.006', '0.006', '0.006']
```

## Package verdict

A1-A4 pass numerically for the rebuilt formal package. Stage I still retracts because `A_pos` positivity for `E_xi` is not derived from declared primitives.
