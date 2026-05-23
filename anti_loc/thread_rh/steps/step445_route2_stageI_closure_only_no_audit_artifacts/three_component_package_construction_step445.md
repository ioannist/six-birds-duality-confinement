# Step 445 Three-Component Package Construction

## needles.tex citations

Sec. 575 adequacy interface:

```text
Let A_*:=K_DL K_LL^dagger. Then K_DD=A_*K_LL A_*^*+Xi_C(D|L).
```

Sec. 738 predictive native membranes:

```text
A native predictive membrane with budget Theta is the bound Khat_j <= Theta for every accepted stage j.
```

Sec. 875 layer-dissolving endpoint:

```text
If K^L_j <= Theta^Y_j, Xi_j <= Xi^Z_j, and
S_j(A_j Theta^Y_j A_j^*+Xi^Z_j)S_j^* <= Theta^D,
then S_j K^D_j S_j^* <= Theta^D.
```

NDO/SAU certificate shape:

```text
[U not_down_q, C(U) down_B a^sharp]
```

## K^L

Stages `j=0..4` use diagonal `K^L_j`; all satisfy `K^L_j <= Theta^Y` with `Theta^Y=diag(0.25,0.16,0.08)`. Propagation product is `1.192464`.

## Xi

```text
K_LL = diag(1.0,0.85,0.70,0.55)
K_DL = [[0.34,0.12,0.05,0], [0.04,0.29,0.12,0.04], [0,0.06,0.25,0.20]]
Xi = diag(0.0007,0.0018,0.0036)
```

`K^D = K_DL K_LL^-1 K_DL^T + Xi`; `A_*=K_DL K_LL^dagger`.

## K^D and S

`S=diag(0.96,0.94,0.92)`. `Theta^D` is chosen as `S K^D S^* + 0.004 I` for the formal target package, so the formal capacity bound passes.

## Primitive set

Finite matrices, Loewner order, Schur identity, Moore-Penrose pseudoinverse, gamma-factor metadata, functional-equation symmetry marker, conductor 1, finite native/dissolving probe labels. No zeta-values, prime sums, modular forms, adeles, Euler product, or L-special values are used.
