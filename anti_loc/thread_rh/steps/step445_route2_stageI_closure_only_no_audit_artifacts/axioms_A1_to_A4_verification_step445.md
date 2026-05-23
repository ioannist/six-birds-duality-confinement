# Step 445 A1-A4 Verification

All numerics use `mpmath` with `mp.dps=80`.

## A1

`K^L_j <= Theta^Y` for all `j=0..4`. Minimum final diagonal gap: `0.022`.

## A2

`epsilon = ['0.05', '0.05', '0.04', '0.04']` and `prod(1+epsilon_j) = 1.192464 <= 2`.

## A3

Schur identity max absolute error:

```text
1.3177747429038154030435717564087523759637451727961e-82
```

`Xi` eigenvalues:

```text
['0.0007', '0.0018', '0.0036']
```

Thus `Xi_Z = 0.0036 I`.

## A4

Target package gap eigenvalues for `Theta^D - S K^D S^*`:

```text
['0.004', '0.004', '0.004']
```

Control off-critical package gap eigenvalues under same `Theta^D`:

```text
['-0.021392', '-0.013672', '-0.005216']
```

The constructed control fails the capacity bound numerically. The semantic issue remains: the target/control distinction is only a formal matrix distinction unless `D` and `Theta^D` are independently tied to zero-localization without an implicit audit.
