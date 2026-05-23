# Step 109: Finite Matrix Moment Lower-Bound Prototype

## Main theorem

Let `R_N:Y_B,N -> C^N` be the boundary coefficient map and let `G_X,N` be the character/mollifier source Gram. If

```math
G_{X,N} \succeq \gamma_N I,\qquad R_N^*R_N \succeq c_NG_{B,N},
```

then

```math
R_N^*G_{X,N}R_N \succeq \gamma_Nc_NG_{B,N}.
```

With defects, `G_X >= gamma I - E_G` and `R^*R >= cG_B - E_R` imply

```math
R^*G_XR \succeq \gamma cG_B-\gamma E_R-R^*E_GR.
```

## Finite toy checks

Boundary dimension: `18`. Coefficient dimension: `72`.

Observable coefficient map constant: `c_N ≈ 0.2304`.

Rank-deficient coefficient map constant: `c_N ≈ -3.16102e-16`.

Full coefficient-frame lower constant: `gamma = 3.2`.

Defect theorem minimum slack: `-7.59957e-15`.

Rank-one scalar-source minimum generalized eigenvalue: `-7.97224e-15`.

## Nonclaim

This is not RH evidence. It is a finite algebraic prototype identifying exactly what arithmetic estimates must supply.
