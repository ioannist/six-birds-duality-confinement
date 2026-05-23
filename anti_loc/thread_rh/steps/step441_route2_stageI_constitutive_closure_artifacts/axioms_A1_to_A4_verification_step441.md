# Step 441 A1-A4 Verification

All numerical matrix calculations were performed with `mpmath` at `mp.dps = 80`.

## A1 membrane

For all `j=0..4`, `Khat_j <= Theta` by diagonal Loewner comparison.

Minimum diagonal gaps `Theta-Khat_j`:

```text
j=0: 0.05
j=1: 0.04
j=2: 0.035
j=3: 0.03
j=4: 0.025
```

## A2 summable propagation

Epsilon values:

```text
['0.05', '0.05', '0.04', '0.04']
```

Product:

```text
prod_j(1+epsilon_j) = 1.192464 <= 2
```

Additive defects `D_j` are diagonal and nonnegative; `D_infty=sum_j D_j` has diagonal:

```text
['0.0147', '0.0187', '0.0181']
```

## A3 adequacy interface

The Schur identity

```text
K_DD = A_* K_LL A_*^* + Xi_C(D|L)
```

holds with max absolute residual error:

```text
7.90664845742289241826143053845e-82
```

The residual eigenvalues are:

```text
['0.0025', '0.0064', '0.0144']
```

Thus `Xi_C(D|L) >= 0` and `Xi_C(D|L) <= Xi_Z` with `Xi_Z=0.0144 I`.

## A4 layer-dissolving endpoint

With `S=I`, `Theta^Y=K_LL+0.1I`, `Xi^Z=Xi_Z`, and

```text
Theta^D = A_* Theta^Y A_*^* + Xi^Z + 0.01 I,
```

the endpoint gap has eigenvalues:

```text
['0.01', '0.01', '0.01']
```

The capacity bound for `z=e_1` is:

```text
z^* Theta^D z = 0.511025
```

## Verification status

A1-A4 pass for the finite formal package. This does not close Stage I because the audit currency `A` fails to derive the 10 nontrivial zero heights without importing zeta-side data.
